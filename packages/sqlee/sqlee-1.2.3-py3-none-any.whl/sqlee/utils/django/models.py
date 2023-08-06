#coding: utf-8
import os
import json
import requests
from sqlee.utils.backend import SqleeTable

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    settings = __import__(os.environ['DJANGO_SETTINGS_MODULE']).settings
else:
    raise ImportError("Django工程未被执行，请在Django工程中导入Sqlee的Django组件.")
try:
    if not settings.ENABLE_SQLEE or settings.SQLEE_NAME.replace(" ", "") == "":
        raise ImportError('Sqlee未在Django被正确配置.')
except Exception as exc:
    raise ImportError('Sqlee未在Django被正确配置.') from exc

class Model:
    def __init__(self):
        self.repo = settings.SQLEE
        self.tablename = "%s_%s" % (
            self.app,
            self.__class__.__name__
            )

    @property
    def table(self):
        return SqleeTable(name=self.tablename, repo=self.repo)