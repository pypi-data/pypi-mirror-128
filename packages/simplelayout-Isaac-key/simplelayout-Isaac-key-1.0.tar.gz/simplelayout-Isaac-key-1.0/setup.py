from setuptools import setup, find_packages
import os

setup(
   
    name = 'simplelayout-Isaac-key',
    version = '1.0',
    description = ' The third github classroom work',
    author = 'Isaac',
    license = 'ZJU',
    #packages = find_packages(include=["src/simplelayout", "src/simplelayout.*"]),
    packages = find_packages('src/simplelayout'),
    package_dir={'':'src/simplelayout'},
    
    #package_data={

    #    '':['*.py'],

    #},

    long_description=open(
        os.path.join(
            os.path.dirname(__file__),
            'README.rst'
        )
    ).read(),

    install_requires = [
        'matplotlib',
        'scipy',
        'numpy'
    ],

    entry_points = {
        'console_scripts':[
            'simplelayout=Important.__main__:main'
        ]
    }
    
    )

