import os
import os.path
import re
import unit_test_src_generator

class unit_test_dir_generator():

   def __init__(self):
      self.__top_level_dir = "/home/mchalfant/core"
      self.__src_level_dir = self.__top_level_dir + "/src"
      self.__pattern = r"^((?!common)(?!tools)(?!libraries).)*$"
      self.__pattern_2 = r"[\w-]+\.+cpp"
      self.__file_count = 0
   
   def collect_valid_directories(self, arr):
      for __dir, dirnames, filenames in os.walk(self.__src_level_dir):
         for dirname in dirnames:
            new_dir = self.__src_level_dir + "/" + dirname
            for __dir_secondary, dirnames_secondary, filenames_secondary in os.walk(new_dir):
               for new_dirname in dirnames_secondary:
                  if re.match(self.__pattern, new_dirname):
                     arr.append(new_dir + "/" + new_dirname + "/")
      return arr

   def find_valid_src_files(self, arr):
      new_arr = []
      for pathname in arr:
         for __dir, dirnames, filenames in os.walk(pathname):
            for filename in filenames:
               if re.match(self.__pattern_2, filename):
                  new_arr.append(filename)
      return new_arr
            
   def prepare_unit_test_dir(self, dirpaths, filepaths):
      
      new_dirpaths = []
      cwd = os.getcwd()

      for dirpath in dirpaths:
         new_dirpaths.append(dirpath.replace("src", "test"))

      with open(cwd + "/UnitTestGeneration/" + "TestMain.cpp", "r") as test_main:
         test_main_data = test_main.readlines()

      with open(cwd + "/UnitTestGeneration/" + "makefile", "r") as make_file:
         make_file_data = make_file.readlines()

      for new_dirpath in new_dirpaths:
         dir_names = new_dirpath.split('/')
         if ( not(os.path.exists( new_dirpath ))):
            os.makedirs( new_dirpath )
         unit_test_dir = re.split(r"\/", new_dirpath)

         if ( not(os.path.isfile( new_dirpath + "TestMain.cpp" ))):
            with open(new_dirpath + "TestMain.cpp", "w+") as new_test_main:
               for data in test_main_data:
                  if (re.search(r"ofstream xmlFileOut", data)):
                     new_test_main.write("ofstream xmlFileOut( cppTest" + dir_names[-2] +".xml );\n")
                  else:
                     new_test_main.write(data)
            self.__file_count += 1
            print("Created new file: " + new_dirpath + "TestMain.cpp")

         if (not(os.path.isfile(new_dirpath + "makefile"))):
            with open(new_dirpath + "makefile", "w+") as new_make_file:
               for data in make_file_data:
                  if (re.search(r"SUB_PROJ_DIR=", data)):
                     new_make_file.write("SUB_PROJ_DIR="+ dir_names[-3] + "\n")
                  elif (re.search(r"SRC_UT=", data)):
                     new_make_file.write("SRC_UT=" + dir_names[-2] + "\n")
                  elif (re.search(r"PROJ_DIR=", data)):
                     proj_dir = ""
                     for dir_name in dir_names[1:-5]:
                        proj_dir += "/" + dir_name
                     new_make_file.write("PROJ_DIR=" + proj_dir)
                  else:
                     new_make_file.write(data)
            self.__file_count += 1
            print("Created new file: " + new_dirpath + "makefile")

         for filepath in filepaths:
            if ( not(os.path.isfile(new_dirpath + "Test" + filepath)) 
                 and (filepath.find(unit_test_dir[-2])) != -1 ):
               utsg = unit_test_src_generator.unit_test_src_generator(new_dirpath, filepath)
               utsg.write_unit_test()
               self.__file_count += 1
               print("Created new file: " + new_dirpath + "Test" + filepath)

   def get_file_created_count(self):
      return self.__file_count
