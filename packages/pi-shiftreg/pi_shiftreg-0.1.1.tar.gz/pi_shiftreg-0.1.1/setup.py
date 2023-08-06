from setuptools import setup

setup(
    name='pi_shiftreg',
    version='0.1.1',    
    description='A simple tool for controlling Shift Registers with RPi GPIO pins',
    url='https://github.com/kevinpthorne/pi_shiftreg',
    author='Kevin Thorne',
    author_email='kevinpthorne@gmail.com',
    license='MIT',
    packages=['pi_shiftreg'],
    install_requires=['RPi.GPIO>=0.7.0'],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',  
        'Operating System :: POSIX :: Linux',        
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
