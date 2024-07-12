from sqlalchemy import Column, String, Integer, Boolean
from model import Base


class Tarefa(Base):
    __tablename__ = 'tarefa'

    id = Column("pk_tarefa", Integer, primary_key=True)  # Define a coluna 'id' como a chave primária.
    titulo = Column(String(140), unique=True)  # nome da tarefa é único
    concluida = Column(Boolean)

    def __init__(self, titulo: str, concluida: bool = False):
        """
        Cria uma Tarefa

        Arguments:
            titulo: nome da tarefa.
            concluida: diz se a tarefa foi concluída.
        """
        self.titulo = titulo
        self.concluida = concluida
