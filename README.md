
## 🚀 Getting Started (with Docker)

### 1. Prerequisites

- Install **Docker** and **Docker Compose**:
  - [Docker Desktop](https://www.docker.com/products/docker-desktop/)
  - Verify:
    ```bash
    docker --version
    docker-compose --version
    ```

### 2. Set your `.env` file (in root)

Create a `.env` file in the **root** of the project with the following keys:

```env
JIRA_HOST=your-domain.atlassian.net
JIRA_PROTOCOL=https
JIRA_API_TOKEN=your_jira_api_token
JIRA_EMAIL=your_email@example.com
```

### 3. Build & Start the App

Run the following from the project root directory:

```
docker-compose up --build
```
This will build the backend image and start the FastAPI server on http://localhost:8000

Verify
  ```
  http://localhost:8000/health
  ```
