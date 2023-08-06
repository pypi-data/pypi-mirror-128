from setuptools import setup, find_packages
 
setup(
    name='metathing',
    version='0.0.4',
    description='MT-Service Python',
    license='N/A',
    packages=find_packages(exclude=['test', 'workdir']),
)