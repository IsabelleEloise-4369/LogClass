# importando módulos e classes necessários para a aplicação
import random
from flask import Flask, render_template, request, redirect, session, jsonify, flash
from conexao import Conexao
from aluno import Aluno
from professor import Professor
from cadastramento import Cadastramento
from estoque import Estoque
from expedicao import Expedicao
from picking import Picking
from pop import Pop
from rnc import Rnc
from simulador import Simulador

#app é o servidor
#criei o objeto app usando a classe Flask
app = Flask(__name__)
app.secret_key = 'logclass'

# # -------------------------------------------------------------------
# # planejamento de código (ainda não está funcionando)
# @app.route("/confirmacao")
# def confirmacao_usuario():
#     # verificando se o usuário logado é o aluno ou professor, para poder liberar a vizualização
#     if "master_logado" in session:
#         if request.method == "GET":
#             #conectando com o banco de dados
#             mydb = Conexao.conectar()
            
#             mycursor = mydb.cursor()

#             confirmacao = (f"SELECT * FROM databaseProfessor.tb_aluno")

#             mycursor.execute(confirmacao)

#             resultado = mycursor.fetchall()

#             # fechar a conexão
#             mydb.close()

#             lista_usuarios = []

#             for usuario in resultado:
#                 lista_usuarios.append({
#                     "id": usuario[0],
#                     "nome": usuario[1]
#                 })

#             return render_template("confirmacao.html", lista_usuarios = lista_usuarios)
   
# @app.route("/aprovar_usuario")
# def aprovar_usuario():
#     # verificando se o usuário logado é o aluno ou professor, para poder liberar a vizualização
#     if "master_logado" in session:
#         if request.method == "GET":
#             #conectando com o banco de dados
#             mydb = Conexao.conectar()
            
#             mycursor = mydb.cursor()
# # -----------------------------------------------------------------------------

#roteamento da página inicial
@app.route("/")
#função da página inicial
def pagina_inicial():
    # varificação se há algum usuário logado no sistema para a liberar a visualização da página
    if "usuario_logado" in session:
        # conectando o banco de dados
        mydb = Conexao.conectar()

        # criando um objeto Aluno
        mycursor = mydb.cursor()

        # Consulta ao banco de dados para obter os produtos da categoria "ouro"
        mensagens = (f"SELECT cod_mensagem, mensagens FROM databaseprofessor.tb_mensagens WHERE turma = '{session['usuario_logado']['turma']}'")

        #executar
        mycursor.execute(mensagens)

        # pegando os dados e guardando em uma variável
        resultado = mycursor.fetchall()

        # fechar a conexão
        mydb.close()
        
        # criando uma lista para armazenar todas as mensagens que foram "retiradas" do banco de dados
        lista_mensagens = []
        
        # criando um loop para cada mensagem que foi "retirada" do banco de dados
        for mensagens_enviadas in resultado:
            lista_mensagens.append({
                "cod_mensagem":mensagens_enviadas[0],
                "mensagem":mensagens_enviadas[1]
            })

        # retornando para a página inicial juntamente com as mensagens que foram enviadas pelo professor
        return render_template("pagina-inicial.html", lista_mensagens = lista_mensagens)

    # se o professor estiver logado então ele será redirecionado para a página inicial mas sem a vizualização das mensagens
    elif "professor_logado" in session:
        return render_template("pagina-inicial.html")
    # se não houver nenhum usuário logado o mesmo será direcionado para a página de cadastro e login
    else:
        # se não estiver nehum usuário logado ele será redirecionado para a página de cadastro
        return redirect("/login")
    
# roteamento da página de cadastro e login que no caso são "juntas" 
# RF001
# RF002
# RF003
# RF004
@app.route("/login", methods=["GET", "POST"])
def pagina_cadastro():
    if request.method == "GET":
        # conectando com o banco de dados
        mydb = Conexao.conectar()
        # criando um objeto Aluno
        mycursor = mydb.cursor()
        # criando uma variável para armazenar a lista de turmas
        mycursor.execute("SELECT * FROM databaseprofessor.tb_database")
        resultado = mycursor.fetchall()
        mydb.close()

        # criando uma lista para armazenar todas as turmas que foram "retirados"
        lista_nomes = [{"database": nomeBD[0]} for nomeBD in resultado]
        return render_template("login.html", lista_nomes=lista_nomes)

    if request.method == "POST":
        # criando uma variável para armazenar o valor do input no formulário
        formulario = request.json.get("tipo")

        # realizando o cadastro do aluno
        if formulario == "Aluno":
            # pegando os dados do formulário, mas em forma de json
            nome = request.json.get("nome")
            email = request.json.get("email")
            senha = request.json.get("senha")
            turma = request.json.get("turma")
            # criando um objeto Aluno
            aluno = Aluno()

            # verificando, por meio de uma função dentro do objeto aluno, se existem duas pessoas com os mesmos cadastros no banco de dados
            if aluno.verificar_duplicata(email, turma):
                # retornando um arquivo json para caso haja usuários com esses dados
                return jsonify({'mensagem': 'Usuário já cadastrado'}), 409
            
            # realizando o cadastro do usuário
            if aluno.cadastrar(nome, email, senha, turma):
                # retornando um arquivo json confirmando o cadastro realizado com sucesso
                return jsonify({'mensagem': 'Cadastro realizado com sucesso'}), 201
            else:
                # retornando um arquivo json caso o cadastro nao seja concluído
                return jsonify({'mensagem': 'Erro ao cadastrar o aluno'}), 400
        

        # realizando o cadastro do professor
        if formulario == "Professor":
            # pegando os dados do formulário, mas em forma de json
            nome = request.json.get("nome")
            email = request.json.get("email")
            senha = request.json.get("senha")

            # criando um objeto para armazrnar a classe Professor
            professor = Professor()

            # verificando se já existe um usuário cadastrado esses dados no banco de dados
            if professor.verificar_duplicata(email):
                # retornando um arquivo json caso haja usuários com esses dados
                return jsonify({'mensagem': 'Usuário já cadastrado'}), 409

            # verificando se o usuário cadastrado inserio a senha correta de acesso
            if senha == "logclass":
                # realizando o cadastro do professor através da função que está dentro do objeto
                if professor.cadastrarProf(nome, email, senha):
                    # retornando um arquivo json confirmando o cadastro realizado com sucesso
                    return jsonify({'mensagem': 'Cadastro realizado com sucesso'}), 201
                else:
                    # retornando um arquivo json caso o cadastro nao seja concluído
                    return jsonify({'mensagem': 'Erro ao cadastrar o professor'}), 400
                
            else:
                # retornando um arquivo json caso a senha inserida seja incorreta
                return jsonify({'mensagem': 'Senha incorreta'}), 401

        # Adicionando aqui a lógica para login de alunos e professores...

        # RF003
        # login de alunos e professores
        formulario = request.json.get("tipo")  
        if formulario == "LoginAluno":
            # pegando os dados do formulário, mas em forma de json
            email = request.json.get("email")
            senha = request.json.get("senha")
            turma = request.json.get("turma")

            # criando um objeto com a classe Aluno
            loginAluno = Aluno()

            # realizando o login do aluno por meio da função armazenada na variável
            if loginAluno.logar(email, senha, turma):
                # armazenando os dados em uma session para poder consultar posteriormente 
                session['usuario_logado'] = {
                    'email': loginAluno.email,
                    'turma': loginAluno.turma,
                    'nome': loginAluno.nome,
                    'cod_aluno': loginAluno.cod_aluno
                }
                # validação por meio de um alert na tela do usuário, para quando o login der certo 
                flash("alert('Muito Bem Vindo ao seu ambiente educacional!!')")
                return redirect('/')
            else:
                # limpando a session caso o login esteja errado
                session.clear()
                return 'Email ou senha incorretos.', 401

        if formulario == "LoginProfessor":
            # pegando os dados do formulário, mas em forma de json
            email = request.json.get("email")
            senha = request.json.get("senha")

            # criando um objeto com a classe Professor
            loginProfessor = Professor()

            # realizando o login do aluno por meio da função armazenada na variável
            if loginProfessor.logarProf(email, senha):
                # armazenando os dados em uma session para poder consultar posteriormente
                session['professor_logado'] = {
                    'email': loginProfessor.email_prof,
                    'nome': loginProfessor.nome_prof,
                    'turma': "databaseProfessor",
                    'senha': loginProfessor.senha_espec,
                    'cod_aluno': loginProfessor.cod_aluno
                }
                # validação por meio de um alert na tela do usuário, para quando o login der certo
                flash("alert('Muito Bem Vindo ao seu ambiente educacional!!')")
                return redirect('/')
            else:
                # limpando a session caso o login esteja errado
                session.clear()
                return 'Email ou senha incorretos.', 401

# Rota para exibir e processar a redefinição de senha
@app.route("/redefinir_senha", methods=["GET", "POST"])
def redefinir_senha():
    # Verifica se o professor está logado
    if "professor_logado" not in session:
        return redirect("/login")

    if request.method == "GET":
        # Conectando ao banco de dados do professor para obter as turmas
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()
        mycursor.execute("SELECT nomeBase FROM databaseprofessor.tb_database")
        turmas = mycursor.fetchall()
        mydb.close()

        # Lista para armazenar dados de todos os alunos
        alunos = []

        # Itera sobre cada turma e busca os alunos
        for turma in turmas:
            nome_turma = turma[0]
            try:
                mydb_turma = Conexao.conectarAluno(nome_turma)  # Conectando ao banco da turma
                cursor_turma = mydb_turma.cursor()
                cursor_turma.execute("SELECT nome, email, %s AS turma, senha, cod_aluno FROM tb_aluno", (nome_turma,))
                alunos.extend(cursor_turma.fetchall())
            finally:
                mydb_turma.close()

        return render_template("redefinir_senha.html", alunos=alunos)

    elif request.method == "POST":
        # Coletando dados do formulário para atualização
        cod_aluno = request.form.get("cod_aluno")
        nova_senha = request.form.get("nova_senha")
        turma = request.form.get("turma")

        # Atualiza a senha no banco de dados da turma específica
        mydb_turma = Conexao.conectarAluno(turma)
        cursor_turma = mydb_turma.cursor()
        cursor_turma.execute("UPDATE tb_aluno SET senha = %s WHERE cod_aluno = %s", (nova_senha, cod_aluno))
        mydb_turma.commit()
        mydb_turma.close()

        flash("Senha redefinida com sucesso!")
        return redirect("/redefinir_senha")

# roteamento da página de cadastramento
# RF005
@app.route("/cadastramento", methods=["GET", "POST"])
def pagina_cadastramento():
# as páginas são protegidas por autenticação de sessão para garantir que apenas usuários autenticados possam acessá-las.
# if que determina o acesso às páginas apenas se o aluno estiver logado.
    if "usuario_logado" in session:
        if request.method == "GET":
            return render_template("cadastramento.html")
        if request.method == "POST":
            # pegando os valores dos inputs da página cadastramento
            descricao = request.form.get("descricao")
            modelo = request.form.get("modelo")
            fabricante = request.form.get("fabricante")
            codigo = request.form.get("codigo")
            numeroLote = request.form.get("numeroLote")
            enderecamento = request.form.get("enderecamento")
            
            # armazenando a classe da página de cadastramento em que estão os comandos sql em uma várial
            tbCadastramento = Cadastramento()

            # chamando a função que está dentro da classe 
            if tbCadastramento.cadastramento(codigo, descricao, modelo, fabricante, numeroLote, enderecamento, session['usuario_logado']['turma']):
                return render_template("cadastramento.html")
            else:
                return 'Erro ao realizar o processo de Cadastramento'
    # verificando se o usuário logado é o professor, para poder liberar a vizualização das páginas
    elif "professor_logado" in session:
        if request.method == "GET":
            return render_template("cadastramento.html")
        if request.method == "POST":
            # pegando os valores dos inputs da página cadastramento
            descricao = request.form.get("descricao")
            modelo = request.form.get("modelo")
            fabricante = request.form.get("fabricante")
            codigo = request.form.get("codigo")
            numeroLote = request.form.get("numeroLote")
            enderecamento = request.form.get("enderecamento")
            # transformando a classe Cadastramento em um objeto
            tbCadastramento = Cadastramento()

            # pegando a função armazenada no objeto para realizar o processo de cadastramento de um produto
            if tbCadastramento.cadastramentoProf(codigo, descricao, modelo, fabricante, numeroLote, enderecamento):
                return render_template("cadastramento.html")
            else:
                return 'Erro ao realizar o processo de Cadastramento'
    else:
        return redirect("/login")

# roteamento da página inventário
@app.route('/inventario')
def inventario():
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            turma = session['usuario_logado']['turma'] if "usuario_logado" in session else session['professor_logado']['turma']

            # Query para listar os produtos do inventário
            produtos = f"SELECT cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento, quantidade FROM {turma}.tb_cadastramento"
            mycursor.execute(produtos)
            resultado = mycursor.fetchall()

            lista_produtos = []
            for produto in resultado:
                lista_produtos.append({
                    "codigo": produto[0],
                    "descricao": produto[1],
                    "modelo": produto[2],
                    "fabricante": produto[3],
                    "numero_lote": produto[4],
                    "enderecamento": produto[5],
                    "quantidade": produto[6]
                })

            # Obtém a lista de bancos de dados, incluindo o do professor
            mycursor.execute("SELECT * FROM databaseprofessor.tb_database")
            resultado = mycursor.fetchall()

            # Adiciona a turma do professor à lista de opções se ele estiver logado
            if "professor_logado" in session:
                resultado.append((session['professor_logado']['turma'],))

            mydb.close()

            # Cria a lista de opções para o select
            lista_nomes = [{"database": nomeBD[0]} for nomeBD in resultado]

            return render_template("inventario.html", lista_produtos=lista_produtos, lista_nomes=lista_nomes)


# roteamento da função para excluir os produtos do inventário
@app.route("/excluir_produto", methods=["POST"])
def excluir_produto():
    if "professor_logado" in session:
        # Captura os dados do formulário
        cod_prod = request.form.get("cod_prod")
        turma = request.form.get("turma")

        if not cod_prod or not turma:
            return "Erro: Código do produto ou banco de dados não fornecido."

        try:
            # Conecta ao banco de dados selecionado
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # Monta a query de exclusão com o banco de dados correto
            sql_delete = f"DELETE FROM {turma}.tb_cadastramento WHERE cod_prod = %s"
            mycursor.execute(sql_delete, (cod_prod,))

            # Confirma a transação e fecha a conexão
            mydb.commit()
            mydb.close()

            return redirect("/inventario")  # Redireciona para a página de inventário após a exclusão
        except Exception as e:
            return f"Erro ao excluir o produto: {e}"
    else:
        return redirect("/login")

# Página de controle de estoque
@app.route("/estoque", methods=["GET", "POST"])
def pagina_estoque():
    # verificando se há algum usuário logado no sistema, seja ele professor ou aluno
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            mydb = Conexao.conectar()

            mycursor = mydb.cursor()

            turma = session['usuario_logado']['turma'] if "usuario_logado" in session else session['professor_logado']['turma']
            
            produtos = f"SELECT * FROM {turma}.tb_cadastramento"

            mycursor.execute(produtos)

            resultado = mycursor.fetchall()

            lista_produtos = [{"codigo": produto[0], "descricao": produto[1], "modelo": produto[2], "fabricante": produto[3], "numero_lote": produto[4], "enderecamento": produto[5], "quantidade": produto[6]} for produto in resultado]

            return render_template("estoque.html", lista_produtos=lista_produtos)

        if request.method == "POST":
            cod_prod = request.form.get("cod_prod")
            num_lote = request.form.get("num_lt")
            loc_ = request.form.get("loc_")
            descricao = request.form.get("descricao")
            dt_enter = request.form.get("dt_enter")
            qt_item = int(request.form.get("qt_item") or 0)  # Define 0 se o campo estiver vazio
            dt_end = request.form.get("dt_end")
            qt_saida = int(request.form.get("qt_saida") or 0)  # Define 0 se o campo estiver vazio
            _saldo = int(request.form.get("_saldo") or 0)  # Define 0 se o campo estiver vazio
            funcionario = request.form.get("funcionario")

            # armazenando o banco de dados de cada usuário logado e seus respectivos códigos que são AUTO_INCREMENT
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # Conectar ao banco e buscar o saldo atual
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()
            # adicionando o saldo na tabela tb_estoque
            mycursor.execute(f"SELECT saldo FROM {turma}.tb_estoque WHERE cod_prod_est = %s", (cod_prod,))
            resultado = mycursor.fetchone()
            saldo_atual = resultado[0] if resultado else 0

            # Atualizar saldo
            saldo_novo = saldo_atual + qt_item - qt_saida

            # Inserir/Atualizar registro no estoque
            tbEstoque = Estoque()
            sucesso = tbEstoque.estoque(cod_prod, num_lote, loc_, descricao, dt_enter, qt_item, dt_end, qt_saida, saldo_novo, funcionario, cod_aluno, turma)
            
            mycursor.execute(
                f"UPDATE {turma}.tb_cadastramento SET quantidade = quantidade + %s WHERE cod_prod = %s",
                (qt_item - qt_saida, cod_prod)
            )
            mydb.commit()
            
            if sucesso:
                flash("alert('Movimentação de estoque registrada com sucesso!')")
                return redirect("/")
            else:
                return "Erro ao registrar movimentação de estoque"

    else:
        return redirect("/login")


# Nova rota para buscar informações do produto pelo código para preenchimento automático
# Rota para obter informações de um produto pelo código para preenchimento automático
@app.route("/produto-info/<codigo>", methods=["GET"])
def produto_info(codigo):
    # Obtém o código do produto passado como query string
    codigo_produto = codigo
    if "usuario_logado" in session or "professor_logado" in session:
        # Obtendo a turma do usuário logado para acessar a tabela correta
        turma = session['usuario_logado']['turma'] if "usuario_logado" in session else session['professor_logado']['turma']
        
        # Conectando ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()
        
        # Consulta SQL para buscar as informações do produto pelo código
        query = f"SELECT cod_prod, descricao_tecnica, modelo, fabricante, num_lote, enderecamento FROM {turma}.tb_cadastramento WHERE cod_prod = %s"
        mycursor.execute(query, (codigo_produto,))
        produto = mycursor.fetchone()

        # Verifica se o produto foi encontrado e retorna os dados em JSON
        if produto:
            produto_info = {
                "codigo": produto[0],
                "descricao": produto[1],
                "modelo": produto[2],
                "fabricante": produto[3],
                "numero_lote": produto[4],
                "enderecamento": produto[5]
            }
            return jsonify(produto_info), 200
        else:
            # Retorna um erro 404 se o produto não foi encontrado
            return jsonify({"erro": "Produto não encontrado"}), 404
    return jsonify({"erro": "Usuário não autorizado"}), 403

        
# roteamento da página dos processos de registro expedição
# RF010
@app.route("/expedicao", methods=["GET", "POST"])
def pagina_expedicao():
    # verificando se um dos usuários estão conectados para habilitar a visualização da página
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            #conectando com o banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()

            # armazenando o banco de dados de cada usuário logado e seus respectivos códigos que são AUTO_INCREMENT
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # armazenando o banco de dados de cada usuário logado e seus respectivos códigos que são AUTO_INCREMENT
            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            # criando uma lista para armazenar os produtos
            lista_produtos = []
            
            # usando um loop para ir adicionando os produtos na lista (variável) que foi criada anteriormente
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5],
                    "quantidade":produto[6]
                })
            return render_template("expedicao.html", lista_produtos=lista_produtos)
        
        if request.method == "POST":
            # armazenando os dados do formulário
            cod_prod = request.form.get("cod_prod")
            data_saida = request.form.get("data_saida")
            num_lote = request.form.get("num_lote")
            responsavel = request.form.get("responsavel")
            quantidade = request.form.get("quantidade")
            descricao_tec = request.form.get("descricao_tec")

            # transformando a classe em um objeto
            tbExpedicao = Expedicao()

            # pegando dados que foram armazenados na session e "guardando" em uma variável 
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizando o processo de registro de expedição
            if tbExpedicao.expedicao(cod_prod, descricao_tec, num_lote, quantidade, data_saida, responsavel, cod_aluno, turma):
                # exibindo uma mensagem na interface do usuário para quando o cadastro for realizado com sucesso
                flash("alert('Parabéns, você acabou de realizar o processo de registro de expedição!!🎉')")
                return redirect ('/')
            else:
                # exibindo uma mensagem na interface do usuário para quando o cadastro não for realizado
                return "Erro ao realizar o processo de cadastro de expedição."
    else:
        return redirect("/login")
    
# roteamento da página dos processos de registro picking
# RF007
@app.route("/picking", methods=["GET", "POST"])
def pagina_picking():
    # verificando se há algum usuário cadastrado e logado para poder habilitar a visualização da página
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            #conectando com o banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()

            # verificando se os usuários estão logados para poder armazenar as informações que foram guardadas na sessão, em uma variável 
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # comando sql para poder pegar todos os produtos que foram cadastrados no banco de dados
            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            # criando uma lista para posterioirmente armazenar os produtos
            lista_produtos = []
            
            # loop para poder ir adicionando os produtos na lista 
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5],
                    "quantidade":produto[6],
                })
            return render_template("picking.html", lista_produtos=lista_produtos)
        
        if request.method == "POST":
            # pegando os dados que foram enviados pelo formulário
            numPicking = request.form.get("numPicking")
            enderecamento = request.form.get("enderecamento")
            descTec = request.form.get("descTec")
            modeloPick = request.form.get("modeloPick")
            fabri = request.form.get("fabri")
            qtde = request.form.get("qtde")
            data = request.form.get("data")
            lote = request.form.get("lote")
            totalProd = request.form.get("totalProd")
            codProd = request.form.get("codProd")

            # criando um objeto para aramzenar a classe Picking
            tbpicking = Picking()

            # armazenando as irformações que são guardadas na session, em uma variável 
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizando o registro de picking por meio da função que pertence ao objeto criado
            if tbpicking.picking(numPicking, enderecamento, descTec, modeloPick, fabri, qtde, data, lote, totalProd, codProd, turma):
                # emitindo uma mensagem para quando o cadastro for realizado com sucesso
                flash("alert('Parabéns, você acaou de realizar o processo de picking!!🎉')")
                return redirect("/")
            else:
                # emitindo uma mensagem para quando o cadastro não for realizado
                return 'Erro ao realizar o processo de Picking'
    
    else:
        return redirect("/login")
    
# rota para a página do sorteador de simulação de pedidos
@app.route('/simulador')
def simulador():
    if "usuario_logado" in session or "professor_logado" in session:
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        if "usuario_logado" in session:           
            turma = session['usuario_logado']['turma']
        else:
            turma = session['professor_logado']['turma']

        mycursor.execute(f"SELECT * FROM {turma}.tb_picking")
        pedidos = mycursor.fetchall()

        pedido_aleatorio = random.choice(pedidos) if pedidos else {}

        if pedido_aleatorio:
            pedido_info = {
                "num_picking": pedido_aleatorio[0],
                "enderecamento": pedido_aleatorio[1],
                "desc_tecnica": pedido_aleatorio[2],
                "modelo": pedido_aleatorio[3],
                "fabricante": pedido_aleatorio[4],
                "quantidade": pedido_aleatorio[5],
                "data": pedido_aleatorio[6],
                "lote": pedido_aleatorio[7],
                "total_produtos": pedido_aleatorio[8],
                "cod_prod": pedido_aleatorio[9]
            }
        else:
            pedido_info = {}

        mycursor.close()
        mydb.close()


        return render_template("simulador.html", pedido=pedido_info)
    else:
        return redirect("/login")
       
    
# roteamento da página dos processos de registro pop
# RF009
@app.route("/pop", methods=["GET", "POST"])
def pagina_pop():
    # verificando se há algum perfil logado no sistema
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            return render_template("pop.html")
        if request.method == "POST":
            # pegando os dados que foram enviados pelo formulário
            dt_end1 = request.form.get("dt_end1")
            task_name = request.form.get("task_name")
            resp_ = request.form.get("resp_")
            material = request.form.get("material")
            passos = request.form.get("passos")
            manuseio = request.form.get("manuseio")
            resultados = request.form.get("resultados")
            acoes = request.form.get("acoes")

            # criando um objeto com a classe Pop
            tbPop = Pop()

            # armazenando os dados da session em uma variável
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizandpo o processo de registro de POP por meio de uma função que está armazenada no objeto criado anteriormente
            if tbPop.pop(dt_end1, task_name, resp_, material, passos, manuseio, resultados, acoes, cod_aluno, turma):
                # emitindo uma mensagem para quando o processo for realizado com sucesso
                flash("alert('Parabéns, você acaou de realizar o processo de registro de POP!!🎉')")
                return redirect ('/')
            else:
                # emitindo uma mensagem para quando o processo não for realizado
                return 'Erro ao realizar o processo de POP'
    else:
        return redirect("/login")

# roteamento da página dos processos de registro rnc
# RF006
@app.route("/rnc", methods=["GET", "POST"])
def pagina_rnc():
    # verificando se há alguém logado no sistema 
    if  "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            #conectando com o banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()
            
            # armazenando os dados que estão na session em uma variável 
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']
            
            # comando sql para pegar todos os produtos que foram cadastrados no banco de dados 
            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            # criando uma lista para armazenar os produtos posteriormente 
            lista_produtos = []
            
            # loop para ir adicioando cada produto na lista
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5],
                    "quantidade":produto[6]
                })

            return render_template("rnc.html", lista_produtos = lista_produtos)
        
        if request.method == "POST":
            # pegando os dados que foram enviados pelo formulário
            data = request.form.get("date")
            numRNC = request.form.get("numRNC")
            local = request.form.get("local")
            qtdentregue = request.form.get("qtdentregue")
            qtdrepro = request.form.get("qtdrepro")
            descRNC = request.form.get("descRNC")
            respInsp = request.form.get("respInsp")
            codProd = request.form.get("codProd")

            # criando um objeto para armazenar a classe
            tbrnc = Rnc()

            # armazendo os dados que estão guardados na session, em uma variável
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizando o processo de RNC por meio de uma função que está armazenada no objeto criado anteriormente 
            if tbrnc.rnc(descRNC, data, numRNC, local, qtdentregue, qtdrepro, respInsp, codProd, cod_aluno, turma):
                # emitindo uma mensagem de confirmação da realização do processo na interface do sistema 
                flash("alert('Parabéns, você acaou de realizar o processo de Registro de Não Conformidade!!🎉')")
                return redirect("/")
            else:
                return 'Erro ao realizar o processo de RNC'
    
    else:
        return redirect("/login")

# Roteamento da página que cria os bancos de dados para cada turma 
# RF011
@app.route("/criarBD", methods=["GET", "POST"])
def criarBD():
    # verificando se o usuário está logado no sistema 
    if "professor_logado" in session:
        if request.method == "GET":
            return render_template("professor.html")
        if request.method == "POST":
            # pegando os dados que foram enviados pelo formulário
            nomeBD = request.form.get("nomeTurma")

            # criando um objeto 
            criarDataBase = Professor()

            # criando uma turma (banco de dados) por meio de uma função armazenada dentro do objeto
            if criarDataBase.criaDatabse(nomeBD):
                # emitindo uma mensagem na interfacew do usuário quando o processo por realizado 
                flash("alert('Parabéns, você acabou de criar uma nova turma!!🎉')")
                return redirect("/")
            else:
                return "Erro ao criar o banco de dados"
    else:
        return "Acesso negado", 403

# roteamento da página que o professor utiliza para enviar mensagens para os alunos 
@app.route("/enviar_mensagem", methods=["GET", "POST"])
def enviar_mensagens():
    # verificando se o usuário está logado para poder permitir a vizualização da página
    if "professor_logado" in session:
        # Conectando ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        if request.method == "GET":
            # Consulta para obter a lista de turmas
            mycursor.execute("SELECT * FROM databaseprofessor.tb_database")
            resultado = mycursor.fetchall()
            lista_nomes = [{"database": nomeBD[0]} for nomeBD in resultado]

            # Consulta para obter a lista de mensagens enviadas
            mycursor.execute("SELECT cod_mensagem, mensagens, turma FROM tb_mensagens")
            mensagens = mycursor.fetchall()
            lista_mensagens = [{"cod_mensagem": msg[0], "mensagem": msg[1], "turma": msg[2]} for msg in mensagens]

            # Fechar a conexão com o banco de dados
            mydb.close()

            # Renderizar a página com as listas de turmas e mensagens
            return render_template("mensagem.html", lista_nomes=lista_nomes, lista_mensagens=lista_mensagens)

        if request.method == "POST":
            # Conectando ao banco de dados para enviar mensagem
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()

            # Pega a mensagem do formulário
            mensagem = request.form.get("mensagem")
            bancoDados = request.form.get("turma")

            # Inserir a nova mensagem no banco de dados
            inserir_mensagem = f"INSERT INTO tb_mensagens (mensagens, turma) VALUES (%s, %s)"
            mycursor.execute(inserir_mensagem, (mensagem, bancoDados))
            mydb.commit()
            mydb.close()

            # Emite uma mensagem de confirmação ao usuário
            flash("alert('Mensagem enviada para a turma com sucesso! 🎉')")
            return redirect("/enviar_mensagem")



# rota em que está a função que o professor usará para excluir uma mensagem do banco de dados e da interface do usuário
@app.route("/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    if "professor_logado" in session:
        # peagndo o id da mensagem 
        mensagem_id = request.form.get("mensagem_id")
        
        if mensagem_id:
            # Conectando ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()
            
            # Query para deletar a mensagem com o ID fornecido
            delete_query = "DELETE FROM databaseProfessor.tb_mensagens WHERE cod_mensagem = %s"
            
            # Executar a query passando o ID da mensagem
            mycursor.execute(delete_query, (mensagem_id,))
            mydb.commit()
            mydb.close()

            # mensagem na interface do usuário para quando der certo o processo de excluir uma mensagem 
            flash("alert('Mensagem excluída com sucesso!')")
        else:
            # mensagem na interface do usuário para quando não for possível excluir uma mensagem
            flash("alert('Erro ao excluir a mensagem. ID inválido.')")
    # retornando para a p´gina inicial 
    return redirect("/")

# roteamento para exibir todos os bancos de dados que foram criados pelo professor 
@app.route("/professor/listarBD")
def listar_bancos():
    # verificando se o usuário está logado para poder exibir a página
    if "professor_logado" in session:
        # Conectando ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        # Buscando os nomes dos bancos de dados criados
        mycursor.execute("SELECT nomeBase FROM databaseprofessor.tb_database")
        bancos = mycursor.fetchall()

        # Convertendo o resultado em uma lista de dicionários
        lista_bancos = [{"nome": banco[0]} for banco in bancos]

        # Fechando a conexão
        mycursor.close()
        mydb.close()

        # Renderizando o template com a lista de bancos de dados
        return render_template("listar_bancos.html", lista_bancos=lista_bancos)
    else:
        return "Acesso negado", 403

# roteamento para excluir os bancos de dados criados pelo professor 
@app.route("/professor/excluirBD/<nomeBD>", methods=["POST"])
def excluir_banco(nomeBD):
    # verificando se há algum usuário logado para poder liberar a visualização da página 
    if "professor_logado" in session:
        # Conectando ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        # Comando para excluir o banco de dados
        mycursor.execute(f"DROP DATABASE IF EXISTS {nomeBD}")

        # Remover o banco de dados da tabela de referência
        mycursor.execute("DELETE FROM databaseprofessor.tb_database WHERE nomeBase = %s", (nomeBD,))
        
        mydb.commit()
        mycursor.close()
        mydb.close()
 
        # mensagem na interface do usuário para quando a turma for excluída
        flash("alert('Turma finalizada com sucesso!!🎉')")
        # retornando para a página em que estão sendo exibidos os bancos de dados em forma de lista 
        return redirect("/professor/listarBD")
    else:
        return "Acesso negado", 403

if  __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)  # Iniciando o servidor com debug ativado
