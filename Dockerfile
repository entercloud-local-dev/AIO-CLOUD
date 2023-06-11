
#ARG VIRTUAL_ENV=/opt/aws
FROM python:3
#ENV VIRTUAL_ENV=$VIRTUAL_ENV
WORKDIR /app

### Install the following dependenices in the docker image
#default value is for an AWS virtual environment how this be overwritten via cli. 
ADD test/src/src.tar.gz /app

#RUN apt-get install -y curl iproute2 sshfs unzip less groff ca-certificates apt-transport-https && //
# echo "deb [signed-by=/etc/apt/keyrings/kubernetes-archive-keyring.gpg] https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list && //
## sudo apt-get update -y ;; apt-get install -y curl iproute2 sshfs unzip less groff ca-certificates apt-transport-https kubectl

RUN python3 -m venv aio 
ENV PATH="/app/aio/bin:$PATH" 
#cloud developements includes the constructs of the the cloud providers

RUN pip install --upgrade pip && pip install -r requirements.txt


### Invocation of the applicatin. 
CMD [ "python", "AIO-cloud.py"]