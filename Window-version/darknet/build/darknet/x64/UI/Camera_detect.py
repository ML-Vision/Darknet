from tkinter import *
import os
import UI.my_path as mp

class camera_detect():
    cfg  = ""
    data = ""
    weights = ""
    name = ""
    filepath = ""
    def __init__(self,root):
        self.root = root
        self.root.title("Camera Detect")
        self.root.geometry("700x100")
        self.my_name = ""
        def set_model():
            SEL = Tk()
            model_box = Listbox(SEL,height=0,selectmode = "browse")
            folder_name =  mp.model_names() # os.listdir(os.path.dirname(os.path.abspath(__file__))+"/../models")
            for i,name in enumerate(folder_name):
                model_box.insert(i,name)
            model_box.grid(column = 0,row = 0,padx = 10,pady = 10)
            
            def data():
                selection = model_box.curselection()
                self.my_name = folder_name[selection[0]]
                Model_path["text"] = self.filepath = "./models/"+self.my_name
                file_list = os.listdir(self.filepath)
                print(file_list)
                for f in file_list:
                    if f[-3:] =="cfg":
                        self.cfg = f
                    elif f[-4:]=="data":
                        self.data = f
                    elif f[-7:] == "weights":
                        self.weights = f
                SEL.destroy()
                
            Button(SEL,text = "선택" , command = data).grid(column = 0,row = 1,padx = 10,pady = 10)


        def out_of():
            instrument = "start python ./CAM.py --config_file "+self.filepath +"/"+self.cfg + " --data_file "+self.filepath+"/"+self.data+" --weights "+self.filepath+"/"+self.weights + "  --model_name ./CAM_Detections/" + self.my_name + '/'
            print(instrument)
            os.system(instrument)
        def web_out_of():
            instrument = "start python ./CAM.py --config_file "+self.filepath +"/"+self.cfg + " --data_file "+self.filepath+"/"+self.data+" --weights "+self.filepath+"/"+self.weights + "  --model_name ./CAM_Detections/" + self.my_name + '/' + " --web_cam True"
            print(instrument)
            os.system(instrument)

        Model = Label(self.root,text = "Model Path: ",font = ("Times","15")).grid(column = 0,row = 1)
        Model_path = Label(self.root,text = "",height = 2,width = 50,borderwidth = 1,relief="groove")
        Model_path.grid(column = 1, row = 1)
        Model_set = Button(self.root,text = "Sel_path",font = ("Times","12") , command = set_model)
        Model_set.grid(column = 2,row = 1)
        
        ok_label = Label(self.root,text = "모델 선택하였으면 클릭 -> ").grid(column = 1,row = 2)
        OK = Button(self.root,text = " 실시간검사 시작 ",command = out_of)
        OK.grid(column = 2,row = 2)
        web = Button(self.root,text = " WebCAM 검사 시작 ",command = web_out_of)
        web.grid(column = 3,row = 2)
