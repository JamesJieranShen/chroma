from setuptools import setup, find_packages, Extension
import subprocess
import os


#####
setup(
    name = 'Chroma',
    version = '0.5',
    packages = find_packages(),
    include_package_data=True,

    scripts = ['bin/chroma-sim', 'bin/chroma-cam',
               'bin/chroma-geo', 'bin/chroma-bvh',
               'bin/chroma-server'],
    setup_requires = [],
    install_requires = ['uncertainties',
                        'pyzmq', 
                        'pycuda',
                        'pytools==2022.1.2',
                        'numpy>=1.6', 
                        'scipy',
                        'pygame', 
                        #'nose', 
                        'sphinx', 
                        'particle', 
                        'uproot'],
    #test_suite = 'nose.collector',
    
)
