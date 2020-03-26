
from setuptools import setup, find_packages


with open('README.md') as file:
    description = file.read()


setup(
    name='razdel',
    version='0.5.0',

    description='Splits russian text into tokens, sentences, section. Rule-based',
    long_description=description,
    long_description_content_type='text/markdown',

    url='https://github.com/natasha/razdel',
    author='Alexander Kukushkin',
    author_email='alex@alexkuk.ru',
    license='MIT',

    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
    keywords='nlp, natural language processing, russian, token, sentence, tokenize',

    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'razdel-ctl=razdel.tests.ctl:main'
        ],
    },
    install_requires=[]
)
