# ai_video_generator.py
from pathlib import Path
from video_pipeline import build_video_professional

OUT_DIR = Path("videos")
OUT_DIR.mkdir(exist_ok=True)

def generate_ai_video(prompt: str, filename: str = None, duration: int = 20, template: str = "clean", assets: list[Path] | None = None, voice: str = "gtts"):
    """
    Returns: (mp4_path: Path, audio_path: Path|None)
    """
    mp4_path, audio_path = build_video_professional(
        prompt=prompt,
        out_filename=filename,
        duration_seconds=duration,
        lesson_title=prompt,
        template=template,
        logo=None,
        assets=assets,
        voice=voice
    )
    return mp4_path, audio_path
