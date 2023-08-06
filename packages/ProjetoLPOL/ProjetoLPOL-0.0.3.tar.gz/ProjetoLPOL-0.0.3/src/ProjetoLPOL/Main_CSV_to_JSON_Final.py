from pathlib import Path
import os

def tipo_arquivo(filename):
    if filename.endswith('.csv'):
        return 'csv'
    else:
        return 'json'

def read_csv(input_path: Path, delimiter: str =",") -> list[list[str]]:
    items = []

    with open(input_path, encoding='utf-8-sig') as f:
        lines = f.readlines()
    
    items = [line.strip().split(delimiter) for line in lines]

    return items

def muda_csv_json(data: list[list[str]]) -> list[dict[str,str]]:
    column = data[0]
    lines = data[1:]
    return [dict(zip(column, line)) for line in lines]

def grava_linha(line: tuple, io, append_comma: bool):
    key, value = line
    if append_comma:
        io.write(f'\t\t"{key}": "{value}",\n')
    else:
        io.write(f'\t\t"{key}": "{value}"\n')

def grava_dicionario(data: dict, io, append_comma: True):
    io.write("\t{\n")
    items = tuple(data.items())
    for line in items[:-1]:
        grava_linha(line, io, append_comma=True)
    grava_linha(items[-1], io, append_comma=False)
    io.write("\t}")
    if append_comma:
        io.write(",\n")
    else:
        io.write("\n")

def grava_json(data: list[dict[str,str]], output_path: Path):
    '''escreve um dicionario json em disco no endereco'''
    with open(output_path, mode='w', encoding='utf-8') as f:
        f.write("[\n")
        for d in data[:-1]:
            grava_dicionario(d, f, append_comma=True)
        grava_dicionario(data[-1], f, append_comma=False)
        f.write("]\n")

def d_CSV_JSON(filename, output, delimitador):
    items = read_csv(filename, delimitador)
    json_data = muda_csv_json(items)
    grava_json(json_data, output)

def trata_arquivo(filename):
    linhas_tratadas =[]
    
    #abre o arquivo, trata as linhas e adiciona na variavel somente quem possue chave
    with open(filename, encoding='utf-8') as f:
        for line in f:
            if ':' in line:
                line = line.replace(" ", "").replace("\n", "").replace("\t", "")
                linhas_tratadas.append(line)

    return linhas_tratadas

def busca_header(filename):
    header =[]
    lines = trata_arquivo(filename)

    for i in range(0, len(lines)):
        inicial = lines[i].find('"')
        final = lines[i].find(":")
        
        lines[i] = lines[i][inicial+1:final-1]

    return list(dict.fromkeys(lines))

def d_JSON_CSV(filename, output):
    cabecalho = busca_header(filename)
    lines = trata_arquivo(filename)
    Arquivo_final = []
    cabecalho_temporario = ''

    #input do header no arquivo CSV
    for c in cabecalho:
        if not cabecalho_temporario =='':
            cabecalho_temporario = cabecalho_temporario + ',' + c
        else:
             cabecalho_temporario = cabecalho_temporario + c   
    
    #adiciona o cabelho na versao final do arquivo
    Arquivo_final.append(cabecalho_temporario.replace(',',';'))

    #remove as chaves das linhas do arquivo
    for l in range(0,len(lines)):
        for c in cabecalho:
            lines[l] = lines[l].replace(c, "")

    #remove alguns outros caracteres das linhas
    cabe = len(cabecalho)
    for _ in range(0,cabe):
        line = ''
        virgula = ';'
        for m in range(0,len(lines)):
            if m+1 == cabe: virgula = ''
            line = line + lines[m].replace('"','').replace(':','').replace(',','') + virgula
            if m+1 == cabe:
                Arquivo_final.append(line)
                line = ''
                cabe += len(cabecalho)
                virgula = ';'

    #grava os dados no arquivo convertido
    with open(output, mode='w') as file:
        file.writelines(["%s\n" % item for item in Arquivo_final])


def executar():
    filename = ''
    while not os.path.isfile(filename):
        print('\nNome do arquivo de origem:')
        filename = input()

    print('\nNome do arquivo de saída:')
    output = input()
    tipo_arquivo_origem = tipo_arquivo(filename)
    if tipo_arquivo_origem == 'csv':
        delimitador = ''
        while delimitador not in [',',';']:
            print('\nInforme o delimitador ("," ou ";"):')
            delimitador = input()

    '''
    filename = 'ExemploProfessor.json'
    output = 'ExemploProfessorOi.csv'
    delimitador = ';'
    '''

    tipo_arquivo_origem = tipo_arquivo(filename)

    if tipo_arquivo_origem == "json":
        d_JSON_CSV(filename, output)
    else:
        d_CSV_JSON(filename, output, delimitador)

if __name__ == "__main__":
    executar()