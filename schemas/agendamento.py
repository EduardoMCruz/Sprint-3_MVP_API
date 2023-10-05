from pydantic import BaseModel
from typing import Optional, List
from model.agendamento import Agendamento
from datetime import datetime


class AgendamentoSchema(BaseModel):
    """ Define como um novo agendamento a ser inserido deve ser representado
    """
    
    codigo: int
    nome: str
    telefone: str
    categoria: str
    especialidade: Optional[str]
    c_data: Optional[str]
    c_hora: Optional[str]

class AgendamentoUpdateSchema(BaseModel):
    """ Define como um agendamento a ser editado deve ser representado
    """
    
    nome: str
    telefone: str
    categoria: str
    especialidade: Optional[str]
    c_data: Optional[str]
    c_hora: Optional[str]
        
class AgendamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do agendamento.
    """
    codigo: int = 1

class ListagemAgendamentosSchema(BaseModel):
    """ Define como uma listagem de agendamentos será retornada.
    """
    agendamentos:List[AgendamentoSchema]

class IntegracaoSchema(BaseModel):
    """ Define como uma mensagem de erro será representada
    """
    mesage: str

def apresenta_agendamentos(agendamentos: List[Agendamento]):
    """ Retorna uma representação do agendamento.
    """
    lista_agendamentos = []
    for agendamento in agendamentos:
        lista_agendamentos.append({
            "codigo": agendamento.codigo, 
            "nome": agendamento.nome,
            "telefone": agendamento.telefone,
            "categoria": agendamento.categoria,
            "especialidade": agendamento.especialidade,
            "c_data": agendamento.c_data,
            "c_hora": agendamento.c_hora
        })

    return {"agendamentos": lista_agendamentos}

def apresenta_agendamento(agendamento: Agendamento):
    """ Retorna uma representação do agendamento.
    """
    return {
        "codigo": agendamento.codigo, 
        "nome": agendamento.nome,
        "telefone": agendamento.telefone,
        "categoria": agendamento.categoria,
        "especialidade": agendamento.especialidade,
        "c_data": agendamento.c_data,
        "c_hora": agendamento.c_hora
    }



class AgendamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    codigo: int

class AgendamentoViewSchema(BaseModel):
    """ Define como um agendamento será retornado.
    """
    codigo: int = 1
    nome: str = "Eduardo Cesar"
    telefone: str = "(DD) NNNN-NNNN"
    categoria: str = "Retorno"
    especialidade: Optional[str] = "Pediatra"
    c_data: Optional[str] = "dd/mm/aaaa"
    c_hora: Optional[str] = "MM:HH"
    data_insercao: Optional[datetime] = datetime.today()