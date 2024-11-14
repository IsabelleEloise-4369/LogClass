from conexao import Conexao
# classe que irá armazenar as funções de registro de picking
class Picking:
    def __init__(self):
        self.num_picking = None
        self.endereco = None
        self.desc_tecnica = None
        self.modelo_pk = None
        self.fabricante_pk = None
        self.quant_pk = None
        self.data_pk = None
        self.lote_pk = None
        self.total_pk = None
        self.cod_prod = None

    # criando a função para que possa ser realizado o processo de picking
    def picking(self, num_picking,endereco, desc_tecnica, modelo_pk, fabricante_pk, quant_pk, data_pk, lote_pk, total_pk, cod_prod, turma):
        # conectando com o banco de dados
        mydb = Conexao.conectarAluno(turma)

        mycursor = mydb.cursor()

        valores = (num_picking, endereco, desc_tecnica, modelo_pk, fabricante_pk, quant_pk, data_pk, lote_pk, total_pk, cod_prod)

        dados = f"INSERT INTO tb_picking(num_picking, endereco, desc_tecnica, modelo_pk, fabricante_pk, quant_pk, data_pk, lote_pk, total_pk, cod_prod) VALUES( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        #executar
        mycursor.execute(dados, valores)

        mydb.commit()

        mydb.close()

        return True