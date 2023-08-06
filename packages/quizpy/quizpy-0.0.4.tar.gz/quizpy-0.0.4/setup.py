import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="quizpy",
    version="0.0.4",
    author="Sebastian Bräuer",
    author_email="braeuer@tu-berlin.de",
    description="A package to create Moodle exams using Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://git.tu-berlin.de/tkn/quizpy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
