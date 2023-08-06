from distutils.core import setup

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pulemet',
    version='1.0.1a',
    license='MIT',
    license_files='LICENSE.txt',
    author='Data Science SWAT',
    author_email='UnitDataScienceSwat@avito.ru',
    description='Manage coroutine execution speed',
    packages=[
        'pulemet',
    ],
    install_requires=[
        'asyncio>=3.4.3,<4',
        'aiohttp>=3.7.3,<4'
    ],
    url='https://github.com/avito-tech/pulemet',
    download_url='https://github.com/avito-tech/pulemet/archive/refs/heads/main.zip',
    keywords=['rps', 'coroutines'],
    python_requires='>=3.6',
    include_package_data=True,
    long_description=long_description,
    long_description_content_type='text/x-rst',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering',
        'Topic :: Software Development :: Build Tools',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.6',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Operating System :: Unix',
        'Operating System :: OS Independent',
    ]
)
