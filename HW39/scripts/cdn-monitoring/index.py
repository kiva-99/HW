import json
import requests
import datetime
import boto3
import os

def handler(event, context):
    """
    Функция собирает метрики Cloud CDN из Monitoring API
    и сохраняет отчёт в Object Storage
    """
    # --- 1. Конфигурация ---
    FOLDER_ID = os.environ.get('FOLDER_ID', 'b1gcijdrjlf3m935prl2')
    CDN_RESOURCE_ID = os.environ.get('CDN_RESOURCE_ID', 'bc8rjft7hd6zxa3unmtt')
    BUCKET_NAME = os.environ.get('BUCKET_NAME', 'hw39-cdn-site-8945')
    
    # Ключи S3 из environment
    AWS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # --- 2. Получаем IAM-токен из метаданных ---
    iam_token = get_iam_token()
    
    # --- 3. Формируем запрос к Monitoring API ---
    to_time = datetime.datetime.utcnow()
    from_time = to_time - datetime.timedelta(hours=3)
    from_time_str = from_time.isoformat() + 'Z'
    to_time_str = to_time.isoformat() + 'Z'
    
    # Query для получения метрик CDN (правильный синтаксис)
    query = '{service="cdn", resource_id="' + CDN_RESOURCE_ID + '"}'
    
    monitoring_url = 'https://monitoring.api.cloud.yandex.net/monitoring/v2/data/read'
    
    try:
        response = requests.post(
            monitoring_url,
            params={'folderId': FOLDER_ID},  # folderId в query params!
            headers={'Authorization': f'Bearer {iam_token}'},
            json={
                'query': query,
                'fromTime': from_time_str,
                'toTime': to_time_str
            },
            timeout=20
        )
        
        if response.status_code != 200:
            metrics_data = {'metrics': [], 'error': response.text}
        else:
            metrics_data = response.json()
    except Exception as e:
        metrics_data = {'metrics': [], 'error': str(e)}
    
    # --- 4. Агрегируем метрики ---
    total_requests = 0
    total_bandwidth = 0
    cache_hits = 0
    cache_misses = 0
    
    for metric in metrics_data.get('metrics', []):
        metric_name = metric.get('name', '')
        timeseries = metric.get('timeseries', {})
        values = timeseries.get('doubleValues', [])
        
        if values:
            last_value = values[-1] if values else 0
            if 'requests_total' in metric_name:
                total_requests = int(last_value)
            elif 'bandwidth' in metric_name:
                total_bandwidth = last_value
            elif 'cache_hit' in metric_name:
                cache_hits = int(last_value)
            elif 'cache_miss' in metric_name:
                cache_misses = int(last_value)
    
    # --- 5. Формируем отчёт (СЖАТЫЙ JSON) ---
    report = {
        'ts': to_time_str,
        'cdn': CDN_RESOURCE_ID,
        'period': '3h',
        'req': total_requests,
        'bw': round(total_bandwidth, 2),
        'ch': cache_hits,
        'cm': cache_misses,
        'chr': round(cache_hits / (cache_hits + cache_misses), 4) if (cache_hits + cache_misses) > 0 else 0,
        'err': metrics_data.get('error', '')
    }
    
    # Сжимаем JSON
    json_body = json.dumps(report, separators=(',', ':'))
    
    # --- 6. Сохраняем в S3 (с явными ключами!) ---
    today_str = datetime.datetime.utcnow().strftime('%Y-%m-%d')
    filename = f'cdn-reports/cdn-monitoring-{today_str}.json'
    
    try:
        s3 = boto3.client(
            's3',
            endpoint_url='https://storage.yandexcloud.net',
            region_name='ru-central1',
            aws_access_key_id=AWS_KEY_ID,
            aws_secret_access_key=AWS_SECRET
        )
        s3.put_object(
            Bucket=BUCKET_NAME,
            Key=filename,
            Body=json_body,
            ContentType='application/json'
        )
        log_msg = f'✅ Report saved: {filename}'
    except Exception as e:
        log_msg = f'❌ S3 error: {str(e)}'
    
    # --- 7. Возврат результата ---
    return {
        'statusCode': 200,
        'body': log_msg
    }

def get_iam_token():
    """Получает IAM-токен из метаданных функции"""
    response = requests.get(
        'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',
        headers={'Metadata-Flavor': 'Google'},
        timeout=10
    )
    return response.json()['access_token']
