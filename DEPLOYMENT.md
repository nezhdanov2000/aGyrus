# Deployment Guide для Ubuntu Server

## 1. Установка зависимостей

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Apache
sudo apt install apache2 -y

# Установка PHP и расширений
sudo apt install php php-mysql php-curl php-json php-cli -y

# Установка MySQL
sudo apt install mysql-server -y

# Включение модулей Apache
sudo a2enmod rewrite
sudo systemctl restart apache2
```

## 2. Настройка MySQL

```bash
# Безопасная установка MySQL
sudo mysql_secure_installation

# Создание базы данных
sudo mysql -u root -p << 'SQL'
CREATE DATABASE aGyrus_db;
CREATE USER 'agyrus_user'@'localhost' IDENTIFIED BY 'STRONG_PASSWORD_HERE';
GRANT ALL PRIVILEGES ON aGyrus_db.* TO 'agyrus_user'@'localhost';
FLUSH PRIVILEGES;
SQL

# Импорт схемы
sudo mysql -u root -p aGyrus_db < aGyrus_db.sql
```

## 3. Установка проекта

```bash
# Клонирование репозитория
cd /var/www/html
sudo git clone https://github.com/nezhdanov2000/aGyrus.git
sudo chown -R www-data:www-data aGyrus
sudo chmod -R 755 aGyrus
```

## 4. Настройка конфигурации

```bash
cd /var/www/html/aGyrus/backend/config
sudo cp config.example.php config.php
sudo nano config.php
```

**Изменить в config.php:**
```php
// Google OAuth Configuration
define('GOOGLE_CLIENT_ID', 'your-real-client-id');
define('GOOGLE_CLIENT_SECRET', 'your-real-client-secret');
define('GOOGLE_REDIRECT_URI', 'https://yourdomain.com/backend/auth/google/callback.php');

// Database configuration
define('DB_HOST', 'localhost');
define('DB_NAME', 'aGyrus_db');
define('DB_USER', 'agyrus_user');
define('DB_PASS', 'STRONG_PASSWORD_HERE');

// Debug mode - MUST BE FALSE IN PRODUCTION!
define('DEBUG_MODE', false);
```

## 5. Настройка Apache VirtualHost

```bash
sudo nano /etc/apache2/sites-available/agyrus.conf
```

```apache
<VirtualHost *:80>
    ServerName yourdomain.com
    DocumentRoot /var/www/html/aGyrus
    
    <Directory /var/www/html/aGyrus>
        Options -Indexes +FollowSymLinks
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog ${APACHE_LOG_DIR}/agyrus_error.log
    CustomLog ${APACHE_LOG_DIR}/agyrus_access.log combined
</VirtualHost>
```

```bash
# Включение сайта
sudo a2ensite agyrus.conf
sudo systemctl reload apache2
```

## 6. SSL/HTTPS (рекомендуется)

```bash
# Установка Certbot
sudo apt install certbot python3-certbot-apache -y

# Получение SSL сертификата
sudo certbot --apache -d yourdomain.com
```

## 7. Проверка работоспособности

- Откройте браузер: https://yourdomain.com
- Проверьте авторизацию через Google
- Протестируйте API эндпоинты

## 8. Безопасность

```bash
# Защита config.php
sudo chmod 600 /var/www/html/aGyrus/backend/config/config.php

# Настройка firewall
sudo ufw allow 'Apache Full'
sudo ufw enable

# Настройка логов
sudo chmod 640 /var/log/apache2/agyrus_*.log
```

## Требования к серверу:
- Ubuntu 20.04 LTS или новее
- PHP 7.4+
- MySQL 5.7+ или MariaDB 10.3+
- Apache 2.4+ с mod_rewrite
- 1GB RAM минимум
- 10GB свободного места на диске
