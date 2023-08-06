from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()

setup(
    name='pylimo',
    version='0.3.0',
    author='agilexrobotics',
    author_email='support@agilex.ai',
    description='A small example package for limo',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/agilexrobotics/limo_ros',
    project_urls={
        'Bug Tracker': 'https://github.com/agilexrobotics/limo_ros/issues',
    },
    classifiers=[
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        
    ],

    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['pyserial>=3.5'],
    python_requires='>=3.6',
)
