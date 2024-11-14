function pesquisar() {
    var input, filtro, tabela, linhas, textoLinha;

    input = document.getElementById('pesquisa');
    filtro = removerAcentos(input.value.toUpperCase());

    tabela = document.querySelector(".tabela-inventario tbody");
    linhas = tabela.querySelectorAll('tr');

    linhas.forEach(linha => {
        textoLinha = Array.from(linha.querySelectorAll('td'))
        .map(coluna => removerAcentos(coluna.textContent.toUpperCase()))
        .join(" ");

        if (textoLinha.indexOf(filtro) > -1) {
            linha.style.display = "";
        } else {
            linha.style.display = "none";
        }
    });
}

function removerAcentos(texto) {
    return texto.normalize("NFD").replace(/[\u0300-\u036f]/g, "");
}