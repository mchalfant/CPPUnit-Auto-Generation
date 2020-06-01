
# Environmental Variables for Project Directory

PROJ_DIR=

SUB_PROJ_DIR=

UTIL_TOP_DIR=utilities

SRC_UT=

OBJ_DIR=OBJS

COV_DIR=COVERAGE

REPORTS_DIR=REPORTS

SRC_DIR=$(PROJ_DIR)/core/src/

SRC_UT_DIR=$(SRC_DIR)/$(SUB_PROJ_DIR)/$(SRC_UT)

UTIL_DIR=$(PROJ_DIR)/core/src/$(UTIL_TOP_DIR)

SRC = Test$(SRC_UT).cpp                                                      \
      TestMain.cpp                                                           \
      $(SRC_UT_DIR)/$(SRC_UT).cpp

INCLUDE=-I/$(SRC_DIR)/tools/cppunit-1.15-1/include                           \
        -I/$(SRC_DIR)/$(SUB_PROJ_DIR)/global                                 \
        -I/$(SRC_DIR)/common

OBJS = Test$(SRC_UT).o                                                       \
       TestMain.o                                                            \
       $(SRC_UT).o

COMPILE=g++

LINK=g++

CFLAGS=-g -c

COVFLAGS=-fprofile-arcs -ftest-coverage

LINKCOV=--coverage -lgcov

LIB=-lcppunit

TARGET=Test$(SRC_UT)

OUTPUT:
	$(COMPILE) $(INCLUDE) $(CFLAGS) $(SRC)
	
	$(LINK) $(LIBS) -o $(TARGET)
	
	[ -d ./$(OBJ_DIR) ] || mkdir ./$(OBJ_DIR)
	
	mv *.o ./$(OBJ_DIR)	 

COVERAGE:
	$(COMPILE) $(COVFLAGS) $(INCLUDE) $(CFLAGS) $(SRC)
	
	$(LINK) $(LINKCOV) $(LIBS) -o $(TARGET)
	
	./$(TARGET)
	
	gcov --object-directory=. $(SRC_UT_DIR)/$(SRC_UT).cpp
	
	[ -d ./$(OBJ_DIR) ] || mkdir ./$(OBJ_DIR)
	
	[ -d ./$(COV_DIR) ] || mkdir ./$(COV_DIR)
	
	[ -d ./$(REPORTS_DIR) ] || mkdir ./$(REPORTS_DIR)
	
	mv *.o ./$(OBJ_DIR)
	
	mv *.gcno *.gcda *.gcov ./$(COV_DIR)
	
	gcovr -f $(SRC_UT_DIR) 

clean:
	rm -rf ./$(OBJ_DIR) ./$(COV_DIR) ./$(REPORTS_DIR)
	rm $(TARGET)

