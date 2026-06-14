FROM python:3.14-rc-slim AS trainer
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY train.py .
RUN python train.py

FROM python:3.14-rc-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY --from=trainer /app/savedmodel.pth .
COPY app.py .
COPY templates/ templates/
EXPOSE 5000
CMD ["python", "app.py"]