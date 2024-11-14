# importando a classe necessária para poder realizar a conexão com o banco de dados
from conexao import Conexao
# classe que irá contar todas as funções referente a tudo que diz respeito ao aluno
class Aluno:
# método construtor em Python, ele é utilizado para inicializar um novo objeto de uma classe
    def __init__(self):
        self.nome = None
        self.email = None
        self.senha = None
        self.turma = None
        self.cod_aluno = None

    # criando uma função para cadastrar o aluno
    def cadastrar (self, nome, email, senha, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        dados = f"INSERT INTO tb_aluno (nome, email, senha) VALUES ('{nome}', '{email}', '{senha}')"

        #executar
        mycursor.execute(dados)

        mydb.commit()

        mydb.close()

        return True
    
    # função para logar o aluno 
    def logar (self, email, senha, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        # variável que armazena uma função do sql
        dados = f"SELECT * FROM tb_aluno WHERE email = '{email}' AND senha = '{senha}'"

        # executando
        mycursor.execute(dados)

        # selecionando apenas um dado do comando acima
        resultado = mycursor.fetchone()

        # fechando o banco de dados 
        mydb.close()

        # caso não encontre o usuário com os dados que foram passados 
        if not resultado == None:
            self.logado = True
            self.email = resultado[2]
            self.senha = resultado[3]
            self.nome = resultado[1]
            self.turma = turma
            self.cod_aluno = resultado[0]
            return True
        else:
            self.logado = False
            return False

    def verificar_duplicata(self, email, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        query = "SELECT COUNT(*) FROM tb_aluno WHERE email = %s"
        mycursor.execute(query, (email,))
        resultado = mycursor.fetchone()[0]

        mydb.close()
        
        return resultado > 0
