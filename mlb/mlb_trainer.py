import player_splits
import regression_scraper
import numpy as np 

full_data = regression_scraper.getMLBData()

# Least squares estimate for Ax = b #

def createAMatrix(player):
    sorted_keys = sorted(full_data[player].keys())
    A_matr = None
    for i in sorted_keys:
        if not i == 'POS' and (not i == sorted_keys[0]): # only key that is not a date
            x1, x2, x3, x4 = full_data[player][i]['REG-OVERALL'], full_data[player][i]['REG-LAST-FIVE'], full_data[player][i]['REG-STADIUM-AVG'], full_data[player][i]['REG-TEAM-AVG']
            row = np.transpose(np.array([x1, x2, x3, x4]))
            if A_matr == None:
                A_matr = row
            else:
                A_matr = np.vstack([A_matr, row])
    return A_matr

def createAMatrixDate(player, date):
    sorted_keys = sorted(full_data[player].keys())
    print(sorted_keys)
    A_matr = None
    ind = sorted_keys.index(date)
    for i in sorted_keys:
        ind1 = sorted_keys.index(i)
        if not ind1 > ind-1:
            print("Using date: " + i + " for creating: " + date)
            if not i == 'POS' and (not i == sorted_keys[0]): # only key that is not a date
                x1, x2, x3, x4 = full_data[player][i]['REG-OVERALL'], full_data[player][i]['REG-LAST-FIVE'], full_data[player][i]['REG-STADIUM-AVG'], full_data[player][i]['REG-TEAM-AVG']
                row = np.transpose(np.array([x1, x2, x3, x4]))
                if A_matr == None:
                    A_matr = row
                else:
                    A_matr = np.vstack([A_matr, row])
    return A_matr

def createbMatrix(player):
    sorted_keys = sorted(full_data[player].keys())
    b = None
    for i in sorted_keys:
        if not i == 'POS' and (not i == sorted_keys[0]): # only key that is not a date
            if b == None:
                b = np.array([full_data[player][i]['FPTS']])
            else:
                b = np.vstack([b, np.array(full_data[player][i]['FPTS'])])
    return b

def createbMatrixDate(player, date):
    sorted_keys = sorted(full_data[player].keys())
    b = None
    ind = sorted_keys.index(date)
    for i in sorted_keys:
        ind1 = sorted_keys.index(i)
        if not ind1 > ind-1:
            if not i == 'POS' and (not i == sorted_keys[0]): # only key that is not a date
                if b == None:
                    b = np.array([full_data[player][i]['FPTS']])
                else:
                    b = np.vstack([b, np.array(full_data[player][i]['FPTS'])])
    return b

def trainModel(player):
    A = createAMatrix(player)
    y = createbMatrix(player)
    weights = np.linalg.lstsq(A, y)[0]
    return weights

def averageAccuracy(player):
    sorted_keys = sorted(full_data[player].keys())
    for i in range(3, len(sorted_keys) - 1):
        A_matr = createAMatrixDate(player, sorted_keys[i])
        b_matr = createbMatrixDate(player, sorted_keys[i])
        print("A matrix: " + str(A_matr))
        print(" --   --  --  --")
        print("y matrix: " + str(b_matr))
        print(" --   --  --  --")
        trainedModel = np.linalg.lstsq(A_matr, b_matr)[0]
        num_weights = trainedModel.tolist()
        w1, w2, w3, w4 = num_weights[0][0],num_weights[1][0],num_weights[2][0],num_weights[3][0]
        prediction = w1 * full_data[player][sorted_keys[i]]['REG-OVERALL'] + w2 * full_data[player][sorted_keys[i]]['REG-LAST-FIVE'] + w3 * full_data[player][sorted_keys[i]]['REG-STADIUM-AVG'] + w4 * full_data[player][sorted_keys[i]]['REG-TEAM-AVG']

        print("Prediction: " + str(prediction) + " Actual: " + str(full_data[player][sorted_keys[i]]['FPTS']))






