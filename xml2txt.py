import os
import sys
import xml.etree.ElementTree as ET
import glob


def main(indir, outdir):
    os.chdir(indir)
    annotations = os.listdir('.')
    annotations = glob.glob(str(annotations) + '*.xml')

    for i, file in enumerate(annotations):

        file_save = file.split('.')[0] + '.txt'
        file_txt = os.path.join(outdir, file_save)
        f_w = open(file_txt, 'w+')

        # actual parsing
        in_file = open(file)
        tree = ET.parse(in_file)
        root = tree.getroot()
        file_name=root[1].text
        f_w.write(file_name+' ')
        for obj in root.iter('object'):
            name = obj.find('name').text
            if name == 'dish':
                name = '1'
            elif name == 'rice':
                name = '2'
            xmlbox = obj.find('bndbox')
            xn = xmlbox.find('xmin').text
            xx = xmlbox.find('xmax').text
            yn = xmlbox.find('ymin').text
            yx = xmlbox.find('ymax').text
            # print xn
            f_w.write(xn + ' ' + yn + ' ' + xx + ' ' + yx + ' '+name+' ')
        f_w.close()


if __name__ == '__main__':
    main(indir='C:\\Users\\DELL\\Downloads\\SmartReji_Annotation\\',
         outdir='C:\\Users\\DELL\\Downloads\\SmartReji_Annotation\\')
