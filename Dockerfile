
# docker build . -t thesis && docker run --rm -e OPENAI_API_KEY=$OPENAI_API_KEY -it -v $(pwd)/docker_files:/root/ thesis /bin/bash

# Pick operating system
FROM ubuntu:22.04

# Set non-interactive mode to avoid prompts during apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Pick working directory
WORKDIR /root/

# General dependencies
RUN apt-get update && apt-get upgrade -y && apt-get install -y nano python3.10 python3-pip git
# OpenAI and Langchain dependencies
RUN pip3 install --no-cache-dir openai langchain langchain-openai langchain-community GitPython langgraph
# Clean-up unnecessary files
RUN apt-get clean && rm -rf /var/lib/apt/lists/*
