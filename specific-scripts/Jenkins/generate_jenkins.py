#!/usr/bin/env python3
import ollama
import argparse
import os

PROMPT = '''
ONLY generate a Jenkinsfile for a CI/CD pipeline of the application in {environment}. Do not include any description
Include:
- Checkout stage
- Build and test stages
- Docker build and push stage
- Deployment stage invoking Terraform, Ansible, or Kubernetes as appropriate
- Pipeline parameters for branch, environment, and credentials
- If using Jenkins, ask whether job type is Freestyle, Pipeline, Multibranch, or Multiconfiguration and generate accordingly
- If using GitLab CI, generate a .gitlab-ci.yml pipeline instead
'''

def main():
    parser = argparse.ArgumentParser(description="Generate Jenkinsfile via Ollama LLM")
    parser.add_argument('--model', required=True, help='LLM model')
    parser.add_argument('--env', default='production', help='Target environment')
    parser.add_argument('--platform', required=True, choices=['jenkins', 'gitlab'], help='CI/CD platform (jenkins/gitlab)')
    parser.add_argument('--jobtype', default='pipeline', help='If Jenkins, specify job type (freestyle, pipeline, multibranch, multiconfiguration)')
    parser.add_argument('--output', default='Jenkinsfile', help='Output path')
    args = parser.parse_args()

    if args.platform == 'jenkins':
        prompt = PROMPT.format(environment=args.env) + f"\nJob Type: {args.jobtype}"
    else:
        prompt = PROMPT.format(environment=args.env) + "\nPlatform: GitLab CI"

    resp = ollama.chat(model=args.model, messages=[{'role': 'user', 'content': prompt}])
    content = resp['message']['content']

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(content)
    print(f"✅ Generated {args.output}")

if __name__ == '__main__':
    main()