cmake_minimum_required(VERSION 3.8)
project(examen_msgs)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)

# Genera las interfaces (.msg)
rosidl_generate_interfaces(${PROJECT_NAME}
  "msg/Tipico.msg"
  # Si tu .msg usara tipos de otros paquetes, agrega:
  # DEPENDENCIES std_msgs
)

ament_package()
