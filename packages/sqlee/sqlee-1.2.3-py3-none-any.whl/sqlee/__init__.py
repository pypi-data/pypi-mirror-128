from .sqlee import Sqlee

__name__ = "sqlee"
__version__ = "1.2.3"
__all__ = [
    'connect', 'utils',
    ]
__author__ = "Entropy <fu050409@163.com>"
__incantation__ = "嗡嘛呢叭咪吽"

def connect(token=None, repo=None, owner=None):
    return Sqlee(access_token=token, repo=repo, owner=owner)
