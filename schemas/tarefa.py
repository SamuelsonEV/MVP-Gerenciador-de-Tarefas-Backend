from pydantic import BaseModel
from typing import List
from model.tarefa import Tarefa


class TarefaSchema(BaseModel):
    """ Define como uma nova tarefa deve ser representada ao ser inserida.
    """
    id: int = 0
    titulo: str = "Exemplo de Tarefa"
    concluida: bool = False


class TarefaBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome da tarefa.
    """
    tarefa: str = "Exemplo de Tarefa"


class TarefaIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a exclusão, busca ou modificação da
    tarefa pelo id.
    """
    id: int = 0


class ListagemTarefasSchema(BaseModel):
    """ Define como uma listagem de tarefas será retornada.
    """
    tarefas:List[TarefaSchema]


def apresenta_tarefas(tarefas: List[Tarefa]):
    """ Retorna uma representação da tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    result = []
    for tarefa in tarefas:
        result.append({
            "id": tarefa.id,
            "titulo": tarefa.titulo,
            "concluida": tarefa.concluida,
        })

    return {"tarefas": result}


class TarefaViewSchema(BaseModel):
    """ Define como uma tarefa será retornadoa.
    """
    id: int = 0
    titulo: str = "Exemplo de Tarefa"
    concluida: bool = False
   

class TarefaDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    tarefa: str

class TarefaDelIdSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mensagem: str
    id: int

def apresenta_tarefa(tarefa: Tarefa):
    """ Retorna uma representação da Tarefa seguindo o schema definido em
        TarefaViewSchema.
    """
    return {
        "id": tarefa.id,
        "titulo": tarefa.titulo,
        "concluida": tarefa.concluida,
    }
