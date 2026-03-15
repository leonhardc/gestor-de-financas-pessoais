# Gestor de Finanças Pessoais

<p align="center">
    <img src="https://img.shields.io/badge/Por-Leonardo%20Rodrigues%20da%20Costa-blue"/>
    <img src="https://img.shields.io/badge/Status-Em_Andamento-green"/>
</p>

<h2 align='center'>Tecnologias Utilizadas</h2>

<br>
<div align='center'>
    <img src='https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white'/>
    <img src='https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white'/>
    <img src='https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white'/>
    <img src='https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white'/>
    <img src='https://img.shields.io/badge/JavaScript-323330?style=for-the-badge&logo=javascript&logoColor=F7DF1E'/>
    <img src='https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white'/>
</div>
<br>

## Descrição

Um gestor de finanças pessoais desenvolvido com Django que permite controlar receitas, despesas e acompanhar o orçamento pessoal de forma prática e eficiente.

## Como Executar

### Pré-requisitos
- Python 3.8+
- pip

### Passo a Passo

1. **Clone o repositório**
    ```bash
    git clone <url-do-repositorio>
    cd gestor-de-financas-pessoais
    ```

2. **Crie um ambiente virtual**
    ```bash
    python -m venv venv
    ```

3. **Ative o ambiente virtual**
    - No Windows:
      ```bash
      venv\Scripts\activate
      ```
    - No Linux/macOS:
      ```bash
      source venv/bin/activate
      ```

4. **Instale as dependências**
    ```bash
    pip install -r requirements.txt
    ```

5. **Execute as migrações**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```

6. **Inicie o servidor**
    ```bash
    python manage.py runserver
    ```

7. **Acesse a aplicação**
    Abra seu navegador e vá para `http://localhost:8000`

## Galeria de Fotos do Projeto

### Index

![Pagina Inicial](./img/index.png)

### Dashboard

![Dashboard](./img/dashboard.png)

### Contas

![Contas](./img/Contas.png)

### Transações

![Transacoes](./img/Transacoes.png)

### Categorias

![Categorias](./img/Categorias.png)

### Orçamentos

![Orcamentos](./img/Orcamentos.png)
