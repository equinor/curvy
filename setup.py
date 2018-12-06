from distutils.core import setup

setup(
    name='curvy',
    version='0.1dev',
    packages=['curvy',],
    license='MIT',
    long_description=open('README.txt').read(),
    keyswords='smooth curve curves interpolation swap forward prices price python forecast spline electricity gas market maximum smoothness',
    author='Joachim Holwech',
    author='jholw@equinor.com',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'scipy',
        'pandas',
        'matplotlib'
    ]
)