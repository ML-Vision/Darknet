from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil
import UI as ui
 
def main():
    root = Tk()
    UI = ui.UI(root)
    UI.root.mainloop()


if __name__ == "__main__":
    main()