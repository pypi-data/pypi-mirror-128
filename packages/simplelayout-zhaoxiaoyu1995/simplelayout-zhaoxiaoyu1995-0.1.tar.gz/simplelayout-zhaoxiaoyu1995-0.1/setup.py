import setuptools


with open("README.md", "r", encoding='utf-8') as fr:
    long_descriptions = fr.read()


setuptools.setup(
    name="simplelayout-zhaoxiaoyu1995",
    version="0.1",
    author="zhaoxiaoyu",
    author_email="zhaoxiaoyu1995@foxmail.com",
    description="The Simple Layout Generator",
    long_description=long_descriptions,
    long_description_content_type="text/markdown",
    # url="",
    # project_urls={
    #     "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    # },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy'
    ],
    entry_points={
        'console_scripts': [
            'simplelayout = src.simplelayout.__main__:main'
        ]
    }
)
