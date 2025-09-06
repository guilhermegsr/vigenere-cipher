# 🔐 Trabalho 01 - Cifra de Vigenère

Este projeto implementa a **Cifra de Vigenère** e um **ataque de análise de frequência** para recuperação de chave.  
Faz parte da disciplina **Segurança Computacional (CIC0201)**.

---

## 🚀 Funcionalidades

- **Cifrador/Decifrador**
  - Implementação da cifra de Vigenère.
  - Preserva caracteres não alfabéticos.
  - Chave validada automaticamente.

- **Ataque por Análise de Frequência**
  - Estimativa do tamanho da chave usando **Índice de Coincidência (IC)**.
  - Recuperação da chave usando **análise de frequências + teste qui-quadrado**.
  - Redução automática de chaves cíclicas (ex.: `ABCABCABC` → `ABC`).

- **Relatórios**
  - Geração de tabelas com métricas (CSV).
  - Gráficos salvos em PNG:
    - IC médio por tamanho de chave.
    - Distribuição de qui-quadrado por coluna.

---

## 📂 Estrutura do Projeto
```
vigenere-cipher/
│
├── crypto/
│ ├── __init__.py
│ └── vigenere.py
│
├── analyser/
│ ├── __init__.py
│ └── vigenere_analyser.py
│
├── tests/
│ └── test_vigenere.py
│
├── texts/
│ ├── sample_pt.txt
│ ├── sample_en.txt
│
├── results/
│ ├── ic_scores.csv
│ ├── ic_scores.png
│ ├── column_metrics.csv
│ ├── column_0_scores.png
│ ├── ...
│
├── main.py
├── requirements.txt
├── .gitignore
└── README.md
```
---

## ⚙️ Instalação

1. Clone o repositório ou baixe os arquivos:
    ```bash
    git clone https://github.com/guilhermegsr/vigenere-cipher.git
    cd vigenere-cipher
    ```

2. Crie um ambiente virtual (opcional):
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```

3. Instale as dependências:
    ```bash
    pip install -r requirements.txt
    ```

## ▶️ Como executar

1. Coloque seus textos na pasta texts/

2. Execute o programa principal:

    ```bash
    python main.py
    ```

3. O programa irá:

    - Pedir a chave de cifragem.
    - Perguntar o idioma do texto (pt ou en).
    - Mostrar os arquivos disponíveis em `texts/` para você escolher.
    - Cifrar e decifrar o texto.
    - Rodar o ataque de análise de frequência.
    - Gerar tabelas e gráficos em `results/`.

## 📈 Saídas

- **results/ic_scores.csv** → IC médio por tamanho de chave.

- **results/ic_scores.png** → Gráfico IC × tamanho de chave.

- **results/column_metrics.csv** → Métricas por coluna (qui-quadrado).

- **results/column_X_scores.png** → Gráficos por coluna (teste qui-quadrado).