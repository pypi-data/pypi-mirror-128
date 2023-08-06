#!/usr/bin/env python
#coding: utf-8
#by yangbin at 2018.11.28

from __future__ import print_function
import os
import sys
import json
import time

from .helper import IS_PY3, is_macos
from .conf import *
from .m2c import swaggerhtml
if M2C_VERSION == 'v3':
    from .m2c import goswagger3 as goswagger
elif M2C_VERSION == 'v4':
    from .m2c import goswagger3 as goswagger
else:
    from .m2c import goswagger

# amd64 only
os.environ.update({
    "CGO_ENABLED": "0",
    "GOARCH": "amd64"
})

# auto gen build details
date = time.strftime('%Y%m%d', time.localtime())
head = os.popen('git rev-parse HEAD').read().strip()
ldflags = " ".join([
    '-extldflags -static',
    '-X main.BuildDate=%s' %  date,
    '-X main.BuildGitHash=%s' % head
])

def _get_version():
    return head[:6]

def _get_name():
    return json.loads(open(M2C_PATH).read())['name']


def _get_logdir():
    name = _get_name()
    return os.path.join(LOG_HOME, name)


def _run(cmd):
    print('running: %s' % cmd)
    code = os.system(cmd)
    if code != 0:
        print(Color.red('run: %s failed' % cmd))
    else:
        print(Color.green('run: %s success' % cmd))


def version():
    print(_get_version())


def name():
    print(_get_name())


def build():
    os.chdir(GOPHER_DIR)
    app = os.path.join(BUILD_DIST, _get_name())
    cmds = [
        'mkdir -p %s' % BUILD_DIST,
        'go mod vendor',
        'go build -mod=vendor -ldflags "%s" -o %s .' % (ldflags, app),
    ]
    list(map(_run, cmds))
    print('Done')


def build_linux():
    os.environ.update({
        "GOOS": "linux",
    })
    os.chdir(GOPHER_DIR)
    app = os.path.join(BUILD_DIST, _get_name())
    cmds = [
        'mkdir -p %s' % BUILD_DIST,
        'go mod vendor',
        'go build -mod=vendor -ldflags "%s" -o %s .' % (ldflags, app),
    ]
    list(map(_run, cmds))
    print('Done')


def pack(env='dev', goos='linux'):
    os.environ.update({
        "GOOS": goos,
    })
    build()
    name = _get_name()
    version = _get_version()
    dist = os.path.join(BUILD_DIST, '%s-%s.tar.gz' % (name, version))
    cfg = os.path.join(GOPHER_DIR, 'config', '%s.yaml' % env)
    os.system('cp %s %s' % (cfg, BUILD_DIST))
    files = " ".join([name, '%s.yaml' % env])

    os.chdir(BUILD_DIST)
    cmds = [
        'tar -zcf %s %s' % (dist, files)
    ]
    list(map(_run, cmds))

    print('name: %s' % name)
    print('version: %s' % version)
    print('pack: %s' %  dist)

def packsrc():
    name = _get_name()
    version = _get_version()
    dist = os.path.join('dist', '%s-%s-src.tar.gz' % (name, version))

    cmds = [
        'tar -zcf %s %s' % (dist, 'gopher')
    ]
    map(_run, cmds)

    print('name: %s' % name)
    print('version: %s' % version)
    print('pack: %s' %  dist)


def clean():
    os.system('rm -rf dist/*')


def unittest():
    os.chdir(GOPHER_DIR)
    cmds = [
        'cd test/ && docker-compose run --rm unittest'
    ]
    map(_run, cmds)
    print('Done')
    

def supervisor_conf(apphome='/data/app', env='dev'):
    conf = '''
[program:{APPNAME}]
directory={APPHOME}
command={APPBIN_PATH} -c {APPCONF_PATH}
autostart=true
autorestart=true
stdout_logfile={STDOUT_LOG_PATH}
stdout_logfile_maxbytes=50M
stderr_logfile={STDERR_LOG_PATH}
stderr_logfile_maxbytes=50M'''
    appname = _get_name()
    apphome = os.path.join(apphome, appname)
    appbin_path = os.path.join(apphome, appname)
    appconf_path = os.path.join(apphome, '%s.yaml' % env)
    logdir = _get_logdir()
    if not os.path.isabs(logdir):
        if logdir.startswith('./'):
            logdir = logdir.lstrip('./')
        logdir = os.path.join(apphome, logdir)
    stdout_log_path = os.path.join(logdir, '%s_stdout.log' % appname)
    stderr_log_path = os.path.join(logdir, '%s_stderr.log' % appname)
    print(conf.format(**{
        "APPNAME": appname, 
        "APPHOME": apphome, 
        "APPBIN_PATH": appbin_path, 
        "APPCONF_PATH": appconf_path,
        "STDOUT_LOG_PATH": stdout_log_path,
        "STDERR_LOG_PATH": stderr_log_path,
    }))


def run(*args):
    goswagger()
    vendor()
    from .watchgo import WatchGo
    os.chdir(GOPHER_DIR)
    command = ['go', 'run', '.']
    if args:
        command.extend(args)
    WatchGo(command, GOPHER_DIR).start_watch()

def debug():
    os.chdir(GOPHER_DIR)
    os.system('dlv debug .')

def vendor():
    os.chdir(GOPHER_DIR)
    os.system('go mod vendor')

def swaggerCodegen(lang, outputDir, pkg='', swaggerYamlPath=SWAGGER_YAML_PATH):
    if os.system('which swagger-codegen') != 0:
        print(Color.red('swagger-codgen 不存在, 安装参考: https://github.com/swagger-api/swagger-codegen'))
        if is_macos():
            print(Color.green('当前为macos 自动执行安装中...'))
            _run('brew install swagger-codegen')
        return
    if pkg == '':
        _run('swagger-codegen generate -i %s -l %s -o %s' % (swaggerYamlPath, lang, outputDir))
    else:
        _run('swagger-codegen generate -i %s -l %s -o %s -DpackageName=%s' % (swaggerYamlPath, lang, outputDir, pkg))

def swaggerHtmlDoc(apimodelPath, pkg=''):
    html = swaggerhtml(apimodelPath)
    savedir = os.path.dirname(apimodelPath)
    savepath = os.path.join(savedir, 'swagger.yaml')
    print(savedir, savepath)
    fp = open(savepath, 'wb')
    header = '# Code generated by m2c. DO NOT EDIT.\n'
    if IS_PY3():
        fp.write(header.encode('utf-8'))
        fp.write(html.encode('utf-8'))
    else:
        fp.write(header)
        fp.write(html)
    fp.close()

    swaggerCodegen('html2', savedir, pkg=pkg, swaggerYamlPath=savepath)
