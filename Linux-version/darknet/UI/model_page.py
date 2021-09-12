from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil


class info():
    def __init__(self,root,model):
        self.root = root
        self.root.title("Model information")
        self.root.geometry('250x500')
        self.root.resizable(True,True)

        model_box = Listbox(self.root,height=0,selectmode = "browse")
        folder_name = os.listdir(os.path.dirname(os.path.abspath(__file__))+"/../models")
        for i,name in enumerate(folder_name):
            if name == 'models.json':
                continue;
            model_box.insert(i,name)
        model_box.grid(column = 0,row = 0,padx = 10,pady = 10)

        def select_model():
            selection = model_box.curselection()  
            class_info  = open("../models/"+folder_name[selection[0]]+"/obj.names","r")
            class_name = "\nCLASSES : \n"
            for name in class_info:
                class_name  +=name

            info  = "Model Name :       " + folder_name[selection[0]]+"\n" +class_name           #결과임 이게 
            model["text"] = info 
            self.root.destroy()

        Button(self.root,text = "선택" , command = select_model).grid(column = 0,row = 1,padx = 10,pady = 10)
 
