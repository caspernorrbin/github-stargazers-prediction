import pandas as pd


df = pd.read_csv('top_repos.csv')

# Drop all entrys with nan
df = df.dropna(axis=0)
# Split dataset
y = df['Stargazers']
X = df.drop('Stargazers', axis=1)
X = X.drop('Name', axis=1)

if 'Language' in X.columns:
    category_mapping = {category: index for index, category in enumerate(
        X['Language'].unique())}
    
    X['Language'] = X['Language'].map(category_mapping)

X['Stargazers'] = y

X.to_csv("top_repos_new.csv", index=False)