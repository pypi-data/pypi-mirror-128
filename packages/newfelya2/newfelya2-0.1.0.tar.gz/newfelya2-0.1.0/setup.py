from setuptools import setup, find_packages

setup(
    name='newfelya2',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['mpi4py>=2.0',
                      'numpy',                     
                      ],
    entry_points={
        'console_scripts':
            ['newfelya2 = newfelya2.core:minus']
        }

    
)