import psycopg2
import logging
logging.basicConfig(filename='/home/gav/Projetos/Python/BuscaChamados/log.txt',level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')

class ConectaBdTSE:
    def __init__(self, host, port, user, password, dbname):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.dbname = dbname
        self.conexao = None

    def RealizaConexaoBdTSE(self):
        try:
            self.conexao = psycopg2.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                dbname=self.dbname
            )
            print(f"Conexão bem-sucedida ao banco de dados {self.dbname}.")
        except psycopg2.OperationalError as e:
            logging.error(f"O erro '{e}' ocorreu ao tentar conectar ao banco de dados {self.dbname}.")
        return self.conexao

    def DesconectaBdChamados(self):
        if self.conexao:
            self.conexao.close()
            logging.info(f"Conexão com o banco de dados {self.dbname} fechada.")