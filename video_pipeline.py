# video_pipeline.py
"""
Professional template-driven video pipeline (Option D).
- Uses moviepy + imageio-ffmpeg (bundled ffmpeg) so system ffmpeg is NOT required.
- Uses uploaded background images at /mnt/data/0018.jpg and /mnt/data/0019.jpg as template backgrounds.
- Produces MP4 (clean, modern) and an MP3 narration file.
"""

from pathlib import Path
import shutil
import tempfile
import textwrap
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# MoviePy imports
from moviepy.editor import ImageClip, AudioFileClip, concatenate_videoclips, CompositeVideoClip, vfx
from moviepy.config import change_settings
import imageio_ffmpeg

# Point moviepy to the imageio-ffmpeg binary (ensures no system ffmpeg required)
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
change_settings({"FFMPEG_BINARY": ffmpeg_exe})

# Optional TTS: gTTS
try:
    from gtts import gTTS
    GTTs_AVAILABLE = True
except Exception:
    GTTs_AVAILABLE = False

# Windows SAPI fallback
try:
    import win32com.client
    SAPI_AVAILABLE = True
except Exception:
    SAPI_AVAILABLE = False

# Paths
ROOT = Path(__file__).resolve().parent
VIDEO_DIR = ROOT / "videos"
ASSETS_DIR = ROOT / "assets"
TEMPLATES_DIR = ASSETS_DIR / "templates"
VIDEO_DIR.mkdir(exist_ok=True)
ASSETS_DIR.mkdir(exist_ok=True)
TEMPLATES_DIR.mkdir(exist_ok=True)

# Use uploaded images as defaults
UPLOADED_BG_1 = Path("/mnt/data/0018.jpg")
UPLOADED_BG_2 = Path("/mnt/data/0019.jpg")

# Visual defaults
W, H = 1280, 720
FPS = 24
DEFAULT_FONT = None
if Path("C:/Windows/Fonts/arial.ttf").exists():
    DEFAULT_FONT = str(Path("C:/Windows/Fonts/arial.ttf"))

def _load_font(size=48):
    try:
        if DEFAULT_FONT:
            return ImageFont.truetype(DEFAULT_FONT, size)
    except Exception:
        pass
    return ImageFont.load_default()

def _wrap_text(text, width_chars=36):
    return textwrap.fill(text, width=width_chars)

def _render_slide_using_background(bg_path: Path | None, text: str, out_path: Path, template_style: str = "clean", logo: Path | None = None):
    """
    Render a slide PNG using either a provided background image or a template color.
    """
    # Create base canvas
    if bg_path and bg_path.exists():
        try:
            base = Image.open(str(bg_path)).convert("RGB").resize((W, H))
        except Exception:
            base = Image.new("RGB", (W, H), color=(250,252,255))
    else:
        # fallback template colors by style
        if template_style == "dark":
            base = Image.new("RGB", (W, H), color=(12,14,20))
        elif template_style == "kids":
            base = Image.new("RGB", (W, H), color=(255,245,230))
        elif template_style == "gradient":
            base = Image.new("RGB", (W, H), color=(245,240,255))
        else:
            base = Image.new("RGB", (W, H), color=(250,252,255))

    draw = ImageDraw.Draw(base)
    body_font = _load_font(44)
    title_font = _load_font(56)

    # Title (small top-left)
    # we won't force a big title; keep text centered
    wrapped = _wrap_text(text, width_chars=32)
    lines = wrapped.split("\n")

    # compute height
    total_h = 0
    line_heights = []
    for line in lines:
        bbox = draw.textbbox((0,0), line, font=body_font)
        lh = bbox[3] - bbox[1]
        line_heights.append(lh)
        total_h += lh + 8

    current_y = (H - total_h) // 2
    text_color = (18,30,50) if template_style != "dark" else (230,230,240)
    for i, line in enumerate(lines):
        bbox = draw.textbbox((0,0), line, font=body_font)
        w_line = bbox[2] - bbox[0]
        draw.text(((W - w_line) // 2, current_y), line, font=body_font, fill=text_color)
        current_y += line_heights[i] + 8

    # optional logo overlay (top-right)
    if logo and Path(logo).exists():
        try:
            logo_img = Image.open(str(logo)).convert("RGBA")
            logo_w = 140
            logo_h = int(logo_img.size[1] * (logo_w / logo_img.size[0]))
            logo_img = logo_img.resize((logo_w, logo_h))
            base.paste(logo_img, (W - logo_w - 30, 30), mask=logo_img)
        except Exception:
            pass

    base.save(out_path)
    return out_path

def _tts_gtts(text: str, out_mp3: Path, lang: str = "en"):
    tts = gTTS(text=text, lang=lang)
    tmp = out_mp3.with_suffix(".tmp.mp3")
    tts.save(str(tmp))
    tmp.replace(out_mp3)
    return out_mp3

def _tts_sapi(text: str, out_wav: Path):
    import win32com.client
    speaker = win32com.client.Dispatch("SAPI.SpVoice")
    stream = win32com.client.Dispatch("SAPI.SpFileStream")
    from comtypes.gen import SpeechLib
    stream.Open(str(out_wav), SpeechLib.SSFMCreateForWrite)
    speaker.AudioOutputStream = stream
    speaker.Speak(text)
    stream.Close()
    return out_wav

def build_video_professional(prompt: str,
                             out_filename: str | None = None,
                             duration_seconds: int = 20,
                             lesson_title: str | None = None,
                             template: str = "clean",
                             logo: Path | None = None,
                             assets: list[Path] | None = None,
                             voice: str = "gtts"):
    """
    Build professional MP4 and narration MP3 and return (mp4_path, audio_path_or_None).
    Uses uploaded backgrounds by default (/mnt/data/0018.jpg).
    """
    tmp = Path(tempfile.mkdtemp(prefix="spvid_"))
    try:
        slides_dir = tmp / "slides"
        slides_dir.mkdir(parents=True, exist_ok=True)

        # choose background image (use uploaded bg by default)
        bg_choice = UPLOADED_BG_1 if UPLOADED_BG_1.exists() else None

        # slides array
        slide_paths = []

        # Title slide
        title_text = (lesson_title or prompt)
        p0 = slides_dir / "slide_0.png"
        _render_slide_using_background(bg_choice, title_text, p0, template_style=template, logo=logo)
        slide_paths.append(p0)

        # Main content slide
        p1 = slides_dir / "slide_1.png"
        _render_slide_using_background(bg_choice, prompt, p1, template_style=template, logo=logo)
        slide_paths.append(p1)

        # assets (if any)
        if assets:
            for i, a in enumerate(assets[:4]):
                try:
                    dest = slides_dir / f"asset_{i}.png"
                    Image.open(str(a)).convert("RGB").resize((W, H)).save(dest)
                    slide_paths.append(dest)
                except Exception:
                    pass

        # practice + end slides
        practice = slides_dir / "slide_practice.png"
        _render_slide_using_background(bg_choice, "Practice: say 'apple', 'dog', 'book'", practice, template_style=template, logo=logo)
        slide_paths.append(practice)

        end = slides_dir / "slide_end.png"
        _render_slide_using_background(bg_choice, "Great job — see you next time!", end, template_style=template, logo=logo)
        slide_paths.append(end)

        # per-slide duration
        per_slide = max(2, duration_seconds // max(1, len(slide_paths)))

        # create moviepy clips with subtle zoom
        clips = []
        for p in slide_paths:
            clip = ImageClip(str(p)).set_duration(per_slide)
            # apply a small zoom (ken-burns) across the duration
            # moviepy: resize with lambda expects factor function; fallback to vfx.resize if unavailable
            try:
                clip = clip.fx(vfx.resize, lambda t: 1 + 0.02 * (t / per_slide))
            except Exception:
                clip = clip.resize((W, H))
            clips.append(clip)

        final_clip = concatenate_videoclips(clips, method="compose")

        # narration
        narration_path = None
        if voice == "gtts" and GTTs_AVAILABLE:
            narration_path = VIDEO_DIR / ((out_filename or prompt.replace(" ", "_"))[:80] + ".mp3")
            _tts_gtts(f"Hello. I am Lumi. Today we learn: {prompt}.", narration_path)
            audio_clip = AudioFileClip(str(narration_path))
            final_clip = final_clip.set_audio(audio_clip)
        elif voice == "sapi" and SAPI_AVAILABLE:
            wavp = tmp / "narration.wav"
            _tts_sapi(f"Hello. I am Lumi. Today we learn: {prompt}.", wavp)
            narration_path = VIDEO_DIR / ((out_filename or prompt.replace(" ", "_"))[:80] + ".wav")
            shutil.copy2(wavp, narration_path)
            audio_clip = AudioFileClip(str(narration_path))
            final_clip = final_clip.set_audio(audio_clip)
        else:
            narration_path = None

        # finalize file name
        if out_filename:
            out_name = out_filename if out_filename.lower().endswith(".mp4") else out_filename + ".mp4"
        else:
            out_name = prompt.lower().strip().replace(" ", "_")[:80] + ".mp4"
        out_path = VIDEO_DIR / out_name

        # export mp4 (MoviePy uses imageio-ffmpeg binary set above)
        final_clip.write_videofile(str(out_path), fps=FPS, codec="libx264", audio_codec="aac", preset="medium")
        final_clip.close()
        return out_path, narration_path

    finally:
        try:
            shutil.rmtree(tmp, ignore_errors=True)
        except Exception:
            pass
