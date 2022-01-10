cmake_minimum_required(VERSION 3.0)
project(car)

# Default to C11, C++17, Wall as error
if(NOT CMAKE_C_STANDARD)
  set(CMAKE_C_STANDARD 11)
  set(CMAKE_C_STANDARD_REQUIRED ON)
endif()
if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
  set(CMAKE_CXX_STANDARD_REQUIRED ON)
endif()
if(CMAKE_COMPILER_IS_GNUC OR CMAKE_C_COMPILER_ID MATCHES "Clang")
  add_definitions(-Wall -Wextra -Werror -Wno-enum-compare)
endif()
if(CMAKE_COMPILER_IS_GNUCXX OR CMAKE_CXX_COMPILER_ID MATCHES "Clang")
  add_definitions(-Wall -Wextra -Werror -Wno-enum-compare)
endif()

if(BUILD_TESTING)
  find_package(ament_lint_auto REQUIRED)
  # the following line skips the linter which checks for copyrights
  # uncomment the line when a copyright and license is not present in all source files
  #set(ament_cmake_copyright_FOUND TRUE)
  # the following line skips cpplint (only works in a git repo)
  # uncomment the line when this package is not in a git repo
  #set(ament_cmake_cpplint_FOUND TRUE)
  # Disable it since it's not a package.
  #ament_lint_auto_find_test_dependencies()
endif()

find_package(Boost REQUIRED)

set(DEFAULT_NAME ${PROJECT_NAME}) # current level

#configure_file()
#file(GLOB SRC_FILES *.cpp)

add_library(${DEFAULT_NAME}_lib car.cpp )
add_executable(${DEFAULT_NAME} main.cpp)
target_link_libraries(${DEFAULT_NAME} ${DEFAULT_NAME}_lib)
target_link_libraries(${DEFAULT_NAME}_lib ${Boost_LIBRARIES})

target_include_directories(${DEFAULT_NAME} PUBLIC "./include/")
target_include_directories(${DEFAULT_NAME}_lib PUBLIC
  "include"
  "${Boost_INCLUDE_DIR}" # omit when == /usr/include(/)
)
