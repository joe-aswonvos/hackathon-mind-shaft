# MindShaft

## Overview
MindShaft is a Django-based web application designed to simplify the process of managing and studying flashcards. It provides an intuitive interface for creating, organizing, and reviewing your flashcards, making it easier to retain knowledge and improve learning efficiency.

---

## Table of Contents
1. [Purpose and Scope](#purpose-and-scope)
2. [Technologies Used](#technologies-used)
3. [Features and Functionality](#features-and-functionality)
    - [Models](#models)
    - [Pages and Interaction](#pages-and-interaction)
4. [How to Run the Project](#how-to-run-the-project)
5. [Future Scope](#future-scope)
6. [Contributing](#contributing)
7. [License](#license)

---

## Purpose and Scope

MindShaft aims to provide:
- A robust flashcard management system for students, educators, and lifelong learners.
- A simple yet powerful interface to create, edit, and delete flashcards.
- Functionality for organizing flashcards into categories or decks for easy access.
- A study/review mode to facilitate better retention of knowledge.

The application is scalable and can be extended to incorporate advanced features like spaced repetition algorithms and user collaboration.

---

## Technologies Used

MindShaft is built using the following technologies:
- **Programming Language:** Python (v3.9+)
- **Web Framework:** Django (v4.x)
- **Frontend Technologies:** HTML5, CSS3, JavaScript
- **Database:** SQLite (default) - configurable to PostgreSQL, MySQL, etc.
- **Version Control:** Git
- **Deployment Platform:** Localhost (development) — Ready for deployment on Heroku, AWS, or other cloud providers.

---

## Features and Functionality

### Models
MindShaft leverages Django's ORM to define data models for the application:
1. **Deck**: Represents a collection of flashcards under a specific topic or category.
    - Fields: `name`, `description`, `created_at`, `updated_at`
2. **Card**: Represents an individual flashcard with a front (question) and a back (answer).
    - Fields: `question`, `answer`, `deck`, `created_at`, `updated_at`

### Pages and Interaction
The following pages provide seamless interaction with the system:
1. **Home Page**:
    - Overview of the application with navigation links to decks and study modes.
2. **Decks Page**:
    - Users can create, view, and delete decks.
3. **Flashcard Management**:
    - Add flashcards to decks and edit/delete them as necessary.
4. **Study Mode**:
    - Review deck contents in a user-friendly interface.
    - Optional features: shuffle cards, mark as learned, etc.
5. **Admin Dashboard**:
    - Django-admin to manage the database manually (for advanced users).

### Interaction Diagram
The interaction between models, pages, and the database can be visualized as follows:
1. **Deck <> Card Relationship**: Each deck contains multiple cards (One-To-Many).
2. **User Interaction**: User actions on pages update models and reflect in the database.

---

## How to Run the Project

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/MindShaft.git
   cd MindShaft
   ```

2. **Set up a Virtual Environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate   # Linux/Mac
   venv\Scripts\activate      # Windows
   ```

3. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Apply Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Run the Development Server**:
   ```bash
   python manage.py runserver
   ```

6. **Access the Application**:
   Visit [http://127.0.0.1:8000/](http://127.0.0.1:8000/) in your web browser.

---

## Future Scope

- Implementing a spaced repetition algorithm for smarter study sessions.
- User authentication to support collaborative decks and personalized flashcards.
- Integration with third-party APIs (e.g., Anki, Quizlet) for import/export functionality.
- Deployment to a production environment with containerization (Docker) or cloud hosting.

---

## Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create a new branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes:
   ```bash
   git commit -m "Describe the feature/fix briefly"
   ```
4. Push to your branch:
   ```bash
   git push origin feature-name
   ```
5. Submit a pull request.

---

## License

This project is licensed under the MIT License. See the [`LICENSE`](LICENSE) file for details.