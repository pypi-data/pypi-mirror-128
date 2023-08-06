import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="testwizard.smart-tv",
    version="3.5.0b1250",
    author="Eurofins Digital Testing - Belgium",
    author_email="testwizard-support@eurofins-digitaltesting.com",
    description="Testwizard for Smart TV testobjects",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.eurofins-digitaltesting.com/testwizard/",
    packages=['testwizard.smart_tv'],
    install_requires=[
        'testwizard.test==3.5.0b1250',
        'testwizard.testobjects-core==3.5.0b1250',
        'testwizard.commands-audio==3.5.0b1250',
        'testwizard.commands-mobile==3.5.0b1250',
        'testwizard.commands-powerswitch==3.5.0b1250',
        'testwizard.commands-remotecontrol==3.5.0b1250',
        'testwizard.commands-video==3.5.0b1250',
        'testwizard.commands-camera==3.5.0b1250'
    ],
    classifiers=[
        "Programming Language :: Python :: 3.3",
        "Development Status :: 5 - Production/Stable",
        "Operating System :: OS Independent",
    ],
)













