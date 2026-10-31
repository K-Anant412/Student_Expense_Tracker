-- Student Expense Tracker and Analyzer
-- Database Schema Definition (MySQL)

CREATE DATABASE IF NOT EXISTS student_expense_tracker CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE student_expense_tracker;

-- Table: users (Student profile / single-user isolation)
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    full_name VARCHAR(100) NOT NULL,
    college_name VARCHAR(150) DEFAULT 'College of Engineering & Technology',
    currency VARCHAR(10) DEFAULT '₹',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: categories (Income and Expense categorization)
CREATE TABLE IF NOT EXISTS categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    type ENUM('Income', 'Expense') NOT NULL,
    description VARCHAR(255) NULL,
    is_default BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_category_name_type UNIQUE (name, type)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: transactions (Financial transaction ledger)
CREATE TABLE IF NOT EXISTS transactions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT 1,
    category_id INT NOT NULL,
    type ENUM('Income', 'Expense') NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    date DATE NOT NULL,
    payment_method VARCHAR(50) NOT NULL DEFAULT 'UPI',
    description VARCHAR(255) NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE RESTRICT,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    INDEX idx_trans_date (date),
    INDEX idx_trans_type (type),
    INDEX idx_trans_cat (category_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Table: budgets (Monthly category spending budgets)
CREATE TABLE IF NOT EXISTS budgets (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT DEFAULT 1,
    category_id INT NOT NULL,
    month INT NOT NULL,
    year INT NOT NULL,
    amount DECIMAL(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL,
    CONSTRAINT uq_cat_month_year UNIQUE (category_id, month, year),
    INDEX idx_budget_period (year, month)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
