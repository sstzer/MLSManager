import json,requests
from pathlib import Path
from tqdm import tqdm
from config import mod_path,record_path,version,loader
from mods import Mod,Record,Version


def load_record(p: Path) -> list[Record]:
    if not p.exists():
        p.write_text("[]",encoding="utf-8")
        return []
    try:
        rec=json.loads(p.read_text(encoding="utf-8"))
        rec=[Record(t) for t in rec]
    except (json.JSONDecodeError,ValueError):
        rec=[]
    return rec

def add_record(p: Path,item: Record) -> None:
    recs=load_record(p)
    if item not in recs:
        recs.append(item)
    p.write_text(str(recs),encoding="utf-8")


def download_url(name: str,url: str) -> None:
    response=requests.get(url,stream=True)
    total_size=int(response.headers.get('content-length',0))
    if not mod_path.exists():
        mod_path.mkdir(parents=True)
    file_path=mod_path/name
    with file_path.open("wb") as f:
        with tqdm(total=total_size,unit='B',unit_scale=True,desc=name,initial=0) as progress_bar:
            for data in response.iter_content(1024):
                f.write(data)
                progress_bar.update(len(data))

def search(q:str ="",num: int=10) -> list[Mod]:
    res=requests.get(f"https://api.modrinth.com/v2/search?query={q}&limit={num}").json()
    mods=[Mod(t) for t in res["hits"]]
    return mods


def in_record(file: Path,recs:list[Record]) -> bool:
    for rec in recs:
        if rec.file_name == file.name:
            add_record(record_path,rec)
            return  True
    return False


def down_versions(idx:str)->list[Version]:
    res: list[dict] = requests.get(f"https://api.modrinth.com/v2/project/{idx}/version").json()
    return [Version(t) for t in res if version in t["game_versions"] and loader in t["loaders"]]
