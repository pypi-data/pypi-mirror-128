from setuptools import setup, find_packages

setup(
    name='newfelya12',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['opencv-python',
                      'numpy<=1.14.5',                
                      ],
    entry_points={
        'console_scripts':
            ['newfelya12 = newfelya12.core:minus']
        }

    
)