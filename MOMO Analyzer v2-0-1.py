import sys
import os
import glob
from IPython import display
from tkinter import *
import tkinter.messagebox
import ultralytics
from ultralytics import YOLO
from IPython.display import display, Image
import numpy as np
from PIL import ImageTk,Image
#import PIL.Image
from itertools import product
from tkinter.filedialog import askdirectory
from tkinter.filedialog import askopenfilename
import math
from skimage import measure, io, img_as_ubyte
import matplotlib.pyplot as plt
import pandas as pd
import torchvision.transforms as T
from tkinter import messagebox
from datetime import date,datetime
from setuptools import setup
from multiprocessing import Process, freeze_support
freeze_support()
application_path =os.path.dirname(sys.executable)
now = datetime.now()
current_time = now.strftime("%H-%M-%S")
today = str(date.today())
default_path =  str(os.getcwd())+ "/" + today + ".csv"
#print(default_path)
area = 0;diameter=0;intensity=0;solidity=0;area_mc=0;diameter_mc=0
#INTERFACE---------------------------------------------------------
UI = Tk()
UI.geometry('500x250')
UI.minsize(500, 250)
UI.maxsize(500, 250)
UI.title('MOMO ML-BASED Alpha Track Analyser version 2.0.2 by: Pannathad ( updated:7 NOV 2023 )')
img2 = ImageTk.PhotoImage(Image.open("MOMO (6).png"))

UI.config(bg='#21618C')
Font_tuple = ("Bahnschrift",10)
pv = DoubleVar()
pv2 = DoubleVar()
var_chk1 = IntVar()
var_chk2 = IntVar()

#global area,diameter,intensity,solidity,area_mc,diameter_mc
scale = pv.get()

#tiling image function
def tile(filename, dir_in, dir_out, d):
    name, ext = os.path.splitext(filename)
    img = Image.open(os.path.join(dir_in, filename))
    w, h = img.size
    if w*h <= 0:
      messagebox.showwarning("Warning", "image size is not correct" )
    else:
        s = math.sqrt((w*h)/24)
        d = int(s)    
    print(filename,":image size = ",w,h)
    print('tiled image size = ',d,'x',d,'pixels')
    grid = product(range(0, h-h%d, d), range(0, w-w%d, d))
    for i, j in grid:
        box = (j, i, j+d, i+d)
        out = os.path.join(dir_out, f'{name}_{i}_{j}{ext}')
        img.crop(box).save(out)

#-------------------------------------------------------------------
def CSV(x,a,name,csv_path,count_each):
    scale = pv.get()
    #print(scale)
    #print(csv_path)
    for i in range(len(a)):
        img = np.array(T.ToPILImage()(a[i]))
        from skimage.filters import threshold_local
        threshold = threshold_local(img)

        thresholded_img = img < threshold
        plt.imshow(thresholded_img)
        #plt.show()

        from skimage.segmentation import watershed
        edge_touching_removed = watershed(thresholded_img)
        plt.imshow(edge_touching_removed)
        label_image = measure.label(edge_touching_removed, connectivity=img.ndim)
        all_props=measure.regionprops(label_image, img)

        props = measure.regionprops_table(label_image, img, 
                                  properties=[
                                              'area', 'equivalent_diameter',
                                              'mean_intensity', 'solidity'])
        df = pd.DataFrame(props)
        #print(df.iloc[1]['area'],df.iloc[1]['equivalent_diameter'],df.iloc[1]['mean_intensity'])
        df.insert(0,'Name',name)
        df.insert(1,'Count',count_each)
        df = df[df['area'] < 10000]
        df = df[df['area'] > 1]
        df['area_sq_microns'] = df['area'] * (scale**2)
        df['equivalent_diameter_microns'] = df['equivalent_diameter'] * (scale)
        global area,diameter,intensity,solidity,area_mc,diameter_mc
        
        area += df.iloc[0]['area']
        diameter += df.iloc[0]['equivalent_diameter']
        intensity += df.iloc[0]['mean_intensity']
        solidity += df.iloc[0]['solidity']
        area_mc  += df.iloc[0]['area_sq_microns']
        diameter_mc += df.iloc[0]['equivalent_diameter_microns']
        
        
        if x == 0:
            df.to_csv(csv_path,mode='a',index=False,header=True)
            x+=1
        else:
            df.to_csv(csv_path,mode='a',index=False,header=False)
            x+=1
            #print('lap:',x)
        #print(df.head())
#-------------------------------------------------------------------

def excel():
    path = str(askdirectory())
    global default_path
    default_path = path + "/" + today + "  " + current_time + ".csv"
    b1.config(state='normal')
    #print(area)
    return  default_path

def select():
    confident = pv2.get()
    print(confident)
    lap = 0
    s1 = False
    s2 = False
    c_value = var_chk1.get()
    c_value2 = var_chk2.get()
    if c_value == 1:
        s1 = True
    else:
        pass
    if c_value2 == 1:
        s2 = True
    else:
        pass
    try:
        path = str(askdirectory()) #picture folder path
        path2 = path + "/tiled folders" + " " + today + " " + current_time #tiled pic folder path
        os.mkdir(path2) # create tiled folder in path
        allfn = os.listdir(path) #list all pic in folder
        i = 0
        for f in allfn:
            global area,diameter,intensity,solidity,area_mc,diameter_mc
            area = 0;diameter=0;intensity=0;solidity=0;area_mc=0;diameter_mc=0
            if ".JPG" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".JPG",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            elif ".jpg" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".jpg",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            if ".JPEG" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".JPG",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            elif ".jpeg" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".jpg",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            
            elif ".PNG" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".PNG",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            elif ".png" in f:
                i+=1
                name = f
                #fd1 = "/tile"+str(i)
                fd1 = "/"+str(f.replace(".png",""))
                #print(fd1)
                pathf =path2+fd1
                #print(pathf)
                os.mkdir(pathf)
                tile(name,path,pathf,500)
            else:
                pass
                #print("not .JPG")
            model = YOLO("MOMOv2-0-1.pt")
        allfn2 = os.listdir(path2)

        
        for y in allfn2: #list all pic folder in tiled folder
            x = path2 + "/" + y
            allpic = os.listdir(x)
            #print(allpic)
            total_count = 0
            for k in allpic: # list all picture in one tiled pic
                DSC = x + "/" + k
                #print(DSC)
                results = model.predict(source=DSC, conf=confident,save=s1,save_txt=s1,boxes = True,retina_masks = True,iou = 0.1,show=s2)
                for i in range(len(results)):
                    result = results[i]
                    masks = result.masks # tensor array show in binary values

                    if masks == None:
                        pass
                        #print('None is detected')
                    else:   
                        a = result.masks.data #store all mask in list a
                        #print(k,':scale:',scale,'micron/pixcel::count:',len(masks),'count')
                        total_count += len(masks)
                        count_each = len(masks)
                        CSV(lap,a,k,default_path,count_each)
                
                lap +=1
            print(y,': total count =',total_count)
            data = np.array([[]])
            dn = pd.DataFrame(data)
            k2 = k.replace("_500_500","")
            dn.insert(0,'Name',k2)
            dn.insert(1,'Total_count',total_count)
            if total_count == 0:
                dn.insert(2,'Avr Area',area)
                dn.insert(3,'Avr diameter',diameter)
                dn.insert(4,'Avr intensity',intensity)
                dn.insert(5,'Avr solidity',solidity)
                dn.insert(6,'Avr area in micron',area_mc)
                dn.insert(7,'Avr diameter in micron',diameter_mc)
                
            else:
                dn.insert(2,'Avr Area',area/total_count)
                dn.insert(3,'Avr diameter',diameter/total_count)
                dn.insert(4,'Avr intensity',intensity/total_count)
                dn.insert(5,'Avr solidity',solidity/total_count)
                dn.insert(6,'Avr area in micron',area_mc/total_count)
                dn.insert(7,'Avr diameter in micron',diameter_mc/total_count)
            new_path = default_path.replace(".csv","")+' result'+'.csv'
            #print(os.getcwd())
            dn.to_csv(new_path,mode='a',index=False,header=True)
            area = 0;diameter=0;intensity=0;solidity=0;area_mc=0;diameter_mc
            print(path)
            message = "Files has been saved at :"+path
        messagebox.showinfo("Detection completed", message )
    except FileExistsError as e:
        print(e)
        messagebox.showwarning("Warning", "This folder has already been detected; please choose another folder." )
    except PermissionError as e2:
        print(e2)
        messagebox.showwarning("Warning", "Please choose another folder or close the related running file or folder." )
    #except Exception as e3:
        #print('An Error has occured:',e3)
        #messagebox.showwarning("Warning", "An error has occurred. Please restart the program." )
    
#Widgets---------------------------------------------------------------------------

Label(image =img2,bg='#21618C').place(anchor=NW)
b1 = Button(UI,text='DETECT',command = select,width=30,height=1,state = DISABLED,bg = '#79ECE5',font=Font_tuple)
b1.place(x=250,y=200)
b2 = Button(UI,text='SELECT SAVE FOLDER',command = excel,width=30,height=1,bg = '#79ECE5',font=Font_tuple).place(x=250,y=165)
Label(text='SCALE :',bg = '#21618C',font=Font_tuple).place(x=250,y=50)
Label(text='CONFIDENT LEVEL:',bg = '#21618C',font=Font_tuple).place(x=250,y=80)
Label(text=' micron/pixel',bg = '#21618C',font=Font_tuple).place(x=350,y=50)
Label(text='SETTING',bg = '#79ECE5',font=Font_tuple).place(x=250,y=20)
#Label(image =img,bg='#76D7C4').grid(row=9,column=0,sticky=W)
scaleinput= Entry(UI,textvariable=pv,width=5)
scaleinput.delete(0,2)
scaleinput.insert(0,0.6)
scaleinput.place(x=310,y=50)
scaleinput2= Entry(UI,textvariable=pv2,width=5)
scaleinput2.delete(0,2)
scaleinput2.insert(0,0.38)
scaleinput2.place(x=370,y=80)

c1 = Checkbutton(UI,text='save post-processing images',font=Font_tuple,variable=var_chk1, onvalue=1, offvalue=0,bg = '#21618C')
c2 = Checkbutton(UI,text='show images during the process',font=Font_tuple,variable=var_chk2, onvalue=1, offvalue=0,bg = '#21618C')
c1.place(x=250,y=100)
c2.place(x=250,y=130)
UI.mainloop()     
