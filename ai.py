# ai.py
# ------------------------------
# Tiny "AI-ish" helpers:
# - mood_prompt: selects a prompt based on mood (expandable list)
# - adaptive_streak_banner: changes encouragement text based on streak
# - progress_summary: a simple natural-language summary over recent entries
# ------------------------------
from collections import Counter

# You can freely edit the moods and prompts here.
MOOD_PROMPTS = {
    "stressed": "Take a breath—what’s one small thing that went right?",
    "anxious": "Name one tiny step you handled today.",
    "tired": "Low energy is okay—note one small thing you still did.",
    "okay": "What’s a small win you want to lock in today?",
    "focused": "While you’re in flow, capture one concrete win.",
    "motivated": "Ride the momentum—what win are you proud of?",
    "grateful": "What’s one thing you appreciated today?",
    "hopeful": "What small step today supports the bigger picture?",
    "great": "Great day! Document one highlight.",
    "": "What’s one small win worth capturing right now?"
}

def mood_prompt(mood: str) -> str:
    return MOOD_PROMPTS.get(mood.lower(), MOOD_PROMPTS[""])

def adaptive_streak_banner(streak_days: int) -> str:
    if streak_days == 0:
        return "Start fresh: one tiny win is all it takes."
    if streak_days == 1:
        return "1-day streak—let’s make it 2!"
    if streak_days < 7:
        return f"{streak_days}-day streak—keep the chain going."
    return f"{streak_days}-day streak—nice consistency!"

def progress_summary(entries_last_week):
    # Minimal NLP-ish summary: count entries and surface top categories.
    total = len(entries_last_week)
    cats = Counter((e.get("category") or "").lower() for e in entries_last_week if e.get("category"))
    lead = f"You logged {total} wins this week."
    if cats:
        top, count = cats.most_common(1)[0]
        lead += f" Most were in “{top}” ({count})."
    return lead
