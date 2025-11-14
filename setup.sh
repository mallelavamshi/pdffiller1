#!/bin/bash

# PDF Filler API - Quick Setup Script
# This script automates the initial setup on Ubuntu server

set -e  # Exit on error

echo "=================================="
echo "PDF Filler API - Quick Setup"
echo "=================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_info() {
    echo -e "${YELLOW}ℹ $1${NC}"
}

# Check if running as root
if [ "$EUID" -ne 0 ]; then 
    print_error "Please run as root (use sudo)"
    exit 1
fi

print_info "Starting setup..."

# Update system
print_info "Updating system packages..."
apt update && apt upgrade -y
print_success "System updated"

# Install Docker
print_info "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    usermod -aG docker ubuntu
    systemctl enable docker
    systemctl start docker
    rm get-docker.sh
    print_success "Docker installed"
else
    print_success "Docker already installed"
fi

# Install Docker Compose
print_info "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    apt install docker-compose -y
    print_success "Docker Compose installed"
else
    print_success "Docker Compose already installed"
fi

# Install Java for Jenkins
print_info "Installing Java..."
if ! command -v java &> /dev/null; then
    apt install openjdk-11-jdk -y
    print_success "Java installed"
else
    print_success "Java already installed"
fi

# Install Jenkins
print_info "Installing Jenkins..."
if ! command -v jenkins &> /dev/null; then
    curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | tee \
        /usr/share/keyrings/jenkins-keyring.asc > /dev/null

    echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
        https://pkg.jenkins.io/debian-stable binary/ | tee \
        /etc/apt/sources.list.d/jenkins.list > /dev/null

    apt update
    apt install jenkins -y

    # Change Jenkins port to 9090
    print_info "Configuring Jenkins to use port 9090..."
    sed -i 's/HTTP_PORT=8080/HTTP_PORT=9090/g' /etc/default/jenkins

    systemctl enable jenkins
    systemctl start jenkins
    print_success "Jenkins installed on port 9090"

    sleep 5
    print_info "Jenkins initial admin password:"
    cat /var/lib/jenkins/secrets/initialAdminPassword
else
    print_success "Jenkins already installed"
fi

# Install Nginx
print_info "Installing Nginx..."
if ! command -v nginx &> /dev/null; then
    apt install nginx -y
    systemctl enable nginx
    systemctl start nginx
    print_success "Nginx installed"
else
    print_success "Nginx already installed"
fi

# Install Git
print_info "Installing Git..."
if ! command -v git &> /dev/null; then
    apt install git -y
    print_success "Git installed"
else
    print_success "Git already installed"
fi

# Install other utilities
print_info "Installing utilities..."
apt install curl wget net-tools ufw -y
print_success "Utilities installed"

# Configure firewall
print_info "Configuring firewall..."
ufw --force enable
ufw allow 22/tcp    # SSH
ufw allow 80/tcp    # HTTP
ufw allow 443/tcp   # HTTPS
ufw allow 9090/tcp  # Jenkins
ufw allow 8003/tcp  # Application
print_success "Firewall configured"

# Create application directories
print_info "Creating application directories..."
mkdir -p /opt/pdf-filler/templates
mkdir -p /opt/pdf-filler/outputs
chown -R ubuntu:ubuntu /opt/pdf-filler
print_success "Directories created"

# Display versions
echo ""
echo "=================================="
echo "Installation Complete!"
echo "=================================="
echo "Installed versions:"
echo "  - Docker: $(docker --version)"
echo "  - Docker Compose: $(docker-compose --version)"
echo "  - Java: $(java -version 2>&1 | head -n 1)"
echo "  - Nginx: $(nginx -v 2>&1)"
echo "  - Git: $(git --version)"
echo ""
echo "Port Configuration:"
echo "  - Application: 8003"
echo "  - Jenkins: 9090"
echo "  - Nginx HTTP: 80"
echo "  - Nginx HTTPS: 443"
echo ""
echo "Next steps:"
echo "  1. Access Jenkins: http://YOUR_SERVER_IP:9090"
echo "  2. Clone your repository to /opt/pdf-filler"
echo "  3. Copy PDF template to /opt/pdf-filler/templates/"
echo "  4. Configure Jenkins pipeline"
echo "  5. Deploy application"
echo ""
echo "=================================="
