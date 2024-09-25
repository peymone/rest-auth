FROM python:3.11.3

WORKDIR /rest-auth-gateway

COPY requirements.txt .
COPY . .

EXPOSE 8000
RUN pip install --no-cache-dir -r requirements.txt

CMD ["fastapi", "run", "app/api.py", "--port", "8000"]