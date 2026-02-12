#!/usr/bin/env python3

import launch
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import OpaqueFunction
from launch_ros.substitutions import FindPackageShare
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution
from webots_ros2_driver.webots_controller import WebotsController
from webots_ros2_driver.webots_launcher import WebotsLauncher


def _launch_setup(context):
    world = LaunchConfiguration("world").perform(context)
    mode = LaunchConfiguration("mode").perform(context)
    gui = LaunchConfiguration("gui").perform(context).lower() in ("true", "1", "yes")
    robot_name = LaunchConfiguration("robot_name").perform(context)
    port = LaunchConfiguration("port").perform(context)
    params_file = LaunchConfiguration("driver_params_file").perform(context)
    robot_description_file = LaunchConfiguration("robot_description_file").perform(context)

    webots = WebotsLauncher(
        world=world,
        mode=mode,
        gui=gui,
        port=port,
        ros2_supervisor=True,
    )

    webots_driver = WebotsController(
        robot_name=robot_name,
        parameters=[
            params_file,
            {"robot_description": robot_description_file},
        ],
        port=port,
        respawn=True,
    )

    return [
        webots,
        webots._supervisor,
        webots_driver,
        launch.actions.RegisterEventHandler(
            event_handler=launch.event_handlers.OnProcessExit(
                target_action=webots,
                on_exit=[launch.actions.EmitEvent(event=launch.events.Shutdown())],
            )
        ),
    ]


def generate_launch_description():
    return LaunchDescription(
        [
            DeclareLaunchArgument(
                "world",
                description="Absolute path to the .wbt world file to launch.",
            ),
            DeclareLaunchArgument(
                "mode",
                default_value="realtime",
                description="Webots startup mode.",
            ),
            DeclareLaunchArgument(
                "gui",
                default_value="true",
                description="Whether to start Webots with GUI.",
            ),
            DeclareLaunchArgument(
                "robot_name",
                default_value="P3Bot",
                description="Name of the Robot node in the Webots world.",
            ),
            DeclareLaunchArgument(
                "port",
                default_value="1234",
                description="TCP port used by Webots and the extern controller.",
            ),
            DeclareLaunchArgument(
                "driver_params_file",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("p3bot_bringup"), "config", "webots_driver.yaml"]
                ),
                description="Default parameters file for webots_ros2_driver.",
            ),
            DeclareLaunchArgument(
                "robot_description_file",
                default_value=PathJoinSubstitution(
                    [FindPackageShare("p3bot_description"), "urdf", "P3Bot.urdf.xacro"]
                ),
                description="Path to robot description file used by webots_ros2_driver.",
            ),
            OpaqueFunction(function=_launch_setup),
        ]
    )
