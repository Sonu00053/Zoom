FROM python:3.11-slim

WORKDIR /app

# system deps (IMPORTANT for playwright)
RUN apt-get update && apt-get install -y \
    wget curl gnupg \
    libglib2.0-0 libnss3 libnspr4 \
    libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libdbus-1-3 \
    libxkbcommon0 libxcomposite1 libxdamage1 \
    libxrandr2 libxfixes3 libxext6 \
    libasound2 libpangocairo-1.0-0 \
    libpango-1.0-0 libcairo2 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# install chromium
RUN python -m playwright install --with-deps chromium

COPY . .

# Railway uses PORT env
CMD ["sh", "-c", "uvicorn app:app --host 0.0.0.0 --port ${PORT:-8000}"]