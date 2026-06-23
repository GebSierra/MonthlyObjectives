#!/usr/bin/env python3
"""Render index.html from objectives-history.json + template.html."""
import json, os, html
HERE = os.path.dirname(os.path.abspath(__file__))
data = json.load(open(os.path.join(HERE,"objectives-history.json"), encoding="utf-8"))
tpl  = open(os.path.join(HERE,"template.html"), encoding="utf-8").read()
out = tpl.replace("__TITLE__", html.escape(data.get("title","Monthly Objectives"))) \
         .replace("__DATA__", json.dumps(data, ensure_ascii=False))
open(os.path.join(HERE,"index.html"),"w",encoding="utf-8").write(out)
print("Wrote index.html (", len(out), "bytes )")
