from setuptools import setup, find_packages

setup(
    name='falcon-error-handling',
    packages=['falcon_error_handling'],
    version='0.0.3',
    author="Develper Junio",
    author_email='developer@junio.in',
    classifiers=[
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.7',
    ],
    description="falcon error handling",
    license="MIT license",
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "marshmallow==3.13.0",
        "pyparsing==2.4.7",
        "typing-extensions==3.10.0.2",
        "falcon==3.0.1",
        "falcon-jsonify==1.2",
        "ptyprocess==0.7.0"
    ]
)
