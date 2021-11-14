import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="illallangi-gazelletelegraf",
    version="0.0.1",
    author="Andrew Cole",
    author_email="andrew.cole@illallangi.com",
    description="TODO: SET DESCRIPTION",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/illallangi/GazelleTelegraf",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    entry_points={
        'console_scripts': [
            'gazelle-telegraf=illallangi.gazelletelegraf:__main__.cli'
        ],
    },
    install_requires=[
        'click',
        'six',
        'telegraf_pyplug',
        'illallangi.orpheusapi @ git+https://github.com/illallangi/OrpheusAPI@master',
        'illallangi.redactedapi @ git+https://github.com/illallangi/RedactedAPI@master',
        'illallangi.btnapi @ git+https://github.com/illallangi/BTNAPI@master',
    ]
)
