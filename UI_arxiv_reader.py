import json
import subprocess
from datetime import datetime
from pathlib import Path
import io
import zipfile
import time

import pandas as pd
import streamlit as st
import requests


APP_DIR = Path(__file__).resolve().parent
RUNS_DIR = (APP_DIR / "runs").resolve()
RUNS_DIR.mkdir(exist_ok=True)

TOPICS = {
    "Mathematics": {
        "Differential Geometry (math.DG)": ["riemannian", "curvature", "geodesic", "ricci", "soliton"],
        "Algebraic Geometry (math.AG)": ["scheme", "variety", "moduli", "stack"],
        "Geometric Topology (math.GT)": ["3-manifold", "knot", "hyperbolic"],
        "Analysis of PDEs (math.AP)": ["pde", "elliptic", "parabolic"],
        "Functional Analysis (math.FA)": ["banach", "hilbert", "operator"],
        "Number Theory (math.NT)": ["prime", "l-function", "modular"],
        "General Mathematics (math)": [],
    },
    "Physics": {
        "General Relativity & Cosmology (gr-qc)": ["spacetime", "einstein", "black hole", "cosmology"],
        "Mathematical Physics (math-ph)": ["field theory", "quantization", "operator"],
        "Quantum Physics (quant-ph)": ["quantum", "entanglement"],
        "High Energy Physics (hep-th)": ["string", "ads/cft"],
        "Condensed Matter (cond-mat)": ["topological", "phase transition"],
    },
    "Computer Science": {
        "Machine Learning (cs.LG)": ["learning", "neural", "optimization"],
        "Artificial Intelligence (cs.AI)": ["planning", "reasoning", "agent"],
        "Theory of Computation (cs.CC)": ["complexity", "np-hard"],
        "Computer Vision (cs.CV)": ["image", "vision"],
        "Cryptography (cs.CR)": ["cryptography", "security"],
    },
}


def list_snapshots():
    return sorted(RUNS_DIR.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)


def latest_snapshot():
    snaps = list_snapshots()
    return snaps[0] if snaps else None


def score_row(title: str, summary: str, kws: list[str]) -> int:
    if not kws:
        return 1
    text = (title + " " + summary).lower()
    return sum(text.count(k.lower()) for k in kws)


def run_spider_to_snapshot(query: str, start_date: str, end_date: str, max_items: int, page_size: int) -> Path:
    ts = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    safe = "".join(c if c.isalnum() else "_" for c in query)[:80]
    out = (RUNS_DIR / f"{ts}__{safe}.json").resolve()

    cmd = [
        "python", "-m", "scrapy", "crawl", "arxiv",
        "-a", f"query={query}",
        "-a", f"start_date={start_date}",
        "-a", f"end_date={end_date}",
        "-a", f"max_items={max_items}",
        "-a", f"page_size={page_size}",
        "-O", str(out),
    ]

    scrapy_project_dir = (APP_DIR / "arxiv_scraper").resolve()

    p = subprocess.run(
        cmd,
        cwd=str(scrapy_project_dir),
        capture_output=True,
        text=True,
        shell=False,
    )

    if p.returncode != 0:
        msg = (p.stderr or p.stdout or "Spider failed.").strip()
        raise RuntimeError(msg[-2500:])

    if not out.exists():
        raise FileNotFoundError(f"Spider reported success but snapshot not found: {out}")

    return out


def normalize_snapshot_to_df(papers: list[dict]) -> pd.DataFrame:
    rows = []
    for p in papers:
        rows.append({
            "select": False,
            "published": (p.get("published") or "")[:10],
            "title": (p.get("title") or "").replace("\n", " ").strip(),
            "authors": ", ".join(p.get("authors", [])) if isinstance(p.get("authors"), list) else str(p.get("authors", "")),
            "summary": (p.get("summary") or "").strip(),
            "url": (p.get("id") or "").replace("http://", "https://"),
        })
    return pd.DataFrame(rows)


def abs_to_pdf_url(abs_url: str) -> str:
    u = (abs_url or "").strip()
    u = u.replace("http://", "https://")
    if "/abs/" in u:
        u = u.replace("/abs/", "/pdf/")
    if not u.endswith(".pdf"):
        u = u + ".pdf"
    return u


def make_pdf_zip(selected_df: pd.DataFrame) -> bytes:
    mem = io.BytesIO()
    zf = zipfile.ZipFile(mem, mode="w", compression=zipfile.ZIP_DEFLATED)

    headers = {
        "User-Agent": "arXiv-Reader (academic use; local app)",
        "Accept": "application/pdf",
    }

    urls = selected_df["url"].tolist()
    total = len(urls)

    progress = st.progress(0)
    status = st.empty()

    for i, abs_url in enumerate(urls, start=1):
        pdf_url = abs_to_pdf_url(abs_url)
        status.write(f"Downloading {i}/{total}: {pdf_url}")

        try:
            r = requests.get(pdf_url, headers=headers, timeout=30)
            if r.status_code == 200 and (r.headers.get("Content-Type", "").startswith("application/pdf") or r.content[:4] == b"%PDF"):
                filename = pdf_url.split("/")[-1]
                zf.writestr(filename, r.content)
            else:
                zf.writestr(f"FAILED_{i}.txt", f"Failed: {pdf_url}\nStatus: {r.status_code}\nContent-Type: {r.headers.get('Content-Type')}\n")
        except Exception as e:
            zf.writestr(f"ERROR_{i}.txt", f"Error downloading: {pdf_url}\n{repr(e)}\n")

        progress.progress(int(i / total * 100))
        time.sleep(0.2)  # be polite

    zf.close()
    mem.seek(0)
    status.write("Done.")
    return mem.read()


# -----------------------------
# Streamlit config + style
# -----------------------------
st.set_page_config(page_title="arXiv Reader", layout="wide")
st.markdown(
    """
    <style>
      header[data-testid="stHeader"] { background: rgba(0,0,0,0) !important; }
      div[data-testid="stToolbar"] { background: rgba(0,0,0,0) !important; }
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("arXiv Reader (local app)")


# -----------------------------
# Session state
# -----------------------------
if "snapshot_path" not in st.session_state:
    st.session_state.snapshot_path = None
if "uploaded_bytes" not in st.session_state:
    st.session_state.uploaded_bytes = None
if "uploaded_name" not in st.session_state:
    st.session_state.uploaded_name = None
if "uploaded_papers" not in st.session_state:
    st.session_state.uploaded_papers = None

if "domain" not in st.session_state:
    st.session_state.domain = "Mathematics"
if "topic" not in st.session_state:
    st.session_state.topic = "Differential Geometry (math.DG)"
if "select_all_flag" not in st.session_state:
    st.session_state.select_all_flag = False


# =========================================================
# Layout: left panel (crawler) wider
# =========================================================
left, right = st.columns([1.2, 1.8], gap="large")

with left:
    st.subheader("Run crawler")

    domains = list(TOPICS.keys())
    st.session_state.domain = st.selectbox("Domain", domains, index=domains.index(st.session_state.domain))

    topics = list(TOPICS[st.session_state.domain].keys())
    if st.session_state.topic not in TOPICS[st.session_state.domain]:
        st.session_state.topic = topics[0]
    st.session_state.topic = st.selectbox("Topic", topics, index=topics.index(st.session_state.topic))

    default_kws = TOPICS[st.session_state.domain][st.session_state.topic]
    cat = st.session_state.topic.split("(")[-1].split(")")[0].strip()
    default_query = f"cat:{cat}"

    query = st.text_input("arXiv query (edit freely)", value=default_query)
    start_date = st.text_input("Start date (YYYY-MM-DD)", value="2025-01-01")
    end_date = st.text_input("End date (YYYY-MM-DD)", value="2025-12-31")

    max_items = st.slider("Max papers to save", 1, 200, 35)
    page_size = st.selectbox("Page size", [25, 50, 100], index=2)

    b1, b2 = st.columns(2)
    with b1:
        run_clicked = st.button("Run spider", use_container_width=True)
    with b2:
        use_latest = st.button("Use latest snapshot", use_container_width=True)

    st.divider()
    st.subheader("Open snapshot")

    up = st.file_uploader("Choose snapshot (.json)", type=["json"])
    load_up = st.button("Load uploaded snapshot", use_container_width=True, disabled=(up is None))

    if up is not None:
        st.session_state.uploaded_bytes = up.getvalue()
        st.session_state.uploaded_name = up.name

    if load_up:
        st.session_state.uploaded_papers = json.loads(st.session_state.uploaded_bytes.decode("utf-8"))
        st.session_state.snapshot_path = "uploaded"
        st.success(f"Loaded: {st.session_state.uploaded_name}")
        st.rerun()

    if run_clicked:
        try:
            with st.spinner("Running spider..."):
                out = run_spider_to_snapshot(query, start_date, end_date, max_items, page_size)
            st.session_state.snapshot_path = out
            st.session_state.uploaded_papers = None
            st.success(f"Saved: {out.name}")
            st.rerun()
        except Exception as e:
            st.error(str(e))

    if use_latest:
        lp = latest_snapshot()
        if lp:
            st.session_state.snapshot_path = lp
            st.session_state.uploaded_papers = None
            st.success(f"Using latest: {lp.name}")
            st.rerun()
        else:
            st.warning("No snapshots found in runs/")

with right:
    st.subheader("Results")

    papers = None
    if isinstance(st.session_state.snapshot_path, Path):
        papers = json.load(st.session_state.snapshot_path.open("r", encoding="utf-8"))
        st.caption(f"Using snapshot: {st.session_state.snapshot_path.name}")
    elif st.session_state.snapshot_path == "uploaded":
        papers = st.session_state.uploaded_papers
        st.caption("Using snapshot: uploaded")
    else:
        st.info("Run spider or load a snapshot to begin.")
        st.stop()

    if not papers:
        st.warning("Snapshot contains 0 papers.")
        st.stop()

    df = normalize_snapshot_to_df(papers)

    kws_text = st.text_area(
        "Keywords for ranking (one per line). Leave empty to show everything.",
        value="\n".join(default_kws),
    )
    kws = [k.strip() for k in kws_text.splitlines() if k.strip()]

    df["score"] = df.apply(lambda r: score_row(r["title"], r["summary"], kws), axis=1)
    min_score = st.slider("Minimum score", 0, 30, 0)
    df = df[df["score"] >= min_score].sort_values(["score", "published"], ascending=False)

    topbar = st.columns([1.2, 2.0, 6])
    with topbar[0]:
        st.session_state.select_all_flag = st.checkbox("Select all", value=st.session_state.select_all_flag)
    with topbar[1]:
        st.caption(f"Showing {len(df)} papers")
    with topbar[2]:
        pass

    df["select"] = bool(st.session_state.select_all_flag)

    edited = st.data_editor(
        df,
        use_container_width=True,
        height=520,
        column_config={
            "select": st.column_config.CheckboxColumn("Select"),
            "url": st.column_config.LinkColumn("arXiv"),
        },
        disabled=["published", "score", "title", "authors", "summary", "url"],
    )

    selected = edited[edited["select"] == True]

    st.divider()
    st.subheader("Downloads")

    d1, d2, d3, d4 = st.columns([1, 1, 1, 1])
    out_records = selected.drop(columns=["select"]).to_dict("records") if not selected.empty else []

    with d1:
        st.download_button(
            "JSON",
            json.dumps(out_records, indent=2, ensure_ascii=False),
            "reading_list.json",
            disabled=selected.empty,
        )
    with d2:
        st.download_button(
            "CSV",
            pd.DataFrame(out_records).to_csv(index=False),
            "reading_list.csv",
            disabled=selected.empty,
        )
    with d3:
        md = "\n\n".join(f"- **{r['title']}**  \n  {r['url']}" for r in out_records)
        st.download_button(
            "Markdown",
            md,
            "reading_list.md",
            disabled=selected.empty,
        )

    with d4:
        if selected.empty:
            st.button("PDFs (ZIP)", use_container_width=True, disabled=True)
        else:
            if st.button("Build PDFs ZIP", use_container_width=True):
                with st.spinner("Downloading PDFs and building ZIP..."):
                    zip_bytes = make_pdf_zip(selected)
                st.download_button(
                    "Download PDFs.zip",
                    zip_bytes,
                    "pdfs.zip",
                    mime="application/zip",
                    use_container_width=True,
                )
