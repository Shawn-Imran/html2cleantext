from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="html2cleantext",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="Convert HTML to clean, structured Markdown or plain text",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/html2cleantext",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Markup :: HTML",
        "Topic :: Text Processing :: Markup :: Markdown",
    ],
    python_requires=">=3.7",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "html2cleantext=html2cleantext.cli:main",
        ],
    },
    keywords="html markdown text cleaning boilerplate nlp",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/html2cleantext/issues",
        "Source": "https://github.com/yourusername/html2cleantext",
    },
)
