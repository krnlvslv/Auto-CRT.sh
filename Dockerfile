FROM python:3.11

WORKDIR /app

COPY CRTshAuto.py .

RUN pip install requests

CMD ["python", "CRTshAuto.py"]