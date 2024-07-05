from dash import html,dcc

import pandas as pd
import plotly.graph_objs as go
import numpy as np

def stats_graph(df):

    # Convert columns to numeric, replace non-numeric values with NaN
    df['taux_reussite_bac'] = pd.to_numeric(df['taux_reussite_bac'], errors='coerce')
    df['taux_mentions_bac'] = pd.to_numeric(df['taux_mentions_bac'], errors='coerce')
    df['effectifs_terminale'] = pd.to_numeric(df['effectifs_terminale'], errors='coerce')

    # Filter 'taux_reussite_bac' for values above 60% and not NaN
    reussite_filtered = df[df['taux_reussite_bac'].notna() & (df['taux_reussite_bac'] > 60)]
    reussite_bins_filtered = pd.cut(reussite_filtered['taux_reussite_bac'], bins=np.arange(70, 110, 10))
    reussite_grouped_filtered = reussite_filtered.groupby(reussite_bins_filtered)['taux_reussite_bac'].count()

    # Similar filtering for 'taux_mentions_bac'
    mentions_filtered = df[df['taux_mentions_bac'].notna() & (df['taux_mentions_bac'] > 0)]
    mentions_bins_filtered = pd.cut(mentions_filtered['taux_mentions_bac'], bins=np.arange(0, 110, 10))
    mentions_grouped_filtered = mentions_filtered.groupby(mentions_bins_filtered)['taux_mentions_bac'].count()


    # Correcting the binning for 'effectifs_terminale'
    # Ensure there's at least one non-NaN value
    if df['effectifs_terminale'].notna().any():
        max_value = df['effectifs_terminale'].max()
        effectifs_bins = pd.cut(df['effectifs_terminale'], bins=np.arange(50, max_value + 50, 50))
        effectifs_grouped = df.groupby(effectifs_bins)['effectifs_terminale'].count()

        # Create the Plotly figure for 'effectifs_terminale'
        fig_effectifs = go.Figure(data=[
            go.Bar(x=effectifs_grouped.index.astype(str), y=effectifs_grouped, marker_color='coral')
        ])
        fig_effectifs.update_layout(
            title='Nombre de Lycées par Effectifs de Terminale',
            xaxis_title='Effectifs de Terminale',
            yaxis_title='Nombre de Lycées'
        )
    else:
        print("No valid data in 'effectifs_terminale'")

    # Créer les figures Plotly avec les données filtrées
    fig_reussite = go.Figure(data=[
        go.Bar(x=reussite_grouped_filtered.index.astype(str), y=reussite_grouped_filtered, marker_color='skyblue')
    ])
    fig_reussite.update_layout(
        title='Nombre de Lycées par Taux de Réussite au Bac',
        xaxis_title='Taux de Réussite au Bac (%)',
        yaxis_title='Nombre de Lycées'
    )

    fig_mentions = go.Figure(data=[
        go.Bar(x=mentions_grouped_filtered.index.astype(str), y=mentions_grouped_filtered, marker_color='lightgreen')
    ])

    fig_mentions.update_layout(
        title='Nombre de Lycées par Taux de Mentions au Bac',
        xaxis_title='Taux de Mentions au Bac (%)',
        yaxis_title='Nombre de Lycées'
    )

    # Créer la figure Plotly pour 'effectifs_terminale'
    fig_effectifs = go.Figure(data=[
        go.Bar(x=effectifs_grouped.index.astype(str), y=effectifs_grouped, marker_color='coral')
    ])
    fig_effectifs.update_layout(
        title='Nombre de Lycées par Effectifs de Terminale',
        xaxis_title='Effectifs de Terminale',
        yaxis_title='Nombre de Lycées',
        showlegend=False  # Ajout de cette ligne pour masquer la légende
    )

    # Créer la figure Plotly pour le graphique en secteurs
    fig_statut = go.Figure(data=[
        go.Pie(labels=df['statut'].value_counts().index, values = df['statut'].value_counts(), hole=.3)
    ])
    fig_statut.update_layout(
        title='Répartition des Lycées par Statut'
    )

    return fig_effectifs,fig_mentions,fig_reussite,fig_statut


def update_layout(fig):

    fig.update_layout(font=dict(
        family="Arial",
        size=15,
        color="black"
    ))
    
    return fig

def layout_stats(df):

    fig_effectifs,fig_mentions,fig_reussite,fig_statut = stats_graph(df)
    fig_effectifs = update_layout(fig_effectifs)
    fig_mentions = update_layout(fig_mentions)
    fig_reussite = update_layout(fig_reussite)
    fig_statut = update_layout(fig_effectifs)

    return html.Div([
        html.Div(id='page-stat', children=[
            html.Div(id='container-graph-1', children=[
                html.Div(children=[
                    dcc.Graph(id='graph-1-1',figure=fig_reussite)  # Intégration du premier graphique
                ], id='container-graph-1-1'),
                html.Div(children=[
                    dcc.Graph(id='graph-1-2',figure=fig_mentions)  # Intégration du deuxième graphique
                ], id='container-graph-1-2')
            ]),
            html.Div(id='container-line2', children=[
                html.Div(children=[dcc.Graph(id='graph-2-1', figure=fig_effectifs)
                ], id='container-graph-2'),
                html.Div(children=[dcc.Graph(id='graph-2-2', figure=fig_statut)], id='container-graph-3')
            ])
        ]),
    ], className='conteneur-page')