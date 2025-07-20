from setuptools import setup, find_packages

setup(
    name="shared_core",
    version="0.1.0",
    description="Shared core components for Data Centralization Platform",
    packages=find_packages(),
    python_requires=">=3.9",
    install_requires=[
        "pandas",
        "numpy",
        "openai",
        "pydantic",
    ],
)
