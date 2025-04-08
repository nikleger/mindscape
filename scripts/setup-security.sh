#!/bin/bash

# Setup Security Script

# Generate SSL certificates
echo "Generating SSL certificates..."
mkdir -p certs
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
  -keyout certs/private.key -out certs/certificate.crt \
  -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Set up environment variables
echo "Setting up environment variables..."
cat > .env << EOF
# Security
JWT_SECRET=$(openssl rand -hex 32)
REFRESH_TOKEN_SECRET=$(openssl rand -hex 32)
ENCRYPTION_KEY=$(openssl rand -hex 32)

# Database
DB_USER=postgres
DB_PASSWORD=$(openssl rand -hex 16)
DB_NAME=mindscape
DB_HOST=localhost
DB_PORT=5432

# API
API_PORT=8000
API_HOST=0.0.0.0
CORS_ORIGINS=http://localhost:3000

# Frontend
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_WS_URL=ws://localhost:8000
EOF

# Set up database security
echo "Setting up database security..."
psql -U postgres << EOF
ALTER USER postgres WITH PASSWORD '$(grep DB_PASSWORD .env | cut -d '=' -f2)';
CREATE DATABASE mindscape;
\c mindscape
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pgcrypto";
EOF

# Set up firewall rules
echo "Setting up firewall rules..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 22/tcp
    sudo ufw allow 80/tcp
    sudo ufw allow 443/tcp
    sudo ufw allow 3000/tcp
    sudo ufw allow 8000/tcp
    sudo ufw enable
fi

# Set up fail2ban
echo "Setting up fail2ban..."
if command -v fail2ban-client &> /dev/null; then
    sudo cp /etc/fail2ban/jail.conf /etc/fail2ban/jail.local
    sudo systemctl enable fail2ban
    sudo systemctl start fail2ban
fi

# Set up automatic security updates
echo "Setting up automatic security updates..."
if command -v apt-get &> /dev/null; then
    sudo apt-get install -y unattended-upgrades
    sudo dpkg-reconfigure -plow unattended-upgrades
fi

# Set up file permissions
echo "Setting up file permissions..."
find . -type f -exec chmod 644 {} \;
find . -type d -exec chmod 755 {} \;
find . -name "*.sh" -exec chmod +x {} \;

# Create security audit script
echo "Creating security audit script..."
cat > scripts/security-audit.sh << 'EOF'
#!/bin/bash

# Security Audit Script

echo "Running security audit..."

# Check for outdated packages
echo "Checking for outdated packages..."
if command -v apt-get &> /dev/null; then
    apt-get update
    apt-get upgrade -s
fi

# Check for open ports
echo "Checking for open ports..."
netstat -tuln

# Check for failed login attempts
echo "Checking for failed login attempts..."
if command -v fail2ban-client &> /dev/null; then
    fail2ban-client status
fi

# Check SSL certificate expiration
echo "Checking SSL certificate expiration..."
openssl x509 -in certs/certificate.crt -noout -dates

# Check file permissions
echo "Checking file permissions..."
find . -type f -perm /o+w -ls
find . -type f -perm /o+x -ls

# Check for sensitive information
echo "Checking for sensitive information..."
grep -r "password\|secret\|key\|token" --exclude-dir=.git --exclude-dir=node_modules .

echo "Security audit complete."
EOF

chmod +x scripts/security-audit.sh

echo "Security setup complete!" 