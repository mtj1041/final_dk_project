import player_splits
import regression_scraper
import numpy as np 

full_data = regression_scraper.getMLBData()

# Least squares estimate for Ax = b #

def createAMatrix(player):
    sorted_keys = sorted(full_data[player].keys())
    A_matr = None
    for i in sorted_keys:
        if not i == 'POS': # only key that is not a date
            x1, x2, x3, x4 = full_data[player][i]['REG-OVERALL'], full_data[player][i]['REG-LAST-FIVE'], full_data[player][i]['REG-STADIUM-AVG'], full_data[player][i]['REG-TEAM-AVG']
            row = np.transpose(np.array([x1, x2, x4]))
            if A_matr == None:
                A_matr = row
            else:
                A_matr = np.vstack([A_matr, row])
    return A_matr

def createbMatrix(player):
    sorted_keys = sorted(full_data[player].keys())
    b = None
    for i in sorted_keys:
        if not i == 'POS': # only key that is not a date
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
    for i in range(4, len(sorted_keys) - 1):
        A_to_point = None
        y_to_point = None
        for x in range(0, i):
            x1, x2, x3, x4 = full_data[player][sorted_keys[x]]['REG-OVERALL'], full_data[player][sorted_keys[x]]['REG-LAST-FIVE'], full_data[player][sorted_keys[x]]['REG-STADIUM-AVG'], full_data[player][sorted_keys[x]]['REG-TEAM-AVG']
            row = np.transpose(np.array([x1, x2, x3, x4]))
            if x == 0:
                A_to_point = row
                y_to_point = np.array([full_data[player][sorted_keys[x]]['FPTS']])
            else:
                A_to_point = np.vstack([A_to_point, row])
                y_to_point = np.vstack([y_to_point, np.array(full_data[player][sorted_keys[x]]['FPTS'])])
        print("A matrix: " + str(A_to_point))
        print(" --   --  --  --")
        print("y matrix: " + str(y_to_point))
        print(" --   --  --  --")
        weights = np.linalg.lstsq(A_to_point, y_to_point)[0]
        print("weights " + str(weights))
        num_weights = weights.tolist()
        w1, w2, w3, w4 = num_weights[0][0],num_weights[1][0],num_weights[2][0],num_weights[3][0]
        prediction = 0
        prediction = w1 * full_data[player][sorted_keys[i]]['REG-OVERALL'] + w2 * full_data[player][sorted_keys[i]]['REG-LAST-FIVE'] + w3 * full_data[player][sorted_keys[i]]['REG-STADIUM-AVG'] + w4 * full_data[player][sorted_keys[i]]['REG-TEAM-AVG']

        if not full_data[player][sorted_keys[i]]['FPTS'] == 0:
            error = abs(prediction - full_data[player][sorted_keys[i]]['FPTS']) / full_data[player][sorted_keys[i]]['FPTS']
        else:
            error = prediction - full_data[player][sorted_keys[i]]['FPTS']

        print("Prediction " + str(prediction) + " Actual: " + str(full_data[player][sorted_keys[i]]['FPTS']) + " Error: " + str(error * 100))






