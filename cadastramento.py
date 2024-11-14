from conexao import Conexao
# classe que irá armazenar as funções referentes ao processo de cadastramento
class Cadastramento:
    def __init__(self):
        # inicializa os atributos da classe com o valor None
        self.cod_prod = None
        self.descricao_tecnica = None
        self.modelo = None
        self.fabricante = None
        self.num_lote = None
        self.enderecamento = None

    # função para cadastrar os produtos
    def cadastramento (self, cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        # criando um cursor para executar comandos SQL na conexão com o banco de dados
        mycursor = mydb.cursor()

        # armazenando as variáveis que contém os valores obtidos no form (na página "cadastramento.html")
        valores = (cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento)
        # comando sql para inserir os dados no banco de dados 
        dados = f"INSERT INTO tb_cadastramento (cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento) VALUES (%s, %s, %s, %s, %s, %s)"

        #executando a variável a cima
        mycursor.execute(dados, valores)

        # realiza o commit da transação, garantindo que as alterações feitas na base de dados sejam salvas
        mydb.commit()

        # fechando o banco de dados
        mydb.close()

        return True
    
    def cadastramentoProf (self, cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento):
        # conectando com o banco de dados
        mydb = Conexao.conectar()

        # criando um cursor para executar comandos SQL na conexão com o banco de dados
        mycursor = mydb.cursor()

        dados = f"INSERT INTO databaseProfessor.tb_cadastramento (cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento) VALUES ('{cod_prod}', '{descricao_tecnica}', '{modelo}', '{fabricante}', '{num_lote}', '{enderecamento}')"

        #executando a variável a cima
        mycursor.execute(dados)

        # realiza o commit da transação, garantindo que as alterações feitas na base de dados sejam salvas
        mydb.commit()

        mydb.close()

        return True