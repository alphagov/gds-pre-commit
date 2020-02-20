import re
import boto3
import git


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
            "MaxResults": 10
        }
        if token:
            client_params["NextToken"] = token

        response = ssm_client.get_parameters_by_path(
            **client_params
        )
        ssm_params = ssm_params + response["Parameters"]
        if "NextToken" in response:
            token = response["NextToken"]
            has_next_page = True
        else:
            token = None
            has_next_page = False
    return ssm_params

def main():

    ssm_params = get_paged_ssm_params("/detect-secrets/example-data")
    template_file = open("template.py", "r")
    template = template_file.read()
    template_file.close()

    for param in ssm_params:
        # print(str(param))
        parents = param["Name"].split("/")
        secret_type = parents.pop()
        source = parents.pop()
        print(f"{source}: {secret_type}")
        # print(param["Value"])

        with open(f"commits/commit-{source}-{secret_type}.py", "w") as code_file:
            multi_line = param["Value"].replace("\"", "\\\"")
            single_line = param["Value"].encode('unicode_escape').decode().replace("\"", "\\\"")
            code_content = template.replace(
                "%SINGLE_LINE_VARIABLE%",
                single_line
            )
            code_content = code_content.replace(
                "%MULTI_LINE_VARIABLE%",
                multi_line
            )
            code_file.write(code_content)


if __name__ == "__main__":
    main()