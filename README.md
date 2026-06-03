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

Python 3.14 

Download oficial: https://www.python.org/downloads/ 

Poetry (para gerenciar dependências) 

https://python-poetry.org/docs/ 

 

Instalação do poetry:  
```
pip install pipx 

pipx install poetry 
```
 

### Clonar o repositório 
```
git clone https://github.com/rafaelguerreiro77/raizes.git 
```
 

### Entrar na pasta 
```
cd raizes 
```
 

 

### Instalar as dependências 
```
poetry install 
```
 

### Ativar ambiente virtual 
```
poetry shell 
```
 

### Criar arquivo `.env` 

Na raiz do projeto, criar um arquivo chamado `.env` com o conteúdo: 
```
DATABASE_URL=sqlite:///./database.db 

CHAVE=senha_de_acesso_raizes_com_32_caracteres 

ALGORITIMO=HS256 

TOKEN_EXPIRA=20 
```
 

### Criar banco de dados (Alembic) 
```
alembic upgrade head 
```
 

### Rodar a API 
```
task run 
```
 

### Documentação (Swagger) 

Acesse pelo navegador: 

http://127.0.0.1:8000/docs 

 

### Testes com Postman 

Collection incluída na pasta:

postman/Raizes API.postman_collection.json 

 

### Autenticação usando JWT  

Login 

Post     http://localhost:8000/auth/token/ 

Body (form-data / x-www-form-urlencoded) 
```
username: email 
password: senha 
 ```

 

### Comandos taskipy  

Rodar API 
```
task run 
```
 

Formatar código 
```
task format 
```
 

Rodar testes 
```
task test 
```
 

Rodar lint 
```
task lint 
```
 

### Estrutura projeto 
```
raizes/
├── raizes/        # aplicação
├── tests/         # testes
├── migrations/    # banco
├── postman/       # testes API
├── pyproject.toml
└── README.md
```

### Autor 

Rafael Andreazzi Guerreiro 
