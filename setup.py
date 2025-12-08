from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="crewai-amorce",
    version="0.1.0",
    description="Secure CrewAI crews with Amorce (Ed25519 + HITL + A2A)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Amorce Team",
    author_email="team@amorce.io",
    url="https://github.com/amorce/crewai-amorce",
    project_urls={
        "Bug Tracker": "https://github.com/amorce/crewai-amorce/issues",
        "Documentation": "https://amorce.io/docs",
        "Source Code": "https://github.com/amorce/crewai-amorce",
    },
    packages=find_packages(),
    install_requires=[
        "amorce-sdk>=0.2.1",
        "crewai>=0.1.0",
    ],
    python_requires=">=3.10",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
    ],
    keywords="crewai amorce ai agents security ed25519 signatures hitl a2a",
)
