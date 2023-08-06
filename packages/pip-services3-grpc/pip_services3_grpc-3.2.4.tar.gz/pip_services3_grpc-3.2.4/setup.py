"""
Pip.Services gRRPC
------------------

Pip.Services is an open-source library of basic microservices.
pip_services3_grpc provides grpc clients and services components.

Links
`````

* `website <http://github.com/pip-services/pip-services>`_
* `development version <http://github.com/pip-services3-python/pip-services3-grpc-python>`

"""

from setuptools import setup
from setuptools import find_packages

try:
    readme = open('readme.md').read()
except:
    readme = __doc__

setup(
    name='pip_services3_grpc',
    version='3.2.4',
    url='http://github.com/pip-services3-python/pip-services3-grpc-python',
    license='MIT',
    author='Conceptual Vision Consulting LLC',
    author_email='seroukhov@gmail.com',
    description='gRPC clients and services for Pip.Services in Python',
    long_description=readme,
    long_description_content_type="text/markdown",
    packages=find_packages(exclude=['config', 'data', 'test']),
    include_package_data=True,
    zip_safe=True,
    platforms='any',
    install_requires=[
        'grpcio',
        'grpcio-tools',
        'protobuf',
        'pytest',
        'iso8601',
        'PyYAML',
        'pystache',

        'pip_services3_commons',
        'pip_services3_rpc',
        'pip_services3_components'
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]    
)
