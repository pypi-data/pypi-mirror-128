#coding: utf-8
if __name__ == "__main__":
    from gitee import GiteeRepo
else:
    from .gitee import GiteeRepo

import json

class URL:
    url = "https://gitee.com/"
    def __init__(self, url=None):
        self.url = url if url != None else self.url
        self.url = self.url if self.url[-1] == "/" else self.url + "/"
        
    def __add__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)
        
    def __truediv__(self, value):
        value = str(value)
        value = value if value[-1] == "/" else value + "/"
        return URL(url=self.url + value)

    def __str__(self):
        return self.url

class table_objects:
    def __init__(self, obj=None):
        self.obj = obj

    def all(self):
        return self.obj.columns
    
    def get(self, id=None):
        for column in self.obj.columns:
            if column.id == id:
                return column
        raise ValueError("目标栏不存在.")

    def create(self, *args, **kwargs):
        column = self.obj.repo.list_folder(path=self.obj.name, int=True)
        if len(column) == 0:
            column = 0
        else:
            column = max(column) + 1
        self.obj.repo.make_folder(path=URL(self.obj.name)/column)

        datas = []
        for name in self.obj.namespace:
            if name == "id":
                continue

            if name in kwargs:
                datas.append(kwargs[name])
            else:
                datas.append(None)

        for i in range(len(datas)):
            self.obj.repo.upload_file(
                path = URL(self.obj.name) / column / i,
                content = json.dumps({"content": datas[i]})
                )
        self.obj.sync()
        return self.obj.columns

    def delete(self):
        self.obj.delete()
    
    @property
    def length(self):
        return len(self.obj.columns)

    def count(self):
        return len(self.obj.columns)
    
    def filter(self, *args, **kwargs):
        need = len(kwargs)
        result = []
        for column in self.obj.columns:
            transit = 0
            for kwarg in kwargs:
                if kwargs[kwarg] in column.data:
                    transit += 1
            if transit == need:
                result.append(column)
        return result

class SqleeData:
    data = None
    url = None
    repo = None
    id = None
    def __init__(self, data, url=None, repo=None, namespace=[]):
        if not isinstance(url, str) and not isinstance(url, URL):
            raise ValueError("参数'url'必须是字符串.")
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数'repo'必须是GiteeRepo.")
        self.data = data
        self.url = url
        self.repo = repo
        self.namespace = namespace

    @property
    def type(self):
        return type(self.data)

    def update(self, data=None):
        splited_url = self.url.split("/")
        answer = self.repo.update_file(
            path = str(URL(splited_url[-3])/splited_url[-2]/splited_url[-1]),
            content = json.dumps({"content": data})
            )
        self.data = data
        return answer

    def delete(self):
        answer = self.repo.delete_file(
            path = str(URL(splited_url[-3])/splited_url[-2]/splited_url[-1])
            )
        del self
        return answer

    def __str__(self):
        return self.data

class SqleeColumn:
    datas = []
    repo = None
    table = None
    id = None
    def __init__(self, url=None, repo=None, id=None, table=None,
                 namespace=[], *args, **kwargs):
        if not isinstance(url, str) and not isinstance(url, URL):
            raise ValueError("参数'url'必须是字符串或URL.")
        if not isinstance(id, int):
            raise ValueError("参数'id'必须是整型数.")
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数'repo'必须是GiteeRepo.")

        self.id = id
        self.repo = repo
        self.table = table
        self.url = url
        self.namespace = namespace
        self.sync()

    @property
    def data(self):
        result = []
        for data in self.datas:
            result.append(data.data)
        return tuple(result)

    @property
    def length(self):
        return len(self.data)

    def count(self):
        return len(self.data)

    def sync(self):
        self.datas = []
        datas = [self.id, ]
        datas += list(self.repo.list_file(path="%s/%d" % (self.table.name, self.id), detail=True))
        for data in datas:
            if isinstance(data, int):
                continue
            if data["name"] == ".keep":
                del datas[datas.index(data)]
        for data in datas:
            if isinstance(data, int):
                self.datas.append(
                    SqleeData(data, url="id",
                              namespace="id",
                              repo=self.repo)
                    )
                continue
            loads = self.repo.get_data(path=data["path"])
            self.__setattr__(self.namespace[int(data["name"])], loads)
            self.datas.append(
                SqleeData(loads, url=data["url"],
                          namespace=self.namespace[int(data["name"])],
                          repo=self.repo)
                )
        if len(datas) != len(self.namespace):
            raise ValueError("数据错误: 数据与命名域不符合.")
        self.datas = tuple(self.datas)
        return self.datas
        
    def update(self, datas):
        for data in datas:
            self.datas[datas.index(data)].update(data)
        self.sync()
        return self.datas

    def delete(self):
        for data in self.datas:
            self.datas[self.datas.index(data)].delete()
        del self
        return True

class SqleeTable:
    columns = []
    def __init__(self, name=None, repo=None):
        if not isinstance(name, str) and not isinstance(name, URL):
            raise ValueError("参数'name'必须是字符串或URL.")
        if not isinstance(repo, GiteeRepo):
            raise ValueError("参数'repo'必须是GiteeRepo.")

        self.name = name
        self.repo = repo
        self.url = URL()/self.repo.user/self.repo.repo/self.name
        self.sync()
        self.objects = table_objects(obj=self)
    
    def get_column(self, id=None):
        for column in self.columns:
            if column.id == id:
                return column
        else:
            raise ValueError("目标栏不存在.")

    def insert(self, datas=None):
        return self.objects.create(datas=datas)

    def sync(self):
        self.namespace = ["id", ]
        self.namespace += json.loads(self.repo.get_file(path=URL(self.name)/".namespace"))
        self.columns = []
        for column in self.repo.list_folder_int(path=self.name):
            self.columns.append(
                SqleeColumn(
                    url = self.url / column,
                    repo = self.repo,
                    id = int(column),
                    table = self,
                    namespace = self.namespace,
                    )
                )
        self.columns = tuple(self.columns)
        return self.columns

    def delete(self):
        answer = self.repo.drop_folder(path=self.name)
        del self
        return answer

if __name__ == "__main__":
    repo = GiteeRepo(token="1895956f770eb0e4d08013ee4b753203", user="fu050409", repo="TEST_API")
    table = SqleeTable(
        name="Table",
        repo = repo
        )
    print(table.columns[0].datas[0].data)
    
