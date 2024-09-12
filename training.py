from ddls import ddls_database

def init_training(vn):

    # Load all ddl of the database
    [vn.train(ddl=ddl)for ddl in ddls_database]

    context_business = """
    AI technology to help you optimize your routes.
    Simplify your operation and maximize your delivery results with the best performing last mile software according to our customers.
    """

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

    vn.train(
        question="¿Cuántas rutas fueron creadas hoy?",
        sql="SELECT COUNT(*) FROM routes_route WHERE planned_date = CURRENT_DATE;"
    )

    vn.train(
        question="",
        sql="SELECT COUNT(r.id) AS total_rutas FROM public.routes_route r JOIN public.routes_vehicle v ON r.vehicle_id = v.id JOIN public.accounts_account a ON v.account_id = a.id WHERE a.name ILIKE '%Liverpool%' AND r.planned_date = CURRENT_DATE;"
    )

    vn.train(
        question="",
        sql="SELECT COUNT(r.id) AS total_rutas FROM public.routes_route r JOIN public.routes_vehicle v ON r.vehicle_id = v.id JOIN public.accounts_account a ON v.account_id = a.id WHERE a.name ILIKE '%falabella%' AND r.planned_date = CURRENT_DATE;"
    )

    vn.train(
        question="¿Cuantos planes tienen estado completado en el rango de 1 hora?",
        sql="SELECT COUNT(*) FROM public.routes_plan WHERE status = 'completed' AND (modified - created) <= interval '1 hour';"
    )

    vn.train(
        question="¿Que porcentaje de visitas tiene estado fallido hoy?",
        sql="SELECT (COUNT(*) * 100.0 / (SELECT COUNT(*) FROM routes_visit WHERE planned_date = CURRENT_DATE)) AS percentage_failed FROM routes_visit WHERE planned_date = CURRENT_DATE AND status = 'failed';"
    )

    vn.train(
        question="¿Qué porcentaje de visitas tiene estado completado hoy?",
        sql="SELECT COUNT(*) FILTER (WHERE status = 'completed') * 100.0 / COUNT(*) FROM routes_visit WHERE planned_date = CURRENT_DATE;"
    )

    vn.train(
        question="¿Cuál es el porcentaje de visitas de la cuenta andina qué están pendientes hoy?",
        sql="SELECT (COUNT(CASE WHEN v.status = 'pending' THEN 1 END) * 100.0 / (SELECT COUNT(*) FROM public.routes_visit rv JOIN public.accounts_account aa ON rv.account_id = aa.id WHERE rv.planned_date = CURRENT_DATE AND aa.name ILIKE '%Andina%')) AS percentage_completed FROM public.routes_visit v JOIN public.accounts_account a ON v.account_id = a.id WHERE v.planned_date = CURRENT_DATE AND a.name ILIKE '%Andina%';"
    )

    vn.train(
        question="¿Cuántas visitas planificadas hoy hay en Santiago de Chile?",
        sql="SELECT COUNT(*) AS total_visitas FROM public.routes_visit WHERE planned_date::date = CURRENT_DATE AND CAST(latitude AS numeric) BETWEEN -33.5 AND -33.0 AND CAST(longitude AS numeric) BETWEEN -70.7 AND -70.3;"
    )

    vn.train(
        question="¿Cuántas visitas planificadas hoy hay en México?",
        sql="SELECT COUNT(*) AS total_visitas FROM public.routes_visit WHERE planned_date::date = CURRENT_DATE AND CAST(latitude AS numeric) BETWEEN 19.0 AND 19.5 AND CAST(longitude AS numeric) BETWEEN -99.3 AND -98.9;"
    )

    vn.train(
        question="¿Cuántas visitas planificadas hay hoy en Santiago de Chile si la longitud es -33.0 y la latitud es -70.3?",
        sql="SELECT COUNT(*) AS total_visitas FROM public.routes_visit WHERE planned_date::date = CURRENT_DATE AND CAST(latitude AS numeric) BETWEEN 19.0 AND 19.5 AND CAST(longitude AS numeric) BETWEEN -99.3 AND -98.9;"
    )

    vn.train(
        question="¿Cuántas visitas planificadas hay hoy en México?",
        sql="SELECT COUNT(*) AS total_visitas FROM public.routes_visit WHERE planned_date::date = CURRENT_DATE AND CAST(latitude AS numeric) BETWEEN 19.0 AND 19.5 AND CAST(longitude AS numeric) BETWEEN -99.3 AND -98.9;"
    )

    vn.train(
        question="¿Muestra las primeras 10 cuentas en orden descendente que van a vencer este mes?",
        sql="SELECT * FROM public.accounts_account  WHERE active_until >= CURRENT_DATE  AND active_until < CURRENT_DATE + INTERVAL '1 month'  ORDER BY active_until DESC  LIMIT 10;"
    )

    vn.train(
        question="Quiero saber el top 10 de cuentas que más visitas tuvieron ayer",
        sql="SELECT aa.name AS client_name, aa.status AS estado, COUNT(rv.id) AS number_of_visits FROM public.routes_visit rv JOIN public.accounts_account aa ON rv.account_id = aa.id WHERE rv.planned_date::date = CURRENT_DATE - INTERVAL '1 day' GROUP BY aa.name, aa.status ORDER BY number_of_visits DESC LIMIT 10;"
    )

    vn.train(
        question="Quiero saber el top 5 de cuentas activas por pais",
        sql="SELECT country, COUNT(*) AS number_of_active_accounts FROM public.accounts_account WHERE status = 'active' GROUP BY country ORDER BY number_of_active_accounts DESC LIMIT 5;"
    )

    vn.train(
        question="cuantos kilometros tenemos registrados de ayer",
        sql="SELECT SUM(kilometers) AS total_kilometers FROM public.routes_route WHERE planned_date::date = CURRENT_DATE - INTERVAL '1 day';"
    )

    vn.train(
        question="cuantas rutas tuvimos ayer con más de 50 visitas",
        sql="SELECT COUNT(*) AS rutas_con_mas_de_50_visitas FROM (SELECT rr.id FROM public.routes_route rr JOIN public.routes_visit rv ON rr.id = rv.route_id WHERE rr.planned_date::date = CURRENT_DATE - INTERVAL '1 day' GROUP BY rr.id HAVING COUNT(rv.id) > 50) AS rutas_filtradas;"
    )

    vn.train(
        question="dame todos los usaurios y token de la cuenta Andina Paraguay (id 88557)",
        sql="select a.key, a.user_id, au.name, au.email, * from accounts_account aa join  public.accounts_user au on aa.id = au.account_id join public.authtoken_token a on au.id = a.user_id where aa.id = 88557;"
    )

    vn.train(
        question="cuantas cuentas de liverpool tenemos registradas",
        sql="SELECT COUNT(*) FROM public.accounts_account WHERE 'name' LIKE '%Liverpool%' AND status = 'active';"
    )
