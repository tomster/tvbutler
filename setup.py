from setuptools import setup
version = '0.1a5'

setup(name='tvbutler',
    version=version,
    description="tvbutler reads RSS feeds from http://tvtorrents.com and "
        "downloads torrents of new episodes for you in your preferred quality",
    long_description=open('README.rst').read() + "\n" +
        open("HISTORY.rst").read(),
    classifiers=[
        "Environment :: Console",
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python :: 2.5",
        "Programming Language :: Python :: 2.6",
        "Topic :: Multimedia :: Video",
        "Topic :: Communications :: File Sharing",
    ], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='rss bittorrent tv',
    author='Tom Lazar',
    author_email='tom@tomster.org',
    url='https://github.com/tomster/tvbutler',
    license='BSD',
    packages=['tvbutler'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
      # -*- Extra requirements: -*-
      'distribute',
      'feedparser',
      'sqlalchemy',
    ],
    entry_points="""
    # -*- Entry points: -*-
    [console_scripts]
    tvbutler=tvbutler.command:main
    """,
    )
