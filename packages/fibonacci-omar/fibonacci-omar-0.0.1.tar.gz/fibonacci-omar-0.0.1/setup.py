from setuptools import find_packages, setup


AUTHOR = 'Omar Elazhary'
AUTHOR_EMAIL = 'omazhary@gmail.com'
LICENSE = 'MIT'
SHORT_DESCRIPTION = 'Plays around with Fibonacci sequences.'
VERSION = '0.0.1'

with open("README.md", "r", encoding="utf-8") as long_description_in:
    long_description = long_description_in.read()
setup(
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    name='fibonacci-omar',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
    ],
    description=SHORT_DESCRIPTION,
    install_requires=[],
    keywords='fibonacci sequence',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires='>=3.9',
    scripts=[
        'bin/fibonacci'
    ],
    url='https://reposherlock.readthedocs.io/en/latest/index.html',
    version=VERSION,
    zip_safe=False
)
