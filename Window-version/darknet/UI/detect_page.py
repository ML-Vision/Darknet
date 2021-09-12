from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil



class detect():
    def __init__(self,root,model_name,model_path,data_name,data_path):
        #새 페이지 오픈
        self.root = root
        self.root.title("Detect_Select")
        self.root.geometry('700x200')
        #select model 함수
        
        def sel_page():
            SEL = Tk()
       
            model_box = Listbox(SEL,height=0,selectmode = "browse")
            folder_name = os.listdir(os.path.dirname(os.path.abspath(__file__))+"/../models")
            folder_name.remove("models.json")
            for i,name in enumerate(folder_name):
                model_box.insert(i,name)
            model_box.grid(column = 0,row = 0,padx = 10,pady = 10)
            
            def data():
                selection = model_box.curselection()
                dec_model_path1["text"] = "../models/"+folder_name[selection[0]]
                dec_model_name1["text"] = folder_name[selection[0]]
                SEL.destroy()
                
            Button(SEL,text = "선택" , command = data).grid(column = 0,row = 1,padx = 10,pady = 10)

            """
            filepath = filedialog.askdirectory()
            dec_model_path1["text"] = filepath
            filepath = filepath.split('/')
            dec_model_name1["text"] = filepath[-1]
            """

        #select data 함수
        def sel_data():
            
            filepath = filedialog.askdirectory()
            dec_data_path1["text"] = filepath
            filepath = filepath.split('/')
            dec_data_name1["text"] = filepath[-1]
            
        #디텍트시 실행되는 함수 터미널열어서 명령어 넣음
        def out_of():
            model_name["text"] = dec_model_name1["text"]
            model_path["text"] = dec_model_path1["text"]
            data_name["text"] = dec_data_name1["text"]
            data_path["text"] = dec_data_path1["text"]
            #모델 상대경로
            model_str = os.path.relpath(dec_model_path1["text"],os.getcwd())
            #데이터 상대경
            data_str = os.path.relpath(dec_data_path1["text"],os.getcwd())
            os.system('export PYTHONPATH=$PYTHONPATH:$(pwd)')
            os.system('export LD_PRELOAD=/usr/lib/aarch64-linux-gnu/libgomp.so.1')

            print(model_str)
            file_list = os.listdir(model_str)
            cfg = ""
            data = ""
            weights = ""
            name = ""
            for f in file_list:
                if f[-3:] == "cfg":
                    cfg = f
                elif f[-4:] == "data":
                    data = f
                elif f[-7:] == "weights":
                    weights = f
                elif f[-5:] == "names":
                    name = f
            f = open(model_str+"/"+data,'r',encoding = 'UTF8')
            Read = f.readlines()
            new_text = ''
            for i,lines in enumerate(Read):
                l = lines.split('=')
                if(l[0].strip() == "names"):
                    name = "names = " + model_str + "/" + name+"\n"
                    new_string = name
                else:
                    new_string = lines
                new_text+=new_string
            with open(model_str+"/"+data,'w',encoding = 'UTF8') as f:
                f.write(new_text) 
           
            #자동 실행
            instrument_str = "python3 ../darknet_images.py --input " + data_str+ "  --config_file " + model_str + "/" + cfg + "  --data_file "+model_str+"/"+data + "  --weights " + model_str + "/" + weights
            print(instrument_str)
            instrument_str = 'gnome-terminal -- '+instrument_str
            os.system(instrument_str)
            self.root.destroy()
        



        #모델이름 select
        dec_model_name0 = Label(self.root,text = "Name of Model: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 0)
        dec_model_name1 = Label(self.root,text = "Model Name")
        dec_model_name1.grid(column = 1,row = 0)

        dec_model_path0 = Label(self.root,text = "Model Path: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 1)
        dec_model_path1 = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="ridge")
        dec_model_path1.grid(column = 1, row = 1)
        dec_model_path_sel = Button(self.root,text = "Sel_path",command = sel_page,overrelief = "groove")
        dec_model_path_sel.grid(column = 2,row = 1)

        #모델 데이터 select
        dec_data_name0 = Label(self.root,text = "Name of Data: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 2)
        dec_data_name1 = Label(self.root,text = "Data name",borderwidth = 3)
        dec_data_name1.grid(column = 1, row = 2)
   
        dec_data_path0 = Label(self.root,text = "Data Path: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 3)
        dec_data_path1 = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="ridge")
        dec_data_path1.grid(column = 1, row = 3)
        dec_data_sel = Button(self.root,text = "Sel_path",command = sel_data,overrelief = "groove")
        dec_data_sel.grid(column = 2,row = 3)
        #확인란
        ok_label = Label(self.root,text = "모두 입력 완료하였다면 클릭 ->",borderwidth = 1).grid(column = 1,row = 6)
        OK = Button(self.root,text = "  인식 시작   ",command = out_of,overrelief = "groove")
        OK.grid(column = 2,row = 6)

        self.root.mainloop()


