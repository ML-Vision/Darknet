																																																																																	
from tkinter import *
import tkinter as tk
import os
import shutil
import UI as ui
from datetime import datetime
import uuid
import UI.my_path as mp


class train():
    def __init__(self,root,model_name,model_path,data_name,data_path):
        self.root = root
        #새 페이지 오픈
        self.root.title("Train_Select")
        self.root.geometry('700x200-100+100')
        
        
        def sel_data():
            SEL = Tk()
       
            model_box = Listbox(SEL,height=0,selectmode = "browse")
            folder_name = mp.Image_Train_folders()
            for i,name in enumerate(folder_name):
                model_box.insert(i,name)
            model_box.grid(column = 0,row = 0,padx = 10,pady = 10)
            
            def data():
                selection = model_box.curselection()
                set_data_path1["text"] = "./Image_to_Train/"+folder_name[selection[0]]
                set_data_name = folder_name[selection[0]]
                SEL.destroy()
                
            Button(SEL,text = "선택" , command = data).grid(column = 0,row = 1,padx = 10,pady = 10)
           

        def out_of():
            data_str = set_data_path1["text"]  #데이터의 위치
            model_name["text"] = set_model_name1.get("1.0","end")[:-1]
            model_path["text"] = os.getcwd() + "/models"
            data_name["text"] = set_data_name1["text"]
            data_path["text"] = set_data_path1["text"]
            #데이터 절대경로
            data_str = mp.str_to_path(data_str)
            name = set_model_name1.get("1.0","end")[:-1]
            if not (os.path.isdir("./models/"+set_model_name1.get("1.0","end")[:-1])):
                os.mkdir("./models/"+name)
            print(data_str,name)

            info_path = mp.join_path(mp.model_root(),name+'/information.txt')
            info = open(info_path,'w')
            info.write("ID = "+str(uuid.uuid4())+"\n")
            now = datetime.now()
            info.write("Date/Time = " + str(now)[:10] + str(now)[10:19]+"\n")
            info.write("User = "+ set_name1.get("1.0","end"))
            info.write("Model Name = "+model_name["text"]+"\n")
            info.write("Data = "+data_path["text"])
            info.close()

            #names복사해오기
            shutil.copyfile(str(data_str)+"/train/_darknet.labels" , "./models/"+name+"/obj.names")
            print(str(data_str)+"/train/_darknet.labels" , "./models/"+name+"/obj.names")
            f = open("./models/"+name+"/obj.names",'r')
            class_num = len(f.readlines())
            f.close()
            
            #data파일 작성
            obj = open("./models/"+name+"/obj.data",'w')
            obj.write("classes= " + str(class_num)+"\n")
            obj.write("train = "+data_path["text"]+"/train.txt\n")
            obj.write("valid = "+data_path["text"]+"/valid.txt\n")
            obj.write("names = ./models/"+name+"/obj.names\n")
            obj.write("backup = ./models/"+name+"/")
            obj.close()

            #cfg파일 작성
            #class_num을 class개수대로 수정
            filter_num = (class_num + 5) * 3
            max_batches = class_num * 20 # TEST 용
            # max_batches = class_num * 2000
            #if(max_batches<6000):
                #max_batches = 6000
            step1 = int(max_batches*0.8)
            step2 = int(max_batches*0.9)
            new_text_content = ''
            with open("./yolo-obj.cfg",'r') as f:
                lines = f.readlines()
                for i, l in enumerate(lines):
                    if i == 19:
                        new_string = 'max_batches = ' + str(max_batches) + '\n'
                    elif i == 21:
                        new_string = 'steps=' + str(step1) + ',' + str(step2) + '\n'
                    elif i == 962:
                        new_string = 'filters=' + str(filter_num) + '\n'
                    elif i == 969:
                        new_string = 'classes=' + str(class_num) + '\n'
                    elif i == 1050:
                        new_string = 'filters=' + str(filter_num) + '\n'
                    elif i == 1057:
                        new_string = 'classes=' + str(class_num) + '\n'
                    elif i == 1138:
                        new_string = 'filters=' + str(filter_num) + '\n'
                    elif i == 1145:
                        new_string = 'classes=' + str(class_num) + '\n'
                    else:
                        new_string = l
        
                    if new_string:
                        new_text_content += new_string
                    else:
                        new_text_content += ''
            
            with open("./models/"+name+"/yolo-obj.cfg",'w') as f:
                f.write(new_text_content)

            #train.txt 파일 작성
            f1 = os.listdir(data_path["text"]+"/train")
            imgs1 = [file for file in f1 if file.endswith(".jpg")]
            with open(data_path["text"]+"/train.txt", "w", encoding="utf-8") as wf:
                for img in imgs1:
                    data = data_path["text"]+'/train/' + img + '\n'
                    wf.write(data)
            #valid.txt 파일 작성
            f2 = os.listdir(data_path["text"]+"/valid")
            imgs2 = [file for file in f1 if file.endswith(".jpg")]
            with open(data_path["text"]+"/valid.txt", "w", encoding="utf-8") as wf:
                for img in imgs2:
                    data = data_path["text"] +'/valid/' + img + '\n'
                    wf.write(data)
            
            instrument = "start ./darknet detector train ./models/"+name+"/obj.data ./models/"+name+"/yolo-obj.cfg yolov4.conv.137"
            print(instrument)
            os.system(instrument)            
            ui.model_information()
            #self.root.destroy()

        #모델이름 select
        set_model_name0 = Label(self.root,text = "Name of Model: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 0)
        set_model_name1 = tk.Text(self.root,height = 2,width = 50)
        set_model_name1.grid(column = 1,row = 0)
        #이름설정
        set_name0 = Label(self.root,text = "만든사람 이름: ",font = ("Times","10"),borderwidth = 1).grid(column = 0,row = 1)
        set_name1 = tk.Text(self.root,height = 2,width = 50)
        set_name1.grid(column = 1,row = 1)

        #모델 데이터 select
        set_data_name0 = Label(self.root,text = "Name of Data: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 2)
        set_data_name1 = Label(self.root,text = "Data name",borderwidth = 3)
        set_data_name1.grid(column = 1, row = 2)
   
        set_data_path0 = Label(self.root,text = "Data Path: ",font = ("Times","12"),borderwidth = 1).grid(column = 0,row = 3)
        set_data_path1 = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="ridge")
        set_data_path1.grid(column = 1, row = 3)
        set_data_sel = Button(self.root,text = "Sel_path",command = sel_data,overrelief = "groove")
        set_data_sel.grid(column = 2,row = 3)

        #확인란
        ok_label = Label(self.root,text = "모두 입력 완료하였다면 클릭 ->",borderwidth = 1,relief="ridge").grid(column = 1,row = 6)
        OK = Button(self.root,text = "  학습 시작   ",command = out_of,overrelief = "solid")
        OK.grid(column = 2,row = 6)


