"""Setup configuration for OxFlow package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="oxflow",
    version="2.1.0",
    author="rejre",
    description="OxFlow (变色牛) - 极简现代风万能下载工具",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rejre/OxFlow",
    project_urls={
        "Bug Tracker": "https://github.com/rejre/OxFlow/issues",
        "Documentation": "https://github.com/rejre/OxFlow#readme",
        "Source Code": "https://github.com/rejre/OxFlow",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Multimedia :: Video",
        "Topic :: Internet",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: MacOS",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.10",
    install_requires=[
        "customtkinter>=5.2.0,<6.0.0",
        "yt-dlp>=2024.3.0,<2025.0.0",
        "psutil>=5.9.0,<6.0.0",
        "requests>=2.31.0,<3.0.0",
        "Pillow>=10.0.0,<11.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0,<8.0.0",
            "pytest-cov>=4.1.0,<5.0.0",
            "black>=23.7.0,<24.0.0",
            "flake8>=6.0.0,<7.0.0",
            "isort>=5.12.0,<6.0.0",
            "mypy>=1.5.0,<2.0.0",
            "pre-commit>=3.3.0,<4.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "oxflow=ui.main_window:main",
        ],
    },
)
