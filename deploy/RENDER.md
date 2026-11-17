# Render free demo

Deploy `render.yaml` as a Blueprint from the repository root. It creates one
free Docker web service. Set HR_TOKEN when Render prompts; enter that same
value in the HR Portal. Never put this credential in GitHub.

The public port serves Streamlit. FastAPI binds only to loopback inside the
container. The image builds an evaluated TF-IDF index from the bundled sample
documents. No Gemini key or embedding download is needed for this demo.

The health check is `/_stcore/health`. The launcher waits for API index readiness
before exposing Streamlit and stops both processes on shutdown or failure.

Free storage is ephemeral: document uploads, deletions, feedback counters,
MLflow runs and logs are not durable. A restart restores the image's sample
corpus and index. Do not use this setup as a production document repository.

Local equivalent (Docker required):

```sh
docker build -f Dockerfile.render -t rag-ops-render .
docker run --rm -p 10000:10000 -e HR_TOKEN rag-ops-render
```

Set HR_TOKEN in your shell before the run command. Open http://localhost:10000.
