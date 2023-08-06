from sqlee.utils.django import models
import os
import sqlee
import sys
import json
import requests

if 'DJANGO_SETTINGS_MODULE' in os.environ:
    settings = __import__(os.environ['DJANGO_SETTINGS_MODULE']).settings
else:
    raise ImportError("Django工程未被执行，请在Django工程中导入Sqlee的Django组件.")
try:
    if not settings.ENABLE_SQLEE or settings.SQLEE_NAME.replace(" ", "") == "":
        raise ImportError('Sqlee未在Django被正确配置.')
except Exception as exc:
    raise ImportError('Sqlee未在Django被正确配置.') from exc

def init():
    url = json.loads(requests.get("https://gitee.com/api/v5/repos/{user}/{name}?access_token={token}".format(
        user = settings.SQLEE_SETTINGS["OWNER"],
        name = settings.SQLEE_SETTINGS["NAME"],
        token = settings.SQLEE_SETTINGS["TOKEN"]
        )).text)
    if "message" in url:
        if url["message"] == "Not Found Project":
            print("开始创建数据库...")
            sqlee.utils.gitee.make_repo(token=settings.SQLEE_SETTINGS["TOKEN"], user=settings.SQLEE_SETTINGS["OWNER"], name=settings.SQLEE_SETTINGS["NAME"]).text
        else:
            raise Exception(url["message"])
    else:
        return True
            
def migrate():
    repo = sqlee.connect(token=settings.SQLEE_SETTINGS["TOKEN"], repo=settings.SQLEE_SETTINGS["NAME"], owner=settings.SQLEE_SETTINGS["OWNER"])
    sys.path.append(settings.BASE_DIR)

    for app in settings.INSTALLED_APPS:
        if app.split(".")[0] != "django":
            try:
                sqlee_models = __import__("%s.sqlee_models" % (app)).sqlee_models
                print("正在解析模块'%s'内的SQLEE数据库声明文件." % (app))
            except ModuleNotFoundError:
                print("模块'%s'中未找到SQLEE数据库声明文件." % (app))
                continue
            for model in dir(sqlee_models):
                model = getattr(eval("sqlee_models"), model)
                if hasattr(model, "__base__"):
                    print("正在读取Model '%s'" % (model.__name__))
                    if model.__base__ is models.Model:
                        print("\n正在创建数据库: '%s'\n" % (model().tablename))
                        repo.objects.create(name=model().tablename, namespace=model().namespaces)
    return True
                
