import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplelayoutpiglet94",
    version="0.0.5",
    author="piglet94",
    author_email="715654107@qq.com",
    description="A small study package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    url="https://github.com/pypa/sampleproject",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(include=['src', 'src.*']),
    python_requires=">=3.0",
    install_requires=['numpy','argparse','matplotlib','scipy'],
    entry_points={'console_scripts': ['simplelayout=simplelayout:main',],}
)