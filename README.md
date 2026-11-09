# CifraFlow

[![CI](https://github.com/MauricioApCastro/cifraflow/actions/workflows/ci.yml/badge.svg)](https://github.com/MauricioApCastro/cifraflow/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/python-3.10%2B-blue)
![PyQt6](https://img.shields.io/badge/GUI-PyQt6-41cd52)

Leitor de letras e cifras para músicos que **acompanha a música pela sua voz**. Enquanto você canta, o CifraFlow ouve o microfone, reconhece a frase e destaca automaticamente a próxima linha, sem precisar tirar as mãos do instrumento.

Um projeto [MAC Tecnology](https://mactecnology.com.br).

## Funcionalidades

- **Abrir música:** carrega a letra/cifra de um arquivo de texto (`.txt`).
- **Acompanhamento por voz:** reconhece em português o que você canta e avança o destaque quando a frase atual termina.
- **Linha centralizada:** a linha atual fica sempre no meio da tela.
- **Modo Palco:** fonte maior e tela limpa para usar no show ou no ensaio.
- **Indicador de volume** do microfone e status do reconhecimento em tempo real.

## Requisitos

- Python 3.10 ou superior
- Microfone
- Conexão com a internet (o reconhecimento de voz usa o serviço do Google)

## Como executar

```bash
git clone https://github.com/MauricioApCastro/cifraflow.git
cd cifraflow

python -m venv .venv
# Windows: .venv\Scripts\activate   |   Linux/macOS: source .venv/bin/activate

pip install -r requirements.txt
python main.py
```

Coloque suas músicas em `.txt` na pasta `musicas/` e abra pelo botão **Abrir Música**.

## Privacidade

Quando o microfone está ligado, trechos curtos de áudio são enviados ao serviço de reconhecimento de voz do Google para virar texto. Nada é gravado em disco e o áudio não é enviado para a MAC Tecnology. Veja a [política de privacidade](https://mactecnology.com.br/privacidade.html).

## Estrutura

```
├── main.py               # ponto de entrada e tema escuro
├── controllers/          # lógica de acompanhamento da letra
├── services/             # captura de áudio e transcrição de voz
├── views/                # janela principal (PyQt6)
└── musicas/              # suas letras e cifras em .txt
```

## Desenvolvimento

```bash
pip install -r requirements-dev.txt
ruff check .          # análise de código
ruff format .         # formatação automática
```

O GitHub Actions roda essas verificações a cada envio para a branch `main`.

## Autor

**Maurício Castro** · [MAC Tecnology](https://mactecnology.com.br) · contato@mactecnology.com.br
