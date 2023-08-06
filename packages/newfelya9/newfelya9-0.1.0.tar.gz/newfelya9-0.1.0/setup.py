from setuptools import setup, find_packages

setup(
    name='newfelya9',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['numpy<1.7',
                      'numexpr',                
                      ],
    entry_points={
        'console_scripts':
            ['newfelya9 = newfelya9.core:minus']
        }

    
)
