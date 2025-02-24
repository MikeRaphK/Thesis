
# docker build . -t thesis && docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -it -v $(pwd)/docker_files:/root/ thesis /bin/bash

# Pick operating system
FROM ubuntu:20.04

# Set non-interactive mode to avoid prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Pick working directory
WORKDIR /root/

# General dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y nano python3.8 python3-pip git && rm -rf /var/lib/apt/lists/*
# OpenAI and Langchain dependencies
RUN pip3 install --no-cache-dir openai==1.64.0 langchain==0.2.17 langchain-openai==0.1.25 langchain-community==0.2.19 GitPython==3.1.44
# Clean-up unnecessary files
RUN apt-get clean
