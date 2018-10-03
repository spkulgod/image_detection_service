from setuptools import setup
from setuptools import find_packages

setup(
    name='cnn_im_detect',
    version='0.0.1',
    packages=[],
    py_modules=['scripts.cnn_im_detect'],
    install_requires=['setuptools'],
    author='Sutej Kulgod',
    author_email='sutej.kulgod@nymble.in',
    maintainer='Rohin Malhotra',
    maintainer_email='rohin@nymble.in',
    keywords=['ROS'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python',
        'Topic :: Software Development',
    ],
    description='Package containing a service for image detection using tensor flow CNN',
    license='Apache License, Version 2.0',
    test_suite='test',
    entry_points={
        'console_scripts': [
            'cnn_im_detect = scripts.cnn_im_detect:main',
        ],
    },
)
