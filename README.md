# 🎓 AcAI Backend - Academic AI Accreditation Platform

## 🚀 Overview

AcAI Backend is a sophisticated text prompt accreditation system designed to revolutionize academic credential information extraction using advanced AI technologies.

![Python Version](https://img.shields.io/badge/Python-3.13.0+-blue.svg)
![FastAPI](https://img.shields.io/badge/Framework-FastAPI-green.svg)
![SQLAlchemy](https://img.shields.io/badge/ORM-SQLAlchemy-red.svg)
![AI Powered](https://img.shields.io/badge/AI-Powered-blueviolet.svg)

## 🌟 Key Features

- 🤖 AI-Powered Text Prompt Analysis
- 🔍 Advanced Search and Filtering
- 📈 Fast and Easy to Install
- 🕶️ Not so State of Art Parser Implementation

## 🛠 Tech Stack

- **Backend Framework**: FastAPI
- **ORM**: SQLAlchemy
- **Database**: SQLite & MySQL

## 🚀 Quick Start

### Prerequisites
- Python 3.13+
- [AcAI Core](https://github.com/ForgeSherpa/acai-core) / MockAPI

### Setting up MockAPI (optional)

Install [Mockoon](https://mockoon.com/download/), import `mock-api.json`. Run.

### Installation (Linux Only Guide)

```bash
# clone the repo
git clone https://github.com/ForgeSherpa/acai-backend

# Create the virtual environment
python -m venv . # or venv/
source bin/activate

# install dependencies
pip install -r requirements.txt

# Serve
python cli.py serve
```

### SQLite Setup

```bash
cp .env.example .env
python cli.py migrate:schema
python cli.py migrate
```

### MySQL Setup

```bash
cp .env.example .env
# Set USE_SQLITE to true in the ENV
sed -i 's/\(USE_SQLITE=\)true/\1false/' .env
# Set the MySQL credentials or just use nano/vim.
# sed -i 's/\(MYSQL_USER=\)root/\1your_user/' .env
# sed -i 's/\(MYSQL_PASSWORD=\)/\1your_password/' .env
# sed -i 's/\(MYSQL_HOST=\)localhost/\1your_host/' .env
# sed -i 's/\(MYSQL_DB=\)acai/\1your_database/' .env
python cli.py migrate:schema
python cli.py migrate
```

> Windows users, please consult ChatGPT for assistance in case you don't know.

## Made with ❤️ by AcAI Team

- [@Justatnann](https://www.github.com/Justatnann) - Designer / Data Collector
- [@Albetnv](https://www.github.com/albetnov) - BackEnd Developer
- [@DJason](https://www.github.com/Djason28) - Data Scientist / Model Developer
- [@Wira](https://www.github.com/Wira) - Designer / Front End Developer
- [@JesenJeverlino](https://www.github.com/JesenJeverlino) - Designer / Front End Developer
- @Kelvin - Data Scientist / Model Developer
