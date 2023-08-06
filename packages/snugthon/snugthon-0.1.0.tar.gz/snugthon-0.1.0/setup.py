from setuptools import setup, find_packages

with open("README.md", "r") as f:
    desc = f.read()

setup(
    name="snugthon",
    version="0.1.0",
    description="Snug for python3.",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/snuglibs/snugthon",
    author="aiocat",
    author_email="",
    license="MIT",
    project_urls={
        "Bug Tracker": "https://gitlab.com/snuglibs/snugthon/-/issues",
    },
    classifiers=[
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3"
    ],
    keywords=["snug", "config"],
    packages=find_packages(),
    python_requires=">=3.6.0",
    install_requires=[]
)
