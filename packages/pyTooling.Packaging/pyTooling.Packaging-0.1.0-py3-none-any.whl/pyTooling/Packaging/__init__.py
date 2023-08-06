# =============================================================================
#             _____           _ _               ____            _               _
#  _ __  _   |_   _|__   ___ | (_)_ __   __ _  |  _ \ __ _  ___| | ____ _  __ _(_)_ __   __ _
# | '_ \| | | || |/ _ \ / _ \| | | '_ \ / _` | | |_) / _` |/ __| |/ / _` |/ _` | | '_ \ / _` |
# | |_) | |_| || | (_) | (_) | | | | | | (_| |_|  __/ (_| | (__|   < (_| | (_| | | | | | (_| |
# | .__/ \__, ||_|\___/ \___/|_|_|_| |_|\__, (_)_|   \__,_|\___|_|\_\__,_|\__, |_|_| |_|\__, |
# |_|    |___/                          |___/                             |___/         |___/
# =============================================================================
# Authors:            Patrick Lehmann
#
# Python package:     A set of helper functions to describe a Python package for setuptools.
#
# License:
# ============================================================================
# Copyright 2021-2021 Patrick Lehmann - Bötzingen, Germany
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#		http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# SPDX-License-Identifier: Apache-2.0
# ============================================================================
#
from ast        import parse as ast_parse, iter_child_nodes, Assign, Constant, Name
from pathlib    import Path
from setuptools import (
	setup as setuptools_setup,
	find_namespace_packages as setuptools_find_namespace_packages
)
from typing import Tuple, List, Iterable, Dict

from pyTooling.Decorators   import export


__author__ =    "Patrick Lehmann"
__email__ =     "Paebbels@gmail.com"
__copyright__ = "2021-2021, Patrick Lehmann"
__license__ =   "Apache License, Version 2.0"
__version__ =   "0.1.0"


# Read README for upload to PyPI
def loadReadmeFile(readmeFile: Path) -> Tuple[str, str]:
	if readmeFile.suffix == ".md":
		readmeContentType = "text/markdown"
		with readmeFile.open("r") as file:
			readmeContent = file.read()
	else:
		raise ValueError("Unsupported README format.")

	return (readmeContent, readmeContentType)


# Read requirements file and add them to package dependency list
def loadRequirementsFile(requirementsFile: Path) -> List[str]:
	with requirementsFile.open("r") as file:
		requirements = [line for line in file.readlines()]

	return requirements


# Read __version__ from source file
def extractVersionInformation(sourceFile: Path) -> Tuple[str, str, str]:
	author =  None
	email =   None
	version = None

	with sourceFile.open("r") as file:
		for item in iter_child_nodes(ast_parse(file.read())):
			if isinstance(item, Assign) and len(item.targets) == 1:
				target = item.targets[0]
				value = item.value
				if isinstance(target, Name) and target.id == "__author__" and isinstance(value, Constant) and isinstance(value.value, str):
					author = value.value
				if isinstance(target, Name) and target.id == "__email__" and isinstance(value, Constant) and isinstance(value.value, str):
					email = value.value
				if isinstance(target, Name) and target.id == "__version__" and isinstance(value, Constant) and isinstance(value.value, str):
					version = value.value

	if author is None:
		raise AssertionError(f"Could not extract '__author__' from '{sourceFile}'.")
	if email is None:
		raise AssertionError(f"Could not extract '__email__' from '{sourceFile}'.")
	if version is None:
		raise AssertionError(f"Could not extract '__version__' from '{sourceFile}'.")

	return (author, email, version)

LICENSES: Dict[str, str] = {
	"Apache 2.0": "License :: OSI Approved :: Apache Software License"
}

STATUS: Dict[str, str] = {
	"alpha":  "Development Status :: 3 - Alpha",
	"beta":   "Development Status :: 4 - Beta",
	"stable": "Development Status :: 5 - Production/Stable"
}

@export
def DescribePythonPackage(
	packageName: str,
	description: str,
	keywords: str,
	projectURL: str,
	sourceCodeURL: str,
	documentationURL: str,
	issueTrackerCodeURL: str,
	license: str = "Apache 2.0",
	readmeFile: Path = Path("README.md"),
	requirementsFile: Path = Path("requirements.txt"),
	sourceFileWithVersion: Path = Path("__init__.py"),
	classifiers: Iterable[str] = (
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Topic :: Utilities"
	),
	developmentStatus: str = "stable",
	pythonVersions: Iterable[str] = ("3.6", "3.7", "3.8", "3.9", "3.10")
) -> None:
	# Read README for upload to PyPI
	(readmeContent, readmeContentType) = loadReadmeFile(readmeFile)

	# Read requirements file and add them to package dependency list
	requirements = loadRequirementsFile(requirementsFile)

	# Read __author__, __email__, __version__ from source file
	(author, email, version) = extractVersionInformation(sourceFileWithVersion)

	# Scan for packages and source files
	packages = setuptools_find_namespace_packages(exclude=["doc", "doc.*", "tests", "tests.*"])

	# Assemble classifiers
	classifiers = list(classifiers)

	# Translate license to classifier
	try:
		classifiers.append(LICENSES[license])
	except KeyError:
		raise ValueError(f"Unsupported license '{license}'.")

	# Translate Python versions to classifiers
	classifiers.append("Programming Language :: Python :: 3 :: Only")
	for v in pythonVersions:
		classifiers.append(f"Programming Language :: Python :: {v}")

	# Translate status to classifier
	try:
		classifiers.append(STATUS[developmentStatus])
	except KeyError:
		raise ValueError(f"Unsupported development status '{developmentStatus}'.")

	# Assemble all package information
	parameters = {
		"name": packageName,
		"version": version,
		"author": author,
		"author_email": email,
		"license": license,
		"description": description,
		"long_description": readmeContent,
		"long_description_content_type": readmeContentType,
		"url": projectURL,
		"project_urls": {
			'Documentation': documentationURL,
			'Source Code':   sourceCodeURL,
			'Issue Tracker': issueTrackerCodeURL
		},
		"packages": packages,
		"classifiers": classifiers,
		"keywords": keywords,
		"python_requires": f">={pythonVersions[0]}",
	  "install_requires": requirements,
	}

	setuptools_setup(**parameters)

@export
def DescribePythonPackageHostedOnGitHub(
	packageName: str,
	description: str,
	keywords: str,
	gitHubNamespace: str,
	gitHubRepository: str = None,
	projectURL: str = None,
	license: str = "Apache 2.0",
	readmeFile: Path = Path("README.md"),
	requirementsFile: Path = Path("requirements.txt"),
	sourceFileWithVersion: Path = Path("__init__.py"),
	classifiers: Iterable[str] = (
		"Operating System :: OS Independent",
		"Intended Audience :: Developers",
		"Topic :: Utilities"
	),
	developmentStatus: str = "stable",
	pythonVersions: Iterable[str] = ("3.6", "3.7", "3.8", "3.9", "3.10")
):
	gitHubRepository = gitHubRepository if gitHubRepository is not None else packageName

	# Derive URLs
	sourceCodeURL = f"https://GitHub.com/{gitHubNamespace}/{gitHubRepository}"
	documentationURL = f"https://{gitHubNamespace}.GitHub.io/{gitHubRepository}"
	issueTrackerCodeURL = f"{sourceCodeURL}/issues"

	projectURL = projectURL if projectURL is not None else sourceCodeURL

	DescribePythonPackage(
		packageName=packageName,
		description=description,
		keywords=keywords,
		projectURL=projectURL,
		sourceCodeURL=sourceCodeURL,
		documentationURL=documentationURL,
		issueTrackerCodeURL=issueTrackerCodeURL,
		license=license,
		readmeFile=readmeFile,
		requirementsFile=requirementsFile,
		sourceFileWithVersion=sourceFileWithVersion,
		classifiers=classifiers,
		developmentStatus=developmentStatus,
		pythonVersions=pythonVersions
	)
