#!/usr/bin/env python
import os.path
import json


def get_bounding_box(points):
    left = points[0][0]
    top = points[0][1]
    right = points[0][0]
    bottom= points[0][1]

    for point in points:
        if left >  point[0]:
            left = point[0]
        if top > point[1]:
            top = point[1]
        if right < point[0]:
            right = point[0]
        if bottom < point[1]:
            bottom = point[1]
    return left, top, right, bottom


def prase_svg(file_path):
    return_value = {}
    return_value["doors"] = []
    data = None
    with open(file_path, "r") as myfile:
        data=myfile.readlines()

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

if __name__ == "__main__":
    import sys
    test_image = "/tmp/annote.svg"
    print(json.dumps(prase_svg(sys.argv[1])))
