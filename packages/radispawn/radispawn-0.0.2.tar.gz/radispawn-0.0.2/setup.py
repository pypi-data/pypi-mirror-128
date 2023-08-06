from setuptools import setup, find_packages

setup(
    name='radispawn',
    version='0.0.2',
    description='Launch programs and scripts using a radial menu.',
    
    url="https://github.com/aprzn123/RadiSpawn/",
    author="aprzn",
    author_email="apr0alt@gmail.com",

    packages=["radispawn", "radispawn.radial_widget"],
    package_dir={'' :'src'},
    install_requires=['PySide6'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: X11 Applications :: Qt",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Topic :: Utilities"
    ],
    entry_points={"console_scripts": ["radispawn = radispawn.__main__:main"]},
)
