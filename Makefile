PROJECT_ID=k8s-demo-342604
BUCKET_NAME=maple_server
CONTAINER_REGISTRY_URL=asia.gcr.io/$(PROJECT_ID)/$(BUCKET_NAME)

makemigrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

.PHONY: build
build:
	docker build -t $(CONTAINER_REGISTRY_URL) .

.PHONY: push
push: build
	docker push $(CONTAINER_REGISTRY_URL)

.PHONY: deploy
deploy:
	kubectl apply -f k8s/secrets.yaml
	kubectl apply -f k8s/deployment.yaml
	kubectl apply -f k8s/service.yaml
	kubectl apply -f k8s/ingress.yaml

.PHONY: delete
delete:
	kubectl delete deployment --all

