# gds-pre-commit
This repository is here to assist GDS users in setting up pre-commit hooks that can improve the quality and security of projects hosted on GitHub.

## pre-commit framework
One of the easiest ways to get started with pre-commit hooks is by using the [pre-commit framework](https://pre-commit.com/).

### Installing pre-commit

To get started you can either run:

`brew install pre-commit` (on Mac)

or

`pip install pre-commit` (on Linux or Mac)

### Configuring pre-commit
We recommend using some of the plugins that come with the framework, as well as installing the [detect-secrets plugin](https://github.com/Yelp/detect-secrets).

An example [.pre-commit-config.yaml file](https://github.com/alphagov/gds-pre-commit/blob/add-yaml/.pre-commit-config.yaml) used to set up your pre-commit config can be found in this repository.
