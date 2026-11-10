from helpers.database import get_conn


class InstituicaoEnsinoRepository:

    def getAllInstituicoes(self):
        # abre a conexão com o banco de dados
        conn = get_conn()

        # cria um um cursor, obj responsavel por executar comandos SQL e navegar pelos resultados
        cursor = conn.cursor()

        # executa a DML de consulta
        cursor.execute(f'SELECT * FROM tb_instituicao_ensino')

        # fetchall pega todos os registros retornados pelo banco e os armazena na variavel dataset
        dataset = cursor.fetchall()

        return dataset

    def getByIdIntituicoes(self, id):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute(f'SELECT * FROM tb_instituicao_ensino WHERE id = ?', (id,))

        row = cursor.fetchone()

        return row

    def postInstituicoes(self, data):
        conn = get_conn()
        cursor = conn.cursor()

        # insere os dados
        (cursor.execute
         ('''
            INSERT INTO tb_instituicao_ensino 
            (no_entidade, co_entidade, no_uf, sg_uf, co_uf, no_municipio, co_municipio, 
             nu_ano_censo, qt_mat_bas, qt_mat_inf, qt_mat_fund, qt_mat_med, qt_mat_prof, qt_mat_eja, qt_mat_esp) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) 
            RETURNING *
        ''', (
            data.get("no_entidade"), data.get("co_entidade"), data.get("no_uf"),
            data.get("sg_uf"), data.get("co_uf"), data.get("no_municipio"),
            data.get("co_municipio"), data.get("nu_ano_censo"), data.get("qt_mat_bas"),
            data.get("qt_mat_inf"), data.get("qt_mat_fund"), data.get("qt_mat_med"),
            data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp")
        )))

        row = cursor.fetchone()

        conn.commit()

        return row

    def putInstituicoes(self, id, data):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tb_instituicao_ensino 
            SET no_entidade = ?, co_entidade = ?, no_uf = ?, sg_uf = ?, co_uf = ?, 
                no_municipio = ?, co_municipio = ?, nu_ano_censo = ?, qt_mat_bas = ?, 
                qt_mat_inf = ?, qt_mat_fund = ?, qt_mat_med = ?, qt_mat_prof = ?, 
                qt_mat_eja = ?, qt_mat_esp = ?
            WHERE id = ?
            RETURNING *
        ''', (
            data.get("no_entidade"), data.get("co_entidade"), data.get("no_uf"),
            data.get("sg_uf"), data.get("co_uf"), data.get("no_municipio"),
            data.get("co_municipio"), data.get("nu_ano_censo"), data.get("qt_mat_bas"),
            data.get("qt_mat_inf"), data.get("qt_mat_fund"), data.get("qt_mat_med"),
            data.get("qt_mat_prof"), data.get("qt_mat_eja"), data.get("qt_mat_esp"),
            id
        ))

        row = cursor.fetchone()

        # só confirma a transação se encontrou o registro
        if row is not None:
            conn.commit()

        return row

    def deleteInstituicoes(self, id):
        conn = get_conn()
        cursor = conn.cursor()

        cursor.execute('''
            UPDATE tb_instituicao_ensino SET ativo = 0 
            WHERE id = ? AND ativo = 1 RETURNING no_entidade, ativo ''', (id,))

        row = cursor.fetchone()

        # só confirma a transação se encontrou o registro
        if row is not None:
            conn.commit()

        return row