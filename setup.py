import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="usefulpython",
    version="0.1.5",
    author="Augustin Garcia",
    author_email="albusdumbledore101123@gmail.com",
    description="tools for a cleaner python experience",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Augustin007/usefulpy",
    project_urls={
        "Bug Tracker": "https://github.com/Augustin007/usefulpy",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)
