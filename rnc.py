from conexao import Conexao
# classe que armazena as funções referentes ao processo de registro de rnc
class Rnc:
    def __init__(self):
        self.desc_rnc = None
        self.recebimento = None
        self.num_rnc = None
        self.local_rnc = None
        self.quant_entregue = None
        self.quant_reprovada = None
        self.resp_inspecao = None
        self.cod_prod = None

    # criando uma função para que seja possível a realização do processo de rnc
    def rnc(self, desc_rnc, recebimento, num_rnc, local_rnc, quant_entregue, quant_reprovada, resp_inspecao, cod_prod, cod_aluno, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        valores = (desc_rnc, recebimento, num_rnc, local_rnc, quant_entregue, quant_reprovada, resp_inspecao, cod_prod, cod_aluno)

        dados = f"INSERT INTO tb_rnc(desc_rnc, recebimento, num_rnc, local_rnc, quant_entregue, quant_reprovada, resp_inspecao, cod_prod, cod_aluno) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"

        #executar
        mycursor.execute(dados, valores)

        # realiza o commit da transação, garantindo que as alterações feitas na base de dados sejam salvas
        mydb.commit()

        mydb.close()
        
        # retorna True indicando que a operação foi realizada com sucesso
        return True