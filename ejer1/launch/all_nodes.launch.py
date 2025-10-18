from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    silent = ['--ros-args', '--log-level', 'fatal']  # callar logs

    return LaunchDescription([
        Node(
            package='ejer1', executable='sensor1_pub', name='sensor1_pub',
            output='log', arguments=silent
        ),
        Node(
            package='ejer1', executable='sensor1_pub', name='sensor2_pub',
            output='log', arguments=silent,
            remappings=[('sensor_1', 'sensor_2')]
        ),
        Node(
            package='ejer1', executable='sensor1_pub', name='sensor3_pub',
            output='log', arguments=silent,
            remappings=[('sensor_1', 'sensor_3')]
        ),
        Node(
            package='ejer1', executable='nodo4_sub', name='nodo4_sub',
            output='log', arguments=silent
        ),

    ])
