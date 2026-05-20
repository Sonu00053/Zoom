FROM python:3.13-slim

WORKDIR /app

# system dependencies (IMPORTANT for Playwright)
RUN apt-get update && apt-get install -y \
    wget \
    curl \
    libnss3 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxrandr2 \
    libgbm1 \
    libasound2 \
    libpangocairo-1.0-0 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# install python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# install playwright browser
RUN python -m playwright install --with-deps chromium

# copy project
COPY . .

# start app
CMD ["python", "app.py"]