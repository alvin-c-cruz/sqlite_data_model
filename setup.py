from distutils.core import setup

setup(
    name='sqlite_data_model',
    packages = ['sqlite_data_model'],
    version = '0.2',
    license = 'mit',
    description='A class using the built-in @dataclass decorator in conjunction with sqlite3.',
    author='Alvin C. Cruz',
    author_email='alvinccruz12@gmail.com',
    url='https://github.com/alvin-c-cruz/sqlite_data_model',
    download_url='https://github.com/alvin-c-cruz/sqlite_data_model/archive/refs/tags/v0.2.tar.gz',
    keywords=['dataclass', 'sqlite', 'datamodel'],
    install_requires=[],
    classifiers=[
        'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.7',      
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        ],
)