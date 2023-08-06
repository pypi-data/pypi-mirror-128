import os
import setuptools

install_requires = [
	"Click",
	"click-option-group",
	"requests",
	"markdown",
	"requests",
	"bs4",
	"matplotlib",
	"nltk",
	"numpy",
	"scikit-learn==1.0",
	"pandas",
	"textblob",
	"rdflib",
	"rdflib-jsonld",
	"xgboost",
	"validators"
]

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

def find_package_data(dirname):
    def find_paths(dirname):
        items = []
        for fname in os.listdir(dirname):
            path = os.path.join(dirname, fname)
            if os.path.isdir(path):
                items += find_paths(path)
            elif not path.endswith(".py") and not path.endswith(".pyc"):
                items.append(path)
        return items

    items = find_paths(dirname)
    return [os.path.relpath(path, dirname) for path in items]

version = {}
with open("src/somef/__init__.py") as fp:
    exec(fp.read(), version)

setuptools.setup(
    name="somef",
    version=version["__version__"],
    author="Daniel Garijo",
    author_email="daniel.garijo@upm.es",
    description="Software Metadata Extraction Framework (SOMEF)",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KnowledgeCaptureAndDiscovery/somef",
    classifiers=[
        "License :: OSI Approved :: Apache Software License",
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.9",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src", exclude=["somef.tests*"]),
    package_data={"somef": find_package_data("src/somef")},
    exclude_package_data={"somef": ["test/*"]},
    zip_safe=False,
    python_requires=">=3.9",
    entry_points={"console_scripts": ["somef = somef.__main__:cli"]},
    install_requires=install_requires,
)
