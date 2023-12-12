FROM jupyterhub/jupyterhub:3.1.1

RUN apt-get update
RUN apt-get -y install gcc
RUN apt-get -y install python3-dev
RUN python3 -m pip install --upgrade pip
RUN apt-get -y install git
# RUN pip install --upgrade setuptools

WORKDIR jupyter
COPY jupyterhub-builder/config/requirements.txt .
RUN pip install -r ./requirements.txt
COPY jupyterhub-builder/config/jupyterhub_config.py /srv/

ENTRYPOINT jupyterhub --log-level=DEBUG -f /srv/jupyterhub_config.py
