from setuptools import setup, find_packages


with open("README.md", "r") as file:
    long_description = file.read()

with open("requirements.txt", 'r') as file:
    requirements = file.read().split('\n')

dev_status = {
    "Alpha": "Development Status :: 3 - Alpha",
    "Beta": "Development Status :: 4 - Beta",
    "Pro": "Development Status :: 5 - Production/Stable",
    "Mature": "Development Status :: 6 - Mature",
}

setup(
    name="BloomTechLib",
    author="Robert Sharp - BloomTech Labs",
    author_email="webmaster@sharpdesigndigital.com",
    packages=find_packages(),
    install_requires=requirements,
    version="0.0.1",
    description="Python Library of General Data Science Solutions",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    classifiers=[
        dev_status["Alpha"],
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=[
        "BloomTech", "Data Science",
    ],
    python_requires=">=3.6",
)
