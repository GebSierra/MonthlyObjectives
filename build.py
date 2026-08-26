#!/usr/bin/env python3
"""Refresh builder. Mirrors the TickTick board into the ACTIVE month only.

The active month is set by "activeMonth" in objectives-history.json. This task
never changes it; month rollover is a deliberate, separate step. That way a new
month is never created (and the prior month never frozen) until you confirm the
new month's objectives are in place.

Inputs (same folder):  current_board.json (raw TickTick JSON), objectives-history.json, template.html
Outputs:               objectives-history.json (active month merged), index.html
"""
import json, os, html, re, datetime, sys
HERE = os.path.dirname(os.path.abspath(__file__))
def p(n): return os.path.join(HERE,n)

def find_board(o):
    if isinstance(o,dict):
        if "tasks" in o and "columns" in o: return o
        for v in o.values():
            r=find_board(v)
            if r: return r
    if isinstance(o,list):
        for v in o:
            r=find_board(v)
            if r: return r
    return None
def status_of(name):
    n=(name or "").lower()
    if "not started" in n: return "notStarted"
    if "progress" in n:    return "inProgress"
    if "done" in n:        return "done"
    if "quarter" in n:     return "quarterly"
    return None
def clean(t):
    return re.sub(r"\s+"," ", re.sub(r"[⭐★]","", t or "")).strip()
QG_RE = re.compile(r"^\s*\[?QG\s*0*([0-9]+)\]?\s*[:\-–—]?\s*", re.IGNORECASE)
def extract_qg(title):
    m = QG_RE.match(title)
    if not m: return None, title
    return "QG"+m.group(1), QG_RE.sub("", title, count=1).strip()

raw=json.load(open(p("current_board.json"),encoding="utf-8"))
board=find_board(raw)
if not board: print("ERROR: no tasks/columns in current_board.json"); sys.exit(1)
col={c["id"]:status_of(c["name"]) for c in board["columns"]}
proj_id=(board.get("project") or {}).get("id","")
items,seen=[],set()
for t in board["tasks"]:
    st=col.get(t.get("columnId"))
    if not st: continue
    title=clean(t.get("title",""))
    if not title: continue
    top=("⭐" in (t.get("title") or "")) or ("★" in (t.get("title") or "")) or (t.get("priority")==5)
    qg,title=extract_qg(title)
    k=(title.lower(),st)
    if k in seen: continue
    seen.add(k)
    item={"title":title,"status":st,"top":bool(top)}
    if qg: item["qg"]=qg
    if st=="quarterly" and proj_id and t.get("id"):
        item["url"]=f"https://ticktick.com/webapp/#p/{proj_id}/kanban/{t['id']}"
    items.append(item)

data=json.load(open(p("objectives-history.json"),encoding="utf-8")) if os.path.exists(p("objectives-history.json")) else {"title":"Monthly Objectives","subtitle":"","months":[]}
today=datetime.date.today()
active=data.get("activeMonth") or today.strftime("%Y-%m")
data["activeMonth"]=active
label=datetime.datetime.strptime(active+"-01","%Y-%m-%d").strftime("%B %Y")
data["lastUpdated"]=today.strftime("%Y-%m-%d")
months={m["key"]:m for m in data.get("months",[])}
prev=months.get(active,{})
entry={"key":active,"label":label,"items":items}
if prev.get("people"): entry["people"]=prev["people"]  # preserve curated People list across objective refreshes
if data.get("quarterEndDate"): entry["quarterEndDate"]=data["quarterEndDate"]  # stamp current quarter end date onto this month's snapshot
if data.get("quarterStartDate"): entry["quarterStartDate"]=data["quarterStartDate"]
months[active]=entry
data["months"]=[months[k] for k in sorted(months)]
json.dump(data,open(p("objectives-history.json"),"w",encoding="utf-8"),ensure_ascii=False,indent=2)

tpl=open(p("template.html"),encoding="utf-8").read()
out=tpl.replace("__TITLE__",html.escape(data.get("title","Monthly Objectives"))).replace("__DATA__",json.dumps(data,ensure_ascii=False))
open(p("index.html"),"w",encoding="utf-8").write(out)
print(f"OK {label}: " + ", ".join(f"{s}={sum(1 for i in items if i['status']==s)}" for s in ["notStarted","inProgress","done","quarterly"]) + f"; months={len(data['months'])}")
