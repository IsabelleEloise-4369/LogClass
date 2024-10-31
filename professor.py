from conexao import Conexao
# classe que armazena as funções referentes ao processo de cadastro e login do professor
class Professor:
    def __init__(self):
        self.nome_prof = None
        self.email_prof = None
        self.senha_espec = None

    # criando função para cadastrar o professor
    def cadastrarProf (self, nome_prof, email_prof, senha_espec):
        # conectando com o banco de dados
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        dados = f"INSERT INTO tb_aluno (nome, email, senha) VALUES ('{nome_prof}', '{email_prof}', '{senha_espec}')"

        #executar
        mycursor.execute(dados)

        mydb.commit()

        mydb.close()

        return True

    # logando o professor
    def logarProf (self, email_prof, senha_espec):
        # conectando com o banco de dados
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        dados = f"SELECT * FROM tb_aluno WHERE email = '{email_prof}' AND senha = '{senha_espec}'"

        # executando
        mycursor.execute(dados)

        resultado = mycursor.fetchone()

        mydb.close()

        # caso não encontre o usuário com os dados que foram passados 
        if not resultado == None:
            self.logado = True
            self.email_prof = resultado[2]
            self.senha_espec = resultado[3]
            self.cod_aluno = resultado[0]
            return True
        else:
            self.logado = False
            return False



    def criaDatabse(self, bancodedados):
        # conectando com o banco de dados
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        # variável que armazena o comando que executará um novo banco de dados
        # criando um banco de dados caso ele ainda não exista (IF NOT EXISTS)
        dados = [
            f"""
                CREATE DATABASE IF NOT EXISTS {bancodedados};
            """,
            f"""
                USE {bancodedados};
            """,
            """
                CREATE TABLE tb_aluno (
                cod_aluno INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                nome VARCHAR(100) NOT NULL,
                email VARCHAR(100) NOT NULL,
                senha VARCHAR(100) NOT NULL
                );
            """,
            """
                CREATE TABLE tb_cadastramento (
                cod_prod VARCHAR(100),
                descricao_tecnica VARCHAR(100),
                modelo VARCHAR(100),
                fabricante VARCHAR(100),
                num_lote VARCHAR(100),
                enderecamento VARCHAR(100),
                quantidade INT DEFAULT 0
                );
            """,
            """
                ALTER TABLE tb_cadastramento ADD CONSTRAINT PK_tb_cadastramento PRIMARY KEY (cod_prod);
            """,
            """
                CREATE TABLE tb_estoque (
                id INT AUTO_INCREMENT PRIMARY KEY,
                cod_prod_est INT,
                num_lote_est INT ,
                loc_est CHAR(100) ,
                desc_tec VARCHAR(100) ,
                data_entrega DATE ,
                quant_itens_entrada INT ,
                data_saida DATE ,
                quant_saida INT ,
                saldo INT ,
                func_responsavel VARCHAR(100) ,
                cod_aluno INT
                );
            """,
            """
                CREATE TABLE tb_expedicao (
                cod_prod_exp VARCHAR(100) ,
                desc_exp VARCHAR(100) ,
                num_lote_exp VARCHAR(100) ,
                quant_exp VARCHAR(100) ,
                data_emb_exp DATE ,
                respnsavel_exp VARCHAR(100) ,
                cod_aluno INT 
                );
            """,
            """
                ALTER TABLE tb_expedicao ADD CONSTRAINT PK_tb_expedicao PRIMARY KEY (cod_prod_exp);
            """,
            """
                CREATE TABLE tb_picking (
                num_picking INT ,
                endereco VARCHAR(100) ,
                desc_tecnica VARCHAR(100) ,
                modelo_pk VARCHAR(100) ,
                fabricante_pk VARCHAR(100) ,
                quant_pk INT ,
                data_pk DATE ,
                lote_pk VARCHAR(100) ,
                total_pk INT ,
                cod_prod VARCHAR(100) 
                );
            """,
            """
                ALTER TABLE tb_picking ADD CONSTRAINT PK_tb_picking PRIMARY KEY (num_picking);
            """,
            """
                CREATE TABLE tb_pop (
                cod_pop INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
                data_pop DATE ,
                tarefa_pop VARCHAR(100) ,
                responsavel_pop VARCHAR(100) ,
                material_pop VARCHAR(100) ,
                passos_pop VARCHAR(100) ,
                manuseio_pop VARCHAR(100) ,
                resul_pop VARCHAR(100) ,
                acao_pop VARCHAR(100) ,
                cod_aluno INT 
                );
            """,
            """
                CREATE TABLE tb_rnc (
                desc_rnc VARCHAR(100) ,
                recebimento DATE ,
                num_rnc VARCHAR(100) ,
                local_rnc VARCHAR(100) ,
                quant_entregue INT ,
                quant_reprovada INT NOT NULL,
                resp_inspecao VARCHAR(100) ,
                cod_prod VARCHAR(100) ,
                cod_aluno INT 
                );
            """,
            """
                ALTER TABLE tb_rnc ADD CONSTRAINT PK_tb_rnc PRIMARY KEY (desc_rnc);
            """,
            """
                ALTER TABLE tb_estoque ADD CONSTRAINT FK_tb_estoque_0 FOREIGN KEY (cod_aluno) REFERENCES tb_aluno (cod_aluno);
            """,
            """
                ALTER TABLE tb_expedicao ADD CONSTRAINT FK_tb_expedicao_0 FOREIGN KEY (cod_prod_exp) REFERENCES tb_cadastramento (cod_prod);
            """,
            """
                ALTER TABLE tb_expedicao ADD CONSTRAINT FK_tb_expedicao_1 FOREIGN KEY (cod_aluno) REFERENCES tb_aluno (cod_aluno);
            """,
            """
                ALTER TABLE tb_picking ADD CONSTRAINT FK_tb_picking_0 FOREIGN KEY (cod_prod) REFERENCES tb_cadastramento (cod_prod);
            """,
            """
                ALTER TABLE tb_pop ADD CONSTRAINT FK_tb_pop_0 FOREIGN KEY (cod_aluno) REFERENCES tb_aluno (cod_aluno);
            """,
            """
                ALTER TABLE tb_rnc ADD CONSTRAINT FK_tb_rnc_0 FOREIGN KEY (cod_prod) REFERENCES tb_cadastramento (cod_prod);
            """,
            """
                ALTER TABLE tb_rnc ADD CONSTRAINT FK_tb_rnc_1 FOREIGN KEY (cod_aluno) REFERENCES tb_aluno (cod_aluno);
            """,
            f"""
                INSERT INTO {bancodedados}.tb_cadastramento SELECT * FROM databaseProfessor.tb_cadastramento;
            """
        ]
            

        #executar
        # Executar cada comando de criação de tabela
        for comando in dados:
            print(comando)
            mycursor.execute(comando)

        # salvar o que foi adicionado ao banco de dados
        mydb.commit()
        
        nomes = f"INSERT into databaseprofessor.tb_database (nomeBase) VALUES ('{bancodedados}')"
        mycursor.execute(nomes)
        mydb.commit()
        
        # fechando o banco de dados
        mydb.close()

        # retornando um valor verdadeiro
        return True
    
    def verificar_duplicata(self, email):
        # conectando com o banco de dados
        mydb = Conexao.conectar()

        mycursor = mydb.cursor()

        query = "SELECT COUNT(*) FROM databaseProfessor.tb_aluno WHERE email = %s"
        mycursor.execute(query, (email,))
        resultado = mycursor.fetchone()[0]

        mydb.close()
        
        return resultado > 0