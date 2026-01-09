import pandas as pd
import os

if ('df_despesas.csv' in os.listdir('./data') and ('df_receitas.csv' in os.listdir('./data'))):
    df_despesas = pd.read_csv('./data/df_despesas.csv', index_col=0, parse_dates=True)
    df_receitas = pd.read_csv('./data/df_receitas.csv', index_col=0, parse_dates=True)
    df_receitas['Data'] = pd.to_datetime(df_receitas['Data'])
    df_despesas['Data'] = pd.to_datetime(df_despesas['Data'])
    df_receitas['Data'] = df_receitas['Data'].apply(lambda x: x.date())
    df_despesas['Data'] = df_despesas['Data'].apply(lambda x: x.date())

else:
    data_structure = {'Valor':[],
        'Efetuado':[],
        'Fixo':[],
        'Data':[],
        'Categoria':[],
        'Descrição':[]}
    df_receitas = pd.DataFrame(data_structure)
    df_despesas = pd.DataFrame(data_structure)
    df_despesas.to_csv('./data/df_despesas.csv')
    df_receitas.to_csv('./data/df_receitas.csv')

if ('df_cat_despesas.csv' in os.listdir('./data') and ('df_cat_receitas.csv' in os.listdir('./data'))):
    df_cat_despesas = pd.read_csv('./data/df_cat_despesas.csv', index_col=0)
    df_cat_receitas = pd.read_csv('./data/df_cat_receitas.csv', index_col=0)
    # Make sure category lists are flat lists of strings (not list-of-lists)
    if 'Categoria' in df_cat_receitas.columns:
        cat_receitas = df_cat_receitas['Categoria'].astype(str).tolist()
    else:
        cat_receitas = df_cat_receitas.iloc[:, 0].astype(str).tolist()

    if 'Categoria' in df_cat_despesas.columns:
        cat_despesas = df_cat_despesas['Categoria'].astype(str).tolist()
    else:
        cat_despesas = df_cat_despesas.iloc[:, 0].astype(str).tolist()

else:
    cat_despesas = ['Alimentação', 'Transporte', 'Moradia', 'Lazer', 'Saúde', 'Educação', 'Outros', 'Streaming']
    cat_receitas = ['Salário', 'Freelance', 'Investimentos', 'Aluguel', 'Outros']

    df_cat_despesas = pd.DataFrame({'Categoria': cat_despesas})
    df_cat_receitas = pd.DataFrame({'Categoria': cat_receitas})
    df_cat_despesas.to_csv('./data/df_cat_despesas.csv')
    df_cat_receitas.to_csv('./data/df_cat_receitas.csv')
