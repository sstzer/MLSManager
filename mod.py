import json,requests
from pathlib import Path
from config import record_path


class Search:
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

    @classmethod
    def search_list(cls,idx:str,num:int) -> list["Search"]:
        res=requests.get(f"https://api.modrinth.com/v2/search?query={idx}&limit={num}").json()
        mods=[cls(t) for t in res["hits"]]
        return mods

class Version:
    def __init__(self,info: dict) -> None:
        self.game_versions: list[str]=info["game_versions"]
        self.loaders: list[str]=info["loaders"]
        self.project_id: str=info["project_id"]
        self.file_url: str=info["files"][0]["url"]
        self.file_name: str=info["files"][0]["filename"]

    def record(self,version,loader):
        return Record({"file_name":self.file_name,"project_id":self.project_id,"version":version,"loader":loader})

    @classmethod
    def version_list(cls,idx:str) -> list["Version"]:
        res=requests.get(f"https://api.modrinth.com/v2/project/{idx}/version").json()
        versions=[cls(t) for t in res]
        return versions

class Record:
    def __init__(self,info: dict) -> None:
        self.file_name=info["file_name"]
        self.project_id=info["project_id"]
        self.version=info["version"]
        self.loader=info["loader"]

    @classmethod
    def load(cls,p: Path) -> list["Record"]:
        if not p.exists():
            p.write_text("[]",encoding="utf-8")
            return []
        try:
            rec=json.loads(p.read_text(encoding="utf-8"))
            rec=[cls(t) for t in rec]
        except (json.JSONDecodeError,ValueError):
            rec=[]
        return rec

    @classmethod
    def add(cls,p: Path,item: "Record") -> None:
        recs=cls.load(p)
        if item not in recs:
            recs.append(item)
        p.write_text(str(recs),encoding="utf-8")

    @classmethod
    def isin(cls,file: Path,recs:list["Record"]) -> bool:
        for rec in recs:
            if rec.file_name == file.name:
                Record.add(record_path,rec)
                return  True
        return False



    def __str__(self) -> str:
        return json.dumps({"file_name":self.file_name,"project_id":self.project_id,"version":self.version,"loader":self.loader})

    def __repr__(self) -> str:
        return json.dumps({"file_name":self.file_name,"project_id":self.project_id,"version":self.version,"loader":self.loader})

    def __eq__(self, other) :
        return str(self)==str(other)
