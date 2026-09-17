#!/usr/bin/env bash
set -euo pipefail

# PX4/Gazebo-Umgebung, Ubuntu 22.04 arm64
# Niklas Pfeil — drone-dev

PX4_VERSION="v1.17.0"
PX4_DIR="$HOME/PX4-Autopilot"

echo "==> 1/5 System aktualisieren"
sudo apt update
sudo apt upgrade -y



echo "==> 2/5 PX4 klonen"

if [ -d "$PX4_DIR" ]; then
    echo "    $PX4_DIR existiert bereits, überspringe Clone"
else
    git clone https://github.com/PX4/PX4-Autopilot.git "$PX4_DIR" --recursive
fi

echo "==> 3/5 Auf $PX4_VERSION festnageln"
cd "$PX4_DIR"
git checkout "$PX4_VERSION"
git submodule update --init --recursive

echo "==> 4/5 Abhängigkeiten (ohne NuttX — nur Simulation)"
bash ./Tools/setup/ubuntu.sh --no-nuttx

echo "==> 5/5 Build"
make px4_sitl_default

echo
echo "Fertig. Reboot nötig (neuer Kernel)."
echo "Danach:  HEADLESS=1 make px4_sitl gz_x500"


