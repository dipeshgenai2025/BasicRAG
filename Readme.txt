Plan:
Base LLM: LLaMA 3.1 8B Instruct (Q4_K_M under Ollama)
Embeddings: bge-m3
Vector DB: Qdrant
Orchestration Framework: LlamaIndex (proto) + LangChain (prod)


Prerequsits for Windows
1. WSL
2. Docker for Windows




1. Create Linux distro OR VM on Linux or WSL on Windows to create a Linux runnable
- Enable docker integration

2. Create seperate directory for this project
- $ mkdir SchoolStudyRAG
- $ cd SchoolStudyRAG

3. Create Python virtual environment
- $ sudo apt-get update
- $ sudo apt-get install python3-venv
- $ sudo apt-get install pip -y
- $ python3 -m venv .SchoolStudyRAGEnv

4. Launch VS Code and locate the same path (<PWD>\SchoolStudyRAG\)

5. Open terminal and activate the Python3 environment
- $ source .SchoolStudyRAGEnv/bin/activate

6. Launch the Qdrant docker image
- Please visit following link for Qdrant information,  https://qdrant.tech/documentation/quickstart/
- $ docker pull qdrant/qdrant
- $ docker run -d --name qdrant -p 6333:6333 -p 6334:6334 -v "$(pwd)/qdrant_storage:/qdrant/storage:z" qdrant/qdrant
	This will start the Qdrant server and same can be checked on http://localhost:6333/dashboard
- And for the next run just docker start qdrant

7. Launch the Ollama docker image
- $ docker pull ollama/ollama
- $ docker run -d --name ollama -p 11434:11434 -v /home/dipesh/SchoolStudyRAG/local_models:/root/.ollama ollama/ollama:latest
	This will start the ollama server and same can be checked on http://localhost:11434
- And for the next run just docker start ollama

9. Pull required model
- $ docker exec -it ollama ollama pull mxbai-embed-large
- $ docker exec -it ollama ollama pull gemma3:4b
- $ docker exec -it ollama ollama list
- $ docker exec -it ollama ollama pull gemma3:12b
- $ docker exec -it ollama ollama rm llama3.1:8b deepseek-r1:8b
- $ docker exec -it ollama ollama pull deepseek-r1:8b
llama3.1:8b
mistral:7b <Good one>
deepseek-r1:8b

7. Install required Python packages
- $ pip install -r requirements.txt
