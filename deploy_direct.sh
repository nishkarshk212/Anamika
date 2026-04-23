#!/bin/bash

# ============================================
# AnnieXMusic - Direct Deployment via SCP
# ============================================
# This uploads files directly without Git

SERVER_IP="161.118.250.195"
SERVER_USER="root"
SERVER_PORT="22"
DEPLOY_DIR="/opt/AnnieXMusic"

echo "🚀 Starting Direct Deployment to $SERVER_IP..."
echo ""

# Step 1: Test SSH
echo "🔑 Testing SSH connection..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '✅ Connected'"

if [ $? -ne 0 ]; then
    echo "❌ SSH failed!"
    exit 1
fi

# Step 2: Prepare server
echo "📁 Preparing server..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'EOF'
mkdir -p /opt/AnnieXMusic
cd /opt/AnnieXMusic

# Install dependencies
if ! command -v python3 &> /dev/null; then
    apt-get update
    apt-get install -y python3 python3-pip python3-venv ffmpeg git
fi

# Create venv if not exists
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi
EOF

# Step 3: Upload project files (excluding unnecessary files)
echo "📤 Uploading project files..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "rm -rf /opt/AnnieXMusic/AnnieXMedia /opt/AnnieXMusic/strings"

rsync -avz --exclude='.git' --exclude='.venv' --exclude='venv' --exclude='__pycache__' --exclude='.env' --exclude='*.session' --exclude='cache' --exclude='downloads' --exclude='couples' --exclude='log.txt' --exclude='.DS_Store' \
    /Users/nishkarshkr/Desktop/AnnieXMusic/ $SERVER_USER@$SERVER_IP:$DEPLOY_DIR/

# Step 4: Upload .env file
echo "🔐 Uploading .env file..."
sshpass -p "Akshay343402355468" scp -P $SERVER_PORT /Users/nishkarshkr/Desktop/AnnieXMusic/.env $SERVER_USER@$SERVER_IP:$DEPLOY_DIR/.env

# Step 5: Install Python dependencies
echo "📦 Installing Python dependencies..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'EOF'
cd /opt/AnnieXMusic
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
EOF

# Step 6: Setup systemd service
echo "⚙️  Setting up systemd service..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'EOF'
cat > /etc/systemd/system/anniemusic.service << 'SERVICEEOF'
[Unit]
Description=AnnieXMusic Bot
After=network.target

[Service]
Type=simple
WorkingDirectory=/opt/AnnieXMusic
ExecStart=/opt/AnnieXMusic/venv/bin/python3 -m AnnieXMedia
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
SERVICEEOF

systemctl daemon-reload
systemctl enable anniemusic
systemctl restart anniemusic
sleep 3
EOF

# Step 7: Check status
echo ""
echo "✅ Deployment Complete!"
echo ""
echo "📊 Bot Status:"
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "systemctl status anniemusic --no-pager | head -15"

echo ""
echo "📝 Useful Commands:"
echo "   Status:  sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'systemctl status anniemusic'"
echo "   Logs:    sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'journalctl -u anniemusic -f'"
echo "   Restart: sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'systemctl restart anniemusic'"
echo ""
