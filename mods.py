import json


class Mod:
    def __init__(self,info: dict) -> None:
        self.project_id: str=info["project_id"]
        self.slug:str=info["slug"]
        self.title: str=info["title"]
        self.description: str=info["description"]
        self.versions: list[str]=info["versions"]

    def record(self,file_name,version,loader):
        return Record({"file_name":file_name,"project_id":self.project_id,"version":version,"loader":loader})

    def __str__(self) -> str:
        tmp={"title":self.title,"project_id":self.project_id}
        return json.dumps(tmp)

class Version:
    def __init__(self,info: dict) -> None:
        self.game_versions: list[str]=info["game_versions"]
        self.loaders: list[str]=info["loaders"]
        self.project_id: str=info["project_id"]
        self.file_url: str=info["files"][0]["url"]
        self.file_name: str=info["files"][0]["filename"]

    def record(self,version,loader):
        return Record({"file_name":self.file_name,"project_id":self.project_id,"version":version,"loader":loader})

class Record:
    def __init__(self,info: dict) -> None:
        self.file_name=info["file_name"]
        self.project_id=info["project_id"]
        self.version=info["version"]
        self.loader=info["loader"]

    def __str__(self) -> str:
        return json.dumps({"file_name":self.file_name,"project_id":self.project_id,"version":self.version,"loader":self.loader})

    def __repr__(self) -> str:
        return json.dumps({"file_name":self.file_name,"project_id":self.project_id,"version":self.version,"loader":self.loader})

    def __eq__(self, other) :
        return self.__str__()==other.__str__()