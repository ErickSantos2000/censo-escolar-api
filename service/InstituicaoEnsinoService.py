from schema.InstituicaoEnsinoSchema import InstituicaoEnsinoSchema
from mapper.InstituicaoEnsinoMapper import InstituicaoEnsinoMapper
from repository.InstituicaoEnsinoRepository import InstituicaoEnsinoRepository


class InstituicaoEnsinoService:

    def __init__(self):
        self.instituicoes_schema = InstituicaoEnsinoSchema()
        self.instituicaoEnsinoMapper = InstituicaoEnsinoMapper()
        self.repository = InstituicaoEnsinoRepository()

    def get_all(self):
        listaIntuicoesEnsino = []

        dataset = self.repository.getAllInstituicoes()

        # percorre cada linha da tupla retornada pelo dataset
        for row in dataset:
            instituicaoEnsino = self.instituicaoEnsinoMapper.to_entity(row)

            listaIntuicoesEnsino.append(instituicaoEnsino)

        # converte e monta a lista de resposta com todas as inttuições de ensino do banco
        insituicoesEnsinoReponse = self.instituicoes_schema.dump(listaIntuicoesEnsino, many=True)

        return insituicoesEnsinoReponse

    def get_by_id(self, id):
        row = self.repository.getByIdIntituicoes(id)

        # retorna None quando não encontra (o controller devolve o 404)
        if row is None:
            return None

        instituicaoEnsino = self.instituicaoEnsinoMapper.to_entity(row)

        insituicaoEnsinoReponse = self.instituicoes_schema.dump(instituicaoEnsino)

        return insituicaoEnsinoReponse

    def create(self, json_data):
        # valida os dados (pode lançar ValidationError, tratado no controller)
        data = self.instituicoes_schema.load(json_data)

        row = self.repository.postInstituicoes(data)

        instituicaoEnsino = self.instituicaoEnsinoMapper.to_entity(row)

        insituicaoEnsinoReponse = self.instituicoes_schema.dump(instituicaoEnsino)

        return insituicaoEnsinoReponse

    def update(self, id, json_data):
        # valida os dados (pode lançar ValidationError, tratado no controller)
        data = self.instituicoes_schema.load(json_data)

        row = self.repository.putInstituicoes(id, data)

        # retorna None quando não encontra (o controller devolve o 404)
        if row is None:
            return None

        instituicaoEnsino = self.instituicaoEnsinoMapper.to_entity(row)

        instituicoesEnsinoResponse = self.instituicoes_schema.dump(instituicaoEnsino)

        return instituicoesEnsinoResponse

    def delete(self, id):
        row = self.repository.deleteInstituicoes(id)

        # retorna None quando não encontra (o controller devolve o 404)
        if row is None:
            return None

        nome = row[0]
        ativo = row[1]

        return {"sucesso": True, "no_entidade": nome, "ativo": ativo}