import os

from setuptools import setup

ROOT = os.path.dirname(os.path.realpath(__file__))


setup(
    # Meta data
    name='useragent_rs',
    version='0.1.5',
    author="Rosario Sensale",
    author_email='pcassistenzatecnica@gmail.com',
    maintainer="Rosario Sensale",
    maintainer_email='pcassistenzatecnica@gmail.com',
    url='https://github.com/aloneinthedark/useragent_rs',
    description='User-Agent generator',
    long_description=open(os.path.join(ROOT, 'README.rst')).read(),
    download_url='http://pypi.python.org/pypi/useragent_rs',
    keywords="user agent browser navigator",
    license="MIT License",
    # Package files
    packages=['useragent_rs'],
    include_package_data=True,
    install_requires=['six'],
    entry_points={
        'console_scripts': [
            'ua = useragent_rs.base:script_ua',
        ],
    },
    # Topics
    classifiers=[
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython',
        'License :: OSI Approved :: MIT License',
        #'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Internet :: WWW/HTTP',
    ],
)
