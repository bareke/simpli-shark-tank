# The import statement will vary depending on your LLM and vector database. This is an example for OpenAI + ChromaDB

from vanna.flask import VannaFlaskApp
from vanna.openai.openai_chat import OpenAI_Chat
from vanna.chromadb.chromadb_vector import ChromaDB_VectorStore

from ddls import ddl_visits, ddl_routes, ddl_account, ddl_account_user
from environment import settings

class MyVanna(ChromaDB_VectorStore, OpenAI_Chat):
    def __init__(self, config=None):
        ChromaDB_VectorStore.__init__(self, config=config)
        OpenAI_Chat.__init__(self, config=config)

vn = MyVanna(config={'api_key': settings.get('ia_apikey'), 'model': 'gpt-3.5-turbo'})

vn.connect_to_postgres(
    host=settings.get('db_host'),
    dbname=settings.get('db_name'),
    user=settings.get('db_user'),
    password=settings.get('db_password'),
    port=settings.get('db_port')
)

df_information_schema = vn.run_sql("SELECT * FROM INFORMATION_SCHEMA.COLUMNS")

context_business = """
AI technology to help you optimize your routes.
Simplify your operation and maximize your delivery results with the best performing last mile software according to our customers.
"""

# ddl_final = ddl_visits + ddl_routes

vn.train(ddl=ddl_visits)
vn.train(ddl=ddl_routes)
vn.train(ddl=ddl_account)
vn.train(ddl=ddl_account_user)

vn.train(documentation=context_business)

vn.train(
    question="Encontrar usuarios por account id", 
    sql="SELECT id, name from accounts_user where account_id = 25057;"
)

vn.train(
    question="Encontrar cuentas por token", 
    sql="SELECT au.account_id, au.id AS user_id, a.key AS token FROM accounts_user au INNER JOIN authtoken_token a ON au.id = a.user_id WHERE a.key IN ('blabla');"
)

vn.train(
    question="Encontrar tokens por account id", 
    sql="SELECT au.account_id, au.id AS user_id, a.key AS token FROM accounts_user au INNER JOIN authtoken_token a ON au.id = a.user_id WHERE au.account_id = 25057;"
)

vn.train(
    question="Encontrar visitar por dia , conductor y account", 
    sql="SELECT id, log_id, created, modified, status, status_changed, l25_address, l25_latitude, l25_longitude, load, window_start, window_end, duration, contact_name, contact_phone, reference, notes, checkin_time, checkin_latitude, checkin_longitude, checkout_time, checkout_latitude, checkout_longitude, checkout_comment, account_id, signature, estimated_time_arrival, estimated_time_departure, planned_date, route_id, checkout_observation_id, l25_account_id, order, load_2, load_3, window_end_2, window_start_2, track_id, priority, contact_email, has_alert, priority_level, calculated_service_time, on_its_way, geocode_alert, programmed_date, vtsl_typ_2, current_eta, postal_code, flex1, geocode_id, checkout_user_id FROM routes_visit WHERE account_id = 29642 AND planned_date = \"2024-04-08\" AND checkout_user_id = 80664;"
)

vn.train(
    question="sacar un promedio de tiempo desde que la app envío el mensaje hasta que la api lo recibió, siendo mas facil determinar usuarios que sobrepasan el promedio para ir con otra query a buscar por visitas en particular, ademas despliega las cantidades de visitas por estado, lo que permite observar si quedaron muchas pendientes.", 
    sql="SELECT ac.app_version, ac.id, COUNT(rv.id) AS visits, rr.planned_date AS planned_date, AVG(rv.modified - rv.checkout_time) AS Checkout_time, SUM(CASE WHEN rv.status = 'completed' THEN 1 ELSE 0 END) AS completed, SUM(CASE WHEN rv.status = 'failed' THEN 1 ELSE 0 END) AS failed, SUM(CASE WHEN rv.status = 'pending' THEN 1 ELSE 0 END) AS pending FROM accounts_user ac INNER JOIN routes_route rr ON ac.id = rr.driver_id INNER JOIN routes_visit rv ON rr.id = rv.route_id WHERE ac.account_id = 29642 AND is_driver = TRUE AND rr.driver_id = ac.id AND rr.planned_date BETWEEN '2024-04-08' AND '2024-04-09' GROUP BY ac.app_version, ac.id, rr.planned_date, rv.modified - rv.checkout_time ORDER BY Checkout_time DESC, rr.planned_date, ac.app_version, pending DESC;"
)

vn.train(
    question="determinar las rutas por usuario y versión APP en determinadas fechas", 
    sql="SELECT ac.app_version, ac.id, COUNT(rr.id) AS routes FROM accounts_user ac INNER JOIN routes_route rr ON ac.id = rr.driver_id WHERE ac.account_id = 29642 AND is_driver = TRUE AND rr.driver_id = ac.id AND rr.planned_date BETWEEN '2024-03-10' AND '2024-04-10' GROUP BY ac.app_version, ac.id ORDER BY ac.app_version;"
)

vn.train(
    question="Busca una cuenta que le pertenezca al cliente mexicano Liverpool",
    sql="SELECT * FROM accounts_account WHERE country = 'MX' AND name = 'Liverpool';"
)

vn.train(
    question="numero de cuentas del cliente liverpool en estado activo",
    sql="SELECT COUNT(*) FROM public.accounts_account WHERE name LIKE '%Liverpool%' AND status = 'active';"
)

vn.train(
    question="cuantos usuarios conductores estan activos",
    sql="SELECT COUNT(*) FROM public.accounts_user WHERE is_driver = true AND status = 'active';"
)

vn.train(
    question="¿Cuál es el usuario más antiguo creado cómo owner?",
    sql="SELECT * FROM public.accounts_user WHERE is_owner = TRUE ORDER BY created ASC LIMIT 1;"
)

vn.train(
    question="cuantos usuarios activos tiene liverpool",
    sql="SELECT COUNT(*) FROM public.accounts_user WHERE status = 'active' AND account_id IN (SELECT id FROM public.accounts_account WHERE name LIKE '%Liverpool%'AND status = 'active');"
)

plan = vn.get_training_plan_generic(df_information_schema)
print('my plan is', plan)

app = VannaFlaskApp(
    vn,
    logo="https://simpliroute.com/_next/image?url=%2F_next%2Fstatic%2Fmedia%2FLogoSimpliRoute.ae5a87d3.png&w=256&q=100",
    sql=False,
    title="Bienvenido al Simpli del Futuro",
    subtitle="Tu herramienta de IA para responder dudas y consultas de nuestros datos",
    allow_llm_to_see_data=True,
    csv_download=True,
    chart=False,
    redraw_chart=False
)
app.run()
