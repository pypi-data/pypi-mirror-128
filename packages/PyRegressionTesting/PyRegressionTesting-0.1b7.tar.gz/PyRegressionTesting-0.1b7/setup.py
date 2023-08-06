import setuptools

setuptools.setup(
    name="PyRegressionTesting",
    version="0.1-B7",
    author="Sascha Huber",
    author_email="kontakt@sascha-huber.com",
    description="Easily run regression tests on your website!",
    long_descritpion="Regression-Testing-Framework with Selenium for your Website",
    long_description_content_type="text/markdown",
    url="https://github.com/saschahuber/PyRegressionTesting",
    entry_points = {
        'console_scripts': ['PyRegressionTesting=PyRegressionTesting.CommandLine:main'],
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'selenium'
    ]
)

#Commands to build
#pip install --upgrade setuptools wheel twine