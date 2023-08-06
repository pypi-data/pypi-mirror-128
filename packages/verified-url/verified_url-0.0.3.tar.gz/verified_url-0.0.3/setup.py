from setuptools import setup, find_packages

classifiers = [
    'Development Status :: 5 - Production/Stable',
    'Intended Audience :: Developers',
    'Operating System :: Microsoft',
    'Operating System :: Unix',
    'Operating System :: MacOS',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3'
]


setup(
    name='verified_url',
    version='0.0.3',
    description='Package for check url',
    long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
    long_description_content_type='text/markdown',
    url='',
    author='Maxime JARRY',
    author_email='maxime.jarry@outlook.com',
    license='MIT',

    classifiers=classifiers,
    keywords='URL,STATUS',
    packages=find_packages()
)
