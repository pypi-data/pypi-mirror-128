#! /usr/bin/python
import json
import os
from datetime import datetime

from src.url_is_reacheable import check


def check_urls_by_json_file(in_json_file_path, out_json_report_folder_path):
    output = dict()
    output["report"] = []
    if in_json_file_path == '':
        print("Path of in JSON file cannot be empty")
        return -1
    elif out_json_report_folder_path == '':
        print("Path of out JSON file cannot be empty")
        return -1

    try:
        f = open(in_json_file_path, )
    except OSError as errOpenFile:
        print("File cannot be open")
        return -1
    try:
        data = json.load(f)
    except ValueError as err:
        print("JSON file cannot be loaded")
        return -2

    try:
        for i in data['urls']:
            output["report"].append(check(i))
    except KeyError as err:
        print("Error during parsing JSON file, urls array are wait")
        return -3

    path_file_output = os.path.join(out_json_report_folder_path,
                                    "report_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".json")
    print("Result exported in " + path_file_output)
    f.close()
    with open(path_file_output, 'w') as outfile:
        json.dump(output, outfile, indent=4)
    return 0


def check_urls_by_string(list_urls_json):
    output = dict()
    output["report"] = []
    if list_urls_json == '':
        print("List cannot be empty")
        return -1
    print(str(list_urls_json))

    try:
        for i in list_urls_json['urls']:
            output["report"].append(check(i))
    except KeyError as err:
        print("Error during parsing JSON file, urls array are wait")
        return -3

    path_file_output = os.path.join(os.path.dirname(os.path.abspath(__file__)), '../backup',
                                    "report_" + datetime.now().strftime('%Y%m%d_%H%M%S') + ".json")
    print("Result save in " + path_file_output)
    with open(path_file_output, 'w') as outfile:
        json.dump(output, outfile, indent=4)
    return output
