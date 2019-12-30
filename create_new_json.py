import json
import os

def main(json_path):
    json_list=[]
    with open(json_path) as json_file:
        anno=json.load(json_file)
        for anno_img in anno:
            image_name='2_'+anno_img['image_name']
            for item in anno_img['annotations'][0]['anno']:
                new_dict={}
                new_dict['image_name']=image_name
                new_dict['anno']=item
                json_list.append(new_dict)
        str=json.dumps(json_list)
    json_file.close()
    new_json= open('D:\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\annot\\temp_back.json','w+')
    new_json.write(str)
    new_json.close()
if __name__ == '__main__':
    main('D:\\PycharmProjects\\deep-high-resolution-net.pytorch\\data\\cabin\\annot\\#5108back.json')