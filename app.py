import subprocess
import time
import webview
import sys
import socket
from pathlib import Path


def wait_for_server(host="127.0.0.1", port=8501, timeout=30):
    start = time.time()
    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except OSError:
            time.sleep(0.5)
    return False


def main():
    base_dir = Path(sys.executable).parent if getattr(sys, "frozen", False) else Path(__file__).parent
    ui_file = base_dir / "ui_arxiv_reader.py"

    # Start Streamlit
    p = subprocess.Popen(
        [
            sys.executable,
            "-m",
            "streamlit",
            "run",
            str(ui_file),
            "--server.headless=true",
            "--server.port=8501",
            "--browser.gatherUsageStats=false",
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        cwd=str(base_dir),
    )

    # Wait until Streamlit is actually listening
    if not wait_for_server(port=8501, timeout=40):
        p.terminate()
        raise RuntimeError("Streamlit server did not start in time.")

    try:
        webview.create_window(
            "arXiv Reader",
            "http://127.0.0.1:8501",
            width=1280,
            height=860,
        )
        webview.start()
    finally:
        p.terminate()


if __name__ == "__main__":
    main()
