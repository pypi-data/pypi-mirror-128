import pathlib
import setuptools

HERE = pathlib.Path(__file__).parent
print(HERE)
LONG_DESCRIPTION = (HERE / "pypi.md").read_text()
print(LONG_DESCRIPTION)
REQUIREMENTS = [
    'Flask>=2.0.2',
    'pycountry>=20.7.3',
    'pymongo>=3.12.1',
    'cloup>=0.12.1',
    'deepdiff>=5.6.0',
    'Flask-Babel>=2.0.0',
]

setuptools.setup(
    name="elemental-cms",
    version="1.0.60",
    author="Paranoid Software",
    author_email="info@paranoid.software",
    license="MIT",
    description="Flask and MongoDB CMS for developers first.",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url='https://github.com/paranoid-software/elemental-cms',
    packages=setuptools.find_packages(exclude=['tests']),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    include_package_data=True,
    python_requires='>=3.6',
    scripts=['elementalcms/bin/elemental-cms'],
)
