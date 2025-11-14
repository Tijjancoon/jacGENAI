import streamlit as st
import subprocess, shlex, os, time

st.set_page_config(page_title="Codebase Genius v1")
st.title("Codebase Genius — v1 (Python pipeline)")

repo = st.text_input("Git repository URL", value="https://github.com/pallets/flask.git")

if st.button("Generate docs"):
    if not repo:
        st.error("Please provide a repository URL.")
    else:
        status = st.empty()
        status.info("Running pipeline... this may take a minute.")
        cmd = f"python3 BE/v1/run_pipeline.py {repo}"
        proc = subprocess.run(shlex.split(cmd), capture_output=True, text=True)
        if proc.returncode == 0:
            status.success("Pipeline finished successfully.")
            st.code(proc.stdout)
            # attempt to show results
            repo_name = os.path.basename(repo.rstrip("/")).replace(".git","")
            md_path = os.path.join("outputs", repo_name, "docs.md")
            img_path = os.path.join("outputs", repo_name, "ccg.png")
            if os.path.exists(md_path):
                with open(md_path, "r", encoding="utf-8") as fh:
                    st.markdown("### Generated docs (preview)")
                    st.code(fh.read()[:4000])
                    st.download_button("Download docs.md", fh.read(), file_name=f"{repo_name}_docs.md")
            else:
                st.warning("docs.md not found in outputs.")
            if os.path.exists(img_path):
                st.image(img_path, caption="CCG Diagram")
        else:
            status.error("Pipeline failed. See error below.")
            st.code(proc.stderr)
