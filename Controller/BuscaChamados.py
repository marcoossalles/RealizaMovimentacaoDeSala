import psycopg2
import logging
logging.basicConfig(filename='/home/gav/Projetos/Python/BuscaChamados/log.txt',level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


class BuscaChamados:
    def __init__(self, conexao_bd):
        self.conexao_bd = conexao_bd

    def BuscaChamadosParaMovimentar(self):
        cursor = self.conexao_bd.cursor()
        query = """SELECT * FROM chamadosmovimentacao WHERE date(datainsercao) = CURRENT_DATE;"""
        try:
            cursor.execute(query)
            lista_chamados = cursor.fetchall()
            return lista_chamados
        except psycopg2.Error as error:
            logging.error(f"Erro ao buscar chamados banco interno: {error}")
            return None

    def AlteraStatusBdChamados(self, lista_processo_realizado_com_sucesso):
        if self.conexao_bd is None:
            logging.error("Falha com a conexão do banco de dados!")
            return

        cursor = self.conexao_bd.cursor()
        for item in lista_processo_realizado_com_sucesso:
            try:
                query = f"""UPDATE chamadosmovimentacao
                            SET statusmovimentacao = true
                            WHERE idchamado = {item[1]};"""
                cursor.execute(query)
            except Exception as error:
                logging.error(f"Ocorreu um erro: {error} ao realizar a alteração do status do chamado!")
        self.conexao_bd.commit()

