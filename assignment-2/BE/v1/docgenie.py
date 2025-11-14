# docgenie.py
import libs.py_helpers as pyh
import os

def generate_markdown(repo: dict, out_dir: str) -> str:
    local_path = repo.get("local_path")
    repo_name = pyh.repo_name_from_path(local_path)
    save_dir = os.path.join(out_dir, repo_name)
    pyh.ensure_dir(save_dir)
    md_path = os.path.join(save_dir, "docs.md")

    md = []
    md.append(f"# {repo_name}\n")
    md.append("## Summary\n")
    md.append(repo.get("readme_summary", "No summary available.") + "\n")
    md.append("## File Tree\n")
    md.append("```\n" + pyh.file_tree_pretty(repo.get("map", {})) + "\n```\n")
    md.append("## Code Context Graph\n")
    md.append(pyh.ccg_to_markdown(repo.get("ccg", {})))

    try:
        img = pyh.make_ccg_diagram(repo.get("ccg", {}), os.path.join(save_dir, "ccg.png"))
        if img:
            md.append("\n\n![CCG](./ccg.png)\n")
    except Exception:
        pass

    final = "\n".join(md)
    pyh.write_text(md_path, final)
    return md_path
