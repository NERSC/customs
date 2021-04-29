from setuptools import setup, find_packages

setup(
    author="R. C. Thomas",
    author_email="rcthomas@lbl.gov",
    description="Inspect and report Python packages of interest",
    name="customs",
    version="0.3.0",
    packages=find_packages(exclude=["tests"]),
)
