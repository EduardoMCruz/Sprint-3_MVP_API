from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base

class Agendamento(Base):
    __tablename__ = 'agendamento'

    codigo = Column("Código", Integer, primary_key=True)
    nome = Column(String(140))
    telefone = Column(String(140))
    categoria = Column(String(140))
    especialidade = Column(String(140))
    c_data = Column(String(140))
    c_hora = Column(String(140))

    def __init__(self, codigo: int, nome:str, telefone:str, categoria:str, especialidade:str, 
                 c_data:str, c_hora:str, 
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Agendamento eletrônico

        Arguments:
            codigo: 
            nome: 
            telefone: 
            categoria:
            especialidade: 
            c_data: 
            c_hora: 
            data_insercao: 
        """
        self.codigo = codigo
        self.nome = nome
        self.telefone = telefone
        self.categoria = categoria
        self.especialidade=especialidade
        self.c_data = c_data
        self.c_hora = c_hora

        if data_insercao:
            self.data_insercao = data_insercao
        else:
            self.data_insercao = datetime.today()