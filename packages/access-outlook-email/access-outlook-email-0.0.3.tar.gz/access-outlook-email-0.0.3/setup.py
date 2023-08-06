from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'Send Emails via Outlook'
LONG_DESCRIPTION = 'A package that allows to send emails from an outlook account'

# Setting up
setup(
    name="access-outlook-email",
    version=VERSION,
    author="Valentin Baier",
    author_email="valentin_baier@gmx.de",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=['exchangelib'],
    keywords=['python', 'email', 'outlook', 'send', 'send email'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
