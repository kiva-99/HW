#!/bin/bash
# Скрипт создания публичного бакета S3 с файлами для HW38
# Автор: Кирилл Иванов
set -e  # Остановиться при ошибке

echo "=== HW38: Создание публичного бакета S3 ==="

# Генерируем уникальное имя бакета
BUCKET_NAME="hw38-demo-$(date +%s | tail -c 6)"

echo "1. Создаем бакет: $BUCKET_NAME"
yc storage bucket create --name $BUCKET_NAME

echo "2. Включаем публичный доступ..."
yc storage bucket update \
--name $BUCKET_NAME \
--public-read \
--public-list

echo "3. Создаем тестовые файлы..."

# Файл 1 - простой текст
echo "Привет из HW38! Это тестовый файл." > file1.txt

# Файл 2 - HTML страница
cat > index.html << 'HTMLEOF'
<!DOCTYPE html>
<html lang="ru">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>HW38 - Object Storage + Boto3</title>
<style>
body {
    font-family: Arial, sans-serif;
    max-width: 800px;
    margin: 0 auto;
    padding: 20px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}
.container {
    background: white;
    padding: 30px;
    border-radius: 10px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
h1 {
    color: #667eea;
    text-align: center;
}
.info {
    background: #f4f4f4;
    padding: 15px;
    border-radius: 5px;
    margin: 20px 0;
}
.success {
    color: #28a745;
    font-weight: bold;
}
</style>
</head>
<body>
    <div class="container">
        <h1>🎉 HW38 Выполнено!</h1>
        <div class="info">
            <p class="success">✓ Object Storage настроен</p>
            <p class="success">✓ Boto3 работает</p>
            <p class="success">✓ Публичный доступ включен</p>
        </div>
        <p><strong>Студент:</strong> Иванов Кирилл</p>
        <p><strong>Задание:</strong> HW38 - Работа с AWS CLI и Boto3</p>
        <p><strong>Платформа:</strong> Yandex Cloud</p>
        <hr>
        <p><em>Файл загружен через YC CLI с публичным доступом</em></p>
        <p><small>Дата создания: $(date '+%Y-%m-%d %H:%M:%S')</small></p>
    </div>
</body>
</html>
HTMLEOF

echo "4. Загружаем файлы в бакет..."
yc storage s3 cp file1.txt s3://$BUCKET_NAME/file1.txt
yc storage s3 cp index.html s3://$BUCKET_NAME/index.html

echo "5. Делаем файлы публичными..."
yc storage s3api put-object-acl \
--bucket $BUCKET_NAME \
--key file1.txt \
--acl public-read

yc storage s3api put-object-acl \
--bucket $BUCKET_NAME \
--key index.html \
--acl public-read

echo ""
echo "=== ✅ ГОТОВО! ==="
echo ""
echo "Имя бакета: $BUCKET_NAME"
echo ""
echo "📄 Публичные ссылки:"
echo "   HTML страница: https://storage.yandexcloud.net/$BUCKET_NAME/index.html"
echo "   Текстовый файл: https://storage.yandexcloud.net/$BUCKET_NAME/file1.txt"
echo ""
echo "📋 Список файлов в бакете:"
aws s3 ls s3://$BUCKET_NAME/
echo ""
echo "💡 Для удаления бакета выполни:"
echo "   yc storage bucket delete --name $BUCKET_NAME"
echo ""

# Сохраняем имя бакета в файл для удобства
echo $BUCKET_NAME > ~/last-bucket-name.txt
echo "💾 Имя бакета сохранено в ~/last-bucket-name.txt"
