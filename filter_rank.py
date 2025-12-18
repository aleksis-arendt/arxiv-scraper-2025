import json
import re
from pathlib import Path
from datetime import datetime

IN = Path("dg_all.json")
OUT_DIR = Path("out")
OUT_DIR.mkdir(exist_ok=True)

with IN.open("r", encoding="utf-8") as f:
    papers = json.load(f)

TOPICS = {
    "riemannian": [r"\briemann", r"\bsectional curvature\b", r"\bscalar curvature\b", r"\bricci\b"],
    "ricci_flow": [r"\bricci flow\b", r"\bmean curvature flow\b", r"\bperelman\b", r"\bentropy\b"],
    "lorentzian": [r"\blorentz", r"\bspacetime\b", r"\bcausal", r"\bglobally hyperbolic\b", r"\beinstein\b"],
    "minimal_surfaces": [r"\bminimal surface", r"\bmean curvature\b", r"\bwillmore\b", r"\bconstant mean curvature\b"],
    "geometric_analysis": [r"\bpde\b", r"\bsobolev\b", r"\bheat kernel\b", r"\bgromov\b"],
}

def score_paper(p, patterns):
    text = (p.get("title","") + " " + p.get("summary","")).lower()
    s = 0
    for pat in patterns:
        s += len(re.findall(pat, text))
    return s

def parse_date(p):
    # published like "2025-12-01T..."
    return p.get("published","")[:10]

ranked_all = []

for topic, pats in TOPICS.items():
    bucket = []
    for p in papers:
        s = score_paper(p, pats)
        if s > 0:
            pp = dict(p)
            pp["topic"] = topic
            pp["score"] = s
            bucket.append(pp)
    bucket.sort(key=lambda x: (x["score"], parse_date(x)), reverse=True)
    (OUT_DIR / f"{topic}.json").write_text(json.dumps(bucket, indent=2, ensure_ascii=False), encoding="utf-8")
    ranked_all.extend(bucket)

ranked_all.sort(key=lambda x: (x["score"], parse_date(x)), reverse=True)
(OUT_DIR / "all_ranked.json").write_text(json.dumps(ranked_all, indent=2, ensure_ascii=False), encoding="utf-8")

print("Total papers:", len(papers))
for t in TOPICS:
    cnt = len(json.loads((OUT_DIR / f"{t}.json").read_text(encoding="utf-8")))
    print(f"{t}: {cnt}")
print("Wrote: out/*.json")
def md_line(p):
    url = p["id"]
    title = p["title"].strip()
    date = p["published"][:10]
    authors = ", ".join(p["authors"][:3]) + (" et al." if len(p["authors"]) > 3 else "")
    return f"- [{title}]({url})  \n  {authors}  \n  Published: {date}  \n  Score: {p['score']}  \n"

topN = 50
md = ["# DG Reading List (top 50)\n"]
for p in ranked_all[:topN]:
    md.append(md_line(p))

(OUT_DIR / "reading_list.md").write_text("\n".join(md), encoding="utf-8")
print("Wrote: out/reading_list.md")
