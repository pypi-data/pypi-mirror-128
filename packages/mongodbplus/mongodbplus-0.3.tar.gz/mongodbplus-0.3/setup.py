from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Education',
    'License :: OSI Approved :: MIT License',
    "Operating System :: Unix",
    "Operating System :: MacOS :: MacOS X",
    "Operating System :: Microsoft :: Windows",
    'Programming Language :: Python :: 3'
]

setup(
    name='mongodbplus',
    version='0.3',
    description='Use pymongo with a bit of sugar.',
    long_description='Use pymongo with a bit of sugar.',
    url='https://github.com/anthony16t/mongodbplus',  
    author='anthony16t',
    author_email='info@anthony16t.com',
    license='MIT', 
    classifiers=classifiers,
    keywords=['json','mongo','mongodb'], 
    install_requires=['pymongo'],
    packages=find_packages()
)