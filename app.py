from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from model import Session
from logger import logger
from model.tarefa import Tarefa
from schemas import *
from flask_cors import CORS

info = Info(title="API Gerenciamento de Tarefas", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
home_tag = Tag(name="Documentação Swagger", description="Documentação estilo Swagger.")
tarefa_tag = Tag(name="Tarefa", description="Adição, visualização e remoção de tarefas na base de dados.")


def home():
    """Redireciona para documentação da API no estilo Swagger.
    """
    return redirect('/openapi/swagger')


@app.post('/tarefa', tags=[tarefa_tag],
          responses={"200": TarefaViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_tarefa(form: TarefaSchema):
    """Adiciona uma nova Tarefa à base de dados

    Retorna uma representação das tarefas cadastradas.
    """

    tarefa = Tarefa(
        titulo=form.titulo,
        concluida=form.concluida
    )

    logger.debug(f"Adicionando tarefa: '{tarefa.titulo}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando tarefa
        session.add(tarefa)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado tarefa: '{tarefa.titulo}'")
        return apresenta_tarefa(tarefa), 200

    except IntegrityError as e:
        # A duplicidade do nome da tarefa é a provável razão do IntegrityError
        error_msg = "Uma tarefa com o mesmo titulo já existe."
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.titulo}', {error_msg}")
        return {"mensagem": error_msg}, 409

    except Exception as e:
        # caso ocorra um erro fora do previsto
        error_msg = "Não foi possível salvar uma nova tarefa."
        logger.warning(f"Erro ao adicionar tarefa '{tarefa.titulo}', {error_msg}, {e}")
        return {"mensagem": error_msg}, 400


@app.get('/tarefa/todas', tags=[tarefa_tag],
         responses={"200": ListagemTarefasSchema, "404": ErrorSchema})
def get_tarefas():
    """Faz a busca por todos os Tarefas cadastrados.

    Retorna uma representação da listagem de tarefas.
    """
    logger.debug(f"Coletando tarefas ")

    session = Session()
    tarefas = session.query(Tarefa).all()

    if not tarefas:
        return {"tarefas": []}, 200
    else:
        logger.debug(f"%d tarefas econtrados" % len(tarefas))
        print(tarefas)
        return apresenta_tarefas(tarefas), 200

@app.get('/tarefa/titulo', tags=[tarefa_tag],
         responses={"200": TarefaViewSchema, "404": ErrorSchema})
def get_tarefa(query: TarefaBuscaSchema):
    """Faz a busca por um Tarefa a partir do nome da tarefa

    Retorna uma representação das tarefas cadastrados.
    """
    tarefa_titulo = query.tarefa.strip().lower()  # Remove espaços e converte para minúsculas
    logger.debug(f"Coletando dados sobre tarefa #{tarefa_titulo}")

    session = Session()

    # fazendo a busca, usando ilike para busca insensível a maiúsculas/minúsculas
    task = session.query(Tarefa).filter(
        func.lower(Tarefa.titulo).ilike(f"%{tarefa_titulo}%")).first()

    if not task:
        error_msg = "Tarefa não encontrado."
        logger.warning(f"Erro ao buscar tarefa '{tarefa_titulo}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(f"Tarefa encontrada: '{task.titulo}'")
        return apresenta_tarefa(task), 200

@app.delete('/tarefa/titulo', tags=[tarefa_tag],
            responses={"200": TarefaDelSchema, "404": ErrorSchema})
def del_tarefa(query: TarefaBuscaSchema):
    """Deleta um Tarefa a partir do nome da tarefa informada.

    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_titulo = unquote(unquote(query.tarefa))
    print(tarefa_titulo)
    logger.debug(f"Deletando dados da tarefa #{tarefa_titulo}")

    session = Session()

    count = session.query(Tarefa).filter(Tarefa.titulo== tarefa_titulo).delete()
    session.commit()

    if count:
        logger.debug(f"Deletada tarefa #{tarefa_titulo}")
        return {"mesage": "Tarefa removida", "id": tarefa_titulo}
    else:
        error_msg = "Tarefa não encontrada."
        logger.warning(f"Erro ao deletar tarefa #'{tarefa_titulo}', {error_msg}")
        return {"mensagem": error_msg}, 404


@app.delete('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaDelIdSchema, "404": ErrorSchema})
def del_tarefa_id(query: TarefaIdSchema):
    """Deleta um Tarefa a partir do id da tarefa informada.

    Retorna uma mensagem de confirmação da remoção.
    """
    tarefa_id = query.id
    print(tarefa_id)
    logger.debug(f"Deletando dados sobre tarefa #{tarefa_id}")

    session = Session()

    count = session.query(Tarefa).filter(Tarefa.id== tarefa_id).delete()
    session.commit()

    if count:
        logger.debug(f"Deletada tarefa #{tarefa_id}")
        return {"mensagem": "Tarefa removido", "id": tarefa_id}
    else:
        error_msg = "Tarefa não encontrado."
        logger.warning(f"Erro ao deletar tarefa #'{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404

@app.get('/tarefa', tags=[tarefa_tag],
            responses={"200": TarefaViewSchema, "404": ErrorSchema})
def get_tarefa_id(query: TarefaIdSchema):
    """Faz a busca por um Tarefa a partir do ID da tarefa

    Retorna uma representação da tarefa.
    """
    tarefa_id = query.id
    print(tarefa_id)
    logger.debug(f"Coletando dados sobre tarefa de id:{tarefa_id}")

    session = Session()

    task = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()

    if not task:
        error_msg = "Tarefa não encontrado."
        logger.warning(f"Erro ao buscar tarefa de id:'{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404
    else:
        logger.debug(f"Tarefa encontrada: '{task.titulo}'")
        return apresenta_tarefa(task), 200

@app.put('/tarefa/concluida', tags=[tarefa_tag],
            responses={"200": TarefaViewSchema, "404": ErrorSchema})
def put_tarefa_concluida(query: TarefaIdSchema):
    """Marca uma Tarefa como concluída ou não a partir do id da tarefa informada.

    Retorna uma mensagem de confirmação da modificação.
    """
    tarefa_id = query.id
    print(tarefa_id)
    logger.debug(f"Marcando como concluida a tarefa de id:{tarefa_id}")
    session = Session()
    tarefa = session.query(Tarefa).filter(Tarefa.id == tarefa_id).first()
    if tarefa:
        tarefa.concluida = not tarefa.concluida
        session.commit()
        logger.debug(f"Tarefa de id: {tarefa.id} marcada como {'não' if tarefa.concluida else ''} concluída")
        return apresenta_tarefa(tarefa), 200

    else:
        error_msg = "Tarefa não encontrada."
        logger.warning(f"Erro ao buscar tarefa de id:'{tarefa_id}', {error_msg}")
        return {"mensagem": error_msg}, 404