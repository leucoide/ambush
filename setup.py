import setuptools

setuptools.setup(
    name="ambush",
    version="0.1.0",
    url="https://github.com/borntyping/cookiecutter-pypackage-minimal",
    author="Yuri Vasquez",
    author_email="yuri.vasquez91@gmail.com",
    description="A smart file system watcher",
    long_description=open('README.rst').read(),
    packages=setuptools.find_packages(),
    install_requires=[],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
)
