build:
	cd app && docker build -t slack-bot-wizard:latest .

load:
	minikube image load slack-bot-wizard:latest

deploy:
	kubectl apply -f k8s/namespace.yaml
	kubectl create secret generic -n slack-bot-wizard slack-secrets --from-literal=app-token=${SLACK_APP_TOKEN} --from-literal=bot-token=${SLACK_BOT_TOKEN}
	kubectl apply -f k8s/

destroy:
	kubectl delete namespace slack-bot-wizard

logs-app:
	kubectl logs -n slack-bot-wizard deploy/wizard-bot -f

port-forward:
	kubectl port-forward -n slack-bot-wizard svc/ollama-api-service 8080:8080
