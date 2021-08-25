
from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil



class train():
    def __init__(self,root):
        self.root = root
    #새 페이지 오픈
        self.root.attributes('-topmost', True)
        self.root.title("Train_Select")
        self.root.geometry('700x200')
        
        #select model 함수
        def sel_page():
            filepath = filedialog.askdirectory()
            set_model_path1["text"] = filepath
            #model_path["text"]= filepath

        def sel_data():
            filepath = filedialog.askdirectory()
            set_data_path1["text"] = filepath
            #data_path["text"]= filepath
            filepath = filepath.split('/')
            #set_data_name1["text"] = data_name["text"]= filepath[-1]
            set_data_name1["text"] = filepath[-1]
            #Train function

        def out_of():
            #model_name["text"] = set_model_name1.get("1.0","end") #모델의 이름
            data_str = set_data_path1["text"]  #데이터의 위치
            data_str = os.path.relpath(data_str,os.getcwd())    #데이터 상대경로
            if not (os.path.isdir("models/"+set_model_name1.get("1.0","end")[:-1])):
                os.mkdir("models/"+set_model_name1.get("1.0","end")[:-1])
            os.system('export PYTHONPATH=$PYTHONPATH:$(pwd)')
            os.system('export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1')

            instrument1 = "python train.py --data_path ./" + data_str
            shutil.copyfile(data_str+"/_classes.txt" ,"./models/"+set_model_name1.get("1.0","end")[:-1]+"/_classes.txt")
            #instrument1 = 'gnome-terminal -e "' + instrument1 + '\"' 
            #os.system(instrument1)
            instrument2 = "python ckpt_to_pb.py --weights ./temp_checkpoints/temp --cfg "+ data_str+"/_classes.txt" +" --output ./models/" +set_model_name1.get("1.0","end")[:-1] 

            instrument2 = 'gnome-terminal -- sh -c "' +instrument1 + "; "  + instrument2 + ';\"'
            os.system(instrument2)
            self.root.destroy()

        #모델이름 select
        set_model_name0 = Label(self.root,text = "Name of Model: ",font = ("Times","12"),borderwidth = 1,relief="solid").grid(column = 0,row = 0)
        set_model_name1 = tk.Text(self.root,height = 2,width = 50)
        set_model_name1.grid(column = 1,row = 0)

        set_model_path0 = Label(self.root,text = "Model Path: ",font = ("Times","12"),borderwidth = 1,relief="ridge").grid(column = 0,row = 1)
        set_model_path1 = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="ridge")
        set_model_path1.grid(column = 1, row = 1)
        set_model_path_sel = Button(self.root,text = "Sel_path",command = sel_page)
        set_model_path_sel.grid(column = 2,row = 1)
        #select data 함수


        #모델 데이터 select
        set_data_name0 = Label(self.root,text = "Name of Data: ",font = ("Times","12"),borderwidth = 1,relief="ridge").grid(column = 0,row = 2)
        set_data_name1 = Label(self.root,text = "Data name",borderwidth = 3,relief="ridge")
        set_data_name1.grid(column = 1, row = 2)
   
        set_data_path0 = Label(self.root,text = "Data Path: ",font = ("Times","12"),borderwidth = 1,relief="solid").grid(column = 0,row = 3)
        set_data_path1 = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="solid")
        set_data_path1.grid(column = 1, row = 3)
        set_data_sel = Button(self.root,text = "Sel_path",command = sel_data)
        set_data_sel.grid(column = 2,row = 3)
        #확인란
        ok_label = Label(self.root,text = "모두 입력 완료하였다면 클릭 ->",borderwidth = 1,relief="ridge").grid(column = 1,row = 6)
        OK = Button(self.root,text = "  학습 시작   ",command = out_of)
        OK.grid(column = 2,row = 6)


