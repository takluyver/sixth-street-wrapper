## Build / Publishing

`pyproject.yaml` is used to configure the project and Flit to simplify the build process and publish to PyPI (either test or production servers).

Run: `flit -h` to see options.
or `flit build`

or for local development: `flit install [--symlink] [--python path/to/python]`

To publish to test pypi `flit publish --pypirc ./.pypirc --repository testpypi`

## Installation

Instal into your Python project using the tools you are familiar with and consistent with the package installation you are using for other dependencies.

### Usage Example

Stocker can be used generally in two different ways:

1. If you will be making more than one request for the same symbol, you may wish to initialize the library with the Alpha Vantage Api key and the symbol you plan to work with.

Then your calls to `lookup`, `min`, `max` are simplified to focus on the parameters that are relevant to that function:

```python
msftStocker = stocker.Stocker("YOUR_ALPHAVANTAGE_API_KEY", "MSFT")
result = msftStocker.lookup("2023-09-01")
print(result)
# prints: {'1. open': '331.3100', '2. high': '331.9900', '3. low': '326.7800', '4. close': '328.6600', '5. volume': '14942024'}

min5 = msftStocker.min(5)
print(min5)
# prints: 281.96

max5 = msftStocker.max(5)
print(max5)
# prints: 331.99
```

2. If you will not be focusing on a particular symbol, initialize with only the api key:

```python
st = stocker.Stocker("YOUR_ALPHAVANTAGE_API_KEY").lookup("2023-09-01", "MSFT")
print(result)
# prints: {'1. open': '331.3100', '2. high': '331.9900', '3. low': '326.7800', '4. close': '328.6600', '5. volume': '14942024'}
```

### Discussion

As with any new tool that is introduced to a team of people, there are technical and soft constraints to consider. Care needs to be taken that the folks are on board and interested in augmenting their workflow. This could be because the tool is a breeze to set up and has zero onboarding (great!), or because the existing process has problems that are worse than the initial investment in updating their toolset/processes or because the Org is ready to grow and the current ways of operating aren't scaling well (think about onboarding experience while scaling up the team, the ability for security to effectively do their job, or leadership being go after some new business goal).

Without having much information about the existing tools and familiarity or some of the incentives the team and or management is experiencing, it's difficult to say with much certainty what a good first step towards the ultimate goal would be. That being said, with the time constraints I have and my python being rusty, I have documented some of the ways we could approach building libraries. I have started with a python template provided by Microsoft to jump start this project. Template can be found here: https://github.com/microsoft/python-package-template. This template has many useful features that are mentioned more in depth at the source linked - some of which I believe most python folks are already using (like Black) and some that could be new and potentially disruptive (working in vscode .devcontainer dockerized environment).

### Compromises

- I would like to research more in depth most things in python and be more knowledgeable about different options for example private package managers, or the standard that python uses for libraries. Somewhat
- Similarly, I'm not familiar with python mocking and testing so no tests have been written. I simply used `python3 __main__.py` to check the code worked and that's not a great experience long term.
- All the code is in one file - 3 methods are simple enough that they don't need to be broken out, but further thought needs to be made for more use cases (40 methods, more providers than alpha vantage, etc)
- Without knowing the specifics around the use cases, I would like to add in caching for the api requests to be faster, possibly reducing costs from using the alpha vantage API.
- Caching the api requests would also help ensure the data was sorted only once the first time we fetched it rather than each api request.
- Depending on use cases if multiple libraries are written for each provider or if this wrapper only supports alpha vantage, it would be interesting to see if there should be a unified sixth street wrapper that fetches and combines data from multiple sources into one output.
- The error handling is non-existent. If something is not configured with the api correctly, the user will have a very hard time figuring that out. If a request failed for some reason, that error response is not being forwarded along to give some guidance as to what could fix the request (for example rate limiting, or missing api key)
- There is no way to set the function we are using for Alpha Vantage - this is hard coded to "Time Series (Daily)".

#### Library Versioning Approach

Assuming I have buy in from the folks maintaining the library, myself or otherwise, I would automate release versioning based on semantic commits. [Pythong Semantic Release](https://python-semantic-release.readthedocs.io/en/latest/) appears to be an open source project that meets the needs. For the unfamiliar, this works to automate the versioning of the library by reading in the commits (semantic commits) and if there are any that trigger certain rules, the version is updated and a 'release' can be created in the version control system.

#### Service vs Library

If this were going to be a service rather than a library there would be many more concerns around:

- hosting
- security (authentication), who is allowed to use our api
- is python the best framework for this service, the language is not as important to the users if it's not a library anymore.
- the initialization and passing in of API keys would no longer be necessary by users, but a framework would need to be added to handle routing, startup execution, possibly a database, redis for caching, etc.
- retrieving data from multiple data sources and combining would be much easier since users can remain unaware of where the data is coming from
- caching and sharing amongst all users would be easier and enable polling to update the data
- outages at Alpha Vantage would be less impactful to our users if we had cached data

### Time

Hours upon hours were spent researching python in general, library specifications, and tools that folks use commonly. Eventually I found the microsoft template and offloaded most of the decision making to the folks that created that template which seems to be a safe choice for now. Writing the actual functions after doing research was pretty quick, possibly an hour and this writeup was probably at half hour, but was good to organize my thoughts.

I did publish to pypi and test pypi while following a tutorial so that is possible and straightforward using flit, but I have not done it again for this repository and would have liked to.

### General Feedback

It was fun and interesting creating a python library. Dependency management seems vitally important. At times I took a shortcut and just installed packages globally, which is a bad idea. I am curious to see the usual workflow for engineers/data scientists that would be using this library (or one similar). What they are used to doing, and how they might contribute effectively to a new library and have a pleasant experience.

There are so many competing tools in python that it was difficult to pick which was best.

## Project Organization

- `.github/workflows`: Contains GitHub Actions used for building, testing, and publishing.
- `.devcontainer/Dockerfile`: Contains Dockerfile to build a development container for VSCode with all the necessary extensions for Python development installed.
- `.devcontainer/devcontainer.json`: Contains the configuration for the development container for VSCode, including the Docker image to use, any additional VSCode extensions to install, and whether or not to mount the project directory into the container.
- `.vscode/settings.json`: Contains VSCode settings specific to the project, such as the Python interpreter to use and the maximum line length for auto-formatting.
- `src`: Contains the functionality of the stocker library that encapsulates the fetching of stock quotes
- `tests`: (TODO:) Contains Python-based test cases to validate source code. Currently simply a placeholder.
- `pyproject.toml`: Contains metadata about the project and configurations for additional tools used to format, lint, type-check, and analyze Python code.

### Additional Info About This Template and Configurations

### `pyproject.toml`

The pyproject.toml file is a centralized configuration file for modern Python projects. It streamlines the development process by managing project metadata, dependencies, and development tool configurations in a single, structured file. This approach ensures consistency and maintainability, simplifying project setup and enabling developers to focus on writing quality code. Key components include project metadata, required and optional dependencies, development tool configurations (e.g., linters, formatters, and test runners), and build system specifications.

In this particular pyproject.toml file, the [build-system] section specifies that the Flit package should be used to build the project. The [project] section provides metadata about the project, such as the name, description, authors, and classifiers. The [project.optional-dependencies] section lists optional dependencies, like pyspark, while the [project.urls] section supplies URLs for project documentation, source code, and issue tracking.

The file also contains various configuration sections for different tools, including bandit, black, coverage, flake8, pyright, pytest, tox, and pylint. These sections specify settings for each tool, such as the maximum line length for flake8 and the minimum code coverage percentage for coverage.
