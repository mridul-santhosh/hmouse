# CMake generated Testfile for 
# Source directory: /home/radxa/projects/mraa/tests
# Build directory: /home/radxa/projects/mraa/build/tests
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(py_general "/usr/bin/python3" "/home/radxa/projects/mraa/tests/general_checks.py")
set_tests_properties(py_general PROPERTIES  ENVIRONMENT "PYTHONPATH=/home/radxa/projects/mraa/build/src/python/python3" _BACKTRACE_TRIPLES "/home/radxa/projects/mraa/tests/CMakeLists.txt;26;add_test;/home/radxa/projects/mraa/tests/CMakeLists.txt;0;")
add_test(py_platform "/usr/bin/python3" "/home/radxa/projects/mraa/tests/platform_checks.py")
set_tests_properties(py_platform PROPERTIES  ENVIRONMENT "PYTHONPATH=/home/radxa/projects/mraa/build/src/python/python3" _BACKTRACE_TRIPLES "/home/radxa/projects/mraa/tests/CMakeLists.txt;29;add_test;/home/radxa/projects/mraa/tests/CMakeLists.txt;0;")
add_test(py_gpio "/usr/bin/python3" "/home/radxa/projects/mraa/tests/gpio_checks.py")
set_tests_properties(py_gpio PROPERTIES  ENVIRONMENT "PYTHONPATH=/home/radxa/projects/mraa/build/src/python/python3" _BACKTRACE_TRIPLES "/home/radxa/projects/mraa/tests/CMakeLists.txt;32;add_test;/home/radxa/projects/mraa/tests/CMakeLists.txt;0;")
subdirs("unit")
