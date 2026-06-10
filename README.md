#  Projeto Raizes Backend 

 

Trata-se de um projeto de backend desenvolvido com FastAPI, utilizando Poetry para dependências, Alembic para migrations e Taskipy para automação de comandos. 

Projeto elaborado para estudo de backend, incluindo: 

CRUD de usuários e entidades 

Autenticação JWT para usuários 

Migrations com Alembic 

Testes com Swagger e Postman 

--- 

##  Tecnologias utilizadas 

Python 3.14

FastAPI

SQLAlchemy

Alembic

Poetry

Taskipy

SQLite

JWT

Postman

--- 

##  Instalação e Utilização do projeto 

### Requisitos 

Para utilizar o projeto Raízes, é necessário ter instalado: 

Python 3.14 ou superior (projeto desenvolvido com Python 3.14)

Download oficial: https://www.python.org/downloads/

Git (para clonar o repositório)

Download https://desktop.github.com/download/ 


### Clonar o repositório 
```
git clone https://github.com/rafaelguerreiro77/raizes.git 
```
 

### Entrar na pasta 
```
cd raizes 
```

### Poetry (para gerenciar dependências) 


Instalação do poetry:  
```
pip install --user pipx

pipx ensurepath

pipx install poetry

pipx inject poetry poetry-plugin-shell (opcional)
```


### Instalar as dependências 
```
poetry install 
```
 

### Ativar ambiente virtual (opcional)
```
poetry shell 
```
 

### Criar arquivo `.env` 

Na raiz do projeto, criar um arquivo chamado `.env` com o conteúdo: 
```
DATABASE_URL=sqlite:///database.db 

CHAVE=senha_de_acesso_raizes_com_32_caracteres 

ALGORITMO=HS256 

TOKEN_EXPIRA=20 
```
 

### Criar banco de dados (Alembic) 
```
poetry run alembic upgrade head 
```
 

### Rodar a API 
```
poetry run task run
```
 

### Documentação (Swagger) 

Acesse pelo navegador após iniciar o servidor: 

http://127.0.0.1:8000/docs 

 

### Testes com Postman 

Collection incluída na pasta:

postman/Raizes API.postman_collection.json 

 

### Autenticação usando JWT  

Antes de realizar o login, é necessário cadastrar um usuário com email e senha através do endpoint de criação de usuários.

Login 

Post     http://localhost:8000/auth/token/ 

Body (form-data / x-www-form-urlencoded) 
```
username: email 
password: senha 
 ```

 

### Comandos Taskipy

Os comandos abaixo utilizam o Taskipy e devem ser executados via Poetry.


Rodar API 
```
poetry run task run 
```
 

Formatar código 
```
poetry run task format 
```
 

Rodar testes 
```
poetry run task test 
```
 

Rodar lint 
```
poetry run task lint 
```
 

### Estrutura projeto 
```
raizes/
├── raizes/              # aplicação
├── tests/                # testes
├── migrations/      # banco
├── postman/          # testes API
├── pyproject.toml
└── README.md
```

### Autor 

Rafael Andreazzi Guerreiro 

