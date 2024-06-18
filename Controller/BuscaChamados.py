import psycopg2

class BuscaChamados:
    def __init__(self, conexao_bd):
        self.conexao_bd = conexao_bd

    def BuscaChamadosParaMovimentar(self):
        cursor = self.conexao_bd.cursor()
        query = """SELECT * FROM chamadosmovimentacao"""
        try:
            cursor.execute(query)
            lista_chamados = cursor.fetchall()
            return lista_chamados
        except psycopg2.Error as error:
            print(f"Erro ao buscar chamados banco interno: {error}")
            return None

    def AlteraStatusBdChamados(self, lista_chamados):
        if self.conexao_bd is None:
            print("Falha com a conexão do banco de dados!")
            return

        cursor = self.conexao_bd.cursor()
        for item in lista_chamados:
            try:
                query = f"""UPDATE chamadosmovimentacao
                            SET statusmovimentacao = false
                            WHERE idchamado = {item[1]};"""
                cursor.execute(query)
            except Exception as error:
                print(f"Ocorreu um erro: {error} ao realizar a alteração do status do chamado!")
        self.conexao_bd.commit()

