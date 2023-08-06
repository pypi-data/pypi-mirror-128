from setuptools import setup, find_packages

VERSION = '3'
DESCRIPTION = 'PyLexers is a python lexical analyzer generator.'
LONG_DESCRIPTION = 'PyLexer can be used to make many different types of ' \
                   'lexical analyzer generators for your project.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="pylexers",
    version=VERSION,
    author="Andrew Reed",
    author_email="andrewreed2017@icloud.com",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'lexical analysis', 'lexical analyzer generator', 'lexer'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)