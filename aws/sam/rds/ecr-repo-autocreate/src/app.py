import boto3

def lambda_handler(event, context):

    session = boto3.Session()

    client_ecr = session.client("ecr")

    print("Event:", str(event))

    if event["detail"]["errorCode"] == "RepositoryNotFoundException":
        try:
            ecr_response = client_ecr.describe_repositories()
            repo_name = event["detail"]["requestParameters"]["repositoryName"]
    
            print(event)

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
            error = True
            message = "Repository [{}] already exists:{}".format(repo_name,repoException)
        except Exception as exception:
            error = True
            message = "Error while creating repository [{}]: {}".format(repo_name,exception)
        else:
            return { 'message': "Repository [{}] created".format(repo_name) }


if __name__ == "__main__":
    with open('event.json') as user_file:
        json_event_contents = user_file.read()
    lambda_handler(json_event_contents,"{}")