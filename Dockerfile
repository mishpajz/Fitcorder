FROM python:3-slim
WORKDIR /app
COPY requirements.txt .
RUN apt-get -y update
RUN apt-get -y upgrade
RUN apt-get install -y ffmpeg
RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r requirements.txt
COPY . .
RUN mkdir -p /app/volume
CMD ["python", "main.py"]