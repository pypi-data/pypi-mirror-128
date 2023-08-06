from setuptools import setup, find_packages

setup(
    name='newfelya10',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['numpy<=1.6',
                      'numexpr',                
                      ],
    entry_points={
        'console_scripts':
            ['newfelya10 = newfelya10.core:minus']
        }

    
)
