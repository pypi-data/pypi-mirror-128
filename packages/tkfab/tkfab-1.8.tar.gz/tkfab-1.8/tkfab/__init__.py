# -*- coding:utf-8 -*-
# ========================================
# Author: Chris.Huang
# Mail: Chris.Huang@batechworks.com
# Data: 2021/8/5
# ========================================
from functools import lru_cache
from collections import Counter
from fabric.api import *
from fabric.state import _AttributeDict
from collections import namedtuple
from configparser import ConfigParser
import os.path as osp
import site
import shutil
import logging
import re
import os
import warnings

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s [line:%(lineno)d] %(levelname)s %(message)s',
    datefmt='%a, %d %b %Y %H:%M:%S'
)

# ==============================  SETTING ===============================
env.ape = _AttributeDict()
env.ape.pip_update = True
env.ape.pip_default_file = 'requirements.txt'
env.ape.pip_install_with_user = True
env.ape.allure_patch = False
# =======================================================================


# ==============================  DEFINITION ============================
FAB_PATH = osp.abspath(os.getcwd())
c = Counter()
Repo = namedtuple('Repo', 'url module target')
REPO_LIST = []  # type: list[Repo]
REPO_DICT = {}  # type: dict[Repo.module:abs_join(Repo.target,Repo.module)]


# =======================================================================


def new_idx():
    c.update('i')
    return c.get('i')


def abs_join(*args):
    return osp.abspath(osp.join(*args))


@lru_cache
def get_site_packages():
    if site.ENABLE_USER_SITE:
        logging.debug('enable user sitepackages')
        site_pkg = site.getusersitepackages()
    else:
        site_pkg = site.getsitepackages()[0]
    logging.debug(f'sitepackages: {site_pkg}')
    return site_pkg


@lru_cache
def get_origin_repo_name() -> str:
    repo_name = osp.basename(osp.abspath(osp.join(os.getcwd())))
    logging.debug(f'origin repo name:{repo_name}')
    return repo_name.strip()


@lru_cache
def get_origin_url() -> str:
    def _get_url(config_path):
        cp = ConfigParser()
        cp.read(config_path)
        url = cp.get('remote "origin"', 'url')
        logging.debug(f'origin repo url:{url}')
        return url

    try:
        return _get_url('.git/config')
    except Exception as e:
        return _get_url('config')


# def repo_url_join(*_paths, **kwargs):
#     _paths = list(_paths)
#     if len(_paths) >= 1:
#         pattern = r'(http|https):\/\/'
#         baseurl = _paths[0]
#         _paths[0] = re.sub(pattern, '', baseurl)
#
#     _url = '/'.join(_paths)
#     token = kwargs.get('token', None)
#     if token is None:
#         repo_url = f'https://{_url}.git'
#     else:
#         repo_url = f'https://{token}@{_url}.git'
#     return repo_url


@lru_cache
def repo_url_join(repo_name):
    ori_repo_name = get_origin_repo_name()
    logging.debug(f'ori_repo_name:{ori_repo_name}')
    logging.debug(f'new_repo_name:{repo_name}')
    url = get_origin_url()
    new_url = url.replace(ori_repo_name, repo_name)
    logging.debug(f'ori_url:{url}')
    logging.debug(f'new_url:{new_url}')
    assert url != new_url, 'invalid repo url'
    return new_url


def register_repo(repo_name: str, module: str, target=None):
    url = repo_url_join(repo_name.strip())
    if not target:
        target = get_site_packages()
    repo = Repo(url, module.strip(), target)
    REPO_LIST.append(repo)
    REPO_DICT.__setitem__(module, abs_join(target, module))


@task
def pip():
    cmd = [
        'pip',
        'install',
        '-r',
        env.ape.pip_default_file
    ]
    if env.ape.pip_install_with_user:
        cmd.append('--user')
    local(' '.join(cmd))


@task
def pytest():
    with warn_only():
        local(f'pytest -s -q --alluredir=report')
        local(f'allure serve report -p 8888')


def git_clone(repo, module, target, branch='master'):
    idx = new_idx()
    logging.debug(f'repo = {repo}')
    logging.debug(f'module = {module}')
    repo_target = abs_join(FAB_PATH, f'tmp/{idx}')
    local(f'git clone -v {repo} {repo_target} -b {branch}')
    dst_path = abs_join(target, module)
    logging.debug(f'dst = {dst_path}')
    if osp.exists(dst_path):
        shutil.rmtree(dst_path)
        logging.debug(f'rmtree {dst_path}')
    src_path = abs_join(repo_target, module)
    shutil.copytree(src_path, dst_path)
    logging.debug(f'{src_path} --> {dst_path}')


def rm_dir(_path):
    if osp.exists(_path):
        shutil.rmtree(_path)


def rm_dir_tmp():
    tmp_path = abs_join(FAB_PATH, 'tmp')
    rm_dir(tmp_path)


@task
def patch_allure():
    if not env.ape.allure_patch:
        return
    src = osp.join(get_site_packages(), 'tkfab', 'allure_pytest_listener.txt')
    dst = osp.join(get_site_packages(), 'allure_pytest', 'listener.py')
    shutil.copy(src, dst)


def _pkg_off():
    for repo in REPO_LIST:
        rm_dir(osp.join(repo.target, repo.module))
    rm_dir_tmp()


def _pkg_on():
    for repo in REPO_LIST:
        git_clone(*repo)
    patch_allure()
    rm_dir_tmp()


@task
def pkg(flag: str = 'on'):
    if flag == 'on':
        _pkg_off()
        _pkg_on()
    elif flag == 'off':
        _pkg_off()


def _clb(module, branch):
    new_repo = list()
    for repo in REPO_LIST:
        if repo.module == module:
            new_repo = list(repo)
            new_repo.append(branch)
            break
        else:
            continue
    if not new_repo:
        raise ValueError(f'module "{module}" has not be registered in fabfile.py')
    git_clone(*new_repo)
    logging.critical(f'module "{module}" has been cloned to local with branch "{branch}"')
    patch_allure()
    rm_dir_tmp()


@task
def clb(repo: str, branch: str = 'master'):
    _clb(repo, branch)
