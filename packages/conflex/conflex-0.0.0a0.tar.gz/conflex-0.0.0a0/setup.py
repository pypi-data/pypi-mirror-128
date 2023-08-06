from setuptools import setup

v_long_description = '''
# Conflex
Flexible, extensible configuration reader for Python 3.6+ projects for multiple tree-like config sources.

## Introduction
**Conflex** means "flexible configuration" it is a tool for parsing tree-like configuration with 
any level of depth. Thus, here the configuration is a tree structure with two types of nodes: 
_Section_ and _Option_. _Sections_ is used for grouping other nodes and _option_ is a key-value 
pair. As it mentioned above depth is unlimited, _section_ can have a child _sections_  moreover
_options_ can have child _options_ or _sections_. 
'''

setup(
    name='conflex',
    keywords='configuration parser development',
    version='0.0.0a0',
    packages=['conflex'],
    url='https://github.com/TEH30P/conflex',
    license='MIT',
    author='TEH3OP',
    author_email='TEH3OP@gmail.com',
    description='Flexible tree-like configuration reader.',
    long_description=v_long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.6.0',
    extras_require={
        'testing': [
            'pytest >= 5.3.5',
            'pytest-cov >= 2.8.1',
            'mypy',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',

        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
