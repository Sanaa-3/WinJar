# WinJar — Micro-Journaling for Small Wins & Reflection

WinJar is a lightweight journaling application designed to help users capture small daily wins, reflect when needed, and build motivation through positive reinforcement.  
The goal is to make journaling fast, flexible, and emotionally supportive — not rigid or overwhelming.


## Features (MVP)

- **Quick Win Entry:** Add a short “win” in under 10 seconds.
- **Optional Elaboration:** Expand a win into a longer reflection whenever you want.
- **Mood-Based Prompts:** Personalized journaling prompts based on mood.
- **Adaptive Streak Banner:** Encouraging messages that change depending on streak length.
- **Weekly Summary:** Simple NLP-style summary of wins from the last 7 days.
- **Export to JSON:** Download all entries as a JSON file.
- **Storage Abstraction Layer:** `DataAccess` module allows swapping JSON → SQLite → cloud later.


## Why WinJar?

Big goals can feel far away. Small wins build momentum and confidence.
WinJar helps users focus on consistent progress — not perfection.

It supports:
- Students managing workload
- Professionals balancing life and career
- Anyone trying to build healthier mental habits


## Tech Stack

- **Python 3**
- **Flask** (backend + templating)
- **HTML/CSS** (UI)
- **JSON Storage** (via `DataAccess`)
- Future: SQLite, Postgres, Firebase


## Project Structure

``
winjar/
├── app.py # Flask routes + rendering
├── ai.py # Mood prompts, streak messages, weekly summaries
├── data_access.py # Storage abstraction layer
├── templates/
│ └── index.html # Main UI
└── data/
└── entries.json # Auto-generated data file
└── README.md 
``


# Running WinJar (VS Code Setup Instructions)

Follow these steps exactly.

## 1 Open the Project in VS Code

- Go to **File → Open Folder**
- Select the **winjar** folder

## 2 Open a Terminal

**Terminal → New Terminal**

Make sure your terminal path ends in: ./winjar $
If not, run:
`bash`
`cd winjar`

## 3 Create a Virtual Environment
**Mac / Linux**

`python3 -m venv venv`
`source venv/bin/activate`

**Windows**
`python -m venv venv`
`venv\Scripts\activate`

You should now see:
`(venv)`

## 4 Install Flask
`pip install flask`

## 5 Run the App
**Mac / Linux**
`python3 app.py`

**Windows**
`python app.py`

If successful, you will see:
`* Running on http://127.0.0.1:5000`

## Running the App Later

Every time you reopen VS Code:
1. Open a terminal
2. Activate the virtual environment

Mac:
`source venv/bin/activate`

Windows
`venv\Scripts\activate`

3. Run the App
`python app.py`
