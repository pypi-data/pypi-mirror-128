import setuptools


with open("README.md", "r", encoding='utf-8') as fh:
    long_description = fh.read()

setuptools.setup(
    name="simplelayout-YujieFeng20",
    description="simplelayout",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/idrl-assignment/3-simplelayout-package-YujieFeng20",
    packages=setuptools.find_packages(),
    install_requires=['matplotlib==3.4.3', 'numpy==1.21.2', 'scipy==1.7.1'],
    entry_points={
        'console_scripts': [
            'simplelayout=simplelayout:main'
        ],
    },
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
