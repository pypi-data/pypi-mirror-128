from setuptools import setup, find_packages

setup(
    name='newfelya6',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['statsmodels>0.11.0',
                      'pandas<0.21',                     
                      ],
    entry_points={
        'console_scripts':
            ['newfelya6 = newfelya6.core:minus']
        }

    
)