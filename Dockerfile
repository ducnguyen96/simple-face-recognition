FROM python:3.6.2

RUN apt-get update

RUN apt install -y libgl1-mesa-glx

RUN mkdir -p /usr/src/app

WORKDIR /usr/src/app

COPY . ./

RUN pip install --upgrade pip

RUN pip install -r packages.txt

EXPOSE 5000

CMD ["python", "main.py"]