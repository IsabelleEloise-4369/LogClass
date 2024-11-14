from conexao import Conexao
# classe que irá armazenar as funções referentes ao processo de cadastro de expedição
class Expedicao:
    def __init__(self):
        self.cod_prod_exp = None
        self.desc_exp = None
        self.num_lote_exp = None
        self.quant_exp = None
        self.data_emb_exp = None
        self.responsavel_exp = None
        self.cod_aluno = None

    # criando a função para cadastro da expedição dos produtos
    def expedicao(self, cod_prod_exp, desc_exp, num_lote_exp, quant_exp, data_emb_exp, responsavel_exp, cod_aluno, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        valores = (cod_prod_exp, desc_exp, num_lote_exp, quant_exp, data_emb_exp, responsavel_exp, cod_aluno)

        dados = f"INSERT INTO tb_expedicao(cod_prod_exp, desc_exp, num_lote_exp, quant_exp, data_emb_exp, respnsavel_exp, cod_aluno) VALUES (%s, %s, %s, %s, %s, %s, %s)"

        #executar
        mycursor.execute(dados, valores)

        mydb.commit()

        mydb.close()

        return True