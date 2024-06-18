import psycopg2
import json
from datetime import datetime
import logging

class ControlerTSE:
    def __init__(self, conexao_bd_tse):
        self.conexao_bd_tse = conexao_bd_tse

    def BuscaIdsFuncionario(self, lista_chamados):
        cursor = self.conexao_bd_tse.cursor()
        lista_ids_funcionarios = []
        for chamado in lista_chamados:
            if chamado[5] == None:
                try:
                    cursor.execute(f"""SELECT idfuncionario FROM funcionario inner join pessoa on funcionario.idpessoa = pessoa.idpessoa where pessoa.cpfcnpj = '{chamado[4]}'""")
                    resultado = cursor.fetchone()
                    if resultado:
                        lista_ids_funcionarios.append((resultado[0], chamado[1], chamado[2], chamado[3], chamado[4]))
                    else:
                        print(f"Nenhum funcionário encontrado para o CPF: {chamado[4]}")
                except psycopg2.Error as error:
                    print(f"Erro ao realizar busca ID funcionario: {error}")
                    pass
            else:
                try:
                    cursor.execute(f"""SELECT idfuncionario FROM funcionario inner join pessoa on funcionario.idpessoa = pessoa.idpessoa where pessoa.cpfcnpj = '{chamado[5]}'""")
                    resultado = cursor.fetchone()
                    if resultado:
                        lista_ids_funcionarios.append((resultado[0], chamado[1], chamado[2], chamado[3], chamado[4]))
                    else:
                        print(f"Nenhum funcionário encontrado para o CPF: {chamado[5]}")
                except psycopg2.Error as error:
                    print(f"Erro ao realizar busca ID funcionario: {error}")
                    pass
        return lista_ids_funcionarios

    def DesvinculaSala(self, lista_ids_funcionarios):
        cursor = self.conexao_bd_tse.cursor()
        
        for item in lista_ids_funcionarios:
            query = f"""update  permissaoacessounidadenegocio set permitido = 'false' where idunidadenegociopermissao not in(163,9,4,64,192,25) and permitido = 'true' and idfuncionariopermissao = {item[0]}"""
            try:
                cursor.execute(query)
                self.conexao_bd_tse.commit()
            except psycopg2.Error as error:
                print(f"Erro ao desvincular sala:{item[0]} ERROR:{error}")
                lista_ids_funcionarios.remove(item)
                pass
        return lista_ids_funcionarios

    def VerificaSeSalaFoiVinculada(self, chaveAtual, id_funcionario):
        try:
            cursor = self.conexao_bd_tse.cursor()
            query = f"select permitido from permissaoacessounidadenegocio where idunidadenegociopermissao  in({chaveAtual}) and idfuncionariopermissao = {id_funcionario}"
            cursor.execute(query)
            resultado = cursor.fetchone()
            return resultado
        except psycopg2.Error as error:
            print(f"Ocorreu um erro: {error} ao verifica o id funcionario: {id_funcionario}, chava da sala: {chaveAtual}")
            return True


    def LiberaSala(self, lista_ids_funcionarios_desvinculados):
        cursor = self.conexao_bd_tse.cursor()

        with open('ListaCodSalas.json', encoding='utf-8') as f:lista_cod_salas = json.load(f)
        data_cadastro = datetime.now()
        cod_user_isercao = 781
        permite = 'true'

        for item in lista_ids_funcionarios_desvinculados:
            try:
                sala = item[3]
                id_funcionario = item[0]
                codigosSalaDeVenda = lista_cod_salas[0][sala]
                contaCod = 1
                chaveCod = f'cod{contaCod}'
                while True:
                    if chaveCod in codigosSalaDeVenda:
                        chaveAtual = codigosSalaDeVenda[chaveCod]
                        resultado = self.VerificaSeSalaFoiVinculada(chaveAtual, id_funcionario)
                        match resultado[0]:
                            case True:
                                print(f"Id: {id_funcionario} ja vinculado a sala: {chaveAtual}")
                            case False:
                                cursor.execute(f"""update  permissaoacessounidadenegocio set permitido = 'true' where idunidadenegociopermissao in({chaveAtual}) and permitido = 'false' and idfuncionariopermissao = {id_funcionario}""")
                                self.conexao_bd_tse.commit()
                            case None:
                                cursor.execute("""INSERT INTO public.permissaoacessounidadenegocio(idrespcadastro, idunidadenegociopermissao, permitido, datacadastro, idfuncionariopermissao) VALUES(%s, %s, %s, %s, %s)""", (cod_user_isercao, chaveAtual, permite, data_cadastro, id_funcionario))
                                self.conexao_bd_tse.commit()                        
                    else:
                        break
                    contaCod += 1
                    chaveCod = f'cod{contaCod}'
            except Exception as error:
                lista_ids_funcionarios_desvinculados.remove(item)
                logging.error(f"Erro ao realizar a liberação da sala: {error} id funcionario: {id_funcionario}")
                pass
        return lista_ids_funcionarios_desvinculados