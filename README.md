# Genel Kultur README

## Overview

This web application is designed to generate Turkish trivia questions for users to answer. It utilizes Flask as the web framework, LLM model for question generation, Azure App Service for hosting, Azure SQL for database storage, and Google Login for user management.

## Features

- **Question Generation:** The application generates trivia questions with varying difficulty levels, categories, and types.
- **User Management:** Users can log in using their Google accounts to track their progress and scores.
- **Database Storage:** Azure SQL is used to store the generated questions and user information securely.

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/your-username/your-web-app.git
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Configure Azure services:

    - Set up an Azure SQL database and update the connection string in the `config.py` file.
    - Deploy the Flask app to Azure App Service.

4. Configure Google Login:

    - Set up a Google Developer Console project.
    - Obtain the client ID and secret and update them in the `config.py` file.

5. Run the application:

    ```bash
    flask run
    ```

## Database Schema

The application uses a SQL Server database with the following schema:

```sql
CREATE TABLE questions (
    id INT PRIMARY KEY IDENTITY(1,1),
    question NVARCHAR(MAX),
    answer NVARCHAR(MAX),
    score INT,
    qtype NVARCHAR(255),
    category NVARCHAR(255)
);

CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    google_id NVARCHAR(255),
    username NVARCHAR(255),
    email NVARCHAR(255),
    picture_url NVARCHAR(255),
    score INT
);
```

## Sample Questions

```sql
INSERT INTO [dbo].[questions] (question, answer, score, qtype, category)
VALUES 
('Mersin''de ''Eshab-i Kehf'' olarak bilinen mağaranın diğer adıdır ... UYURLAR MAĞARASI', 'yedi', 30, 'gercek', 'coğrafya'),
-- Add more questions here
```


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.