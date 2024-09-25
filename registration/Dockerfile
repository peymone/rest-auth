FROM python:3.11.3

WORKDIR /rest-auth-reg
COPY . .

EXPOSE 8001
RUN pip install --no-cache-dir -r requirements.txt
RUN python app/db.py

CMD ["fastapi", "run", "app/api.py", "--port", "8001"]