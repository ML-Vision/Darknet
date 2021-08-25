from tkinter import *
from tkinter import filedialog
import tkinter as tk
import subprocess
import os
import json
import pathlib
import shutil

class camera_detect():
    def __init__(self,root):
        self.root = root
        self.root.title("Camera Detect")
        self.root.geometry("700x100")
        cfg = ""
        data = ""
        weights = ""
        name = ""
        filepath = ""
        def set_model():
            SEL = Tk()
            model_box = Listbox(SEL,height=0,selectmode = "browse")
            folder_name = os.listdir(os.path.dirname(os.path.abspath(__file__))+"/../models")
            for i,name in enumerate(folder_name):
                model_box.insert(i,name)
            model_box.grid(column = 0,row = 0,padx = 10,pady = 10)
            
            def data():
                selection = model_box.curselection()
                Model_path["text"] = filepath = "../models/"+folder_name[selection[0]]
                file_list = os.listdir(filepath)
                for f in file_list:
                    if f[-3:] =="cfg":
                        cfg = f
                    elif f[-4:]=="data":
                        data = f
                    elif f[-7:] == "weights":
                        weights = f
                SEL.destroy()
                
            Button(SEL,text = "선택" , command = data).grid(column = 0,row = 1,padx = 10,pady = 10)


        def out_of():
            instrument = "python3 ../CAM/CAM.py --config_file "+filepath +"/"+cfg + " --data_file "+filepath+"/"+data+" --weights "+filepath+"/"+weights
            instrument = 'gnome-terminal -- ' + instrument
            os.system(instrument)

        Model = Label(self.root,text = "Model Path: ",font = ("Times","15")).grid(column = 0,row = 1)
        Model_path = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="groove")
        Model_path.grid(column = 1, row = 1)
        Model_set = Button(self.root,text = "Sel_path",font = ("Times","12") , command = set_model)
        Model_set.grid(column = 2,row = 1)
        
        ok_label = Label(self.root,text = "모델 선택하였으면 클릭 -> ").grid(column = 1,row = 2)
        OK = Button(self.root,text = " 실시간검사 시작 ",command = out_of)
        OK.grid(column = 2,row = 2)
