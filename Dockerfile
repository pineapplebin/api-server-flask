FROM python:3.6-slim-stretch
WORKDIR /app
COPY ./requirements.txt /app
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
CMD ["python", "manager.py"]

