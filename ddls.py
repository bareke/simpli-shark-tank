
ddl_routes = """
    CREATE TABLE public.routes_route (
        created timestamptz NOT NULL,
        modified timestamptz NOT NULL,
        id uuid NOT NULL,
        planned_date date NOT NULL,
        estimated_time_start time NOT NULL,
        estimated_time_end time NOT NULL,
        total_duration interval NOT NULL,
        total_distance int4 NOT NULL,
        total_load float8 NOT NULL,
        total_load_percentage int2 NOT NULL,
        location_start_address varchar(508) NOT NULL,
        location_start_latitude numeric(9, 6) NOT NULL,
        location_start_longitude numeric(9, 6) NOT NULL,
        location_end_address varchar(508) NOT NULL,
        location_end_latitude numeric(9, 6) NOT NULL,
        location_end_longitude numeric(9, 6) NOT NULL,
        driver_id int4 NULL,
        vehicle_id int4 NOT NULL,
        plan_id uuid NOT NULL,
        status varchar(100) NOT NULL,
        status_changed timestamptz NOT NULL,
        "comment" varchar(254) NULL,
        end_time timestamptz NULL,
        start_time timestamptz NULL,
        total_load_2 float8 NOT NULL,
        total_load_2_percentage int2 NOT NULL,
        total_load_3 float8 NOT NULL,
        total_load_3_percentage int2 NOT NULL,
        kilometers numeric(6, 1) NULL,
        latitude_finish numeric(9, 6) NULL,
        latitude_init numeric(9, 6) NULL,
        longitude_finish numeric(9, 6) NULL,
        longitude_init numeric(9, 6) NULL,
        is_revised bool NOT NULL,
        reference varchar(254) NULL,
        CONSTRAINT routes_route_pkey PRIMARY KEY (id),
        CONSTRAINT routes_route_total_distance_check CHECK ((total_distance >= 0)),
        CONSTRAINT routes_route_total_load_2_percentage_check CHECK ((total_load_2_percentage >= 0)),
        CONSTRAINT routes_route_total_load_3_percentage_check CHECK ((total_load_3_percentage >= 0)),
        CONSTRAINT routes_route_total_load_percentage_check CHECK ((total_load_percentage >= 0))
    );
    CREATE INDEX routes_rout_planned_350ab5_idx ON public.routes_route USING btree (planned_date);
    CREATE INDEX routes_rout_planned_492a0d_idx ON public.routes_route USING btree (planned_date, status);
    CREATE INDEX routes_route_17565772 ON public.routes_route USING btree (driver_id);
    CREATE INDEX routes_route_35ec04dc ON public.routes_route USING btree (vehicle_id);
    CREATE INDEX routes_route_60fb6a05 ON public.routes_route USING btree (plan_id);
    CREATE INDEX routes_route_reference_eccf1816 ON public.routes_route USING btree (reference);
    CREATE INDEX routes_route_reference_eccf1816_like ON public.routes_route USING btree (reference varchar_pattern_ops);


    -- public.routes_route foreign keys

    ALTER TABLE public.routes_route ADD CONSTRAINT routes_route_driver_id_31d00f58_fk_accounts_user_id FOREIGN KEY (driver_id) REFERENCES public.accounts_user(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_route ADD CONSTRAINT routes_route_plan_id_b3e926ac_fk_routes_plan_id FOREIGN KEY (plan_id) REFERENCES public.routes_plan(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_route ADD CONSTRAINT routes_route_vehicle_id_88429bf7_fk_routes_vehicle_id FOREIGN KEY (vehicle_id) REFERENCES public.routes_vehicle(id) DEFERRABLE INITIALLY DEFERRED;
    """

ddl_visits = """
    CREATE TABLE public.routes_visit (
        id serial4 NOT NULL,
        created timestamptz NOT NULL,
        modified timestamptz NOT NULL,
        status varchar(100) NOT NULL,
        status_changed timestamptz NOT NULL,
        title varchar(254) NOT NULL,
        address varchar(508) NOT NULL,
        latitude numeric(9, 6) NULL,
        longitude numeric(9, 6) NULL,
        "load" float8 NULL,
        window_start time NULL,
        window_end time NULL,
        duration interval NOT NULL,
        contact_name varchar(254) NOT NULL,
        contact_phone varchar(254) NOT NULL,
        reference varchar(254) NOT NULL,
        notes text NOT NULL,
        checkin_time timestamptz NULL,
        checkin_latitude numeric(9, 6) NULL,
        checkin_longitude numeric(9, 6) NULL,
        checkout_time timestamptz NULL,
        checkout_latitude numeric(9, 6) NULL,
        checkout_longitude numeric(9, 6) NULL,
        checkout_comment text NOT NULL,
        account_id int4 NOT NULL,
        signature varchar(100) NULL,
        estimated_time_arrival time NULL,
        estimated_time_departure time NULL,
        planned_date date NULL,
        route_id uuid NULL,
        checkout_observation_id uuid NULL,
        "order" int4 NULL,
        load_2 float8 NULL,
        load_3 float8 NULL,
        window_end_2 time NULL,
        window_start_2 time NULL,
        tracking_id varchar(254) NULL,
        priority bool NULL,
        contact_email text NULL,
        has_alert bool NULL,
        priority_level int4 NULL,
        calculated_service_time interval NULL,
        on_its_way timestamptz NULL,
        geocode_alert varchar(22) NULL,
        programmed_date date NULL,
        visit_type_id int4 NULL,
        current_eta timestamptz NULL,
        postal_code varchar(15) NULL,
        fleet_id int4 NULL,
        checkout_user_id int4 NULL,
        geocoder_id varchar(64) NULL,
        CONSTRAINT routes_visit_pkey PRIMARY KEY (id)
    )
    WITH (
        autovacuum_vacuum_scale_factor=0.0,
        autovacuum_vacuum_threshold=5000,
        autovacuum_analyze_scale_factor=0.0,
        autovacuum_analyze_threshold=5000
    );
    CREATE INDEX routes_visit_11fe7161 ON public.routes_visit USING btree (visit_type_id);
    CREATE INDEX routes_visit_3b4c8329 ON public.routes_visit USING btree (fleet_id);
    CREATE INDEX routes_visit_4b3a3201 ON public.routes_visit USING btree (checkout_observation_id);
    CREATE INDEX routes_visit_8a089c2a ON public.routes_visit USING btree (account_id);
    CREATE INDEX routes_visit_account_id_0e5ab885_idx ON public.routes_visit USING btree (account_id, checkout_time);
    CREATE INDEX routes_visit_account_id_c100489d_idx ON public.routes_visit USING btree (account_id, reference);
    CREATE INDEX routes_visit_account_title_d6ccd1_idx ON public.routes_visit USING btree (account_id, title);
    CREATE INDEX routes_visit_b4347999 ON public.routes_visit USING btree (route_id);
    CREATE INDEX routes_visit_id_c630a799_idx ON public.routes_visit USING btree (id, account_id);
    CREATE INDEX routes_visit_planned_account ON public.routes_visit USING btree (account_id, planned_date);
    CREATE INDEX routes_visit_planned_date_f5e621f3_uniq ON public.routes_visit USING btree (planned_date);
    CREATE INDEX routes_visit_route_id_83fd01a0_idx ON public.routes_visit USING btree (route_id, status);
    CREATE INDEX routes_visit_tracking_id_e7a335ca_idx ON public.routes_visit USING btree (tracking_id);


    -- public.routes_visit foreign keys

    ALTER TABLE public.routes_visit ADD CONSTRAINT route_checkout_observation_id_a902f1b5_fk_routes_observation_id FOREIGN KEY (checkout_observation_id) REFERENCES public.routes_observation(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_visit ADD CONSTRAINT routes_visit_account_id_68079d0b_fk_accounts_account_id FOREIGN KEY (account_id) REFERENCES public.accounts_account(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_visit ADD CONSTRAINT routes_visit_fleet_id_54ce5be0_fk_fleets_fleets_id FOREIGN KEY (fleet_id) REFERENCES public.fleets_fleets(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_visit ADD CONSTRAINT routes_visit_route_id_686427be_fk_routes_route_id FOREIGN KEY (route_id) REFERENCES public.routes_route(id) DEFERRABLE INITIALLY DEFERRED;
    ALTER TABLE public.routes_visit ADD CONSTRAINT routes_visit_visit_type_id_e463401d_fk_accounts_visittype_id FOREIGN KEY (visit_type_id) REFERENCES public.accounts_visittype(id) DEFERRABLE INITIALLY DEFERRED;"""

ddl_account = """
CREATE TABLE public.accounts_account (
	id serial4 NOT NULL,
	created timestamptz NOT NULL,
	modified timestamptz NOT NULL,
	status varchar(100) NOT NULL,
	status_changed timestamptz NOT NULL,
	stripe_customer_id varchar(254) NOT NULL,
	"name" varchar(254) NOT NULL,
	active_until timestamptz NOT NULL,
	card_last4 varchar(4) NOT NULL,
	plan_quantity int4 NOT NULL,
	stripe_subscription_id varchar(254) NOT NULL,
	old_id int4 NULL,
	country varchar(2) NULL,
	card_brand varchar(254) NULL,
	exp_month int4 NULL,
	exp_year int4 NULL,
	funding varchar(254) NULL,
	coupon varchar(254) NULL,
	timezone varchar(100) NULL,
	vehicle_quantity varchar(254) NULL,
	logo varchar(254) NOT NULL,
	module_interest varchar(254) NULL,
	utm varchar(1024) NULL,
	sso_domain varchar(1024) NULL,
	sso_scheme varchar(5) DEFAULT ''::character varying NOT NULL,
	geocoder_quality_level int4 NULL,
	mrr float8 NULL,
	parent_id int4 NULL,
	tin varchar(30) NULL,
	piriod_subscription_id varchar(30) NULL,
	organization_id int4 NULL,
	CONSTRAINT accounts_account_pkey PRIMARY KEY (id),
	CONSTRAINT accounts_account_stripe_customer_id_cacce7a4_uniq UNIQUE (stripe_customer_id)
);
CREATE INDEX accounts_account_26b2345e ON public.accounts_account USING btree (organization_id);
CREATE INDEX accounts_account_stripe_customer_id_cacce7a4_like ON public.accounts_account USING btree (stripe_customer_id varchar_pattern_ops);


-- public.accounts_account foreign keys

ALTER TABLE public.accounts_account ADD CONSTRAINT accounts_a_organization_id_54f21554_fk_accounts_organization_id FOREIGN KEY (organization_id) REFERENCES public.accounts_organization(id) DEFERRABLE INITIALLY DEFERRED;
"""

ddl_account_user = """
CREATE TABLE public.accounts_user (
	id serial4 NOT NULL,
	"password" varchar(128) NOT NULL,
	last_login timestamptz NULL,
	email varchar(254) NULL,
	"name" varchar(254) NOT NULL,
	is_staff bool NOT NULL,
	created timestamptz NOT NULL,
	modified timestamptz NOT NULL,
	account_id int4 NOT NULL,
	username varchar(254) NOT NULL,
	is_owner bool NOT NULL,
	old_id int4 NULL,
	is_admin bool NOT NULL,
	is_driver bool NOT NULL,
	phone varchar(128) NOT NULL,
	app_version text NOT NULL,
	is_monitor bool NOT NULL,
	is_coordinator bool NOT NULL,
	is_router bool NOT NULL,
	is_router_jr bool NOT NULL,
	last_logout timestamptz NULL,
	is_codriver bool DEFAULT false NOT NULL,
	organization_id int4 NULL,
	failed_login int4 NOT NULL,
	last_mobile_activity timestamptz NULL,
	status varchar(100) NOT NULL,
	status_changed timestamptz NOT NULL,
	is_seller_viewer bool NOT NULL,
	CONSTRAINT accounts_user_pkey PRIMARY KEY (id),
	CONSTRAINT accounts_user_username_key UNIQUE (username)
);
CREATE INDEX accounts_user_26b2345e ON public.accounts_user USING btree (organization_id);
CREATE INDEX accounts_user_8a089c2a ON public.accounts_user USING btree (account_id);
CREATE INDEX accounts_user_account_id_5a730369_idx ON public.accounts_user USING btree (account_id, is_owner);
CREATE INDEX accounts_user_account_id_84a736b0_idx ON public.accounts_user USING btree (account_id, is_admin);
CREATE INDEX accounts_user_account_id_a92d74d0_idx ON public.accounts_user USING btree (account_id, is_monitor);
CREATE INDEX accounts_user_account_id_d716253e_idx ON public.accounts_user USING btree (account_id, is_driver);
CREATE INDEX accounts_user_email_70e5d3371c73dba5_like ON public.accounts_user USING btree (email varchar_pattern_ops);
"""
