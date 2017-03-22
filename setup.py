import sys
from cx_Freeze import setup, Executable

setup(  name = "wowLadder",
        version = "1.0",
        description = "와우 래더",
        author = "Phraust",
        executables = [Executable("wowarena.py", base="Win32GUI")]) 

