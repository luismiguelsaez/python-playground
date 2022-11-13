import boto3
import logging
from sys import stdout

def lambda_handler(event, context):

    logger = logging.getLogger("custom")
    h_stdout = logging.StreamHandler(stdout)
    f_stdout = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    h_stdout.setFormatter(f_stdout)
    logger.addHandler(h_stdout)
    logger.setLevel(logging.DEBUG)

    session = boto3.Session()

    client_ecr = session.client("ecr")

    logger.debug("Event: {}".format(str(event)))

    if event["detail"]["errorCode"] == "RepositoryNotFoundException":
        try:
            ecr_response = client_ecr.describe_repositories()
            repo_name = event["detail"]["requestParameters"]["repositoryName"]

            if len(list(filter(lambda x: x['repositoryName'] == repo_name, ecr_response['repositories']))) > 0:
                response = client_ecr.create_repository(
                    repositoryName=repo_name,
                    tags=[
                        {
                        'Key':'auto-create',
                        'Value':'true'
                        }
                    ],
                    imageScanningConfiguration={
                        'scanOnPush': True
                    },
                    encryptionConfiguration={
                        'encryptionType': 'AES256'
                    }
                )
        except boto3.RepositoryAlreadyExistsException as repoException:
            logger.error("Repository [{}] already exists:{}".format(repo_name,repoException))
            return { 'message' : "Repository [{}] already exists:{}".format(repo_name,repoException) }
        except Exception as exception:
            logger.error("Error while creating repository [{}]: {}")
            return { 'message' : "Error while creating repository [{}]: {}".format(repo_name,exception) }
        else:
            logger.info("Repository [{}] created".format(repo_name))
            return { 'message': "Repository [{}] created".format(repo_name) }


if __name__ == "__main__":
    with open('event.json') as user_file:
        json_event_contents = user_file.read()
    lambda_handler(json_event_contents,"{}")