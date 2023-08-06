from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='SetSolver1',
    version='1!2021.11.2',
    url='https://github.com/LukasWestholt/SetSolver1',
    author='lukaswestholt',
    author_email='support@lukaswestholt.de',
    description='This script is solving set problems by brute-force.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    # package_dir={"": "src"},
    python_requires=">=3.10",
    project_urls={
        "Bug Tracker": "https://github.com/LukasWestholt/SetSolver1/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    license='GPLv3',
    license_files=('LICENSE',)
)
