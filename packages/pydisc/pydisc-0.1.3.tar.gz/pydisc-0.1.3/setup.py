from setuptools import setup

with open("README.md", "r") as f:
    readme = f.read()
setup(
    name="pydisc",
    version="0.1.3",
    description="a discord bot wrapper for python have slash command",
    url="https://github.com/pydisc/pydisc",
    author="cutebear0123",
    long_description=readme,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["pydisc", "pydisc.types", "pydisc.setup"],
    install_requires=["websockets", "requests"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Utilities",
        "Typing :: Typed",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.7",
)
