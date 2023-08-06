from setuptools import setup, find_packages

setup(
    name='falcon-error-handling',
    packages=['falcon_error_handling'],
    version='0.0.6',
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
        "typing-extensions==3.10.0.2",
        "falcon==3.0.0",
        "ptyprocess==0.7.0"
    ]
)
