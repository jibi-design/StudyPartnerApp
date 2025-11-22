# scripts/generate_sample.py
import sys, os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from ai_video_generator import generate_ai_video
from pathlib import Path

sample_asset = Path("/mnt/data/0018.jpg")
assets = [sample_asset] if sample_asset.exists() else None

mp4, audio = generate_ai_video("Alphabet A for kids — A for Apple", filename="alphabet_A_pro", duration=18, template="clean", assets=assets, voice="gtts")
print("Generated:", mp4, audio)
