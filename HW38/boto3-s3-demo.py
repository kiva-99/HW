#!/usr/bin/env python3
"""
HW38: Демонстрация работы с Yandex Object Storage через Boto3
Студент: Иванов Кирилл
"""
import boto3
from botocore.exceptions import ClientError
import os

# Конфигурация для Yandex Cloud
ENDPOINT_URL = 'https://storage.yandexcloud.net'
REGION = 'ru-central1'

# Создаём клиент S3 для Yandex Cloud
s3_client = boto3.client(
    's3',
    endpoint_url=ENDPOINT_URL,
    region_name=REGION
    # Ключи берутся из ~/.aws/credentials автоматически
)

# Имя существующего бакета
BUCKET_NAME = 'hw38-demo-*****'

def test_connection():
    """Проверяем подключение к S3"""
    try:
        s3_client.list_buckets()
        print("✅ Подключение к S3 успешно!")
        return True
    except ClientError as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def upload_file_via_boto3(local_file, object_name):
    """Загружаем файл через Boto3"""
    try:
        s3_client.upload_file(local_file, BUCKET_NAME, object_name)
        print(f"✅ Файл '{local_file}' загружен как '{object_name}'")
        return True
    except ClientError as e:
        print(f"❌ Ошибка загрузки: {e}")
        return False

def set_public_acl(object_name):
    """Делаем файл публичным через Boto3"""
    try:
        s3_client.put_object_acl(
            ACL='public-read',
            Bucket=BUCKET_NAME,
            Key=object_name
        )
        print(f"✅ Файл '{object_name}' сделан публичным")
        return True
    except ClientError as e:
        print(f"❌ Ошибка установки ACL: {e}")
        return False

def download_file_via_boto3(object_name, local_file):
    """Скачиваем файл через Boto3"""
    try:
        s3_client.download_file(BUCKET_NAME, object_name, local_file)
        print(f"✅ Файл '{object_name}' скачан как '{local_file}'")
        return True
    except ClientError as e:
        print(f"❌ Ошибка скачивания: {e}")
        return False

def delete_file_via_boto3(object_name):
    """Удаляем файл через Boto3"""
    try:
        s3_client.delete_object(Bucket=BUCKET_NAME, Key=object_name)
        print(f"✅ Файл '{object_name}' удалён")
        return True
    except ClientError as e:
        print(f"❌ Ошибка удаления: {e}")
        return False

def list_objects():
    """Показываем список файлов в бакете"""
    try:
        response = s3_client.list_objects_v2(Bucket=BUCKET_NAME)
        print(f"\n📦 Файлы в бакете '{BUCKET_NAME}':")
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f"   - {obj['Key']} ({obj['Size']} bytes)")
        else:
            print("   (бакет пуст)")
        return True
    except ClientError as e:
        print(f"❌ Ошибка получения списка: {e}")
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("HW38: Работа с Object Storage через Boto3")
    print("=" * 60)
    
    # 1. Проверяем подключение
    print("\n[1] Проверка подключения...")
    if not test_connection():
        exit(1)
    
    # 2. Создаём тестовый файл
    print("\n[2] Создание тестового файла...")
    test_file = '/tmp/boto3-test.txt'
    with open(test_file, 'w', encoding='utf-8') as f:
        f.write("HW38: Тестовый файл для Boto3\n")
        f.write("Создано через Python скрипт\n")
        f.write("Студент: Иванов Кирилл\n")
    print(f"✅ Файл '{test_file}' создан")
    
    # 3. Загружаем файл через Boto3
    print("\n[3] Загрузка файла через Boto3...")
    upload_file_via_boto3(test_file, 'boto3-test.txt')
    
    # 4. Делаем файл публичным
    print("\n[4] Установка публичного доступа...")
    set_public_acl('boto3-test.txt')
    
    # 5. Показываем список файлов
    print("\n[5] Список файлов в бакете:")
    list_objects()
    
    # 6. Скачиваем файл через Boto3
    print("\n[6] Скачивание файла через Boto3...")
    download_file_via_boto3('boto3-test.txt', '/tmp/downloaded-boto3.txt')
    
    # 7. Проверяем скачанный файл
    print("\n[7] Проверка скачанного файла:")
    with open('/tmp/downloaded-boto3.txt', 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   Содержимое:\n{content}")
    
    print("\n" + "=" * 60)
    print("✅ HW38: Boto3 демонстрация завершена!")
    print("=" * 60)
    print(f"\n🔗 Публичная ссылка на файл:")
    print(f"   https://storage.yandexcloud.net/{BUCKET_NAME}/boto3-test.txt")