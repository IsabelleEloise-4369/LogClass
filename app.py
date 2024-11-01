# importando módulos e classes necessários para a aplicação
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

#app é o servidor
#criei o objeto app usando a classe Flask
app = Flask(__name__)
app.secret_key = 'logclass'

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

        return render_template("pagina-inicial.html", lista_mensagens = lista_mensagens)

    elif "professor_logado" in session:
        return render_template("pagina-inicial.html")
    # se não houver nenhum usuário logado o mesmo será direcionado para a página de cadastro e login
    else:
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
                flash("alert('Parabéns, você acaou de realizar o processo de cadastramento de um produto!!🎉')")
                return redirect("/")
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
                flash("alert('Parabéns, você acaou de realizar o processo de cadastramento de um produto!!🎉')")
                return redirect("/")
            else:
                return 'Erro ao realizar o processo de Cadastramento'
    else:
        return redirect("/login")


# roteamento da página dos processos de registro estoque
# RF008
@app.route("/estoque",  methods=["GET", "POST"])
def pagina_estoque():
    # verificando se o usuário logado é o aluno ou professor, para poder liberar a vizualização
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            #conectando com o banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()

            # armazenando o banco de dados dos usuários que estão logados, em uma variável
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
            else:
                turma = session['professor_logado']['turma']
            
            
            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            # armazenando os produtos em uma lista
            lista_produtos = []
            # adicioando cada produto na lista 
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5]
                })
            return render_template("estoque.html", lista_produtos=lista_produtos)
        
        if request.method == "POST":
            # pegando os dados do formulário
            cod_prod = request.form.get("cod_prod")
            num_lote = request.form.get("num_lt")
            loc_ = request.form.get("loc_")
            descricao = request.form.get("descricao")
            dt_enter = request.form.get("dt_enter")
            qt_item = request.form.get("qt_item")
            dt_end = request.form.get("dt_end")
            qt_saida = request.form.get("qt_saida")
            _saldo = request.form.get("_saldo")
            funcionario = request.form.get("funcionario")

            # criando um objeto aramzenando a classe Estoque em uma variável
            tbEstoque = Estoque()

            # armazenando o banco de dados de cada usuário logado e seus respectivos códigos que são AUTO_INCREMENT
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizando o cadastro do controle de estoque, por meio da função que foi armazenada dentro do objeto Estoque
            if tbEstoque.estoque(cod_prod, num_lote, loc_, descricao, dt_enter, qt_item, dt_end, qt_saida, _saldo, funcionario, cod_aluno, turma):
                flash("alert('Parabéns, você acaou de realizar o processo de cadastramento de estoque!!🎉')")
                return redirect("/")
            else:
                return "Erro ao realizar o processo de Controle de Estoque"
        else:
            return redirect("/login")
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
            
            lista_produtos = []
            
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5]
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

            # pegando dados que foram armazenados na session e "guardandando" em uma variável 
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            # realizando o processo de registro de expedição
            if tbExpedicao.expedicao(cod_prod, descricao_tec, num_lote, quantidade, data_saida, responsavel, cod_aluno, turma):
                # exibindo uma mensagem na interface do usuário para quando o cadastro for realizado com sucesso
                flash("alert('Parabéns, você acaou de realizar o processo de registro de expedição!!🎉')")
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

            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            lista_produtos = []
            
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5]
                })
            return render_template("picking.html", lista_produtos=lista_produtos)
        if request.method == "POST":
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

            tbpicking = Picking()

            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            if tbpicking.picking(numPicking, enderecamento, descTec, modeloPick, fabri, qtde, data, lote, totalProd, codProd, turma):
                flash("alert('Parabéns, você acaou de realizar o processo de picking!!🎉')")
                return redirect("/")
            else:
                return 'Erro ao realizar o processo de Picking'
    
    else:
        return redirect("/login")
    
# roteamento da página dos processos de registro pop
# RF009
@app.route("/pop", methods=["GET", "POST"])
def pagina_pop():
    if "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            return render_template("pop.html")
        if request.method == "POST":
            dt_end1 = request.form.get("dt_end1")
            task_name = request.form.get("task_name")
            resp_ = request.form.get("resp_")
            material = request.form.get("material")
            passos = request.form.get("passos")
            manuseio = request.form.get("manuseio")
            resultados = request.form.get("resultados")
            acoes = request.form.get("acoes")
            tbPop = Pop()

            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            if tbPop.pop(dt_end1, task_name, resp_, material, passos, manuseio, resultados, acoes, cod_aluno, turma):
                flash("alert('Parabéns, você acaou de realizar o processo de registro de POP!!🎉')")
                return redirect ('/')
            else:
                return 'Erro ao realizar o processo de POP'
    else:
        return redirect("/login")

# roteamento da página dos processos de registro rnc
# RF006
@app.route("/rnc", methods=["GET", "POST"])
def pagina_rnc():
    if  "usuario_logado" in session or "professor_logado" in session:
        if request.method == "GET":
            #conectando com o banco de dados
            mydb = Conexao.conectar()
            
            mycursor = mydb.cursor()
            
            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            produtos = (f"SELECT * FROM {turma}.tb_cadastramento")
            
            mycursor.execute(produtos)
            
            resultado = mycursor.fetchall()
            
            lista_produtos = []
            
            for produto in resultado:
                lista_produtos.append({
                    "codigo":produto[0],
                    "descricao":produto[1],
                    "modelo":produto[2],
                    "fabricante":produto[3],
                    "numero_lote":produto[4],
                    "enderecamento":produto[5]
                })

            return render_template("rnc.html", lista_produtos = lista_produtos)
        if request.method == "POST":
            data = request.form.get("date")
            numRNC = request.form.get("numRNC")
            local = request.form.get("local")
            qtdentregue = request.form.get("qtdentregue")
            qtdrepro = request.form.get("qtdrepro")
            descRNC = request.form.get("descRNC")
            respInsp = request.form.get("respInsp")
            codProd = request.form.get("codProd")

            tbrnc = Rnc()

            if "usuario_logado" in session:           
                turma = session['usuario_logado']['turma']
                cod_aluno = session['usuario_logado']['cod_aluno']
            else:
                turma = session['professor_logado']['turma']
                cod_aluno = session['professor_logado']['cod_aluno']

            if tbrnc.rnc(descRNC, data, numRNC, local, qtdentregue, qtdrepro, respInsp, codProd, cod_aluno, turma):
                flash("alert('Parabéns, você acaou de realizar o processo de Registro de Não Conformidade!!🎉')")
                return redirect("/")
            else:
                return 'Erro ao realizar o processo de RNC'
    
    else:
        return redirect("/login")
    
# @app.route("/api/get/produtos")
# def get_produtos():
#     #conectando com o banco de dados
#     mydb = Conexao.conectar()
    
#     mycursor = mydb.cursor()
    
#     produtos = ("SELECT * FROM databaseProfessor.tb_cadastramento")
    
#     mycursor.execute(produtos)
    
#     resultado = mycursor.fetchall()
    
#     lista_produtos = []
    
#     for produto in resultado:
#         lista_produtos.append({
#             "codigo":produto[0],
#             "descricao":produto[1],
#             "modelo":produto[2],
#             "fabricante":produto[3],
#             "numero_lote":produto[4],
#             "enderecamento":produto[5]
#         })
#     return jsonify(lista_produtos), 200

# Roteamento da página que cria os bancos de dados para cada turma 
# RF011
@app.route("/criarBD", methods=["GET", "POST"])
def criarBD():
    if "professor_logado" in session:
        if request.method == "GET":
            return render_template("professor.html")
        if request.method == "POST":
            nomeBD = request.form.get("nomeTurma")
            criarDataBase = Professor()

            if criarDataBase.criaDatabse(nomeBD):
                flash("alert('Parabéns, você acaou de criar uma nova turma!!🎉')")
                return redirect("/")
            else:
                return "Erro ao criar o banco de dados"
    else:
        return "Acesso negado", 403

# roteamento da página que o professor utiliza para enviar mensagens para os alunos 
@app.route("/enviar_mensagem", methods=["GET", "POST"])
def enviar_mensagens():
    if "professor_logado" in session:
        # Conectando ao banco de dados
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        if request.method == "GET":
            # Consulta ao banco de dados para obter as mensagens
            consulta_mensagens = "SELECT cod_mensagem, mensagens FROM databaseProfessor.tb_mensagens"
            mycursor.execute(consulta_mensagens)
            resultado = mycursor.fetchall()
            
            lista_mensagens = []
            for mensagem in resultado:
                lista_mensagens.append({
                    "cod_mensagem": mensagem[0],
                    "mensagem": mensagem[1]
                })

            mydb.close()

            return render_template("mensagem.html", lista_mensagens=lista_mensagens)

        if request.method == "POST":
            # Conectando ao banco de dados
            mydb = Conexao.conectar()
            mycursor = mydb.cursor()
            # Pega a mensagem do formulário
            mensagem = request.form.get("mensagem")
            bancoDados = request.form.get("turma")

            # Inserir a nova mensagem no banco de dados
            inserir_mensagem = f"INSERT INTO tb_mensagens (mensagens, turma) VALUES (%s, %s)"
            mycursor.execute(inserir_mensagem, (mensagem, bancoDados))
            mydb.commit()

            flash("alert('Mensagem enviada para a turma com sucesso! 🎉')")
            mydb.close()

            return redirect("/")


@app.route("/excluir_mensagem", methods=["POST"])
def excluir_mensagem():
    if "professor_logado" in session:
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

            flash("alert('Mensagem excluída com sucesso!')")
        else:
            flash("alert('Erro ao excluir a mensagem. ID inválido.')")
    
    return redirect("/")


@app.route("/professor/listarBD")
def listar_bancos():
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

@app.route("/professor/excluirBD/<nomeBD>", methods=["POST"])
def excluir_banco(nomeBD):
    if "professor_logado" in session:
        mydb = Conexao.conectar()
        mycursor = mydb.cursor()

        # Comando para excluir o banco de dados
        mycursor.execute(f"DROP DATABASE IF EXISTS {nomeBD}")

        # Remover o banco de dados da tabela de referência
        mycursor.execute("DELETE FROM databaseprofessor.tb_database WHERE nomeBase = %s", (nomeBD,))
        
        mydb.commit()
        mycursor.close()
        mydb.close()

        flash("alert('Turma finalizada com sucesso!!🎉')")
        return redirect("/professor/listarBD")
    else:
        return "Acesso negado", 403


if  __name__ == "__main__":
    app.run(debug=True, host="0.0.0", port=8080)  # Iniciando o servidor com debug ativado


app.run(debug=True)