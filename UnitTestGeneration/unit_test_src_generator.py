import os
import re
from collections import deque

class unit_test_src_generator():

    def __init__(self, dirpath, filename):
        self.__src__declaration_pattern = r".*\)(\n|{)"
        self.__exclude_from_global_search = r"^(((?!utilities)(?!Utilities).)*$"
        self.__separate_header_abstraction = r"(private:|public:)[\s\S]*?(?=\n.*?=|}|(private:|public:))"
        self.__get_methods_pattern = r".*\(.*\);"
        self.__include_header_pattern = r"(.*.h\"|.*>)"
        
        self.__source_file_path = dirpath.replace("src", "test")
        # Goes up two level for global headers
        self.__header_file_path = dirpath + "/../.." 
        self.__unit_test_path = dirpath
        self.__header_full_file_path = ""
        self.__desired_header_full_path = ""

        dirname = re.split(r"\/", dirpath)
        self.__source_dir_name = dirname[-2]
        self.__sut_full_path = self.__source_file_path + "/" + filename
        self.__new_unit_test = self.__unit_test_path + "Test" + filename


    def get_header_file(self):
        if(re.search(self.__exclude_from_global_search, self.__header_file_path)):
            self.__header_full_file_path = self.__header_file_path + "global/"                             \
                 + self.__source_dir_name + ".h"
            self.__desired_header_full_path = self.__header_full_file_path
        else:
            self.__header_full_file_path = self.__header_file_path +                                       \
                self.__source_dir_name + self.__source_dir_name + ".h"      
            self.__desired_header_full_path = self.__header_file_path + "Utilities.h"

    #Not Sure: How to implement nested classes
    def get_header_declarations(self):
        header_method_arr = []
        abstraction_queue = deque()
        is_public_method = False
        with open(self.__header_full_file_path, "r") as new_file:
            all_lines = new_file.readlines()
            
        for line in all_lines:
            # Keeps track of Header File Class Abstraction 
            if (re.search(r"{", line)):
                abstraction_queue.append(line)
            elif (re.search(r"}", line)):
                abstraction_queue.pop()

            # Adds C++ Class/Struct Definitions to Array
            if (bool(abstraction_queue)):
                if (re.search("private:", line)):
                    is_public_method = False
                elif (re.search("public:", line)):
                    is_public_method = True
                elif (re.search(self.__get_methods_pattern, line) and is_public_method):
                    line = line.lstrip()
                    header_method_arr.append(line)
                else:
                    pass

            # Once we exit the class collect all C header declarations
            elif (re.search(self.__get_methods_pattern, line)):
                line = line.lstrip()
                header_method_arr.append(line)

        return header_method_arr

    def get_source_data(self):
        source_data_arr = [[],[]]
        with open(self.__sut_full_path, "r") as new_file:
            all_lines = new_file.readlines()

        for line in all_lines:
            #Gets Include Files in Source Files
            if (re.search(self.__include_header_pattern, line)):
                line = line.lstrip()
                source_data_arr[0].append(line)
            #Gets Source File Declarations
            elif (re.search(self.__src__declaration_pattern, line)):
                line = line.lstrip()
                source_data_arr[1].append(line)
            else:
                pass
        return source_data_arr

    # Declaration Array - 0: Return Data Type | 1: Function Name | 2 and greater argument list
    def unit_test_gen(self, *decl_arr):  
        with open(self.__new_unit_test, "a+") as new_unit_test:
            
            new_unit_test.write("   //Arrange\n")
            # Return Data Type
            if (decl_arr[0] != "void"):
                new_unit_test.write("   " + decl_arr[0] + " expected = 0;\n")
            elif (re.search(r"(^|,)\*.*,", decl_arr[2])):
                new_unit_test.write("   " + decl_arr[2] + " expected;\n")
            else:
                new_unit_test.write("\n")
            # Argument Lines
            for index in range(len(decl_arr[2:])):
                new_unit_test.write("   " + decl_arr[index + 2] +" itemUnderTest" + str(index + 2) + "\n")
            
            new_unit_test.write("   //Act\n")
            if (decl_arr[0] != "void"):
                arg_list = ""
                new_unit_test.write("   " + self.__source_file_path.lower() +                                       \
                                    "Obj->" + decl_arr[1] + "( ")
                for index in range(len(decl_arr[2:])):
                    if (index == len(decl_arr[2:])):
                        arg_list += "itemUnderTest );\n\n"
                    else:
                        arg_list += "itemUnderTest" + index + ", "
                new_unit_test.write( arg_list )
            else:
                new_unit_test.write("   " + decl_arr[0] + self.__source_file_path.lower() +                         \
                                    "Obj->" + decl_arr[1] + "();\n\n")
            
            new_unit_test.write("   //Assert\n")
            if (re.search(r"( bool.* | int.* | char.* )", decl_arr[0])):
                new_unit_test.write("   CPPUNIT_ASSERT_EQUAL(expected, actual);\n\n")
            elif (re.search(r"( double.* | float.* )", decl_arr[0])):
                new_unit_test.write("   CPPUNIT_ASSERT_DOUBLES_EQUAL(expected, actual, DELTA);\n\n")
            else:
                new_unit_test.write("   CPPUNIT_ASSERT_MESSAGE(\"test" + decl_arr[1] + \
                                    " test not fully implemented\", true);\n\n")
            new_unit_test.write("};\n\n")

    def unit_test_generation(self, arr):
        initial_header = []
        makefile_path = os.getcwd() + "/UnitTestGeneration"

        with open(makefile_path + "makefile", "r") as make_file:
            for i in range(14):
                initial_header.append(make_file.readline())

        with open(self.__new_unit_test, "w+") as new_unit_test:
            # Initial Header File Setup
            for i in range(14):
                new_unit_test.write(initial_header)
            new_unit_test.write("\n")
            for item in range(arr[1][0]):
                new_unit_test.write(item)
            new_unit_test.write("\n")
            new_unit_test.write("#define DELTA 0.1\n")
            new_unit_test.write("\n")
            new_unit_test.write("Using namespace CPPUnit;\n")
            new_unit_test.write("Using namespace std;\n")
            new_unit_test.write("\n\n")

            #Test Class Initialization
            new_unit_test.write("class Test" + self.__source_dir_name + " : public CppUnit::TestFixture\n{\n")
            new_unit_test.write("   CPPUNIT_TEST_SUITE(Test" + self.__source_file_path + ");\n")
            #TODO: Figure out a way to autogenerate Parameterized Tests
            for item in range(arr[0]):
                decl_arr = re.split(r"( |.*\(\))",item)
                new_unit_test.write("   CPPUNIT_TEST(test" + decl_arr[1] + ")\n")
            new_unit_test.write("   CPPUNIT_TEST_SUITE_END();\n\n")

            new_unit_test.write("   public:\n")
            new_unit_test.write("      void setUp(void);\n")
            new_unit_test.write("      void tearDown(void);\n\n")
            new_unit_test.write("   protected:\n")
            for item in range(arr[0]):
                decl_arr = re.split(r"( |\(|\))",item)
                new_unit_test.write("      void test" + decl_arr[1] + "( void );\n")
            new_unit_test.write("\n")
            new_unit_test.write("   private:\n")
            new_unit_test.write("      " + self.__source_file_path + "* " + \
                self.__source_file_path.lower() + "Obj;\n};\n\n")

            # Set Up and Tear Down methods
            new_unit_test.write("/*<===============================================>*/\n")
            new_unit_test.write("/*                SETUP and TEARDOWN               */\n")
            new_unit_test.write("/*<===============================================>*/\n\n")

            new_unit_test.write("void Test" + self.__source_file_path + "::setUp(void)\n{\n")
            new_unit_test.write("   " + self.__source_file_path.lower() + "= new " + self.__source_file_path + "();\n")
            new_unit_test.write("   printf(\"<==================== Starting Test =====================>\");\n}\n")

            new_unit_test.write("void Test" + self.__source_file_path + "::tearDown(void)\n{\n")
            new_unit_test.write("   delete " + self.__source_file_path.lower() + ";\n")
            new_unit_test.write("   printf(\"<==================== Finishing Test ====================>\");\n}\n")

            new_unit_test.write("/*<===============================================>*/\n")
            new_unit_test.write("/*                 UNIT TEST SETUP                 */\n")
            new_unit_test.write("/*<===============================================>*/\n\n")

        # Generating Unit Test Functions
        # Need to figure out a way to
        f = open(self.__new_unit_test, "a+")
        for item in range(arr[0]):
            decl_arr = re.split(r"( |\(|\))", item)
            if(decl_arr[0] == "bool"):
                f.write("void Test" + self.__source_dir_name + "::test" + item[1] + "Success( void )\n{\n")
                f.close()
                self.unit_test_gen(decl_arr)
                f = open(self.__new_unit_test, "a+")
                f.write("void Test" + self.__source_dir_name + "::test" + item[1] + "Failure( void )\n{\n")
                f.close()
                self.unit_test_gen(decl_arr)
                f = open(self.__new_unit_test, "a+")
            else:
                new_unit_test.write("void Test" + self.__source_dir_name + "::test" + item[1] + "( void )\n{\n")
                f.close()
                self.unit_test_gen(decl_arr)
                f = open(self.__new_unit_test, "a+")

        f.write("CPPUNIT_TEST_SUITE_REGISTRATION( Test" + self.__source_dir_name + " );")
        f.close()

    #Main Functions
    def write_unit_test(self):
        unit_test_data = []

        # Initialization
        self.get_header_file()
        header_data = self.get_header_declarations()
        src_data = self.get_source_data()

        unit_test_data.append(header_data)
        unit_test_data.append(src_data)

        # Create Unit Tests
        self.unit_test_generation(unit_test_data)


    

            



            