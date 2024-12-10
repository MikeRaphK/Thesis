# Create new image:                                     docker build -t <name> .
# List of all available docker images:                  docker images
# Run an image interactively and remove container:      docker run -it --rm <name> bash
# Remove docker image:                                  docker rmi <image id>

# Example
# docker build -t thesis . && docker run -it --rm -e OPENAI_API_KEY=$OPENAI_API_KEY thesis bash

# Pick operating system
FROM ubuntu:20.04

# Pick working directory
WORKDIR /root/

COPY ./docker_files/ /root/

# General dependencies
RUN apt-get update && apt-get upgrade && apt install nano
# Python dependencies
RUN apt install python3 -y && apt install python3-pip -y
# OpenAI dependencies
RUN pip install openai
