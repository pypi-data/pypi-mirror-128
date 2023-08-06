import setuptools

setuptools.setup(
    name="picompress",
    version="2.0.8",
    description="python compression lib",
    packages=['picompress'],
    package_data={'picompress': ['so/*']},
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
)

