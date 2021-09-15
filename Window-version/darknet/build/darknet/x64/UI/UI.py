from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
from pathlib import Path as mypath
import shutil
from UI.detect_page import detect as de
from UI.Train_select import select as ts
from UI.model_page import info as mo
from UI.Camera_detect import camera_detect as  te
import UI.my_path as mp
from datetime import datetime
import uuid

def model_information():
    model_root = mp.model_root() #mypath.joinpath(mypath.cwd(),"models")
    model_names = mp.model_names()# os.listdir(model_root)
    json_path = mp.model_json_path()# mypath.joinpath(model_root,"models.json")
    
    model_group = dict()
    for group in model_names:
        file_path = mp.inner_file_path(model_root,group,"information.txt") #mypath.joinpath(mypath.joinpath(model_root,group),"information.txt")
        if not os.path.isfile(file_path):
            f = open(file_path,'w')
            f.write("ID = "+str(uuid.uuid4())+"\n")
            now = datetime.now()
            f.write("Date/Time = "+str(now)[:10] + str(now)[10:19]+"\n")
            f.write("User = NONE\n")
            f.write("Model Name = "+group+"\n")
            f.write("Data = NONE")
            f.close()
        with open(file_path,'r') as f:
            temp = dict()
            lines = f.readlines()
            for i in lines:
                l = i.split('=')
                if(l[0] == "ID "):
                   temp["ID"] = l[1][1:-1]
                if(l[0] == "Date/Time "):
                   temp["Date/Time"] = l[1][1:-1]
                if(l[0] == "User "):
                   temp["User"] = l[1][1:-1]
                if(l[0] == "Model Name "):
                    temp["Model Name"] = l[1][1:-1]
                if(l[0] == "Data "):
                    temp["Data"] = l[1][1:]
            model_group[temp["ID"]] = temp
    with open(json_path,'w',encoding = 'utf-8') as make_file:
        json.dump(model_group,make_file,indent = "\t", ensure_ascii=False)

    with open(json_path,'r',encoding = 'utf-8') as f:
        json_data = json.load(f)

class UI():

    def __init__(self,root):
        self.root = root
        self.root.title("Vision")
        self.root.geometry("800x600+100+100") # w, h, 왼쪽 끝에서의 거리, 오른쪽 끝에서의 거리
        
        #모델 이름 쇼박스
        Label(text = "MODEL : ",font = ("Times","12"),foreground = 'white',background = '#000000',width = 10).place(x = 50, y = 80)
        model_name = Label(text = "model_name")
        model_name.place(x=150,y=80)
        model_path = Label(text = "model path")
        model_path.place(x = 300,y=80)
        #데이터 이름 쇼박스
        Label(text = "DATA : ",font = ("Times","12"),foreground = 'white',background = '#000000',width = 10).place(x = 50, y = 120)
        data_name = Label(text = "data name")
        data_name.place(x=150,y=120)
        data_path = Label(text = "data path")
        data_path.place(x = 300,y = 120)
        #모델 정보 표시
        show_model = Label(text = "Model Information" , font = ("20"),borderwidth = 1,relief="solid",width = 40,height = 15,justify = "left")
        show_model.place(x = 300, y = 200)
        self.root.resizable(True,True)

        def train():
            page = Tk()
            train_page = ts(page,model_name,model_path,data_name,data_path)

        def detect():
            page = Tk()
            detect_page = de(page,model_name,model_path,data_name,data_path)

        def info():
            page = Tk()
            information_page = mo(page,show_model)

        def camera():
            page = Tk()
            camera_page = te(page)


        model_information()
        #train 버튼
        Button(self.root,text = "Train" ,command = train,overrelief = "groove").place(x = 50,y=200,width = 100,height = 50)
        #detect버튼
        Button(self.root,text = "Detect",command = detect,overrelief = "groove").place(x = 50,y=280,width = 100,height = 50)
        #model_info 버튼
        Button(self.root,text = "model_info",command = info,overrelief = "groove").place(x = 50,y=360,width = 100,height = 50)
        #텐서보드 버튼
        Button(self.root,text = "Camera Detect",command = camera,overrelief = "groove").place(x = 50,y=440,width = 100,height = 50)
        
        self.root.mainloop()


