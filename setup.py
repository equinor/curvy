from setuptools import setup

setup(
    name='curvy',
    version='0.1dev',
    packages=['curvy',],
    license='MIT',
    long_description=open('README.md').read(),
    keyswords='smooth curve curves interpolation swap forward prices price python forecast spline electricity gas market maximum smoothness',
    author='Joachim Holwech',
    author_email='jholw@equinor.com',
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
#        'matplotlib'
    ]
)