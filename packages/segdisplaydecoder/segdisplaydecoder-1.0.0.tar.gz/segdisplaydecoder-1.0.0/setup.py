from setuptools import setup, find_packages

VERSION = '1.0.0'
DESCRIPTION = 'BCD to 7 Segment Display Decoder'
# LONG_DESCRIPTION = ''

# Setting up
setup(
    name="segdisplaydecoder",
    version=VERSION,
    author="Rounak Shaw , Prasun Roy",
    author_email="prasunroyinfo@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    # long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'decoder', 'displaydecoder'],
    license="MIT",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Microsoft :: Windows",
    ]
)