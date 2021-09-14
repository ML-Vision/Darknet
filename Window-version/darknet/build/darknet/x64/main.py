from tkinter import *
from tkinter import filedialog
import tkinter as tk
import os
import sys
import UI.UI as ui
def main():
    root = Tk()
    UI = ui.UI(root)
    UI.root.mainloop()


if __name__ == "__main__":
    main()