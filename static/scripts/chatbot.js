const caixaTexto = document.getElementById("caixaTexto");

const mensagensHome = [
    "Olá! 👋",
    "Seja bem-vindo ao meu site pessoal.",
    "Aqui você encontra meu currículo, contatos e projetos."
];

const mensagensCurriculo = [
    "Esse é o meu currículo.",
    "Aqui você encontra minha formação, experiências e tecnologias.",
    "Você também pode baixar o PDF pelo botão disponível na página."
];

const mensagensAlgoritmo = [
    "Bem-vindo aos meus projetos e códigos.",
    "Aqui estão exemplos de algoritmos em Python, com explicação e botão de copiar.",
    "A página agora está responsiva para computador e celular."
];

let mensagens;

if (document.title.includes("Currículo")) {
    mensagens = mensagensCurriculo;
} else if (document.title.includes("Meus projetos e códigos")) {
    mensagens = mensagensAlgoritmo;
} else {
    mensagens = mensagensHome;
}

let indiceMensagem = 0;
let indiceLetra = 0;

function escrever() {
    if (!caixaTexto || !mensagens || mensagens.length === 0) return;

    if (indiceLetra < mensagens[indiceMensagem].length) {
        caixaTexto.innerHTML += mensagens[indiceMensagem][indiceLetra];
        indiceLetra++;
        setTimeout(escrever, 70);
        return;
    }

    indiceLetra = 0;
    indiceMensagem++;

    if (indiceMensagem < mensagens.length) {
        caixaTexto.innerHTML += "<br><br>";
        setTimeout(escrever, 350);
    }
}

document.addEventListener("DOMContentLoaded", escrever);
