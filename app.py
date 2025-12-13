# app.py
# ------------------------------
# WinJar (Flask) – routes and page rendering
# ------------------------------
# What this file does:
# - Serves the main page (/) with today's entries, streak, and weekly summary
# - Handles adding a quick win (/add)
# - Lets the user add an optional "elaboration" after a win is created (/elaborate)
# - Exports all data as JSON (/export)
# Tip: If you change storage later (SQLite, Firebase), you won't touch this file's UI logic;
#      you'll only update data_access.py to keep things abstracted.

from flask import Flask, render_template, request, redirect, url_for, send_file, jsonify
from io import BytesIO
import json, datetime as dt
from data_access import DataAccess
from ai import mood_prompt, adaptive_streak_banner, progress_summary
from collections import defaultdict

app = Flask(__name__)
db = DataAccess()

@app.route("/", methods=["GET"])
def index():
    """Render the home page with today’s entries and personalization."""
    today = dt.date.today().isoformat()
    entries_today = db.list_entries_by_date(today)

    # last 7 days → summary text
    last_week = db.list_entries_last_n_days(7)
    weekly_summary = progress_summary(last_week) if last_week else "No entries yet—today’s a great day to start!"

    # Group last-week entries by date for the history section
    entries_by_date = defaultdict(list)
    for e in last_week:
        entries_by_date[e["date"]].append(e)

    # Sort dates newest → oldest
    history_dates = sorted(entries_by_date.keys(), reverse=True)


    # streak + adaptive banner text
    streak = db.get_streak_days()
    banner = adaptive_streak_banner(streak)

    # mood-specific prompt (placeholder) passed via ?mood=...
    prompt = mood_prompt(request.args.get("mood", ""))

    # if a new win was just added, we pass its id so the page can show the 'Elaborate' box
    new_id = request.args.get("new_id", "")

    return render_template(
        "index.html",
        entries_today=entries_today,
        streak=streak,
        banner=banner,
        weekly_summary=weekly_summary,
        prompt=prompt,
        new_id=new_id,
        history_dates=history_dates,
        history=entries_by_date
    )


@app.route("/add", methods=["POST"])
def add():
    """
    Handle the 'quick add' form.
    - Only the short text is required.
    - Mood/category are optional.
    - it immediately redirects back to home and show an inline 'Elaborate' box.
    """
    text = request.form.get("text", "").strip()
    mood = request.form.get("mood", "")
    category = request.form.get("category", "")

    if text:
        entry = db.add_entry(text=text, mood=mood, category=category)
        # Redirect with ?new_id=<id> so the page shows the optional elaboration form.
        return redirect(url_for("index", mood=mood, new_id=entry["id"]))

    return redirect(url_for("index"))

@app.route("/elaborate", methods=["POST"])
def elaborate():
    """
    Optional elaboration handler.
    - Receives an entry id and a longer 'details' note.
    - Saves on top of the existing quick win (does not replace it).
    """
    entry_id = request.form.get("entry_id", "")
    details = request.form.get("details", "").strip()
    if entry_id and details:
        db.update_details(entry_id, details)
    return redirect(url_for("index"))

@app.route("/export", methods=["GET"])
def export():
    """Download all entries as a JSON file (backup/portability)."""
    data = db.export_json()
    buf = BytesIO(json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8"))
    buf.seek(0)
    filename = f"winjar_export_{dt.date.today().isoformat()}.json"
    return send_file(buf, mimetype="application/json", as_attachment=True, download_name=filename)

@app.route("/health")
def health():
    """Simple healthcheck endpoint."""
    return jsonify({"status": "ok"})

@app.route("/history")
def full_history():
    """Show all wins, grouped by date, on a separate page."""
    entries = db.list_entries()  # all stored entries

    entries_by_date = defaultdict(list)
    for e in entries:
        entries_by_date[e["date"]].append(e)

    # Newest date first
    history_dates = sorted(entries_by_date.keys(), reverse=True)

    return render_template(
        "history.html",
        history_dates=history_dates,
        history=entries_by_date,
    )


if __name__ == "__main__":
    # Debug=True gives you nice error pages and auto-reload in development.
    app.run(debug=True)
