from setuptools import setup, find_namespace_packages


setup(
    name='scrabble-solver',
    version='1.0',
    package_dir={'': 'src'},
    packages=find_namespace_packages(where='src'),
    package_data={'': ['*.txt']},
    url='https://github.com/b33j0r',
    license='',
    author='Brian Jorgensen',
    author_email='',
    description='Calculates optimal moves for word puzzle games',
    install_requires=[],
    entry_points={
        'console_scripts': []
    },
)
