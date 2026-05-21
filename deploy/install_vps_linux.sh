
#!/bin/bash
apt update -y
apt install -y docker.io docker-compose nginx certbot python3-certbot-nginx
systemctl enable docker
systemctl start docker

echo "Copier nginx_ifgsolution.conf dans /etc/nginx/sites-available/ifgsolution.fr"
echo "Activer HTTPS avec : certbot --nginx -d ifgsolution.fr -d www.ifgsolution.fr"
