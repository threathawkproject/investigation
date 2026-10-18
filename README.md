# ThreatHawk — Investigation Service

The Investigation service is a Python/FastAPI component of the [ThreatHawk project](https://github.com/threathawkproject). Its source exposes endpoints for creating, executing, and viewing threat investigations, with Meilisearch used for indexing.

## Key capabilities visible in the source

- Create an investigation via `POST /create_investigation`.
- Trigger investigation processing via `POST /investigate`.
- Display investigation information via `POST /display`.
- Retrieve available investigation types via `GET /get_investigation_types`.
- Check the service root via `GET /`.

The code also contains an unfinished `save_investigation` route; it should not be presented as a supported feature.

## Technology

Python, FastAPI, Uvicorn, Meilisearch, and Docker.

## Local development

1. Provide a running Meilisearch instance. By default the application looks for it at `http://localhost:7700`. Set `MEILI_URL` to use another address.
2. Install Python dependencies from the repository root:

   ```bash
   pip install -r requirements.txt
   ```

3. Start the service from the `src` folder so its local imports resolve:

   ```bash
   cd src
   uvicorn main:app --reload
   ```

4. Open `http://127.0.0.1:8000/docs` to inspect the automatically generated FastAPI API documentation.

Meilisearch is contacted and the `investigations` index is created during application import; ensure the dependency is reachable before startup.

## Code layout

- `src/main.py` — FastAPI application and route definitions
- `src/models/` — request and domain models
- `src/configs/` — configuration files
- `src/utils.py` — investigation operations
- `src/consts.py` — supported investigation types
- `Dockerfile` and `docker-compose.yml` — container configuration

## Security and project status

The current FastAPI setup configures broad CORS access. Authentication, authorization, dependency health checks, and production configuration should be reviewed before exposing this service outside a trusted development environment.

This documentation describes source-visible features. API behavior and end-to-end deployment have not been independently tested in this documentation pass.
