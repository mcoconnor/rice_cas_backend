#!/usr/bin/env python

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

setup(
    name='rice_cas_backend',
    version='0.1',
    description='CAS backend for django_cas incorporating Rice''s LDAP directory',
    author='Michael O''Connor',
    author_email='michael@mcoconnor.net',
    url='https://github.com/mcoconnor/rice_cas_backend',
    license='MIT',
    packages=['rice_cas_backend'],
    requires=['django_cas'],
    include_package_data=True,
    zip_safe=False,
    platforms = ['any'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ]
)