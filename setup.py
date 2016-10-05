from setuptools import setup, find_packages

NAME = 'django-codemirror-widget'
VERSION = '0.4.1'


def read(filename):
    import os
    BASE_DIR = os.path.dirname(__file__)
    filename = os.path.join(BASE_DIR, filename)
    with open(filename, 'r') as fi:
        return fi.read()

 
def readlist(filename):
    rows = read(filename).split("\n")
    rows = [x.strip() for x in rows if x.strip()]
    return list(rows)

 
setup(
    name=NAME,
    version=VERSION,
    description="Django form widget library for using CodeMirror on textarea",
    long_description=read('README.rst'),
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    keywords="django widget textarea codemirror",
    author="Alisue",
    author_email="lambdalisue@hashnote.net",
    url="https://github.com/lambdalisue/django-codemirror-widget",
    download_url="https://github.com/lambdalisue/%s/tarball/master" % NAME,
    license='MIT',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
)
