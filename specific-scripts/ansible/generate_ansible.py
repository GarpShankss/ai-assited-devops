#!/usr/bin/env python3
import ollama
import argparse
import os

PROMPT = '''
ONLY generate an Ansible playbook for deploying the application in {environment}.
Include:
- Hosts and inventory pattern
- Tasks for installing dependencies
- Deploying code
- Configuring services
- Starting the application
- Idempotency and handlers
'''

def main():
    parser = argparse.ArgumentParser(description="Generate Ansible playbook via Ollama LLM")
    parser.add_argument('--model', required=True, help='LLM model')
    parser.add_argument('--env', default='production', help='Target environment')
    parser.add_argument('--output', default=None, help='Output YAML path')
    args = parser.parse_args()

    out = args.output or f'ansible/{args.env}.yml'
    prompt = PROMPT.format(environment=args.env)
    resp = ollama.chat(model=args.model, messages=[{'role': 'user', 'content': prompt}])
    content = resp['message']['content']

    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'w') as f:
        f.write(content)
    print(f"✅ Generated {out}")

if __name__ == '__main__':
    main()