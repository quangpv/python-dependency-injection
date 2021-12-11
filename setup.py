from setuptools import setup, find_packages

setup(
    name='qpvdi',
    version='0.1',
    license='MIT',
    author="Quangpv",
    author_email='quangpv.uit@gmail.com',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/quangpv/python-dependency-injection',
    keywords='dependency injection',
    install_requires=[],
)
