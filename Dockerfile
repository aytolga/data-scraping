# Python base image
FROM python:3.9-slim

# Çalışma dizinini oluştur
WORKDIR /app

# Gereksinim dosyasını kopyala ve bağımlılıkları yükle
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Uygulama dosyalarını kopyala
COPY main.py main.py
COPY kafka-topic.py kafka-topic.py

# Container çalıştığında çalıştırılacak komut
CMD ["python", "kafka-topic.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
