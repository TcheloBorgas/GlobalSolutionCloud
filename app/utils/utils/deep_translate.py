import deepl

# Configurar a chave de autenticação da API DeepL
auth_key = "023f48c8-7767-4df8-b643-d77f0cf35c19:fx"  # Substitua pela sua chave
translator = deepl.Translator(auth_key)

def translate_text(text, target_lang="PT-BR"):
    result = translator.translate_text(text, target_lang=target_lang)
    return result.text
