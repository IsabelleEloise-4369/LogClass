import mysql.connector
class Conexao:
    # função para que seja realizar a conexão com o banco de dados
    def conectar():
        # chama a função connect do módulo mysql.connector para estabelecer uma nova conexão com o banco de dados MySQL
        mydb = mysql.connector.connect(
            host ="logclassbase.mysql.database.azure.com",
            # não esquecer de modificar isso conforme a porta do banco de dados
            user ="logclassadm",
            password ="TccSenai.2024",
            database ="databaseprofessor"
        )

        return mydb
    # função que irá executar um determinado banco de dados (o qual será escolhido pelo aluno)
    def conectarAluno(databaseAluno):
        mydb = mysql.connector.connect(
            host ="logclassbase.mysql.database.azure.com",
            # não esquecer de modificar isso conforme a porta do banco de dados
            user ="logclassadm",
            password ="TccSenai.2024",
            database = databaseAluno           
        )

        return mydb
