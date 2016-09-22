#!/usr/bin/env python
import os.path
import glob
import json
import argparse
import cv2

def get_bounding_box(points):
    left = int(float(points[0][0]))
    top = int(float(points[0][1]))
    right = int(float(points[0][0]))
    bottom= int(float(points[0][1]))

    for point in points:
        point = [int(float(point[0])), int(float(point[1]))]
        if left >  point[0]:
            left = point[0]
        if top > point[1]:
            top = point[1]
        if right < point[0]:
            right = point[0]
        if bottom < point[1]:
            bottom = point[1]
    return left, top, right, bottom


def read_file_to_var(file_path):
    data = None
    with open(file_path, "r") as myfile:
        data=myfile.readlines()
    return data


def prase_svg(file_path):
    """
    Takes an svfile and returns a dict with the doors bounding box
    """
    return_value = {}
    return_value["doors"] = []
    data = read_file_to_var(file_path)

    for line in data:
        line=line.strip()
        if line.startswith("<polygon class=\"Door\""):

            point_list = []
            for point in line.split('"')[9].split(" ")[:-1]:
                point_data = point.strip().split(",")

                x = point_data[0]
                y = point_data[1]

                point_list.append([x,y])

                bounding_box = get_bounding_box(point_list)

            return_value["doors"].append(bounding_box)
    return return_value


def hangleArgs():
    """ Handle input flags """
    parser = argparse.ArgumentParser(add_help=True, description='Parse the strange svg format from ImagesGT')
    parser.add_argument('svg_file', type=str,
                        help='path to svg file')
    
    args = parser.parse_args()
    return args
    
BOUNDING_BOX_FD = 'BBs\\'
imglib = "D:\\ImagesGT\\"

def create_sliding_windows(stride,bb_size):
    
    dataset_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dataset")
    doors_path = os.path.join(dataset_path, "doors")
    not_doors_path = os.path.join(dataset_path, "not_doors")
    
    img = []
    for file in glob.glob(imglib +'*.svg'):
        filename= file[:file.rfind("_gt")]+".png"
        print (filename)
        img = cv2.imread(filename)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        doors = prase_svg(file)["doors"]
        
        f_name = filename.split('\\')
        f_name = f_name[len(f_name)-1].split('.')[0]
       
        i=0
        rows,cols = img.shape
        for y in range(0, cols-bb_size, stride):
            for x in range(0,rows- bb_size, stride):
                
                bb=img[x:x+bb_size, y:y+bb_size]
             #   bb = img[y:y+h,x:x+w]
                path = not_doors_path
                for door in doors:
                    if y<=door[0] and x<=door[1] and y+bb_size >= door[2] and x+bb_size >= door[3]:
                        path = doors_path
                cv2.imwrite(path + "\\" +f_name +'_'+ str(i) + '.png',bb)
                i+=1
            
            

    
    
if __name__ == "__main__":
    test_image = "/tmp/annote.svg"
    
    create_sliding_windows(50,25)
