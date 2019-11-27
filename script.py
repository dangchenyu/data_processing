import os
import cv2
import numpy as np


def main(cabin_img_path, label_path, object_img_path, cabin_label_path, save_path,
         seat_region=(700, 580)):
    overlap_img = _count_overlap()
    last_image_name = ''
    o = open(label_path, 'r')
    label_list = o.readlines()
    cabin_label_list = os.listdir(cabin_label_path)
    with open(save_path + "new_label.txt", 'a+') as f:
        for i, item in enumerate(label_list):
            if_write = True
            item_list = item.split()
            image_name = item_list[0]
            image_label = item_list[-1]
            if image_name == last_image_name:
                continue
            last_image_name = image_name
            if image_name in overlap_img:
                pts_list = []
                for overlap in label_list[i + 1:]:
                    overlap_list = overlap.split()
                    overlap_image_name = overlap_list[0]
                    overlap_image_label = overlap_list[-1]
                    if overlap_image_label == '1' and overlap_image_name == image_name:
                        pts_list.append(overlap_list[1:-1])
                    else:
                        break
            points_int = map(eval, item_list[1:-1])
            point_list = list(points_int)
            point_np = np.array(point_list).reshape(-1, 2).astype(np.int32)
            img = cv2.imread(object_img_path + image_label + '\\' + image_name)
            if img is None:
                continue
            region = cv2.boundingRect(point_np)
            x, y, w, h = region
            cropped = img[y:y + h, x:x + w].copy()
            mask = np.zeros(cropped.shape[:2], np.uint8)
            pts = point_np - point_np.min(axis=0)
            cv2.drawContours(mask, [pts], -1, (255, 255, 255), -1, cv2.LINE_AA)
            if pts_list is not None:
                pts_overlap_list = []
                for x, pts_overlap in enumerate(pts_list):
                    pts_overlap_int = map(eval, pts_overlap)
                    pts_overlap_int_list = list(pts_overlap_int)
                    pts_overlap_int_list_np = np.array(pts_overlap_int_list).reshape(-1, 2).astype(np.int32)
                    pts_overlap_list.append(pts_overlap_int_list_np)
                    pts_temp = pts_overlap_list[x] - point_np.min(axis=0)
                    cv2.drawContours(mask, [pts_temp], -1, (0, 0, 0), -1, cv2.LINE_AA)

            # cv2.imshow('test2', mask)
            # cv2.waitKey()
            ret, mask = cv2.threshold(mask, 175, 255, cv2.THRESH_BINARY)
            if mask is None:
                continue
            cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
            random_scale = np.random.random()
            temp = np.array(list(cropped.shape[:2]))
            new_scale = temp * random_scale
            if image_label == "2":
                object_thres = [60, 100]
            elif image_label == "3":
                object_thres = [50, 100]
            elif image_label == '4':
                object_thres = [150, 300]
            new_scale = np.where(new_scale > object_thres[1], object_thres[1], new_scale).astype(np.int32)
            new_scale = np.where(new_scale < object_thres[0], object_thres[0], new_scale).astype(np.int32)

            if np.random.rand() > 0.5:
                random_degree = np.random.randint(0, 360)
                mask = _rot_degree(mask, random_degree)
                cropped = _rot_degree(cropped, random_degree)

            mask = cv2.resize(mask, tuple(new_scale))

            mask_inv = cv2.bitwise_not(mask)
            img_rand = np.random.randint(0, len(cabin_label_list))
            origin, exist_obj, origin_label, origin_name = _get_img(cabin_label_path, cabin_label_list, cabin_img_path,
                                                                    img_rand)
            temp_para = 360
            pos_y = np.random.randint(0, origin.shape[0] - seat_region[0] - mask.shape[0])
            pos_x = np.random.randint(0, origin.shape[1] - temp_para - seat_region[1] - mask.shape[1])
            paste_region_y = seat_region[0] + pos_y
            paste_region_x = seat_region[1] + pos_x
            paste_region_w = mask.shape[1]
            paste_region_h = mask.shape[0]
            roi = origin[paste_region_y:paste_region_y + paste_region_h,
                  paste_region_x:paste_region_x + paste_region_w]
            if exist_obj is not None:
                for obj in exist_obj:
                    obj_int = map(eval, obj)
                    obj_int_list = list(obj_int)
                    try:
                        iou = _cal_iou([obj_int_list[0], obj_int_list[1], obj_int_list[2] - obj_int_list[0],
                                        obj_int_list[3] - obj_int_list[1]],
                                       [paste_region_x, paste_region_y, paste_region_w, paste_region_h])
                    except IndexError:
                        continue
                    if iou > 0.3:
                        if_write = False
                        break
            if if_write is True:
                img1_bg = cv2.bitwise_and(roi, roi, mask=mask_inv)

                cropped = cv2.resize(cropped, tuple(new_scale))
                img2_fg = cv2.bitwise_and(cropped, cropped, mask=mask)

                img1_bg = cv2.cvtColor(img1_bg, cv2.COLOR_BGR2GRAY)
                origin = cv2.cvtColor(origin, cv2.COLOR_BGR2GRAY)

                dst2 = cv2.add(img1_bg, img2_fg)
                origin[seat_region[0] + pos_y:seat_region[0] + mask.shape[0] + pos_y,
                seat_region[1] + pos_x:seat_region[1] + mask.shape[1] + pos_x] = dst2
                img_name_new = os.path.splitext(origin_name)[0] + '_' + str(np.random.randint(0, 100000)) + '.jpg'
                origin_label[0] = img_name_new
                origin_label_str = ' '.join(origin_label)
                f.write(origin_label_str + ' ' + str(seat_region[1] + pos_x) + ' ' + str(
                    seat_region[0] + pos_y) + ' ' + str(
                    seat_region[1] + pos_x + mask.shape[1]) + ' ' + str(
                    seat_region[0] + pos_y + mask.shape[0]) + ' ' + str(
                    image_label) + '\n')
                cv2.imwrite(save_path + img_name_new, origin)

            else:
                continue

                #
                # f.write(image_name + ' ' + str(seat_region[1] + pos_x) + ' ' + str(seat_region[0] + pos_y) + ' ' + str(
                # mask.shape[1]) + ' ' + str(mask.shape[0]) + ' ' + str(image_label) + '\n')
                # cv2.imwrite("D:\\cabin_data\\temp1\\" + image_name, origin)

    f.close()


def _rot_degree(img, degree):
    rows, cols = img.shape
    center = (cols / 2, rows / 2)
    M = cv2.getRotationMatrix2D(center, degree, 1)
    top_right = np.array((cols - 1, 0)) - np.array(center)
    bottom_right = np.array((cols - 1, rows - 1)) - np.array(center)
    top_right_after_rot = M[0:2, 0:2].dot(top_right)
    bottom_right_after_rot = M[0:2, 0:2].dot(bottom_right)
    new_width = max(int(abs(bottom_right_after_rot[0] * 2) + 0.5), int(abs(top_right_after_rot[0] * 2) + 0.5))
    new_height = max(int(abs(top_right_after_rot[1] * 2) + 0.5), int(abs(bottom_right_after_rot[1] * 2) + 0.5))
    offset_x = (new_width - cols) / 2
    offset_y = (new_height - rows) / 2
    M[0, 2] += offset_x
    M[1, 2] += offset_y
    dst = cv2.warpAffine(img, M, (new_width, new_height))

    return dst


def _get_img(cabin_label_path, cabin_label_list, cabin_img_path, index):
    label_current = cabin_label_list[index]
    o = open(cabin_label_path + label_current)
    label = o.readline()
    label_list = label.split()
    img = cv2.imread(cabin_img_path + label_list[0])
    exist_obj = []
    for ind, i in enumerate(label_list[1:]):
        if i == '2' or i == '3' or i == '4':
            exist_obj.append(label_list[ind - 3:ind + 1])
    return img, exist_obj, label_list, label_list[0]


def _count_overlap():
    o = open("C:\\Users\DELL\\PycharmProjects\\data_processing\\191018_#3802.txt", 'r')
    label_list = o.readlines()
    overleap_img = []
    for item in label_list:
        item_list = item.split()
        image_name = item_list[0]
        image_label = item_list[-1]
        if image_label == '1':
            overleap_img.append(image_name)
    return overleap_img


def _cal_iou(box_a, box_b):
    np_x = np.array([box_a[0], box_b[0]])
    np_w = np.array([box_a[2], box_b[2]])
    np_y = np.array([box_a[1], box_b[1]])
    np_h = np.array([box_a[3], box_b[3]])
    # judge if have intersection or not
    if (abs(box_a[0] - box_b[0]) < np_w[np_x.argmin()]) and (abs(box_a[1] - box_b[1]) < np_h[np_y.argmin()]):
        box_area = box_a[2] * box_a[3] + box_b[2] * box_b[3]
        q_area = (np_x.min() + np_w[np_x.argmin()] - np_x.max()) * (np_y.min() + np_h[np_y.argmin()] - np_y.max())
        iou_c = q_area / (box_area - q_area)
    else:
        iou_c = 0
    return iou_c


if __name__ == '__main__':
    for i in range(2):
        main("D:\\cabin_data\\images\\",
             "C:\\Users\\DELL\\PycharmProjects\\data_processing\\191018_#3802.txt",
             "C:\\Users\\DELL\\PycharmProjects\\data_processing\\images_objects\\",
             "D:\\cabin_data\\labels\\",
             "D:\\cabin_data\\pasted\\"
             )
