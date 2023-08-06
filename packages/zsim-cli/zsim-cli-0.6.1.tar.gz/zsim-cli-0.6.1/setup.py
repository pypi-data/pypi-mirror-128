from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='zsim-cli',
    version='0.6.1',
    author='Justin Lehnen',
    author_email='justin.lehnen@gmx.de',
    description='A simulator for an assembly like toy-language.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://gitlab.com/justin_lehnen/zsim-cli',
    project_urls={
        'Bug Tracker': 'https://gitlab.com/justin_lehnen/zsim-cli/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: The Unlicense (Unlicense)',
        'Operating System :: OS Independent',
    ],
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    py_modules=['zsim'],
    include_package_data=True,
    entry_points='''
        [console_scripts]
        zsim-cli=zsim.cli:entry_point
    ''',
    install_requires=[
        'click>=5.1',
        'pytest',
    ],
    python_requires='>=3.6'
)
