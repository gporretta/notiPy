#!/bin/bash

# Ensure non root run. Systemctl --user requires non root user.
if [ "$EUID" -eq 0 ]; then
  echo "This script must be run as a non-root user."
  exit 1
fi

SERVICE_SCRIPT="notipy_notifier.py"
SERVICE_FILE="notipy.service"
SERVICE_PATH="$HOME/.config/systemd/user/$SERVICE_FILE"

chmod +x "$SERVICE_SCRIPT"

# Create user systemd directory if it doesn't exist
mkdir -p "$HOME/.config/systemd/user"

# Move the service to user systemd directory
echo "Moving $SERVICE_SCRIPT to usr/local/bin..."
sudo cp "$SERVICE_SCRIPT" /usr/local/bin/

# Move the service to user systemd directory
echo "Moving $SERVICE_FILE to $SERVICE_PATH..."
cp "$SERVICE_FILE" "$SERVICE_PATH"

chmod 644 "$SERVICE_PATH"

# Reload user systemd
echo "Reloading user systemd daemon..."
systemctl --user daemon-reload

# Enable the service
echo "Enabling the service..."
systemctl --user enable "$SERVICE_FILE"

# Start service 
echo "Starting the service..."
systemctl --user start "$SERVICE_FILE"

# Initialize database
echo "Initializing database..."
/usr/bin/python3 "$(pwd)/init_db.py"

sudo chmod 777 "$HOME/.config/notipy/notipy.db"

# Create a symbolic link to /usr/local/bin
EX_PATH="$(pwd)/notipy.py"
LINK_PATH="/usr/local/bin/notipy"

echo "Creating a symbolic link in /usr/local/bin..."
sudo ln -sf "$EX_PATH" "$LINK_PATH"

echo "Notipy Installation complete!"
