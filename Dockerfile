# Gunakan base image python
FROM python:3.11-slim

# Set environment agar Python tidak menyimpan cache
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy file requirements.txt jika ada
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project ke dalam container
COPY . .

# Expose port (Coolify otomatis akan baca)
EXPOSE 8100

# Jalankan Flask dengan Gunicorn (lebih production ready)
# Ganti `app:app` sesuai nama file dan object Flask kamu
CMD ["gunicorn", "-b", "0.0.0.0:8100", "wsgi:app"]