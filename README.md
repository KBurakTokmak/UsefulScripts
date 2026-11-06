# UsefulScripts

A collection of small scripts for video clipping, screen automation, network utilities, ID validation, and Windows file management. Each tool is independent; see its section below for its purpose and dependencies.

## Contents

- [`clipper.py`](#clipperpy) — extract a clip from a video using FFmpeg
- [`ssh_finder.py`](#ssh_finderpy) — discover active hosts on a network and check SSH connectivity
- [`Click_on_template_image/`](#click_on_template_image) — find and click a matching screen image
- [`buff_checker/`](#buff_checker) — watch a screen region for a template and optionally press a key
- [`ID_check_full_stack/`](#id_check_full_stack) — Flask app for checking Turkish national ID numbers
- [`WinCmd/RemovePrefix.bat`](#wincmdremoveprefixbat) — remove a prefix from matching filenames

## Requirements

Requirements vary by script:

| Script or folder | Dependencies |
| --- | --- |
| `clipper.py` | FFmpeg and FFprobe available on `PATH` |
| `ssh_finder.py` | `python-nmap`, `paramiko`, and Nmap |
| `Click_on_template_image/` | `opencv-python`, `numpy`, `pyautogui`, `pillow` |
| `buff_checker/` | `opencv-python`, `numpy`, `pyautogui`, `pillow`, `keyboard` |
| `ID_check_full_stack/` | Flask and Flask-WTF |
| `WinCmd/RemovePrefix.bat` | Windows |

Install Python packages for the scripts you intend to use. For example:

```bash
pip install opencv-python numpy pyautogui pillow keyboard
pip install python-nmap paramiko
pip install flask flask-wtf
```

Install Nmap, FFmpeg, and FFprobe separately using the package manager or installer for your operating system.

## Tools

### `clipper.py`

Cuts a segment from a video file. Start and end times can be given in seconds or as `HH:MM:SS[.fraction]`. When the output is MP4, the script checks whether the streams need re-encoding for compatibility; you can also force transcoding or stream copying.

```bash
python clipper.py input.mp4 00:00:30 00:02:00
python clipper.py input.mp4 30 120 --output clip.mp4
python clipper.py input.mp4 30 120 --force-transcode
python clipper.py input.mp4 30 120 --copy
```

If no output filename is supplied, the script generates one based on the input filename and clip times.

### `ssh_finder.py`

Discovers active hosts in a specified network and checks whether SSH authentication succeeds using the username and password provided to the script. Use it only on networks and devices you own or are authorized to administer. Avoid putting real passwords in shell history or other logs.

### `Click_on_template_image/`

`click_it.py` repeatedly captures the screen and searches for `template.png`. When the match score exceeds its threshold, it clicks the detected location. The script expects the template image in its working directory and runs continuously until stopped.

### `buff_checker/`

`buff.py` checks a configured screen rectangle for `template.png`. Press **F6** to toggle detection. When the match score reaches the configured threshold, it presses **W**, subject to a cooldown. Edit the region, threshold, and timing settings in the script to suit your display.

Optional debug captures can be enabled in the script; they are saved under `buff_checker/debug_caps/`.

`mouse_location.py` prints the current mouse coordinates when **J** is pressed. Those coordinates can help configure the detector’s screen region.

### `ID_check_full_stack/`

A Flask web form that checks whether an entered value meets the Turkish national ID format and checksum rules. The folder includes a separate README with additional details.

Install Flask and Flask-WTF, then run the app from its directory:

```bash
cd ID_check_full_stack
python web_app.py
```

The app defines a `/valid_id` route. Its host address is configured in `web_app.py`; adjust that setting if needed for your environment. Do not expose this development app to an untrusted network.

### `WinCmd/RemovePrefix.bat`

Removes a specified prefix from filenames matching a supplied file mask. Run it from a Windows command prompt with the prefix and mask as arguments. Test it on copies of files first, since renaming is applied to matching files.

## Notes

- Screen automation scripts capture the display and send mouse or keyboard input. Review their settings and stop them when they are not needed.
- The scripts are standalone utilities and do not share a single dependency set or common launcher.
- No license file was found at the repository root. Check with the repository owner before redistributing or using the code in ways that require a license.
