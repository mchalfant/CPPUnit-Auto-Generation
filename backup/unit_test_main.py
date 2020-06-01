import unit_test_generation
import create_unit_test_template

u = unit_test_generation.unit_test_generation()
t = create_unit_test_template.create_unit_test_template()

header_data_arr = t.get_header_data("/home/mchalfant/core/src/rdpop/global/Camera.h")

arr = []

source_data_arr = t.get_source_data("/home/mchalfant/core/src/rdpop/Camera/Camera.cpp")

dir_arr = u.collect_valid_directories(arr)
print(dir_arr)
src_arr = u.find_valid_src_files(dir_arr)
print(src_arr)
u.prepare_unit_test_dir(dir_arr, src_arr)