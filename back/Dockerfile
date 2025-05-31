FROM python:3.11.2

RUN apt-get update && apt-get install -y libgl1 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY model/aisoft_resnet_model.h5 /app/model/aisoft_resnet_model.h5


EXPOSE 5000

CMD ["python", "app.py"]
