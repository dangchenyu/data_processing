import cv2
def main():
    o=open("C:\\Users\\DELL\\Desktop\\new_label1.txt")
    while True:
        item=o.readline()
        item_list=item.split()
        img_name=item_list[0]
        img=cv2.imread("D:\\cabin_data\\temp1\\"+img_name)
        object_num=(len(item_list)-1)/5
        for i in range(int(object_num)):
            obj_lt=(int(float(item_list[1+i*5])),int(float(item_list[2+i*5])))
            obj_br=(int(float(item_list[3+i*5])),int(float(item_list[4+i*5])))
            cv2.rectangle(img,obj_lt,obj_br,(0,255,0),3)
        cv2.imshow('test',img)
        cv2.waitKey()
if __name__ == '__main__':
    main()