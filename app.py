from flask_openapi3 import OpenAPI, Info, Tag
from sqlalchemy.exc import IntegrityError
from flask_cors import CORS
from flask import redirect
import requests

from model import Session, Agendamento
from schemas import *

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
agendamento_tag = Tag(name="Agendamento", description="Cria, lista e remove agendamentos da base")
integracao_tag = Tag(name="Integrações", description="Serviços de integração com outras APIs")

def verifica_existencia_especialidade(nome_especialidade):
    """
    Verifica se um especialidade existe na API de especialidades
    """
    # Chamada à API de especialidade para verificar se o especialidade existe
    url = f'http://172.17.0.1:5001/especialidade?nome={nome_especialidade}'
    response = requests.get(url)
    
    if response.status_code == 200:
        # O especialidade existe
        return True
    else:
        # O especialidade não existe
        return False

@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/agendamento', tags=[agendamento_tag],
          responses={"200": AgendamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_agendamento(form: AgendamentoSchema):
    """Adiciona um novo Agendamento à base de dados. Quando preenchido, verifica se o especialidade informado existe na API de especialidades.
    """
    especialidade=form.especialidade
    if especialidade!=None:
        if not verifica_existencia_especialidade(especialidade):
            error_msg = "O especialidade especificado não existe"
            return {"message": error_msg}, 400

    agendamento = Agendamento(
        codigo=form.codigo, 
        nome=form.nome,
        telefone=form.telefone,
        categoria=form.categoria,
        especialidade=especialidade,
        c_data=form.c_data,
        c_hora=form.c_hora)
    
    try:
        session = Session()
        session.add(agendamento)
        session.commit()
        return apresenta_agendamento(agendamento), 200

    except IntegrityError as e:
        error_msg = "Não foi possível cadastrar o agendamento, pois já existe um agendamento com esse código"
        print("erro: agendamento já cadastrado")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Erro inesperado, o agendamento inserido não foi cadastrado"
        print("erro!")
        return {"mesage": error_msg}, 400


@app.get('/agendamentos', tags=[agendamento_tag],
         responses={"200": ListagemAgendamentosSchema, "404": ErrorSchema})
def get_agendamentos():
    """Retorna uma listagem de agendamentos cadastrados na base.
    """
    
    session = Session()
    agendamentos = session.query(Agendamento).all()

    if not agendamentos:
        return {"agendamentos": []}, 200
    return apresenta_agendamentos(agendamentos), 200

@app.get('/agendamento', tags=[agendamento_tag],
            responses={"200": AgendamentoViewSchema, "404": ErrorSchema})
def get_agendamento(query: AgendamentoBuscaSchema):
    """Encontra um Agendamento a partir do nome informado

    Retorna o agendamento.
    """
    codigo = query.codigo
    session = Session()
    agendamento = session.query(Agendamento).filter(Agendamento.codigo == codigo).first()
    if agendamento:
        return apresenta_agendamento(agendamento), 200
    error_msg = "Agendamento não encontrado"
    return {"mesage": error_msg}, 404

@app.put('/agendamento', tags=[agendamento_tag],
          responses={"200": AgendamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def edit_agendamento(query: AgendamentoBuscaSchema, form: AgendamentoUpdateSchema):
    """Edita um Agendamento existente na base de dados. Quando preenchido, verifica se o especialidade informado existe na API de especialidades.
    """
    codigo=query.codigo
    especialidade=form.especialidade
    if especialidade!=None:
        if not verifica_existencia_especialidade(especialidade):
            error_msg = "O especialidade especificado não existe"
            return {"message": error_msg}, 400
    session = Session()
    agendamento = session.query(Agendamento).filter(Agendamento.codigo == codigo).first()

    if agendamento is None:
        error_msg = "Não foi possível editar o agendamento, pois não existe um agendamento com esse código"
        return {"message": error_msg}, 409
    
    try:
        agendamento.nome = form.nome
        agendamento.telefone = form.telefone
        agendamento.categoria = form.categoria
        agendamento.especialidade = especialidade
        agendamento.c_data = form.c_data
        agendamento.c_hora = form.c_hora
        session.commit()
        return apresenta_agendamento(agendamento), 200

    except IntegrityError as e:
        error_msg = "Não foi possível editar o agendamento, pois não existe um agendamento com esse código"
        print("erro: agendamento não existente")
        return {"mesage": error_msg}, 409

    except Exception as e:
        error_msg = "Erro inesperado, o agendamento não foi editado"
        print("erro na edição!")
        return {"mesage": error_msg}, 400
    

@app.delete('/agendamento', tags=[agendamento_tag],
            responses={"200": AgendamentoDelSchema, "404": ErrorSchema})
def del_agendamento(query: AgendamentoBuscaSchema):
    """Deleta um Agendamento a partir do nome informado

    Retorna uma mensagem de confirmação da remoção.
    """
    codigo = query.codigo
    session = Session()
    count = session.query(Agendamento).filter(Agendamento.codigo == codigo).delete()
    session.commit()

    if count:
        return {"mesage": "Agendamento removido", "agendamento": codigo}
    error_msg = "Agendamento não encontrado"
    return {"mesage": error_msg}, 404
    