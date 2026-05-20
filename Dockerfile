FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    wget curl \
    libnss3 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 \
    libxcomposite1 libxdamage1 libxrandr2 \
    libgbm1 libasound2 libpangocairo-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# IMPORTANT: stable playwright install
RUN pip install playwright
RUN python -m playwright install chromium

COPY . .

CMD ["python", "app.py"]