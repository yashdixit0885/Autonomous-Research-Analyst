from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "pytest",
        "pytest-asyncio",
        "httpx",
        "yfinance",
        "pandas",
        "numpy"
    ],
) 