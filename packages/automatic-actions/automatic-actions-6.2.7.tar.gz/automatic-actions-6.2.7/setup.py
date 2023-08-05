import setuptools
import requests

# response = requests.get("https://api.github.com/repos/cxnt/automatic-actions/releases/latest")
response = requests.get("https://api.github.com/repos/supervisely/supervisely/releases/latest")
version = response.json()["tag_name"]

# with open("docker/VERSION", "w", encoding="utf-8") as fh:
#     fh.write(f"{version.lstrip('v')}\n")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automatic-actions",
    version=version,
    author="cxnt",
    author_email="pavelbartsits@gmail.com",
    description="Automatic builds for PYPI and Docker",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cxnt/automatic-actions",
    project_urls={
        "Bug Tracker": "https://github.com/cxnt/automatic-actions/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
)
