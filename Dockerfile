FROM python:3.9
WORKDIR /mvp_api
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV HOST=0.0.0.0
ENV PORT=5000
EXPOSE $PORT

#CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]

CMD ["flask", "run", "--host", "0.0.0.0", "--port", "5000"]