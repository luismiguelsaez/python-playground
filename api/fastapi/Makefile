.PHONY: build test push

build:
	docker build -t fastapi:latest .

push:
	docker login -u luismiguelsaez
	docker tag fastapi:latest docker.io/luismiguelsaez/fastapi:latest
	docker push docker.io/luismiguelsaez/fastapi:latest

push-ecr:
	aws --profile <local-aws-profile> ecr get-login-password --region <aws_region> | docker login -u AWS --password-stdin https://<aws-account-id>.dkr.ecr.<aws_region>.amazonaws.com
	docker push 053497547689.dkr.ecr.eu-central-1.amazonaws.com/fastapi:latest

test:
	echo "Creating local environment ..."
	docker-compose up -d --build

	echo "Launching test commands"
	curl -XGET localhost:8000
	curl -XGET localhost:8000/list

helm-install:
	helm repo add bitnami https://charts.bitnami.com/bitnami
	helm upgrade --install mariadb bitnami/mariadb --create-namespace -n db -f helm/mariadb/values.yaml
	helm upgrade --install fastapi helm/fastapi --create-namespace -n frontend

k8s-test:
	k run test --image busybox -ti --rm -- sh -c "wget http://fastapi.frontend.svc.cluster.local/list -O-"
