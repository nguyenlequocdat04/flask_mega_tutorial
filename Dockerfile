FROM python:3.7
COPY requirements.txt /
RUN pip install --upgrade pip \
    && pip install -r requirements.txt
RUN apt-get install --reinstall tzdata \
    && cp /usr/share/zoneinfo/Asia/Ho_Chi_Minh /etc/localtime \
    && echo "Asia/Ho_Chi_Minh" > /etc/timezone
COPY . /mnt/flask_login
WORKDIR /mnt/flask_login
