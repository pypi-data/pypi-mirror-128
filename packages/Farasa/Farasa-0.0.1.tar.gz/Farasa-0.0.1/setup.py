import setuptools
import sys
from os import path


this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

INSTALL_REQUIRES = []
EXTRAS_REQUIRE = {}

if int(setuptools.__version__.split(".", 1)[0]) < 18:
    if sys.version_info[0:2] < (3, 7):
        INSTALL_REQUIRES.append("importlib_resources")
else:
    EXTRAS_REQUIRE[":python_version<'3.7'"] = ["importlib_resources"]


setuptools.setup(
    name='Farasa',
    version='0.0.1',
    url='https://github.com/disooqi/PyFarasa',
    author='Mohamed Eldesouki',
    author_email='mohamed@eldesouki.com',
    description='Farasa segmenter implemented in pure Python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    package_dir={"": "src"},
    python_requires='>=3.6',
    packages=setuptools.find_packages(where="src", exclude=['docs', 'tests']),

    # include everything in source control data files must be specified via the distutils’ MANIFEST.in file.
    # include_package_data will nullify the package_data information.
    # include_package_data=True,
    # exclude_package_data={"": ["README.txt"]},  # ...but exclude these from all packages
    package_data={
        # include *.txt files of any package: "": ["*.txt"],
        # include any * files under "pickles" subdirectory of the "farasa" package, also:
        'farasa': ['pickles/*']
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Linguistic",
        "Natural Language :: Arabic",
        "Natural Language :: English",
        "License :: OSI Approved :: Academic Free License (AFL)"
    ],

)
