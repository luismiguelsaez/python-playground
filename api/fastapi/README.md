
## Folders and files in this repository

- helm
  - Helm chart to deploy `fastapi` testing application. It is a pretty simple Helm chart
  - Values for `mariadb` Helm chart, which is used for local testing with `docker-compose`

- infra
  - Definition of AWS infrastructure with `Terragrunt`
  - A folder per AWS service
  - `helm` folder with system components to be deployed
    - In production environments, only `ArgoCD` could be deployed from here, pointing to a repository where every other component deployment is defined
    - Some components should ideally be deployed after the cluster bootstrap from `ArgoCD`

- src
  - Application source code
  - I created a simple application with `fastapi` and 3 different endpoints
    - `/` updates the database with the IP
    - `/list` retrieves every IP from the database and returns it as JSON list
    - `/health` simple endpoint for Kubernetes readiness end health probes

- Makefile
  - For local testing purposes
  - Containts some commands to be launched to, for instance, build the application image
  - Ideally these operations are done from a Jenkins pipeline

- Dockerfile
  - Simple `Dockerfile` to build the application image

- docker-compose.yaml
  - `docker-compose` file for local testing
  - Deploys the application and `mariadb` database for testing


## Infrastructure details

- I used `Terragrunt` because it simplifies the definition of resources
- Defined some local variables, but in real life environments some changes need to be made
  - Create different folder structure per environment, region, project, ...
  - Manage specific variables at folders level, like the name of the environment or the region
- Created a small local module in `infra/modules` to get the credentials `helm` provider needs to connect to the cluster
- All required IAM roles and policies are created in `iam` folder. All of them adapted to OIDC authentication in EKS
- As mentioned in the comments, here we install everything from `helm` provider, but in real life environments I would change some things
  - Deploy `ArgoCD`, pointing to a repository where all required components are defined, overridding the needed values for different environments
  - Some components requiring IAM roles for the configuration, like `external-dns` and `aws-load-balancer-controller`, are easier to deploy from `helm` provider so we can get the role ARN from outputs
  - Prometheus stack is not deployed in this case, so all `ServiceMonitor` resources are disabled in the Helm releases. Usually I tend to deploy it from `ArgoCD`
- The image is not actually being uploaded to ECR, so I keep only a placeholder in the `Makefile` to represent how it would work and I use a Docker HUB image during the deployment
- I don't have an account where I can test that the code actually works, so I am only testing Terragrunt `init` and `plan` commands

## Application details

- It is a pretty simple `fastapi` application with 3 different endpoints ( explained above in the files description )
- I used `sqlalchemy` for simplicity regarding SQL operations
- Not implemented `logging`, although it's easy to create a custom logger in case we want more details not provided from the one `fastapì` creates
- Included the database initialization in the code, although in real life it is not done that way

## Local testing

- I added a small `Makefile` to have a reference for commands executed to build and test the application
- For full application testing, I added a `docker-compose` stack, so we can check that the connection and operations against the DB works as expected
- Used `mariadb` image because there was no available `mysql` image for ARM architecture

## Helm chart

- It is a basic Helm chart with some small changes, like the addition of `env` as values

## Dockerfile

- I added some good practices, like the non-root user for the execution of the container process

