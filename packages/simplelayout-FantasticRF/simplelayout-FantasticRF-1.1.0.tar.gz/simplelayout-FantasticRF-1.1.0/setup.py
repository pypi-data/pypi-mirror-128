from setuptools import setup, find_packages


setup(
    name='simplelayout-FantasticRF',
    version='1.1.0',
    package_dir={'': 'src'},
    packages=find_packages(where='src'),
    install_requires=['numpy', 'matplotlib', 'scipy'],
    entry_points={'console_scripts': ['simplelayout = simplelayout:main'], }
)
