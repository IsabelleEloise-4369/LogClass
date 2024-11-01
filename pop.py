from conexao import Conexao
# classe que armazena as funções que correspondem ao registro de pop
class Pop:
    def __init__(self):
        self.data_pop = None
        self.tarefa_pop = None
        self.responsavel_pop = None
        self.material_pop = None
        self.passos_pop = None
        self.manuseio_pop = None
        self.resul_pop = None
        self.acao_pop = None
        self.cod_aluno = None
    
    # criando a função para realizar o processo de pop
    def pop(self, data_pop, tarefa_pop, responsavel_pop, material_pop, passos_pop, manuseio_pop, resul_pop, acao_pop, cod_aluno, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        valores = (data_pop, tarefa_pop, responsavel_pop, material_pop, passos_pop, manuseio_pop, resul_pop, acao_pop, cod_aluno)
        
        dados = f"INSERT INTO tb_pop(data_pop, tarefa_pop, responsavel_pop, material_pop, passos_pop, manuseio_pop, resul_pop, acao_pop, cod_aluno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        #executar
        mycursor.execute(dados, valores)

        mydb.commit()

        mydb.close()

        return True