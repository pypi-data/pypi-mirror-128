import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='naver-config',
    version='0.0.1-10',
    packages=setuptools.find_packages(),
    author="Jose Cuevas",
    author_email="jose.cuevas.cv@gmail.com",
    description="A Config Ancestor Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacr6/naver-config",
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], install_requires=[
        'python-consul',
        'python-decouple',
        'wheel',
        'twine',
        'bdist_wheel',
    ],
)
