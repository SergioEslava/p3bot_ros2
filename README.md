# p3bot_ros2

ROS 2 workspace for the P3Bot project.

## Scope
- Robot description integration via `p3bot_description`
- SLAM integration via `slam_toolbox`
- Bringup package with launch/config defaults

## Workspace layout
- `src/p3bot_bringup`: Launch and default config files for initial bringup
- `p3bot.repos`: External source dependencies to import with `vcstool` (solo `p3bot_description`)

## Dependencies import
```bash
mkdir -p src
vcs import src < p3bot.repos
```

## Binary dependencies
Install ROS dependencies from packages:
```bash
source /opt/ros/$ROS_DISTRO/setup.bash
rosdep install --from-paths src --ignore-src -r -y
```

`slam_toolbox` is intentionally used as an external dependency (system package), not cloned into this repository.

## Build
```bash
source /opt/ros/$ROS_DISTRO/setup.bash
colcon build --symlink-install
```

## Launch (initial SLAM)
```bash
source install/setup.bash
ros2 launch p3bot_bringup slam_toolbox.launch.xml
```

## Notes
- Current `p3bot.repos` uses branch name for `p3bot_description` because this environment has no internet access to resolve exact SHAs.
- For production reproducibility, pin `p3bot_description` to a commit hash or tag.
