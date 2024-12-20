
# docker build . -t thesis && docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -it thesis /bin/bash

# Pick operating system
FROM ubuntu:20.04

# Pick working directory
WORKDIR /root/

# Copy important files
COPY ./docker_files/ /root/

# General dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install nano -y
# Python dependencies
RUN apt-get install python3.8 -y python3-pip -y
# OpenAI and Langchain dependencies
RUN pip3 install openai==1.57.2 langchain-openai==0.1.25 langchain==0.2.17
# Clean-up unnecessary files
RUN apt-get clean
