from Controller.ConectaBdChamados import ConectaBdChamados
from Controller.BuscaChamados import BuscaChamados
from Controller.ConectaBdTSE import ConectaBdTSE
from Controller.ControlerTSE import ControlerTSE

# Conectar ao banco de chamados
string_conexao_bd_chamados = ConectaBdChamados(host='', port='', user='', password='', dbname='')
conexao_bd_chamados = string_conexao_bd_chamados.RealizaConexaoBdChamado()

# Verificar se a conexão foi bem-sucedida
if conexao_bd_chamados is None:
    print("Não foi possível conectar ao banco de dados.")
    exit()

# Instanciar a classe BuscaChamados
classe_chamados = BuscaChamados(conexao_bd_chamados)

# Buscar a lista de chamados
lista_chamados = classe_chamados.BuscaChamadosParaMovimentar()
if lista_chamados is None or not lista_chamados:
    print("Lista está vazia!")

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
teste = classe_tse.LiberaSala(lista_ids_funcionarios_desvinculados)

#Altera o status do processo
classe_chamados.AlteraStatusBdChamados(teste)
# Desconectar do banco de dados
string_conexao_bd_chamados.DesconectaBdChamados()
