#!/usr/bin/env python3
"""Self-contained dashboard builder for the scheduled refresh.

Inputs (same folder):
  current_board.json   -- raw TickTick project JSON (has 'tasks' and 'columns')
  objectives-history.json (optional) -- prior months; created if missing
Outputs (same folder):
  objectives-history.json  (updated, current month merged in)
  index.html               (regenerated, GitHub-Pages ready)
"""
import json, os, html, re, datetime, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOARD = os.path.join(HERE, "current_board.json")
HIST  = os.path.join(HERE, "objectives-history.json")
OUT   = os.path.join(HERE, "index.html")

DEFAULTS = {
    "title": "Monthly Objectives",
    "subtitle": "Trinity Bible Church · Prepared for the Elders & Gary DeBock",
}

def find_board(obj):
    """Return dict with 'tasks' and 'columns' no matter how the MCP wrapped it."""
    if isinstance(obj, dict):
        if "tasks" in obj and "columns" in obj:
            return obj
        for v in obj.values():
            r = find_board(v)
            if r: return r
    if isinstance(obj, list):
        for v in obj:
            r = find_board(v)
            if r: return r
    return None

def status_of(name):
    n = (name or "").lower()
    if "not started" in n: return "notStarted"
    if "progress" in n:    return "inProgress"
    if "done" in n:        return "done"
    if "quarter" in n:     return "quarterly"
    return None

def clean(title):
    t = re.sub(r"[⭐★]", "", title or "")
    return re.sub(r"\s+", " ", t).strip()

# ---- read board ----
with open(BOARD, encoding="utf-8") as f:
    raw = json.load(f)
board = find_board(raw)
if not board:
    print("ERROR: could not find tasks/columns in current_board.json"); sys.exit(1)

col_status = {c["id"]: status_of(c["name"]) for c in board["columns"]}

items, seen = [], set()
for t in board["tasks"]:
    st = col_status.get(t.get("columnId"))
    if not st:
        continue
    title = clean(t.get("title", ""))
    if not title:
        continue
    top = ("⭐" in (t.get("title") or "")) or ("★" in (t.get("title") or "")) or (t.get("priority") == 5)
    key = (title.lower(), st)
    if key in seen:
        continue
    seen.add(key)
    items.append({"title": title, "status": st, "top": bool(top)})

# ---- month label ----
today = datetime.date.today()
mkey = today.strftime("%Y-%m")
mlabel = today.strftime("%B %Y")

# ---- merge history ----
if os.path.exists(HIST):
    with open(HIST, encoding="utf-8") as f:
        data = json.load(f)
else:
    data = dict(DEFAULTS); data["months"] = []
data.setdefault("title", DEFAULTS["title"])
data.setdefault("subtitle", DEFAULTS["subtitle"])
data["lastUpdated"] = today.strftime("%Y-%m-%d")
data.setdefault("months", [])
months = {m["key"]: m for m in data["months"]}
months[mkey] = {"key": mkey, "label": mlabel, "items": items}
data["months"] = [months[k] for k in sorted(months)]

with open(HIST, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# ---- render (template lives in template.html beside this script) ----
tpl_path = os.path.join(HERE, "template.html")
with open(tpl_path, encoding="utf-8") as f:
    TEMPLATE = f.read()
out = TEMPLATE.replace("__TITLE__", html.escape(data["title"])).replace("__DATA__", json.dumps(data, ensure_ascii=False))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)
print(f"OK: {mlabel}: {len(items)} items; {len(data['months'])} month(s) in history")
