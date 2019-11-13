# gds-pre-commit
This repository is here to assist GDS users in setting up pre-commit hooks that can improve the quality and security of projects hosted on GitHub.

## pre-commit framework
One of the easiest ways to get started with pre-commit hooks is by using the [pre-commit framework](https://pre-commit.com/).

### Installing pre-commit

To get started you can either run:

`$ brew install pre-commit`

or

`$ pip install pre-commit`

### Configuring pre-commit
We recommend using some of the hooks that are supported out of the box, as well as installing the [detect-secrets hook](https://github.com/Yelp/detect-secrets).

An example [.pre-commit-config.yaml file](https://github.com/alphagov/gds-pre-commit/blob/add-yaml/.pre-commit-config.yaml) used to set up your pre-commit config can be found in this repository. The .pre-commit-config.yaml file should be added to the root of your repository and committed to Github.

## detect-secrets
The detect-secrets pre-commit hook requires some minor configuration before it is run with the framework.

First you will need to install detect-secrets manually:

`$ pip install detect-secrets`

Then run the following commands in your local repository:

`$ detect-secrets scan > .secrets.baseline`

`$ detect-secrets audit .secrets.baseline`

This will create a baseline for your repository, initialising [plugins](https://github.com/Yelp/detect-secrets/tree/master/detect_secrets/plugins) used and then scan all of the files in your repository. It will ask you about potential secrets it finds and if they are to real secrets or false positives.

The newly created `.secrets.baseline` file should be committed to Github.

## Initial pre-commit execution
Once you have followed the steps above, the last steps to follow are as follows.

Run the following command to install your pre-commit hooks to git (note that this command will need to be run once locally by every one who uses your repo):

`$ pre-commit install`

Run an initial check to ensure everything is installed and working correctly:

`$ pre-commit run --all-files`

Once that's completed, you're all done! If you want to add any other hooks, take a look at the [extensive list](https://pre-commit.com/hooks.html). There are various handy linters and formatters for Go, Ruby, Python and Terraform.

## Maintaining your hooks
You can update your hooks by periodically running the following command:

`$ pre-commit autoupdate`
