# RAG API

A Retrieval-Augmented Generation (RAG) API built with FastAPI, ChromaDB, and Ollama. This API enables semantic search and question-answering over your knowledge base using vector embeddings and large language models.

## 🚀 Features

- **Semantic Search**: Query your knowledge base using natural language
- **Vector Database**: ChromaDB for efficient similarity search
- **LLM Integration**: Ollama integration for generating contextual answers
- **Mock Mode**: Test mode for CI/CD pipelines without requiring Ollama
- **Docker Support**: Containerized deployment ready
- **Kubernetes Ready**: Includes deployment and service manifests
- **CI/CD Pipeline**: Automated testing with GitHub Actions

## 📋 Table of Contents

- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Testing](#testing)
- [Docker Deployment](#docker-deployment)
- [Kubernetes Deployment](#kubernetes-deployment)
- [Project Structure](#project-structure)
- [Development](#development)
- [Contributing](#contributing)

## 🏗️ Architecture

```
┌─────────────┐
│   Client    │
└──────┬──────┘
       │
       ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  FastAPI    │────▶│  ChromaDB    │     │   Ollama    │
│   Server    │     │ (Vector DB)  │     │     LLM     │
└─────────────┘     └─────────────┘     └─────────────┘
```

1. **FastAPI Server**: RESTful API endpoint for queries
2. **ChromaDB**: Persistent vector database storing document embeddings
3. **Ollama**: Local LLM for generating answers from retrieved context

## 📦 Prerequisites

- Python 3.11+
- [Ollama](https://ollama.com/) installed and running (for production)
- Docker (optional, for containerized deployment)
- Kubernetes cluster (optional, for K8s deployment)

## 🔧 Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd rag-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install fastapi uvicorn chromadb ollama
   ```

4. **Initialize the database**
   ```bash
   python embed.py
   ```

5. **Start the server**
   ```bash
   uvicorn app:app --host 0.0.0.0 --port 8000 --reload
   ```

The API will be available at `http://localhost:8000`

## ⚙️ Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `USE_MOCK_LLM` | Enable mock mode for testing (0 or 1) | `0` |
| `OLLAMA_HOST` | Ollama server host (for Docker) | `http://localhost:11434` |

### Mock Mode

For CI/CD and testing without Ollama:
```bash
export USE_MOCK_LLM=1
uvicorn app:app --host 0.0.0.0 --port 8000
```

## 📖 Usage

### Query the Knowledge Base

```bash
curl -X POST "http://localhost:8000/query?q=What is Kubernetes?"
```

**Response:**
```json
{
  "answer": "Kubernetes is a container orchestration platform that manages containers at scale..."
}
```

### Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    params={"q": "What is Kubernetes?"}
)
print(response.json()["answer"])
```

## 🔌 API Endpoints

### POST `/query`

Query the knowledge base with a natural language question.

**Parameters:**
- `q` (query string, required): The question to ask

**Response:**
```json
{
  "answer": "Generated answer based on retrieved context"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/query?q=What is Kubernetes?"
```

**Error Response:**
```json
{
  "detail": "Error message"
}
```

### Interactive API Documentation

FastAPI provides automatic interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

## 🧪 Testing

### Run Semantic Tests

```bash
# Make sure the server is running
uvicorn app:app --host 0.0.0.0 --port 8000 &

# Run tests
python semantic_test.py
```

The test suite validates:
- API connectivity
- Semantic search functionality
- Response quality (keyword presence)

### CI/CD Testing

The GitHub Actions workflow automatically:
1. Installs dependencies
2. Rebuilds embeddings
3. Starts API in mock mode
4. Runs semantic tests

## 🐳 Docker Deployment

### Build the Image

```bash
docker build -t rag-api .
```

### Run the Container

```bash
docker run -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  rag-api
```

**Note**: For Linux, you may need to use `--network host` or set `OLLAMA_HOST` to your host's IP address.

### Docker Compose (Optional)

Create a `docker-compose.yml`:

```yaml
version: '3.8'
services:
  rag-api:
    build: .
    ports:
      - "8000:8000"
    environment:
      - OLLAMA_HOST=http://host.docker.internal:11434
    volumes:
      - ./db:/app/db
```

## ☸️ Kubernetes Deployment

### Prerequisites

- Kubernetes cluster running
- `kubectl` configured

### Deploy

1. **Build and push the Docker image** (or use local image)

2. **Apply Kubernetes manifests**
   ```bash
   kubectl apply -f deployment.yaml
   kubectl apply -f service.yaml
   ```

3. **Check deployment status**
   ```bash
   kubectl get deployments
   kubectl get services
   ```

4. **Access the service**
   ```bash
   # Get NodePort
   kubectl get service rag-app-service
   
   # Access via NodePort (replace <NODE_IP> and <NODE_PORT>)
   curl -X POST "http://<NODE_IP>:<NODE_PORT>/query?q=What is Kubernetes?"
   ```

### Configuration

The `deployment.yaml` includes:
- Replica count: 1
- Container port: 8000
- Environment variable: `OLLAMA_HOST=host.docker.internal:11434`

Modify as needed for your cluster setup.

## 📁 Project Structure

```
rag-api/
├── app.py                 # FastAPI application and endpoints
├── embed.py               # Script to initialize ChromaDB with documents
├── semantic_test.py       # Test suite for API validation
├── Dockerfile             # Docker container definition
├── deployment.yaml        # Kubernetes deployment manifest
├── service.yaml           # Kubernetes service manifest
├── .github/
│   └── workflows/
│       └── ci.yml         # GitHub Actions CI/CD pipeline
├── db/                    # ChromaDB data directory (gitignored)
├── k8s.txt                # Sample knowledge base document
├── .gitignore             # Git ignore rules
└── README.md              # This file
```

## 🔨 Development

### Adding New Documents

1. **Add your document** (e.g., `new_doc.txt`)

2. **Update `embed.py`** to include the new document:
   ```python
   with open("new_doc.txt", "r") as f:
       text = f.read()
   
   collection.add(documents=[text], ids=["new_doc"])
   ```

3. **Rebuild embeddings**
   ```bash
   python embed.py
   ```

### Code Structure

- **`app.py`**: Main FastAPI application
  - `/query` endpoint for semantic search
  - Mock mode support for testing
  - Error handling

- **`embed.py`**: Database initialization
  - Reads documents from files
  - Creates embeddings and stores in ChromaDB

- **`semantic_test.py`**: Integration tests
  - Validates API responses
  - Checks semantic quality

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Guidelines

- Follow PEP 8 style guide
- Add tests for new features
- Update documentation as needed
- Ensure CI/CD pipeline passes

## 📝 License

[Add your license here]

## 🙏 Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) - Modern web framework
- [ChromaDB](https://www.trychroma.com/) - Vector database
- [Ollama](https://ollama.com/) - Local LLM runtime

## 📞 Support

For issues and questions:
- Open an issue on GitHub
- Check the [documentation](http://localhost:8000/docs) when the server is running

---

**Note**: Make sure Ollama is running and the `tinyllama` model is pulled before using the API in production mode:
```bash
ollama pull tinyllama
```
