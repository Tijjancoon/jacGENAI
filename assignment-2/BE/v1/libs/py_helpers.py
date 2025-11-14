# libs/py_helpers.py
import os, subprocess, json, shutil, tempfile, textwrap, re
from typing import List

def is_valid_git_url(url: str) -> bool:
    return url.startswith("http://") or url.startswith("https://") or url.endswith(".git")

def ensure_outputs_dir(base="outputs"):
    os.makedirs(base, exist_ok=True)
    return os.path.abspath(base)

def clone_repo(url: str, out_dir: str) -> str:
    try:
        repo_name = url.rstrip("/").split("/")[-1].replace(".git","")
        dest = os.path.join(out_dir, repo_name)
        if os.path.exists(dest):
            shutil.rmtree(dest)
        cmd = ["git","clone",url,dest]
        res = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        if res.returncode != 0:
            print("git clone failed:", res.stderr)
            return ""
        return os.path.abspath(dest)
    except Exception as e:
        print("clone exception:", e)
        return ""

def build_file_tree(root: str, exclude: List[str]=None) -> dict:
    exclude = set(exclude or [])
    tree = {}
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in exclude and not d.startswith(".")]
        rel = os.path.relpath(dirpath, root)
        tree[rel if rel != "." else "."] = filenames
    return tree

def file_tree_pretty(tree: dict) -> str:
    s = ""
    for k in sorted(tree.keys()):
        s += f"{k}:\n"
        for f in tree[k]:
            s += f"  - {f}\n"
    return s

def summarize_readme(root: str) -> str:
    candidates = ["README.md", "README"]
    for c in candidates:
        path = os.path.join(root, c)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as fh:
                    txt = fh.read(4000)
                paras = [p.strip() for p in txt.split("\n\n") if p.strip()]
                if len(paras) >= 1:
                    return paras[0] + ("\n\n" + paras[1] if len(paras)>1 else "")
                else:
                    return txt[:800]
            except Exception:
                break
    return "No README found; repository summary unavailable."

def parse_source_file(path):
    info = {"functions": [], "classes": [], "calls": []}
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            txt = fh.read()
    except Exception:
        return info
    for m in re.finditer(r'^\s*def\s+([a-zA-Z_][\w]*)\s*\(', txt, re.MULTILINE):
        name = m.group(1)
        obj = type("F",(object,),{"name":name,"lineno":txt[:m.start()].count("\n")+1,"doc":""})()
        info["functions"].append(obj)
    for m in re.finditer(r'^\s*class\s+([A-Za-z_][\w]*)\s*[:\(]', txt, re.MULTILINE):
        name = m.group(1)
        obj = type("C",(object,),{"name":name,"lineno":txt[:m.start()].count("\n")+1,"doc":""})()
        info["classes"].append(obj)
    for m in re.finditer(r'([A-Za-z_][\w]*)\s*\(', txt):
        name = m.group(1)
        if name in ("if","for","while","return","assert","with","print","len","isinstance","range","open","def","class"):
            continue
        info["calls"].append(("?", name))
    return info

def query_ccg(ccg: dict, q: str):
    out = []
    for n in ccg.get("nodes",[]):
        if q.lower() in n.get("name","").lower():
            out.append(n)
    return out

def repo_name_from_path(path: str) -> str:
    return os.path.basename(path.rstrip("/"))

def ccg_to_markdown(ccg: dict) -> str:
    md = []
    nodes = ccg.get("nodes",[])
    edges = ccg.get("edges",[])
    md.append("### Nodes\n")
    for n in nodes:
        md.append(f"- **{n.get('type')}** {n.get('name')} (file: {n.get('file')})")
    md.append("\n### Edges\n")
    for e in edges:
        md.append(f"- {e.get('from')} -> {e.get('to')} (in {e.get('file')})")
    return "\n".join(md)

def write_text(path: str, text: str):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)

def ensure_dir(p: str):
    os.makedirs(p, exist_ok=True)

def make_ccg_diagram(ccg: dict, target_path: str) -> str:
    try:
        import graphviz
        g = graphviz.Digraph(format='png')
        names = set()
        for n in ccg.get("nodes",[]):
            nm = n.get("name")
            if nm not in names:
                g.node(nm)
                names.add(nm)
        for e in ccg.get("edges",[]):
            g.edge(e.get("from"), e.get("to"))
        out_base = target_path.replace(".png","")
        g.render(filename=out_base, cleanup=True)
        return target_path
    except Exception:
        return ""
