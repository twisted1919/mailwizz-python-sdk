import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='mailwizz-python-sdk',
    version='1.0.0',
    packages=setuptools.find_packages(),
    url='https://www.mailwizz.com',
    license='MIT',
    author='twisted1919',
    author_email='support@mailwizz.com',
    description='This repository contains the Python SDK for MailWizz EMA.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'multidimensional-urlencode>=0.0.4',
        'requests>=2.22.0',
        'urllib3>=1.25.3',
    ],
)
