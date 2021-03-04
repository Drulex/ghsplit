from setuptools import setup

setup(
 name='ghsplit',
 version='0.1',
 python_requires='>=3.5',
 description='Split/merge large files when working with GH',
 author='Alexandru Jora',
 author_email='alexandru@jora.ca',
 license='MIT',
 keywords='',
 install_requires=[],
 packages=['ghsplit'],
 entry_points={'console_scripts': ['ghsplit = ghsplit.__main__:main']}
)
