#!/usr/bin/env python3
import argparse
import subprocess
import shutil
import sys
import os
import re
import json

def run_ffprobe(file_path):
    cmd = [
        "ffprobe",
        "-v", "error",
        "-print_format", "json",
        "-show_streams",
        "-i", file_path
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"ffprobe failed: {result.stderr.strip()}")
    return json.loads(result.stdout)

def parse_time(t):
    """
    Parse a time string which can be:
      - seconds as integer or float: "90" or "90.5"
      - HH:MM:SS[.fraction]: "01:23:45", "00:01:15.5"
    Returns seconds as float.
    """
    if re.match(r'^\d+(\.\d+)?$', t):
        return float(t)
    parts = t.split(':')
    if len(parts) > 3 or len(parts) == 0:
        raise ValueError(f"Invalid time format: {t}")
    parts = [float(p) for p in parts]
    parts = [0.0] * (3 - len(parts)) + parts
    hours, minutes, seconds = parts
    return hours * 3600 + minutes * 60 + seconds

def format_time_for_filename(t):
    hrs = int(t // 3600)
    mins = int((t % 3600) // 60)
    secs = t % 60
    if abs(secs - int(secs)) < 1e-6:
        secs = int(secs)
        return f"{hrs:02d}-{mins:02d}-{secs:02d}"
    else:
        # include millisecond precision
        return f"{hrs:02d}-{mins:02d}-{secs:06.3f}".replace('.', '-')

def needs_transcode_to_mp4(ffinfo):
    """
    Return True if video is not h264 or audio is not aac.
    """
    has_video_h264 = False
    has_audio_aac = False
    for stream in ffinfo.get("streams", []):
        if stream.get("codec_type") == "video":
            if stream.get("codec_name") == "h264":
                has_video_h264 = True
        elif stream.get("codec_type") == "audio":
            if stream.get("codec_name") == "aac":
                has_audio_aac = True
    return not (has_video_h264 and has_audio_aac)

def cut_video(input_file, start_time, end_time, output_file=None, force_transcode=False, force_copy=False):
    if shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None:
        print("Error: ffmpeg and/or ffprobe not found in PATH. Install them first.", file=sys.stderr)
        sys.exit(1)

    start_sec = parse_time(start_time)
    end_sec = parse_time(end_time)
    if end_sec <= start_sec:
        raise ValueError(f"End time ({end_time}) must be after start time ({start_time})")
    duration = end_sec - start_sec

    if output_file is None:
        base, ext = os.path.splitext(os.path.basename(input_file))
        out_ext = ".mp4" if ext.lower() != ".mp4" else ext
        out_name = f"{base}_{format_time_for_filename(start_sec)}_to_{format_time_for_filename(end_sec)}{out_ext}"
        output_file = out_name

    # Determine whether to copy or transcode
    _, out_ext = os.path.splitext(output_file)
    transcode = False
    if force_transcode:
        transcode = True
    elif force_copy:
        transcode = False
    else:
        if out_ext.lower() == ".mp4":
            try:
                info = run_ffprobe(input_file)
                if needs_transcode_to_mp4(info):
                    transcode = True
                else:
                    transcode = False
            except Exception:
                # if probing fails, err on safe side: transcode
                transcode = True
        else:
            # for non-mp4 output, just copy if possible
            transcode = False

    if transcode:
        # re-encode to h264/aac for mp4 compatibility with faststart
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", input_file,
            "-t", str(duration),
            "-c:v", "libx264",
            "-preset", "veryfast",
            "-crf", "23",
            "-c:a", "aac",
            "-b:a", "128k",
            "-movflags", "+faststart",
            output_file
        ]
    else:
        # stream copy (fast) - may be incompatible if putting unsupported codecs into container
        cmd = [
            "ffmpeg",
            "-y",
            "-ss", str(start_time),
            "-i", input_file,
            "-t", str(duration),
            "-c", "copy",
            output_file
        ]

    try:
        subprocess.run(cmd, check=True)
        mode = "re-encoded" if transcode else "stream-copied"
        print(f"Clip saved as: {output_file} ({mode})")
    except subprocess.CalledProcessError as e:
        print("FFmpeg failed:", e, file=sys.stderr)
        sys.exit(e.returncode)

def main():
    parser = argparse.ArgumentParser(
        description="Fast clip extractor with intelligent mp4 compatibility handling."
    )
    parser.add_argument("input_video", help="Source video file")
    parser.add_argument("start", help="Start time (HH:MM:SS[.ms] or seconds)")
    parser.add_argument("end", help="End time (HH:MM:SS[.ms] or seconds)")
    parser.add_argument("-o", "--output", help="Output file name (optional). If omitted, auto-generated.")
    parser.add_argument("--force-transcode", action="store_true", help="Force re-encoding even if copy might work.")
    parser.add_argument("--copy", dest="force_copy", action="store_true", help="Force stream copy (no re-encode).")

    args = parser.parse_args()

    if not os.path.isfile(args.input_video):
        print(f"Error: input file '{args.input_video}' does not exist.", file=sys.stderr)
        sys.exit(1)

    try:
        cut_video(
            args.input_video,
            args.start,
            args.end,
            args.output,
            force_transcode=args.force_transcode,
            force_copy=args.force_copy
        )
    except ValueError as ve:
        print(f"Error: {ve}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
