import dash
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# Carregando os dados simulados
iot_df = pd.read_csv('iot_data.csv')
scada_df = pd.read_csv('scada_data.csv')
commissioning_df = pd.read_csv('commissioning_data.csv')

# Convertendo colunas de data
iot_df['timestamp'] = pd.to_datetime(iot_df['timestamp'])
scada_df['timestamp'] = pd.to_datetime(scada_df['timestamp'])
commissioning_df['commissioning_date'] = pd.to_datetime(commissioning_df['commissioning_date'])

# Inicializando a aplicação Dash
app = dash.Dash(__name__)

# Definindo o layout do dashboard
app.layout = html.Div([
    html.H1("Dashboard de Análise de Dados IoT/OT", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginBottom': '30px'}),
    
    # Filtros globais
    html.Div([
        html.Div([
            html.Label("Período:", style={'fontWeight': 'bold'}),
            dcc.DatePickerRange(
                id='date-range',
                start_date=iot_df['timestamp'].min(),
                end_date=iot_df['timestamp'].max(),
                display_format='DD/MM/YYYY'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Div([
            html.Label("Localização:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='location-filter',
                options=[{'label': loc, 'value': loc} for loc in iot_df['location'].unique()],
                value=iot_df['location'].unique().tolist(),
                multi=True
            )
        ], style={'width': '48%', 'float': 'right', 'display': 'inline-block'})
    ], style={'marginBottom': '30px'}),
    
    # KPIs principais
    html.Div([
        html.Div([
            html.H3(id='total-devices', style={'color': '#27ae60', 'textAlign': 'center'}),
            html.P("Dispositivos Conectados", style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], className='kpi-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%', 
                                       'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3(id='availability-rate', style={'color': '#3498db', 'textAlign': 'center'}),
            html.P("Disponibilidade (%)", style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], className='kpi-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%', 
                                       'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3(id='avg-latency', style={'color': '#e74c3c', 'textAlign': 'center'}),
            html.P("Latência Média (ms)", style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], className='kpi-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%', 
                                       'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'}),
        
        html.Div([
            html.H3(id='commissioning-success', style={'color': '#9b59b6', 'textAlign': 'center'}),
            html.P("Taxa de Sucesso (%)", style={'textAlign': 'center', 'fontWeight': 'bold'})
        ], className='kpi-card', style={'width': '23%', 'display': 'inline-block', 'margin': '1%', 
                                       'padding': '20px', 'backgroundColor': '#ecf0f1', 'borderRadius': '10px'})
    ], style={'marginBottom': '30px'}),
    
    # Abas para diferentes seções
    dcc.Tabs(id='tabs', value='iot-tab', children=[
        dcc.Tab(label='IoT Cloud (Azure)', value='iot-tab'),
        dcc.Tab(label='SCADA (Elipse)', value='scada-tab'),
        dcc.Tab(label='Comissionamento', value='commissioning-tab'),
        dcc.Tab(label='Análise Geral', value='analysis-tab')
    ]),
    
    html.Div(id='tab-content')
])

# Callback para atualizar KPIs
@app.callback(
    [Output('total-devices', 'children'),
     Output('availability-rate', 'children'),
     Output('avg-latency', 'children'),
     Output('commissioning-success', 'children')],
    [Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('location-filter', 'value')]
)
def update_kpis(start_date, end_date, locations):
    # Filtrar dados IoT
    filtered_iot = iot_df[
        (iot_df['timestamp'] >= start_date) & 
        (iot_df['timestamp'] <= end_date) &
        (iot_df['location'].isin(locations))
    ]
    
    # Filtrar dados SCADA
    filtered_scada = scada_df[
        (scada_df['timestamp'] >= start_date) & 
        (scada_df['timestamp'] <= end_date)
    ]
    
    # Calcular KPIs
    total_devices = filtered_iot['device_id'].nunique()
    availability_rate = round(filtered_scada['availability'].mean() * 100, 1)
    avg_latency = round(filtered_iot['latency_ms'].mean(), 1)
    commissioning_success = round(commissioning_df['success'].mean() * 100, 1)
    
    return f"{total_devices:,}", f"{availability_rate}%", f"{avg_latency}", f"{commissioning_success}%"

# Callback para conteúdo das abas
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('date-range', 'start_date'),
     Input('date-range', 'end_date'),
     Input('location-filter', 'value')]
)
def update_tab_content(active_tab, start_date, end_date, locations):
    # Filtrar dados
    filtered_iot = iot_df[
        (iot_df['timestamp'] >= start_date) & 
        (iot_df['timestamp'] <= end_date) &
        (iot_df['location'].isin(locations))
    ]
    
    filtered_scada = scada_df[
        (scada_df['timestamp'] >= start_date) & 
        (scada_df['timestamp'] <= end_date)
    ]
    
    if active_tab == 'iot-tab':
        # Gráfico de status de dispositivos
        status_counts = filtered_iot['status'].value_counts()
        fig_status = px.pie(values=status_counts.values, names=status_counts.index, 
                           title="Status dos Dispositivos IoT")
        
        # Gráfico de latência ao longo do tempo
        latency_trend = filtered_iot.groupby(filtered_iot['timestamp'].dt.date)['latency_ms'].mean().reset_index()
        fig_latency = px.line(latency_trend, x='timestamp', y='latency_ms', 
                             title="Tendência de Latência ao Longo do Tempo")
        
        # Gráfico de volume de mensagens por protocolo
        protocol_volume = filtered_iot.groupby('protocol')['message_volume'].sum().reset_index()
        fig_protocol = px.bar(protocol_volume, x='protocol', y='message_volume', 
                             title="Volume de Mensagens por Protocolo")
        
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_status)
            ], style={'width': '33%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_latency)
            ], style={'width': '67%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_protocol)
            ], style={'width': '100%'})
        ])
    
    elif active_tab == 'scada-tab':
        # Gráfico de disponibilidade de ativos
        availability_trend = filtered_scada.groupby(filtered_scada['timestamp'].dt.date)['availability'].mean().reset_index()
        fig_availability = px.line(availability_trend, x='timestamp', y='availability', 
                                  title="Tendência de Disponibilidade de Ativos")
        
        # Gráfico de tipos de alertas
        alert_counts = filtered_scada['alert_type'].value_counts().dropna()
        if not alert_counts.empty:
            fig_alerts = px.bar(x=alert_counts.index, y=alert_counts.values, 
                               title="Tipos de Alertas SCADA")
        else:
            fig_alerts = go.Figure().add_annotation(text="Nenhum alerta no período selecionado")
        
        # Gráfico de leituras de sensores
        sensor_trend = filtered_scada.groupby(filtered_scada['timestamp'].dt.date)['sensor_reading'].mean().reset_index()
        fig_sensors = px.line(sensor_trend, x='timestamp', y='sensor_reading', 
                             title="Leituras Médias de Sensores")
        
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_availability)
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_alerts)
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_sensors)
            ], style={'width': '100%'})
        ])
    
    elif active_tab == 'commissioning-tab':
        # Gráfico de comissionamentos por tipo de conectividade
        connectivity_counts = commissioning_df['connectivity_type'].value_counts()
        fig_connectivity = px.pie(values=connectivity_counts.values, names=connectivity_counts.index, 
                                 title="Distribuição por Tipo de Conectividade")
        
        # Gráfico de taxa de sucesso ao longo do tempo
        success_trend = commissioning_df.groupby(commissioning_df['commissioning_date'].dt.to_period('M'))['success'].mean().reset_index()
        success_trend['commissioning_date'] = success_trend['commissioning_date'].astype(str)
        fig_success = px.bar(success_trend, x='commissioning_date', y='success', 
                            title="Taxa de Sucesso de Comissionamento por Mês")
        
        # Gráfico de tempo médio de comissionamento
        time_by_type = commissioning_df.groupby('connectivity_type')['commissioning_time_hours'].mean().reset_index()
        fig_time = px.bar(time_by_type, x='connectivity_type', y='commissioning_time_hours', 
                         title="Tempo Médio de Comissionamento por Tipo de Conectividade")
        
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_connectivity)
            ], style={'width': '33%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_success)
            ], style={'width': '67%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_time)
            ], style={'width': '100%'})
        ])
    
    elif active_tab == 'analysis-tab':
        # Análise combinada e insights
        # Correlação entre latência e volume de mensagens
        correlation_data = filtered_iot[['latency_ms', 'message_volume']].dropna()
        fig_correlation = px.scatter(correlation_data, x='message_volume', y='latency_ms', 
                                   title="Correlação: Volume de Mensagens vs Latência")
        
        # Heatmap de atividade por localização e hora
        filtered_iot['hour'] = filtered_iot['timestamp'].dt.hour
        heatmap_data = filtered_iot.groupby(['location', 'hour']).size().reset_index(name='count')
        heatmap_pivot = heatmap_data.pivot(index='location', columns='hour', values='count').fillna(0)
        fig_heatmap = px.imshow(heatmap_pivot, title="Mapa de Calor: Atividade por Localização e Hora")
        
        # Tabela de resumo por localização
        summary_table = filtered_iot.groupby('location').agg({
            'device_id': 'nunique',
            'latency_ms': 'mean',
            'message_volume': 'sum'
        }).round(2).reset_index()
        summary_table.columns = ['Localização', 'Dispositivos', 'Latência Média (ms)', 'Volume Total de Mensagens']
        
        return html.Div([
            html.Div([
                dcc.Graph(figure=fig_correlation)
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                dcc.Graph(figure=fig_heatmap)
            ], style={'width': '50%', 'display': 'inline-block'}),
            
            html.Div([
                html.H3("Resumo por Localização", style={'textAlign': 'center'}),
                dash_table.DataTable(
                    data=summary_table.to_dict('records'),
                    columns=[{"name": i, "id": i} for i in summary_table.columns],
                    style_cell={'textAlign': 'center'},
                    style_header={'backgroundColor': '#3498db', 'color': 'white', 'fontWeight': 'bold'}
                )
            ], style={'width': '100%', 'marginTop': '20px'})
        ])

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)

