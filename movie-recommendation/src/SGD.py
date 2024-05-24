import numpy as np

class SGD:
    def __init__(self, row_user, column_item, M, N ):
        self.row_user = row_user
        self.column_item = column_item
        self.M = M
        self.N = N

    def sgd(self,ratings, K, alpha, reg, epoches):

        np.random.seed(41)

        P = np.random.uniform(0.2, 1.0, size=(self.M, K))*(5)/np.sqrt(np.sqrt(2)*K)
        Q = np.random.uniform(0.2, 1.0, size=(K, self.N))*(5)/np.sqrt(np.sqrt(2)*K)

        erros_final = []
        
        for i in range(epoches):        
            erros = []
            
            for avaliacao in ratings:
                
                usuario, item = avaliacao
                rating = ratings[avaliacao]
        
                linha_usuario = self.row_user[usuario]
                coluna_item = self.column_item[item]
                
                erro = rating - P[linha_usuario,:]@Q[:,coluna_item]

                erros.append(erro)
        
                nova_linha = P[linha_usuario,:] + alpha*(erro*Q[:,coluna_item] - reg*P[linha_usuario,:])
                nova_coluna = Q[:,coluna_item] + alpha*(erro*P[linha_usuario,:] - reg*Q[:,coluna_item])
        
                P[linha_usuario,:] = nova_linha
                Q[:,coluna_item] = nova_coluna

            erros_final.append(np.mean(erros))

        self.P = P
        self.Q = Q

        return P, Q

    def prediction(self,P, Q, user, item):

        user_row = self.row_user[user]
        item_col = self.column_item[item]

        return P[user_row,:]@Q[:,item_col]
