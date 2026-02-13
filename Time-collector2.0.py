'''
Time-collector2.0
项目简介
一个智能化本地照片工具，通过提取照片exif时间信息完成时间差计算，实现照片自动归类到目录中。
创作人：zlj
本次重构是一次**根本性的进化**，主要改进如下：
1、数据源优化：新增对照片EXIF信息提取，提升时间信息的准确性,对于部分照片缺少EXIF信息的照片，可通过文件名提取时间信息。
2、代码现代化：将原程序中的os模块替代为pathlib模块，提升代码可读性和路径操作安全性。
3、算法优化：将原来只能按2025到2026年月份分类的模式改进为按时间差分类，可处理更多照片
'''
import os
from pathlib import Path
import datetime
from PIL import Image,ExifTags
import shutil
import re
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
    for photo,photo_time in 照片与对应时间字典.items():
         print(photo)
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







    

    


    



           
                        
              
              
            
            




                    



                 



