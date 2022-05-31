FROM tensorflow/tensorflow:latest-gpu
WORKDIR /temp

RUN curl -L https://github.com/BattlesnakeOfficial/rules/releases/download/v1.1.4/battlesnake_1.1.4_Linux_x86_64.tar.gz -o battlesnake_1.1.4_Linux_x86_64.tar.gz &&\
    tar -xvzf battlesnake_1.1.4_Linux_x86_64.tar.gz &&\
    mv battlesnake /usr/local/bin &&\
    rm battle* LICENSE README.md

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt
