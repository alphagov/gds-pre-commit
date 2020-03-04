## Quick Install

```shell
git clone https://github.com/alphagov/gds-pre-commit.git ~/.gds-pre-commit/
~/.gds-pre-commit/install.py
```
Once you've run the above commands the pre-commit framework will be installed with the detect-secrets plugin added to it's config globally for git. The first time you run `git commit` **in a repository** will throw a warning to tell you that you need to create a secrets baseline, as shown below:

```shell
Unable to open baseline file: REPO_ROOT/.secrets.baseline
Please create it via
   detect-secrets scan > $HOME/<your-git-repo>/.secrets.baseline
```

Once you've added your secrets baseline, the first time you run `git commit` **on your machine**, will install the hooks that have been added to your global config.

It will look something like this:

```shell
[INFO] Installing environment for https://github.com/pre-commit/pre-commit-hooks.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
[INFO] Installing environment for git@github.com:Yelp/detect-secrets.
[INFO] Once installed this environment will be reused.
[INFO] This may take a few minutes...
Detect Private Key.......................................................Passed
Detect secrets...........................................................Passed
```



# gds-pre-commit
This repository is here to assist GDS users in setting up pre-commit hooks that can improve the quality and security of projects hosted on GitHub.

## Secrets
One of the main motivations for using pre-commit hooks is to prevent secrets being pushed to GitHub repositories. When we say secrets we mean things like private keys, API tokens, SSH keys, AWS keys or Slack keys. All of these 'secrets' are used to authenticate or authorise users to services we use or own and would be beneficial for an attacker to steal.

The detect-secrets tool was tested against AWS keys, a private SSH key and a random hash with the tool successfully catching them all, however pre-commit hooks should not be used as a catch-all solution and users should ensure they are following Secure Software Development Lifecycles.

## pre-commit framework
One of the easiest ways to get started with pre-commit hooks is by using the [pre-commit framework](https://pre-commit.com/).

Read on for step-by-step instruction:

### Installing pre-commit manually
#### Please note that the quick install section at the top will run these commands globally

To get started you can either run:

`$ brew install pre-commit`

or

`$ pip3 install pre-commit`

## detect-secrets
The detect-secrets pre-commit hook requires some initialisation before it is run with the framework.

First you will need to install detect-secrets system-wide:

`$ pip3 install detect-secrets`

Then run the following commands in your local repository:

`$ detect-secrets scan > .secrets.baseline`

`$ detect-secrets audit .secrets.baseline`

This will create a baseline for your repository, initialising [plugins](https://github.com/Yelp/detect-secrets/tree/master/detect_secrets/plugins) used and then scan all of the files in your repository. It will ask you about potential secrets it finds and if they are to real secrets or false positives.

The newly created `.secrets.baseline` file should be committed to Github.


Once that's completed, you're all done! If you want to add any other hooks, take a look at the [extensive list](https://pre-commit.com/hooks.html). There are various handy linters and formatters for Go, Ruby, Python and Terraform.

## Supported editors
This pre-commit hook has been tested and is working with the following editors:

* Atom
* VScode
* IntelliJ
* Pycharm
* Emacs
* Vim (with Fugitive.vim)

## Other useful hooks/plugins

**Please note that these hooks are found on the pre-commit website but have not all been tested**

[github.com/pre-commit/pre-commit-hooks](https://github.com/pre-commit/pre-commit-hooks)

* `check-json`
* `check-xml`
* `check-yaml`
* `pretty-format-json`
* `check-merge-conflict`
* `flake8`

### Python hooks
[github.com/pre-commit/pygrep-hooks](https://github.com/pre-commit/pygrep-hooks)

* `python-check-blanket-noqa`
* `python-no-eval`

[github.com/PyCQA/bandit](https://github.com/PyCQA/bandit)

* `bandit`


### Ruby hooks
[github.com/chriskuehl/puppet-pre-commit-hooks](https://github.com/chriskuehl/puppet-pre-commit-hooks)

* `epp-validate`
* `erb-validate`
* `puppet-lint`
* `ruby-validate`

[github.com/mattlqx/pre-commit-ruby](https://github.com/mattlqx/pre-commit-ruby)

* `rubocop`
* `rspec`

### Go hooks
[github.com/golangci/golangci-lint](https://github.com/golangci/golangci-lint)

* `golangci-lint`

[github.com/dnephin/pre-commit-golang](https://github.com/dnephin/pre-commit-golang)

* `go-fmt`
* `go-unit-tests`


### Terraform hooks
[github.com/antonbabenko/pre-commit-terraform](https://github.com/antonbabenko/pre-commit-terraform)

* `terraform_fmt`
* `terraform_tflint`

### Miscellaneous

[github.com/jumanjihouse/pre-commit-hooks](https://github.com/jumanjihouse/pre-commit-hooks)

* `bundler-audit`
* `fasterer`
* `rubocop`

[github.com/Lucas-C/pre-commit-hooks-go](https://github.com/Lucas-C/pre-commit-hooks-go)

* `checkmake`

[github.com/Lucas-C/pre-commit-hooks-java](https://github.com/Lucas-C/pre-commit-hooks-java)

* `validate-html`

[github.com/IamTheFij/docker-pre-commit](https://github.com/IamTheFij/docker-pre-commit)

* `docker-compose-check`
