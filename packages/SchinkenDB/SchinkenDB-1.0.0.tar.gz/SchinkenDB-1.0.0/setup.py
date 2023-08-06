from setuptools import setup, find_packages

# Get Long Description
with open("README.md", "r") as readme:
    long_description = readme.read().replace("Â", "")
# Get requirements.txt
with open("requirements.txt", "r") as requirements:
    reqs = requirements.read().splitlines()

setup(
    name="SchinkenDB",
    version="1.0.0",
    # Major version 1
    # Minor version 0
    # Maintenance version 0

    author="DerSchinken",
    description="This is my Database it is no gud and shouldn't be used lmao",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=reqs,
    python_requires=">=3.6",
    project_urls={
        "Source": "https://github.com/DerSchinken/SchinkenDB",
    },
    keyword=[
        "Schinken",
        "DataBase", "DB",
        "SchinkenDB",
    ],
    classifiers=[
        'Intended Audience :: Developers',

        'Operating System :: OS Independent',

        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        "Programming Language :: Python :: 3.10"
    ],
)
