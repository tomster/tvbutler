from setuptools import setup, find_packages

version = '0.1a'

setup(name='tvbutler',
    version=version,
    description="",
    long_description=open('README.rst').read() + "\n" +
        open("HISTORY.rst").read(),
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='rss bittorrent tv',
    author='Tom Lazar',
    author_email='tom@tomster.org',
    url='',
    license='BSD',
    packages=find_packages(exclude=['ez_setup', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
      'distribute',
    ],
    entry_points="""
    # -*- Entry points: -*-
    """,
    )
