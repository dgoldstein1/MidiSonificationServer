FROM ubuntu
# copy over files and set env variables
COPY . /
# Update
RUN apt-get update
RUN apt-get install -y python 
RUN apt-get install -y python-pip

# Install app dependencies
RUN pip install -r requirements.txt

ENTRYPOINT python server.py 8080

EXPOSE 8080