import pandas as pd
import numpy as np
from sys import argv

np.random.seed(41)

## Fatoracao
def sgd(avaliacoes, K = 225, alpha = 0.002, reg = 0.05, epocas = 20):

    P = np.random.uniform(0.2, 1.0, size=(M, K))*(5)/np.sqrt(np.sqrt(5)*K)
    Q = np.random.uniform(0.2, 1.0, size=(K, N))*(5)/np.sqrt(np.sqrt(5)*K)

    erros_final = []
    
    for i in range(epocas):

        
        erros = []
        
        for avaliacao in avaliacoes:
            
            usuario, item = avaliacao
            rating = avaliacoes[avaliacao]
    
            linha_usuario = usuario_para_linha[usuario]
            coluna_item = item_para_coluna[item]
            
            erro = rating - P[linha_usuario,:]@Q[:,coluna_item]

            erros.append(erro)
    
            nova_linha = P[linha_usuario,:] + alpha*(erro*Q[:,coluna_item] - reg*P[linha_usuario,:])
            nova_coluna = Q[:,coluna_item] + alpha*(erro*P[linha_usuario,:] - reg*Q[:,coluna_item])
    
            P[linha_usuario,:] = nova_linha
            Q[:,coluna_item] = nova_coluna

        erros_final.append(np.mean(erros))

    
    return P, Q


## Predicao
def predicao(P, Q, usuario, item):

    linha_usuario = usuario_para_linha[usuario]
    coluna_item = item_para_coluna[item]

    return P[linha_usuario,:]@Q[:,coluna_item]
    
    
## Leitura das tabelas
avaliacoes = pd.read_csv(argv[1])
novas_colunas = avaliacoes["UserId:ItemId"].str.split(":", n = 1, expand = True)

avaliacoes["UserId"]= novas_colunas[0] 
avaliacoes["ItemId"]= novas_colunas[1] 
avaliacoes.drop(columns =["UserId:ItemId"], inplace = True) 


usuario_para_linha = avaliacoes['UserId'].unique()
usuario_para_linha = {valor: indice for indice, valor in enumerate(usuario_para_linha)}

M = len(usuario_para_linha)


item_para_coluna = avaliacoes['ItemId'].unique()
item_para_coluna = {valor: indice for indice, valor in enumerate(item_para_coluna)}

N = len(item_para_coluna)


avaliacoes_usuarios = {}

for index, linha in avaliacoes.iterrows():

    avaliacoes_usuarios[(linha['UserId'],linha['ItemId'])] = linha["Rating"]
    

alvos = pd.read_csv(argv[2])
novas_colunas = alvos["UserId:ItemId"].str.split(":", n = 1, expand = True)
alvos["UserId"] = novas_colunas[0]
alvos["ItemId"]= novas_colunas[1] 
alvos.drop("UserId:ItemId", axis = 1, inplace = True)


## Execucao
if __name__ == "__main__":

    fatores_latentes_usuarios, fatores_latentes_itens = sgd(avaliacoes_usuarios)

    print("UserId:ItemId,Rating")

    for linha in alvos.itertuples(index=False):

        usuario_alvo = linha[0]
        item_alvo = linha[1]

        avaliaca_predita = predicao(fatores_latentes_usuarios, fatores_latentes_itens, usuario_alvo, item_alvo)

        avaliaca_predita = min(5, avaliaca_predita)
        avaliaca_predita = max(1, avaliaca_predita)
    
        print(usuario_alvo + ":" + item_alvo + "," + str(avaliaca_predita))

