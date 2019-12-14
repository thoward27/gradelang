from setuptools import setup, find_packages

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='gradelang',
    setup_requires=['setuptools_scm'],
    use_scm_version=True,
    packages=find_packages('.', exclude='test'),
    url='https://github.com/thoward27/gradelang',
    license='AGPL',
    author='Tom Howard',
    author_email='info@tomhoward.codes',
    description='A Domain Specific Language for Autograding.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    python_requires='>=3.7',
    install_requires=['ply', 'grade', 'Click', 'hypothesis']
)
