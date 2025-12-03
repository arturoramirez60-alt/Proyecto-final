import subprocess
import sys
import streamlit as st

"""
Ejecuta el archivo de bienvenida y todas las demas paginas del dashboard
"""

def main():

    streamlit_file = r"C_visualizacion\bienvenida.py"
    subprocess.run([sys.executable, "-m", "streamlit", "run", streamlit_file])
    
if __name__ ==  "__main__":
    main()