import ollama
import os
import argparse

# Define templates for each artifact
TEMPLATES = {
    'dockerfile': '''
ONLY generate an ideal Dockerfile for {docker_language} with best practices. Do not provide any description
Include:
- Base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
''',
    'docker_compose': '''
ONLY generate a production-ready docker-compose.yml for {docker_language} application in {environment}. Do not include any description
Include:
- Service for the app (build from local Dockerfile)
- Common additional services (e.g., database)
- Volumes and networks
- Environment variables and secrets support
- Best practices for production mode
''',
    'terraform': '''
ONLY generate a production-ready Terraform script for provisioning AWS infrastructure in {environment}.
Include:
- AWS provider configuration
- VPC, subnets, security groups
- EC2 instances with EBS volumes (specify size and type)
- Variable definitions and defaults
- Outputs
- Best practices like state backend and tagging
''',
    'ansible': '''
ONLY generate an Ansible playbook for deploying the application in {environment}.
Include:
- Hosts and inventory pattern
- Tasks for installing dependencies
- Deploying code
- Configuring services
- Starting the application
- Idempotency and handlers
''',
    'kubernetes': '''
ONLY generate production-ready Kubernetes manifests and ArgoCD Application YAML for {environment}.
Include:
- Namespace
- Deployment with replicas, resource requests/limits
- Service (ClusterIP or LoadBalancer)
- ConfigMap and Secrets
- Ingress rules
- ArgoCD Application resource pointing to the Git repo
- Best practices like readiness/liveness probes
''',
    'jenkinsfile': '''
ONLY generate a Jenkinsfile for a CI/CD pipeline of the {docker_language} application in {environment}. Do not include any description
Include:
- Checkout stage
- Build and test stages
- Docker build and push stage
- Deployment stage invoking Terraform, Ansible, or Kubernetes as appropriate
- Pipeline parameters for branch, environment, and credentials
''',
    'readme': '''
# Infrastructure & App Scaffold

This repository includes generated artifacts for:
- Dockerfile
- Docker Compose
- Terraform scripts
- Ansible playbook
- Kubernetes manifests (deployed via ArgoCD)
- Jenkinsfile

## Requirements
- ollama CLI
- Gemini or any supported LLM model (e.g., llama3.1:8b)
- AWS credentials (for Terraform)
- Docker / Docker Compose
- Jenkins for CI/CD
- kubectl and ArgoCD CLI

## Setup
1. Install dependencies:
   ```sh
   pip install ollama
   ```
2. Clone and change into the repo:
   ```sh
   git clone <repo-url> && cd <repo-dir>
   ```
3. Generate artifacts (replace <model> as needed):
   ```sh
   python generate_infra_scripts.py --model llama3.1:8b \
       --app-language python --docker-language node \
       --env staging
   ```
4. Review & apply artifacts:
   - Docker: `docker build -t app .`
   - Docker Compose: `docker-compose up -d`
   - Terraform: `terraform init && terraform apply`
   - Ansible: `ansible-playbook -i inventory staging.yml`
   - Kubernetes: `kubectl apply -f k8s/`
   - ArgoCD: `argocd app sync <app-name>`
   - Jenkins: configure pipeline pointing to Jenkinsfile
'''
}


def generate_artifact(artifact, model, **kwargs):
    prompt = TEMPLATES[artifact].format(**kwargs)
    response = ollama.chat(model=model, messages=[{'role': 'user', 'content': prompt}])
    return response['message']['content']


def save_file(path, content):
    os.makedirs(os.path.dirname(path) or '.', exist_ok=True)
    with open(path, 'w') as f:
        f.write(content)
    print(f"Written {path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Dockerfile, Docker Compose, Terraform, Ansible, Kubernetes, Jenkinsfile, and README using Ollama models."
    )
    parser.add_argument('--model', required=True, help='LLM model to use (e.g., llama3.1:8b, gemini)')
    parser.add_argument('--app-language', required=True, help='Application language (e.g., python, node)')
    parser.add_argument('--docker-language', help='Language for Dockerfile (defaults to app language)')
    parser.add_argument('--env', default='production', help='Target environment (e.g., staging, production)')
    args = parser.parse_args()

    docker_lang = args.docker_language or args.app_language

    # Artifacts to generate
    artifacts = [
        'dockerfile', 'docker_compose', 'terraform',
        'ansible', 'kubernetes', 'jenkinsfile', 'readme'
    ]

    for art in artifacts:
        content = generate_artifact(
            art,
            args.model,
            app_language=args.app_language,
            docker_language=docker_lang,
            environment=args.env
        )
        filename = {
            'dockerfile': 'Dockerfile',
            'docker_compose': 'docker-compose.yml',
            'terraform': f'terraform/{args.env}.tf',
            'ansible': f'ansible/{args.env}.yml',
            'kubernetes': f'k8s/{args.env}-app.yaml',
            'jenkinsfile': 'Jenkinsfile',
            'readme': 'README.md'
        }[art]
        save_file(filename, content)

if __name__ == '__main__':
    main()
