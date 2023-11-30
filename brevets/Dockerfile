FROM python:3.8
LABEL Nabil Abdel-Rahman="nabilabdel-rahman@outlook.com"
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "-B"]
CMD ["flask_brevets.py"]
