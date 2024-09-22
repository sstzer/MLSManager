import requests
from config import record_path,mod_path,loader,version
from mod import Version,Search,Record
from utils import download_url,down_versions


def search_project(num: int = 10) -> None:
    while True:
        a=input("输入模组名, 回车返回: ")
        if not a:
            return
        mods=Search.search_list(a,num)

        if not mods:
            print("未找到匹配项")
            continue

        for idx,mod in enumerate(mods):
            print(f"{idx+1}. {mod.title}")

        while True:
            t=input("输入序号下载，直接回车返回搜索界面: ")
            try:
                download_project(mods[int(t)-1].project_id)
                print("完成")
            except ValueError:
                break
            except IndexError:
                print("错误的序号")


def download_project(idx: str) -> None:
    mods = Record.load(record_path)
    if any(t.project_id == idx for t in mods):
        print("已下载")
        return
    res: list[dict]=requests.get(f"https://api.modrinth.com/v2/project/{idx}/version").json()
    dow=[Version(t) for t in res if version in t["game_versions"] and loader in t["loaders"]]
    download_url(dow[0].file_name,dow[0].file_url)
    Record.add(record_path,dow[0].record(version,loader))


def update() -> None:
    recs=Record.load(record_path)
    if not mod_path.exists():
        mod_path.mkdir()
    files = [f.name for f in mod_path.iterdir()]

    for i, rec in enumerate(recs):
        dow = down_versions(rec.project_id)
        if not dow:
            print(f"{rec.file_name} 无当前版本")
            continue

        if dow[0].file_name in files:
            print(f"{rec.file_name}已是最新版")
            continue

        download_url(dow[0].file_name, dow[0].file_url)
        if (mod_path / rec.file_name).exists():
            (mod_path / rec.file_name).unlink()
        recs[i] = dow[0].record(version, loader)

    record_path.write_text(str(recs),encoding="utf-8")
    print("完成")


def init_records() -> None:
    recs=Record.load(record_path)
    record_path.write_text("[]")
    for file in mod_path.iterdir():
        print(f"正在处理{file.name}")
        if Record.isin(file,recs):
            print(f"已存在{file.name}")
            continue
        res=Search.search_list(file.name,1)
        if not res:
            print(f"!!!未找到{file}")
            continue
        if dow:=down_versions(res[0].project_id):
            Record.add(record_path,dow[0].record(version,loader))
        else:
            print(f"!!!错误的{file}")
    print("完成")


def list_noRecord() -> None:
    clear()
    recs=Record.load(record_path)
    if not mod_path.exists():
        mod_path.mkdir()
    for f in mod_path.iterdir():
        if not Record.isin(f,recs):
            print(f.name)

def clear() -> None:
    recs=Record.load(record_path)
    for rec in recs:
        if not (mod_path/rec.file_name).exists():
            recs.remove(rec)
            print(f"delete {rec.file_name}")
    record_path.write_text(str(recs))