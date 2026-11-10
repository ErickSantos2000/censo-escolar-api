from flask import Blueprint, request
from marshmallow import ValidationError
from service.InstituicaoEnsinoService import InstituicaoEnsinoService

instituicao_bp = Blueprint("instituicoesensino", __name__)

instituicaoEnsinoService = InstituicaoEnsinoService()


@instituicao_bp.get("/instituicoesensino")
def getAllInstituicoes():
    insituicoesEnsinoReponse = instituicaoEnsinoService.get_all()

    return insituicoesEnsinoReponse, 200


@instituicao_bp.get("/instituicoesensino/<int:id>")
def getByIdIntituicoes(id):
    insituicaoEnsinoReponse = instituicaoEnsinoService.get_by_id(id)

    if insituicaoEnsinoReponse is None:
        return "intituição não encontrada", 404

    return insituicaoEnsinoReponse, 200


@instituicao_bp.post("/instituicoesensino")
def postInstituicoes():
    # Entrada do dado em Json.
    # Validação.
    try:
        insituicaoEnsinoReponse = instituicaoEnsinoService.create(request.get_json())
    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

    # Retorno.
    # Dado de entrada com identificador.
    return insituicaoEnsinoReponse, 201


@instituicao_bp.put("/instituicoesensino/<int:id>")
def putInstituicoes(id):
    try:
        instituicoesEnsinoResponse = instituicaoEnsinoService.update(id, request.get_json())

        if instituicoesEnsinoResponse is None:
            return {"erro": "Instituição não encontrada"}, 404

    except ValidationError as err:
        return {
            "erro": "Dados inválidos",
            "campos": err.messages
        }, 400

    return instituicoesEnsinoResponse, 200


@instituicao_bp.delete("/instituicoesensino/<int:id>")
def deleteInstituicoes(id):
    resposta = instituicaoEnsinoService.delete(id)

    if resposta is None:
        return {"erro": "Instituição não encontrada"}, 404

    return resposta, 200