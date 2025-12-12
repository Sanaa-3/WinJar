# data_access.py
# ------------------------------
# All reads/writes go through this module.
# If you later move to SQLite or a cloud DB, keep the same method names/signatures
# and update the internals here—no UI code needs to change.
# ------------------------------
import json, os, uuid, datetime as dt

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(DATA_DIR, exist_ok=True)
JSON_PATH = os.path.join(DATA_DIR, "entries.json")

class DataAccess:
    def __init__(self, path=JSON_PATH):
        self.path = path
        if not os.path.exists(self.path):
            self._write({"entries": []})

    # --- low-level IO ---
    def _read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write(self, obj):
        with open(self.path, "w", encoding="utf-8") as f:
            json.dump(obj, f, ensure_ascii=False, indent=2)

    # --- public API used by app.py ---
    def add_entry(self, text, mood="", category=""):
        """Create a new quick win. 'details' can be added later via update_details()."""
        entry = {
            "id": str(uuid.uuid4()),
            "text": text,                  # short, quick win text
            "details": "",                 # longer reflection added later
            "mood": mood,
            "category": category,
            "date": dt.date.today().isoformat(),
            "timestamp": dt.datetime.now().strftime("%Y-%m-%d %H:%M"),
        }
        data = self._read()
        data["entries"].append(entry)
        self._write(data)
        return entry

    def update_details(self, entry_id, details):
        """Attach/replace a longer reflection on an existing win."""
        data = self._read()
        for e in data["entries"]:
            if e["id"] == entry_id:
                e["details"] = details
                break
        self._write(data)

    def list_entries_by_date(self, date):
        return [e for e in self._read()["entries"] if e["date"] == date]

    def list_entries_last_n_days(self, n=7):
        today = dt.date.today()
        window = {(today - dt.timedelta(days=i)).isoformat() for i in range(n)}
        return [e for e in self._read()["entries"] if e["date"] in window]

    def get_streak_days(self):
        """Consecutive days ending today that have at least one entry."""
        entries = self._read()["entries"]
        dates = {e["date"] for e in entries}
        streak, day = 0, dt.date.today()
        while day.isoformat() in dates:
            streak += 1
            day -= dt.timedelta(days=1)
        return streak

    def export_json(self):
        return self._read()
