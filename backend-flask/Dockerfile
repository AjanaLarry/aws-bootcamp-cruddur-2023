FROM python:3.10-slim-buster

# Make a new folder similar to our working directory inside container 
WORKDIR /backend-flask

# Copy this file from outside container to inside container
# This contains the libraries we want to install to run the app 
COPY requirements.txt requirements.txt

# Install the python libraries required for the app (inside container)
RUN pip3 install -r requirements.txt

# Copy everything in the current directory(outside) into the inside container
# Copy First period =/backend-flask (outside directory) -> Second period =/backend-flask (inside container)
COPY . .

#Enables us set ENV variables inside the container
ENV FLASK_ENV=development


EXPOSE ${PORT}

# python3 -m flask run --host=0.0.0.0 --port=4567
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0", "--port=4567"]