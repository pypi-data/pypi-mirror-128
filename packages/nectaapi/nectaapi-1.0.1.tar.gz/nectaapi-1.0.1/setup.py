from setuptools import setup, find_packages

VERSION = '1.0.1'
DESCRIPTION = 'Fetch results of various national examinations done in Tanzania'
LONG_DESCRIPTION = ""
with open('readme.md') as rm:
    LONG_DESCRIPTION = rm.read()

# Setting up
setup(
    name="nectaapi",
    version=VERSION,
    author="Tanzania Programmers (Vincent Laizer)",
    author_email="<laizercorp@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'necta', 'api', 'necta api', 'necta tanzania', 'tanzania programmers'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)