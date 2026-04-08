import json, requests, datetime, boto3, os

def handler(event, context):
    """
    Cloud Function для сбора метрик Yandex Cloud CDN.
    Запрашивает Monitoring API, агрегирует данные и сохраняет отчёт в Object Storage.
    """
    # --- Конфигурация из environment ---
    FOLDER_ID = os.environ.get('FOLDER_ID', 'b1gcijdrjlf3m935prl2')
    CDN_RESOURCE = os.environ.get('CDN_RESOURCE', 'bc8rjft7hd6zxa3unmtt')
    BUCKET_NAME = os.environ.get('BUCKET_NAME', 'hw39-cdn-site-8945')
    AWS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
    AWS_SECRET = os.environ.get('AWS_SECRET_ACCESS_KEY')
    
    # --- Получение IAM-токена из метаданных ---
    iam_token = get_iam_token()
    to_time = datetime.datetime.utcnow()
    from_time = to_time - datetime.timedelta(hours=24)  # ✅ Период: 24 часа
    
    # --- ✅ ПРАВИЛЬНЫЙ QUERY для Monitoring API ---
    # Формат: metric_name{service="yccdn", resource="ID"}
    # service="yccdn" (не "cdn"), метка "resource" (не "resource_id")
    query = f'edge.requests{{service="yccdn", resource="{CDN_RESOURCE}"}}'
    
    try:
        resp = requests.post(
            'https://monitoring.api.cloud.yandex.net/monitoring/v2/data/read',
            params={'folderId': FOLDER_ID},  # ✅ folderId в URL params!
            headers={'Authorization': f'Bearer {iam_token}'},
            json={'query': query, 'fromTime': from_time.isoformat()+'Z', 'toTime': to_time.isoformat()+'Z'},
            timeout=30
        )
        data = resp.json() if resp.status_code == 200 else {'metrics': [], 'error': resp.text}
    except Exception as e:
        data = {'metrics': [], 'error': str(e)}
    
    # --- ✅ Агрегация DGAUGE-метрик ---
    # edge.requests = запросы/секунду (rate)
    # Чтобы получить общее число: sum(rate) * interval_seconds
    INTERVAL = 180  # ~3 минуты между точками данных
    total_requests = 0
    
    for m in data.get('metrics', []):
        values = m.get('timeseries', {}).get('doubleValues', [])
        # Фильтруем только числовые значения (исключаем "NaN" строки и float('nan'))
        numeric = [v for v in values if isinstance(v, (int, float)) and v == v]
        if numeric:
            total_requests = int(sum(numeric) * INTERVAL)
            break
    
    # --- Формирование отчёта (сжатый JSON) ---
    report = {
        'ts': to_time.isoformat()+'Z',
        'cdn': CDN_RESOURCE,
        'period': '24h',  # ✅ Обновлено
        'req': total_requests,
        'bw': 0, 'ch': 0, 'cm': 0, 'chr': 0,  # Можно расширить для edge.bytes_sent
        'err': data.get('error', '')
    }
    json_body = json.dumps(report, separators=(',', ':'))  # ~125 байт
    
    # --- ✅ Сохранение в S3: APPEND в JSONL (не перезапись!) ---
    log_key = f'cdn-reports/cdn-monitoring-{to_time.strftime("%Y-%m-%d")}.jsonl'
    try:
        s3 = boto3.client('s3', endpoint_url='https://storage.yandexcloud.net',
            region_name='ru-central1', aws_access_key_id=AWS_KEY_ID, aws_secret_access_key=AWS_SECRET)
        
        # Читаем существующие записи (если файл есть)
        existing = []
        try:
            obj = s3.get_object(Bucket=BUCKET_NAME, Key=log_key)
            for line in obj['Body'].iter_lines():
                if line.strip():
                    existing.append(json.loads(line))
        except s3.exceptions.NoSuchKey:
            pass
        
        # Добавляем новую запись и пишем обратно
        existing.append(report)
        body = '\n'.join(json.dumps(r, separators=(',', ':')) for r in existing) + '\n'
        s3.put_object(Bucket=BUCKET_NAME, Key=log_key, Body=body, ContentType='application/x-jsonlines')
        msg = f'✅ Report appended: {log_key} ({len(existing)} entries)'
    except Exception as e:
        msg = f'❌ S3 error: {str(e)}'
    
    return {'statusCode': 200, 'body': msg}

def get_iam_token():
    """Получает IAM-токен из метаданных функции"""
    r = requests.get(
        'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',
        headers={'Metadata-Flavor': 'Google'},
        timeout=10
    )
    return r.json()['access_token']