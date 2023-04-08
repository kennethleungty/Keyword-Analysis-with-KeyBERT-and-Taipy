FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
EXPOSE 8501
COPY . /app
ENTRYPOINT ["python"]
CMD ["main.py"]