import pandas as pd

df = pd.read_csv('./data/branch_log.csv')
print(df.columns)
print(df['pred_taken'])

for i in range(10):
    df[f'hist_{i}'] = df['pred_taken'].str[i].astype(int)

df.drop(columns=['pred_taken'])

print(df)