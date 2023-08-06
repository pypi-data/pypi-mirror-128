from setuptools import setup, find_packages

setup(
    name='newfelya3',
    version='0.1.0',    
    packages=find_packages(),
    install_requires=['opencv-python==4.5.4.58',
                      'numpy<1.14.5pip ',                     
                      ],
    entry_points={
        'console_scripts':
            ['newfelya3 = newfelya3.core:minus']
        }

    
)