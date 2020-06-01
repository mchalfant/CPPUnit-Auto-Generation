import unit_test_dir_generator

arr = []
utdg = unit_test_dir_generator.unit_test_dir_generator()

print("Starting Unit Test Generation\n")

dir_arr = utdg.collect_valid_directories(arr)
src_arr = utdg.find_valid_src_files(dir_arr)
utdg.prepare_unit_test_dir(dir_arr, src_arr)

fc = utdg.get_file_created_count()

if(fc):
    print("\nCreated " +  str(fc) + " Unit Test files\n")
else:
    print("All Files are all ready updated")