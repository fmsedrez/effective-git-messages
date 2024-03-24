#! /usr/bin/python

import os
import google.generativeai as genai

MAIN_PROMPT = """
    Usando uma linguagem simples e eficiente escreva o titulo e a descrição do merge.
    Na descrição coloque um texto geral e depois agrupe as alterações classificando por tipo de commit explicando o que mudou o e impacto.
    Se necessário inclua observações e links válidos de referencia para enriquecer as explicações.
    Adicione sugestões de açõess para o revisor as mudanças.
    Baseado nas seguintes mensagem de commit:
"""


def get_default_branch() -> str:
    return os.popen("cat .git/refs/remotes/origin/HEAD | awk -F/ '{print $NF}'").read().strip()


def get_currant_branch() -> str:
    return os.popen('git branch --show-current').read().strip()


def get_logs_from_current_branch(branch: str = get_currant_branch()) -> str:
    return os.popen(f'git log {get_default_branch()}..{get_currant_branch()} --pretty=format:%s ').read().strip()


def print_available_generative_models() -> str:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    for m in genai.list_models():
        if 'generateContent' in m.supported_generation_methods:
            print(m.name)


def generate_title_and_description() -> str:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(f"""
        {MAIN_PROMPT}
        {get_logs_from_current_branch()}
    """)
    return response.text


def main():
    print(f"""Baseado nessas mensagens de commit:
    {get_logs_from_current_branch()}
    Sugestão de merge:
    
    {generate_title_and_description()}
    """)


if __name__ == "__main__":
    main()
