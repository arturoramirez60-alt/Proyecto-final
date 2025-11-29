import subprocess
import sys

def main():

    streamlit_file = "C_visualizacion\inicio.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_file])


