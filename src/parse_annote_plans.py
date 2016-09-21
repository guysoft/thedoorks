#!/usr/bin/env python
import os.path
import json
import argparse

def get_bounding_box(points):
    left = int(points[0][0])
    top = int(points[0][1])
    right = int(points[0][0])
    bottom= int(points[0][1])

    for point in points:
        point = [int(point[0]), int(point[1])]
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
    
    
if __name__ == "__main__":
    test_image = "/tmp/annote.svg"
    
    print(json.dumps(prase_svg(hangleArgs().svg_file)))
