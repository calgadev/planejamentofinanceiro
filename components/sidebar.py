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
                            options=[],
                            value=[],
                            id='switches-input-receita',
                            switch=True,
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Categoria da receita"),
                        dbc.Select(
                            id='select_receita',
                            options=[],
                            value=[]
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
                                    ], width=6),

                                    dbc.Col([
                                        html.Legend("Excluir categorias", style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-selected-style-receita',
                                            options=[],
                                            value=[],                                                                              
                                            label_checked_style={'color': 'red'},
                                            input_checked_style={'backgroundColor': 'blue', 'borderColor': 'orange'},
                                            ),
                                        dbc.Button('Remover', color='warning', id='remove-category-receita', style={'margin-top': '20px'}),
                                    ], width=6)
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
                            options=[],
                            value=[],
                            id='switches-input-despesa',
                            switch=True,
                        ),
                    ], width=4),

                    dbc.Col([
                        dbc.Label("Categoria da despesa"),
                        dbc.Select(
                            id='select_despesa',
                            options=[],
                            value=[]
                        ),
                    ], width=4)                    
                ], style={'margin-top': '25px'}),

                dbc.Row([
                    dbc.Accordion([
                        dbc.AccordionItem(children=[
                                dbc.Row([
                                    dbc.Col([
                                        html.Legend("Adicionar categoria", style={'color': 'green'}),
                                        dbc.Input(type='text', placeholder='Nova categoria', id='input-add-despesa', value=''),
                                        html.Br(),
                                        dbc.Button("Adicionar", className='btn btn-success', id='add-categoria-despesa', style={'margin-top': '20px'}),
                                        html.Br(),
                                        html.Div(id='category-div-add-despesa', style={}),
                                    ], width=6),

                                    dbc.Col([
                                        html.Legend("Excluir categorias", style={'color': 'red'}),
                                        dbc.Checklist(
                                            id='checklist-selected-style-despesa',
                                            options=[],
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