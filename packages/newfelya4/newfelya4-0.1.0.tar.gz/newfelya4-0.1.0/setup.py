from setuptools import setup, find_packages

setup(
    name='newfelya4',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['statsmodels>0.11.0',
                      'numpy<1.14 ',                     
                      ],
    entry_points={
        'console_scripts':
            ['newfelya4 = newfelya4.core:minus']
        }

    
)