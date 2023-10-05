# Sobre o projeto
Essa API é o home de consultas, onde é possivel marcar consultas pegando informações dos médicos cadastrados.

## Como executar em modo desenvolvimento


Instalar todas as libs python listadas no `requirements.txt`.
Copiar o repositório para uma pasta local e executar os comandos abaixo pelo terminal após entrar no diretório do repositório:

1- Criar uma virtualenv
```
virtualenv nome_da_virtualenv
```

2- Ativar a virtualenv
```
nome_da_virtualenv\Scripts\Activate
```

3- Instalar as bibliotecas do arquivo requirements.txt 
```
(env)$ pip install -r requirements.txt
```

4- Executar a API:

```
(env)$ flask run --host 0.0.0.0 --port 5000
```
5- Após uma mudança no código fonte:

```
(env)$ flask run --host 0.0.0.0 --port 5000 --reload
```

6 - Abrir o [http://localhost:5000/#/](http://localhost:5000/#/) no navegador para verificar o status da API em execução.

## Como executar em modo desenvolvimento

Certifique-se de ter o [Docker](https://docs.docker.com/engine/install/) instalado e em execução em sua máquina.

Navegue até o diretório que contém o Dockerfile no terminal.
Execute **como administrador** o seguinte comando para construir a imagem Docker:

```
$ docker build -t mvp_api .
```

Uma vez criada a imagem, para executar o container basta executar, **como administrador**, seguinte o comando:

```
$ docker run -p 5000:5000 mvp_api
```

Uma vez executando, para acessar a documentação em Swagger, basta abrir o [link](http://localhost:5000/openapi/swagger) no navegador.