from setuptools import setup, find_packages

with open('.version') as v:
    version = v.read()

with open('README.md') as r:
    readme = r.read()

with open('requirements.txt') as req:
    requirements = req.read().splitlines()

package_data = {
    '': ['LICENSE', 'README.md', 'requirements.txt', '.version']
}

setup(
    name='gila',
    version=version,
    description=('A simple python3 config library based on'
                 'golang\'s spf13/viper'),
    long_description=readme,
    url='https://gitlab.com/dashwav/gila',
    author='dashwav',
    license='MPL2.0',
    packages=find_packages(exclude=['tests', 'docs']),
    include_package_data=True,
    package_data=package_data,
    install_requires=requirements,
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)',
        'Programming Language :: Python :: 3 :: Only'
        'Intended Audience :: Developers',
        'Natural Language :: English'
    ]
)
