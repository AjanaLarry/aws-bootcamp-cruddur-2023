# Week 1 - Homework Challenges


This week, I containerized the frontend and backend applications that will serve the platform. Also, I completed all the Todo lists for the week. Below is a summary of the homework challenges:

# Task 1 - Install Docker and Containerize Apps on Local Machine


The steps below were taken to successfully install Docker on my local machine (Windows OS) and get the same containers running outside of Gitpod / Codespaces.

## Set up System Requirements

---

- Turn on Windows Subsystem for Linux (WSL) feature

![WSL Windows feature.png](/_docs/assets/week-1/WSL_Windows_feature.png)

- Download and Install WSL on Ubuntu-20.04 Linux distro
- Set ubuntu as the default WSL distribution (version 2) using the below command

```bash
$ **wsl.exe —set-default ubuntu-20.04 2**
```

## Install Docker

---

I ran the commands below to install docker engine:

- Update the `apt`  package index and install packages to allow `apt` to use a repository over HTTPS:

```bash
$ sudo apt-get update

$ sudo apt-get install \
      ca-certificates \
      curl \
      gnupg \
      lsb-release
```

- Add Docker’s official GPG key:

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

- Grant read permission for the Docker public key file and updated the package index:

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
sudo apt-get update
```

- Install Docker Engine, containerd, and Docker Compose.

```bash
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
```

- Verify that the Docker Engine installation is successful by running the `hello-world` image:

```bash
sudo docker run hello-world
```

I received the error message below:

```
ERROR: Cannot connect to the Docker daemon at unix:///var/run/docker.sock. Is the docker daemon running?
```

After troubleshooting and researching, I ran the code below to start and enable docker in systemctl:

```
systemctl start docker
systemctl enable docker
```

I tried rerunning the docker run command and received the error below:

```bash
System has not been booted with systemd as init system (PID 1). Can't operate. Failed to connect to bus:
Host is down.
```

- After further troubleshooting, I created a **.wsl-config** file to allow systems to start the docker service when Linux boots:

```bash
**# created script in linux terminal
cat > /etc/wsl.conf
[boot]
systemd=true
exit

# Then shutdown
wsl.exe --shutdown

# Then restart
wsl.exe**
```

- After restarting the Linux terminal, I ran the following commands:

```bash
systemctl enable docker.service
systemctl enable containerd.service
```

![Docker Hello-world image.png](/_docs/assets/week-1/Docker_Hello-world_image.png)

## Clone and Initialize GitHub Repo on Local Machine

---

- Clone git repo with: https://github.com/{$username}/aws-bootcamp-cruddur-2023.git

## Containerize Backend

---

- Change directory to backend-flask, install python and other requirements

```bash
# Install python on Linux terminal
$ Sudo apt install python

#change directory to backend-flask
cd backend-flask

# Install requirements in requirement.text file
pip install -r requirements.txt

# Set environment variables
export FRONTEND_URL="*"
export BACKEND_URL="*"

# Run local server to host backend
python3 -m flask run --host=0.0.0.0 --port=4567
```

![Backend Server 1.png](/_docs/assets/week-1/Backend_Server_1.png)

Response on port 4567:

![Backend Server response 1.png](/_docs/assets/week-1/Backend_Server_response_1.png)

- Stop the local server and proceed to build the docker image using:

```bash
docker build -t  backend-flask ./backend-flask
```

![Backend image successfully built 2.png](/_docs/assets/week-1/Backend_image_successfully_built_2.png)

- Unset environment variable and build container:

```bash
# Unset env variables
unset FRONTEND_URL="*"
unset BACKEND_URL="*"

# Build container using backend-flask image
docker run --rm -p 4567:4567 -it -e FRONTEND_URL='*' -e BACKEND_URL='*' backend-flask
```

![Backend Container Server 2.png](/_docs/assets/week-1/Backend_Container_Server_2.png)

- Response on the web browser:

![Backend Container Server 1.png](/_docs/assets/week-1/Backend_Container_Server_1.png)

## Containerize Frontend

---

- Change the directory to backend-flask, and install node package manager (npm)

```bash
# Change directory to frontend-react-js
cd frontend-react-js

# Install the node package manager
npm install
```

![Install Node module for frontend.png](/_docs/assets/week-1/Install_Node_module_for_frontend.png)

## Task 2 - Implementing Docker Multi-stage build

---

While trying to build the **frontend-react-js** **app** image, I received an error message while using the **docker build command**. To resolve this, I used a Docker CLI plugin (called **Buildx**) that extends the **docker** command with the full support of the features provided by Moby BuildKit builder toolkit.

- Updated the frontend-react-js docker file with an additional script that installs Buildx

```bash
syntax=docker/dockerfile:1
FROM docker
COPY --from=docker/buildx-bin:latest /buildx /usr/libexec/docker/cli-plugins/docker-buildx
RUN docker buildx version
```

![Docker multistage build.png](/_docs/assets/week-1/Docker_multistage_build.png)

- Build the frontend image using the Buildx command

```bash
docker buildx build -t frontend-react-js ./frontend-react-js
```

![Buildx Build Code.png](/_docs/assets/week-1/Buildx_Build_Code.png)

![Frontend image successfully built 1.png](/_docs/assets/week-1/Frontend_image_successfully_built_1.png)

- Run and server the frontend-react app using the created docker images:

```bash
docker run -p 3000:3000 -d frontend-react-js
```

## Task 3 - Push and Tag an Image to DockerHub

---

- Login to DockerHub,  tag and push the backend docker image to the DockerHub repository:

![Push backend image to Dockerhub.png](/_docs/assets/week-1/Push_backend_image_to_Dockerhub.png)

- Tag and push the frontend docker image to the DockerHub repository:

![Push frontend image to Dockerhub 2.png](/_docs/assets/week-1/Push_frontend_image_to_Dockerhub_2.png)

![Pushed cruddur images on Dockerhub.png](/_docs/assets/week-1/Pushed_cruddur_images_on_Dockerhub.png)

## Task 4 - Launch an EC2 Instance, Install Docker, and Pull a Container

---

- Launch Amazon EC2 Linux instance t2.micro, with a SSSMRole attached.
- Connect to ec2 instance using sessions manager

![Ec2 instance login.png](/_docs/assets/week-1/Ec2_instance_login.png)

- Run the below command to Install Docker

```bash
$ sudo amazon-linux-extras install docker
$	sudo service docker start
$	sudo usermod -a -G docker ec2-user
	
# Make docker auto-start

$ sudo chkconfig docker on

# Because you always need it....
$ sudo yum install -y git

# Reboot to verify it all loads fine on its own.
$ sudo reboot
```

## Task 5 - Run Dockerfile as an External Script

---

- Create docker-compose.yaml script to create and serve an apache-httpd webserver on localhost:8080

```bash
version: '3.9'
services:
  apache:
    image: httpd:latest
    container_name: my-apache-app
    ports:
    - '8080:80'
    volumes:
    - ./website:/usr/local/apache2/htdocs
```

- Install docker-compose

```bash
$ sudo curl -L https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose

# Fix permissions after download
$ sudo chmod +x /usr/local/bin/docker-compose

# Add to $PATH
$ sudo ln -s /usr/local/bin/docker-compose /usr/bin/docker-compose
```

![Ec2 instance docker install.png](/_docs/assets/week-1/Ec2_instance_docker_install.png)

## ****Task 6 - Run Docker-compose to pull Image from DockerHub****

---

- Run docker-compose up -d

![ec2 docker-compose container.png](/_docs/assets/week-1/ec2_docker-compose_container.png)

## ****Task 7 - Implement Healthh Check****

- Implement Docker Health Check in the compose file

```bash
healthcheck:
  test: curl --fail http://localhost || exit 1
  interval: 60s
  retries: 5
  start_period: 20s
  timeout: 10s
```

![ec2 docker health check.png](/_docs/assets/week-1/ec2_docker_health_check.png)

- Run healthcheck on server using:

```bash
$ sudo docker inspect --format='' <container_ID>
```

![ec2 docker health check inspect.png](/_docs/assets/week-1/ec2_docker_health_check_inspect.png)

## Task 8 - Docker Best Practices

Finally, I did a review of my docker file to ensure best practices are implemented. The below was implemented:

- Use multi-stage build as this reduce the size of the final build.
- Exclude files not relevant to the build  with .dockerignore.
- Do not install unnecessary packages.