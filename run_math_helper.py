import os
from dotenv import load_dotenv
import subprocess

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY not found in .env file")

# Prepare environment with API key
env = os.environ.copy()
env["GEMINI_API_KEY"] = api_key


print("Starting Math Helper with Gemini...")
result = subprocess.run(["jac", "run", "math_helper.jac"], env=env)
