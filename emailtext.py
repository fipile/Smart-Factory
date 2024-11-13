import random
import string
import mysql.connector
import sys

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root", 
        password="!",  
        database="testdb"
    )

def get_usermail():
    return sys.argv[1] if len(sys.argv) > 1 else None

def get_username(email):
    db = connect_db()
    cursor = db.cursor(prepared=True)

    query = "SELECT usernames FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    if result:
        return result[0] 


    query = "SELECT username FROM userpj WHERE email = %s"
    cursor.execute(query, (email,))
    result = cursor.fetchone()

    if result:
        return result[0]  

    return "Usuário"



def random_number_string(length):
    random_numbers = ''.join(random.choices(string.digits, k=length))
    return random_numbers
random_string =random_number_string(6)


def generate_email_text(usermail):  # Pass usermail as an argument
    if usermail is not None:
        username = get_username(usermail)
    else:
        username = "Usuário"

    email_text = f"""
    Olá, {username}!

    Recebemos uma solicitação para redefinir sua senha. Seu código de recuperação está logo abaixo:

    {random_string}

    Por favor, insira este código no campo solicitado para prosseguir com a redefinição da sua senha. Caso você não tenha solicitado essa alteração, por favor, ignore este e-mail.

    Se precisar de ajuda, estamos à disposição.

    Atenciosamente,  
    Equipe de Suporte
    Licor Express LTDA  
    +551130391799||smartfactoryltda@gmail.com
    CNPJ: 92.019.133/0001-28
    """
    return email_text

def security_password(usermail):
    if usermail is not None:
        username = get_username(usermail)
    else:
        username = "Usuário"

    email_text = f"""
    Olá,  {username}!

    Detectamos múltiplas tentativas de acesso não autorizadas em sua conta e o número máximo de tentativas foi excedido. Por questões de segurança, a sua senha foi temporariamente redefinida.

    Sua nova senha temporária é: {random_string}

    Por favor, faça login em sua conta usando essa senha e altere-a imediatamente para uma senha segura e de sua preferência.

    Se você não reconhece essas tentativas de acesso, recomendamos que verifique suas configurações de segurança.
    Caso tenha alguma dúvida ou precise de ajuda, entre em contato com nossa equipe de suporte.

    Atenciosamente,  
    Equipe de Suporte
    Licor Express LTDA 
    +551130391799||smartfactoryltda@gmail.com
    CNPJ: 92.019.133/0001-28

    """

    return email_text

def cancel_order(usermail):
    if usermail is not None:
        username = get_username(usermail)
    else:
        username = "Usuário"

    email_text = f"""
    Olá, {username}!
    Informamos que a sua compra foi cancelada. Pedimos desculpas pelo inconveniente e estamos à disposição para esclarecer qualquer dúvida que você possa ter.

    Por favor, entre em contato com o nosso suporte para mais informações ou para que possamos ajudá-lo com alternativas.

    Atenciosamente,  
    Equipe de Suporte
    Licor Express LTDA 
    +551130391799||smartfactoryltda@gmail.com
    CNPJ: 92.019.133/0001-28
    """
    return email_text

def order_done(usermail):
    if usermail is not None:
        username = get_username(usermail)
    else:
        username = "Usuário"

    email_text = f"""
    Olá, {username}!

    Informamos que sua compra foi concluída com sucesso e o pedido já foi entregue. Caso ainda não tenha recebido o produto, pedimos que entre em contato com nosso suporte para que possamos auxiliá-lo.

    Se dentro de dois dias após o contato o produto não for entregue, realizaremos o reembolso completo do valor pago.

    Obrigado por escolher comprar conosco!

    Atenciosamente,  
    Equipe de Suporte
    Licor Express LTDA  
    +551130391799||smartfactoryltda@gmail.com
    CNPJ: 92.019.133/0001-28
    """

    return email_text

def order_status(usermail, status):
    if usermail is not None:
        username = get_username(usermail)
    else:
        username = "Usuário"

    email_text = f"""
    Prezado(a) {username},

    Gostaríamos de informar que o status de sua compra foi alterado para {status}.

    Se tiver alguma dúvida ou precisar de assistência, nossa equipe de suporte está à disposição para ajudar. Não hesite em entrar em contato conosco.

    Agradecemos por escolher nossa loja!

    Atenciosamente,  
    Equipe de Suporte
    Licor Express LTDA 
    +551130391799||smartfactoryltda@gmail.com
    CNPJ: 92.019.133/0001-28
    """

    return email_text
