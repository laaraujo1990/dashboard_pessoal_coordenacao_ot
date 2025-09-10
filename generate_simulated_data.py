
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_iot_data(num_records):
    data = []
    devices = [f'device_{i:04d}' for i in range(1, 101)]
    protocols = ['MQTT', 'SNMP']
    locations = ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro']

    start_date = datetime.now() - timedelta(days=30)

    for i in range(num_records):
        timestamp = start_date + timedelta(minutes=i * 10)
        device_id = random.choice(devices)
        protocol = random.choice(protocols)
        status = random.choice(['online', 'offline'])
        latency = round(random.uniform(50, 500), 2) if status == 'online' else np.nan
        message_volume = random.randint(100, 10000)
        location = random.choice(locations)

        data.append({
            'timestamp': timestamp,
            'device_id': device_id,
            'protocol': protocol,
            'status': status,
            'latency_ms': latency,
            'message_volume': message_volume,
            'location': location
        })
    return pd.DataFrame(data)

def generate_scada_data(num_records):
    data = []
    assets = [f'asset_{i:03d}' for i in range(1, 51)]
    alert_types = ['Pressão Alta', 'Temperatura Crítica', 'Falha de Comunicação', 'Manutenção Necessária']

    start_date = datetime.now() - timedelta(days=30)

    for i in range(num_records):
        timestamp = start_date + timedelta(hours=i)
        asset_id = random.choice(assets)
        availability = random.choice([True, False])
        alert_type = random.choice(alert_types) if not availability and random.random() < 0.7 else None
        mttr_hours = round(random.uniform(1, 24), 2) if not availability and alert_type else np.nan
        sensor_reading = round(random.uniform(10, 100), 2)

        data.append({
            'timestamp': timestamp,
            'asset_id': asset_id,
            'availability': availability,
            'alert_type': alert_type,
            'mttr_hours': mttr_hours,
            'sensor_reading': sensor_reading
        })
    return pd.DataFrame(data)

def generate_commissioning_data(num_records):
    data = []
    new_devices = [f'new_device_{i:04d}' for i in range(1, 201)]
    connectivity_types = ['Celular', 'Local', 'Satélite']

    start_date = datetime.now() - timedelta(days=180)

    for i in range(num_records):
        commissioning_date = start_date + timedelta(days=random.randint(0, 179))
        device_id = random.choice(new_devices)
        success = random.choice([True, False])
        commissioning_time_hours = round(random.uniform(0.5, 8), 2) if success else np.nan
        connectivity_type = random.choice(connectivity_types)

        data.append({
            'commissioning_date': commissioning_date,
            'device_id': device_id,
            'success': success,
            'commissioning_time_hours': commissioning_time_hours,
            'connectivity_type': connectivity_type
        })
    return pd.DataFrame(data)

if __name__ == '__main__':
    iot_df = generate_iot_data(10000)
    scada_df = generate_scada_data(5000)
    commissioning_df = generate_commissioning_data(1000)

    iot_df.to_csv('iot_data.csv', index=False)
    scada_df.to_csv('scada_data.csv', index=False)
    commissioning_df.to_csv('commissioning_data.csv', index=False)

    print('Dados simulados gerados e salvos em iot_data.csv, scada_data.csv e commissioning_data.csv')


