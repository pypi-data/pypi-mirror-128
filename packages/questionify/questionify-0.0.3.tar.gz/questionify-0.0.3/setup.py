import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="questionify",
    version="0.0.3",
    author="Jonathan De Wachter",
    author_email="dewachter.jonathan@gmail.com",
    description="Desktop-based software to help you study",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.intjelic.me/project/questionify",
    project_urls={
        "Website": "https://www.intjelic.me/project/questionify",
        "Repository": "https://github.com/intjelic/questionify",
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Environment :: MacOS X",
        "Environment :: Win32 (MS Windows)",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Education"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6"
)
