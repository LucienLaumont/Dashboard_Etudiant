# Exemple : homes_page.py
from dash import html

from dash import html, dcc

def layout_home():
    return html.Div([
        html.Div(
            id='navbar',
            children=[
                html.Div(
                   html.H1("Dashboard Etudiant", className='titre-gras')
                ),
                html.Div(
                    className='conteneur-box',
                    children=[
                        dcc.Link(
                            html.Div(
                                children=[
                                    html.Img(src='assets/resized_logo_user.png', style={'height': '100%', 'width': '100%'}),
                                ],
                                className='Box'
                            ),
                            href='/page_user'
                        ),
                        dcc.Link(
                            html.Div(
                                children=[
                                    html.Img(src='assets/resized_logo_stat.png', style={'height': '100%', 'width': '100%'}),
                                ],
                                className='Box'
                            ),
                            href='/page_stat'
                        ),
                        dcc.Link(
                            html.Div(
                                children=[
                                    html.Img(src='assets/resized_logo_map.png', style={'height': '100%', 'width': '100%'}),
                                ],
                                className='Box'
                            ),
                            href='/page_map'
                        ),
                    ],
                ),
            ],
            style={'display': 'flex', 'height': '10vh'}
        ),
    ])
