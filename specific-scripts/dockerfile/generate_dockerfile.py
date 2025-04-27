#!/usr/bin/env python3
import ollama
import argparse
import os

PROMPT = '''
ONLY generate an ideal Dockerfile for {language} with best practices. Do not provide any description
Include:
- Base image
- Installing dependencies
- Setting working directory
- Adding source code
- Running the application
'''

def main():
    parser = argparse.ArgumentParser(description="Generate a Dockerfile via Ollama LLM")
    parser.add_argument('--model', required=True, help='LLM model (e.g. llama3.1:8b, gemini)')
    parser.add_argument('--language', required=True, help='App language (python, node, go, etc.)')
    parser.add_argument('--output', default='Dockerfile', help='Output file path')
    args = parser.parse_args()

    prompt = PROMPT.format(language=args.language)
    resp = ollama.chat(model=args.model, messages=[{'role': 'user', 'content': prompt}])
    content = resp['message']['content']

    os.makedirs(os.path.dirname(args.output) or '.', exist_ok=True)
    with open(args.output, 'w') as f:
        f.write(content)
    print(f"✅ Generated {args.output}")

if __name__ == '__main__':
    main()