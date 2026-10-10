import re, sys
from pathlib import Path

A, B = "<!-- edumind-back -->", "<!-- /edumind-back -->"
PATTERNS = [
    re.compile(re.escape(A) + r".*?" + re.escape(B), re.S),   # नया बटन
    re.compile(r'\s*<a id="back-edumind".*?</script>', re.S),  # पुराना बटन
]
skip = {"node_modules", "venv", ".venv", "env", "__pycache__", ".git", "site-packages"}
root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")

for f in root.rglob("*.html"):
    if skip & set(f.parts):
        continue
    t = f.read_text(encoding="utf-8", errors="ignore")
    new = t
    for p in PATTERNS:
        new = p.sub("", new)
    if new != t:
        f.write_text(new, encoding="utf-8")
        print("Removed from:", f)