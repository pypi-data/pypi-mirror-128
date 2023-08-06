#coding: utf-8
"""
   作者: 熵域主
   版本: 1.0
"""
from urllib.parse import urlencode

import requests
import json
import base64

class GiteeRepo:
    token = None
    user = None
    repo = None
    def __init__(self, token=None, user=None, repo=None):
        self.token = token
        self.user = user
        self.repo = repo
        self.url = "https://gitee.com/" + user + "/" + repo + "/"
        if requests.get(url=self.url).status_code == 404:
            raise NameError("仓库 %s 不存在." % (self.repo))

        self.types = {}
        self.types["int"] = int
        self.types["str"] = str

    def get_file(self, path=None):
        return base64.b64decode(json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)["content"].encode()).decode()

    def get_data(self, path=None):
        return json.loads(base64.b64decode(json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)["content"].encode()).decode())["content"]

    def list_file(self, path=None, detail=False, int=False, dir=False):
        if detail and int:
            print("[-] 参数'detail'与参数'int'不可以均设置为True.")
            return False
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if detail:
                if not dir:
                    if file["type"] != "dir":
                        result.append(file)
                else:
                    result.append(file)
                continue
                
            if not int:
                if not dir:
                    if file["type"] != "dir":
                        result.append(file["name"])
                else:
                    result.append(file["name"])
            else:
                if file["name"] != ".keep":
                    if not dir:
                        if file["type"] != "dir":
                            try:
                                result.append(self.types["int"](file["name"]))
                            except ValueError:
                                raise ValueError("目标文件名不支持转换为数字.")
                    else:
                        try:
                            result.append(self.types["int"](file["name"]))
                        except ValueError:
                            raise ValueError("目标文件名不支持转换为数字.")
        return tuple(result)

    def list_file_int(self, path=None):
        return self.list_file(path=path, detail=False, int=True, dir=False)

    def list_folder(self, path=None, detail=False, int=False):
        if detail and int:
            print("[-] 参数'detail'与参数'int'不可以均设置为True.")
            return False
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if detail:
                if file["type"] == "dir":
                    result.append(file)
                continue

            if file["type"] == "dir":
                if not int:
                    result.append(file["name"])
                else:
                    try:
                        result.append(self.types["int"](file["name"]))
                    except ValueError:
                        raise ValueError("目标文件夹名不支持转换为数字.")
        return tuple(result)

    def list_dir(self, path=None, detail=False, int=False):
        return self.list_folder(path=path, detail=detail, int=int)
    
    def list_folder_int(self, path=None):
        result = []
        reception = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        for file in reception:
            if file["type"] == "dir":
                result.append(self.types["int"](file["name"]))
        return tuple(result)

    def upload_file(self, path=None, content=None):
        return requests.post(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}",
            data = {
                "access_token": self.token,
                "content": base64.b64encode(content.encode()),
                "message": "UPLOAD FILE - SQLEE"
                }
            )

    def update_file(self, path=None, content=None):
        return requests.put(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}",
            data = {
                "access_token": self.token,
                "content": base64.b64encode(content.encode()),
                "sha": self.get_sha(path=path),
                "message": "UPDATE FILE - SQLEE"
                }
            )

    def delete_file(self, path=None):
        data = {
            "access_token": self.token,
            "sha": self.get_sha(path=path),
            "message": "DELETE FILE - SQLEE"
            }
        return requests.delete(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?" + urlencode(data)
            )

    def get_sha(self, path=None):
        result = json.loads(requests.get(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}?access_token={self.token}"
            ).text)
        if isinstance(result, dict):
            if "sha" in result:
                return result["sha"]
            else:
                raise ValueError("捕获到的数据无法提取文件sha值.")
        else:
            print(result)
            raise ValueError("捕获到的数据无法提取文件sha值.")

    def make_folder(self, path=None):
        return requests.post(
            url = f"https://gitee.com/api/v5/repos/{self.user}/{self.repo}/contents/{path}/.keep",
            data = {
                "access_token": self.token,
                "content": base64.b64encode("*".encode()),
                "message": "MAKE FOLDER - SQLEE"
                }
            )

    def drop_folder(self, path=None):
        for folder in self.list_file(path=path, detail=True, dir=True):
            if folder["type"] == "dir":
                self.drop_folder(path=folder["path"])
            elif folder["type"] == "file":
                self.delete_file(path=folder["path"])
        return True
        
    def __str__(self):
        return self.repo

def make_repo(token=None, user=None, name=None, private=True, auto_init=True):
    return requests.post(
        url = "https://gitee.com/api/v5/user/repos",
        data = {
            'name': name,
            'access_token': token,
            'auto_init': auto_init,
            'private': private,
        }
    )
if __name__ == "__main__":
    db = GiteeRepo(token="1895956f770eb0e4d08013ee4b753203", user="fu050409", repo="TEST_API")
    #db.drop_folder(path="Table")
    #print(gitee.get_file("TEST"))
    #print(gitee.list_file(""))
    #print(gitee.list_folder("Table", int=True))
    #print(gitee.list_folder("Table", int=False, detail=True))
    #print(gitee.upload_file(path="TEST_UPLOAD", content="测试上传文件"))
    #print(gitee.delete_file(path="TEST_UPLOAD"))
    #print(gitee.update_file(path="TEST_COMMITTER", content="测试更新文件"))
