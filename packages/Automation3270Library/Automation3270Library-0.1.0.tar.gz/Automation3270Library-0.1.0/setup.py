import setuptools

setuptools.setup(
        name = 'Automation3270Library',
        version = '0.1.0',
        description = 'Python library to communicate with IBM hosts, based on the 3270 protocol.',
        author = 'Daniel Beck',
        url = '',
        packages=setuptools.find_packages(),
        python_requires='>=3.6',
        install_requires=[
            'py3270>=0.3.5'
        ],
        long_description = '''
    A Python library that provides an interface to communicate with IBM host.
    ''',
        keywords = 'IBM x3270 s3270 Mainframe ',
        classifiers = [
            'Intended Audience :: Developers',
            'Programming Language :: Python',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3 :: Only',
            'Operating System :: Unix',
            'Operating System :: POSIX :: Linux',
            'Topic :: Software Development :: Testing',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Development Status :: 1 - Planning'
        ]
)