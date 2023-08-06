# This file is placed in the Public Domain.
#
# project on one, pay for millions.


import os


from setuptools import setup


def read():
    return open("README.rst", "r").read()


def uploadlist(dir):
    upl = []
    for file in os.listdir(dir):
        if not file or file.startswith('.'):
            continue
        d = dir + os.sep + file
        if os.path.isdir(d):   
            upl.extend(uploadlist(d))
        else:
            if file.endswith(".pyc") or file.startswith("__pycache"):
                continue
            upl.append(d)
    return upl


setup(
    name='genocide',
    version='45',
    url='https://github.com/bthate/genocide2',
    author='Bart Thate',
    author_email='bthate67@gmail.com', 
    description="project on one, pay for millions",
    long_description=read(),
    license='Public Domain',
    packages=["gcd", "genocide"],
    zip_safe=True,
    include_package_data=True,
    install_requires=["feedparser"],
    data_files=[
                ("share/genocide", ["files/genocide.service"]),
                ("share/genocide", ["files/genocide.1.md"]),
                ("share/doc/genocide", uploadlist("docs")),
                ("share/doc/genocide/jpg", uploadlist("docs/jpg")),
                ("share/doc/genocide/pdf", uploadlist("docs/pdf")),
                ("share/doc/genocide/_templates", uploadlist("docs/_templates")),
                ("share/man/man1/", ["files/genocide.1.gz"]),
               ],
    scripts=["bin/genocide", "bin/genocidec", "bin/genocidectl", "bin/genocided"],
    classifiers=['Development Status :: 3 - Alpha',
                 'License :: Public Domain',
                 'Operating System :: Unix',
                 'Programming Language :: Python',
                 'Topic :: Utilities'
                ]
)
 