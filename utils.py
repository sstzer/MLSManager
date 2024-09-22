import requests
from tqdm import tqdm
from config import mod_path,version,loader
from mod import Version

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



def down_versions(idx:str)->list[Version]:
    res=Version.version_list(idx)
    return [t for t in res if version in t.game_versions and loader in t.loaders]
