import glob
import os
import logging
import json
from datetime import datetime
from collections import defaultdict

import boto3
import fire

import git


def get_paged_ssm_params(path):
    """ Get SSM parameters into single array from 10 item pages """
    ssm_client = boto3.client("ssm")
    has_next_page = True
    ssm_params = []
    token = None
    while has_next_page:

        client_params = {
            "Path": path,
            "Recursive": True,
            "WithDecryption": True,
            "MaxResults": 10,
        }
        if token:
            client_params["NextToken"] = token

        response = ssm_client.get_parameters_by_path(**client_params)
        ssm_params = ssm_params + response["Parameters"]
        if "NextToken" in response:
            token = response["NextToken"]
            has_next_page = True
        else:
            token = None
            has_next_page = False
    return ssm_params


class DetectChecker:
    """ Test pre-commit secret detection """

    def __init__(self):
        """ Load template file contents """
        self.log = logging.getLogger('detect-check')
        self.log.setLevel(logging.DEBUG)
        self.templates = {}
        for template in glob.glob("templates/*"):
            file_name_components = template.split("/")
            file_name = file_name_components.pop()
            template_file = open(template, "r")
            self.templates[file_name] = template_file.read()
            template_file.close()

    def _populate_templates(self, source, secret_type, value):
        """ Make a temporary python file """
        # Generate temp filename from secret type
        for template, content in self.templates.items():
            commit_file = f"commits/commit_{source}_{secret_type}_{template}"
            # Make filename match python module name conventions
            commit_file = commit_file.replace("-", "_").lower()

            with open(commit_file, "w") as code_file:
                multi_line = value.replace('"', '\\"')
                single_line = value.encode("unicode_escape").decode().replace('"', '\\"')
                code_content = content.replace("%SINGLE_LINE_VARIABLE%", single_line)
                code_content = code_content.replace("%MULTI_LINE_VARIABLE%", multi_line)
                code_file.write(code_content)

    @classmethod
    def cleanup(cls):
        """ Clean up previous run """
        for example in glob.glob("commits/*.py"):
            os.remove(example)

    def _build_commitable_temp_files(self):
        """ Iterate over secret types and populate into temp files from self.templates """
        ssm_params = get_paged_ssm_params("/detect-secrets/example-data")

        for param in ssm_params:
            parents = param["Name"].split("/")
            secret_type = parents.pop()
            source = parents.pop()
            print(f"{source}: {secret_type}")

            self._populate_templates(source, secret_type, param["Value"])

    def _load_repo(self):
        self.repo = git.repo.base.Repo("..")
        self.parent_branch = self.repo.active_branch
        print(f"Currently on branch: {self.parent_branch.name}")
        return self.repo

    def _checkout_test_branch(self):
        """ Checkout a new branch to run commit tests against """
        now = datetime.utcnow()
        timestamp = now.strftime("%Y-%m-%d_%H%M")
        self.branch_name = f"detect_test_{timestamp}"
        self.test_branch = self.repo.create_head(self.branch_name)
        self.test_branch.checkout()
        return self.test_branch

    def _delete_test_branch(self):
        """ Delete local test branch """
        self.parent_branch.checkout()
        self.repo.delete_head(self.branch_name)


    def _test_commit(self, example_file):
        """ Try committing and reset on success """
        try:
            index = self.repo.index
            index.add([f"test-detection/{example_file}"])  # add a new file to the index
            commit_message = f"Test committing {example_file}"
            index.commit(commit_message)
            self.repo.active_branch.commit = self.repo.commit('HEAD~1')
            detected = False
            self.log.error(f"Secret not detected for {example_file}")
        except git.GitCommandError as err:
            self.log.info(f"Secret detected for {example_file}: "+str(err))
            detected = True
        except FileNotFoundError as err:
            self.log.error(f"Not found error {example_file}: " + str(err))
            detected = False
        return detected

    def check(self):
        """ Run checks if AWS credentials present """
        self.cleanup()
        if "AWS_ACCESS_KEY_ID" in os.environ:
            self._load_repo()
            self._checkout_test_branch()
            print(f"Testing on branch: {self.repo.active_branch.name}")
            self._build_commitable_temp_files()
            stats = defaultdict(list)
            for example in glob.glob("commits/*.py"):
                detected = self._test_commit(example)
                category = "detected" if detected else "failed"
                stats[category].append(example)

            self._delete_test_branch()
            print(f"Reset to parent branch: {self.repo.active_branch.name}")

            print(json.dumps(stats, indent=4))

        else:
            print("No AWS credentials present. Run with AWS credentials.")


if __name__ == "__main__":
    """ Implement DetectChecker class with Fire CLI wrapper """
    fire.Fire(DetectChecker())
