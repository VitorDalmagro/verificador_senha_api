'''
API - Verificar a qualidade e força de uma senha.
'''
from flask import Flask

app_api = Flask(__name__)

@app_api.route('https://verificador-senha-api.vercel.app/senha/123/senha/<senha>')
def verificar_senha(senha):
    pontos = 0
    relatorio = []

    # Adicionando letras, números e símbolos para ficar mais fácil de testar a senha
    letras_minusculas = "abcdefghijklmnopqrstuvwxyz"
    letras_maiusculas = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    numeros = "0123456789"
    caracteres_especiais = r"!@#$%^&*()-_=+[]}{;:,.<>/|\?" 
    # Esse r antes da string é para evitar erros com caracteres de escape (nem sabia que dava pra fazer isso kkkk)

    senha_vazia = ''

    existe_letras_maiusculas = False
    existe_letras_minusculas = False
    existe_numeros = False
    existe_caracteres_especiais = False

    # Verificação de senha vazia
    if senha == senha_vazia:
        relatorio.append('A senha não pode ser vazia.')
        return {
            "senha": senha,
            "pontuacao": 0,
            "nivel": "Inválida",
            "relatorio": relatorio
        }       

    for caractere in senha:
        if caractere in letras_maiusculas:
            existe_letras_maiusculas = True
        elif caractere in letras_minusculas:
            existe_letras_minusculas = True
        elif caractere in numeros:
            existe_numeros = True
        elif caractere in caracteres_especiais:
            existe_caracteres_especiais = True
        else:
            relatorio.append('Caractere inválido encontrado. Use apenas letras, números e símbolos.')
            return {
                "senha": senha,
                "pontuacao": 0,
                "nivel": "Inválida",
                "relatorio": relatorio
            }
        
    # Adicionando pontos para caracteres existentes
    if existe_letras_maiusculas:
        pontos += 10
    else:
        relatorio.append('A senha deve conter letras maiúsculas.')

    if existe_letras_minusculas:
        pontos += 10
    else:
        relatorio.append('A senha deve conter letras minúsculas.')

    if existe_numeros:
        pontos += 10
    else:
        relatorio.append('A senha deve conter números.')

    if existe_caracteres_especiais:
        pontos += 20
    else:
        relatorio.append('A senha deve conter caracteres especiais.')

    # Verificando senhas comuns
    senhas_comuns = { 
        "123456", "123456789", "12345678", "12345", "1234567", "1234567890", "000000", "111111", "222222", "333333", "444444", "555555", "666666", "777777", "888888", "999999", "password", "senha", "admin", "user", "guest", "login", "welcome", "letmein", "qwerty", "abc123", "iloveyou", "monkey", "dragon", "football", "baseball", "superman", "pokemon", "batman", "sunshine", "princess", "flower", "master", "shadow", "killer", "soccer", "hottie", "freedom", "whatever", "mustang", "hello", "password1", "senha123", "admin123", "qwerty123", "abc1234", "welcome1", "letmein123", "iloveyou1", "dragon123", "123123", "654321", "121212", "112233", "1q2w3e4r", "1qaz2wsx", "zaq12wsx", "qazwsx", "asdfgh", "asdf1234", "qwertyuiop", "asdfghjkl", "zxcvbnm", "1q2w3e", "qwe123", "poiuyt", "mnbvcxz", "qaz123", "passw0rd", "p@ssword", "brasil", "deus", "amor", "familia", "jesus", "corinthians", "flamengo", "vasco", "palmeiras", "santos", "gato", "cachorro", "amorzinho", "123mudar", "meuamor", "minhasenha" 
        }
    
    # Algumas penalidades
    senha_lower = senha.lower()
    if senha_lower in senhas_comuns:
        pontos -= 30
        relatorio.append('A senha é muito comum ou fácil de adivinhar.')

    for seq in ["123", "abc", "qwerty"]:
        if seq in senha_lower:
            pontos -= 20
            relatorio.append("Evite sequências previsíveis (ex: 123, abc, qwerty).")
            break

    # Avaliando tamanho da senha
    tamanho_senha = len(senha)
    if tamanho_senha >= 8:
        pontos += 20
    else:
        relatorio.append("Use pelo menos 8 caracteres.")

    if tamanho_senha >= 12:
        pontos += 10
    else:
        relatorio.append("Senhas com 12+ caracteres são mais seguras.")

    if tamanho_senha >= 16:
        pontos += 20
    else:
        relatorio.append("Para segurança máxima, use mais de 16 caracteres.")

    # Limitar pontuação e calcular nível final
    pontos = max(0, min(100, pontos))

    if pontos < 30:
        nivel = "Muito fraca"
    elif pontos < 50:
        nivel = "Fraca"
    elif pontos < 70:
        nivel = "Média"
    elif pontos < 80:
        nivel = "Forte"
    else:
        nivel = "Excelente"

    # Feedback final
    if pontos >= 80:
        relatorio.append("Ótimo! Sua senha é forte.")
    elif pontos >= 70:
        relatorio.append("Senha mediana, mas pode ser melhorada com mais caracteres ou variedade.")
    elif pontos >= 50:
        relatorio.append("Sua senha é razoável, mas pode melhorar com mais variedade e tamanho.")
    else:
        relatorio.append("Precisa melhorar muito sua senha.")

    return {
        "senha": senha,
        "pontuacao": pontos,
        "nivel": nivel,
        "relatorio": relatorio
    }

if __name__ == '__main__':
    app_api.run()