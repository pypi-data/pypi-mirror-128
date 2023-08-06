# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['unified_range']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'unified-range',
    'version': '0.1.1',
    'description': 'Convert between semver range and maven version range',
    'long_description': "# unified-range\n\nThe library converts input semver ranges to a uniform model, and the other way around, providing objects that are easier to use programmatically.\n\n## Examples of supported ranges\n1. npm style semver - `<1.2.3 >=2.0.0`\n2. ruby style semver - `<1.2.3, >=2.0.0`\n3. maven style version ranges - `[1.2.3,2.1.1), [3.0.0,4.1.1)`\n\n\nAdditionally, use this library to run algorithms on any input version ranges and calculate whether a specific version is included in this range.\n\n\n## Prerequisites\n\n1. Ensure you have installed either pip or pipenv\n2. Install:\n   `pipenv install unified-range` or `pip install unified-range`\n\n3. Import the `api` module:\n   `from unified_range import api`\n\n## How to use\nFollowing are the different functions you can perform with this library.\n\n\n### To convert a range to the uniform string range, from the semver format:\n\n`ver_rng = api.from_semver(semver_str)`\n\nResults: uniform range structure\n\n### Convert from the uniform range structure to a semver string (return str):\n\n`semver = api.to_semver(unified_spec_str)`\n\n\n### To convert the versionrange object to a string:\n\n`version_range_str = str(ver_rng)`\n\n\n### Convert from the uniform string to the uniform model object (VersionRange objects):\n\n`ver_rng = api.unified_range(unified_spec_str)`\n\n```\n>>> api.unified_range('[1.2.3,4.5.6)')\n<unified_range.models.UnifiedVersionRange at 0x7f7e4dc17320>\n```\n\n### Within a list of ranges, retrieve versions not included:\n\n`filtered_lst = api.filter_versions(ascending_version_list, ranges)`\n```\n>>> api.filter_versions(['0.1', '0.2', '1.0', '1.1', '2.0'], ['[,0.2]', '[1.1]'])\n['1.0', '2.0']\n```\n\n\nThe versions in `ascending_version_list` should be sorted in ascending order,\nfrom oldest to newest, and contain all the versions for the package.\n\n\n### From a list of version ranges, retrieve the closest version in the list to the current version (next):\nFilter next version and maximum version from list of version and ranges:\n\n`next_version = api.next_filtered_version(current_version, ascending_version_list, ranges)`\ncurrent_version must be included in the ascending_version_list.\n```\n>>> api.next_filtered_version(current_version='0.2', ascending_version_list=['0.1', '0.2', '1.0', '1.1', '2.0'], ranges=['[,0.2]', '[1.1]'])\n'1.0'\n\n>>> api.next_filtered_version(current_version='1.1', ascending_version_list=['0.1', '0.2', '1.0', '1.1', '2.0'], ranges=['[,0.2]', '[1.1]'])\n'2.0'\n ```\n\n### Retreive the latest version that is not included:\n`max_version = api.maximum_filtered_version(ascending_version_list, ranges)`\n```\n>>> api.maximum_filtered_version(ascending_version_list=['0.1', '0.2', '1.0', '1.1', '2.0'], ranges=['[,0.2]', '[1.1]'])\n'2.0'\n ```\n\n## Uniform structure examples\n\nFollowing are the uniform structures used in this library:\n\nUniform string structure example: (,1.2.3)\n\n### Uniform model examples:\n\n`UnifiedVersionRange.constraints -> List[Restrictions]`\n\n`Restriction.bounds -> Tuple[Bound, Bound]`\n\n`Bound.version -> str`\n\n`Bound.inclusive -> boolean`\n\n\n## References and prior works\n\nThis library was built with the following:\n1. Maven’s VersionRange:\n[model](https://github.com/apache/maven/tree/master/maven-artifact/src/main/java/org/apache/maven/artifact/versioning) and [spec](https://maven.apache.org/enforcer/enforcer-rules/versionRanges.html) of maven.\n2. https://semver.org/\n3. [npm’s semver library](https://www.npmjs.com/package/semver )\n",
    'author': 'Snyk',
    'author_email': None,
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/snyk/unified-range',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
