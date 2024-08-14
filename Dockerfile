FROM python:3.12.5-slim
WORKDIR /app
COPY . .
RUN pip install -r requirements.prod.txt
EXPOSE 8000
CMD ["python", "-u", "server.py"]