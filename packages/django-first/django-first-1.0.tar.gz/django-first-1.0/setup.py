import os
from setuptools import find_packages, setup


# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='django-first',
    version='1.0',
    packages=find_packages(),
    include_package_data=True,
    license='BSD License', # example license
    description='login and register, base on Django',
    author='test',
    author_email='test@example.com',
    classifiers=[
        'Framework :: Django :: 3.2',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
    ]
)
