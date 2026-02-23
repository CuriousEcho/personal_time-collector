'''
Time-collector2.1
项目简介
一个智能化本地照片工具，通过提取照片exif时间信息完成时间差计算，实现照片自动归类到目录中，并自动打印照片日期水印。

'''
import os
from pathlib import Path
import datetime
from PIL import Image,ExifTags,ImageFont,ImageDraw
import shutil
import re
import plotly.express as px
import pandas as pd
import numpy as np
                                      #第一部分，照片路径处理
def get_photo_path(path):
    p=Path(path)
    photo_list=[] 
    if p.is_dir():
        p=os.walk(p)
        for root,dirs,files in p:
            for file in files:
                if file.endswith((".jpg",".png",".jpeg",".bmp")):
                    p=Path(root)/file
                    p=p.resolve()
                    p=p.expanduser()
                    photo_list.append(p)
        return photo_list
    elif p.is_file():
        if p.suffix.lower() in [".jpg",".png",".jpeg",".bmp"]:
            p=p.resolve()
            p=p.expanduser()
            photo_list.append(p)
            return photo_list
                                      #第二部分，照片时间提取
def get_photo_time(photo_list):
    time_code=[36867,36868,306]
    photo_dict={}
    for photo in photo_list:
        with Image.open(photo) as img:
            exif=img.getexif()
            if exif:
                try:
                    for code in time_code:
                        if code in exif.keys():
                            time_str=exif[code]
                            time_str=time_str.replace(":","-")
                            time_str=time_str.replace(" ","-")
                            time_str=time_str.replace(".","-")
                            time_str=time_str.replace(",","-")
                            time_str=time_str.replace("/","-")
                            time_str=time_str.replace("UTC","")
                            photo_time=datetime.datetime.strptime(time_str,"%Y-%m-%d-%H-%M-%S")
                            photo_dict[photo]=photo_time
                            break
                        else:
                            try:
                                if re.search(r"\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}",str(photo.stem)):
                                    match=re.search(r"\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}",str(photo.stem))
                                    photo_time=datetime.datetime.strptime(match.group(),"%Y%m%d_%H%M%S")
                                    photo_dict[photo]=photo_time
                                elif re.search(r"\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}",str(photo.stem)):
                                    match=re.search(r"\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}",str(photo.stem))
                                    photo_time=datetime.datetime.strptime(match.group(),"%Y%m%d%H%M%S")
                                    photo_dict[photo]=photo_time
                            except Exception as e:
                                print("这类有exif信息但没时间信息的照片出现错误：",e)
                                continue
                except Exception as e:
                    print("出现错误：",e)
            elif not exif:
                try:
                    if re.search(r"\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}",str(Path(photo).stem)):
                        match=re.search(r"\d{4}\d{2}\d{2}\d{2}\d{2}\d{2}",str(Path(photo).stem))
                        photo_time=datetime.datetime.strptime(match.group(),"%Y%m%d%H%M%S")
                        photo_dict[photo]=photo_time
                    elif re.search(r"\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}",str(Path(photo).stem)):
                        match=re.search(r"\d{4}\d{2}\d{2}_\d{2}\d{2}\d{2}",str(Path(photo).stem))
                        photo_time=datetime.datetime.strptime(match.group(),"%Y%m%d_%H%M%S")
                        photo_dict[photo]=photo_time
                except Exception as e:
                    print("出现错误：",e)
    return photo_dict
                                      #第三部分：照片归类
def photo_classify(照片与对应时间字典):
    des副本=Path(r"副本")
    Path(des副本).mkdir(parents=True,exist_ok=True)
    for photo,photo_time in 照片与对应时间字典.items():
         #自动批量打印照片日期水印
         shutil.copy2(Path(photo),des副本)
         with Image.open(photo) as img:
             font=ImageFont.truetype(r"c:\WINDOWS\Fonts\MSYH.TTC",size=img.width*0.1)
             img.convert("RGBA")
             draw=ImageDraw.Draw(img)
             dt=datetime.datetime.strftime(photo_time,"%Y-%m-%d %H:%M:%S")
             i=draw.textbbox((0,0),dt)
             w,h=i[2]-i[0],i[3]-i[1]
             Dl=20
             draw.text((img.width-Dl-w,img.height-Dl-h),str(photo),fill=(255,255,255,128),font=font)
             img.convert("RGB")
             img.save(photo)             
         #照片分类
         if (photo_time.year==2018 and photo_time.month>=9) or (photo_time.year==2020 and photo_time.month>9) or (photo_time.year==2021 and photo_time.month<9):
             des=Path(r"C:/Users/32040/Desktop/时光收集册/2018.9-2021.8我的初中时代")
             Path(des).mkdir(parents=True,exist_ok=True)
             shutil.copy2(photo,des)
         elif (photo_time.year==2021 and photo_time.month>=9) or (photo_time.year==2022 and photo_time.month<9) or (photo_time.year==2023 and photo_time.month<9):
             des=Path(r"C:/Users/32040/Desktop/时光收集册/2021.9-2023.8真是爽苦的高中")
             Path(des).mkdir(parents=True,exist_ok=True)
             shutil.copy2(photo,des)
         elif (photo_time.year==2024 and photo_time.month>=9) or (photo_time.year==2025 and photo_time.month<9):
             des=Path(r"C:/Users/32040/Desktop/时光收集册/2024.9-2025.8拖着行李箱的秋天")
             Path(des).mkdir(parents=True,exist_ok=True)
             shutil.copy2(photo,des)
         elif (photo_time.year==2025 and photo_time.month>=9) or (photo_time.year==2026 and photo_time.month<9):
             des=Path(r"C:/Users/32040/Desktop/时光收集册/2025.9-2026.8存活至今")
             Path(des).mkdir(parents=True,exist_ok=True)
             shutil.copy2(photo,des)
         else:
             des=Path(r"C:/Users/32040/Desktop/时光收集册/清朝老照片")
             Path(des).mkdir(parents=True,exist_ok=True)
             shutil.copy2(photo,des)
         
             #此处可以继续添加更多分类条件
    


    


                                     #第四部分：用户输入与程序反馈
input_path=input("请输入照片路径：")
input_path=get_photo_path(input_path)
photo_dict=get_photo_time(input_path)
photo_classify(photo_dict)
print("照片归类完成！")






    

    


    



           
                        
              
              
            
            




                    



                 



