import os
import google.generativeai as genai


def main() -> str:
    genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content("""Usando uma linguagem simples e eficiente escreva o titulo e a descrição do merge.
    Na descrição coloque um texto geral e depois agrupe as alterações classificando por tipo de commit explicando o que mudou o e impacto.
    Se necessário inclua observações e links de referencia para enriquecer as explicações.
    Adicione sugestões de açes para o revisor as mudanças.
    Baseado nas seguintes mensagem de commit:
    feat: remover arquivos indesejados
    ci: incluir arquivo do git actions
    """)
    return response.text


if __name__ == "__main__":
    print(main())
