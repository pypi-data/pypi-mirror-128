from setuptools import setup

with open("README.rst", "r") as f:
    readme = f.read()

setup(
    name='poplar_workflow',
    version='2.0.4',
    author='Poplar Development',
    url='https://poplars.dev',
    author_email='chris@poplars.dev',
    packages=['poplar_workflow'],
    package_data={
        '': ['vi/*.vi', 'expi.json' ],
    },
    description=(""),
    long_description=readme,
    include_package_data=True,
    install_requires=[
        'extools>=0.13.0',
    ],
    # Valid classifiers: https://pypi.org/classifiers/
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Win32 (MS Windows)",
        "Intended Audience :: End Users/Desktop",
        "License :: Other/Proprietary License",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python :: 3.4",
    ],
    keywords=[
        "Orchid", "Extender", "Sage 300", "Automation",
    ],
    download_url="https://expi.dev/poplar_workflow/"
)
