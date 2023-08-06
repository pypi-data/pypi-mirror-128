from setuptools import setup, find_packages

setup(
    name='newfelya11',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['numexpr',
                      'numpy<=1.6',                
                      ],
    entry_points={
        'console_scripts':
            ['newfelya11 = newfelya11.core:minus']
        }

    
)
