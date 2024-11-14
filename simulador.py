from conexao import Conexao
import random

class Simulador:
    def __init__(self):
        self.pedidos = []

    def carregar_pedidos(self):
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        mycursor.execute("SELECT * FROM databaseProfessor.tb_cadastramento")
        self.pedidos = mycursor.fetchall()

        mycursor.close()
        mydb.close()

    def selecionar_pedido_aleatorio(self):
        if self.pedidos:
            return random.choice(self.pedidos)
        return None
    
    def obter_informacoes_pedido(self, pedido):
        if pedido:
            return {
                "codigo": pedido[0],
                "descricao": pedido[1],
                "modelo": pedido[2],
                "fabricante": pedido[3],
                "numero_lote": pedido[4],
                "enderecamento": pedido[5],
                "qtde": pedido[6],
                "data": pedido[7]
            }
        return True