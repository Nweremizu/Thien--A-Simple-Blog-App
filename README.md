# Thien -- A Simple Flask Blog Application

This is a simple blog application built with Flask, a lightweight web framework for Python. The application allows users to create, read, update, and delete blog posts.

## Features

- User Authentication: Users can register, log in, and log out.
- Blog Post Management: Users can create, edit, and delete their blog posts.
- Responsive Design: The application is designed to be accessible on various devices( with some bugs though ).

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/flask-blog-app.git
   cd flask-blog-app```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   pip install -r requirements.txt```

3. Set Up The Database
    <!-- Note this is to be done in the terminal  -->
   ```
   flask db init
   flask db migrate
   flask db upgrade
   ```
   
4. Run The Application
   ```
   flask run
   ```
   
