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
# APP
APP_PORT=8084

# IA
IA_APIKEY='sk-abc'

# DATABASE
DB_HOST='127.0.0.1'
DB_NAME='database name'
DB_USER='user'
DB_PASSWORD='password123'
DB_PORT='1010'
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
