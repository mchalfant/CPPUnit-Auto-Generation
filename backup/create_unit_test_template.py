import os
import re
from collections import deque

class create_unit_test_template():

    def __init__(self):
        self.__src__declaration_pattern = r".*\)(\n|{)"
        self.__exclude_from_global_search = r"^(((?!utilities)(?!Utilities).)*$"
        self.__separate_header_abstraction = r"(private:|public:)[\s\S]*?(?=\n.*?=|}|(private:|public:))"
        self.__get_methods_pattern = r".*\(.*\);"
        self.__include_header_pattern = r"(.*.h\"|.*>)"

    def get_header_dirpath(self, arr):
        header_arr = []
        for dirname in arr:
            if(re.search(self.__exclude_from_global_search, dirname)):
                header_arr.append(dirname + "global")
            else:
                header_arr.append(dirname)
        return header_arr

    #Not Sure: How to implement nested classes
    def get_header_data(self, pathname):
        header_method_arr = []
        abstraction_queue = deque()
        is_public_method = False
        with open(pathname, "r") as new_file:
            all_lines = new_file.readlines()
            
        for lines in all_lines:
            # Keeps track of Header File Abstraction 
            if (re.search(r"{", lines)):
                abstraction_queue.append(lines)
            elif (re.search(r"}", lines)):
                abstraction_queue.pop()

            # Adds C++ Class/Struct Definitions to Array
            if (bool(abstraction_queue)):
                if (re.search("private:", lines)):
                    is_public_method = False
                elif (re.search("public:", lines)):
                    is_public_method = True
                elif (re.search(self.__get_methods_pattern, lines) and is_public_method):
                    header_method_arr.append(lines)
                else:
                    pass
            elif (re.search(self.__get_methods_pattern, lines)):
                header_method_arr.append(lines)

        return header_method_arr

    def get_source_data(self, pathname):
        source_data_arr = [[],[]]
        with open(pathname, "r") as new_file:
            all_lines = new_file.readlines()

        for line in all_lines:
            #Gets Header Files in Source Files
            if (re.search(self.__include_header_pattern, line)):
                source_data_arr[0].append(line)
            #Gets Source Declarations
            elif (re.search(self.__src__declaration_pattern, line)):
                source_data_arr[1].append(line)
            else:
                pass
        return source_data_arr

    def filter_private_declaration(self, header_arr, source_arr):
        

    

            



            