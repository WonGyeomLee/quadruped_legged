from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.substitutions import Command, LaunchConfiguration, PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.descriptions import ParameterValue
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():
    package_share = FindPackageShare("quad_urdf")

    model = LaunchConfiguration("model")
    rviz_config = LaunchConfiguration("rvizconfig")
    use_sim_time = LaunchConfiguration("use_sim_time")

    robot_description = ParameterValue(
        Command(["xacro ", model]),
        value_type=str,
    )

    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "model",
                default_value=PathJoinSubstitution(
                    [package_share, "urdf", "quadruped.xacro"]
                ),
                description="Absolute path to the robot Xacro or URDF file",
            ),
            DeclareLaunchArgument(
                "rvizconfig",
                default_value=PathJoinSubstitution(
                    [package_share, "config", "display.rviz"]
                ),
                description="Absolute path to the RViz configuration file",
            ),
            DeclareLaunchArgument(
                "use_sim_time",
                default_value="false",
                description="Use the simulation clock when true",
            ),
            Node(
                package="robot_state_publisher",
                executable="robot_state_publisher",
                name="robot_state_publisher",
                output="screen",
                parameters=[
                    {
                        "robot_description": robot_description,
                        "use_sim_time": use_sim_time,
                    }
                ],
            ),
            Node(
                package="joint_state_publisher_gui",
                executable="joint_state_publisher_gui",
                name="joint_state_publisher_gui",
                output="screen",
                parameters=[{"use_sim_time": use_sim_time}],
            ),
            Node(
                package="rviz2",
                executable="rviz2",
                name="rviz2",
                output="screen",
                arguments=["-d", rviz_config],
                parameters=[{"use_sim_time": use_sim_time}],
            ),
        ]
    )
