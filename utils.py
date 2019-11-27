import cv2
import os
import shutil
import json
import numpy as np
def crop_img(img_path):
    o=open('C:\\Users\\DELL\\Desktop\\#4561_p.txt')
    list_label=o.readlines()
    for item in list_label:
        item_list=item.split()
        region = map(eval, item_list[1:5])
        region = map(int, region)
        rand_lt=np.random.randint(-100,100,(2))
        rand_rb=np.random.randint(-100,100,(2))

        region=list(region)
        region_new=[region[0]-rand_lt[0],region[1]-rand_lt[1],region[2]+rand_rb[0],region[3]+rand_rb[1]]
        for ind,i in enumerate(region_new):
            if ind<=1:
                if i < 0:
                    region_new[ind]=0
            elif ind ==2:
                if i >1920:
                    region_new[ind] = 1920
            else:
                if i>1280:
                    region_new[ind]=1280
        img=cv2.imread(img_path+item_list[0])
        img=img[region_new[1]:region_new[1]+region_new[3],region_new[0]:region_new[0]+region_new[2]]
        # cv2.imshow('test',img)
        # cv2.waitKey()
        cv2.imwrite('H:\\#4561part1_cropped\\'+item_list[0],img)
        print('writing',item_list[0])

def classify_img():
    o=open("C:\\Users\\DELL\\PycharmProjects\\data_processing\\191018_#3802.txt")
    label_list = o.readlines()
    for i, item in enumerate(label_list):
        item_list = item.split()
        image_name = item_list[0]
        image_label = item_list[-1]
        if image_label=='2':
            shutil.copy("C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\"+image_name,
                        'C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\2')
        elif image_label=='3':
            shutil.copy("C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\"+image_name,
                        'C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\3')
        elif image_label=='4':
            shutil.copy("C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\"+image_name,
                        'C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\4')
        else:
            continue

def move_pic(label_path):
    list = os.listdir(label_path)
    list.sort()

    for index, i in enumerate(list):

        new_path = os.path.join(label_path, i)

        if os.path.isdir(new_path):
            move_pic(new_path)

        if os.path.isfile(new_path):
            if 'jpg' in new_path:
                shutil.copy(new_path,
                            'D:\\cabin_data\\images_objects\\')


def delete_pic(pic_path):
    list = os.listdir(pic_path)
    list.sort()
    for x in test_list:
        basename = os.path.splitext(x)[0]
        for index, i in enumerate(list):
            if os.path.isfile(i):
                if 'jpg' in i:
                    if basename in i:
                        os.remove(i)
def make_video_from_images(img_paths, outvid_path, fps=20, size=None,
               is_color=True, format="XVID"):
    from cv2 import VideoWriter, VideoWriter_fourcc, imread, resize
    fourcc = VideoWriter_fourcc(*format)
    vid = None
    img_list=os.listdir(img_paths)
    img_list.sort()
    for img in img_list:
        img_path=img_paths+img
        if not os.path.exists(img_path):
            raise FileNotFoundError(img_path)
        img = imread(img_path)
        if img is None:
            print(img_path)
            continue
        if vid is None:
            if size is None:
                size = img.shape[1], img.shape[0]
            vid = VideoWriter(outvid_path, fourcc, float(fps), size, is_color)

        if size[0] != img.shape[1] and size[1] != img.shape[0]:
            img = resize(img, size)
        vid.write(img)
    vid.release()
    return vid



def delete_json(json_file):
    with open(json_file) as ajson:
        anno = json.load(ajson)

    new_list = []
    for a in anno:
        for i in test_list:
            basename = os.path.splitext(i)[0]

            if basename in a['image_name']:
                add = False
                break
            else:
                add = True
        if add is True:
            new_list.append(a)

    with open("C:\\Users\\DELL\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\annot\\temp.json",
              "w+") as f:
        json.dump(new_list, f)
        print("加载入文件完成...")
    ajson.close()
    f.close()
def count_num(json_file):
    i=0
    with open(json_file) as ajson:
        anno = json.load(ajson)
    for a in anno:
        i+=1
    print(i)

if __name__ == '__main__':

    test_list = ['NJ_Y_Y_90_20190814_081400_b4573c64.avi',
                 'NJ_Y_Y_90_20190814_081400_cd097d2b.avi ',
                 'NJ_Y_Y_90_20190815_081500_4dba7e36.avi ',
                 'NJ_Y_Y_90_20190815_081500_d9e32e4d.avi ',
                 'NJ_Y_1_70_20190814_081400_5fcf5b40.avi',
                 'NJ_Y_1_70_20190902_151144_f888aba8.avi',
                 'NJ_Y_1_70_20191012_114758_d7246cac.avi',
                 'NJ_Y_1_70_20191013_170709_1f4076f8.avi',
                 'NJ_Y_1_70_20190814_081400_f610fde8.avi',
                 'NJ_Y_1_70_20190902_151640_c68322a1.avi',
                 'NJ_Y_1_70_20191012_164940_f16b9cec.avi',
                 'NJ_Y_1_70_20190815_081500_02a9176f.avi',
                 'NJ_Y_1_70_20190905_101539_5454c7bb.avi',
                 'NJ_Y_1_70_20191013_122859_881e0700.avi',
                 'NJ_Y_1_70_20190815_081500_f1c6ee45.avi',
                 'NJ_Y_1_70_20190905_120526_0b13801c.avi',
                 'NJ_Y_1_70_20191013_160139_cb79ae51.avi']
    # make_video_from_images('D:\\cabin_test\\5_10\\','D:\\cabin_test\\5_10.mp4')
    move_pic('H:\\#4368imgs\\')
    # delete_pic('C:\\Users\\DELL\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\images')
    # delete_json(
    #     'C:\\Users\\DELL\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\annot\\cabin_train.json')
    # count_num("C:\\Users\\DELL\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\annot\\temp.json")
    # classify_img()
    # crop_img('D:\\cabin_data\\#4561part1_imgs\\')
