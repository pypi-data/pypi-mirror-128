import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="ssupervisor",
    version="1.0.0",
    author="Infinium LLC.",
    author_email="infinium-llc@protonmail.com",
    description="Effortlessly run scripts when certain files change.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Infinium8/Supervisor",
    project_urls={
        "Bug Tracker": "https://github.com/Infinium8/Supervisor/issues",
    },
	install_requires=[
        'Click',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
	entry_points={
        'console_scripts': [
            'supervisor = Supervisor:cli',
        ],
    },
)