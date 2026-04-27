# Importa o módulo time para gerar um número único baseado no horário atual
import time


# Define uma classe responsável por criar dados de usuário para os testes
class UserDataFactory:

    # Define um método estático para criar os dados do usuário
    @staticmethod
    def create_user():

        # Gera um número único usando o horário atual em segundos
        timestamp = int(time.time())

        # Retorna um dicionário com os dados do usuário de teste
        return {

            # Define o nome usado no cadastro inicial
            "name": "Laiana",

            # Define um email único usando o timestamp para evitar email repetido
            "email": f"laianacavalcante{timestamp}@gmail.com",

            # Define a senha do usuário
            "password": "Senha@123",

            # Define o primeiro nome usado no formulário completo
            "first_name": "Laiana",

            # Define o sobrenome usado no formulário completo
            "last_name": "Cavalcante",

            # Define a empresa usada no formulário
            "company": "UFAM",

            # Define o primeiro endereço do usuário
            "address1": "Rua Rio Japura, 336",

            # Define o segundo endereço do usuário
            "address2": "Bairro Centro",

            # Define o país usado no cadastro
            "country": "India",

            # Define o estado usado no cadastro
            "state": "Amazonas",

            # Define a cidade usada no cadastro
            "city": "Iranduba",

            # Define o CEP usado no cadastro
            "zipcode": "69000000",

            # Define o número de celular usado no cadastro
            "mobile_number": "92999999999",
        }