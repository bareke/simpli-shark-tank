<div align="center">
  <a style="vertical-align: middle;" href="https://simpliroute.com/" target="blank">
    <img src="https://simpliroute.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FLogoSimpliRoute.ae5a87d3.png&w=256&q=100" width="250" alt="Inndico Logo" />
  </a>
  
</div>


## Description

AI tool for answering questions and queries about our data

## Environment Variables

_Make sure you provide the correct credentials before running the project_

```python
# DATABASE
DATABASE_TYPE=postgresql
SERVICE_DATABASE_URL_TENANT=postgresql://{{user}}:{{password}}@{{host}}:{{port}}/{{database}}

# STORE
STORE_HOST=redis-dev
STORE_PORT=6379
STORE_USERNAME=default
STORE_PASSWORD=abc123
```

## Run project

### Local

```bash
# 1. Exec cloud-sql-proxy

# 2. Install python 3

# 3. Create virtual environment
$ python -m venv venv

# 4. Activate virtual environment

# Windows
$ .\venv\Scripts\activate

# Linux
$ source venv/bin/activate

# 5. Install dependencies
$ pip install -r requirements.txt

# 6. Create file .env (copy env.sample)

# 7. Execute app
$ python main.py

# 8. Open browser in http://localhost:8084/
```
