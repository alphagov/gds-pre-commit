# Test secret detection

We have a pre-commit hook config which detects a number of common secret types. 

We need to test this against the types of secrets we use to ensure it detects 
them successfully. 

## Run the tests 

GitPython doesn't work with the global pre-commit config so you 
have to install it locally. 

### Remove from my global config
```
git config --global --unset core.hookspath
```
### Install pre-commit locally
```   
pre-commit install -c .gds/.pre-commit-config.yaml
``` 
### Re-enable global config
```
git config --global core.hookspath /path/to/gds-pre-commit/global_install/hooks
```
### Run the detection test
``` 
[with aws-vault or gds-cli] -- make run 
```

## How it works 

1. We store a collection of example secrets in SSM under a common path: 

    ```
    /detect-secrets/example-data/[source]/[secret-type]
    # eg 
    /detect-secrets/example-data/rsa/private-key
    /detect-secrets/example-data/aws/secret-access-key
    /detect-secrets/example-data/google/console-credentials-file
    ```

2. We do a `get-parameters-by-path --recursive` to get all the example 
secrets in a single request

3. We iterate through each secret creating a file with the secret hard-coded 
as a variable. 

4. We try to commit the file using GitPython 

5. We log success / failure 

6. We unstage the file or `git reset HEAD^` if the commit was successful

## Next steps 

The results are definitely not 100% correct compared to observed 
behaviour in other repos. 

For example things like the random_string secrets and slack hooks 
have been successfully detected elsewhere and are not being 
detected in these tests. 

In creating fake secrets we may have removed too much randomness
from the data. 