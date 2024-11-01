// // Código para o input de TROCAR TURMAS ---------------------------------------------------
// document.querySelectorAll('.select-menu').forEach(menu => {
//     const selectBtn = menu.querySelector('.select-btn');
//     const options = menu.querySelectorAll('.option');
//     const sBtnText = menu.querySelector('.sBtn-text');

//     selectBtn.addEventListener('click', () => {
//         menu.classList.toggle('active');
//     });

//     options.forEach(option => {
//         option.addEventListener('click', () => {
//             let selectedOption = option.querySelector('.option-text').innerText;
//             sBtnText.innerText = selectedOption;
//             menu.classList.remove('active');
//         });
//     });
// });

// //----------------------------------------------------------------------------------------------------------------

// document.addEventListener("DOMContentLoaded", function() {
//     // Botões e seções principais
//     const signupBtn = document.getElementById("signup-btn");
//     const loginBtn = document.getElementById("login-btn");
//     const introSection = document.getElementById("intro-section");
//     const registerSection = document.getElementById("register-section");
//     const loginSection = document.getElementById("login-section");

//     // Seções de cadastro
//     const alunoRegisterBtn = document.getElementById("aluno-register-btn");
//     const professorRegisterBtn = document.getElementById("professor-register-btn");
//     const registerAluno = document.getElementById("register-aluno");
//     const registerProfessor = document.getElementById("register-professor");
//     const connectBoxRegister = document.querySelector("#register-section .connect-box");

//     // Seções de login
//     const alunoLoginBtn = document.getElementById("aluno-login-btn");
//     const professorLoginBtn = document.getElementById("professor-login-btn");
//     const loginAluno = document.getElementById("login-aluno");
//     const loginProfessor = document.getElementById("login-professor");
//     const connectBoxLogin = document.getElementById("connect-login");

//     // Função para exibir a tela de cadastro
//     signupBtn.addEventListener("click", function() {
//         introSection.style.display = "none";
//         registerSection.style.display = "flex";
//         connectBoxRegister.style.display = "block";
//         registerAluno.style.display = "none";
//         registerProfessor.style.display = "none";
//     });

//     function exibirLogin(){
//         introSection.style.display = "none";
//         loginSection.style.display = "block";
//         connectBoxLogin.style.display = "block";
//         loginAluno.style.display = "none";
//         loginProfessor.style.display = "none";
//     }

//     // Função para exibir a tela de login
//     loginBtn.addEventListener("click", function() {
//         exibirLogin()
//     });


//     // Função para exibir o cadastro do aluno
//     alunoRegisterBtn.addEventListener("click", function() {
//         connectBoxRegister.style.display = "none";
//         registerAluno.style.display = "block";
//         registerProfessor.style.display = "none";
//     });

//     // Função para exibir o cadastro do professor
//     professorRegisterBtn.addEventListener("click", function() {
//         connectBoxRegister.style.display = "none";
//         registerProfessor.style.display = "block";
//         registerAluno.style.display = "none";
//     });

//     function exibirLoginAluno(){
//         connectBoxLogin.style.display = "none";
//         loginAluno.style.display = "block";
//         loginProfessor.style.display = "none";
//     };

//     // Função para exibir o login do aluno
//     alunoLoginBtn.addEventListener("click", function() {
//         exibirLoginAluno();
//     });

//     function exibirLoginProfessor(){
//         connectBoxLogin.style.display = "none";
//         loginProfessor.style.display = "block";
//         loginAluno.style.display = "none";
//     };

//     // Função para exibir o login do professor
//     professorLoginBtn.addEventListener("click", function() {
//         exibirLoginProfessor();
//     });


//     // Função para voltar à tela de seleção no cadastro
//     document.querySelectorAll("#voltar-register").forEach(button => {
//         button.addEventListener("click", function() {
//             registerSection.style.display = "flex";
//             connectBoxRegister.style.display = "block";
//             registerAluno.style.display = "none";
//             registerProfessor.style.display = "none";
//         });
//     });

//     // Função para voltar à tela de seleção no login
//     document.querySelectorAll("#voltar-login").forEach(button => {
//         button.addEventListener("click", function() {
//             loginSection.style.display = "block";
//             connectBoxLogin.style.display = "block";
//             loginAluno.style.display = "none";
//             loginProfessor.style.display = "none";
//         });
//     });
// });


// Código para o input de TROCAR TURMAS ---------------------------------------------------
document.querySelectorAll('.select-menu').forEach(menu => {
    const selectBtn = menu.querySelector('.select-btn');
    const options = menu.querySelectorAll('.option');
    const sBtnText = menu.querySelector('.sBtn-text');

    selectBtn.addEventListener('click', () => {
        menu.classList.toggle('active');
    });

    options.forEach(option => {
        option.addEventListener('click', () => {
            let selectedOption = option.querySelector('.option-text').innerText;
            sBtnText.innerText = selectedOption;
            menu.classList.remove('active');
        });
    });
});

//----------------------------------------------------------------------------------------------------------------

document.addEventListener("DOMContentLoaded", function() {
    // Botões e seções principais
    const signupBtn = document.getElementById("signup-btn");
    const loginBtn = document.getElementById("login-btn");
    const introSection = document.getElementById("intro-section");
    const registerSection = document.getElementById("register-section");
    const loginSection = document.getElementById("login-section");

    // Seções de cadastro
    const alunoRegisterBtn = document.getElementById("aluno-register-btn");
    const professorRegisterBtn = document.getElementById("professor-register-btn");
    const registerAluno = document.getElementById("register-aluno");
    const registerProfessor = document.getElementById("register-professor");
    const connectBoxRegister = document.querySelector("#register-section .connect-box");

    // Seções de login
    const alunoLoginBtn = document.getElementById("aluno-login-btn");
    const professorLoginBtn = document.getElementById("professor-login-btn");
    const loginAluno = document.getElementById("login-aluno");
    const loginProfessor = document.getElementById("login-professor");
    const connectBoxLogin = document.getElementById("connect-login");

    // Função para exibir a tela de cadastro
    signupBtn.addEventListener("click", function() {
        introSection.style.display = "none";
        registerSection.style.display = "flex";
        connectBoxRegister.style.display = "block";
        registerAluno.style.display = "none";
        registerProfessor.style.display = "none";
    });

    function exibirLogin(){
        introSection.style.display = "none";
        loginSection.style.display = "block";
        connectBoxLogin.style.display = "block";
        loginAluno.style.display = "none";
        loginProfessor.style.display = "none";
    }

    // Função para exibir a tela de login
    loginBtn.addEventListener("click", function() {
        exibirLogin()
    });

    // Função para exibir o cadastro do aluno
    alunoRegisterBtn.addEventListener("click", function() {
        connectBoxRegister.style.display = "none";
        registerAluno.style.display = "block";
        registerProfessor.style.display = "none";
    });

    // Função para exibir o cadastro do professor
    professorRegisterBtn.addEventListener("click", function() {
        connectBoxRegister.style.display = "none";
        registerProfessor.style.display = "block";
        registerAluno.style.display = "none";
    });

    function exibirLoginAluno(){
        connectBoxLogin.style.display = "none";
        loginAluno.style.display = "block";
        loginProfessor.style.display = "none";
    };

    // Função para exibir o login do aluno
    alunoLoginBtn.addEventListener("click", function() {
        exibirLoginAluno();
    });

    function exibirLoginProfessor(){
        connectBoxLogin.style.display = "none";
        loginProfessor.style.display = "block";
        loginAluno.style.display = "none";
    };

    // Função para exibir o login do professor
    professorLoginBtn.addEventListener("click", function() {
        exibirLoginProfessor();
    });

    // Função para voltar à tela de seleção no cadastro
    document.querySelectorAll("#voltar-register").forEach(button => {
        button.addEventListener("click", function() {
            registerSection.style.display = "flex";
            connectBoxRegister.style.display = "block";
            registerAluno.style.display = "none";
            registerProfessor.style.display = "none";
        });
    });

    // Função para voltar à tela de seleção no login
    document.querySelectorAll("#voltar-login").forEach(button => {
        button.addEventListener("click", function() {
            loginSection.style.display = "block";
            connectBoxLogin.style.display = "block";
            loginAluno.style.display = "none";
            loginProfessor.style.display = "none";
        });
    });

    // Função para enviar os dados de cadastro do aluno e verificar duplicatas
    document.querySelector('#register-aluno form').addEventListener('submit', function(event) {
        event.preventDefault(); // Previne o envio automático do formulário

        // Coleta os dados do formulário
        const nome = document.querySelector("input[name='nome']").value;
        const email = document.querySelector("input[name='email']").value;
        const senha = document.querySelector("input[name='senha']").value;
        const turma = document.querySelector("input[name='turma']").value;

        // Cria um objeto com os dados
        const dados = {
            tipo: "Aluno",  // Adicione o tipo de usuário aqui
            nome: nome,
            email: email,
            senha: senha,
            turma: turma
        };

        // Envia os dados para o backend para verificar duplicatas
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados),
        })
        .then(response => {
            if (response.status === 409) {
                alert('Erro: Usuário já cadastrado com este email.');
            } else if (response.status === 201) {
                alert('Cadastro realizado com sucesso! Realize o login.');
                window.location.href = '/login'; // Redireciona para o login
            } else {
                alert('Erro ao tentar realizar o cadastro.');
            }
        })
        .catch(error => {
            console.error('Erro ao realizar o cadastro:', error);
        });
    });

    // Função para enviar os dados de cadastro do professor e verificar duplicatas
    document.querySelector('#register-professor form').addEventListener('submit', function(event) {
        event.preventDefault(); // Previne o envio automático do formulário

        // Coleta os dados do formulário
        const nome = document.querySelector("#register-professor input[name='nome']").value;
        const email = document.querySelector("#register-professor input[name='email']").value;
        const senha = document.querySelector("#register-professor input[name='senha']").value;

        // Cria um objeto com os dados
        const dados = {
            tipo: "Professor", // Adicione o tipo de usuário aqui
            nome: nome,
            email: email,
            senha: senha
        };

        // Envia os dados para o backend para verificar duplicatas
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados),
        })
        .then(response => {
            if (response.status === 409) {
                alert('Erro: Usuário já cadastrado com este email.');
            } else if (response.status === 201) {
                alert('Cadastro realizado com sucesso! Realize o login.');
                window.location.href = '/login'; // Redireciona para o login
            } else {
                alert('Erro ao tentar realizar o cadastro.');
            }
        })
        .catch(error => {
            console.error('Erro ao realizar o cadastro:', error);
        });
    });

    // Função para enviar os dados de login do aluno
    document.querySelector('#login-aluno form').addEventListener('submit', function(event) {
        event.preventDefault(); // Previne o envio automático do formulário

        // Coleta os dados do formulário
        const email = document.querySelector("#login-aluno input[name='email']").value;
        const senha = document.querySelector("#login-aluno input[name='senha']").value;
        const turma = document.querySelector("#login-aluno input[name='turma']").value;

        // Cria um objeto com os dados
        const dados = {
            tipo: "LoginAluno",
            email: email,
            senha: senha,
            turma: turma
        };

        // Envia os dados para o backend para realizar o login
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados),
        })
        .then(response => {
            if (response.ok) {
                // Login bem-sucedido
                alert('Login realizado com sucesso! Seja bem vindo ao ambiente educacional.');
                window.location.href = '/'; // Redireciona para a página inicial
            } else {
                alert('Email ou senha incorretos.');
            }
        })
        .catch(error => {
            console.error('Erro ao tentar fazer login:', error);
        });
    });

    // Função para enviar os dados de login do professor
    document.querySelector('#login-professor form').addEventListener('submit', function(event) {
        event.preventDefault(); // Previne o envio automático do formulário

        // Coleta os dados do formulário
        const email = document.querySelector("#login-professor input[name='email']").value;
        const senha = document.querySelector("#login-professor input[name='senha']").value;

        // Cria um objeto com os dados
        const dados = {
            tipo: "LoginProfessor",
            email: email,
            senha: senha
        };

        // Envia os dados para o backend para realizar o login
        fetch('/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(dados),
        })
        .then(response => {
            if (response.ok) {
                // Login bem-sucedido
                alert('Login realizado com sucesso! Seja bem vindo ao ambiente educacional.');
                window.location.href = '/'; // Redireciona para a página inicial
            } else {
                alert('Email ou senha incorretos.');
            }
        })
        .catch(error => {
            console.error('Erro ao tentar fazer login:', error);
        });
    });



});