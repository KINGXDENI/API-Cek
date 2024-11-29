# Gunakan base image Python versi terbaru
FROM python:3.11-slim

# Set environment variable untuk menghindari buffer output
ENV PYTHONUNBUFFERED=1

# Update sistem dan install dependensi yang diperlukan
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Set direktori kerja di container
WORKDIR /app

# Salin file requirements.txt ke container
COPY requirements.txt /app/

# Install pip versi terbaru dan semua dependensi
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# Install waitress sebagai server WSGI
RUN pip install waitress

# Salin semua file proyek ke container
COPY . /app

# Ekspose port aplikasi
EXPOSE 5000

# Perintah untuk menjalankan aplikasi
CMD ["waitress-serve", "--host=0.0.0.0", "--port=5000", "server:app"]
