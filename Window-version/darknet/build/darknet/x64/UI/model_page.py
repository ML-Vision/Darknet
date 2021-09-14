from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
from pathlib import Path as mypath
import UI.my_path as mp
import shutil


class info():
    def __init__(self,root,model):
        self.root = root
        model_root = mp.model_root() # mypath.joinpath(mypath.cwd(),"models")
        model_names = mp.model_names() # os.listdir(model_root)
        window_height = str(len(model_names) * 10 + 100) # 기본값 100. 모델 이름 한개당 10씩 늘어남. 
        self.root.title("Model information")
        self.root.geometry('180x' + window_height)
        self.root.resizable(True,True)

        model_box = Listbox(self.root,height=0,selectmode = "browse")
        for i,name in enumerate(model_names):
            if name == 'models.json':
                continue;
            model_box.insert(i,name)
        model_box.grid(column = 0,row = 0,padx = 10,pady = 10)

        def select_model():
            selection = model_box.curselection()
            obj_file_path = mp.inner_file_path(model_root,model_names[selection[0]],"obj.names") #mypath.joinpath(mypath.joinpath(model_root,model_names[selection[0]]),"obj.names")
            print(obj_file_path)
            class_info  = list(open(obj_file_path,"r"))
            #print(class_info)
            if(len(class_info) > 10) : class_info = class_info[:10] # 클래스 많으면 넘쳐서 개수 제한 .
            class_name = "\nCLASSES : \n"
            for name in class_info:
                class_name  +=name
            info  = "Model Name :       " + model_names[selection[0]]+"\n" +class_name           #결과임 이게 
            model["text"] = info 
            self.root.destroy()

        Button(self.root,text = "선택" , command = select_model).grid(column = 0,row = 1,padx = 10,pady = 10)
 
