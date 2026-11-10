from flask import Blueprint, request
from helpers.database import get_conn
from schema.InstituicaoEnsinoSchema import InstituicaoEnsinoSchema
from services.instituicao_service import InstituicaoService
from marshmallow import ValidationError

instituicao_bp = Blueprint("instituicao", __name__)
instituicoes_schema = InstituicaoSchema()

@instituicao_bp.get("/instituicoesensino")
def getAllInstituicoes():
    conn = get_conn()
    service = InstituicaoService(conn)
    
    lista_instituicoes = service.listar_todas()
    response = instituicoes_schema.dump(lista_instituicoes, many=True)
    return response, 200

@instituicao_bp.get("/instituicoesensino/<int:id>")
def getByIdIntituicoes(id):
    conn = get_conn()
    service = InstituicaoService(conn)
    
    instituicao = service.buscar_por_id(id)
    if instituicao is None:
        return "intituição não encontrada", 404

    response = instituicoes_schema.dump(instituicao)
    return response, 200

@instituicao_bp.post("/instituicoesensino")
def postInstituicoes():
    try:
        data = instituicoes_schema.load(request.get_json())
        
        conn = get_conn()
        service = InstituicaoService(conn)
        
        instituicao = service.criar(data)
        response = instituicoes_schema.dump(instituicao)
        
        return response, 201
    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

@instituicao_bp.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    try:
        data = instituicoes_schema.load(request.get_json())
        
        conn = get_conn()
        service = InstituicaoService(conn)
        
        instituicao = service.atualizar(id, data)
        if instituicao is None:
            return {"erro": "Instituição não encontrada"}, 404

        response = instituicoes_schema.dump(instituicao)
        return response, 200

    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

@instituicao_bp.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    conn = get_conn()
    service = InstituicaoService(conn)
    
    row = service.deletar(id)
    if row is None:
        return {"erro": "Instituição não encontrada"}, 404

    nome = row[0]
    ativo = row[1]
    return {"sucesso": True, "no_entidade": nome, "ativo": ativo}, 200