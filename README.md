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

## Features

- **User Authentication:** Users can register, log in, and log out.
  
- **Blog Post Management:**
  - **Rich Text Editor:** Create and edit blog posts using a powerful rich text editor for a seamless content creation experience.
  - **CRUD Operations:** Perform basic CRUD operations (Create, Read, Update, Delete) on blog posts.
  
- **Followers System:**
  - Users can follow and unfollow other users.
  - See a feed of posts from users they are following.

- **Responsive Design:** The application is designed to be accessible on various devices.

## Technologies Used

- **Flask:** A lightweight web framework for Python.
  
- **Tailwind CSS:** A utility-first CSS framework for building modern and responsive user interfaces.

- **Flask-CKEditor:** Integration of a rich text editor for creating and editing blog posts.

- **Database:** SQLite is used by default. You can modify the `config.py` file to use a different database if needed.


## Configuration

- **Database Configuration:** The application uses SQLite by default. You can modify the config.py file to use a different database.

## Contributing

- Contributions are welcome! If you find any issues or have suggestions for improvements, please create an issue or submit a pull request.

## Acknowledgments

- Flask: [https://flask.palletsprojects.com/](https://flask.palletsprojects.com/)
- Bootstrap: [https://getbootstrap.com/](https://getbootstrap.com/)
- Tailwind CSS: [https://tailwindcss.com/](https://tailwindcss.com/)

   
