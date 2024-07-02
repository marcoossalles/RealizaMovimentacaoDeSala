from Controller.ConectaBdChamados import ConectaBdChamados
from Controller.BuscaChamados import BuscaChamados
from Controller.ConectaBdTSE import ConectaBdTSE
from Controller.ControlerTSE import ControlerTSE
import logging
logging.basicConfig(filename='/home/gav/Projetos/Python/RealizaMovimentacaoSala/log.txt',level=logging.WARNING, format='%(asctime)s - %(levelname)s - %(message)s')


# Conectar ao banco de chamados
string_conexao_bd_chamados = ConectaBdChamados(host='', port='', user='', password='', dbname='')
conexao_bd_chamados = string_conexao_bd_chamados.RealizaConexaoBdChamado()

# Verificar se a conexão foi bem-sucedida
if conexao_bd_chamados is None:
    logging.error("Não foi possível conectar ao banco de dados.")
    exit()

# Instanciar a classe BuscaChamados
classe_chamados = BuscaChamados(conexao_bd_chamados)

# Buscar a lista de chamados
lista_chamados = classe_chamados.BuscaChamadosParaMovimentar()
if lista_chamados is None or not lista_chamados:
    logging.warning("Lista está vazia!")
    exit()

# Conectar ao banco do TSE
string_conexao_bd_tse = ConectaBdTSE(host='', port='', user='', password='', dbname='')
conexao_bd_tse = string_conexao_bd_tse.RealizaConexaoBdTSE()

# Instanciar a classe
classe_tse = ControlerTSE(conexao_bd_tse)

#Busca Lista Id Funcionario 
lista_ids_funcionarios = classe_tse.BuscaIdsFuncionario(lista_chamados)

#Desvincula Sala
lista_ids_funcionarios_desvinculados = classe_tse.DesvinculaSala(lista_ids_funcionarios)

#Libera Sala de Vendas
lista_processo_realizado_com_sucesso = classe_tse.LiberaSala(lista_ids_funcionarios_desvinculados)

#Altera o status do processo
classe_chamados.AlteraStatusBdChamados(lista_processo_realizado_com_sucesso)
# Desconectar do banco de dados
string_conexao_bd_chamados.DesconectaBdChamados()
