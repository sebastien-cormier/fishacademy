# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Architecture Overview

Fish Academy is a Python Streamlit application for managing private poker game accounting and statistics. The application uses:

- **Frontend**: Streamlit web interface (main entry: `fishacademy-app/accueil.py`)
- **Data Storage**: Elasticsearch cluster with single index `fishacademy`
- **Data Format**: Transaction-based system stored in CSV and indexed in Elasticsearch
- **Infrastructure**: Docker Compose stack with Elasticsearch, Kibana, and Streamlit app

### Key Components

- `fishacademy-app/accueil.py` - Main Streamlit application entry point
- `fishacademy-app/include/` - Core application modules:
  - `app_config.py` - Configuration and environment variables
  - `es_client.py` - Elasticsearch client connection
  - `es_queries.py` - Query functions for data retrieval
  - `utils.py` - Utility functions
- `fishacademy-app/pages/` - Streamlit page modules for different features
- `datas/` - CSV data files and session backups
- `resources/` - Static assets (images, etc.)

### Data Architecture

The system uses a single Elasticsearch index storing poker game transactions:
- Token purchases/sales
- Food contributions
- Player-to-player transactions
- Session management via CSV files

## Development Setup

### Prerequisites
- Docker Desktop installed

### Environment Configuration
1. Copy `.env_EXAMPLE` to `.env`
2. Update these required variables:
   - `ELASTIC_PASSWORD` - Set elasticsearch password
   - `KIBANA_PASSWORD` - Set kibana password  
   - `INIT_DATAS_DOC_ID` - Google Sheets document ID for initial data

### Running the Application
```bash
# Start the entire stack (Elasticsearch, Kibana, Streamlit)
docker compose up -d

# Initialize Elasticsearch index with data
docker exec fishacademy-fishacademy-app-1 python reset_index_import_datas.py

# Verify setup
docker exec fishacademy-fishacademy-app-1 python check_elastic.py
```

### Application Access
- Streamlit app: http://localhost:8501
- Kibana: http://localhost:5601
- Elasticsearch: https://localhost:9200

### Working with the Application Container
```bash
# Access application container for debugging/maintenance
docker exec -it fishacademy-fishacademy-app-1 bash

# Export current data to CSV
docker exec fishacademy-fishacademy-app-1 python export_datas_to_csv.py

# Reset and reimport data
docker exec fishacademy-fishacademy-app-1 python reset_index_import_datas.py
```

## Code Structure

### Configuration
- Environment variables defined in `include/app_config.py`
- Elasticsearch connection via `include/es_client.py`
- Player list and constants in `app_config.py`

### Streamlit Pages Architecture
- Multi-page app with main entry at `accueil.py`
- Page modules in `pages/` directory
- Shared utilities and queries in `include/` directory

### Development Notes
- Uses French language throughout (comments, UI, variable names)
- Python 3.9 runtime in container
- No traditional testing framework - verification via `check_elastic.py`
- Data persistence through Docker volumes for Elasticsearch and mounted directories