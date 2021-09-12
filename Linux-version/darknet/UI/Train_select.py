from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil
import detect_page as de
import train_page as tr
import model_page as mo
import webbrowser

class select():
    def __init__(self,root,model_name,model_path,data_name,data_path):
        self.root = root
        self.root.title("Train_select")
        self.root.geometry('580x200')

        def COLAB():
            webbrowser.open("https://colab.research.google.com/drive/1HZpxIQCitg3GqBplAYOL-aGKa6K3r5lz?usp=sharing")
            webbrowser.open("https://roboflow.com/")
            webbrowser.open("https://kimcharless.tistory.com/1")
            self.root.destroy()
       
        def train():
            page = Tk()
            train_page = tr.train(page,model_name,model_path,data_name,data_path)
            self.root.destroy()
 
        colab = Button(self.root,text = "Train in Colab" , width = 70, height = 5 , command = COLAB , overrelief = "groove")
        colab.grid(column = 0, row = 0)
        Train_in_PC = Button(self.root,text = "Train in PC", width = 70, height = 5 , command = train , overrelief = "groove")
        Train_in_PC.grid(column = 0,row = 1)
