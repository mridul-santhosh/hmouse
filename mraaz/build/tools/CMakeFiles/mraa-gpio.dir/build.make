# CMAKE generated file: DO NOT EDIT!
# Generated by "Unix Makefiles" Generator, CMake Version 3.18

# Delete rule output on recipe failure.
.DELETE_ON_ERROR:


#=============================================================================
# Special targets provided by cmake.

# Disable implicit rules so canonical targets will work.
.SUFFIXES:


# Disable VCS-based implicit rules.
% : %,v


# Disable VCS-based implicit rules.
% : RCS/%


# Disable VCS-based implicit rules.
% : RCS/%,v


# Disable VCS-based implicit rules.
% : SCCS/s.%


# Disable VCS-based implicit rules.
% : s.%


.SUFFIXES: .hpux_make_needs_suffix_list


# Command-line flag to silence nested $(MAKE).
$(VERBOSE)MAKESILENT = -s

#Suppress display of executed commands.
$(VERBOSE).SILENT:

# A target that is always out of date.
cmake_force:

.PHONY : cmake_force

#=============================================================================
# Set environment variables for the build.

# The shell in which to execute make rules.
SHELL = /bin/sh

# The CMake executable.
CMAKE_COMMAND = /usr/bin/cmake

# The command to remove a file.
RM = /usr/bin/cmake -E rm -f

# Escaping for special characters.
EQUALS = =

# The top-level source directory on which CMake was run.
CMAKE_SOURCE_DIR = /home/radxa/projects/mraa

# The top-level build directory on which CMake was run.
CMAKE_BINARY_DIR = /home/radxa/projects/mraa/build

# Include any dependencies generated for this target.
include tools/CMakeFiles/mraa-gpio.dir/depend.make

# Include the progress variables for this target.
include tools/CMakeFiles/mraa-gpio.dir/progress.make

# Include the compile flags for this target's objects.
include tools/CMakeFiles/mraa-gpio.dir/flags.make

tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o: tools/CMakeFiles/mraa-gpio.dir/flags.make
tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o: ../tools/mraa-gpio.c
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --progress-dir=/home/radxa/projects/mraa/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_1) "Building C object tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o"
	cd /home/radxa/projects/mraa/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -o CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o -c /home/radxa/projects/mraa/tools/mraa-gpio.c

tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.i: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Preprocessing C source to CMakeFiles/mraa-gpio.dir/mraa-gpio.c.i"
	cd /home/radxa/projects/mraa/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -E /home/radxa/projects/mraa/tools/mraa-gpio.c > CMakeFiles/mraa-gpio.dir/mraa-gpio.c.i

tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.s: cmake_force
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green "Compiling C source to assembly CMakeFiles/mraa-gpio.dir/mraa-gpio.c.s"
	cd /home/radxa/projects/mraa/build/tools && /usr/bin/cc $(C_DEFINES) $(C_INCLUDES) $(C_FLAGS) -S /home/radxa/projects/mraa/tools/mraa-gpio.c -o CMakeFiles/mraa-gpio.dir/mraa-gpio.c.s

# Object files for target mraa-gpio
mraa__gpio_OBJECTS = \
"CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o"

# External object files for target mraa-gpio
mraa__gpio_EXTERNAL_OBJECTS =

tools/mraa-gpio: tools/CMakeFiles/mraa-gpio.dir/mraa-gpio.c.o
tools/mraa-gpio: tools/CMakeFiles/mraa-gpio.dir/build.make
tools/mraa-gpio: src/libmraa.so.2.2.0
tools/mraa-gpio: /usr/lib/aarch64-linux-gnu/libjson-c.so
tools/mraa-gpio: tools/CMakeFiles/mraa-gpio.dir/link.txt
	@$(CMAKE_COMMAND) -E cmake_echo_color --switch=$(COLOR) --green --bold --progress-dir=/home/radxa/projects/mraa/build/CMakeFiles --progress-num=$(CMAKE_PROGRESS_2) "Linking C executable mraa-gpio"
	cd /home/radxa/projects/mraa/build/tools && $(CMAKE_COMMAND) -E cmake_link_script CMakeFiles/mraa-gpio.dir/link.txt --verbose=$(VERBOSE)

# Rule to build all files generated by this target.
tools/CMakeFiles/mraa-gpio.dir/build: tools/mraa-gpio

.PHONY : tools/CMakeFiles/mraa-gpio.dir/build

tools/CMakeFiles/mraa-gpio.dir/clean:
	cd /home/radxa/projects/mraa/build/tools && $(CMAKE_COMMAND) -P CMakeFiles/mraa-gpio.dir/cmake_clean.cmake
.PHONY : tools/CMakeFiles/mraa-gpio.dir/clean

tools/CMakeFiles/mraa-gpio.dir/depend:
	cd /home/radxa/projects/mraa/build && $(CMAKE_COMMAND) -E cmake_depends "Unix Makefiles" /home/radxa/projects/mraa /home/radxa/projects/mraa/tools /home/radxa/projects/mraa/build /home/radxa/projects/mraa/build/tools /home/radxa/projects/mraa/build/tools/CMakeFiles/mraa-gpio.dir/DependInfo.cmake --color=$(COLOR)
.PHONY : tools/CMakeFiles/mraa-gpio.dir/depend

