"""
Setup and packaging for SmartLibrary ERP.
"""
from setuptools import setup, find_packages

setup(
    name="smartlib-erp",
    version="1.0.0",
    description="Enterprise Library Resource Planning System in Pure Python",
    author="SmartLibrary Development Team",
    packages=find_packages(),
    python_requires=">=3.10",
    entry_points={
        "console_scripts": [
            "smartlib=smartlib.cli.manage:main",
        ],
    },
)
