-- Create the database if it doesn't exist
CREATE DATABASE IF NOT EXISTS ruralflow CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

-- Use the database
USE ruralflow;

-- Create a dedicated user for the application
CREATE USER IF NOT EXISTS 'ruralflow_user'@'localhost' IDENTIFIED BY 'your_secure_password';

-- Grant necessary permissions
GRANT ALL PRIVILEGES ON ruralflow.* TO 'ruralflow_user'@'localhost';

-- Flush privileges to apply changes
FLUSH PRIVILEGES;