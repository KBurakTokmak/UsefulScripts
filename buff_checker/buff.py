"""
Screen-spot template detector
─────────────────────────────
• Checks a fixed rectangle for `template.png`.
• Presses “W” at most once per second when a match ≥ THRESHOLD.
• Toggle ON / OFF with F6.
• Optional DEBUG mode: periodically saves the sampled region to disk.

Dependencies
------------
pip install opencv-python pillow pyautogui keyboard
"""

import time
import threading
from datetime import datetime
from pathlib import Path

import cv2
import numpy as np
import pyautogui
import keyboard

# ─── USER SETTINGS ────────────────────────────────────────────────────────────
REGION = (1464, 1012, 62, 62)          # (left, top, width, height)  <-- EDIT
TEMPLATE_PATH = Path(__file__).with_name("template.png")

THRESHOLD   = 0.75                     # 0–1, higher = stricter
CHECK_INTERVAL = 0.5                  # seconds between screen grabs
COOLDOWN       = 1.0                   # min seconds between “W” presses

# ── Debug capture ──
DEBUG        = False                    # ← turn screenshots on/off
DEBUG_EVERY  = 3.0                     # seconds between debug saves
DEBUG_DIR    = Path(__file__).with_name("debug_caps")
# ──────────────────────────────────────────────────────────────────────────────


def load_template():
    if not TEMPLATE_PATH.exists():
        raise FileNotFoundError(f"{TEMPLATE_PATH} not found")
    return cv2.imread(str(TEMPLATE_PATH), cv2.IMREAD_GRAYSCALE)


template_gray = load_template()
templ_h, templ_w = template_gray.shape[:2]

state = {
    "enabled": False,
    "last_press": 0.0,
    "last_debug": 0.0
}


def toggle():
    state["enabled"] = not state["enabled"]
    print(f"[INFO] Detector {'ENABLED' if state['enabled'] else 'DISABLED'}")


keyboard.add_hotkey("F6", toggle)


def save_debug_img(img_pil):
    """
    Save the PIL screenshot of REGION to DEBUG_DIR with a timestamped filename.
    """
    DEBUG_DIR.mkdir(exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")[:-3]
    out_path = DEBUG_DIR / f"cap_{ts}.png"
    img_pil.save(out_path)
    # print(f"[DEBUG] Saved {out_path}")


def detector_loop():
    while True:
        if state["enabled"]:
            shot = pyautogui.screenshot(region=REGION)
            shot_gray = cv2.cvtColor(np.array(shot), cv2.COLOR_RGB2GRAY)

            res = cv2.matchTemplate(shot_gray, template_gray, cv2.TM_CCOEFF_NORMED)
            _, max_val, _, _ = cv2.minMaxLoc(res)

            # Optional debug dump
            if DEBUG and (time.time() - state["last_debug"] >= DEBUG_EVERY):
                save_debug_img(shot)
                state["last_debug"] = time.time()

            # Press W if we have a match and cooldown elapsed
            if (
                max_val >= THRESHOLD
                and time.time() - state["last_press"] >= COOLDOWN
            ):
                keyboard.press_and_release("w")
                state["last_press"] = time.time()
                # print(f"Pressed W (match={max_val:.2f})")

        time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    print("Press F6 to toggle on/off.  Ctrl+C to quit.")
    if DEBUG:
        print(f"[DEBUG] Captures every {DEBUG_EVERY}s → {DEBUG_DIR}")

    t = threading.Thread(target=detector_loop, daemon=True)
    t.start()

    try:
        while True:
            time.sleep(1)           # keep main thread alive for hotkey
    except KeyboardInterrupt:
        print("\nExiting…")
