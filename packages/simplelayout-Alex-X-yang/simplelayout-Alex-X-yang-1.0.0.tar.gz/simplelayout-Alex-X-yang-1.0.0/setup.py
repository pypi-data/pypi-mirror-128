import setuptools

setuptools.setup(
    name="simplelayout-Alex-X-yang",
    version="1.0.0",
    author="Alex-X-yang",
    author_email="735629961@qq.com",
    description="A simplelayout package",
    long_description_content_type="text/markdown",
    url="https://github.com/idrl-assignment/3-simplelayout-package-Alex-X-yang",
    package_dir={'': 'src'},
    packages=setuptools.find_packages(where='src'),
    keywords='simplelayout',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={'console_scripts': ['simplelayout = simplelayout:main']},
    install_requires=[
        'numpy',
        'matplotlib',
        'scipy',
        'argparse',
        'pathlib',
    ]
)
