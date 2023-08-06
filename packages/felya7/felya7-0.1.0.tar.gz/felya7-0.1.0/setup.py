from setuptools import setup

setup(
    name='felya7',
    version='0.1.0',    
    license='BSD 2-clause',
    packages=['test_package'],
    install_requires=['numpy<1.17.3',
                      'pandas',                     
                      ],

    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)