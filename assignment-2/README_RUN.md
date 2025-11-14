# Codebase Genius
# 2. Create venv
python3 -m venv .venv

# 3. Activate venv
source .venv/bin/activate

# 4. Install dependencies
pip install --upgrade pip setuptools
pip install -r BE/requirements.txt
pip install -r FE/requirements.txt

# 5. Install graphviz (optional but recommended)
sudo apt-get update
sudo apt-get install -y graphviz

# 6. Run backend pipeline
python3 BE/v1/run_pipeline.py https://github.com/pallets/flask.git

# 7. (in another WSL terminal) run frontend
cd /mnt/c/Users/TCoon/jacGENAI/agentic_codebase_genius
source .venv/bin/activate
streamlit run FE/streamlit_app.py