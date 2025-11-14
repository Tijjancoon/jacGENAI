# repo_mapper.py
from typing import List
import libs.py_helpers as pyh
import os

def map_repo(local_path: str):
    return pyh.build_file_tree(local_path, exclude=[".git", "node_modules", "__pycache__"])

def summarize_readme(local_path: str) -> str:
    return pyh.summarize_readme(local_path)

def prioritize(file_tree: dict, root: str, n:int=5) -> List[str]:
    names = ["main.py", "app.py", "index.py", "__main__.py", "README.md", "server.py"]
    found = []
    for rel, files in file_tree.items():
        for name in names:
            if name in files:
                p = os.path.join(root, rel) if rel != "." else root
                found.append(os.path.join(p, name) if rel != "." else os.path.join(root, name))
    found = list(dict.fromkeys(found))
    if found:
        return found
    out = []
    for rel, files in file_tree.items():
        for f in files:
            if f.endswith(".py"):
                path = os.path.join(root, rel) if rel != "." else root
                out.append(os.path.join(path, f))
    return out[:n]
