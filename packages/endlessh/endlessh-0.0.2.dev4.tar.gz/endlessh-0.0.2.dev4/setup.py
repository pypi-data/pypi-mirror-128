import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="endlessh",
    version="0.0.2dev4",
    author="slipper",
    author_email="r2fscg@gmail.com",
    description="SSH honeypot implemented with Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/GaoangLiu/pyendlessh",
    packages=setuptools.find_packages(),
    package_data={setuptools.find_packages()[0]: ["keys/private.key"]},
    install_requires=['codefast', 'paramiko', 'argparse'],
    entry_points={'console_scripts': ['endlessh=src.pyendlessh:main']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
