#coding: utf-8

import os, sys, json
import requests, traceback
import argparse, shlex, platform
import importlib

from prompt_toolkit import prompt
from requests import get, post, put, delete

if __name__ == "__main__":
    from utils import gitee
    from utils.backend import URL, SqleeData, SqleeColumn, SqleeTable
else:
    from .utils import gitee
    from .utils.backend import URL, SqleeData, SqleeColumn, SqleeTable
from prompt_toolkit.output.win32 import NoConsoleScreenBufferError

class termios:
    class error(RuntimeError):
        pass
Windows = True if platform.system() == "Windows" else False

class objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.all_tables()
    
    def get(self, name=None):
        if name in self.obj.repo.list_folder(path=""):
            return SqleeTable(name=name, repo=self.obj.repo)
        raise ValueError("目标表不存在.")

    def create(self, name=None, namespace=None):
        return self.obj.create_table(name=name, namespace=namespace)

    def delete(self, *args, **kwargs):
        return self.obj.drop_table(*args, **kwargs)
    
    def count(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

    @property
    def count(self):
        return len(self.obj.repo.list_folder(path="", detail=True))

class Sqlee:
    access_token = None
    repo = None
    owner = None
    def __init__(self, access_token, repo, owner):
        self.access_token = access_token
        self.repo = gitee.GiteeRepo(token=access_token, user=owner, repo=repo)
        self.owner = owner
        self.objects = objects(obj=self)

    def all_tables(self):
        datas = self.repo.list_folder(path="", detail=True)
        tables = [SqleeTable(name=data['name'], repo=self.repo) for data in datas if data['type'] == 'dir']
        return tables

    def create_table(self, name=None, namespace=None):
        for i in namespace:
            if i == "id":
                raise NameError("命名域不可使用'id'参数.")
        make = self.repo.make_folder(path=name)
        self.repo.upload_file(path=name+"/"+".namespace", content=json.dumps(namespace))
        return make

    def drop_table(self, name=None):
        return self.repo.drop_folder(path=name)

    def clear(self, sure=False):
        if not sure:
            confirm = input("你确定删除本数据库(同时删除云端数据)吗? (Y/N) ")
            if confirm == "Y" or confirm == "y":
                pass
            else:
                print("忽略.")
                return
        url = f"https://gitee.com/api/v5/repos/{self.owner}/{self.repo}"

        requests.delete(
            url = url,
            data = {"access_token": self.access_token,}
        )
        del self
        return True
    
    def interact(self):
        def hotreload():
            import os, sys
            os.system("python %s" % sys.argv[0])

        print("SQLEE 1.2.3\nCopyright © 中国左旋联盟×Freet安全组")
        all_tables = self.all_tables
        get_all_tables = self.all_tables
        tables = self.all_tables
        create_table = self.create_table
        create = self.create_table
        exit = lambda: os._exit(0)
        while True:
            try:
                cmd = prompt('SQLEE>>> ')
            except NoConsoleScreenBufferError:
                if Windows:
                    print("SQLEE CONSOLE必须在 'cmd.exe' 中运行 !")
                    restart = input("是否要在CMD中重新执行本程序(或脚本)? (Y/N) ")
                    restart = True if restart == "Y" else False
                    if restart:
                        os.system("python %s" % sys.argv[0])
                else:
                    print("你的终端暂不支持运行HFCONSOLE.")
                exit()
            except termios.error:
                print('[-] Termios 错误, 你的终端不支持SQLEE CONSOLE或由于SQLEE CONSOLE开启时终端显示大小被调整, 请检查终端设置并重试.')
                exit()
            except KeyboardInterrupt:
                print("执行 'exit()' 来退出该会话.")
                continue
            except EOFError:
                print("不要使用 'Ctrl+D'(EOF) 来退出, 用 'exit()' 来代替它.")
                continue

            try:
                print(eval(cmd))
            except:
                traceback.print_exc()

if __name__ == '__main__':
    """t_s = Sqlee(
        access_token="f8eca055b26c3e4c64176d4c9f66902b",
        owner="freetbash",
        repo="sqleedb",
    )"""
    db = Sqlee(
        access_token = "1895956f770eb0e4d08013ee4b753203",
        owner = "fu050409",
        repo = "TEST_API",
    )
    print(db.all_tables()[0].columns[0].datas[1].data)
    #print(t_s.filter('table',blurry=True,kwargs={0:'1'}))
    #t_s.filter('table')
    #print(t_s.select_data('member',[1,0,]))
    #t_s.update_data('table',0,{0:'123333',3:'34535'})
    #t_s.insert_data('test',{0:'123',1:'456'})
    #t_s.interact()
        #t_s.show_tables()

    #t_s.create_table("asdfreet")
