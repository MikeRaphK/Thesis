#!/bin/bash

git clone https://github.com/OpenAutoCoder/Agentless.git
cd Agentless
python3 -m venv agentless && source agentless/bin/activate
pip install -r requirements.txt
export PYTHONPATH=$PYTHONPATH:$(pwd)
rm -rf results/
mkdir results

echo -e "\n\n\n\nexport OPENAI_API_KEY="