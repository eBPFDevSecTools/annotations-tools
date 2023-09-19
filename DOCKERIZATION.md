# Steps for Docker Initialization

- First clone the repo containing the DockerFile.

    `git clone https://github.com/eBPFDevSecTools/annotations-tools.git`

- Find the folder named "dockerization.tar.xz" and extract using the following command.

    `tar -xf dockerization.tar.xz`

- Ensure that there is a DockerFile and a docker-compose.yml file in the extracted folder. There will be two shell scripts namely "setup.sh" and "clean.sh".

    `chmod +x setup.sh`

- Execute the setup.sh script to initialize the elasticsearch and kibana containers and to build the required Ubuntu image.

    `./setup.sh`

- Ensure that the docker image named "ibm/ubuntu" is present in the list of docker images. Run the following command.

    `sudo docker images -a`

- Run the Ubuntu container by executing the following command.

    `sudo docker run -it --privileged --network host ibm/ubuntu:latest`

