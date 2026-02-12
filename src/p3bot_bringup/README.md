# p3bot_bringup

Initial bringup package for P3Bot.

## Overview
This package currently contains:
- XML launch files
- Python launch files (for Webots integration, where required by the API)
- Default YAML configuration files

It launches upstream nodes (currently `slam_toolbox` and `webots_ros2_driver`) and keeps package-specific defaults under `config/`.

## Usage
```bash
ros2 launch p3bot_bringup slam_toolbox.launch.xml
```

Optional arguments:
- `use_sim_time` (bool, default: `false`)
- `params_file` (string, default: `$(find-pkg-share p3bot_bringup)/config/slam_toolbox.yaml`)

Launch Webots + ROS 2 extern driver:
```bash
ros2 launch p3bot_bringup webots.launch.py \
  world:=/absolute/path/to/your_world.wbt \
  robot_name:=P3Bot
```

Optional arguments:
- `mode` (string, default: `realtime`)
- `gui` (bool, default: `true`)
- `port` (string, default: `1234`)
- `driver_params_file` (string, default: `$(find-pkg-share p3bot_bringup)/config/webots_driver.yaml`)

Connect only the ROS 2 extern driver to an already running Webots instance:
```bash
ros2 launch p3bot_bringup webots_driver.launch.py robot_name:=P3Bot
```

## API
Nodes launched by this package:
- `/slam_toolbox` from `slam_toolbox/async_slam_toolbox_node`
- `/webots_controller_<robot_name>` from `webots_ros2_driver`

Topics, services and actions are provided by upstream packages (`slam_toolbox` and Webots device plugins).
Refer to upstream documentation for each full API contract.

## Parameters
Default parameters file:
- `config/slam_toolbox.yaml`
- `config/webots_driver.yaml`

Primary defaults:
- `mode` (`string`): `mapping`
- `resolution` (`double`): `0.05`
- `max_laser_range` (`double`): `30.0`
- `map_update_interval` (`double`): `5.0`
- `transform_publish_period` (`double`): `0.02`
- `use_sim_time` (`bool`): `true` (Webots driver defaults)
- `set_robot_state_publisher` (`bool`): `false` (Webots driver defaults)
