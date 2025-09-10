# Dashboard de Análise de Dados IoT/OT

## Descrição

Dashboard interativo desenvolvido para demonstrar competências em análise de dados aplicadas ao contexto de infraestrutura crítica de telemetria IoT/OT. O projeto simula o monitoramento de milhares de dispositivos conectados, baseado na experiência real como Coordenador Técnico de IoT e OT.

## Características Principais

- 📊 **KPIs em Tempo Real**: Monitoramento de dispositivos conectados, disponibilidade, latência e taxa de sucesso
- 🔄 **Interatividade Completa**: Filtros dinâmicos por período e localização
- 📈 **Visualizações Especializadas**: Seções dedicadas para IoT Cloud, SCADA, Comissionamento e Análise Geral
- 🌐 **Interface Responsiva**: Layout adaptável para diferentes dispositivos
- 📋 **Análises Avançadas**: Correlações, mapas de calor e tabelas de resumo

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem principal
- **Dash**: Framework para dashboards web interativos
- **Plotly**: Biblioteca de visualização de dados
- **Pandas**: Manipulação e análise de dados
- **NumPy**: Computação numérica

## Estrutura do Projeto

```
├── dashboard.py                # Aplicação principal do dashboard
├── generate_simulated_data.py  # Script para geração de dados simulados
├── iot_data.csv                # Dados de telemetria IoT
├── scada_data.csv              # Dados do sistema SCADA
├── commissioning_data.csv      # Dados de comissionamento
├── documentacao_dashboard.md   # Documentação técnica completa
├── apresentacao.md             # Resposta profissional para recrutador
└── README.md                   # Este arquivo
```

## Como Executar

### Pré-requisitos
```bash
pip install dash plotly pandas numpy
```

### Execução
```bash
# Gerar dados simulados (se necessário)
python generate_simulated_data.py

# Executar o dashboard
python dashboard.py
```

O dashboard estará disponível em: `http://localhost:8050`

## Funcionalidades por Seção

### IoT Cloud (Azure)
- Status dos dispositivos (online/offline)
- Tendência de latência temporal
- Volume de mensagens por protocolo

### SCADA (Elipse)
- Disponibilidade de ativos críticos
- Distribuição de tipos de alertas
- Leituras de sensores

### Comissionamento
- Distribuição por tipo de conectividade
- Taxa de sucesso mensal
- Tempo médio de comissionamento

### Análise Geral
- Correlação volume vs. latência
- Mapa de calor de atividade
- Resumo por localização

## Dados Simulados

O projeto utiliza dados simulados que representam:
- **10.000 registros** de telemetria IoT
- **5.000 registros** de monitoramento SCADA
- **1.000 registros** de comissionamento
- **Período**: Últimos 30-180 dias
- **Localizações**: 5 regiões geográficas

## Competências Demonstradas

1. **Análise de Dados**: Processamento e visualização de grandes volumes de dados
2. **Desenvolvimento Web**: Criação de interfaces interativas e responsivas
3. **Conhecimento de Domínio**: Experiência específica em IoT/OT e telemetria industrial
4. **Pensamento Analítico**: Identificação de padrões e correlações relevantes
5. **Visualização de Dados**: Criação de gráficos informativos e intuitivos

## Contexto Profissional

Este projeto reflete a experiência real como Coordenador Técnico de IoT e OT na Comgás, onde atuo com:
- Infraestrutura de telemetria com milhares de dispositivos
- Azure IoT Hub e sistemas SCADA (Elipse)
- Protocolos MQTT, SNMP e redes VPN
- Comissionamento de equipamentos remotos
- Análise de performance e confiabilidade de sistemas críticos

## Contato

Desenvolvido como projeto de demonstração para oportunidades em Análise de Dados, showcasing experiência real em coordenação de infraestruturas críticas de telemetria IoT/OT.

