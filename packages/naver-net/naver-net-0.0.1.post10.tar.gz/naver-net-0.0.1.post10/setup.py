import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='naver-net',
    version='0.0.1-10',
    packages=setuptools.find_packages(),
    author="Jose Cuevas",
    author_email="jose.cuevas.cv@gmail.com",
    description="A Net Persistence Ancestor Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacr6/naver-net",
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], install_requires=[
        'Pyro4',
        'pika',
        'protocol',
        'naver-config',  
        'twine',
        'bdist_wheel',
    ],
)
