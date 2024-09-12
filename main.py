# The import statement will vary depending on your LLM and vector database. This is an example for OpenAI + ChromaDB

from vanna.flask import VannaFlaskApp
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from environment import settings

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={'api_key': settings.get('ia_apikey'), 'model': 'gpt-4o-mini'})

vn.connect_to_postgres(
    host=settings.get('db_host'),
    dbname=settings.get('db_name'),
    user=settings.get('db_user'),
    password=settings.get('db_password'),
    port=settings.get('db_port')
)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

plan = vn.get_training_plan_generic(df_information_schema)
print('my plan is', plan)

app = VannaFlaskApp(
    vn,
    logo="https://simpliroute.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FLogoSimpliRoute.ae5a87d3.png&w=256&q=100",
    sql=False,
    title="Bienvenido al Simpli del Futuro - DataMO",
    subtitle="smart queries made Simpli",
    allow_llm_to_see_data=True,
    csv_download=True,
    chart=False,
    redraw_chart=False,
    table=False,
)
app.run()
