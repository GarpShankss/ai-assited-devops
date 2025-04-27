#!/usr/bin/env python3
import ollama
import argparse
import os

PROMPT = '''
ONLY generate production-ready Kubernetes manifests and ArgoCD Application YAML for {environment}.
Include:
- Namespace
- Deployment with replicas, resource requests/limits
- Service (ClusterIP or LoadBalancer)
- ConfigMap and Secrets
- Ingress rules
- ArgoCD Application resource pointing to the Git repo
- Best practices like readiness/liveness probes
'''

def main():
    parser = argparse.ArgumentParser(description="Generate K8s manifests via Ollama LLM")
    parser.add_argument('--model', required=True, help='LLM model')
    parser.add_argument('--env', default='production', help='Target environment')
    parser.add_argument('--output', default=None, help='Output YAML path')
    args = parser.parse_args()

    out = args.output or f'k8s/{args.env}-app.yaml'
    prompt = PROMPT.format(environment=args.env)
    resp = ollama.chat(model=args.model, messages=[{'role': 'user', 'content': prompt}])
    content = resp['message']['content']

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        f.write(content)
    print(f"✅ Generated {out}")

if __name__ == '__main__':
    main()