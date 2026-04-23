#!/bin/bash

# ============================================
# AnnieXMusic - Git-Based Server Deployment
# ============================================

SERVER_IP="161.118.250.195"
SERVER_USER="root"
SERVER_PORT="22"
DEPLOY_DIR="/opt/AnnieXMusic"
GIT_REPO="https://github.com/nishkarshk212/Anamika.git"
GIT_BRANCH="main"

echo "🚀 Git-Based Deployment to $SERVER_IP"
echo "📂 Repository: $GIT_REPO"
echo "🌿 Branch: $GIT_BRANCH"
echo ""

# Step 1: Test SSH Connection
echo "🔑 Testing SSH connection..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT -o StrictHostKeyChecking=no $SERVER_USER@$SERVER_IP "echo '✅ SSH Connected'"

if [ $? -ne 0 ]; then
    echo "❌ SSH connection failed!"
    exit 1
fi

# Step 2: Prepare Server Environment
echo "📦 Preparing server environment..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'ENDSSH'
# Install required packages
if ! command -v python3 &> /dev/null; then
    echo "Installing Python 3 and dependencies..."
    apt-get update
    apt-get install -y python3 python3-pip python3-venv git ffmpeg curl
else
    echo "Python3 already installed"
fi

# Install git if not present
if ! command -v git &> /dev/null; then
    apt-get update
    apt-get install -y git
fi

# Install ffmpeg if not present
if ! command -v ffmpeg &> /dev/null; then
    apt-get update
    apt-get install -y ffmpeg
fi

echo "✅ Server environment ready"
ENDSSH

# Step 3: Clone or Update Repository
echo "📥 Deploying code from Git..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << ENDSSH
cd /opt

if [ -d "AnnieXMusic/.git" ]; then
    echo "📥 Updating existing repository..."
    cd AnnieXMusic
    git reset --hard HEAD
    git clean -fd
    git pull origin $GIT_BRANCH
else
    echo "📥 Cloning fresh repository..."
    rm -rf AnnieXMusic
    git clone $GIT_REPO AnnieXMusic
    cd AnnieXMusic
    git checkout $GIT_BRANCH
fi

echo "✅ Code deployed from Git"
ENDSSH

# Step 4: Setup Python Virtual Environment
echo "🐍 Setting up Python environment..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'ENDSSH'
cd /opt/AnnieXMusic

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate and install dependencies
echo "Installing Python dependencies..."
source venv/bin/activate
pip install --upgrade pip

# Install requirements (ignore errors for git dependencies)
if [ -f "requirements.txt" ]; then
    # Install regular packages first
    grep -v "^git+" requirements.txt | grep -v "^$" | pip install -r /dev/stdin --quiet
    
    # Try to install git-based packages (may fail if private repo)
    grep "^git+" requirements.txt | while read -r git_url; do
        repo_url=$(echo $git_url | sed 's/^git+//')
        echo "Installing: $repo_url"
        pip install "$repo_url" 2>&1 | tail -5 || echo "Warning: Failed to install $repo_url"
    done
fi

echo "✅ Python dependencies installed"
ENDSSH

# Step 5: Upload .env file (from your local machine)
echo "🔐 Uploading .env configuration..."
if [ -f "/Users/nishkarshkr/Desktop/AnnieXMusic/.env" ]; then
    sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "mkdir -p /opt/AnnieXMusic"
    sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "cat > /opt/AnnieXMusic/.env" < /Users/nishkarshkr/Desktop/AnnieXMusic/.env
    echo "✅ .env file uploaded"
else
    echo "⚠️  Warning: .env file not found locally!"
    echo "   You'll need to upload it manually:"
    echo "   sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'cat > /opt/AnnieXMusic/.env' < .env"
fi

# Step 5.5: Fix YouTube async compatibility
echo "🔧 Fixing YouTube search async compatibility..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'ENDSSH'
cd /opt/AnnieXMusic

# Create async compatibility shim for youtube-search-python
cat > venv/lib/python3.10/site-packages/youtubesearchpython/aio.py << 'PYEOF'
"""Async compatibility layer for youtube-search-python 1.5.x"""
from youtubesearchpython import VideosSearch as SyncVideosSearch, Playlist as SyncPlaylist
import asyncio
from concurrent.futures import ThreadPoolExecutor

_executor = ThreadPoolExecutor(max_workers=4)

class VideosSearch:
    def __init__(self, query, limit=20, region=None, language=None, timeout=None):
        self.query = query
        self.limit = limit
        self.region = region
        self.language = language
        self.timeout = timeout
        self._sync = SyncVideosSearch(query, limit=limit, region=region, language=language)
    
    async def next(self):
        """Async wrapper for sync search"""
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(_executor, lambda: self._sync.result())
            return result
        except Exception as e:
            return {"result": []}

class Playlist:
    def __init__(self, name, link=None, timeout=None):
        self.name = name
        self.link = link
        self.timeout = timeout
        if link:
            self._sync = SyncPlaylist(name=link, link=link)
        else:
            self._sync = SyncPlaylist(name=name)
    
    async def next(self):
        """Async wrapper for sync playlist"""
        loop = asyncio.get_event_loop()
        try:
            result = await loop.run_in_executor(_executor, lambda: self._sync.result())
            return result
        except Exception as e:
            return {"result": []}
PYEOF

echo "✅ YouTube async compatibility fixed"
ENDSSH

# Step 6: Create Systemd Service
echo "⚙️  Creating systemd service..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'ENDSSH'
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
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=multi-user.target
SERVICEEOF

# Enable and reload
systemctl daemon-reload
systemctl enable anniemusic
echo "✅ Systemd service configured"
ENDSSH

# Step 7: Start the Bot
echo "🎵 Starting AnnieXMusic bot..."
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP << 'ENDSSH'
systemctl stop anniemusic 2>/dev/null
sleep 2
systemctl start anniemusic
sleep 5
ENDSSH

# Step 8: Check Status
echo ""
echo "📊 Bot Status:"
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "systemctl status anniemusic --no-pager | head -15"

echo ""
echo "📝 Recent Logs:"
sshpass -p "Akshay343402355468" ssh -p $SERVER_PORT $SERVER_USER@$SERVER_IP "journalctl -u anniemusic -n 10 --no-pager | tail -8"

echo ""
echo "=========================================="
echo "✅ Deployment Complete!"
echo "=========================================="
echo ""
echo "📋 Management Commands:"
echo "   Check status:    sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'systemctl status anniemusic'"
echo "   View logs:       sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'journalctl -u anniemusic -f'"
echo "   Restart bot:     sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'systemctl restart anniemusic'"
echo "   Stop bot:        sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'systemctl stop anniemusic'"
echo "   Update from Git: sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195 'cd /opt/AnnieXMusic && git pull && systemctl restart anniemusic'"
echo ""
echo "🔐 SSH Access:"
echo "   sshpass -p 'Akshay343402355468' ssh -p 22 root@161.118.250.195"
echo ""
