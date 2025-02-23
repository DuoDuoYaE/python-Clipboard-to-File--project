from setuptools import setup, find_packages

setup(
    name='clipboard_to_file',
    version='1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    entry_points={
        'console_scripts': [
            'clipboard_to_file = Main:main',  # Assuming you have a main function in Main.py
        ],
    },
    install_requires=[
        'keyboard',
        'tkinter',  # tkinter is included with Python, but you can specify it if needed
    ],
    include_package_data=True,
    zip_safe=False,
)