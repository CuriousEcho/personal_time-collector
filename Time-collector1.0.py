#这是zlj做的第一个python项目，就叫它时光收集器吧
#时光收集器 - 一个用来收集并分类美好照片的小项目
                                          #第一部分：遍历目录，获取所有照片列表
import os
import shutil
from datetime import datetime
def photo_path(目录路径):
    if not os.path.exists(目录路径):
        raise ValueError("目录不存在")
    photo_list=[]
    photo_list1=os.listdir(目录路径)
    for a in photo_list1:
        full_photo_path=os.path.join(目录路径,a)
        if os.path.isfile(full_photo_path):
            b=os.path.splitext(full_photo_path)
            if b[1].lower() in [".jpg",".png",".jpeg"]:
                photo_list.append(full_photo_path)
    print(len(photo_list))
    return photo_list
                                          #第二部分：获取照片日期,并按日期分类
def photo_date(照片列表):
    base_dir=r"C:\Users\32040\Desktop"
    for 照片路径 in 照片列表:
        照片路径=os.path.normpath(照片路径)
        文件名=os.path.basename(照片路径)
        try:
          照片日期=datetime.strptime(os.path.splitext(文件名)[0],"%Y.%m.%d")
        except:
            print("照片名格式应为：年.月.日")
            continue
        年份=照片日期.year
        月份=照片日期.month
        if 月份 in[1,2,3]:
            月份="春天"
        elif 月份 in[4,5,6]:
            月份="夏天"
        elif 月份 in[7,8,9]:
            月份="秋天"
        else:
            月份="冬天"
        新路径=os.path.join(base_dir,str(年份),月份)
        os.makedirs(新路径,exist_ok=True)
        shutil.copy2(照片路径,新路径)
        
    


                                         #第三部分：获取用户输入的目录路径，并调用函数
目录路径=str(input("请输入你的文件夹路径："))
照片列表=photo_path(目录路径)
photo_date(照片列表)


        


    


        
        


    