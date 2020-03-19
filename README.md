## Quick Install

If you are happy with the default location, just run the following two commands to install:

The script installs the hook config to your global `git config` and reports
your registration to us. During the registration step you'll be asked for your
GitHub credentials to create an OAuth token with `read:user` and `read:org`
scopes - this allows us to verify your identity and your GitHub org membership.

```shell
git clone https://github.com/alphagov/gds-pre-commit.git ~/.gds-pre-commit/
```

```shell
~/.gds-pre-commit/install.py
```

Once you've run the above commands the pre-commit framework will be installed with the detect-secrets plugin added to its config globally for git.


## Usage

The first time you run `git commit` in a repository it will throw a warning to tell you that you need to create a secrets baseline, as shown below:

```shell
Unable to open baseline file: REPO_ROOT/.secrets.baseline
Please create it via
   detect-secrets scan > /<path-to-your-git-repo>/.secrets.baseline
```

Once you've added your secrets baseline, the first time you run `git commit` on your machine, it will install the hooks that have been added to your global config.

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


## Run your first audit

The detect-secrets tool may discover a secret in your repository that you want to exclude because it's a false positive. It may also find lots of legitimate secrets that you need to confirm.

If you receive an error message regarding your secrets baseline file, it will most likely be because you didn't follow the [usage instructions](https://github.com/alphagov/gds-pre-commit#usage) and run your first audit guidelines.

### Ensure your repo contains no secrets and ignores false positives
[Run an audit](https://github.com/Yelp/detect-secrets#auditing-a-baseline) against your `.secrets.baseline` file before your run your first commit after installation.

Once you have run a `scan` to create a `.secrets.baseline` file as mentioned in the [Usage section](https://github.com/alphagov/gds-pre-commit#usage) above, run the following command:

```shell
detect-secrets audit /<path-to-your-git-repo>/.secrets.baseline
```

False positives can also be ignored using [inline comments](https://github.com/Yelp/detect-secrets#inline-allowlisting), but running an audit is the preferred method.

### Check in your .secrets.baseline file

Once you've run your first audit of a repository, check in the `.secrets.baseline` file. This way, your colleagues/collaborators won't have to run it themselves.

Likewise, if you see a `.secrets.baseline` file has been checked into GitHub, you won't need to follow the steps in the "[Usage](https://github.com/alphagov/gds-pre-commit#usage)" and "[run your first audit](https://github.com/alphagov/gds-pre-commit#run-your-first-audit)" sections. Simply make sure you have pulled the latest changes before you commit as normal.

### Caveats

This tool is not a catch-all solution. Take some time to review a [list of secrets not detected by detect-secrets](https://github.com/Yelp/detect-secrets#things-that-wont-be-prevented).

You can also [tune the high entropy plugin](https://github.com/Yelp/detect-secrets#plugin-configuration) to your liking when the entropy detected by the Shannon formula is too high.


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
