import setuptools
long_description = """# About


Functional package

```py
from scflcore import CoreManager

core = coreManager(
	name="MyCore"
)

print(core.request(url="https://example.com", json=True))
```
"""
setuptools.setup(
    name="scflcore", # Put your username here!
    version="0.0.6", # The version of your package!
    author="SScefaLI", # Your name here!
    author_email="birka11@list.ru", # Your e-mail here!
    description="Function core package by SScefaLI", # A short description here!
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="", # Link your package website here! (most commonly a GitHub repo)
    packages=setuptools.find_packages(), # A list of all packages for Python to distribute!
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ], # Enter meta data into the classifiers list!
    python_requires='>=3.8', # The version requirement for Python to run your package!
)