import glob
import os

import boto3
import fire

# import git


def get_paged_ssm_params(path):
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

    @classmethod
    def cleanup(cls):
        """ Clean up previous run """
        for example in glob.glob("commits/*.py"):
            os.remove(example)

    @classmethod
    def check(cls):
        """ Run checks if AWS credentials present """
        if "AWS_ACCESS_KEY_ID" in os.environ:
            ssm_params = get_paged_ssm_params("/detect-secrets/example-data")
            template_file = open("templates/template.py", "r")
            template = template_file.read()
            template_file.close()

            # clean up previous run
            for example in glob.glob("commits/*.py"):
                os.remove(example)

            for param in ssm_params:
                parents = param["Name"].split("/")
                secret_type = parents.pop()
                source = parents.pop()
                print(f"{source}: {secret_type}")

                commit_file = f"commits/commit_{source}_{secret_type}.py"
                commit_file = commit_file.replace("-", "_").to_lower_case()

                with open(commit_file, "w") as code_file:
                    multi_line = param["Value"].replace('"', '\\"')
                    single_line = (
                        param["Value"]
                        .encode("unicode_escape")
                        .decode()
                        .replace('"', '\\"')
                    )
                    code_content = template.replace(
                        "%SINGLE_LINE_VARIABLE%", single_line
                    )
                    code_content = code_content.replace(
                        "%MULTI_LINE_VARIABLE%", multi_line
                    )
                    code_file.write(code_content)
        else:
            print("No AWS credentials present. Run with AWS credentials.")


if __name__ == "__main__":

    fire.Fire(DetectChecker)
