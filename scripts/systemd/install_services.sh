#!/bin/bash
# scripts/systemd/install_services.sh

PROJECT_ROOT="/home/samson/apex"
SYSTEMD_DIR="$PROJECT_ROOT/systemd"
TARGET_DIR="/etc/systemd/system"

echo "Installing systemd services for Project Apex..."

if [ ! -d "$SYSTEMD_DIR" ]; then
    echo "Error: Systemd directory not found at $SYSTEMD_DIR"
    exit 1
fi

# Make scripts executable
chmod +x "$PROJECT_ROOT/scripts/systemd/telegram_notify.sh"

# Copy service files
echo "Copying service files to $TARGET_DIR..."
sudo cp "$SYSTEMD_DIR"/*.service "$TARGET_DIR/"

# Reload systemd
echo "Reloading systemd..."
sudo systemctl daemon-reload

# Enable services
SERVICES=(
    "apex-sled-commander.service"
    "apex-tatt-architect.service"
    "apex-security-warden.service"
    "apex-sync-service.service"
)

for service in "${SERVICES[@]}"; do
    echo "Enabling $service..."
    sudo systemctl enable "$service"
    
    # Optional: Check if service is running and restart it, or just leave it for reboot/manual start
    # echo "Starting $service..."
    # sudo systemctl start "$service"
done

echo "✅ Systemd services installed and enabled."
echo "Use 'sudo systemctl start apex-sled-commander' etc. to start them now."
