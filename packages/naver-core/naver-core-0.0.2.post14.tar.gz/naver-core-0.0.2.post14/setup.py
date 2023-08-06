import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
    name='naver-core',
    version='0.0.2-14',
    packages=setuptools.find_packages(),
    author="Jose Cuevas",
    author_email="jose.cuevas.cv@gmail.com",
    description="A Core Ancestor Library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jacr6/naver-core",
    classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
    ], install_requires=[
        'naver-config',
        'naver-db',
        'naver-net',
        'naver-web',
        'naver-business',
        'wheel',
        'twine',
        'bdist_wheel',
    ],
)
