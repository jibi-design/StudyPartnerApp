import os

# Define your folder structure
folders = [
    "app",
    "app/audio",
    "app/video",
    "app/utils",
    "app/models",
    "tests",
    "scripts"
]

# Files to create
files = {
    "app/__init__.py": "",
    "main.py": "# Entry point of your StudyPartnerApp\nprint('App started successfully!')\n",
    "requirements.txt": "",
    ".gitignore": """venv/
__pycache__/
.env
*.pyc
*.pyo
*.pyd
.env/
.ffmpeg/
"""
}

# Create folders
for folder in folders:
    os.makedirs(folder, exist_ok=True)
    print(f"Created folder: {folder}")

# Create files
for file_path, content in files.items():
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Created file: {file_path}")

print("\nAll folder structure created successfully!")
