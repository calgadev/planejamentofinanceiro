import os
import dash
from dash import html, dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from app import app

from datetime import datetime, date
import plotly.express as px
import numpy as np
import pandas as pd

from globals import *


# ========= Layout ========= #
layout = dbc.Col([
    html.H1("Planejamento Financeiro", className='text-primary'),
    html.P("By Calgadev", className='text-info'),
    html.Hr(),

    # Profile Section
    dbc.Button(
        id='avatar_button',
        children=[
            html.Img(
                src=app.get_asset_url('img_hom.png'),
                id='avatar_change',
                alt='Avatar',
                className='profile_avatar',
            )
        ],
        style={'background-color': 'transparent', 'border-color': 'transparent'},
    ),

    # New Section
    dbc.Row(
        [
            dbc.Col([
                dbc.Button(color='success', id='open_novo_receita', children=['+ Receita']),
            ], width=6),
            dbc.Col([
                dbc.Button(color='danger', id='open_novo_despesa', children=['- Despesa']),
            ], width=6),
        ]
    ),

    # Income Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Adicionar Receita")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Descrição"),
                        dbc.Input(type='text', id='input_descricao_receita', placeholder='Ex.: Salário, Freelance...'),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Valor"),
                        dbc.Input(type='number', id='input_valor_receita', placeholder='100.00'),
                    ], width=6),
                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data"),
                        dcc.DatePickerSingle(
                            id='date-receitas',
                            min_date_allowed=date(2000, 1, 1),
                            max_date_allowed=date(2100, 12, 31),
                            date=datetime.today(),
                            style={'width': '100%'}
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Extras"),
                        dbc.Checklist(
                            options=[{'label': "Foi recebido?", 'value': 1},
                                     {'label': "Receita recorrente?", 'value': 2}],
                            value=[1],
                            id='switches-input-receita',
                            switch=True,
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Categoria da receita"),
                        dbc.Select(
                            id='select_receita',
                            options=[{'label': i, 'value': i} for i in cat_receitas],
                            value=[cat_receitas[0]]
                        ),
                    ], width=4)                    
                ], style={'margin-top': '25px'}),

                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Adicionar categoria", style={'color': 'green'}),
                                        dbc.Input(type='text', placeholder="Nova categoria", id='input-add-receita', value=''),
                                        html.Br(),
                                        dbc.Button("Adicionar", className='btn btn-success', id='add-categoria-receita', style={'margin-top': '20px'}),
                                        html.Br(),
                                        html.Div(id='category-div-add-receita', style={}),
                                    ], width=6, style={'padding': '10px'}),

                                    dbc.Col([
                                        html.Legend("Excluir categorias", style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-selected-style-receita',
                                            options=[{'label': i, 'value': i} for i in cat_receitas],
                                            value=[],                                                                              
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                            ),
                                        dbc.Button('Remover', color='warning', id='remove-category-receita', style={'margin-top': '20px'}),
                                    ], width=6, style={'padding': '10px'})
                                ])
                            ], title="Gerenciar categorias")
                    ], flush=True, start_collapsed=True, id='accordion-receita'),

                    html.Div(id='id_teste_receita', style={'padding-top': '20px'}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar Receita", id='salvar_receita', color='success'),
                        dbc.Popover(dbc.PopoverBody("Receita salva"), target='salvar_receita', placement='left', trigger='click'),
                    ])
                ], style={'margin-top': '20px'})
            ])
        ], style={'background-color': 'rgba(17, 140, 79, 0.05)'},
        id='modal-novo-receita',
        size='lg',
        is_open=False,
        centered=True,
        backdrop=True
    ),

    # Expense Modal
    dbc.Modal(
        [
            dbc.ModalHeader(dbc.ModalTitle("Adicionar Despesa")),
            dbc.ModalBody([
                dbc.Row([
                    dbc.Col([
                        dbc.Label("Descrição"),
                        dbc.Input(type='text', id='input_descricao_despesa', placeholder="Ex.: Gasolina, Mercado, Luz..."),
                    ], width=6),
                    dbc.Col([
                        dbc.Label("Valor"),
                        dbc.Input(type='number', id='input_valor_despesa', placeholder="100.00"),
                    ], width=6),
                ]),

                dbc.Row([
                    dbc.Col([
                        dbc.Label("Data"),
                        dcc.DatePickerSingle(
                            id='date-despesas',
                            min_date_allowed=date(2000, 1, 1),
                            max_date_allowed=date(2100, 12, 31),
                            date=datetime.today(),
                            style={'width': '100%'}
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Extras"),
                        dbc.Checklist(
                            options=[{'label': "Despesa Recorrente?", 'value': 1},],
                            value=[0],
                            id='switches-input-despesa',
                            switch=True,
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Categoria da despesa"),
                        dbc.Select(
                            id='select_despesa',
                            options=[{'label': i, 'value': i} for i in cat_despesas],
                            value=[cat_despesas[0]]
                        ),
                    ], width=4)                    
                ], style={'margin-top': '25px'}),

                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Adicionar categoria", style={'color': 'green'}),
                                        dbc.Input(type='text', placeholder="Nova categoria", id='input-add-despesa', value=''),
                                        html.Br(),
                                        dbc.Button("Adicionar", className='btn btn-success', id='add-category-despesa', style={'margin-top': '20px'}),
                                        html.Br(),
                                        html.Div(id='category-div-add-despesa', style={}),
                                    ], width=6),

                                    dbc.Col([
                                        html.Legend("Excluir categorias", style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-selected-style-despesa',
                                            options=[{'label': i, 'value': i} for i in cat_despesas],
                                            value=[],                                                                              
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                            ),
                                        dbc.Button('Remover', color='warning', id='remove-category-despesa', style={'margin-top': '20px'}),
                                    ], width=6)
                                ])
                            ], title="Gerenciar categorias"),
                    ], flush=True, start_collapsed=True, id='accordion-despesa'),
                    html.Div(id='id_teste_despesa', style={'padding-top': '20px'}),
                    dbc.ModalFooter([
                        dbc.Button("Adicionar Despesa", id='salvar_despesa', color='success'),
                        dbc.Popover(dbc.PopoverBody("Despesa salva"), target='salvar_despesa', placement='left', trigger='click'),
                    ])
                ])
            ]),
        ], style={'background-color': 'rgba(17, 140, 79, 0.05)'},
        id='modal-novo-despesa',
        size='lg',
        is_open=False,
        centered=True,
        backdrop=True
    ),

    # NAV section
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("Dashboard", href="/dashboard", active='exact'),
            dbc.NavLink("Extratos", href="/extratos", active='exact'),
        ],
        vertical=True,
        pills=True,
        id='nav_buttons',
        style={'margin-bottom': '50px'},
    )
], id='sidebar')



# =========  Callbacks  =========== #
# Pop-up income

@app.callback(
    Output('modal-novo-receita', 'is_open'),
    [Input('open_novo_receita', 'n_clicks')],
    [State('modal-novo-receita', 'is_open')],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open

# Pop-up expense

@app.callback(
    Output('modal-novo-despesa', 'is_open'),
    [Input('open_novo_despesa', 'n_clicks')],
    [State('modal-novo-despesa', 'is_open')],
)
def toggle_modal(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(
    Output('store-receitas', 'data'),

    Input('salvar_receita', 'n_clicks'),

    [State('input_descricao_receita', 'value'),
     State('input_valor_receita', 'value'),
     State('date-receitas', 'date'),
     State('switches-input-receita', 'value'),
     State('select_receita', 'value'),
     State('store-receitas', 'data')]
)
def save_receita(n, description, value, date, switches, category, dict_receitas):
    cols = ['Valor', 'Efetuado', 'Fixo', 'Data', 'Categoria', 'Descrição']

    if not dict_receitas:
        df_receitas = pd.DataFrame(columns=cols)
    else:
        df_receitas = pd.DataFrame(dict_receitas)
        for c in cols:
            if c not in df_receitas.columns:
                df_receitas[c] = pd.Series(dtype='object')
        df_receitas = df_receitas[cols]

    if n and not (value == '' or value is None):
        value = round(float(value), 2)
        try:
            date_val = pd.to_datetime(date).date()
        except Exception:
            date_val = date

        if isinstance(category, (list, tuple)):
            category = category[0] if len(category) > 0 else ''

        switches = switches or []
        recebido = 1 if 1 in switches else 0
        fixo = 1 if 2 in switches else 0

        row = {
            'Valor': value,
            'Efetuado': recebido,
            'Fixo': fixo,
            'Data': date_val,
            'Categoria': category,
            'Descrição': description,
        }

        df_receitas = pd.concat([df_receitas, pd.DataFrame([row])], ignore_index=True)
        df_receitas.to_csv('./data/df_receitas.csv')

    return df_receitas.to_dict()

@app.callback(
    Output('store-despesas', 'data'),

    Input('salvar_despesa', 'n_clicks'),

    [State('input_descricao_despesa', 'value'),
     State('input_valor_despesa', 'value'),
     State('date-despesas', 'date'),
     State('switches-input-despesa', 'value'),
     State('select_despesa', 'value'),
     State('store-despesas', 'data')]
)
def save_despesa(n, description, value, date, switches, category, dict_despesas):
    cols = ['Valor', 'Efetuado', 'Fixo', 'Data', 'Categoria', 'Descrição']

    if not dict_despesas:
        df_despesas = pd.DataFrame(columns=cols)
    else:
        df_despesas = pd.DataFrame(dict_despesas)
        for c in cols:
            if c not in df_despesas.columns:
                df_despesas[c] = pd.Series(dtype='object')
        df_despesas = df_despesas[cols]

    if n and not (value == '' or value is None):
        value = round(float(value), 2)
        try:
            date_val = pd.to_datetime(date).date()
        except Exception:
            date_val = date

        if isinstance(category, (list, tuple)):
            category = category[0] if len(category) > 0 else ''

        switches = switches or []
        fixo = 1 if 1 in switches else 0

        row = {
            'Valor': value,
            'Efetuado': 0,
            'Fixo': fixo,
            'Data': date_val,
            'Categoria': category,
            'Descrição': description,
        }

        df_despesas = pd.concat([df_despesas, pd.DataFrame([row])], ignore_index=True)
        df_despesas.to_csv('./data/df_despesas.csv')

    return df_despesas.to_dict()

@app.callback(

    [
        Output('select_despesa', 'options'),
        Output('checklist-selected-style-despesa', 'options'),
        Output('checklist-selected-style-despesa', 'value'),
        Output('store-cat-despesas', 'data')
    ],

    [   
        Input('add-category-despesa', 'n_clicks'),
        Input('remove-category-despesa', 'n_clicks')
    ],

    [
        State('input-add-despesa', 'value'),
        State('checklist-selected-style-despesa', 'value'),
        State('store-cat-despesas', 'data')
    ]
)
def add_category(n, n2, txt, check_delete, data):
    global cat_despesas

    if n and not (txt == '' or txt is None):
        cat_despesas = cat_despesas + [txt] if txt not in cat_despesas else cat_despesas

    if n2:
        if len(check_delete) > 0:
            cat_despesas = [i for i in cat_despesas if i not in check_delete]

    opt_despesa = [{'label': i, 'value': i} for i in cat_despesas]
    df_cat_despesas = pd.DataFrame(cat_despesas, columns=['Categoria'])
    df_cat_despesas.to_csv('./data/df_cat_despesas.csv')
    data_return = df_cat_despesas.to_dict()

    return opt_despesa, opt_despesa, [], data_return

@app.callback(

    [
        Output('select_receita', 'options'),
        Output('checklist-selected-style-receita', 'options'),
        Output('checklist-selected-style-receita', 'value'),
        Output('store-cat-receitas', 'data')
    ],

    [   
        Input('add-categoria-receita', 'n_clicks'),
        Input('remove-category-receita', 'n_clicks')
    ],

    [
        State('input-add-receita', 'value'),
        State('checklist-selected-style-receita', 'value'),
        State('store-cat-receitas', 'data')
    ]
)
def add_category_receita(n, n2, txt, check_delete, data):
    global cat_receitas

    if n and not (txt == '' or txt is None):
        cat_receitas = cat_receitas + [txt] if txt not in cat_receitas else cat_receitas

    if n2:
        if len(check_delete) > 0:
            cat_receitas = [i for i in cat_receitas if i not in check_delete]

    opt_receita = [{'label': i, 'value': i} for i in cat_receitas]
    df_cat_receitas = pd.DataFrame(cat_receitas, columns=['Categoria'])
    df_cat_receitas.to_csv('./data/df_cat_receitas.csv')
    data_return = df_cat_receitas.to_dict()

    return opt_receita, opt_receita, [], data_return