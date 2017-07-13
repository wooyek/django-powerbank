# coding=utf-8

import logging
from invoke import task

logging.basicConfig(format='%(asctime)s %(levelname)-7s %(thread)-5d %(filename)s:%(lineno)s | %(funcName)s | %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
logging.getLogger().setLevel(logging.INFO)
logging.disable(logging.NOTSET)
logging.debug('Loading %s', __name__)


@task
def bump(ctx, patch=True):
    if patch:
        ctx.run("bumpversion patch --no-tag")
    else:
        ctx.run("bumpversion minor")


@task
def release(ctx):
    ctx.run("git checkout master")
    ctx.run("python setup.py sdist upload -r pypi")


@task
def sync(ctx):
    """
    Sync master and develop branches in both directions
    """
    ctx.run("git checkout develop")
    ctx.run("git pull origin develop --verbose")

    ctx.run("git checkout master")
    ctx.run("git pull origin master --verbose")

    ctx.run("git checkout develop")
    ctx.run("git merge master --verbose")

    ctx.run("git checkout master")
    ctx.run("git merge develop --verbose")


@task
def test(ctx):
    ctx.run("tox")


@task(sync, test, bump, release)
def publish(ctx):
    ctx.run("git checkout develop")
    ctx.run("git merge master --verbose")

    ctx.run("git push origin develop --verbose")
    ctx.run("git push origin master --verbose")
