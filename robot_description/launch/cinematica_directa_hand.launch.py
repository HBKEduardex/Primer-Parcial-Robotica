"""
    Author: Edu
"""
from ament_index_python.packages import get_package_share_path

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = get_package_share_path('robot_description')
    default_index_model = pkg_share / 'urdf/indice.urdf'     
    default_thumb_model = pkg_share / 'urdf/pulgar.urdf'     
    default_rviz_cfg   = pkg_share / 'rviz/urdf.rviz'       

    # Args
    gui_arg = DeclareLaunchArgument(
        name='gui', default_value='true', choices=['true', 'false'],
        description='Enable joint_state_publisher_gui'
    )
    index_model_arg = DeclareLaunchArgument(
        name='index_model', default_value=str(default_index_model),
        description='Absolute path to INDEX URDF/XACRO file'
    )
    thumb_model_arg = DeclareLaunchArgument(
        name='thumb_model', default_value=str(default_thumb_model),
        description='Absolute path to THUMB URDF/XACRO file'
    )
    rviz_arg = DeclareLaunchArgument(
        name='rvizconfig', default_value=str(default_rviz_cfg),
        description='Absolute path to RViz config file'
    )

    index_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('index_model')]),
        value_type=str
    )
    thumb_description = ParameterValue(
        Command(['xacro ', LaunchConfiguration('thumb_model')]),
        value_type=str
    )

    rsp_index = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        namespace='index', name='rsp_index',
        parameters=[{'robot_description': index_description},
                    {'frame_prefix': 'idx_'}],            # evita colisiones TF
        remappings=[('joint_states', '/index/joint_states')]
    )

    jsp_index_cli = Node(
        package='joint_state_publisher', executable='joint_state_publisher',
        namespace='index', name='jsp_index_cli',
        condition=UnlessCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', 'joint_states')]
    )
    jsp_index_gui = Node(
        package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
        namespace='index', name='jsp_index_gui',
        condition=IfCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', 'joint_states')]
    )

    rsp_thumb = Node(
        package='robot_state_publisher', executable='robot_state_publisher',
        namespace='thumb', name='rsp_thumb',
        parameters=[{'robot_description': thumb_description},
                    {'frame_prefix': 'th_'}],             
        remappings=[('joint_states', '/thumb/joint_states')]
    )

    jsp_thumb_cli = Node(
        package='joint_state_publisher', executable='joint_state_publisher',
        namespace='thumb', name='jsp_thumb_cli',
        condition=UnlessCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', 'joint_states')]
    )
    jsp_thumb_gui = Node(
        package='joint_state_publisher_gui', executable='joint_state_publisher_gui',
        namespace='thumb', name='jsp_thumb_gui',
        condition=IfCondition(LaunchConfiguration('gui')),
        remappings=[('joint_states', 'joint_states')]
    )


    tf_index = Node(
        package='tf2_ros', executable='static_transform_publisher', name='tf_idx',
        arguments=['0', '0', '0', '0', '0', '0', 'world', 'idx_link0_passive']
    )
    tf_thumb = Node(
        package='tf2_ros', executable='static_transform_publisher', name='tf_th',
        arguments=['0.15', '0', '0', '0', '0', '0', 'world', 'th_link0_passive']
    )


    rviz = Node(
        package='rviz2', executable='rviz2', name='rviz2', output='screen',
        arguments=['-d', LaunchConfiguration('rvizconfig')]
    )

    return LaunchDescription([
        gui_arg, index_model_arg, thumb_model_arg, rviz_arg,
        rsp_index, jsp_index_cli, jsp_index_gui,
        rsp_thumb, jsp_thumb_cli, jsp_thumb_gui,
        tf_index, tf_thumb, rviz
    ])
