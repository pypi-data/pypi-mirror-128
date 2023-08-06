# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['todoist_api_python']

package_data = \
{'': ['*']}

install_requires = \
['requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'todoist-api-python',
    'version': '1.1.0',
    'description': 'Official Python SDK for the Todoist REST API.',
    'long_description': '# Todoist API Python Client\n\nThis is the official Python API client for the Todoist REST API.\n\n### Installation\n\nThe repository can be included as a Poetry dependency in `pyproject.toml`, it is best to integrate to a release tag to ensure a stable dependency:\n\n```\n[tool.poetry.dependencies]\ntodoist-api-python = "^v1.1.0"\n```\n\n### Supported Python Versions\n\nPython 3.8 is fully supported and tested, and while it may work with other Python 3 versions, we do not test for them.\n\n### Usage\n\nAn example of initializing the API client and fetching a user\'s tasks:\n\n```python\nfrom todoist_api_python.api_async import TodoistAPIAsync\nfrom todoist_api_python.api import TodoistAPI\n\n# Fetch tasks asynchronously\nasync def get_tasks_async():\n    api = TodoistAPIAsync("YOURTOKEN")\n    try:\n        tasks = await api.get_tasks()\n        print(tasks)\n    except Exception as error:\n        print(error)\n\n# Fetch tasks synchronously\ndef get_tasks_sync():\n    api = TodoistAPI("my token")\n    try:\n        tasks = api.get_tasks()\n        print(tasks)\n    except Exception as error:\n        print(error)\n```\n\n### Documentation\n\nFor more detailed reference documentation, have a look at the [API documentation with Python examples](https://developer.todoist.com/rest/v1/?python).\n\n### Development\n\nTo install Python dependencies:\n\n```sh\n$ poetry install\n```\n\nTo install pre-commit:\n\n```sh\n$ poetry run pre-commit install\n```\n\nYou can try your changes via REPL by running:\n\n```sh\n$ poetry run python\n```\n\nYou can then import the library as describe in [Usage](#usage) without having to create a file. Keep in mind that you have to `import asyncio` and run `asyncio.run(yourmethod())` to make your async methods run as expected if you decide to use `TodoistAPIAsync`.\n\n### Releases\n\nThis API client is public, and available in a PyPI repository.\n\nA new update is automatically released by GitHub Actions, by creating a release with a tag in the format `vX.Y.Z` (`v<Major>.<Minor>.<Patch>`).\n\nUsers of the API client can then update to the new version in their `pyproject.toml` file.\n\n### Feedback\n\nAny feedback, such as bugs, questions, comments, etc. can be reported as *Issues* in this repository, and will be handled by Doist.\n\n### Contributions\n\nWe would love contributions in the form of *Pull requests* in this repository.\n',
    'author': 'Doist Developers',
    'author_email': 'dev@doist.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/Doist/todoist-api-python',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
