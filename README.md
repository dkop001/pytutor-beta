# Gamified Python Tutor: Developer Documentation

Welcome to the internal developer guide for the PyTutor codebase. This document describes the application's architecture, what each script does, and how to safely edit or scale it in the future.

## 📂 Project Structure

```text
saas/
│
├── main.py                 # Core routing logic and application setup
├── data.py                 # State management and database models
├── database.py             # Database connectivity logic (SQLAlchemy placeholder)
│
├── static/                 
│   ├── css/styles.css      # Core Design System (Colors, Fonts, Layouts)
│   └── js/app.js           # Frontend interactivity (checking logic)
│
├── templates/              # Jinja2 HTML Views
│   ├── base.html           # Master layout scaffolding (Headers, imports)
│   ├── index.html          # Gamified path dashboard
│   ├── lesson.html         # Individual lesson quiz container
│   └── notes.html          # Python concepts guidebook
```

---

## 🐍 Backend Architecture (Python)

### 1. `main.py`
**Purpose**: This is the engine of your server. It boots up the Flask application and handles where traffic goes.
- **`@app.route('/')`**: Loads the homepage dashboard and unit lists.
- **`@app.route('/notes')`**: Loads the static Guidebook.
- **`@app.route('/lesson/<id>')`**: Intercepts requests to learn specific concepts, fetches the relevant questions from `data.py`, and maps them to the `lesson.html` interface.
- **`@app.route('/api/check_answer', methods=['POST'])`**: The invisible validation checkpoint. When a user clicks "Check" in a lesson, Javascript sends their answer here. It updates user XP/Hearts, processes whether the lesson was passed, and sends back the verdict.
- **How to Edit**: If you want to add an entirely new page (like `/profile` or `/leaderboard`), you put the route logic right here.

### 2. `data.py`
**Purpose**: The central source of truth for all content. 
- **`mock_user`**: Holds the current session variables for the player (Streak, XP, Hearts, unlock status).
- **`mock_lessons`**: The actual content payload. A dictionary mapping Lesson IDs to titles and multiple-choice questions. 
- **`mock_units`**: Defines the "Overworld" map geometry on the homepage (which lessons belong to which unit).
- **How to Edit**: To add a new lesson, add a new nested dictionary key (e.g. `9: { ... }`) to `mock_lessons`. Make sure to also inject its ID into `mock_units` so the map knows to render it. When migrating to MySQL, this file should be replaced with SQLAlchemy database models (e.g., `class User(db.Model)` and `class Lesson(db.Model)`).

### 3. `database.py`
**Purpose**: Clean boilerplate file holding future connectivity logic.
- **How to Edit**: When you launch this site with a live MySQL Database, put your `SQLAlchemy` connection URIs and environment variables into this file to prevent `main.py` from getting permanently cluttered.


---

## 🖥 Frontend Architecture (Javascript & HTML)

### 1. `static/js/app.js`
**Purpose**: Hooks directly into the user's browser, preventing page refreshes every time they check an answer.
- **Selection Logic**: Highlights an option when clicked by toggling the `selected` CSS class.
- **Validation Execution (`/api/check_answer`)**: Fires an invisible `fetch()` API request to `main.py` pushing the `answer_id` and the `lesson_id`.
- **Response Handling**: Reads the API verdict (True/False). If true, it paints the element green (`correct-state`) and reveals the Continue button. If false, it paints it red (`wrong`).
- **How to Edit**: If you want to add Sound Effects (e.g., *ding* when correct), you uncomment the Audio execution lines in the `if(data.correct)` block. If you want to add different quiz types (like fill-in-the-blank), you expand the Javascript listeners here.

### 2. `templates/`
**Purpose**: Flask passes raw data (like XP) into these files to be evaluated dynamically before the website is shipped to the user. 
- **`base.html`**: The skeleton. Loads font files (`Inter`) and FontAwesome generic scripts. Change your global `<title>` definitions here.
- **`lesson.html`**: The engine of the quiz view. Parses Jinja `progress` arrays to build health bars and render dynamic question loops. 

---

## 🎨 Design System

### `static/css/styles.css`
**Purpose**: Defines your custom Indigo/Violet Gamified aesthetics.
- **`:root { ... }` block**: Every color inside the app pulls from these global root variables. 
- **How to Edit**: If you want to re-brand the site down the line (e.g. from Indigo to Dark Mode or Crimson Red), you **only** need to edit the color variables on Line `1` to `14`. The entire site will universally adapt to the new palette. You don't have to manually hunt down Hex codes anymore. 

## 🚀 Scaling Protocol (Summary)
When you are ready to publish and onboard real users:
1. Setup a MySQL database instance.
2. Spin up `SQLAlchemy` in `database.py` to map properties directly to SQL Rows.
3. Migrate configurations from `data.py` directly into the database.
4. Scale your question architectures!
