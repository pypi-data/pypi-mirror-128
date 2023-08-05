from setuptools import setup

setup(
    name='ismtestpack',
    author = 'Ismail',
    url = 'https://github.com/isba06',
    author_email = 'none@mail.ru',
    version='0.1.6',
    packages=['ismtestpack'],
    install_requires=['numpy<=1.18.0', "sklearn", "typing"],


    classifiers = [
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