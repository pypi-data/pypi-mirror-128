import setuptools

#   to upload
#   python3 -m build
#   python3 -m twine upload --repository pypi dist/*



with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qiwi_handler",
    version="0.0.8",
    author="bezumnui",
    author_email="bezumnui.mistikgt@gmail.com",
    description="обртка с обработчиком для qiwi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bezumnui/qiwi_handler/",
    project_urls={
        "Bug Tracker": "https://github.com/bezumnui/qiwi_handler/issues",
        "Get Qiwi Token": "https://qiwi.com/api"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "qiwi_handler"},
    packages=setuptools.find_packages(where='qiwi_handler'),
    python_requires=">=3.6",
)