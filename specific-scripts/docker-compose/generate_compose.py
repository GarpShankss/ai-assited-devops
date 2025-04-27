#!/usr/bin/env python3
import ollama
import argparse
import os

PROMPT = '''
ONLY generate a production-ready docker-compose.yml for {language} application in {environment}. Do not include any description
Include:
- Service for the app (build from local Dockerfile)
- Common additional services (e.g., database)
- Volumes and networks
- Environment variables and secrets support
- Best practices for production mode
'''

def main():
    parser = argparse.ArgumentParser(description="Generate docker-compose.yml via Ollama LLM")
    parser.add_argument('--model', required=True, help='LLM model (e.g. llama3.1:8b, gemini)')
    parser.add_argument('--language', required=True, help='App language (python, node, go, etc.)')
    parser.add_argument('--env', default='production', help='Target environment')
    parser.add_argument('--output', default='docker-compose.yml', help='Output path')
    args = parser.parse_args()

    prompt = PROMPT.format(language=args.language, environment=args.env)
    resp = ollama.chat(model=args.model, messages=[{'role': 'user', 'content': prompt}])
    content = resp['message']['content']

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(content)
    print(f"✅ Generated {args.output}")

if __name__ == '__main__':
    main()