# Anuvaad_Tokenizer


try:
    from setuptools import setup , find_packages
except ImportError:
    from distutils.core import setup
from os.path import join, dirname

import pathlib
HERE = pathlib.Path(__file__).parent
README = (HERE/"README.md").read_text()

setup(
    name='Anuvaad_Tokenizer',
    version='0.0.3',
    description='Tokenizer by Anuvaad ',
    long_description= README,
    long_description_content_type = "text/markdown",
    author='Anuvaad',
    author_email= "nlp-nmt@tarento.com",
    packages=find_packages(),
    package_data={'Anuvaad_Tokenizer': ['*.txt']}, 
    license='MIT',
    python_requires='>=3.6.0',
    install_requires=['nltk'],
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
      ],
)