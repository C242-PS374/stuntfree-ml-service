## StuntFree ML Service 🤖

### Overview

**StuntFree ML Service** is designed to load and serve machine learning models efficiently using **gRPC**.

### Features

- **gRPC Communication**: For performance and remote procedure call (RPC) communication.
- **Dynamic Model Loading**: Load and infer with models on demand from Cloud Storage.
- **Dockerized Deployment**: Simplified setup and portability using Docker and deploy on Cloud Run.

## Installation

### Local Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/C242-PS374/stuntfree-ml-service.git
   cd stuntfree-ml-service
   ```

2. Set up a virtual environment and install dependencies:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt # pip install -r requirements-dev.txt, If you want to set development settings too
   ```

3. Start the service:
   ```bash
   python src/server.py
   ```

### Using Docker

1. Build the Docker image:
   ```bash
   docker build -t stuntfree-ml-service .
   ```

2. Run the Docker container:
   ```bash
   docker run -p 50051:50051 stuntfree-ml-service
   ```

## Usage

1. Start the StuntFree ML Service (gRPC server service) locally or via Docker.
2. Use a gRPC client to interact and connect as the Main API service. [Main API Service](https://github.com/C242-PS374/stuntfree-api)
