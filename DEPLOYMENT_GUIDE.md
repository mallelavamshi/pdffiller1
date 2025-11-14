# PDF Form Filler API - Deployment Guide

## Complete CI/CD Setup with Docker, GitHub, Jenkins on Ubuntu Hostinger Server

---

## 📋 Prerequisites

### On Your Local Machine:
- Docker installed
- Git installed
- GitHub account
- DockerHub account (optional, for Docker registry)

### On Ubuntu Hostinger Server:
- Ubuntu 20.04 or later
- Root or sudo access
- Minimum 2GB RAM
- 20GB disk space

---

## 🚀 Part 1: Local Setup & Testing

### 1. Project Structure
```
pdf-filler-api/
├── main.py                 # FastAPI application
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker Compose configuration
├── Jenkinsfile            # Jenkins CI/CD pipeline
├── requirements.txt       # Python dependencies
├── .dockerignore          # Docker ignore file
├── .gitignore            # Git ignore file
├── README.md             # This file
└── templates/            # Place PDF template here
    └── Letter_of_Representation_Fillable.pdf
```

### 2. Setup Template Directory
```bash
# Create templates directory
mkdir -p templates

# Copy your PDF template
cp Letter_of_Representation_Fillable.pdf templates/
```

### 3. Test Locally with Docker

#### Build Docker Image:
```bash
docker build -t pdf-filler-api .
```

#### Run Container:
```bash
docker run -d \
  --name pdf-filler-api \
  -p 8000:8000 \
  -v $(pwd)/templates:/app/templates \
  pdf-filler-api
```

#### Test API:
```bash
# Health check
curl http://localhost:8000/health

# Test file upload (using your Excel file)
curl -X POST "http://localhost:8000/fill-pdf" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@Letter_of_Representation_Sample_Data.xlsx" \
  --output filled_pdf.pdf
```

#### Using Docker Compose:
```bash
# Start service
docker-compose up -d

# View logs
docker-compose logs -f

# Stop service
docker-compose down
```

---

## 🐙 Part 2: GitHub Repository Setup

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: PDF Filler API"
```

### 2. Create GitHub Repository
1. Go to https://github.com/new
2. Create a new repository (e.g., `pdf-filler-api`)
3. Don't initialize with README

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/pdf-filler-api.git
git branch -M main
git push -u origin main
```

---

## 🖥️ Part 3: Ubuntu Server Setup

### 1. SSH into Your Hostinger Server
```bash
ssh ubuntu@YOUR_SERVER_IP
```

### 2. Update System
```bash
sudo apt update && sudo apt upgrade -y
```

### 3. Install Docker
```bash
# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh

# Add user to docker group
sudo usermod -aG docker $USER

# Start Docker service
sudo systemctl enable docker
sudo systemctl start docker

# Verify installation
docker --version
```

### 4. Install Docker Compose
```bash
sudo apt install docker-compose -y
docker-compose --version
```

### 5. Install Java (for Jenkins)
```bash
sudo apt install openjdk-11-jdk -y
java -version
```

### 6. Install Jenkins
```bash
# Add Jenkins repository
curl -fsSL https://pkg.jenkins.io/debian-stable/jenkins.io-2023.key | sudo tee \
  /usr/share/keyrings/jenkins-keyring.asc > /dev/null

echo deb [signed-by=/usr/share/keyrings/jenkins-keyring.asc] \
  https://pkg.jenkins.io/debian-stable binary/ | sudo tee \
  /etc/apt/sources.list.d/jenkins.list > /dev/null

# Install Jenkins
sudo apt update
sudo apt install jenkins -y

# Start Jenkins
sudo systemctl enable jenkins
sudo systemctl start jenkins

# Get initial admin password
sudo cat /var/lib/jenkins/secrets/initialAdminPassword
```

### 7. Configure Firewall
```bash
# Allow SSH
sudo ufw allow 22/tcp

# Allow Jenkins
sudo ufw allow 8080/tcp

# Allow Application
sudo ufw allow 8000/tcp

# Enable firewall
sudo ufw enable
```

### 8. Create Application Directories
```bash
sudo mkdir -p /opt/pdf-filler/templates
sudo mkdir -p /opt/pdf-filler/outputs
sudo chown -R ubuntu:ubuntu /opt/pdf-filler
```

---

## 🔧 Part 4: Jenkins Configuration

### 1. Access Jenkins
Open browser: `http://YOUR_SERVER_IP:8080`

### 2. Initial Setup
1. Enter the initial admin password
2. Install suggested plugins
3. Create admin user
4. Configure Jenkins URL: `http://YOUR_SERVER_IP:8080`

### 3. Install Required Plugins
1. Go to: Manage Jenkins → Manage Plugins
2. Install these plugins:
   - Docker Pipeline
   - Git Plugin
   - SSH Agent Plugin
   - Pipeline Plugin
   - GitHub Integration Plugin

### 4. Configure Credentials

#### DockerHub Credentials:
1. Manage Jenkins → Manage Credentials
2. Add Credentials → Username with password
3. ID: `dockerhub-credentials`
4. Username: Your DockerHub username
5. Password: Your DockerHub password

#### SSH Credentials:
1. Generate SSH key on Jenkins server:
```bash
sudo su - jenkins
ssh-keygen -t rsa -b 4096
cat ~/.ssh/id_rsa.pub
```

2. Add public key to server's authorized_keys:
```bash
# On your deployment server
echo "PUBLIC_KEY_HERE" >> ~/.ssh/authorized_keys
```

3. In Jenkins:
   - Add Credentials → SSH Username with private key
   - ID: `ssh-credentials`
   - Username: `ubuntu`
   - Private Key: Enter directly (paste private key)

#### GitHub Credentials:
1. Generate GitHub Personal Access Token:
   - GitHub → Settings → Developer settings → Personal access tokens
   - Generate new token with `repo` access

2. In Jenkins:
   - Add Credentials → Secret text
   - ID: `github-token`
   - Secret: Your GitHub token

### 5. Create Jenkins Pipeline Job

1. New Item → Pipeline → Enter name: `pdf-filler-api-pipeline`

2. Configure Pipeline:
   - **General**:
     - ✓ GitHub project
     - Project URL: `https://github.com/YOUR_USERNAME/pdf-filler-api`

   - **Build Triggers**:
     - ✓ GitHub hook trigger for GITScm polling

   - **Pipeline**:
     - Definition: Pipeline script from SCM
     - SCM: Git
     - Repository URL: `https://github.com/YOUR_USERNAME/pdf-filler-api.git`
     - Credentials: Select your GitHub credentials
     - Branch: `*/main`
     - Script Path: `Jenkinsfile`

3. Save

### 6. Configure GitHub Webhook

1. Go to GitHub repository → Settings → Webhooks
2. Add webhook:
   - Payload URL: `http://YOUR_SERVER_IP:8080/github-webhook/`
   - Content type: `application/json`
   - Events: Just the push event
   - Active: ✓

---

## 🔄 Part 5: Update Jenkinsfile Configuration

Edit the `Jenkinsfile` in your repository and update these values:

```groovy
environment {
    DOCKER_REGISTRY = 'your-dockerhub-username'  // Your DockerHub username
    DEPLOY_SERVER = 'your-server-ip'             // Your Hostinger server IP
}
```

Commit and push:
```bash
git add Jenkinsfile
git commit -m "Update Jenkinsfile with server details"
git push origin main
```

---

## 📦 Part 6: Deployment Process

### Automatic Deployment (via Jenkins):

1. Make changes to your code
2. Commit and push to GitHub:
```bash
git add .
git commit -m "Your commit message"
git push origin main
```

3. Jenkins will automatically:
   - Detect the push via webhook
   - Pull code from GitHub
   - Build Docker image
   - Run tests
   - Push to DockerHub
   - Deploy to your server
   - Run health checks

### Manual Deployment (without Jenkins):

```bash
# SSH to server
ssh ubuntu@YOUR_SERVER_IP

# Clone repository
cd /opt
sudo git clone https://github.com/YOUR_USERNAME/pdf-filler-api.git
cd pdf-filler-api

# Copy PDF template
sudo cp /path/to/Letter_of_Representation_Fillable.pdf templates/

# Deploy with Docker Compose
sudo docker-compose up -d

# Check logs
sudo docker-compose logs -f
```

---

## 🧪 Part 7: Testing the Deployed API

### Test Health Endpoint:
```bash
curl http://YOUR_SERVER_IP:8000/health
```

### Test PDF Generation:
```bash
curl -X POST "http://YOUR_SERVER_IP:8000/fill-pdf" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@Letter_of_Representation_Sample_Data.xlsx" \
  --output filled_pdf.pdf
```

### API Documentation:
Visit: `http://YOUR_SERVER_IP:8000/docs`

---

## 🔍 Part 8: Monitoring & Maintenance

### View Application Logs:
```bash
# Docker logs
docker logs pdf-filler-api -f

# Docker Compose logs
docker-compose logs -f
```

### Check Container Status:
```bash
docker ps
```

### Restart Application:
```bash
docker restart pdf-filler-api
# or
docker-compose restart
```

### Clean Up Old Files:
```bash
# Via API
curl -X DELETE http://YOUR_SERVER_IP:8000/cleanup

# Manual cleanup
rm -rf /opt/pdf-filler/outputs/*
```

### Monitor Server Resources:
```bash
# Check disk space
df -h

# Check memory
free -h

# Check CPU
top
```

### Update Application:
```bash
# Pull latest changes
cd /opt/pdf-filler-api
git pull origin main

# Rebuild and restart
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

---

## 🔒 Part 9: Security Best Practices

### 1. Secure Jenkins:
```bash
# Change default port
sudo nano /etc/default/jenkins
# Change HTTP_PORT=8080 to another port

# Restart Jenkins
sudo systemctl restart jenkins
```

### 2. Enable HTTPS (with Let's Encrypt):
```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx -y

# Install Nginx
sudo apt install nginx -y

# Configure Nginx reverse proxy for your API
sudo nano /etc/nginx/sites-available/pdf-filler-api
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/pdf-filler-api /etc/nginx/sites-enabled/

# Test Nginx configuration
sudo nginx -t

# Restart Nginx
sudo systemctl restart nginx

# Get SSL certificate
sudo certbot --nginx -d your-domain.com
```

### 3. Implement API Key Authentication:
Update `main.py` to add API key validation (optional enhancement)

### 4. Regular Backups:
```bash
# Backup templates
tar -czf templates-backup-$(date +%Y%m%d).tar.gz /opt/pdf-filler/templates

# Backup Jenkins
tar -czf jenkins-backup-$(date +%Y%m%d).tar.gz /var/lib/jenkins
```

---

## 🐛 Troubleshooting

### Issue: Jenkins can't connect to Docker
```bash
# Add Jenkins user to docker group
sudo usermod -aG docker jenkins
sudo systemctl restart jenkins
```

### Issue: Port already in use
```bash
# Check what's using the port
sudo lsof -i :8000

# Kill the process or change port in docker-compose.yml
```

### Issue: Permission denied errors
```bash
# Fix ownership
sudo chown -R ubuntu:ubuntu /opt/pdf-filler
```

### Issue: Container keeps restarting
```bash
# Check logs
docker logs pdf-filler-api

# Check if template exists
ls -la /opt/pdf-filler/templates/
```

---

## 📚 Additional Resources

- FastAPI Documentation: https://fastapi.tiangolo.com
- Docker Documentation: https://docs.docker.com
- Jenkins Documentation: https://www.jenkins.io/doc
- GitHub Actions (Alternative CI/CD): https://docs.github.com/actions

---

## 🎯 Quick Reference Commands

```bash
# Start application
docker-compose up -d

# Stop application
docker-compose down

# View logs
docker-compose logs -f

# Rebuild image
docker-compose build --no-cache

# SSH to server
ssh ubuntu@YOUR_SERVER_IP

# Check Jenkins logs
sudo journalctl -u jenkins -f

# Restart Jenkins
sudo systemctl restart jenkins

# Update from Git
git pull origin main && docker-compose up -d --build
```

---

## 📞 Support

For issues or questions:
1. Check the logs first
2. Review this documentation
3. Check Docker/Jenkins/FastAPI documentation

---

**Last Updated:** November 2025
**Version:** 1.0.0
