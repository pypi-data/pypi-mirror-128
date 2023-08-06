import pathlib
from setuptools import setup, find_packages

CWD = pathlib.Path(__file__).parent
README = (CWD / "README.md").read_text()
REQUIREMENTS = [
    'antlr4-python3-runtime==4.9.3',
    'chess==1.7.0'
]

setup(
    name="chessEngines",
    version="1.1.0",
    author="Mario Di Caprio",
    author_email="mariodicaprio10@gmail.com",
    description="A wrapper for chess engines supporting the UCI protocol",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/MarioDiCaprio/chessEngines",
    project_urls={
        "Bug Tracker": "https://github.com/MarioDiCaprio/chessEngines/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    include_paclage_data=True,
    python_requires=">=3.6",
    install_requires=REQUIREMENTS
)
