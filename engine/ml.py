import pandas as pd
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.linear_model import LogisticRegression, LinearRegression, PassiveAggressiveClassifier,SGDClassifier, Perceptron
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.neural_network import MLPClassifier
from river import linear_model, metrics, compose, preprocessing, tree, neighbors, optim

df = pd.read_csv('./data/insertion.csv', dtype={'pred_json':str, 'pred_all':str})
#ghr_bits = df['pred_taken'].apply(lambda x: [int(b) for b in f'{x:010d}'])
#print(df['pred_json'])

#df['pred_all'] = df['pred_all'].apply(lambda x: f'{x:08d}')
#df['pred_json'] = df['pred_json'].apply(lambda x: f'{x:08d}')

for i in range(8):
    df[f'pred_all_{i}'] = df['pred_all'].str[i].astype(int)

for i in range(8):
    df[f'pred_json_{i}'] = df['pred_json'].str[i].astype(int)

#dpc = df['pc'] - df['next_pc']
#dreg = df['reg_rs1'] - df['reg_rs2']
count_taken = df['pred_json'].apply(lambda x: f'{x}'.count('1'))
count_taken_all = df['pred_all'].apply(lambda x: f'{x}'.count('1'))

#df['pred_all'] = df['pred_all'].apply(lambda x: int(str(x), 2))
#df['pred_json'] = df['pred_json'].apply(lambda x: int(str(x), 2))


df.drop(columns=['pred_all','pred_json'], inplace=True)
#df.insert(2, 'dpc', dpc)
#df.insert(3, 'dreg', dreg)
#df.insert(5, 'count_taken', count_taken)
#df.insert(6, 'count_taken_all', count_taken_all)

stsc = StandardScaler()

X = df.drop(columns=['taken'])  # признаки
k = X.columns
y = df['taken']  # целевая переменная (0/1 или число)

# One-Hot кодирование текстовых признаков
#X = pd.get_dummies(X, columns=['instr_type'], dtype=int)  # закодируем строковые колонки
X = stsc.fit_transform(X, y)
# Разделение на train/test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

logReg = LogisticRegression(max_iter=10**5)
#logReg.fit(X_train, y_train)

linReg = LinearRegression()
#linReg.fit(X_train, y_train)

rbf_low = SVC(kernel='rbf', gamma=0.1)
#rbf_low.fit(X_train, y_train)

dtc = DecisionTreeClassifier()
dtc.fit(X_train, y_train)

pac = PassiveAggressiveClassifier()
#pac.fit(X_train, y_train)

sgd = Perceptron()
#sgd.fit(X_train, y_train)

nn = MLPClassifier(activation='logistic', max_iter=10**5)

model = compose.Pipeline(
    preprocessing.StandardScaler(),
    linear_model.Perceptron()
    #linear_model.LogisticRegression()
)
metric = metrics.ROCAUC()
i = 0
for x, target in zip(X, y.to_list()):
    x_dict = dict(zip(k, x))
    y_pred = model.predict_one(x_dict)
    model.learn_one(x_dict, target)
    metric.update(target, y_pred)
    print(i, metric, target, y_pred)
    i += 1

#print(metric)


'''
for i in (logReg, linReg, rbf_low, dtc, pac, sgd, nn):
    i.fit(X_train, y_train)
    y_pred = i.predict(X_test)
    mse = mean_squared_error(y_test, y_pred)
    r2 = r2_score(y_test, y_pred)

    #print(f'MSE: {mse:.4f}')
    print(f'R²: {r2:.4f}')
'''

'''
#y_pred = linReg.predict(X_test)
#y_pred = rbf_low.predict(X_test)
y_pred = dtc.predict(X_test)
#y_pred = pac.predict(X_test)
#y_pred = sgd.predict(X_test)
#y_pred = nn.predict(X_test)

mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(dtc.get_depth())

print(f'MSE: {mse:.4f}')
print(f'R²: {r2:.4f}')
#print(cross_val_score(logReg, X, y))
'''