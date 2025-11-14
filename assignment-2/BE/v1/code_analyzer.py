# code_analyzer.py
import libs.py_helpers as pyh
import os

def build_ccg(local_path: str, targets: list):
    ccg = {"nodes": [], "edges": []}
    for t in targets:
        t_abs = t if os.path.isabs(t) else os.path.join(local_path, t)
        info = pyh.parse_source_file(t_abs)
        for fn in info.get("functions", []):
            ccg["nodes"].append({"type":"function","name":fn.name,"file":t_abs,"lineno":fn.lineno,"doc":fn.doc})
        for cl in info.get("classes", []):
            ccg["nodes"].append({"type":"class","name":cl.name,"file":t_abs,"lineno":cl.lineno,"doc":cl.doc})
        for call in info.get("calls", []):
            ccg["edges"].append({"from":call[0],"to":call[1],"file":t_abs})
    return ccg
