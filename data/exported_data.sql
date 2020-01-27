--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(150) NOT NULL
);


ALTER TABLE auth_group OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_id_seq OWNER TO postgres;

--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_group_permissions OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_group_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_group_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE auth_permission OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_permission_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_permission_id_seq OWNER TO postgres;

--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    password character varying(128) NOT NULL,
    last_login timestamp with time zone,
    is_superuser boolean NOT NULL,
    username character varying(150) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(150) NOT NULL,
    email character varying(254) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


ALTER TABLE auth_user OWNER TO postgres;

--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE auth_user_groups OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_groups_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_groups_id_seq OWNER TO postgres;

--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_id_seq OWNER TO postgres;

--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE auth_user_user_permissions OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE auth_user_user_permissions_id_seq OWNER TO postgres;

--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: authtoken_token; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE authtoken_token (
    key character varying(40) NOT NULL,
    created timestamp with time zone NOT NULL,
    user_id integer NOT NULL
);


ALTER TABLE authtoken_token OWNER TO postgres;

--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    content_type_id integer,
    user_id integer NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


ALTER TABLE django_admin_log OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_admin_log_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_admin_log_id_seq OWNER TO postgres;

--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE django_content_type OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_content_type_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_content_type_id_seq OWNER TO postgres;

--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE django_session OWNER TO postgres;

--
-- Name: locations_location; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_location (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    "pigletsGroupCell_id" integer,
    section_id integer,
    "sowAndPigletsCell_id" integer,
    "sowGroupCell_id" integer,
    "sowSingleCell_id" integer,
    workshop_id integer
);


ALTER TABLE locations_location OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_location_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_location_id_seq OWNER TO postgres;

--
-- Name: locations_location_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_location_id_seq OWNED BY locations_location.id;


--
-- Name: locations_pigletsgroupcell; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_pigletsgroupcell (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    number character varying(4) NOT NULL,
    section_id integer NOT NULL,
    workshop_id integer NOT NULL
);


ALTER TABLE locations_pigletsgroupcell OWNER TO postgres;

--
-- Name: locations_pigletsgroupcell_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_pigletsgroupcell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_pigletsgroupcell_id_seq OWNER TO postgres;

--
-- Name: locations_pigletsgroupcell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_pigletsgroupcell_id_seq OWNED BY locations_pigletsgroupcell.id;


--
-- Name: locations_section; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_section (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    name character varying(20) NOT NULL,
    number integer NOT NULL,
    workshop_id integer NOT NULL
);


ALTER TABLE locations_section OWNER TO postgres;

--
-- Name: locations_section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_section_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_section_id_seq OWNER TO postgres;

--
-- Name: locations_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_section_id_seq OWNED BY locations_section.id;


--
-- Name: locations_sowandpigletscell; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_sowandpigletscell (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    number character varying(4) NOT NULL,
    section_id integer NOT NULL,
    workshop_id integer NOT NULL
);


ALTER TABLE locations_sowandpigletscell OWNER TO postgres;

--
-- Name: locations_sowandpigletscell_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_sowandpigletscell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_sowandpigletscell_id_seq OWNER TO postgres;

--
-- Name: locations_sowandpigletscell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_sowandpigletscell_id_seq OWNED BY locations_sowandpigletscell.id;


--
-- Name: locations_sowgroupcell; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_sowgroupcell (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    number character varying(4) NOT NULL,
    sows_quantity integer NOT NULL,
    section_id integer NOT NULL,
    workshop_id integer NOT NULL
);


ALTER TABLE locations_sowgroupcell OWNER TO postgres;

--
-- Name: locations_sowgroupcell_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_sowgroupcell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_sowgroupcell_id_seq OWNER TO postgres;

--
-- Name: locations_sowgroupcell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_sowgroupcell_id_seq OWNED BY locations_sowgroupcell.id;


--
-- Name: locations_sowgroupcell_sows; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_sowgroupcell_sows (
    id integer NOT NULL,
    sowgroupcell_id integer NOT NULL,
    sow_id integer NOT NULL
);


ALTER TABLE locations_sowgroupcell_sows OWNER TO postgres;

--
-- Name: locations_sowgroupcell_sows_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_sowgroupcell_sows_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_sowgroupcell_sows_id_seq OWNER TO postgres;

--
-- Name: locations_sowgroupcell_sows_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_sowgroupcell_sows_id_seq OWNED BY locations_sowgroupcell_sows.id;


--
-- Name: locations_sowsinglecell; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_sowsinglecell (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    number character varying(4) NOT NULL,
    section_id integer NOT NULL,
    workshop_id integer NOT NULL
);


ALTER TABLE locations_sowsinglecell OWNER TO postgres;

--
-- Name: locations_sowsinglecell_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_sowsinglecell_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_sowsinglecell_id_seq OWNER TO postgres;

--
-- Name: locations_sowsinglecell_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_sowsinglecell_id_seq OWNED BY locations_sowsinglecell.id;


--
-- Name: locations_workshop; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE locations_workshop (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    number integer NOT NULL,
    title character varying(128) NOT NULL
);


ALTER TABLE locations_workshop OWNER TO postgres;

--
-- Name: locations_workshop_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE locations_workshop_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE locations_workshop_id_seq OWNER TO postgres;

--
-- Name: locations_workshop_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE locations_workshop_id_seq OWNED BY locations_workshop.id;


--
-- Name: piglets_events_cullingpiglets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_cullingpiglets (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    culling_type character varying(50) NOT NULL,
    reason character varying(200),
    is_it_gilt boolean NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_cullingpiglets OWNER TO postgres;

--
-- Name: piglets_events_cullingpiglets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_cullingpiglets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_cullingpiglets_id_seq OWNER TO postgres;

--
-- Name: piglets_events_cullingpiglets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_cullingpiglets_id_seq OWNED BY piglets_events_cullingpiglets.id;


--
-- Name: piglets_events_pigletsmerger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_pigletsmerger (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    created_piglets_id integer,
    initiator_id integer
);


ALTER TABLE piglets_events_pigletsmerger OWNER TO postgres;

--
-- Name: piglets_events_pigletsmerger_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_pigletsmerger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_pigletsmerger_id_seq OWNER TO postgres;

--
-- Name: piglets_events_pigletsmerger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_pigletsmerger_id_seq OWNED BY piglets_events_pigletsmerger.id;


--
-- Name: piglets_events_pigletssplit; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_pigletssplit (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer,
    parent_piglets_id integer
);


ALTER TABLE piglets_events_pigletssplit OWNER TO postgres;

--
-- Name: piglets_events_pigletssplit_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_pigletssplit_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_pigletssplit_id_seq OWNER TO postgres;

--
-- Name: piglets_events_pigletssplit_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_pigletssplit_id_seq OWNED BY piglets_events_pigletssplit.id;


--
-- Name: piglets_events_weighingpiglets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_weighingpiglets (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    total_weight double precision NOT NULL,
    average_weight double precision NOT NULL,
    piglets_quantity integer NOT NULL,
    place character varying(10) NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_weighingpiglets OWNER TO postgres;

--
-- Name: piglets_events_weighingpiglets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_weighingpiglets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_weighingpiglets_id_seq OWNER TO postgres;

--
-- Name: piglets_events_weighingpiglets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_weighingpiglets_id_seq OWNED BY piglets_events_weighingpiglets.id;


--
-- Name: piglets_piglets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_piglets (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    start_quantity integer NOT NULL,
    quantity integer NOT NULL,
    gilts_quantity integer NOT NULL,
    transfer_part_number integer,
    active boolean NOT NULL,
    location_id integer,
    merger_as_parent_id integer,
    split_as_child_id integer,
    status_id integer
);


ALTER TABLE piglets_piglets OWNER TO postgres;

--
-- Name: piglets_piglets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_piglets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_piglets_id_seq OWNER TO postgres;

--
-- Name: piglets_piglets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_piglets_id_seq OWNED BY piglets_piglets.id;


--
-- Name: piglets_pigletsstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_pigletsstatus (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    title character varying(100) NOT NULL
);


ALTER TABLE piglets_pigletsstatus OWNER TO postgres;

--
-- Name: piglets_pigletsstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_pigletsstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_pigletsstatus_id_seq OWNER TO postgres;

--
-- Name: piglets_pigletsstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_pigletsstatus_id_seq OWNED BY piglets_pigletsstatus.id;


--
-- Name: sows_boar; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_boar (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    birth_id character varying(10),
    location_id integer
);


ALTER TABLE sows_boar OWNER TO postgres;

--
-- Name: sows_boar_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_boar_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_boar_id_seq OWNER TO postgres;

--
-- Name: sows_boar_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_boar_id_seq OWNED BY sows_boar.id;


--
-- Name: sows_events_abortionsow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_abortionsow (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer,
    sow_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE sows_events_abortionsow OWNER TO postgres;

--
-- Name: sows_events_abortionsow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_abortionsow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_abortionsow_id_seq OWNER TO postgres;

--
-- Name: sows_events_abortionsow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_abortionsow_id_seq OWNED BY sows_events_abortionsow.id;


--
-- Name: sows_events_cullingsow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_cullingsow (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    culling_type character varying(50) NOT NULL,
    reason character varying(300),
    initiator_id integer,
    sow_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE sows_events_cullingsow OWNER TO postgres;

--
-- Name: sows_events_cullingsow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_cullingsow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_cullingsow_id_seq OWNER TO postgres;

--
-- Name: sows_events_cullingsow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_cullingsow_id_seq OWNED BY sows_events_cullingsow.id;


--
-- Name: sows_events_semination; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_semination (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    boar_id integer,
    initiator_id integer,
    semination_employee_id integer,
    sow_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE sows_events_semination OWNER TO postgres;

--
-- Name: sows_events_semination_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_semination_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_semination_id_seq OWNER TO postgres;

--
-- Name: sows_events_semination_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_semination_id_seq OWNED BY sows_events_semination.id;


--
-- Name: sows_events_sowfarrow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_sowfarrow (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    alive_quantity integer NOT NULL,
    dead_quantity integer NOT NULL,
    mummy_quantity integer NOT NULL,
    initiator_id integer,
    piglets_group_id integer,
    sow_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE sows_events_sowfarrow OWNER TO postgres;

--
-- Name: sows_events_sowfarrow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_sowfarrow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_sowfarrow_id_seq OWNER TO postgres;

--
-- Name: sows_events_sowfarrow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_sowfarrow_id_seq OWNED BY sows_events_sowfarrow.id;


--
-- Name: sows_events_ultrasound; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_ultrasound (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    result boolean NOT NULL,
    initiator_id integer,
    sow_id integer NOT NULL,
    tour_id integer,
    u_type_id integer
);


ALTER TABLE sows_events_ultrasound OWNER TO postgres;

--
-- Name: sows_events_ultrasound_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_ultrasound_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_ultrasound_id_seq OWNER TO postgres;

--
-- Name: sows_events_ultrasound_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_ultrasound_id_seq OWNED BY sows_events_ultrasound.id;


--
-- Name: sows_events_ultrasoundtype; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_ultrasoundtype (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    title character varying(100),
    days integer NOT NULL,
    final boolean NOT NULL
);


ALTER TABLE sows_events_ultrasoundtype OWNER TO postgres;

--
-- Name: sows_events_ultrasoundtype_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_ultrasoundtype_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_ultrasoundtype_id_seq OWNER TO postgres;

--
-- Name: sows_events_ultrasoundtype_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_ultrasoundtype_id_seq OWNED BY sows_events_ultrasoundtype.id;


--
-- Name: sows_events_weaningsow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_events_weaningsow (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    quantity integer NOT NULL,
    initiator_id integer,
    piglets_id integer,
    sow_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE sows_events_weaningsow OWNER TO postgres;

--
-- Name: sows_events_weaningsow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_events_weaningsow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_events_weaningsow_id_seq OWNER TO postgres;

--
-- Name: sows_events_weaningsow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_events_weaningsow_id_seq OWNED BY sows_events_weaningsow.id;


--
-- Name: sows_gilt; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_gilt (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    birth_id character varying(10),
    farrow_id integer,
    location_id integer,
    mother_sow_id integer,
    tour_id integer
);


ALTER TABLE sows_gilt OWNER TO postgres;

--
-- Name: sows_gilt_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_gilt_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_gilt_id_seq OWNER TO postgres;

--
-- Name: sows_gilt_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_gilt_id_seq OWNED BY sows_gilt.id;


--
-- Name: sows_sow; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_sow (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    birth_id character varying(10),
    farm_id integer,
    alive boolean NOT NULL,
    location_id integer,
    status_id integer,
    tour_id integer
);


ALTER TABLE sows_sow OWNER TO postgres;

--
-- Name: sows_sow_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_sow_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_sow_id_seq OWNER TO postgres;

--
-- Name: sows_sow_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_sow_id_seq OWNED BY sows_sow.id;


--
-- Name: sows_sowstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_sowstatus (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    title character varying(100) NOT NULL
);


ALTER TABLE sows_sowstatus OWNER TO postgres;

--
-- Name: sows_sowstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_sowstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_sowstatus_id_seq OWNER TO postgres;

--
-- Name: sows_sowstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_sowstatus_id_seq OWNED BY sows_sowstatus.id;


--
-- Name: staff_workshopemployee; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE staff_workshopemployee (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    farm_name character varying(20) NOT NULL,
    is_officer boolean NOT NULL,
    is_seminator boolean NOT NULL,
    user_id integer NOT NULL,
    workshop_id integer
);


ALTER TABLE staff_workshopemployee OWNER TO postgres;

--
-- Name: staff_workshopemployee_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE staff_workshopemployee_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE staff_workshopemployee_id_seq OWNER TO postgres;

--
-- Name: staff_workshopemployee_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE staff_workshopemployee_id_seq OWNED BY staff_workshopemployee.id;


--
-- Name: tours_metatour; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tours_metatour (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    piglets_id integer NOT NULL
);


ALTER TABLE tours_metatour OWNER TO postgres;

--
-- Name: tours_metatour_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tours_metatour_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tours_metatour_id_seq OWNER TO postgres;

--
-- Name: tours_metatour_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tours_metatour_id_seq OWNED BY tours_metatour.id;


--
-- Name: tours_metatourrecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tours_metatourrecord (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    percentage double precision NOT NULL,
    metatour_id integer NOT NULL,
    tour_id integer NOT NULL
);


ALTER TABLE tours_metatourrecord OWNER TO postgres;

--
-- Name: tours_metatourrecord_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tours_metatourrecord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tours_metatourrecord_id_seq OWNER TO postgres;

--
-- Name: tours_metatourrecord_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tours_metatourrecord_id_seq OWNED BY tours_metatourrecord.id;


--
-- Name: tours_tour; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE tours_tour (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    start_date timestamp with time zone NOT NULL,
    week_number integer NOT NULL,
    year integer NOT NULL
);


ALTER TABLE tours_tour OWNER TO postgres;

--
-- Name: tours_tour_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE tours_tour_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE tours_tour_id_seq OWNER TO postgres;

--
-- Name: tours_tour_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE tours_tour_id_seq OWNED BY tours_tour.id;


--
-- Name: transactions_pigletstransaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE transactions_pigletstransaction (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    from_location_id integer NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL,
    to_location_id integer NOT NULL
);


ALTER TABLE transactions_pigletstransaction OWNER TO postgres;

--
-- Name: transactions_pigletstransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE transactions_pigletstransaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transactions_pigletstransaction_id_seq OWNER TO postgres;

--
-- Name: transactions_pigletstransaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE transactions_pigletstransaction_id_seq OWNED BY transactions_pigletstransaction.id;


--
-- Name: transactions_sowtransaction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE transactions_sowtransaction (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    from_location_id integer NOT NULL,
    initiator_id integer,
    sow_id integer NOT NULL,
    to_location_id integer NOT NULL
);


ALTER TABLE transactions_sowtransaction OWNER TO postgres;

--
-- Name: transactions_sowtransaction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE transactions_sowtransaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE transactions_sowtransaction_id_seq OWNER TO postgres;

--
-- Name: transactions_sowtransaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE transactions_sowtransaction_id_seq OWNED BY transactions_sowtransaction.id;


--
-- Name: auth_group id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: auth_group_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: auth_permission id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: auth_user id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: auth_user_groups id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: auth_user_user_permissions id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: django_admin_log id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: django_content_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: django_migrations id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: locations_location id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location ALTER COLUMN id SET DEFAULT nextval('locations_location_id_seq'::regclass);


--
-- Name: locations_pigletsgroupcell id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_pigletsgroupcell ALTER COLUMN id SET DEFAULT nextval('locations_pigletsgroupcell_id_seq'::regclass);


--
-- Name: locations_section id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_section ALTER COLUMN id SET DEFAULT nextval('locations_section_id_seq'::regclass);


--
-- Name: locations_sowandpigletscell id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowandpigletscell ALTER COLUMN id SET DEFAULT nextval('locations_sowandpigletscell_id_seq'::regclass);


--
-- Name: locations_sowgroupcell id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell ALTER COLUMN id SET DEFAULT nextval('locations_sowgroupcell_id_seq'::regclass);


--
-- Name: locations_sowgroupcell_sows id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell_sows ALTER COLUMN id SET DEFAULT nextval('locations_sowgroupcell_sows_id_seq'::regclass);


--
-- Name: locations_sowsinglecell id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowsinglecell ALTER COLUMN id SET DEFAULT nextval('locations_sowsinglecell_id_seq'::regclass);


--
-- Name: locations_workshop id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_workshop ALTER COLUMN id SET DEFAULT nextval('locations_workshop_id_seq'::regclass);


--
-- Name: piglets_events_cullingpiglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingpiglets ALTER COLUMN id SET DEFAULT nextval('piglets_events_cullingpiglets_id_seq'::regclass);


--
-- Name: piglets_events_pigletsmerger id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletsmerger ALTER COLUMN id SET DEFAULT nextval('piglets_events_pigletsmerger_id_seq'::regclass);


--
-- Name: piglets_events_pigletssplit id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletssplit ALTER COLUMN id SET DEFAULT nextval('piglets_events_pigletssplit_id_seq'::regclass);


--
-- Name: piglets_events_weighingpiglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets ALTER COLUMN id SET DEFAULT nextval('piglets_events_weighingpiglets_id_seq'::regclass);


--
-- Name: piglets_piglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets ALTER COLUMN id SET DEFAULT nextval('piglets_piglets_id_seq'::regclass);


--
-- Name: piglets_pigletsstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_pigletsstatus ALTER COLUMN id SET DEFAULT nextval('piglets_pigletsstatus_id_seq'::regclass);


--
-- Name: sows_boar id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_boar ALTER COLUMN id SET DEFAULT nextval('sows_boar_id_seq'::regclass);


--
-- Name: sows_events_abortionsow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_abortionsow ALTER COLUMN id SET DEFAULT nextval('sows_events_abortionsow_id_seq'::regclass);


--
-- Name: sows_events_cullingsow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_cullingsow ALTER COLUMN id SET DEFAULT nextval('sows_events_cullingsow_id_seq'::regclass);


--
-- Name: sows_events_semination id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination ALTER COLUMN id SET DEFAULT nextval('sows_events_semination_id_seq'::regclass);


--
-- Name: sows_events_sowfarrow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow ALTER COLUMN id SET DEFAULT nextval('sows_events_sowfarrow_id_seq'::regclass);


--
-- Name: sows_events_ultrasound id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound ALTER COLUMN id SET DEFAULT nextval('sows_events_ultrasound_id_seq'::regclass);


--
-- Name: sows_events_ultrasoundtype id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasoundtype ALTER COLUMN id SET DEFAULT nextval('sows_events_ultrasoundtype_id_seq'::regclass);


--
-- Name: sows_events_weaningsow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow ALTER COLUMN id SET DEFAULT nextval('sows_events_weaningsow_id_seq'::regclass);


--
-- Name: sows_gilt id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt ALTER COLUMN id SET DEFAULT nextval('sows_gilt_id_seq'::regclass);


--
-- Name: sows_sow id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow ALTER COLUMN id SET DEFAULT nextval('sows_sow_id_seq'::regclass);


--
-- Name: sows_sowstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sowstatus ALTER COLUMN id SET DEFAULT nextval('sows_sowstatus_id_seq'::regclass);


--
-- Name: staff_workshopemployee id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY staff_workshopemployee ALTER COLUMN id SET DEFAULT nextval('staff_workshopemployee_id_seq'::regclass);


--
-- Name: tours_metatour id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatour ALTER COLUMN id SET DEFAULT nextval('tours_metatour_id_seq'::regclass);


--
-- Name: tours_metatourrecord id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatourrecord ALTER COLUMN id SET DEFAULT nextval('tours_metatourrecord_id_seq'::regclass);


--
-- Name: tours_tour id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_tour ALTER COLUMN id SET DEFAULT nextval('tours_tour_id_seq'::regclass);


--
-- Name: transactions_pigletstransaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction ALTER COLUMN id SET DEFAULT nextval('transactions_pigletstransaction_id_seq'::regclass);


--
-- Name: transactions_sowtransaction id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction ALTER COLUMN id SET DEFAULT nextval('transactions_sowtransaction_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add log entry	1	add_logentry
2	Can change log entry	1	change_logentry
3	Can delete log entry	1	delete_logentry
4	Can view log entry	1	view_logentry
5	Can add permission	2	add_permission
6	Can change permission	2	change_permission
7	Can delete permission	2	delete_permission
8	Can view permission	2	view_permission
9	Can add group	3	add_group
10	Can change group	3	change_group
11	Can delete group	3	delete_group
12	Can view group	3	view_group
13	Can add user	4	add_user
14	Can change user	4	change_user
15	Can delete user	4	delete_user
16	Can view user	4	view_user
17	Can add content type	5	add_contenttype
18	Can change content type	5	change_contenttype
19	Can delete content type	5	delete_contenttype
20	Can view content type	5	view_contenttype
21	Can add session	6	add_session
22	Can change session	6	change_session
23	Can delete session	6	delete_session
24	Can view session	6	view_session
25	Can add location	7	add_location
26	Can change location	7	change_location
27	Can delete location	7	delete_location
28	Can view location	7	view_location
29	Can add piglets group cell	8	add_pigletsgroupcell
30	Can change piglets group cell	8	change_pigletsgroupcell
31	Can delete piglets group cell	8	delete_pigletsgroupcell
32	Can view piglets group cell	8	view_pigletsgroupcell
33	Can add section	9	add_section
34	Can change section	9	change_section
35	Can delete section	9	delete_section
36	Can view section	9	view_section
37	Can add sow and piglets cell	10	add_sowandpigletscell
38	Can change sow and piglets cell	10	change_sowandpigletscell
39	Can delete sow and piglets cell	10	delete_sowandpigletscell
40	Can view sow and piglets cell	10	view_sowandpigletscell
41	Can add work shop	11	add_workshop
42	Can change work shop	11	change_workshop
43	Can delete work shop	11	delete_workshop
44	Can view work shop	11	view_workshop
45	Can add sow single cell	12	add_sowsinglecell
46	Can change sow single cell	12	change_sowsinglecell
47	Can delete sow single cell	12	delete_sowsinglecell
48	Can view sow single cell	12	view_sowsinglecell
49	Can add sow group cell	13	add_sowgroupcell
50	Can change sow group cell	13	change_sowgroupcell
51	Can delete sow group cell	13	delete_sowgroupcell
52	Can view sow group cell	13	view_sowgroupcell
53	Can add boar	14	add_boar
54	Can change boar	14	change_boar
55	Can delete boar	14	delete_boar
56	Can view boar	14	view_boar
57	Can add gilt	15	add_gilt
58	Can change gilt	15	change_gilt
59	Can delete gilt	15	delete_gilt
60	Can view gilt	15	view_gilt
61	Can add sow status	16	add_sowstatus
62	Can change sow status	16	change_sowstatus
63	Can delete sow status	16	delete_sowstatus
64	Can view sow status	16	view_sowstatus
65	Can add sow	17	add_sow
66	Can change sow	17	change_sow
67	Can delete sow	17	delete_sow
68	Can view sow	17	view_sow
69	Can add piglets status	18	add_pigletsstatus
70	Can change piglets status	18	change_pigletsstatus
71	Can delete piglets status	18	delete_pigletsstatus
72	Can view piglets status	18	view_pigletsstatus
73	Can add piglets	19	add_piglets
74	Can change piglets	19	change_piglets
75	Can delete piglets	19	delete_piglets
76	Can view piglets	19	view_piglets
77	Can add ultrasound type	20	add_ultrasoundtype
78	Can change ultrasound type	20	change_ultrasoundtype
79	Can delete ultrasound type	20	delete_ultrasoundtype
80	Can view ultrasound type	20	view_ultrasoundtype
81	Can add weaning sow	21	add_weaningsow
82	Can change weaning sow	21	change_weaningsow
83	Can delete weaning sow	21	delete_weaningsow
84	Can view weaning sow	21	view_weaningsow
85	Can add ultrasound	22	add_ultrasound
86	Can change ultrasound	22	change_ultrasound
87	Can delete ultrasound	22	delete_ultrasound
88	Can view ultrasound	22	view_ultrasound
89	Can add sow farrow	23	add_sowfarrow
90	Can change sow farrow	23	change_sowfarrow
91	Can delete sow farrow	23	delete_sowfarrow
92	Can view sow farrow	23	view_sowfarrow
93	Can add semination	24	add_semination
94	Can change semination	24	change_semination
95	Can delete semination	24	delete_semination
96	Can view semination	24	view_semination
97	Can add culling sow	25	add_cullingsow
98	Can change culling sow	25	change_cullingsow
99	Can delete culling sow	25	delete_cullingsow
100	Can view culling sow	25	view_cullingsow
101	Can add abortion sow	26	add_abortionsow
102	Can change abortion sow	26	change_abortionsow
103	Can delete abortion sow	26	delete_abortionsow
104	Can view abortion sow	26	view_abortionsow
105	Can add weighing piglets	27	add_weighingpiglets
106	Can change weighing piglets	27	change_weighingpiglets
107	Can delete weighing piglets	27	delete_weighingpiglets
108	Can view weighing piglets	27	view_weighingpiglets
109	Can add piglets split	28	add_pigletssplit
110	Can change piglets split	28	change_pigletssplit
111	Can delete piglets split	28	delete_pigletssplit
112	Can view piglets split	28	view_pigletssplit
113	Can add piglets merger	29	add_pigletsmerger
114	Can change piglets merger	29	change_pigletsmerger
115	Can delete piglets merger	29	delete_pigletsmerger
116	Can view piglets merger	29	view_pigletsmerger
117	Can add culling piglets	30	add_cullingpiglets
118	Can change culling piglets	30	change_cullingpiglets
119	Can delete culling piglets	30	delete_cullingpiglets
120	Can view culling piglets	30	view_cullingpiglets
121	Can add sow transaction	31	add_sowtransaction
122	Can change sow transaction	31	change_sowtransaction
123	Can delete sow transaction	31	delete_sowtransaction
124	Can view sow transaction	31	view_sowtransaction
125	Can add piglets transaction	32	add_pigletstransaction
126	Can change piglets transaction	32	change_pigletstransaction
127	Can delete piglets transaction	32	delete_pigletstransaction
128	Can view piglets transaction	32	view_pigletstransaction
129	Can add meta tour	33	add_metatour
130	Can change meta tour	33	change_metatour
131	Can delete meta tour	33	delete_metatour
132	Can view meta tour	33	view_metatour
133	Can add tour	34	add_tour
134	Can change tour	34	change_tour
135	Can delete tour	34	delete_tour
136	Can view tour	34	view_tour
137	Can add meta tour record	35	add_metatourrecord
138	Can change meta tour record	35	change_metatourrecord
139	Can delete meta tour record	35	delete_metatourrecord
140	Can view meta tour record	35	view_metatourrecord
141	Can add work shop employee	36	add_workshopemployee
142	Can change work shop employee	36	change_workshopemployee
143	Can delete work shop employee	36	delete_workshopemployee
144	Can view work shop employee	36	view_workshopemployee
145	Can add Token	37	add_token
146	Can change Token	37	change_token
147	Can delete Token	37	delete_token
148	Can view Token	37	view_token
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$180000$jUl4AfSyYYy7$9zvkA0XmfaQof9cE/DtesjAfKwUVLWwxEW+EIpwIPZo=	\N	t	kaizerj			kzrster@gmail.com	t	t	2020-01-24 04:41:23.608956+00
2	pbkdf2_sha256$180000$zRgGmon0hOoW$HxC/ti/4LXASixxdu3NPukcDkTXCtVyGuCjzkkbHXSw=	\N	f	test_admin			t@t.ru	f	t	2020-01-24 04:41:23.781719+00
3	pbkdf2_sha256$180000$zUqYqJBG4vCH$oNtix3d08SoVdK3DDNib+M2h6IYKzj5JKBYmEbBu97o=	\N	f	test_officer			t@t.ru	f	t	2020-01-24 04:41:23.938849+00
4	pbkdf2_sha256$180000$tZugr14yvrNT$wVkyM9mi7UpttSsL7WyrPYhP/X15fejrvfTf7wV+3nc=	\N	f	shmigina			t@t.ru	f	t	2020-01-24 04:41:24.092875+00
5	pbkdf2_sha256$180000$DklY8F7OAa1A$y/Dzt8ZLBLQAAveOXtMxYWuVNwdHpBhwfNR2l8FzNzU=	\N	f	borisov			t@t.ru	f	t	2020-01-24 04:41:24.246455+00
6	pbkdf2_sha256$180000$HOfxzSbWdz48$eHZe4KY9gsbxdAL0JuoOJp+qrCR0g+XGHQ9k38oop1g=	\N	f	semenova			t@t.ru	f	t	2020-01-24 04:41:24.402652+00
7	pbkdf2_sha256$180000$HZIM0D7bMwRp$o+RjIogw85eh+hGxH0PirvVhkHmM8LgjMdnsLTTLHKg=	\N	f	gary			t@t.ru	f	t	2020-01-24 04:41:24.561546+00
8	pbkdf2_sha256$180000$OutRbHL5wuC8$hfqIAK3By1iWQkdctk26hrIIOVeaTeqxvYN844K+9e4=	\N	f	ivanov			t@t.ru	f	t	2020-01-24 04:41:24.732572+00
9	pbkdf2_sha256$180000$0NPfT0XuiQjv$RZW/1j36I8wcQAZC2Zx7KAr0p8gl+GiFWhzpPT9dljI=	\N	f	stude			t@t.ru	f	t	2020-01-24 04:41:24.892294+00
10	pbkdf2_sha256$180000$7B8VkgAQ6MuH$ixE5u9JxqMILUs+i+0CpIISeWgGoiF13kD/NofZCKik=	\N	f	brigadir1			t@t.ru	f	t	2020-01-24 04:41:25.163421+00
11	pbkdf2_sha256$180000$fynVSFMXJvoZ$ljd6mEjOUbzkUpPPwy0E88msYGqV/Ras0ojh9oSIf2U=	\N	f	brigadir2			t@t.ru	f	t	2020-01-24 04:41:25.322643+00
12	pbkdf2_sha256$180000$2fESouihvEDK$errOnELJMVgC0vLHCL2w6fdo47D/pokPChWdPimslZk=	\N	f	brigadir3			t@t.ru	f	t	2020-01-24 04:41:25.500316+00
13	pbkdf2_sha256$180000$GygTxzKFTFjE$FbstqGtQR66sxPSqF7NJ5NtEwoTCWez9sORWrnsD4Tw=	\N	f	brigadir4			t@t.ru	f	t	2020-01-24 04:41:25.656453+00
14	pbkdf2_sha256$180000$Ps0qbyYHDw1K$Na+clXfmZNwRUDspkzAJvg/bEhH2N6tWmsYwD3LTQJQ=	\N	f	brigadir5			t@t.ru	f	t	2020-01-24 04:41:25.814379+00
15	pbkdf2_sha256$180000$PpOP3xXArsRZ$ECXiB9JebaKFZhG0XNNEPyG8mOeEDrGYFD/EQc4DCCA=	\N	f	brigadir6			t@t.ru	f	t	2020-01-24 04:41:25.973421+00
16	pbkdf2_sha256$180000$fS32WAsn5Ahj$ogAfUokeuHRnGGtdHvMM7KhKAo6vw+wRYP04eBiPUvE=	\N	f	brigadir7			t@t.ru	f	t	2020-01-24 04:41:26.142654+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: authtoken_token; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY authtoken_token (key, created, user_id) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_admin_log (id, action_time, object_id, object_repr, action_flag, change_message, content_type_id, user_id) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_content_type (id, app_label, model) FROM stdin;
1	admin	logentry
2	auth	permission
3	auth	group
4	auth	user
5	contenttypes	contenttype
6	sessions	session
7	locations	location
8	locations	pigletsgroupcell
9	locations	section
10	locations	sowandpigletscell
11	locations	workshop
12	locations	sowsinglecell
13	locations	sowgroupcell
14	sows	boar
15	sows	gilt
16	sows	sowstatus
17	sows	sow
18	piglets	pigletsstatus
19	piglets	piglets
20	sows_events	ultrasoundtype
21	sows_events	weaningsow
22	sows_events	ultrasound
23	sows_events	sowfarrow
24	sows_events	semination
25	sows_events	cullingsow
26	sows_events	abortionsow
27	piglets_events	weighingpiglets
28	piglets_events	pigletssplit
29	piglets_events	pigletsmerger
30	piglets_events	cullingpiglets
31	transactions	sowtransaction
32	transactions	pigletstransaction
33	tours	metatour
34	tours	tour
35	tours	metatourrecord
36	staff	workshopemployee
37	authtoken	token
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2020-01-24 04:40:59.234105+00
2	auth	0001_initial	2020-01-24 04:40:59.292738+00
3	admin	0001_initial	2020-01-24 04:40:59.388379+00
4	admin	0002_logentry_remove_auto_add	2020-01-24 04:40:59.413557+00
5	admin	0003_logentry_add_action_flag_choices	2020-01-24 04:40:59.463956+00
6	contenttypes	0002_remove_content_type_name	2020-01-24 04:40:59.48537+00
7	auth	0002_alter_permission_name_max_length	2020-01-24 04:40:59.492357+00
8	auth	0003_alter_user_email_max_length	2020-01-24 04:40:59.503451+00
9	auth	0004_alter_user_username_opts	2020-01-24 04:40:59.51413+00
10	auth	0005_alter_user_last_login_null	2020-01-24 04:40:59.527466+00
11	auth	0006_require_contenttypes_0002	2020-01-24 04:40:59.534709+00
12	auth	0007_alter_validators_add_error_messages	2020-01-24 04:40:59.545446+00
13	auth	0008_alter_user_username_max_length	2020-01-24 04:40:59.565045+00
14	auth	0009_alter_user_last_name_max_length	2020-01-24 04:40:59.576289+00
15	auth	0010_alter_group_name_max_length	2020-01-24 04:40:59.586667+00
16	auth	0011_update_proxy_permissions	2020-01-24 04:40:59.596926+00
17	authtoken	0001_initial	2020-01-24 04:40:59.618197+00
18	authtoken	0002_auto_20160226_1747	2020-01-24 04:40:59.659257+00
19	locations	0001_initial	2020-01-24 04:40:59.723983+00
20	piglets	0001_initial	2020-01-24 04:40:59.771953+00
21	tours	0001_initial	2020-01-24 04:40:59.825793+00
22	sows	0001_initial	2020-01-24 04:40:59.88684+00
23	locations	0002_auto_20200124_1240	2020-01-24 04:41:00.189603+00
24	piglets_events	0001_initial	2020-01-24 04:41:00.375357+00
25	piglets	0002_auto_20200124_1240	2020-01-24 04:41:00.505291+00
26	sessions	0001_initial	2020-01-24 04:41:00.53992+00
27	sows_events	0001_initial	2020-01-24 04:41:00.846723+00
28	sows	0002_auto_20200124_1240	2020-01-24 04:41:01.155969+00
29	staff	0001_initial	2020-01-24 04:41:01.250216+00
30	transactions	0001_initial	2020-01-24 04:41:01.362121+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
\.


--
-- Data for Name: locations_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_location (id, created_at, modified_at, "pigletsGroupCell_id", section_id, "sowAndPigletsCell_id", "sowGroupCell_id", "sowSingleCell_id", workshop_id) FROM stdin;
1	2020-01-24 04:41:22.928203+00	2020-01-24 04:41:22.928218+00	\N	\N	\N	\N	\N	1
2	2020-01-24 04:41:22.928285+00	2020-01-24 04:41:22.928292+00	\N	\N	\N	\N	\N	2
3	2020-01-24 04:41:22.928329+00	2020-01-24 04:41:22.928335+00	\N	\N	\N	\N	\N	3
4	2020-01-24 04:41:22.928369+00	2020-01-24 04:41:22.928375+00	\N	\N	\N	\N	\N	4
5	2020-01-24 04:41:22.928408+00	2020-01-24 04:41:22.928414+00	\N	\N	\N	\N	\N	5
6	2020-01-24 04:41:22.928463+00	2020-01-24 04:41:22.928469+00	\N	\N	\N	\N	\N	6
7	2020-01-24 04:41:22.928496+00	2020-01-24 04:41:22.928501+00	\N	\N	\N	\N	\N	7
8	2020-01-24 04:41:22.928521+00	2020-01-24 04:41:22.928526+00	\N	\N	\N	\N	\N	8
9	2020-01-24 04:41:22.928545+00	2020-01-24 04:41:22.92855+00	\N	\N	\N	\N	\N	9
10	2020-01-24 04:41:22.92857+00	2020-01-24 04:41:22.928574+00	\N	\N	\N	\N	\N	10
11	2020-01-24 04:41:22.928594+00	2020-01-24 04:41:22.928599+00	\N	\N	\N	\N	\N	11
12	2020-01-24 04:41:22.945145+00	2020-01-24 04:41:22.945164+00	\N	1	\N	\N	\N	\N
13	2020-01-24 04:41:22.945197+00	2020-01-24 04:41:22.945203+00	\N	2	\N	\N	\N	\N
14	2020-01-24 04:41:22.945224+00	2020-01-24 04:41:22.945229+00	\N	3	\N	\N	\N	\N
15	2020-01-24 04:41:22.962501+00	2020-01-24 04:41:22.962519+00	\N	4	\N	\N	\N	\N
16	2020-01-24 04:41:22.962562+00	2020-01-24 04:41:22.962568+00	\N	5	\N	\N	\N	\N
17	2020-01-24 04:41:22.97716+00	2020-01-24 04:41:22.977178+00	\N	6	\N	\N	\N	\N
18	2020-01-24 04:41:22.977212+00	2020-01-24 04:41:22.977217+00	\N	7	\N	\N	\N	\N
19	2020-01-24 04:41:22.977238+00	2020-01-24 04:41:22.977244+00	\N	8	\N	\N	\N	\N
20	2020-01-24 04:41:22.977263+00	2020-01-24 04:41:22.977268+00	\N	9	\N	\N	\N	\N
21	2020-01-24 04:41:22.977287+00	2020-01-24 04:41:22.977292+00	\N	10	\N	\N	\N	\N
22	2020-01-24 04:41:22.977312+00	2020-01-24 04:41:22.977317+00	\N	11	\N	\N	\N	\N
23	2020-01-24 04:41:22.998532+00	2020-01-24 04:41:22.998552+00	\N	\N	1	\N	\N	\N
24	2020-01-24 04:41:22.998588+00	2020-01-24 04:41:22.998594+00	\N	\N	2	\N	\N	\N
25	2020-01-24 04:41:22.998615+00	2020-01-24 04:41:22.99862+00	\N	\N	3	\N	\N	\N
26	2020-01-24 04:41:22.99864+00	2020-01-24 04:41:22.998645+00	\N	\N	4	\N	\N	\N
27	2020-01-24 04:41:22.998664+00	2020-01-24 04:41:22.998669+00	\N	\N	5	\N	\N	\N
28	2020-01-24 04:41:22.998689+00	2020-01-24 04:41:22.998694+00	\N	\N	6	\N	\N	\N
29	2020-01-24 04:41:22.998714+00	2020-01-24 04:41:22.998718+00	\N	\N	7	\N	\N	\N
30	2020-01-24 04:41:22.998738+00	2020-01-24 04:41:22.998743+00	\N	\N	8	\N	\N	\N
31	2020-01-24 04:41:22.998763+00	2020-01-24 04:41:22.998768+00	\N	\N	9	\N	\N	\N
32	2020-01-24 04:41:22.998788+00	2020-01-24 04:41:22.998793+00	\N	\N	10	\N	\N	\N
33	2020-01-24 04:41:22.998813+00	2020-01-24 04:41:22.998818+00	\N	\N	11	\N	\N	\N
34	2020-01-24 04:41:22.998837+00	2020-01-24 04:41:22.998842+00	\N	\N	12	\N	\N	\N
35	2020-01-24 04:41:22.998862+00	2020-01-24 04:41:22.998866+00	\N	\N	13	\N	\N	\N
36	2020-01-24 04:41:22.998886+00	2020-01-24 04:41:22.998891+00	\N	\N	14	\N	\N	\N
37	2020-01-24 04:41:22.99891+00	2020-01-24 04:41:22.998915+00	\N	\N	15	\N	\N	\N
38	2020-01-24 04:41:22.998934+00	2020-01-24 04:41:22.998939+00	\N	\N	16	\N	\N	\N
39	2020-01-24 04:41:22.998959+00	2020-01-24 04:41:22.998963+00	\N	\N	17	\N	\N	\N
40	2020-01-24 04:41:22.999297+00	2020-01-24 04:41:22.999302+00	\N	\N	18	\N	\N	\N
41	2020-01-24 04:41:22.999322+00	2020-01-24 04:41:22.999327+00	\N	\N	19	\N	\N	\N
42	2020-01-24 04:41:22.999347+00	2020-01-24 04:41:22.999352+00	\N	\N	20	\N	\N	\N
43	2020-01-24 04:41:22.999372+00	2020-01-24 04:41:22.999376+00	\N	\N	21	\N	\N	\N
44	2020-01-24 04:41:22.999396+00	2020-01-24 04:41:22.999401+00	\N	\N	22	\N	\N	\N
45	2020-01-24 04:41:22.99942+00	2020-01-24 04:41:22.999425+00	\N	\N	23	\N	\N	\N
46	2020-01-24 04:41:22.999445+00	2020-01-24 04:41:22.999458+00	\N	\N	24	\N	\N	\N
47	2020-01-24 04:41:22.99948+00	2020-01-24 04:41:22.999485+00	\N	\N	25	\N	\N	\N
48	2020-01-24 04:41:22.999504+00	2020-01-24 04:41:22.999509+00	\N	\N	26	\N	\N	\N
49	2020-01-24 04:41:22.999529+00	2020-01-24 04:41:22.999534+00	\N	\N	27	\N	\N	\N
50	2020-01-24 04:41:22.999553+00	2020-01-24 04:41:22.999569+00	\N	\N	28	\N	\N	\N
51	2020-01-24 04:41:22.99959+00	2020-01-24 04:41:22.999595+00	\N	\N	29	\N	\N	\N
52	2020-01-24 04:41:22.999614+00	2020-01-24 04:41:22.999619+00	\N	\N	30	\N	\N	\N
53	2020-01-24 04:41:22.999639+00	2020-01-24 04:41:22.999644+00	\N	\N	31	\N	\N	\N
54	2020-01-24 04:41:22.999663+00	2020-01-24 04:41:22.999668+00	\N	\N	32	\N	\N	\N
55	2020-01-24 04:41:22.999687+00	2020-01-24 04:41:22.999692+00	\N	\N	33	\N	\N	\N
56	2020-01-24 04:41:22.999712+00	2020-01-24 04:41:22.999717+00	\N	\N	34	\N	\N	\N
57	2020-01-24 04:41:22.999736+00	2020-01-24 04:41:22.999741+00	\N	\N	35	\N	\N	\N
58	2020-01-24 04:41:22.999761+00	2020-01-24 04:41:22.999765+00	\N	\N	36	\N	\N	\N
59	2020-01-24 04:41:22.999792+00	2020-01-24 04:41:22.999799+00	\N	\N	37	\N	\N	\N
60	2020-01-24 04:41:22.99982+00	2020-01-24 04:41:22.999825+00	\N	\N	38	\N	\N	\N
61	2020-01-24 04:41:22.999845+00	2020-01-24 04:41:22.99985+00	\N	\N	39	\N	\N	\N
62	2020-01-24 04:41:22.99987+00	2020-01-24 04:41:22.999875+00	\N	\N	40	\N	\N	\N
63	2020-01-24 04:41:22.999894+00	2020-01-24 04:41:22.999899+00	\N	\N	41	\N	\N	\N
64	2020-01-24 04:41:22.999919+00	2020-01-24 04:41:22.999924+00	\N	\N	42	\N	\N	\N
65	2020-01-24 04:41:22.999943+00	2020-01-24 04:41:22.999948+00	\N	\N	43	\N	\N	\N
66	2020-01-24 04:41:22.999968+00	2020-01-24 04:41:22.999973+00	\N	\N	44	\N	\N	\N
67	2020-01-24 04:41:22.999992+00	2020-01-24 04:41:22.999997+00	\N	\N	45	\N	\N	\N
68	2020-01-24 04:41:23.022462+00	2020-01-24 04:41:23.022481+00	\N	\N	46	\N	\N	\N
69	2020-01-24 04:41:23.022516+00	2020-01-24 04:41:23.022522+00	\N	\N	47	\N	\N	\N
70	2020-01-24 04:41:23.022543+00	2020-01-24 04:41:23.022548+00	\N	\N	48	\N	\N	\N
71	2020-01-24 04:41:23.022568+00	2020-01-24 04:41:23.022573+00	\N	\N	49	\N	\N	\N
72	2020-01-24 04:41:23.022593+00	2020-01-24 04:41:23.022598+00	\N	\N	50	\N	\N	\N
73	2020-01-24 04:41:23.022617+00	2020-01-24 04:41:23.022622+00	\N	\N	51	\N	\N	\N
74	2020-01-24 04:41:23.022642+00	2020-01-24 04:41:23.022647+00	\N	\N	52	\N	\N	\N
75	2020-01-24 04:41:23.022666+00	2020-01-24 04:41:23.022671+00	\N	\N	53	\N	\N	\N
76	2020-01-24 04:41:23.022691+00	2020-01-24 04:41:23.022695+00	\N	\N	54	\N	\N	\N
77	2020-01-24 04:41:23.022715+00	2020-01-24 04:41:23.02272+00	\N	\N	55	\N	\N	\N
78	2020-01-24 04:41:23.022739+00	2020-01-24 04:41:23.022744+00	\N	\N	56	\N	\N	\N
79	2020-01-24 04:41:23.022763+00	2020-01-24 04:41:23.022768+00	\N	\N	57	\N	\N	\N
80	2020-01-24 04:41:23.022787+00	2020-01-24 04:41:23.022792+00	\N	\N	58	\N	\N	\N
81	2020-01-24 04:41:23.022811+00	2020-01-24 04:41:23.022816+00	\N	\N	59	\N	\N	\N
82	2020-01-24 04:41:23.022835+00	2020-01-24 04:41:23.022851+00	\N	\N	60	\N	\N	\N
83	2020-01-24 04:41:23.022873+00	2020-01-24 04:41:23.022878+00	\N	\N	61	\N	\N	\N
84	2020-01-24 04:41:23.022897+00	2020-01-24 04:41:23.022902+00	\N	\N	62	\N	\N	\N
85	2020-01-24 04:41:23.022921+00	2020-01-24 04:41:23.022926+00	\N	\N	63	\N	\N	\N
86	2020-01-24 04:41:23.022945+00	2020-01-24 04:41:23.02295+00	\N	\N	64	\N	\N	\N
87	2020-01-24 04:41:23.022979+00	2020-01-24 04:41:23.022984+00	\N	\N	65	\N	\N	\N
88	2020-01-24 04:41:23.023004+00	2020-01-24 04:41:23.023009+00	\N	\N	66	\N	\N	\N
89	2020-01-24 04:41:23.023028+00	2020-01-24 04:41:23.023033+00	\N	\N	67	\N	\N	\N
90	2020-01-24 04:41:23.023053+00	2020-01-24 04:41:23.023058+00	\N	\N	68	\N	\N	\N
91	2020-01-24 04:41:23.023087+00	2020-01-24 04:41:23.023092+00	\N	\N	69	\N	\N	\N
92	2020-01-24 04:41:23.023111+00	2020-01-24 04:41:23.023116+00	\N	\N	70	\N	\N	\N
93	2020-01-24 04:41:23.023135+00	2020-01-24 04:41:23.02314+00	\N	\N	71	\N	\N	\N
94	2020-01-24 04:41:23.02316+00	2020-01-24 04:41:23.023165+00	\N	\N	72	\N	\N	\N
95	2020-01-24 04:41:23.023185+00	2020-01-24 04:41:23.023189+00	\N	\N	73	\N	\N	\N
96	2020-01-24 04:41:23.023209+00	2020-01-24 04:41:23.023214+00	\N	\N	74	\N	\N	\N
97	2020-01-24 04:41:23.023234+00	2020-01-24 04:41:23.023239+00	\N	\N	75	\N	\N	\N
98	2020-01-24 04:41:23.023258+00	2020-01-24 04:41:23.023263+00	\N	\N	76	\N	\N	\N
99	2020-01-24 04:41:23.023282+00	2020-01-24 04:41:23.023287+00	\N	\N	77	\N	\N	\N
100	2020-01-24 04:41:23.023306+00	2020-01-24 04:41:23.023311+00	\N	\N	78	\N	\N	\N
101	2020-01-24 04:41:23.02333+00	2020-01-24 04:41:23.023335+00	\N	\N	79	\N	\N	\N
102	2020-01-24 04:41:23.023355+00	2020-01-24 04:41:23.023367+00	\N	\N	80	\N	\N	\N
103	2020-01-24 04:41:23.023389+00	2020-01-24 04:41:23.023394+00	\N	\N	81	\N	\N	\N
104	2020-01-24 04:41:23.023418+00	2020-01-24 04:41:23.023425+00	\N	\N	82	\N	\N	\N
105	2020-01-24 04:41:23.023446+00	2020-01-24 04:41:23.023451+00	\N	\N	83	\N	\N	\N
106	2020-01-24 04:41:23.02347+00	2020-01-24 04:41:23.023475+00	\N	\N	84	\N	\N	\N
107	2020-01-24 04:41:23.023494+00	2020-01-24 04:41:23.023499+00	\N	\N	85	\N	\N	\N
108	2020-01-24 04:41:23.023519+00	2020-01-24 04:41:23.023523+00	\N	\N	86	\N	\N	\N
109	2020-01-24 04:41:23.023543+00	2020-01-24 04:41:23.023547+00	\N	\N	87	\N	\N	\N
110	2020-01-24 04:41:23.023567+00	2020-01-24 04:41:23.023571+00	\N	\N	88	\N	\N	\N
111	2020-01-24 04:41:23.023591+00	2020-01-24 04:41:23.023596+00	\N	\N	89	\N	\N	\N
112	2020-01-24 04:41:23.023623+00	2020-01-24 04:41:23.023629+00	\N	\N	90	\N	\N	\N
113	2020-01-24 04:41:23.041068+00	2020-01-24 04:41:23.041089+00	\N	\N	91	\N	\N	\N
114	2020-01-24 04:41:23.041126+00	2020-01-24 04:41:23.041132+00	\N	\N	92	\N	\N	\N
115	2020-01-24 04:41:23.041152+00	2020-01-24 04:41:23.041157+00	\N	\N	93	\N	\N	\N
116	2020-01-24 04:41:23.041178+00	2020-01-24 04:41:23.041182+00	\N	\N	94	\N	\N	\N
117	2020-01-24 04:41:23.041202+00	2020-01-24 04:41:23.041207+00	\N	\N	95	\N	\N	\N
118	2020-01-24 04:41:23.041226+00	2020-01-24 04:41:23.041231+00	\N	\N	96	\N	\N	\N
119	2020-01-24 04:41:23.041251+00	2020-01-24 04:41:23.041255+00	\N	\N	97	\N	\N	\N
120	2020-01-24 04:41:23.041275+00	2020-01-24 04:41:23.04128+00	\N	\N	98	\N	\N	\N
121	2020-01-24 04:41:23.0413+00	2020-01-24 04:41:23.041305+00	\N	\N	99	\N	\N	\N
122	2020-01-24 04:41:23.041325+00	2020-01-24 04:41:23.041329+00	\N	\N	100	\N	\N	\N
123	2020-01-24 04:41:23.041357+00	2020-01-24 04:41:23.041363+00	\N	\N	101	\N	\N	\N
124	2020-01-24 04:41:23.041383+00	2020-01-24 04:41:23.041388+00	\N	\N	102	\N	\N	\N
125	2020-01-24 04:41:23.041407+00	2020-01-24 04:41:23.041412+00	\N	\N	103	\N	\N	\N
126	2020-01-24 04:41:23.041432+00	2020-01-24 04:41:23.041436+00	\N	\N	104	\N	\N	\N
127	2020-01-24 04:41:23.041456+00	2020-01-24 04:41:23.041461+00	\N	\N	105	\N	\N	\N
128	2020-01-24 04:41:23.04148+00	2020-01-24 04:41:23.041485+00	\N	\N	106	\N	\N	\N
129	2020-01-24 04:41:23.041504+00	2020-01-24 04:41:23.041509+00	\N	\N	107	\N	\N	\N
130	2020-01-24 04:41:23.041529+00	2020-01-24 04:41:23.041534+00	\N	\N	108	\N	\N	\N
131	2020-01-24 04:41:23.041554+00	2020-01-24 04:41:23.041558+00	\N	\N	109	\N	\N	\N
132	2020-01-24 04:41:23.041578+00	2020-01-24 04:41:23.041583+00	\N	\N	110	\N	\N	\N
133	2020-01-24 04:41:23.041602+00	2020-01-24 04:41:23.041607+00	\N	\N	111	\N	\N	\N
134	2020-01-24 04:41:23.041626+00	2020-01-24 04:41:23.041631+00	\N	\N	112	\N	\N	\N
135	2020-01-24 04:41:23.041651+00	2020-01-24 04:41:23.041655+00	\N	\N	113	\N	\N	\N
136	2020-01-24 04:41:23.041675+00	2020-01-24 04:41:23.04168+00	\N	\N	114	\N	\N	\N
137	2020-01-24 04:41:23.041699+00	2020-01-24 04:41:23.041704+00	\N	\N	115	\N	\N	\N
138	2020-01-24 04:41:23.041724+00	2020-01-24 04:41:23.041728+00	\N	\N	116	\N	\N	\N
139	2020-01-24 04:41:23.041748+00	2020-01-24 04:41:23.041753+00	\N	\N	117	\N	\N	\N
140	2020-01-24 04:41:23.041772+00	2020-01-24 04:41:23.041777+00	\N	\N	118	\N	\N	\N
141	2020-01-24 04:41:23.041797+00	2020-01-24 04:41:23.041802+00	\N	\N	119	\N	\N	\N
142	2020-01-24 04:41:23.041821+00	2020-01-24 04:41:23.041826+00	\N	\N	120	\N	\N	\N
143	2020-01-24 04:41:23.041846+00	2020-01-24 04:41:23.041851+00	\N	\N	121	\N	\N	\N
144	2020-01-24 04:41:23.04187+00	2020-01-24 04:41:23.041875+00	\N	\N	122	\N	\N	\N
145	2020-01-24 04:41:23.041894+00	2020-01-24 04:41:23.041899+00	\N	\N	123	\N	\N	\N
146	2020-01-24 04:41:23.041918+00	2020-01-24 04:41:23.041923+00	\N	\N	124	\N	\N	\N
147	2020-01-24 04:41:23.041942+00	2020-01-24 04:41:23.041947+00	\N	\N	125	\N	\N	\N
148	2020-01-24 04:41:23.041966+00	2020-01-24 04:41:23.041971+00	\N	\N	126	\N	\N	\N
149	2020-01-24 04:41:23.041996+00	2020-01-24 04:41:23.042002+00	\N	\N	127	\N	\N	\N
150	2020-01-24 04:41:23.042024+00	2020-01-24 04:41:23.042028+00	\N	\N	128	\N	\N	\N
151	2020-01-24 04:41:23.042048+00	2020-01-24 04:41:23.042053+00	\N	\N	129	\N	\N	\N
152	2020-01-24 04:41:23.042072+00	2020-01-24 04:41:23.042077+00	\N	\N	130	\N	\N	\N
153	2020-01-24 04:41:23.042096+00	2020-01-24 04:41:23.042101+00	\N	\N	131	\N	\N	\N
154	2020-01-24 04:41:23.04212+00	2020-01-24 04:41:23.042125+00	\N	\N	132	\N	\N	\N
155	2020-01-24 04:41:23.042144+00	2020-01-24 04:41:23.042149+00	\N	\N	133	\N	\N	\N
156	2020-01-24 04:41:23.042168+00	2020-01-24 04:41:23.042173+00	\N	\N	134	\N	\N	\N
157	2020-01-24 04:41:23.042192+00	2020-01-24 04:41:23.042197+00	\N	\N	135	\N	\N	\N
158	2020-01-24 04:41:23.069972+00	2020-01-24 04:41:23.069992+00	\N	\N	136	\N	\N	\N
159	2020-01-24 04:41:23.070032+00	2020-01-24 04:41:23.070037+00	\N	\N	137	\N	\N	\N
160	2020-01-24 04:41:23.070059+00	2020-01-24 04:41:23.070064+00	\N	\N	138	\N	\N	\N
161	2020-01-24 04:41:23.070084+00	2020-01-24 04:41:23.070089+00	\N	\N	139	\N	\N	\N
162	2020-01-24 04:41:23.070108+00	2020-01-24 04:41:23.070113+00	\N	\N	140	\N	\N	\N
163	2020-01-24 04:41:23.070133+00	2020-01-24 04:41:23.070138+00	\N	\N	141	\N	\N	\N
164	2020-01-24 04:41:23.070167+00	2020-01-24 04:41:23.070172+00	\N	\N	142	\N	\N	\N
165	2020-01-24 04:41:23.070192+00	2020-01-24 04:41:23.070197+00	\N	\N	143	\N	\N	\N
166	2020-01-24 04:41:23.070217+00	2020-01-24 04:41:23.070222+00	\N	\N	144	\N	\N	\N
167	2020-01-24 04:41:23.070243+00	2020-01-24 04:41:23.070248+00	\N	\N	145	\N	\N	\N
168	2020-01-24 04:41:23.070267+00	2020-01-24 04:41:23.070272+00	\N	\N	146	\N	\N	\N
169	2020-01-24 04:41:23.070293+00	2020-01-24 04:41:23.070298+00	\N	\N	147	\N	\N	\N
170	2020-01-24 04:41:23.070326+00	2020-01-24 04:41:23.070332+00	\N	\N	148	\N	\N	\N
171	2020-01-24 04:41:23.070352+00	2020-01-24 04:41:23.070357+00	\N	\N	149	\N	\N	\N
172	2020-01-24 04:41:23.070377+00	2020-01-24 04:41:23.070382+00	\N	\N	150	\N	\N	\N
173	2020-01-24 04:41:23.070452+00	2020-01-24 04:41:23.07046+00	\N	\N	151	\N	\N	\N
174	2020-01-24 04:41:23.070483+00	2020-01-24 04:41:23.070487+00	\N	\N	152	\N	\N	\N
175	2020-01-24 04:41:23.070508+00	2020-01-24 04:41:23.070512+00	\N	\N	153	\N	\N	\N
176	2020-01-24 04:41:23.070532+00	2020-01-24 04:41:23.070537+00	\N	\N	154	\N	\N	\N
177	2020-01-24 04:41:23.070557+00	2020-01-24 04:41:23.070562+00	\N	\N	155	\N	\N	\N
178	2020-01-24 04:41:23.070582+00	2020-01-24 04:41:23.070587+00	\N	\N	156	\N	\N	\N
179	2020-01-24 04:41:23.070606+00	2020-01-24 04:41:23.070611+00	\N	\N	157	\N	\N	\N
180	2020-01-24 04:41:23.070631+00	2020-01-24 04:41:23.070636+00	\N	\N	158	\N	\N	\N
181	2020-01-24 04:41:23.070656+00	2020-01-24 04:41:23.07066+00	\N	\N	159	\N	\N	\N
182	2020-01-24 04:41:23.07068+00	2020-01-24 04:41:23.070685+00	\N	\N	160	\N	\N	\N
183	2020-01-24 04:41:23.070705+00	2020-01-24 04:41:23.07071+00	\N	\N	161	\N	\N	\N
184	2020-01-24 04:41:23.070729+00	2020-01-24 04:41:23.070734+00	\N	\N	162	\N	\N	\N
185	2020-01-24 04:41:23.070754+00	2020-01-24 04:41:23.070759+00	\N	\N	163	\N	\N	\N
186	2020-01-24 04:41:23.070778+00	2020-01-24 04:41:23.070783+00	\N	\N	164	\N	\N	\N
187	2020-01-24 04:41:23.070803+00	2020-01-24 04:41:23.070808+00	\N	\N	165	\N	\N	\N
188	2020-01-24 04:41:23.071011+00	2020-01-24 04:41:23.071019+00	\N	\N	166	\N	\N	\N
189	2020-01-24 04:41:23.071042+00	2020-01-24 04:41:23.071047+00	\N	\N	167	\N	\N	\N
190	2020-01-24 04:41:23.071068+00	2020-01-24 04:41:23.071073+00	\N	\N	168	\N	\N	\N
191	2020-01-24 04:41:23.071092+00	2020-01-24 04:41:23.071097+00	\N	\N	169	\N	\N	\N
192	2020-01-24 04:41:23.071117+00	2020-01-24 04:41:23.071122+00	\N	\N	170	\N	\N	\N
193	2020-01-24 04:41:23.071141+00	2020-01-24 04:41:23.071146+00	\N	\N	171	\N	\N	\N
194	2020-01-24 04:41:23.071173+00	2020-01-24 04:41:23.07118+00	\N	\N	172	\N	\N	\N
195	2020-01-24 04:41:23.071201+00	2020-01-24 04:41:23.071206+00	\N	\N	173	\N	\N	\N
196	2020-01-24 04:41:23.071226+00	2020-01-24 04:41:23.071231+00	\N	\N	174	\N	\N	\N
197	2020-01-24 04:41:23.071255+00	2020-01-24 04:41:23.07126+00	\N	\N	175	\N	\N	\N
198	2020-01-24 04:41:23.07128+00	2020-01-24 04:41:23.071285+00	\N	\N	176	\N	\N	\N
199	2020-01-24 04:41:23.071305+00	2020-01-24 04:41:23.07131+00	\N	\N	177	\N	\N	\N
200	2020-01-24 04:41:23.07133+00	2020-01-24 04:41:23.071334+00	\N	\N	178	\N	\N	\N
201	2020-01-24 04:41:23.071354+00	2020-01-24 04:41:23.071359+00	\N	\N	179	\N	\N	\N
202	2020-01-24 04:41:23.071379+00	2020-01-24 04:41:23.071383+00	\N	\N	180	\N	\N	\N
203	2020-01-24 04:41:23.093512+00	2020-01-24 04:41:23.093533+00	\N	\N	181	\N	\N	\N
204	2020-01-24 04:41:23.093569+00	2020-01-24 04:41:23.093575+00	\N	\N	182	\N	\N	\N
205	2020-01-24 04:41:23.093596+00	2020-01-24 04:41:23.093601+00	\N	\N	183	\N	\N	\N
206	2020-01-24 04:41:23.093621+00	2020-01-24 04:41:23.093626+00	\N	\N	184	\N	\N	\N
207	2020-01-24 04:41:23.093646+00	2020-01-24 04:41:23.093651+00	\N	\N	185	\N	\N	\N
208	2020-01-24 04:41:23.09367+00	2020-01-24 04:41:23.093675+00	\N	\N	186	\N	\N	\N
209	2020-01-24 04:41:23.093695+00	2020-01-24 04:41:23.0937+00	\N	\N	187	\N	\N	\N
210	2020-01-24 04:41:23.09372+00	2020-01-24 04:41:23.093725+00	\N	\N	188	\N	\N	\N
211	2020-01-24 04:41:23.093744+00	2020-01-24 04:41:23.093756+00	\N	\N	189	\N	\N	\N
212	2020-01-24 04:41:23.093781+00	2020-01-24 04:41:23.093786+00	\N	\N	190	\N	\N	\N
213	2020-01-24 04:41:23.093806+00	2020-01-24 04:41:23.093811+00	\N	\N	191	\N	\N	\N
214	2020-01-24 04:41:23.09383+00	2020-01-24 04:41:23.093835+00	\N	\N	192	\N	\N	\N
215	2020-01-24 04:41:23.093855+00	2020-01-24 04:41:23.093859+00	\N	\N	193	\N	\N	\N
216	2020-01-24 04:41:23.093879+00	2020-01-24 04:41:23.093884+00	\N	\N	194	\N	\N	\N
217	2020-01-24 04:41:23.093903+00	2020-01-24 04:41:23.093908+00	\N	\N	195	\N	\N	\N
218	2020-01-24 04:41:23.093927+00	2020-01-24 04:41:23.093932+00	\N	\N	196	\N	\N	\N
219	2020-01-24 04:41:23.093952+00	2020-01-24 04:41:23.093957+00	\N	\N	197	\N	\N	\N
220	2020-01-24 04:41:23.093987+00	2020-01-24 04:41:23.093992+00	\N	\N	198	\N	\N	\N
221	2020-01-24 04:41:23.094011+00	2020-01-24 04:41:23.094016+00	\N	\N	199	\N	\N	\N
222	2020-01-24 04:41:23.094036+00	2020-01-24 04:41:23.09404+00	\N	\N	200	\N	\N	\N
223	2020-01-24 04:41:23.09406+00	2020-01-24 04:41:23.094065+00	\N	\N	201	\N	\N	\N
224	2020-01-24 04:41:23.094085+00	2020-01-24 04:41:23.09409+00	\N	\N	202	\N	\N	\N
225	2020-01-24 04:41:23.094109+00	2020-01-24 04:41:23.094114+00	\N	\N	203	\N	\N	\N
226	2020-01-24 04:41:23.094134+00	2020-01-24 04:41:23.094139+00	\N	\N	204	\N	\N	\N
227	2020-01-24 04:41:23.094158+00	2020-01-24 04:41:23.094163+00	\N	\N	205	\N	\N	\N
228	2020-01-24 04:41:23.094183+00	2020-01-24 04:41:23.094187+00	\N	\N	206	\N	\N	\N
229	2020-01-24 04:41:23.094207+00	2020-01-24 04:41:23.094212+00	\N	\N	207	\N	\N	\N
230	2020-01-24 04:41:23.094231+00	2020-01-24 04:41:23.094244+00	\N	\N	208	\N	\N	\N
231	2020-01-24 04:41:23.094265+00	2020-01-24 04:41:23.09427+00	\N	\N	209	\N	\N	\N
232	2020-01-24 04:41:23.094289+00	2020-01-24 04:41:23.094294+00	\N	\N	210	\N	\N	\N
233	2020-01-24 04:41:23.094314+00	2020-01-24 04:41:23.094318+00	\N	\N	211	\N	\N	\N
234	2020-01-24 04:41:23.094338+00	2020-01-24 04:41:23.094343+00	\N	\N	212	\N	\N	\N
235	2020-01-24 04:41:23.094363+00	2020-01-24 04:41:23.094367+00	\N	\N	213	\N	\N	\N
236	2020-01-24 04:41:23.094387+00	2020-01-24 04:41:23.094392+00	\N	\N	214	\N	\N	\N
237	2020-01-24 04:41:23.094412+00	2020-01-24 04:41:23.094416+00	\N	\N	215	\N	\N	\N
238	2020-01-24 04:41:23.094436+00	2020-01-24 04:41:23.09444+00	\N	\N	216	\N	\N	\N
239	2020-01-24 04:41:23.094466+00	2020-01-24 04:41:23.094473+00	\N	\N	217	\N	\N	\N
240	2020-01-24 04:41:23.094494+00	2020-01-24 04:41:23.094499+00	\N	\N	218	\N	\N	\N
241	2020-01-24 04:41:23.094519+00	2020-01-24 04:41:23.094524+00	\N	\N	219	\N	\N	\N
242	2020-01-24 04:41:23.094543+00	2020-01-24 04:41:23.094548+00	\N	\N	220	\N	\N	\N
243	2020-01-24 04:41:23.094568+00	2020-01-24 04:41:23.094572+00	\N	\N	221	\N	\N	\N
244	2020-01-24 04:41:23.094592+00	2020-01-24 04:41:23.094597+00	\N	\N	222	\N	\N	\N
245	2020-01-24 04:41:23.094617+00	2020-01-24 04:41:23.094621+00	\N	\N	223	\N	\N	\N
246	2020-01-24 04:41:23.094641+00	2020-01-24 04:41:23.094646+00	\N	\N	224	\N	\N	\N
247	2020-01-24 04:41:23.094666+00	2020-01-24 04:41:23.094671+00	\N	\N	225	\N	\N	\N
248	2020-01-24 04:41:23.117948+00	2020-01-24 04:41:23.117968+00	\N	\N	226	\N	\N	\N
249	2020-01-24 04:41:23.118004+00	2020-01-24 04:41:23.118009+00	\N	\N	227	\N	\N	\N
250	2020-01-24 04:41:23.118031+00	2020-01-24 04:41:23.118035+00	\N	\N	228	\N	\N	\N
251	2020-01-24 04:41:23.118055+00	2020-01-24 04:41:23.11806+00	\N	\N	229	\N	\N	\N
252	2020-01-24 04:41:23.11808+00	2020-01-24 04:41:23.118084+00	\N	\N	230	\N	\N	\N
253	2020-01-24 04:41:23.118104+00	2020-01-24 04:41:23.118109+00	\N	\N	231	\N	\N	\N
254	2020-01-24 04:41:23.118129+00	2020-01-24 04:41:23.118134+00	\N	\N	232	\N	\N	\N
255	2020-01-24 04:41:23.118154+00	2020-01-24 04:41:23.118159+00	\N	\N	233	\N	\N	\N
256	2020-01-24 04:41:23.118178+00	2020-01-24 04:41:23.118183+00	\N	\N	234	\N	\N	\N
257	2020-01-24 04:41:23.118202+00	2020-01-24 04:41:23.118207+00	\N	\N	235	\N	\N	\N
258	2020-01-24 04:41:23.118227+00	2020-01-24 04:41:23.118232+00	\N	\N	236	\N	\N	\N
259	2020-01-24 04:41:23.118251+00	2020-01-24 04:41:23.118256+00	\N	\N	237	\N	\N	\N
260	2020-01-24 04:41:23.118275+00	2020-01-24 04:41:23.11828+00	\N	\N	238	\N	\N	\N
261	2020-01-24 04:41:23.1183+00	2020-01-24 04:41:23.118305+00	\N	\N	239	\N	\N	\N
262	2020-01-24 04:41:23.118324+00	2020-01-24 04:41:23.118329+00	\N	\N	240	\N	\N	\N
263	2020-01-24 04:41:23.118348+00	2020-01-24 04:41:23.118353+00	\N	\N	241	\N	\N	\N
264	2020-01-24 04:41:23.118372+00	2020-01-24 04:41:23.118377+00	\N	\N	242	\N	\N	\N
265	2020-01-24 04:41:23.118397+00	2020-01-24 04:41:23.118402+00	\N	\N	243	\N	\N	\N
266	2020-01-24 04:41:23.118421+00	2020-01-24 04:41:23.118426+00	\N	\N	244	\N	\N	\N
267	2020-01-24 04:41:23.118445+00	2020-01-24 04:41:23.11845+00	\N	\N	245	\N	\N	\N
268	2020-01-24 04:41:23.11847+00	2020-01-24 04:41:23.118475+00	\N	\N	246	\N	\N	\N
269	2020-01-24 04:41:23.118495+00	2020-01-24 04:41:23.118499+00	\N	\N	247	\N	\N	\N
270	2020-01-24 04:41:23.118519+00	2020-01-24 04:41:23.118524+00	\N	\N	248	\N	\N	\N
271	2020-01-24 04:41:23.118543+00	2020-01-24 04:41:23.118548+00	\N	\N	249	\N	\N	\N
272	2020-01-24 04:41:23.118568+00	2020-01-24 04:41:23.118572+00	\N	\N	250	\N	\N	\N
273	2020-01-24 04:41:23.118592+00	2020-01-24 04:41:23.118597+00	\N	\N	251	\N	\N	\N
274	2020-01-24 04:41:23.118617+00	2020-01-24 04:41:23.118622+00	\N	\N	252	\N	\N	\N
275	2020-01-24 04:41:23.118642+00	2020-01-24 04:41:23.118647+00	\N	\N	253	\N	\N	\N
276	2020-01-24 04:41:23.118676+00	2020-01-24 04:41:23.118681+00	\N	\N	254	\N	\N	\N
277	2020-01-24 04:41:23.1187+00	2020-01-24 04:41:23.118705+00	\N	\N	255	\N	\N	\N
278	2020-01-24 04:41:23.118725+00	2020-01-24 04:41:23.11873+00	\N	\N	256	\N	\N	\N
279	2020-01-24 04:41:23.118749+00	2020-01-24 04:41:23.118754+00	\N	\N	257	\N	\N	\N
280	2020-01-24 04:41:23.118774+00	2020-01-24 04:41:23.118778+00	\N	\N	258	\N	\N	\N
281	2020-01-24 04:41:23.118798+00	2020-01-24 04:41:23.118803+00	\N	\N	259	\N	\N	\N
282	2020-01-24 04:41:23.118822+00	2020-01-24 04:41:23.118827+00	\N	\N	260	\N	\N	\N
283	2020-01-24 04:41:23.118847+00	2020-01-24 04:41:23.118851+00	\N	\N	261	\N	\N	\N
284	2020-01-24 04:41:23.118888+00	2020-01-24 04:41:23.118895+00	\N	\N	262	\N	\N	\N
285	2020-01-24 04:41:23.118937+00	2020-01-24 04:41:23.118944+00	\N	\N	263	\N	\N	\N
286	2020-01-24 04:41:23.119223+00	2020-01-24 04:41:23.119232+00	\N	\N	264	\N	\N	\N
287	2020-01-24 04:41:23.119267+00	2020-01-24 04:41:23.119274+00	\N	\N	265	\N	\N	\N
288	2020-01-24 04:41:23.119306+00	2020-01-24 04:41:23.119313+00	\N	\N	266	\N	\N	\N
289	2020-01-24 04:41:23.119345+00	2020-01-24 04:41:23.119352+00	\N	\N	267	\N	\N	\N
290	2020-01-24 04:41:23.119383+00	2020-01-24 04:41:23.11939+00	\N	\N	268	\N	\N	\N
291	2020-01-24 04:41:23.119422+00	2020-01-24 04:41:23.119429+00	\N	\N	269	\N	\N	\N
292	2020-01-24 04:41:23.11946+00	2020-01-24 04:41:23.119467+00	\N	\N	270	\N	\N	\N
293	2020-01-24 04:41:23.137862+00	2020-01-24 04:41:23.137888+00	\N	12	\N	\N	\N	\N
294	2020-01-24 04:41:23.137922+00	2020-01-24 04:41:23.137928+00	\N	13	\N	\N	\N	\N
295	2020-01-24 04:41:23.137948+00	2020-01-24 04:41:23.137953+00	\N	14	\N	\N	\N	\N
296	2020-01-24 04:41:23.137973+00	2020-01-24 04:41:23.137978+00	\N	15	\N	\N	\N	\N
297	2020-01-24 04:41:23.137997+00	2020-01-24 04:41:23.138002+00	\N	16	\N	\N	\N	\N
298	2020-01-24 04:41:23.138021+00	2020-01-24 04:41:23.138026+00	\N	17	\N	\N	\N	\N
299	2020-01-24 04:41:23.138046+00	2020-01-24 04:41:23.138051+00	\N	18	\N	\N	\N	\N
300	2020-01-24 04:41:23.13807+00	2020-01-24 04:41:23.138075+00	\N	19	\N	\N	\N	\N
301	2020-01-24 04:41:23.138095+00	2020-01-24 04:41:23.1381+00	\N	20	\N	\N	\N	\N
302	2020-01-24 04:41:23.138119+00	2020-01-24 04:41:23.138124+00	\N	21	\N	\N	\N	\N
303	2020-01-24 04:41:23.155326+00	2020-01-24 04:41:23.155345+00	1	\N	\N	\N	\N	\N
304	2020-01-24 04:41:23.155381+00	2020-01-24 04:41:23.155387+00	2	\N	\N	\N	\N	\N
305	2020-01-24 04:41:23.155408+00	2020-01-24 04:41:23.155413+00	3	\N	\N	\N	\N	\N
306	2020-01-24 04:41:23.155432+00	2020-01-24 04:41:23.155437+00	4	\N	\N	\N	\N	\N
307	2020-01-24 04:41:23.174955+00	2020-01-24 04:41:23.174985+00	5	\N	\N	\N	\N	\N
308	2020-01-24 04:41:23.17502+00	2020-01-24 04:41:23.175025+00	6	\N	\N	\N	\N	\N
309	2020-01-24 04:41:23.175057+00	2020-01-24 04:41:23.175062+00	7	\N	\N	\N	\N	\N
310	2020-01-24 04:41:23.175083+00	2020-01-24 04:41:23.175088+00	8	\N	\N	\N	\N	\N
311	2020-01-24 04:41:23.188936+00	2020-01-24 04:41:23.188953+00	9	\N	\N	\N	\N	\N
312	2020-01-24 04:41:23.188986+00	2020-01-24 04:41:23.188991+00	10	\N	\N	\N	\N	\N
313	2020-01-24 04:41:23.189012+00	2020-01-24 04:41:23.189017+00	11	\N	\N	\N	\N	\N
314	2020-01-24 04:41:23.189037+00	2020-01-24 04:41:23.189041+00	12	\N	\N	\N	\N	\N
315	2020-01-24 04:41:23.20184+00	2020-01-24 04:41:23.201856+00	13	\N	\N	\N	\N	\N
316	2020-01-24 04:41:23.201888+00	2020-01-24 04:41:23.201894+00	14	\N	\N	\N	\N	\N
317	2020-01-24 04:41:23.201915+00	2020-01-24 04:41:23.20192+00	15	\N	\N	\N	\N	\N
318	2020-01-24 04:41:23.20194+00	2020-01-24 04:41:23.201945+00	16	\N	\N	\N	\N	\N
319	2020-01-24 04:41:23.212883+00	2020-01-24 04:41:23.212899+00	17	\N	\N	\N	\N	\N
320	2020-01-24 04:41:23.212931+00	2020-01-24 04:41:23.212937+00	18	\N	\N	\N	\N	\N
321	2020-01-24 04:41:23.212958+00	2020-01-24 04:41:23.212963+00	19	\N	\N	\N	\N	\N
322	2020-01-24 04:41:23.212983+00	2020-01-24 04:41:23.212988+00	20	\N	\N	\N	\N	\N
323	2020-01-24 04:41:23.257846+00	2020-01-24 04:41:23.257866+00	21	\N	\N	\N	\N	\N
324	2020-01-24 04:41:23.2579+00	2020-01-24 04:41:23.257906+00	22	\N	\N	\N	\N	\N
325	2020-01-24 04:41:23.257927+00	2020-01-24 04:41:23.257932+00	23	\N	\N	\N	\N	\N
326	2020-01-24 04:41:23.257952+00	2020-01-24 04:41:23.257956+00	24	\N	\N	\N	\N	\N
327	2020-01-24 04:41:23.265312+00	2020-01-24 04:41:23.265327+00	25	\N	\N	\N	\N	\N
328	2020-01-24 04:41:23.265361+00	2020-01-24 04:41:23.265367+00	26	\N	\N	\N	\N	\N
329	2020-01-24 04:41:23.265388+00	2020-01-24 04:41:23.265393+00	27	\N	\N	\N	\N	\N
330	2020-01-24 04:41:23.265412+00	2020-01-24 04:41:23.265417+00	28	\N	\N	\N	\N	\N
331	2020-01-24 04:41:23.272423+00	2020-01-24 04:41:23.272437+00	29	\N	\N	\N	\N	\N
332	2020-01-24 04:41:23.272469+00	2020-01-24 04:41:23.272474+00	30	\N	\N	\N	\N	\N
333	2020-01-24 04:41:23.272495+00	2020-01-24 04:41:23.2725+00	31	\N	\N	\N	\N	\N
334	2020-01-24 04:41:23.272519+00	2020-01-24 04:41:23.272524+00	32	\N	\N	\N	\N	\N
335	2020-01-24 04:41:23.279315+00	2020-01-24 04:41:23.279328+00	33	\N	\N	\N	\N	\N
336	2020-01-24 04:41:23.279359+00	2020-01-24 04:41:23.279365+00	34	\N	\N	\N	\N	\N
337	2020-01-24 04:41:23.279386+00	2020-01-24 04:41:23.279391+00	35	\N	\N	\N	\N	\N
338	2020-01-24 04:41:23.27941+00	2020-01-24 04:41:23.279415+00	36	\N	\N	\N	\N	\N
339	2020-01-24 04:41:23.289466+00	2020-01-24 04:41:23.289481+00	37	\N	\N	\N	\N	\N
340	2020-01-24 04:41:23.289514+00	2020-01-24 04:41:23.28952+00	38	\N	\N	\N	\N	\N
341	2020-01-24 04:41:23.304349+00	2020-01-24 04:41:23.304365+00	\N	22	\N	\N	\N	\N
342	2020-01-24 04:41:23.304399+00	2020-01-24 04:41:23.304405+00	\N	23	\N	\N	\N	\N
343	2020-01-24 04:41:23.304426+00	2020-01-24 04:41:23.304431+00	\N	24	\N	\N	\N	\N
344	2020-01-24 04:41:23.304451+00	2020-01-24 04:41:23.304456+00	\N	25	\N	\N	\N	\N
345	2020-01-24 04:41:23.318248+00	2020-01-24 04:41:23.318265+00	39	\N	\N	\N	\N	\N
346	2020-01-24 04:41:23.318299+00	2020-01-24 04:41:23.318305+00	40	\N	\N	\N	\N	\N
347	2020-01-24 04:41:23.318326+00	2020-01-24 04:41:23.318331+00	41	\N	\N	\N	\N	\N
348	2020-01-24 04:41:23.31835+00	2020-01-24 04:41:23.318355+00	42	\N	\N	\N	\N	\N
349	2020-01-24 04:41:23.330047+00	2020-01-24 04:41:23.330064+00	43	\N	\N	\N	\N	\N
350	2020-01-24 04:41:23.330097+00	2020-01-24 04:41:23.330102+00	44	\N	\N	\N	\N	\N
351	2020-01-24 04:41:23.330123+00	2020-01-24 04:41:23.330128+00	45	\N	\N	\N	\N	\N
352	2020-01-24 04:41:23.330149+00	2020-01-24 04:41:23.330154+00	46	\N	\N	\N	\N	\N
353	2020-01-24 04:41:23.341014+00	2020-01-24 04:41:23.341029+00	47	\N	\N	\N	\N	\N
354	2020-01-24 04:41:23.341062+00	2020-01-24 04:41:23.341068+00	48	\N	\N	\N	\N	\N
355	2020-01-24 04:41:23.341089+00	2020-01-24 04:41:23.341094+00	49	\N	\N	\N	\N	\N
356	2020-01-24 04:41:23.341114+00	2020-01-24 04:41:23.341118+00	50	\N	\N	\N	\N	\N
357	2020-01-24 04:41:23.354161+00	2020-01-24 04:41:23.35418+00	51	\N	\N	\N	\N	\N
358	2020-01-24 04:41:23.354215+00	2020-01-24 04:41:23.35422+00	52	\N	\N	\N	\N	\N
359	2020-01-24 04:41:23.354242+00	2020-01-24 04:41:23.354247+00	53	\N	\N	\N	\N	\N
360	2020-01-24 04:41:23.354267+00	2020-01-24 04:41:23.354272+00	54	\N	\N	\N	\N	\N
361	2020-01-24 04:41:23.368952+00	2020-01-24 04:41:23.36897+00	\N	26	\N	\N	\N	\N
362	2020-01-24 04:41:23.369005+00	2020-01-24 04:41:23.36901+00	\N	27	\N	\N	\N	\N
363	2020-01-24 04:41:23.369031+00	2020-01-24 04:41:23.369036+00	\N	28	\N	\N	\N	\N
364	2020-01-24 04:41:23.369056+00	2020-01-24 04:41:23.369061+00	\N	29	\N	\N	\N	\N
365	2020-01-24 04:41:23.378013+00	2020-01-24 04:41:23.378027+00	55	\N	\N	\N	\N	\N
366	2020-01-24 04:41:23.378059+00	2020-01-24 04:41:23.378064+00	56	\N	\N	\N	\N	\N
367	2020-01-24 04:41:23.378085+00	2020-01-24 04:41:23.37809+00	57	\N	\N	\N	\N	\N
368	2020-01-24 04:41:23.378111+00	2020-01-24 04:41:23.378116+00	58	\N	\N	\N	\N	\N
369	2020-01-24 04:41:23.384895+00	2020-01-24 04:41:23.384907+00	59	\N	\N	\N	\N	\N
370	2020-01-24 04:41:23.384939+00	2020-01-24 04:41:23.384945+00	60	\N	\N	\N	\N	\N
371	2020-01-24 04:41:23.384965+00	2020-01-24 04:41:23.38497+00	61	\N	\N	\N	\N	\N
372	2020-01-24 04:41:23.38499+00	2020-01-24 04:41:23.384995+00	62	\N	\N	\N	\N	\N
373	2020-01-24 04:41:23.398695+00	2020-01-24 04:41:23.398712+00	63	\N	\N	\N	\N	\N
374	2020-01-24 04:41:23.398745+00	2020-01-24 04:41:23.398751+00	64	\N	\N	\N	\N	\N
375	2020-01-24 04:41:23.398772+00	2020-01-24 04:41:23.398777+00	65	\N	\N	\N	\N	\N
376	2020-01-24 04:41:23.398796+00	2020-01-24 04:41:23.398801+00	66	\N	\N	\N	\N	\N
377	2020-01-24 04:41:23.411692+00	2020-01-24 04:41:23.41171+00	67	\N	\N	\N	\N	\N
378	2020-01-24 04:41:23.411744+00	2020-01-24 04:41:23.41175+00	68	\N	\N	\N	\N	\N
379	2020-01-24 04:41:23.411771+00	2020-01-24 04:41:23.411776+00	69	\N	\N	\N	\N	\N
380	2020-01-24 04:41:23.411796+00	2020-01-24 04:41:23.411801+00	70	\N	\N	\N	\N	\N
381	2020-01-24 04:41:23.431223+00	2020-01-24 04:41:23.431243+00	\N	30	\N	\N	\N	\N
382	2020-01-24 04:41:23.431279+00	2020-01-24 04:41:23.431285+00	\N	31	\N	\N	\N	\N
383	2020-01-24 04:41:23.431306+00	2020-01-24 04:41:23.431311+00	\N	32	\N	\N	\N	\N
384	2020-01-24 04:41:23.431331+00	2020-01-24 04:41:23.431336+00	\N	33	\N	\N	\N	\N
385	2020-01-24 04:41:23.45078+00	2020-01-24 04:41:23.450799+00	71	\N	\N	\N	\N	\N
386	2020-01-24 04:41:23.450833+00	2020-01-24 04:41:23.450839+00	72	\N	\N	\N	\N	\N
387	2020-01-24 04:41:23.450864+00	2020-01-24 04:41:23.450869+00	73	\N	\N	\N	\N	\N
388	2020-01-24 04:41:23.450889+00	2020-01-24 04:41:23.450949+00	74	\N	\N	\N	\N	\N
389	2020-01-24 04:41:23.469371+00	2020-01-24 04:41:23.46939+00	75	\N	\N	\N	\N	\N
390	2020-01-24 04:41:23.469586+00	2020-01-24 04:41:23.469594+00	76	\N	\N	\N	\N	\N
391	2020-01-24 04:41:23.469633+00	2020-01-24 04:41:23.46964+00	77	\N	\N	\N	\N	\N
392	2020-01-24 04:41:23.469662+00	2020-01-24 04:41:23.469667+00	78	\N	\N	\N	\N	\N
393	2020-01-24 04:41:23.486515+00	2020-01-24 04:41:23.486534+00	79	\N	\N	\N	\N	\N
394	2020-01-24 04:41:23.486568+00	2020-01-24 04:41:23.486573+00	80	\N	\N	\N	\N	\N
395	2020-01-24 04:41:23.486594+00	2020-01-24 04:41:23.486599+00	81	\N	\N	\N	\N	\N
396	2020-01-24 04:41:23.486618+00	2020-01-24 04:41:23.486623+00	82	\N	\N	\N	\N	\N
397	2020-01-24 04:41:23.502611+00	2020-01-24 04:41:23.502629+00	83	\N	\N	\N	\N	\N
398	2020-01-24 04:41:23.502673+00	2020-01-24 04:41:23.502679+00	84	\N	\N	\N	\N	\N
399	2020-01-24 04:41:23.502757+00	2020-01-24 04:41:23.502763+00	85	\N	\N	\N	\N	\N
400	2020-01-24 04:41:23.502784+00	2020-01-24 04:41:23.50279+00	86	\N	\N	\N	\N	\N
401	2020-01-24 04:41:23.513117+00	2020-01-24 04:41:23.513132+00	\N	34	\N	\N	\N	\N
402	2020-01-24 04:41:23.513165+00	2020-01-24 04:41:23.513171+00	\N	35	\N	\N	\N	\N
403	2020-01-24 04:41:23.513192+00	2020-01-24 04:41:23.513197+00	\N	36	\N	\N	\N	\N
404	2020-01-24 04:41:23.513217+00	2020-01-24 04:41:23.513222+00	\N	37	\N	\N	\N	\N
405	2020-01-24 04:41:23.522618+00	2020-01-24 04:41:23.522632+00	87	\N	\N	\N	\N	\N
406	2020-01-24 04:41:23.522663+00	2020-01-24 04:41:23.522669+00	88	\N	\N	\N	\N	\N
407	2020-01-24 04:41:23.52269+00	2020-01-24 04:41:23.522695+00	89	\N	\N	\N	\N	\N
408	2020-01-24 04:41:23.522714+00	2020-01-24 04:41:23.522719+00	90	\N	\N	\N	\N	\N
409	2020-01-24 04:41:23.531249+00	2020-01-24 04:41:23.531263+00	91	\N	\N	\N	\N	\N
410	2020-01-24 04:41:23.531295+00	2020-01-24 04:41:23.5313+00	92	\N	\N	\N	\N	\N
411	2020-01-24 04:41:23.531321+00	2020-01-24 04:41:23.531326+00	93	\N	\N	\N	\N	\N
412	2020-01-24 04:41:23.531346+00	2020-01-24 04:41:23.531351+00	94	\N	\N	\N	\N	\N
413	2020-01-24 04:41:23.539911+00	2020-01-24 04:41:23.539928+00	95	\N	\N	\N	\N	\N
414	2020-01-24 04:41:23.539961+00	2020-01-24 04:41:23.539966+00	96	\N	\N	\N	\N	\N
415	2020-01-24 04:41:23.539988+00	2020-01-24 04:41:23.539993+00	97	\N	\N	\N	\N	\N
416	2020-01-24 04:41:23.540013+00	2020-01-24 04:41:23.540018+00	98	\N	\N	\N	\N	\N
417	2020-01-24 04:41:23.551338+00	2020-01-24 04:41:23.551361+00	99	\N	\N	\N	\N	\N
418	2020-01-24 04:41:23.55146+00	2020-01-24 04:41:23.551467+00	100	\N	\N	\N	\N	\N
419	2020-01-24 04:41:23.551488+00	2020-01-24 04:41:23.551493+00	101	\N	\N	\N	\N	\N
420	2020-01-24 04:41:23.551513+00	2020-01-24 04:41:23.551518+00	102	\N	\N	\N	\N	\N
421	2020-01-24 04:41:23.567035+00	2020-01-24 04:41:23.567053+00	\N	38	\N	\N	\N	\N
422	2020-01-24 04:41:23.581916+00	2020-01-24 04:41:23.581934+00	103	\N	\N	\N	\N	\N
423	2020-01-24 04:41:23.581968+00	2020-01-24 04:41:23.581974+00	104	\N	\N	\N	\N	\N
424	2020-01-24 04:41:23.582007+00	2020-01-24 04:41:23.582012+00	105	\N	\N	\N	\N	\N
425	2020-01-24 04:41:23.582032+00	2020-01-24 04:41:23.582037+00	106	\N	\N	\N	\N	\N
\.


--
-- Data for Name: locations_pigletsgroupcell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_pigletsgroupcell (id, created_at, modified_at, number, section_id, workshop_id) FROM stdin;
1	2020-01-24 04:41:23.146755+00	2020-01-24 04:41:23.146774+00	1	12	4
2	2020-01-24 04:41:23.146809+00	2020-01-24 04:41:23.146815+00	2	12	4
3	2020-01-24 04:41:23.146835+00	2020-01-24 04:41:23.14684+00	3	12	4
4	2020-01-24 04:41:23.146859+00	2020-01-24 04:41:23.146863+00	4	12	4
5	2020-01-24 04:41:23.162214+00	2020-01-24 04:41:23.162232+00	1	13	4
6	2020-01-24 04:41:23.162267+00	2020-01-24 04:41:23.162273+00	2	13	4
7	2020-01-24 04:41:23.162292+00	2020-01-24 04:41:23.162297+00	3	13	4
8	2020-01-24 04:41:23.162315+00	2020-01-24 04:41:23.16232+00	4	13	4
9	2020-01-24 04:41:23.181341+00	2020-01-24 04:41:23.181357+00	1	14	4
10	2020-01-24 04:41:23.181391+00	2020-01-24 04:41:23.181396+00	2	14	4
11	2020-01-24 04:41:23.181416+00	2020-01-24 04:41:23.181422+00	3	14	4
12	2020-01-24 04:41:23.181441+00	2020-01-24 04:41:23.181446+00	4	14	4
13	2020-01-24 04:41:23.1954+00	2020-01-24 04:41:23.195417+00	1	15	4
14	2020-01-24 04:41:23.195459+00	2020-01-24 04:41:23.195466+00	2	15	4
15	2020-01-24 04:41:23.195487+00	2020-01-24 04:41:23.195492+00	3	15	4
16	2020-01-24 04:41:23.195515+00	2020-01-24 04:41:23.195521+00	4	15	4
17	2020-01-24 04:41:23.208962+00	2020-01-24 04:41:23.208979+00	1	16	4
18	2020-01-24 04:41:23.209025+00	2020-01-24 04:41:23.209031+00	2	16	4
19	2020-01-24 04:41:23.209052+00	2020-01-24 04:41:23.209057+00	3	16	4
20	2020-01-24 04:41:23.209076+00	2020-01-24 04:41:23.20908+00	4	16	4
21	2020-01-24 04:41:23.25192+00	2020-01-24 04:41:23.25194+00	1	17	4
22	2020-01-24 04:41:23.251978+00	2020-01-24 04:41:23.251984+00	2	17	4
23	2020-01-24 04:41:23.252004+00	2020-01-24 04:41:23.252009+00	3	17	4
24	2020-01-24 04:41:23.252028+00	2020-01-24 04:41:23.252032+00	4	17	4
25	2020-01-24 04:41:23.261727+00	2020-01-24 04:41:23.261742+00	1	18	4
26	2020-01-24 04:41:23.261782+00	2020-01-24 04:41:23.261812+00	2	18	4
27	2020-01-24 04:41:23.261834+00	2020-01-24 04:41:23.261861+00	3	18	4
28	2020-01-24 04:41:23.261882+00	2020-01-24 04:41:23.261887+00	4	18	4
29	2020-01-24 04:41:23.269105+00	2020-01-24 04:41:23.26912+00	1	19	4
30	2020-01-24 04:41:23.269153+00	2020-01-24 04:41:23.269159+00	2	19	4
31	2020-01-24 04:41:23.269179+00	2020-01-24 04:41:23.269185+00	3	19	4
32	2020-01-24 04:41:23.269204+00	2020-01-24 04:41:23.269209+00	4	19	4
33	2020-01-24 04:41:23.275946+00	2020-01-24 04:41:23.27596+00	1	20	4
34	2020-01-24 04:41:23.275993+00	2020-01-24 04:41:23.275998+00	2	20	4
35	2020-01-24 04:41:23.276018+00	2020-01-24 04:41:23.276023+00	3	20	4
36	2020-01-24 04:41:23.276051+00	2020-01-24 04:41:23.276056+00	4	20	4
37	2020-01-24 04:41:23.284715+00	2020-01-24 04:41:23.284729+00	1	21	4
38	2020-01-24 04:41:23.284762+00	2020-01-24 04:41:23.284768+00	2	21	4
39	2020-01-24 04:41:23.311522+00	2020-01-24 04:41:23.311539+00	1	22	8
40	2020-01-24 04:41:23.311578+00	2020-01-24 04:41:23.311584+00	2	22	8
41	2020-01-24 04:41:23.311605+00	2020-01-24 04:41:23.31161+00	3	22	8
42	2020-01-24 04:41:23.311628+00	2020-01-24 04:41:23.311633+00	4	22	8
43	2020-01-24 04:41:23.324501+00	2020-01-24 04:41:23.324518+00	1	23	8
44	2020-01-24 04:41:23.324552+00	2020-01-24 04:41:23.324558+00	2	23	8
45	2020-01-24 04:41:23.324577+00	2020-01-24 04:41:23.324582+00	3	23	8
46	2020-01-24 04:41:23.324601+00	2020-01-24 04:41:23.324606+00	4	23	8
47	2020-01-24 04:41:23.335632+00	2020-01-24 04:41:23.335647+00	1	24	8
48	2020-01-24 04:41:23.335692+00	2020-01-24 04:41:23.335698+00	2	24	8
49	2020-01-24 04:41:23.335719+00	2020-01-24 04:41:23.335724+00	3	24	8
50	2020-01-24 04:41:23.335747+00	2020-01-24 04:41:23.335753+00	4	24	8
51	2020-01-24 04:41:23.347574+00	2020-01-24 04:41:23.347593+00	1	25	8
52	2020-01-24 04:41:23.34763+00	2020-01-24 04:41:23.347636+00	2	25	8
53	2020-01-24 04:41:23.347657+00	2020-01-24 04:41:23.347662+00	3	25	8
54	2020-01-24 04:41:23.347681+00	2020-01-24 04:41:23.347686+00	4	25	8
55	2020-01-24 04:41:23.374274+00	2020-01-24 04:41:23.37429+00	1	26	5
56	2020-01-24 04:41:23.374325+00	2020-01-24 04:41:23.37433+00	2	26	5
57	2020-01-24 04:41:23.37435+00	2020-01-24 04:41:23.374355+00	3	26	5
58	2020-01-24 04:41:23.374374+00	2020-01-24 04:41:23.374379+00	4	26	5
59	2020-01-24 04:41:23.381937+00	2020-01-24 04:41:23.381952+00	1	27	5
60	2020-01-24 04:41:23.381984+00	2020-01-24 04:41:23.38199+00	2	27	5
61	2020-01-24 04:41:23.382009+00	2020-01-24 04:41:23.382015+00	3	27	5
62	2020-01-24 04:41:23.382034+00	2020-01-24 04:41:23.382039+00	4	27	5
63	2020-01-24 04:41:23.391701+00	2020-01-24 04:41:23.391719+00	1	28	5
64	2020-01-24 04:41:23.391756+00	2020-01-24 04:41:23.391762+00	2	28	5
65	2020-01-24 04:41:23.391791+00	2020-01-24 04:41:23.3918+00	3	28	5
66	2020-01-24 04:41:23.39182+00	2020-01-24 04:41:23.391825+00	4	28	5
67	2020-01-24 04:41:23.405014+00	2020-01-24 04:41:23.40503+00	1	29	5
68	2020-01-24 04:41:23.405063+00	2020-01-24 04:41:23.405069+00	2	29	5
69	2020-01-24 04:41:23.405089+00	2020-01-24 04:41:23.405094+00	3	29	5
70	2020-01-24 04:41:23.405113+00	2020-01-24 04:41:23.405118+00	4	29	5
71	2020-01-24 04:41:23.438805+00	2020-01-24 04:41:23.438822+00	1	30	6
72	2020-01-24 04:41:23.438855+00	2020-01-24 04:41:23.438861+00	2	30	6
73	2020-01-24 04:41:23.438881+00	2020-01-24 04:41:23.438886+00	3	30	6
74	2020-01-24 04:41:23.438905+00	2020-01-24 04:41:23.43891+00	4	30	6
75	2020-01-24 04:41:23.461012+00	2020-01-24 04:41:23.461052+00	1	31	6
76	2020-01-24 04:41:23.461091+00	2020-01-24 04:41:23.461097+00	2	31	6
77	2020-01-24 04:41:23.461118+00	2020-01-24 04:41:23.461123+00	3	31	6
78	2020-01-24 04:41:23.461143+00	2020-01-24 04:41:23.461148+00	4	31	6
79	2020-01-24 04:41:23.476964+00	2020-01-24 04:41:23.476982+00	1	32	6
80	2020-01-24 04:41:23.477074+00	2020-01-24 04:41:23.477081+00	2	32	6
81	2020-01-24 04:41:23.477103+00	2020-01-24 04:41:23.477108+00	3	32	6
82	2020-01-24 04:41:23.477128+00	2020-01-24 04:41:23.477133+00	4	32	6
83	2020-01-24 04:41:23.493578+00	2020-01-24 04:41:23.493597+00	1	33	6
84	2020-01-24 04:41:23.493637+00	2020-01-24 04:41:23.493643+00	2	33	6
85	2020-01-24 04:41:23.493663+00	2020-01-24 04:41:23.493668+00	3	33	6
86	2020-01-24 04:41:23.493687+00	2020-01-24 04:41:23.493692+00	4	33	6
87	2020-01-24 04:41:23.518517+00	2020-01-24 04:41:23.518533+00	1	34	7
88	2020-01-24 04:41:23.518569+00	2020-01-24 04:41:23.518575+00	2	34	7
89	2020-01-24 04:41:23.518602+00	2020-01-24 04:41:23.518608+00	3	34	7
90	2020-01-24 04:41:23.518627+00	2020-01-24 04:41:23.518636+00	4	34	7
91	2020-01-24 04:41:23.527496+00	2020-01-24 04:41:23.527512+00	1	35	7
92	2020-01-24 04:41:23.527547+00	2020-01-24 04:41:23.527553+00	2	35	7
93	2020-01-24 04:41:23.527574+00	2020-01-24 04:41:23.527579+00	3	35	7
94	2020-01-24 04:41:23.527598+00	2020-01-24 04:41:23.527603+00	4	35	7
95	2020-01-24 04:41:23.536024+00	2020-01-24 04:41:23.536041+00	1	36	7
96	2020-01-24 04:41:23.536074+00	2020-01-24 04:41:23.53608+00	2	36	7
97	2020-01-24 04:41:23.536099+00	2020-01-24 04:41:23.536105+00	3	36	7
98	2020-01-24 04:41:23.536152+00	2020-01-24 04:41:23.536173+00	4	36	7
99	2020-01-24 04:41:23.544512+00	2020-01-24 04:41:23.544528+00	1	37	7
100	2020-01-24 04:41:23.544562+00	2020-01-24 04:41:23.544568+00	2	37	7
101	2020-01-24 04:41:23.544588+00	2020-01-24 04:41:23.544593+00	3	37	7
102	2020-01-24 04:41:23.544611+00	2020-01-24 04:41:23.544616+00	4	37	7
103	2020-01-24 04:41:23.574667+00	2020-01-24 04:41:23.574685+00	1	38	11
104	2020-01-24 04:41:23.574719+00	2020-01-24 04:41:23.574725+00	2	38	11
105	2020-01-24 04:41:23.574745+00	2020-01-24 04:41:23.57475+00	3	38	11
106	2020-01-24 04:41:23.574769+00	2020-01-24 04:41:23.574775+00	4	38	11
\.


--
-- Data for Name: locations_section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_section (id, created_at, modified_at, name, number, workshop_id) FROM stdin;
1	2020-01-24 04:41:22.9395+00	2020-01-24 04:41:22.939519+00	Змейка	1	1
2	2020-01-24 04:41:22.939549+00	2020-01-24 04:41:22.939555+00	Ряд осеменения	2	1
3	2020-01-24 04:41:22.939572+00	2020-01-24 04:41:22.939577+00	Групповые клетки	3	1
4	2020-01-24 04:41:22.955429+00	2020-01-24 04:41:22.955448+00	Секция 2-1	1	2
5	2020-01-24 04:41:22.95548+00	2020-01-24 04:41:22.955485+00	Секция 2-2	2	2
6	2020-01-24 04:41:22.970296+00	2020-01-24 04:41:22.970314+00	Секция 3-1	1	3
7	2020-01-24 04:41:22.970345+00	2020-01-24 04:41:22.970351+00	Секция 3-2	2	3
8	2020-01-24 04:41:22.970367+00	2020-01-24 04:41:22.970372+00	Секция 3-3	3	3
9	2020-01-24 04:41:22.970388+00	2020-01-24 04:41:22.970392+00	Секция 3-4	4	3
10	2020-01-24 04:41:22.970408+00	2020-01-24 04:41:22.970413+00	Секция 3-5	5	3
11	2020-01-24 04:41:22.970428+00	2020-01-24 04:41:22.970433+00	Секция 3-6	6	3
12	2020-01-24 04:41:23.130146+00	2020-01-24 04:41:23.130164+00	Секция 4-1	1	4
13	2020-01-24 04:41:23.130195+00	2020-01-24 04:41:23.130201+00	Секция 4-2	2	4
14	2020-01-24 04:41:23.130219+00	2020-01-24 04:41:23.130224+00	Секция 4-3	3	4
15	2020-01-24 04:41:23.130239+00	2020-01-24 04:41:23.130244+00	Секция 4-4	4	4
16	2020-01-24 04:41:23.13026+00	2020-01-24 04:41:23.130264+00	Секция 4-5	5	4
17	2020-01-24 04:41:23.13028+00	2020-01-24 04:41:23.130285+00	Секция 4-6	6	4
18	2020-01-24 04:41:23.1303+00	2020-01-24 04:41:23.130305+00	Секция 4-7	7	4
19	2020-01-24 04:41:23.13032+00	2020-01-24 04:41:23.130325+00	Секция 4-8	8	4
20	2020-01-24 04:41:23.13034+00	2020-01-24 04:41:23.130345+00	Секция 4-9	9	4
21	2020-01-24 04:41:23.130369+00	2020-01-24 04:41:23.130374+00	Секция 4-10	10	4
22	2020-01-24 04:41:23.298454+00	2020-01-24 04:41:23.298472+00	Секция 8-1	1	8
23	2020-01-24 04:41:23.298503+00	2020-01-24 04:41:23.298508+00	Секция 8-2	2	8
24	2020-01-24 04:41:23.298525+00	2020-01-24 04:41:23.29853+00	Секция 8-3	3	8
25	2020-01-24 04:41:23.298546+00	2020-01-24 04:41:23.298551+00	Секция 8-4	4	8
26	2020-01-24 04:41:23.362122+00	2020-01-24 04:41:23.362141+00	Секция 5-1	1	5
27	2020-01-24 04:41:23.362172+00	2020-01-24 04:41:23.362178+00	Секция 5-2	2	5
28	2020-01-24 04:41:23.362194+00	2020-01-24 04:41:23.362199+00	Секция 5-3	3	5
29	2020-01-24 04:41:23.362215+00	2020-01-24 04:41:23.36222+00	Секция 5-4	4	5
30	2020-01-24 04:41:23.417487+00	2020-01-24 04:41:23.417506+00	Секция 6-1	1	6
31	2020-01-24 04:41:23.417539+00	2020-01-24 04:41:23.417545+00	Секция 6-2	2	6
32	2020-01-24 04:41:23.417562+00	2020-01-24 04:41:23.417567+00	Секция 6-3	3	6
33	2020-01-24 04:41:23.417583+00	2020-01-24 04:41:23.417588+00	Секция 6-4	4	6
34	2020-01-24 04:41:23.509186+00	2020-01-24 04:41:23.509205+00	Секция 7-1	1	7
35	2020-01-24 04:41:23.509238+00	2020-01-24 04:41:23.509243+00	Секция 7-2	2	7
36	2020-01-24 04:41:23.509261+00	2020-01-24 04:41:23.509266+00	Секция 7-3	3	7
37	2020-01-24 04:41:23.509282+00	2020-01-24 04:41:23.509286+00	Секция 7-4	4	7
38	2020-01-24 04:41:23.560531+00	2020-01-24 04:41:23.560549+00	Секция 11-1	1	11
\.


--
-- Data for Name: locations_sowandpigletscell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowandpigletscell (id, created_at, modified_at, number, section_id, workshop_id) FROM stdin;
1	2020-01-24 04:41:22.984869+00	2020-01-24 04:41:22.984887+00	1	6	3
2	2020-01-24 04:41:22.984923+00	2020-01-24 04:41:22.984928+00	2	6	3
3	2020-01-24 04:41:22.984948+00	2020-01-24 04:41:22.984952+00	3	6	3
4	2020-01-24 04:41:22.984971+00	2020-01-24 04:41:22.984976+00	4	6	3
5	2020-01-24 04:41:22.984994+00	2020-01-24 04:41:22.984999+00	5	6	3
6	2020-01-24 04:41:22.985017+00	2020-01-24 04:41:22.985022+00	6	6	3
7	2020-01-24 04:41:22.98504+00	2020-01-24 04:41:22.985045+00	7	6	3
8	2020-01-24 04:41:22.985063+00	2020-01-24 04:41:22.985068+00	8	6	3
9	2020-01-24 04:41:22.985087+00	2020-01-24 04:41:22.985092+00	9	6	3
10	2020-01-24 04:41:22.98511+00	2020-01-24 04:41:22.985115+00	10	6	3
11	2020-01-24 04:41:22.985133+00	2020-01-24 04:41:22.985138+00	11	6	3
12	2020-01-24 04:41:22.985157+00	2020-01-24 04:41:22.985162+00	12	6	3
13	2020-01-24 04:41:22.98518+00	2020-01-24 04:41:22.985184+00	13	6	3
14	2020-01-24 04:41:22.985202+00	2020-01-24 04:41:22.985207+00	14	6	3
15	2020-01-24 04:41:22.985225+00	2020-01-24 04:41:22.98523+00	15	6	3
16	2020-01-24 04:41:22.985249+00	2020-01-24 04:41:22.985254+00	16	6	3
17	2020-01-24 04:41:22.985283+00	2020-01-24 04:41:22.985289+00	17	6	3
18	2020-01-24 04:41:22.985307+00	2020-01-24 04:41:22.985312+00	18	6	3
19	2020-01-24 04:41:22.985331+00	2020-01-24 04:41:22.985335+00	19	6	3
20	2020-01-24 04:41:22.985354+00	2020-01-24 04:41:22.985359+00	20	6	3
21	2020-01-24 04:41:22.985378+00	2020-01-24 04:41:22.985383+00	21	6	3
22	2020-01-24 04:41:22.985401+00	2020-01-24 04:41:22.985406+00	22	6	3
23	2020-01-24 04:41:22.985424+00	2020-01-24 04:41:22.985429+00	23	6	3
24	2020-01-24 04:41:22.985447+00	2020-01-24 04:41:22.985452+00	24	6	3
25	2020-01-24 04:41:22.98547+00	2020-01-24 04:41:22.985475+00	25	6	3
26	2020-01-24 04:41:22.985494+00	2020-01-24 04:41:22.985498+00	26	6	3
27	2020-01-24 04:41:22.985517+00	2020-01-24 04:41:22.985522+00	27	6	3
28	2020-01-24 04:41:22.985541+00	2020-01-24 04:41:22.985545+00	28	6	3
29	2020-01-24 04:41:22.985564+00	2020-01-24 04:41:22.985569+00	29	6	3
30	2020-01-24 04:41:22.985587+00	2020-01-24 04:41:22.985592+00	30	6	3
31	2020-01-24 04:41:22.98561+00	2020-01-24 04:41:22.985615+00	31	6	3
32	2020-01-24 04:41:22.985633+00	2020-01-24 04:41:22.985638+00	32	6	3
33	2020-01-24 04:41:22.985657+00	2020-01-24 04:41:22.985661+00	33	6	3
34	2020-01-24 04:41:22.98568+00	2020-01-24 04:41:22.985684+00	34	6	3
35	2020-01-24 04:41:22.985703+00	2020-01-24 04:41:22.985708+00	35	6	3
36	2020-01-24 04:41:22.985726+00	2020-01-24 04:41:22.985731+00	36	6	3
37	2020-01-24 04:41:22.985755+00	2020-01-24 04:41:22.985762+00	37	6	3
38	2020-01-24 04:41:22.985782+00	2020-01-24 04:41:22.985787+00	38	6	3
39	2020-01-24 04:41:22.985805+00	2020-01-24 04:41:22.98581+00	39	6	3
40	2020-01-24 04:41:22.985828+00	2020-01-24 04:41:22.985833+00	40	6	3
41	2020-01-24 04:41:22.985859+00	2020-01-24 04:41:22.985864+00	41	6	3
42	2020-01-24 04:41:22.985882+00	2020-01-24 04:41:22.985887+00	42	6	3
43	2020-01-24 04:41:22.985905+00	2020-01-24 04:41:22.98591+00	43	6	3
44	2020-01-24 04:41:22.985928+00	2020-01-24 04:41:22.985933+00	44	6	3
45	2020-01-24 04:41:22.985951+00	2020-01-24 04:41:22.985956+00	45	6	3
46	2020-01-24 04:41:23.009459+00	2020-01-24 04:41:23.00948+00	1	7	3
47	2020-01-24 04:41:23.00952+00	2020-01-24 04:41:23.009526+00	2	7	3
48	2020-01-24 04:41:23.009545+00	2020-01-24 04:41:23.00955+00	3	7	3
49	2020-01-24 04:41:23.009568+00	2020-01-24 04:41:23.009573+00	4	7	3
50	2020-01-24 04:41:23.009591+00	2020-01-24 04:41:23.009596+00	5	7	3
51	2020-01-24 04:41:23.009614+00	2020-01-24 04:41:23.009619+00	6	7	3
52	2020-01-24 04:41:23.009637+00	2020-01-24 04:41:23.009642+00	7	7	3
53	2020-01-24 04:41:23.00966+00	2020-01-24 04:41:23.009665+00	8	7	3
54	2020-01-24 04:41:23.009683+00	2020-01-24 04:41:23.009687+00	9	7	3
55	2020-01-24 04:41:23.009705+00	2020-01-24 04:41:23.00971+00	10	7	3
56	2020-01-24 04:41:23.009728+00	2020-01-24 04:41:23.009733+00	11	7	3
57	2020-01-24 04:41:23.009752+00	2020-01-24 04:41:23.009756+00	12	7	3
58	2020-01-24 04:41:23.009774+00	2020-01-24 04:41:23.009779+00	13	7	3
59	2020-01-24 04:41:23.009808+00	2020-01-24 04:41:23.009813+00	14	7	3
60	2020-01-24 04:41:23.009831+00	2020-01-24 04:41:23.009836+00	15	7	3
61	2020-01-24 04:41:23.009854+00	2020-01-24 04:41:23.009859+00	16	7	3
62	2020-01-24 04:41:23.009877+00	2020-01-24 04:41:23.009881+00	17	7	3
63	2020-01-24 04:41:23.0099+00	2020-01-24 04:41:23.009904+00	18	7	3
64	2020-01-24 04:41:23.009922+00	2020-01-24 04:41:23.009927+00	19	7	3
65	2020-01-24 04:41:23.009945+00	2020-01-24 04:41:23.00995+00	20	7	3
66	2020-01-24 04:41:23.009967+00	2020-01-24 04:41:23.009972+00	21	7	3
67	2020-01-24 04:41:23.00999+00	2020-01-24 04:41:23.009995+00	22	7	3
68	2020-01-24 04:41:23.010013+00	2020-01-24 04:41:23.010018+00	23	7	3
69	2020-01-24 04:41:23.010045+00	2020-01-24 04:41:23.010051+00	24	7	3
70	2020-01-24 04:41:23.010069+00	2020-01-24 04:41:23.010074+00	25	7	3
71	2020-01-24 04:41:23.010092+00	2020-01-24 04:41:23.010097+00	26	7	3
72	2020-01-24 04:41:23.010115+00	2020-01-24 04:41:23.01012+00	27	7	3
73	2020-01-24 04:41:23.010138+00	2020-01-24 04:41:23.010143+00	28	7	3
74	2020-01-24 04:41:23.010161+00	2020-01-24 04:41:23.010166+00	29	7	3
75	2020-01-24 04:41:23.010193+00	2020-01-24 04:41:23.010198+00	30	7	3
76	2020-01-24 04:41:23.010216+00	2020-01-24 04:41:23.010221+00	31	7	3
77	2020-01-24 04:41:23.010239+00	2020-01-24 04:41:23.010243+00	32	7	3
78	2020-01-24 04:41:23.010261+00	2020-01-24 04:41:23.010266+00	33	7	3
79	2020-01-24 04:41:23.010284+00	2020-01-24 04:41:23.010288+00	34	7	3
80	2020-01-24 04:41:23.010306+00	2020-01-24 04:41:23.010311+00	35	7	3
81	2020-01-24 04:41:23.010328+00	2020-01-24 04:41:23.010333+00	36	7	3
82	2020-01-24 04:41:23.010356+00	2020-01-24 04:41:23.010363+00	37	7	3
83	2020-01-24 04:41:23.010383+00	2020-01-24 04:41:23.010388+00	38	7	3
84	2020-01-24 04:41:23.010406+00	2020-01-24 04:41:23.010411+00	39	7	3
85	2020-01-24 04:41:23.010429+00	2020-01-24 04:41:23.010433+00	40	7	3
86	2020-01-24 04:41:23.010451+00	2020-01-24 04:41:23.010456+00	41	7	3
87	2020-01-24 04:41:23.010474+00	2020-01-24 04:41:23.010479+00	42	7	3
88	2020-01-24 04:41:23.010497+00	2020-01-24 04:41:23.010501+00	43	7	3
89	2020-01-24 04:41:23.010519+00	2020-01-24 04:41:23.010524+00	44	7	3
90	2020-01-24 04:41:23.010542+00	2020-01-24 04:41:23.010547+00	45	7	3
91	2020-01-24 04:41:23.029931+00	2020-01-24 04:41:23.02995+00	1	8	3
92	2020-01-24 04:41:23.02999+00	2020-01-24 04:41:23.029996+00	2	8	3
93	2020-01-24 04:41:23.030015+00	2020-01-24 04:41:23.03002+00	3	8	3
94	2020-01-24 04:41:23.030038+00	2020-01-24 04:41:23.030043+00	4	8	3
95	2020-01-24 04:41:23.030061+00	2020-01-24 04:41:23.030066+00	5	8	3
96	2020-01-24 04:41:23.030084+00	2020-01-24 04:41:23.030089+00	6	8	3
97	2020-01-24 04:41:23.030107+00	2020-01-24 04:41:23.030112+00	7	8	3
98	2020-01-24 04:41:23.03013+00	2020-01-24 04:41:23.030135+00	8	8	3
99	2020-01-24 04:41:23.030153+00	2020-01-24 04:41:23.030158+00	9	8	3
100	2020-01-24 04:41:23.030176+00	2020-01-24 04:41:23.030181+00	10	8	3
101	2020-01-24 04:41:23.030208+00	2020-01-24 04:41:23.030214+00	11	8	3
102	2020-01-24 04:41:23.030232+00	2020-01-24 04:41:23.030237+00	12	8	3
103	2020-01-24 04:41:23.030255+00	2020-01-24 04:41:23.03026+00	13	8	3
104	2020-01-24 04:41:23.030278+00	2020-01-24 04:41:23.030283+00	14	8	3
105	2020-01-24 04:41:23.030301+00	2020-01-24 04:41:23.030306+00	15	8	3
106	2020-01-24 04:41:23.030324+00	2020-01-24 04:41:23.030329+00	16	8	3
107	2020-01-24 04:41:23.030347+00	2020-01-24 04:41:23.030352+00	17	8	3
108	2020-01-24 04:41:23.03037+00	2020-01-24 04:41:23.030375+00	18	8	3
109	2020-01-24 04:41:23.030394+00	2020-01-24 04:41:23.030399+00	19	8	3
110	2020-01-24 04:41:23.030417+00	2020-01-24 04:41:23.030422+00	20	8	3
111	2020-01-24 04:41:23.03044+00	2020-01-24 04:41:23.030445+00	21	8	3
112	2020-01-24 04:41:23.030463+00	2020-01-24 04:41:23.030468+00	22	8	3
113	2020-01-24 04:41:23.030521+00	2020-01-24 04:41:23.030527+00	23	8	3
114	2020-01-24 04:41:23.030547+00	2020-01-24 04:41:23.030552+00	24	8	3
115	2020-01-24 04:41:23.030571+00	2020-01-24 04:41:23.030576+00	25	8	3
116	2020-01-24 04:41:23.030594+00	2020-01-24 04:41:23.0306+00	26	8	3
117	2020-01-24 04:41:23.030618+00	2020-01-24 04:41:23.030623+00	27	8	3
118	2020-01-24 04:41:23.030642+00	2020-01-24 04:41:23.030646+00	28	8	3
119	2020-01-24 04:41:23.030665+00	2020-01-24 04:41:23.03067+00	29	8	3
120	2020-01-24 04:41:23.030688+00	2020-01-24 04:41:23.030693+00	30	8	3
121	2020-01-24 04:41:23.030712+00	2020-01-24 04:41:23.030717+00	31	8	3
122	2020-01-24 04:41:23.030735+00	2020-01-24 04:41:23.03074+00	32	8	3
123	2020-01-24 04:41:23.030758+00	2020-01-24 04:41:23.030763+00	33	8	3
124	2020-01-24 04:41:23.030782+00	2020-01-24 04:41:23.030787+00	34	8	3
125	2020-01-24 04:41:23.030805+00	2020-01-24 04:41:23.03081+00	35	8	3
126	2020-01-24 04:41:23.030828+00	2020-01-24 04:41:23.030833+00	36	8	3
127	2020-01-24 04:41:23.030858+00	2020-01-24 04:41:23.030865+00	37	8	3
128	2020-01-24 04:41:23.030886+00	2020-01-24 04:41:23.030891+00	38	8	3
129	2020-01-24 04:41:23.03091+00	2020-01-24 04:41:23.030915+00	39	8	3
130	2020-01-24 04:41:23.030933+00	2020-01-24 04:41:23.030938+00	40	8	3
131	2020-01-24 04:41:23.030964+00	2020-01-24 04:41:23.03098+00	41	8	3
132	2020-01-24 04:41:23.031+00	2020-01-24 04:41:23.031004+00	42	8	3
133	2020-01-24 04:41:23.031032+00	2020-01-24 04:41:23.031037+00	43	8	3
134	2020-01-24 04:41:23.031056+00	2020-01-24 04:41:23.031061+00	44	8	3
135	2020-01-24 04:41:23.031079+00	2020-01-24 04:41:23.031084+00	45	8	3
136	2020-01-24 04:41:23.051563+00	2020-01-24 04:41:23.051589+00	1	9	3
137	2020-01-24 04:41:23.051629+00	2020-01-24 04:41:23.051635+00	2	9	3
138	2020-01-24 04:41:23.051654+00	2020-01-24 04:41:23.051659+00	3	9	3
139	2020-01-24 04:41:23.051678+00	2020-01-24 04:41:23.051683+00	4	9	3
140	2020-01-24 04:41:23.051701+00	2020-01-24 04:41:23.051705+00	5	9	3
141	2020-01-24 04:41:23.051724+00	2020-01-24 04:41:23.051728+00	6	9	3
142	2020-01-24 04:41:23.051746+00	2020-01-24 04:41:23.051751+00	7	9	3
143	2020-01-24 04:41:23.051769+00	2020-01-24 04:41:23.051774+00	8	9	3
144	2020-01-24 04:41:23.051792+00	2020-01-24 04:41:23.051797+00	9	9	3
145	2020-01-24 04:41:23.051815+00	2020-01-24 04:41:23.05182+00	10	9	3
146	2020-01-24 04:41:23.051838+00	2020-01-24 04:41:23.051843+00	11	9	3
147	2020-01-24 04:41:23.051861+00	2020-01-24 04:41:23.051866+00	12	9	3
148	2020-01-24 04:41:23.051891+00	2020-01-24 04:41:23.051897+00	13	9	3
149	2020-01-24 04:41:23.051917+00	2020-01-24 04:41:23.051922+00	14	9	3
150	2020-01-24 04:41:23.05194+00	2020-01-24 04:41:23.051945+00	15	9	3
151	2020-01-24 04:41:23.051963+00	2020-01-24 04:41:23.051968+00	16	9	3
152	2020-01-24 04:41:23.051986+00	2020-01-24 04:41:23.05199+00	17	9	3
153	2020-01-24 04:41:23.052008+00	2020-01-24 04:41:23.052013+00	18	9	3
154	2020-01-24 04:41:23.052031+00	2020-01-24 04:41:23.052036+00	19	9	3
155	2020-01-24 04:41:23.052054+00	2020-01-24 04:41:23.052059+00	20	9	3
156	2020-01-24 04:41:23.052077+00	2020-01-24 04:41:23.052082+00	21	9	3
157	2020-01-24 04:41:23.0521+00	2020-01-24 04:41:23.052104+00	22	9	3
158	2020-01-24 04:41:23.05215+00	2020-01-24 04:41:23.052156+00	23	9	3
159	2020-01-24 04:41:23.052175+00	2020-01-24 04:41:23.05218+00	24	9	3
160	2020-01-24 04:41:23.052198+00	2020-01-24 04:41:23.052203+00	25	9	3
161	2020-01-24 04:41:23.052221+00	2020-01-24 04:41:23.052226+00	26	9	3
162	2020-01-24 04:41:23.052244+00	2020-01-24 04:41:23.052249+00	27	9	3
163	2020-01-24 04:41:23.052267+00	2020-01-24 04:41:23.052272+00	28	9	3
164	2020-01-24 04:41:23.05229+00	2020-01-24 04:41:23.052295+00	29	9	3
165	2020-01-24 04:41:23.052313+00	2020-01-24 04:41:23.052317+00	30	9	3
166	2020-01-24 04:41:23.052336+00	2020-01-24 04:41:23.052341+00	31	9	3
167	2020-01-24 04:41:23.052358+00	2020-01-24 04:41:23.052363+00	32	9	3
168	2020-01-24 04:41:23.052381+00	2020-01-24 04:41:23.052386+00	33	9	3
169	2020-01-24 04:41:23.052404+00	2020-01-24 04:41:23.052408+00	34	9	3
170	2020-01-24 04:41:23.052427+00	2020-01-24 04:41:23.052431+00	35	9	3
171	2020-01-24 04:41:23.052449+00	2020-01-24 04:41:23.052454+00	36	9	3
172	2020-01-24 04:41:23.052484+00	2020-01-24 04:41:23.052491+00	37	9	3
173	2020-01-24 04:41:23.052511+00	2020-01-24 04:41:23.052516+00	38	9	3
174	2020-01-24 04:41:23.052534+00	2020-01-24 04:41:23.052539+00	39	9	3
175	2020-01-24 04:41:23.052557+00	2020-01-24 04:41:23.052562+00	40	9	3
176	2020-01-24 04:41:23.05258+00	2020-01-24 04:41:23.052585+00	41	9	3
177	2020-01-24 04:41:23.052603+00	2020-01-24 04:41:23.052608+00	42	9	3
178	2020-01-24 04:41:23.052626+00	2020-01-24 04:41:23.052631+00	43	9	3
179	2020-01-24 04:41:23.052648+00	2020-01-24 04:41:23.052653+00	44	9	3
180	2020-01-24 04:41:23.052671+00	2020-01-24 04:41:23.052676+00	45	9	3
181	2020-01-24 04:41:23.082311+00	2020-01-24 04:41:23.082333+00	1	10	3
182	2020-01-24 04:41:23.082376+00	2020-01-24 04:41:23.082382+00	2	10	3
183	2020-01-24 04:41:23.082401+00	2020-01-24 04:41:23.082406+00	3	10	3
184	2020-01-24 04:41:23.082424+00	2020-01-24 04:41:23.082429+00	4	10	3
185	2020-01-24 04:41:23.082447+00	2020-01-24 04:41:23.082452+00	5	10	3
186	2020-01-24 04:41:23.082471+00	2020-01-24 04:41:23.082475+00	6	10	3
187	2020-01-24 04:41:23.082494+00	2020-01-24 04:41:23.082499+00	7	10	3
188	2020-01-24 04:41:23.082525+00	2020-01-24 04:41:23.082531+00	8	10	3
189	2020-01-24 04:41:23.082935+00	2020-01-24 04:41:23.082945+00	9	10	3
190	2020-01-24 04:41:23.083322+00	2020-01-24 04:41:23.083329+00	10	10	3
191	2020-01-24 04:41:23.083351+00	2020-01-24 04:41:23.083356+00	11	10	3
192	2020-01-24 04:41:23.083375+00	2020-01-24 04:41:23.083388+00	12	10	3
193	2020-01-24 04:41:23.083409+00	2020-01-24 04:41:23.083414+00	13	10	3
194	2020-01-24 04:41:23.083433+00	2020-01-24 04:41:23.083437+00	14	10	3
195	2020-01-24 04:41:23.083456+00	2020-01-24 04:41:23.083461+00	15	10	3
196	2020-01-24 04:41:23.083479+00	2020-01-24 04:41:23.083484+00	16	10	3
197	2020-01-24 04:41:23.083502+00	2020-01-24 04:41:23.083507+00	17	10	3
198	2020-01-24 04:41:23.083525+00	2020-01-24 04:41:23.08353+00	18	10	3
199	2020-01-24 04:41:23.083548+00	2020-01-24 04:41:23.083553+00	19	10	3
200	2020-01-24 04:41:23.083571+00	2020-01-24 04:41:23.083576+00	20	10	3
201	2020-01-24 04:41:23.083594+00	2020-01-24 04:41:23.083599+00	21	10	3
202	2020-01-24 04:41:23.083618+00	2020-01-24 04:41:23.083622+00	22	10	3
203	2020-01-24 04:41:23.083641+00	2020-01-24 04:41:23.083646+00	23	10	3
204	2020-01-24 04:41:23.083664+00	2020-01-24 04:41:23.083668+00	24	10	3
205	2020-01-24 04:41:23.083687+00	2020-01-24 04:41:23.083692+00	25	10	3
206	2020-01-24 04:41:23.083896+00	2020-01-24 04:41:23.083905+00	26	10	3
207	2020-01-24 04:41:23.083931+00	2020-01-24 04:41:23.083937+00	27	10	3
208	2020-01-24 04:41:23.083956+00	2020-01-24 04:41:23.083961+00	28	10	3
209	2020-01-24 04:41:23.08398+00	2020-01-24 04:41:23.083985+00	29	10	3
210	2020-01-24 04:41:23.084003+00	2020-01-24 04:41:23.084008+00	30	10	3
211	2020-01-24 04:41:23.084026+00	2020-01-24 04:41:23.084031+00	31	10	3
212	2020-01-24 04:41:23.084059+00	2020-01-24 04:41:23.084064+00	32	10	3
213	2020-01-24 04:41:23.084084+00	2020-01-24 04:41:23.084089+00	33	10	3
214	2020-01-24 04:41:23.084107+00	2020-01-24 04:41:23.084112+00	34	10	3
215	2020-01-24 04:41:23.084155+00	2020-01-24 04:41:23.084161+00	35	10	3
216	2020-01-24 04:41:23.084179+00	2020-01-24 04:41:23.084184+00	36	10	3
217	2020-01-24 04:41:23.084208+00	2020-01-24 04:41:23.084215+00	37	10	3
218	2020-01-24 04:41:23.084235+00	2020-01-24 04:41:23.08424+00	38	10	3
219	2020-01-24 04:41:23.084259+00	2020-01-24 04:41:23.084263+00	39	10	3
220	2020-01-24 04:41:23.084281+00	2020-01-24 04:41:23.084338+00	40	10	3
221	2020-01-24 04:41:23.084359+00	2020-01-24 04:41:23.084365+00	41	10	3
222	2020-01-24 04:41:23.084383+00	2020-01-24 04:41:23.084388+00	42	10	3
223	2020-01-24 04:41:23.084406+00	2020-01-24 04:41:23.084411+00	43	10	3
224	2020-01-24 04:41:23.084429+00	2020-01-24 04:41:23.084434+00	44	10	3
225	2020-01-24 04:41:23.084452+00	2020-01-24 04:41:23.084457+00	45	10	3
226	2020-01-24 04:41:23.101886+00	2020-01-24 04:41:23.101907+00	1	11	3
227	2020-01-24 04:41:23.101947+00	2020-01-24 04:41:23.101953+00	2	11	3
228	2020-01-24 04:41:23.101993+00	2020-01-24 04:41:23.101999+00	3	11	3
229	2020-01-24 04:41:23.102017+00	2020-01-24 04:41:23.102022+00	4	11	3
230	2020-01-24 04:41:23.10204+00	2020-01-24 04:41:23.102045+00	5	11	3
231	2020-01-24 04:41:23.102063+00	2020-01-24 04:41:23.102068+00	6	11	3
232	2020-01-24 04:41:23.102086+00	2020-01-24 04:41:23.102091+00	7	11	3
233	2020-01-24 04:41:23.102109+00	2020-01-24 04:41:23.102113+00	8	11	3
234	2020-01-24 04:41:23.102179+00	2020-01-24 04:41:23.102185+00	9	11	3
235	2020-01-24 04:41:23.102204+00	2020-01-24 04:41:23.102209+00	10	11	3
236	2020-01-24 04:41:23.102227+00	2020-01-24 04:41:23.102232+00	11	11	3
237	2020-01-24 04:41:23.10225+00	2020-01-24 04:41:23.102255+00	12	11	3
238	2020-01-24 04:41:23.102273+00	2020-01-24 04:41:23.102277+00	13	11	3
239	2020-01-24 04:41:23.102295+00	2020-01-24 04:41:23.1023+00	14	11	3
240	2020-01-24 04:41:23.102327+00	2020-01-24 04:41:23.102332+00	15	11	3
241	2020-01-24 04:41:23.10235+00	2020-01-24 04:41:23.102355+00	16	11	3
242	2020-01-24 04:41:23.102373+00	2020-01-24 04:41:23.102378+00	17	11	3
243	2020-01-24 04:41:23.102396+00	2020-01-24 04:41:23.102401+00	18	11	3
244	2020-01-24 04:41:23.102419+00	2020-01-24 04:41:23.102596+00	19	11	3
245	2020-01-24 04:41:23.102631+00	2020-01-24 04:41:23.102637+00	20	11	3
246	2020-01-24 04:41:23.102656+00	2020-01-24 04:41:23.102661+00	21	11	3
247	2020-01-24 04:41:23.102679+00	2020-01-24 04:41:23.102684+00	22	11	3
248	2020-01-24 04:41:23.102762+00	2020-01-24 04:41:23.102777+00	23	11	3
249	2020-01-24 04:41:23.10281+00	2020-01-24 04:41:23.102815+00	24	11	3
250	2020-01-24 04:41:23.102834+00	2020-01-24 04:41:23.102839+00	25	11	3
251	2020-01-24 04:41:23.102857+00	2020-01-24 04:41:23.102862+00	26	11	3
252	2020-01-24 04:41:23.1029+00	2020-01-24 04:41:23.102907+00	27	11	3
253	2020-01-24 04:41:23.102927+00	2020-01-24 04:41:23.102932+00	28	11	3
254	2020-01-24 04:41:23.10295+00	2020-01-24 04:41:23.102955+00	29	11	3
255	2020-01-24 04:41:23.102982+00	2020-01-24 04:41:23.102988+00	30	11	3
256	2020-01-24 04:41:23.103007+00	2020-01-24 04:41:23.103011+00	31	11	3
257	2020-01-24 04:41:23.10303+00	2020-01-24 04:41:23.103035+00	32	11	3
258	2020-01-24 04:41:23.103053+00	2020-01-24 04:41:23.103058+00	33	11	3
259	2020-01-24 04:41:23.103084+00	2020-01-24 04:41:23.103089+00	34	11	3
260	2020-01-24 04:41:23.103108+00	2020-01-24 04:41:23.103113+00	35	11	3
261	2020-01-24 04:41:23.103131+00	2020-01-24 04:41:23.103136+00	36	11	3
262	2020-01-24 04:41:23.10316+00	2020-01-24 04:41:23.103167+00	37	11	3
263	2020-01-24 04:41:23.103187+00	2020-01-24 04:41:23.103192+00	38	11	3
264	2020-01-24 04:41:23.10321+00	2020-01-24 04:41:23.103215+00	39	11	3
265	2020-01-24 04:41:23.103234+00	2020-01-24 04:41:23.103239+00	40	11	3
266	2020-01-24 04:41:23.103257+00	2020-01-24 04:41:23.103262+00	41	11	3
267	2020-01-24 04:41:23.10328+00	2020-01-24 04:41:23.103285+00	42	11	3
268	2020-01-24 04:41:23.103304+00	2020-01-24 04:41:23.103309+00	43	11	3
269	2020-01-24 04:41:23.103327+00	2020-01-24 04:41:23.103332+00	44	11	3
270	2020-01-24 04:41:23.10335+00	2020-01-24 04:41:23.103355+00	45	11	3
\.


--
-- Data for Name: locations_sowgroupcell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowgroupcell (id, created_at, modified_at, number, sows_quantity, section_id, workshop_id) FROM stdin;
\.


--
-- Data for Name: locations_sowgroupcell_sows; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowgroupcell_sows (id, sowgroupcell_id, sow_id) FROM stdin;
\.


--
-- Data for Name: locations_sowsinglecell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowsinglecell (id, created_at, modified_at, number, section_id, workshop_id) FROM stdin;
\.


--
-- Data for Name: locations_workshop; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_workshop (id, created_at, modified_at, number, title) FROM stdin;
1	2020-01-24 04:41:22.924152+00	2020-01-24 04:41:22.924183+00	1	Цех 1 Осеменение
2	2020-01-24 04:41:22.924204+00	2020-01-24 04:41:22.924209+00	2	Цех 2 Ожидание родов
3	2020-01-24 04:41:22.92422+00	2020-01-24 04:41:22.924225+00	3	Цех 3 Маточник
4	2020-01-24 04:41:22.924235+00	2020-01-24 04:41:22.924245+00	4	Цех 4 Доращивание 4
5	2020-01-24 04:41:22.924326+00	2020-01-24 04:41:22.924336+00	5	Цех 5 Откорм 5
6	2020-01-24 04:41:22.924348+00	2020-01-24 04:41:22.924353+00	6	Цех 6 Откорм 6
7	2020-01-24 04:41:22.924363+00	2020-01-24 04:41:22.924368+00	7	Цех 7 Откорм 7
8	2020-01-24 04:41:22.924378+00	2020-01-24 04:41:22.924382+00	8	Цех 8 Доращивание 8
9	2020-01-24 04:41:22.924392+00	2020-01-24 04:41:22.924397+00	9	Цех 9 Убойный цех
10	2020-01-24 04:41:22.924407+00	2020-01-24 04:41:22.924412+00	10	Цех 10 Крематорий
11	2020-01-24 04:41:22.924422+00	2020-01-24 04:41:22.924426+00	11	Цех 7-5 Ремонтные
\.


--
-- Data for Name: piglets_events_cullingpiglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_cullingpiglets (id, created_at, modified_at, date, culling_type, reason, is_it_gilt, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_pigletsmerger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_pigletsmerger (id, created_at, modified_at, date, created_piglets_id, initiator_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_pigletssplit; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_pigletssplit (id, created_at, modified_at, date, initiator_id, parent_piglets_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_weighingpiglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_weighingpiglets (id, created_at, modified_at, date, total_weight, average_weight, piglets_quantity, place, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_piglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_piglets (id, created_at, modified_at, start_quantity, quantity, gilts_quantity, transfer_part_number, active, location_id, merger_as_parent_id, split_as_child_id, status_id) FROM stdin;
\.


--
-- Data for Name: piglets_pigletsstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_pigletsstatus (id, created_at, modified_at, title) FROM stdin;
1	2020-01-24 04:41:23.603799+00	2020-01-24 04:41:23.60382+00	Родились, кормятся
2	2020-01-24 04:41:23.603831+00	2020-01-24 04:41:23.603836+00	Готовы ко взвешиванию
3	2020-01-24 04:41:23.603844+00	2020-01-24 04:41:23.603849+00	Взвешены, готовы к заселению
4	2020-01-24 04:41:23.603856+00	2020-01-24 04:41:23.603861+00	Кормятся
5	2020-01-24 04:41:23.603868+00	2020-01-24 04:41:23.603873+00	Объединены с другой группой
\.


--
-- Data for Name: sows_boar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_boar (id, created_at, modified_at, birth_id, location_id) FROM stdin;
1	2020-01-24 04:41:26.303394+00	2020-01-24 04:41:26.303411+00	1	1
2	2020-01-24 04:41:26.30999+00	2020-01-24 04:41:26.310006+00	2	1
3	2020-01-24 04:43:05.494438+00	2020-01-24 04:43:05.494457+00	020	1
4	2020-01-24 04:43:05.502111+00	2020-01-24 04:43:05.502128+00	022	1
5	2020-01-24 04:43:06.019506+00	2020-01-24 04:43:06.019524+00	021	1
6	2020-01-24 04:43:07.360356+00	2020-01-24 04:43:07.360376+00	019	1
7	2020-01-24 04:43:07.45346+00	2020-01-24 04:43:07.453478+00	417	1
8	2020-01-24 04:43:07.530705+00	2020-01-24 04:43:07.530723+00	018	1
9	2020-01-24 04:43:07.88418+00	2020-01-24 04:43:07.884197+00	216	1
10	2020-01-24 04:43:10.171654+00	2020-01-24 04:43:10.17167+00	017	1
11	2020-01-24 04:43:12.117799+00	2020-01-24 04:43:12.117815+00	011	1
12	2020-01-24 04:43:17.140852+00	2020-01-24 04:43:17.14087+00	416	1
\.


--
-- Data for Name: sows_events_abortionsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_abortionsow (id, created_at, modified_at, date, initiator_id, sow_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_events_cullingsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_cullingsow (id, created_at, modified_at, date, culling_type, reason, initiator_id, sow_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_events_semination; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_semination (id, created_at, modified_at, date, boar_id, initiator_id, semination_employee_id, sow_id, tour_id) FROM stdin;
1	2020-01-24 04:43:05.520972+00	2020-01-24 04:43:05.52099+00	2019-09-16 16:00:00+00	3	\N	5	1	1
2	2020-01-24 04:43:05.535998+00	2020-01-24 04:43:05.536021+00	2019-09-16 16:00:00+00	4	\N	5	1	1
3	2020-01-24 04:43:05.615848+00	2020-01-24 04:43:05.615866+00	2019-09-16 16:00:00+00	3	\N	6	2	1
4	2020-01-24 04:43:05.632555+00	2020-01-24 04:43:05.632575+00	2019-09-16 16:00:00+00	4	\N	6	2	1
5	2020-01-24 04:43:05.71193+00	2020-01-24 04:43:05.711949+00	2019-09-16 16:00:00+00	3	\N	6	3	1
6	2020-01-24 04:43:05.72463+00	2020-01-24 04:43:05.724648+00	2019-09-16 16:00:00+00	4	\N	6	3	1
7	2020-01-24 04:43:05.788295+00	2020-01-24 04:43:05.788312+00	2019-09-16 16:00:00+00	3	\N	5	4	1
8	2020-01-24 04:43:05.800325+00	2020-01-24 04:43:05.800344+00	2019-09-16 16:00:00+00	4	\N	5	4	1
9	2020-01-24 04:43:05.854236+00	2020-01-24 04:43:05.854255+00	2019-09-16 16:00:00+00	3	\N	5	5	1
10	2020-01-24 04:43:05.866179+00	2020-01-24 04:43:05.866193+00	2019-09-16 16:00:00+00	4	\N	5	5	1
11	2020-01-24 04:43:05.929105+00	2020-01-24 04:43:05.929122+00	2019-09-16 16:00:00+00	3	\N	4	6	1
12	2020-01-24 04:43:05.942263+00	2020-01-24 04:43:05.942279+00	2019-09-16 16:00:00+00	4	\N	4	6	1
13	2020-01-24 04:43:06.031988+00	2020-01-24 04:43:06.032004+00	2019-09-17 16:00:00+00	4	\N	5	7	1
14	2020-01-24 04:43:06.047404+00	2020-01-24 04:43:06.047422+00	2019-09-17 16:00:00+00	5	\N	5	7	1
15	2020-01-24 04:43:06.115759+00	2020-01-24 04:43:06.115777+00	2019-09-17 16:00:00+00	4	\N	5	8	1
16	2020-01-24 04:43:06.127792+00	2020-01-24 04:43:06.127807+00	2019-09-17 16:00:00+00	4	\N	5	8	1
17	2020-01-24 04:43:06.188788+00	2020-01-24 04:43:06.188807+00	2019-09-17 16:00:00+00	4	\N	4	9	1
18	2020-01-24 04:43:06.203575+00	2020-01-24 04:43:06.203589+00	2019-09-17 16:00:00+00	5	\N	4	9	1
19	2020-01-24 04:43:06.274766+00	2020-01-24 04:43:06.274785+00	2019-09-17 16:00:00+00	4	\N	4	10	1
20	2020-01-24 04:43:06.288461+00	2020-01-24 04:43:06.288477+00	2019-09-17 16:00:00+00	4	\N	4	10	1
21	2020-01-24 04:43:06.345737+00	2020-01-24 04:43:06.345756+00	2019-09-17 16:00:00+00	4	\N	6	11	1
22	2020-01-24 04:43:06.357488+00	2020-01-24 04:43:06.357504+00	2019-09-17 16:00:00+00	5	\N	6	11	1
23	2020-01-24 04:43:06.420946+00	2020-01-24 04:43:06.420964+00	2019-09-17 16:00:00+00	5	\N	4	12	1
24	2020-01-24 04:43:06.432822+00	2020-01-24 04:43:06.432838+00	2019-09-17 16:00:00+00	4	\N	4	12	1
25	2020-01-24 04:43:06.495386+00	2020-01-24 04:43:06.495405+00	2019-09-17 16:00:00+00	4	\N	4	13	1
26	2020-01-24 04:43:06.509467+00	2020-01-24 04:43:06.509484+00	2019-09-17 16:00:00+00	4	\N	4	13	1
27	2020-01-24 04:43:06.584145+00	2020-01-24 04:43:06.584168+00	2019-09-18 16:00:00+00	4	\N	8	14	1
28	2020-01-24 04:43:06.601704+00	2020-01-24 04:43:06.601723+00	2019-09-18 16:00:00+00	5	\N	8	14	1
29	2020-01-24 04:43:06.653973+00	2020-01-24 04:43:06.653997+00	2019-09-18 16:00:00+00	4	\N	6	15	1
30	2020-01-24 04:43:06.665645+00	2020-01-24 04:43:06.665666+00	2019-09-18 16:00:00+00	5	\N	6	15	1
31	2020-01-24 04:43:06.741731+00	2020-01-24 04:43:06.741751+00	2019-09-18 16:00:00+00	5	\N	6	16	1
32	2020-01-24 04:43:06.754382+00	2020-01-24 04:43:06.7544+00	2019-09-18 16:00:00+00	5	\N	6	16	1
33	2020-01-24 04:43:06.833838+00	2020-01-24 04:43:06.833857+00	2019-09-18 16:00:00+00	5	\N	6	17	1
34	2020-01-24 04:43:06.842279+00	2020-01-24 04:43:06.842291+00	2019-09-18 16:00:00+00	5	\N	6	17	1
35	2020-01-24 04:43:06.898003+00	2020-01-24 04:43:06.898025+00	2019-09-18 16:00:00+00	4	\N	6	18	1
36	2020-01-24 04:43:06.906319+00	2020-01-24 04:43:06.906333+00	2019-09-18 16:00:00+00	5	\N	6	18	1
37	2020-01-24 04:43:06.966862+00	2020-01-24 04:43:06.966881+00	2019-09-18 16:00:00+00	4	\N	4	19	1
38	2020-01-24 04:43:06.980492+00	2020-01-24 04:43:06.980507+00	2019-09-18 16:00:00+00	5	\N	4	19	1
39	2020-01-24 04:43:07.033702+00	2020-01-24 04:43:07.033721+00	2019-09-19 16:00:00+00	5	\N	5	20	1
40	2020-01-24 04:43:07.042055+00	2020-01-24 04:43:07.042068+00	2019-09-19 16:00:00+00	5	\N	5	20	1
41	2020-01-24 04:43:07.131228+00	2020-01-24 04:43:07.131249+00	2019-09-19 16:00:00+00	5	\N	5	21	1
42	2020-01-24 04:43:07.144961+00	2020-01-24 04:43:07.144976+00	2019-09-19 16:00:00+00	5	\N	5	21	1
43	2020-01-24 04:43:07.228296+00	2020-01-24 04:43:07.228315+00	2019-09-19 16:00:00+00	5	\N	8	22	1
44	2020-01-24 04:43:07.24129+00	2020-01-24 04:43:07.241306+00	2019-09-19 16:00:00+00	5	\N	8	22	1
45	2020-01-24 04:43:07.299936+00	2020-01-24 04:43:07.299956+00	2019-09-19 16:00:00+00	5	\N	5	23	1
46	2020-01-24 04:43:07.309645+00	2020-01-24 04:43:07.309658+00	2019-09-19 16:00:00+00	5	\N	5	23	1
47	2020-01-24 04:43:07.370655+00	2020-01-24 04:43:07.370673+00	2019-09-20 16:00:00+00	5	\N	5	24	1
48	2020-01-24 04:43:07.386131+00	2020-01-24 04:43:07.386153+00	2019-09-20 16:00:00+00	6	\N	5	24	1
49	2020-01-24 04:43:07.466039+00	2020-01-24 04:43:07.466057+00	2019-09-22 16:00:00+00	7	\N	4	25	2
50	2020-01-24 04:43:07.4769+00	2020-01-24 04:43:07.476915+00	2019-09-22 16:00:00+00	7	\N	4	25	2
51	2020-01-24 04:43:07.542922+00	2020-01-24 04:43:07.542942+00	2019-09-22 16:00:00+00	8	\N	4	26	2
52	2020-01-24 04:43:07.558269+00	2020-01-24 04:43:07.558321+00	2019-09-22 16:00:00+00	4	\N	4	26	2
53	2020-01-24 04:43:07.642468+00	2020-01-24 04:43:07.642486+00	2019-09-22 16:00:00+00	6	\N	5	27	2
54	2020-01-24 04:43:07.652668+00	2020-01-24 04:43:07.652684+00	2019-09-22 16:00:00+00	6	\N	5	27	2
55	2020-01-24 04:43:07.710457+00	2020-01-24 04:43:07.710475+00	2019-09-22 16:00:00+00	8	\N	8	28	2
56	2020-01-24 04:43:07.718051+00	2020-01-24 04:43:07.718062+00	2019-09-22 16:00:00+00	4	\N	8	28	2
57	2020-01-24 04:43:07.766387+00	2020-01-24 04:43:07.766405+00	2019-09-22 16:00:00+00	6	\N	6	29	2
58	2020-01-24 04:43:07.778839+00	2020-01-24 04:43:07.778855+00	2019-09-22 16:00:00+00	8	\N	6	29	2
59	2020-01-24 04:43:07.841386+00	2020-01-24 04:43:07.841404+00	2019-09-22 16:00:00+00	6	\N	6	30	2
60	2020-01-24 04:43:07.849593+00	2020-01-24 04:43:07.849608+00	2019-09-22 16:00:00+00	8	\N	6	30	2
61	2020-01-24 04:43:07.893848+00	2020-01-24 04:43:07.893866+00	2019-09-22 16:00:00+00	8	\N	6	31	2
62	2020-01-24 04:43:07.923604+00	2020-01-24 04:43:07.923903+00	2019-09-22 16:00:00+00	9	\N	6	31	2
63	2020-01-24 04:43:08.027408+00	2020-01-24 04:43:08.027431+00	2019-09-22 16:00:00+00	6	\N	4	32	2
64	2020-01-24 04:43:08.043889+00	2020-01-24 04:43:08.043911+00	2019-09-22 16:00:00+00	8	\N	4	32	2
65	2020-01-24 04:43:08.140064+00	2020-01-24 04:43:08.140085+00	2019-09-22 16:00:00+00	6	\N	6	33	2
66	2020-01-24 04:43:08.149521+00	2020-01-24 04:43:08.149534+00	2019-09-22 16:00:00+00	8	\N	6	33	2
67	2020-01-24 04:43:08.187902+00	2020-01-24 04:43:08.187921+00	2019-09-22 16:00:00+00	7	\N	4	34	2
68	2020-01-24 04:43:08.208329+00	2020-01-24 04:43:08.208349+00	2019-09-22 16:00:00+00	7	\N	4	34	2
69	2020-01-24 04:43:08.277484+00	2020-01-24 04:43:08.277503+00	2019-09-22 16:00:00+00	6	\N	8	35	2
70	2020-01-24 04:43:08.291094+00	2020-01-24 04:43:08.291116+00	2019-09-22 16:00:00+00	8	\N	8	35	2
71	2020-01-24 04:43:08.341008+00	2020-01-24 04:43:08.341026+00	2019-09-22 16:00:00+00	6	\N	4	36	2
72	2020-01-24 04:43:08.348331+00	2020-01-24 04:43:08.348343+00	2019-09-22 16:00:00+00	3	\N	4	36	2
73	2020-01-24 04:43:08.404503+00	2020-01-24 04:43:08.404523+00	2019-09-22 16:00:00+00	8	\N	4	37	2
74	2020-01-24 04:43:08.433388+00	2020-01-24 04:43:08.433403+00	2019-09-22 16:00:00+00	8	\N	4	37	2
75	2020-01-24 04:43:08.504941+00	2020-01-24 04:43:08.504959+00	2019-09-22 16:00:00+00	6	\N	4	38	2
76	2020-01-24 04:43:08.515872+00	2020-01-24 04:43:08.516115+00	2019-09-22 16:00:00+00	8	\N	4	38	2
77	2020-01-24 04:43:08.561865+00	2020-01-24 04:43:08.561883+00	2019-09-22 16:00:00+00	8	\N	8	39	2
78	2020-01-24 04:43:08.571389+00	2020-01-24 04:43:08.571404+00	2019-09-22 16:00:00+00	6	\N	8	39	2
79	2020-01-24 04:43:08.62797+00	2020-01-24 04:43:08.62799+00	2019-09-22 16:00:00+00	6	\N	6	40	2
80	2020-01-24 04:43:08.639984+00	2020-01-24 04:43:08.639998+00	2019-09-22 16:00:00+00	9	\N	6	40	2
81	2020-01-24 04:43:08.680535+00	2020-01-24 04:43:08.680552+00	2019-09-22 16:00:00+00	6	\N	5	41	2
82	2020-01-24 04:43:08.691435+00	2020-01-24 04:43:08.691549+00	2019-09-22 16:00:00+00	6	\N	5	41	2
83	2020-01-24 04:43:08.755474+00	2020-01-24 04:43:08.755493+00	2019-09-22 16:00:00+00	6	\N	8	42	2
84	2020-01-24 04:43:08.768802+00	2020-01-24 04:43:08.768817+00	2019-09-22 16:00:00+00	8	\N	8	42	2
85	2020-01-24 04:43:08.8481+00	2020-01-24 04:43:08.848135+00	2019-09-22 16:00:00+00	8	\N	8	43	2
86	2020-01-24 04:43:08.877318+00	2020-01-24 04:43:08.877597+00	2019-09-22 16:00:00+00	4	\N	8	43	2
87	2020-01-24 04:43:08.955061+00	2020-01-24 04:43:08.955089+00	2019-09-22 16:00:00+00	6	\N	5	44	2
88	2020-01-24 04:43:08.969206+00	2020-01-24 04:43:08.969224+00	2019-09-22 16:00:00+00	6	\N	5	44	2
89	2020-01-24 04:43:09.022717+00	2020-01-24 04:43:09.022735+00	2019-09-22 16:00:00+00	7	\N	6	45	2
90	2020-01-24 04:43:09.032744+00	2020-01-24 04:43:09.032759+00	2019-09-22 16:00:00+00	7	\N	6	45	2
91	2020-01-24 04:43:09.075523+00	2020-01-24 04:43:09.075542+00	2019-09-22 16:00:00+00	8	\N	8	46	2
92	2020-01-24 04:43:09.087403+00	2020-01-24 04:43:09.087418+00	2019-09-22 16:00:00+00	4	\N	8	46	2
93	2020-01-24 04:43:09.14993+00	2020-01-24 04:43:09.149948+00	2019-09-22 16:00:00+00	6	\N	6	47	2
94	2020-01-24 04:43:09.162606+00	2020-01-24 04:43:09.162619+00	2019-09-22 16:00:00+00	8	\N	6	47	2
95	2020-01-24 04:43:09.201792+00	2020-01-24 04:43:09.201809+00	2019-09-22 16:00:00+00	6	\N	8	48	2
96	2020-01-24 04:43:09.208724+00	2020-01-24 04:43:09.208736+00	2019-09-22 16:00:00+00	9	\N	8	48	2
97	2020-01-24 04:43:09.272217+00	2020-01-24 04:43:09.272235+00	2019-09-22 16:00:00+00	8	\N	6	49	2
98	2020-01-24 04:43:09.285867+00	2020-01-24 04:43:09.285882+00	2019-09-22 16:00:00+00	4	\N	6	49	2
99	2020-01-24 04:43:09.344089+00	2020-01-24 04:43:09.344107+00	2019-09-22 16:00:00+00	6	\N	8	50	2
100	2020-01-24 04:43:09.35552+00	2020-01-24 04:43:09.355533+00	2019-09-22 16:00:00+00	8	\N	8	50	2
101	2020-01-24 04:43:09.412914+00	2020-01-24 04:43:09.412932+00	2019-09-22 16:00:00+00	6	\N	6	51	2
102	2020-01-24 04:43:09.428773+00	2020-01-24 04:43:09.42881+00	2019-09-22 16:00:00+00	8	\N	6	51	2
103	2020-01-24 04:43:09.479431+00	2020-01-24 04:43:09.47945+00	2019-09-22 16:00:00+00	8	\N	8	52	2
104	2020-01-24 04:43:09.498223+00	2020-01-24 04:43:09.49824+00	2019-09-22 16:00:00+00	9	\N	8	52	2
105	2020-01-24 04:43:09.554776+00	2020-01-24 04:43:09.554794+00	2019-09-22 16:00:00+00	6	\N	4	53	2
106	2020-01-24 04:43:09.566946+00	2020-01-24 04:43:09.566962+00	2019-09-22 16:00:00+00	8	\N	4	53	2
107	2020-01-24 04:43:09.62178+00	2020-01-24 04:43:09.621798+00	2019-09-22 16:00:00+00	6	\N	8	54	2
108	2020-01-24 04:43:09.634807+00	2020-01-24 04:43:09.634824+00	2019-09-22 16:00:00+00	3	\N	8	54	2
109	2020-01-24 04:43:09.69463+00	2020-01-24 04:43:09.694649+00	2019-09-22 16:00:00+00	6	\N	4	55	2
110	2020-01-24 04:43:09.707256+00	2020-01-24 04:43:09.707272+00	2019-09-22 16:00:00+00	9	\N	4	55	2
111	2020-01-24 04:43:09.765755+00	2020-01-24 04:43:09.765774+00	2019-09-22 16:00:00+00	8	\N	8	56	2
112	2020-01-24 04:43:09.77661+00	2020-01-24 04:43:09.776623+00	2019-09-22 16:00:00+00	9	\N	8	56	2
113	2020-01-24 04:43:09.820778+00	2020-01-24 04:43:09.820796+00	2019-09-22 16:00:00+00	8	\N	4	57	2
114	2020-01-24 04:43:09.833849+00	2020-01-24 04:43:09.833866+00	2019-09-22 16:00:00+00	4	\N	4	57	2
115	2020-01-24 04:43:09.897409+00	2020-01-24 04:43:09.897427+00	2019-09-22 16:00:00+00	6	\N	6	58	2
116	2020-01-24 04:43:09.911094+00	2020-01-24 04:43:09.911112+00	2019-09-22 16:00:00+00	6	\N	6	58	2
117	2020-01-24 04:43:09.965983+00	2020-01-24 04:43:09.966002+00	2019-09-22 16:00:00+00	6	\N	6	59	2
118	2020-01-24 04:43:09.97443+00	2020-01-24 04:43:09.974446+00	2019-09-22 16:00:00+00	8	\N	6	59	2
119	2020-01-24 04:43:10.023224+00	2020-01-24 04:43:10.023242+00	2019-09-22 16:00:00+00	6	\N	8	60	2
120	2020-01-24 04:43:10.03712+00	2020-01-24 04:43:10.037137+00	2019-09-22 16:00:00+00	9	\N	8	60	2
121	2020-01-24 04:43:10.094109+00	2020-01-24 04:43:10.094128+00	2019-09-22 16:00:00+00	7	\N	6	61	2
122	2020-01-24 04:43:10.106099+00	2020-01-24 04:43:10.106111+00	2019-09-22 16:00:00+00	7	\N	6	61	2
123	2020-01-24 04:43:10.18133+00	2020-01-24 04:43:10.181346+00	2019-09-24 16:00:00+00	4	\N	6	62	2
124	2020-01-24 04:43:10.193568+00	2020-01-24 04:43:10.193583+00	2019-09-24 16:00:00+00	10	\N	6	62	2
125	2020-01-24 04:43:10.251845+00	2020-01-24 04:43:10.251864+00	2019-09-24 16:00:00+00	3	\N	6	63	2
126	2020-01-24 04:43:10.264143+00	2020-01-24 04:43:10.264159+00	2019-09-24 16:00:00+00	4	\N	6	63	2
127	2020-01-24 04:43:10.321678+00	2020-01-24 04:43:10.321697+00	2019-09-24 16:00:00+00	4	\N	6	64	2
128	2020-01-24 04:43:10.334484+00	2020-01-24 04:43:10.3345+00	2019-09-24 16:00:00+00	10	\N	6	64	2
129	2020-01-24 04:43:10.403531+00	2020-01-24 04:43:10.403549+00	2019-09-24 16:00:00+00	4	\N	6	65	2
130	2020-01-24 04:43:10.416593+00	2020-01-24 04:43:10.416607+00	2019-09-24 16:00:00+00	10	\N	6	65	2
131	2020-01-24 04:43:10.479854+00	2020-01-24 04:43:10.479872+00	2019-09-24 16:00:00+00	4	\N	4	66	2
132	2020-01-24 04:43:10.49323+00	2020-01-24 04:43:10.493247+00	2019-09-24 16:00:00+00	3	\N	4	66	2
133	2020-01-24 04:43:10.551055+00	2020-01-24 04:43:10.551086+00	2019-09-24 16:00:00+00	3	\N	5	67	2
134	2020-01-24 04:43:10.560852+00	2020-01-24 04:43:10.560867+00	2019-09-24 16:00:00+00	10	\N	5	67	2
135	2020-01-24 04:43:10.618794+00	2020-01-24 04:43:10.618811+00	2019-09-24 16:00:00+00	4	\N	6	68	2
136	2020-01-24 04:43:10.63177+00	2020-01-24 04:43:10.631797+00	2019-09-24 16:00:00+00	3	\N	6	68	2
137	2020-01-24 04:43:10.694448+00	2020-01-24 04:43:10.694467+00	2019-09-24 16:00:00+00	4	\N	4	69	2
138	2020-01-24 04:43:10.706862+00	2020-01-24 04:43:10.706876+00	2019-09-24 16:00:00+00	3	\N	4	69	2
139	2020-01-24 04:43:10.768754+00	2020-01-24 04:43:10.768773+00	2019-09-25 16:00:00+00	10	\N	6	70	2
140	2020-01-24 04:43:10.777858+00	2020-01-24 04:43:10.77787+00	2019-09-25 16:00:00+00	3	\N	6	70	2
141	2020-01-24 04:43:10.835047+00	2020-01-24 04:43:10.835065+00	2019-09-25 16:00:00+00	10	\N	4	71	2
142	2020-01-24 04:43:10.848418+00	2020-01-24 04:43:10.848431+00	2019-09-25 16:00:00+00	3	\N	4	71	2
143	2020-01-24 04:43:10.90396+00	2020-01-24 04:43:10.903979+00	2019-09-25 16:00:00+00	10	\N	8	72	2
144	2020-01-24 04:43:10.920585+00	2020-01-24 04:43:10.920604+00	2019-09-25 16:00:00+00	3	\N	8	72	2
145	2020-01-24 04:43:10.974085+00	2020-01-24 04:43:10.974102+00	2019-09-25 16:00:00+00	10	\N	8	73	2
146	2020-01-24 04:43:10.986071+00	2020-01-24 04:43:10.986086+00	2019-09-25 16:00:00+00	3	\N	8	73	2
147	2020-01-24 04:43:11.039394+00	2020-01-24 04:43:11.039412+00	2019-09-25 16:00:00+00	10	\N	6	74	2
148	2020-01-24 04:43:11.050562+00	2020-01-24 04:43:11.050577+00	2019-09-25 16:00:00+00	3	\N	6	74	2
149	2020-01-24 04:43:11.111579+00	2020-01-24 04:43:11.111598+00	2019-09-25 16:00:00+00	5	\N	8	75	2
150	2020-01-24 04:43:11.124257+00	2020-01-24 04:43:11.124271+00	2019-09-25 16:00:00+00	3	\N	8	75	2
151	2020-01-24 04:43:11.182404+00	2020-01-24 04:43:11.182423+00	2019-09-26 16:00:00+00	3	\N	8	76	2
152	2020-01-24 04:43:11.191124+00	2020-01-24 04:43:11.191136+00	2019-09-26 16:00:00+00	10	\N	8	76	2
153	2020-01-24 04:43:11.239255+00	2020-01-24 04:43:11.239273+00	2019-09-26 16:00:00+00	3	\N	8	77	2
154	2020-01-24 04:43:11.251366+00	2020-01-24 04:43:11.251381+00	2019-09-26 16:00:00+00	10	\N	8	77	2
155	2020-01-24 04:43:11.307917+00	2020-01-24 04:43:11.307935+00	2019-09-26 16:00:00+00	3	\N	5	78	2
156	2020-01-24 04:43:11.317595+00	2020-01-24 04:43:11.317607+00	2019-09-26 16:00:00+00	10	\N	5	78	2
157	2020-01-24 04:43:11.354315+00	2020-01-24 04:43:11.354333+00	2019-09-26 16:00:00+00	3	\N	5	79	2
158	2020-01-24 04:43:11.3631+00	2020-01-24 04:43:11.363113+00	2019-09-26 16:00:00+00	10	\N	5	79	2
159	2020-01-24 04:43:11.413184+00	2020-01-24 04:43:11.413202+00	2019-09-26 16:00:00+00	3	\N	5	80	2
160	2020-01-24 04:43:11.426074+00	2020-01-24 04:43:11.426094+00	2019-09-26 16:00:00+00	10	\N	5	80	2
161	2020-01-24 04:43:11.502399+00	2020-01-24 04:43:11.50242+00	2019-09-26 16:00:00+00	3	\N	6	81	2
162	2020-01-24 04:43:11.51425+00	2020-01-24 04:43:11.514273+00	2019-09-26 16:00:00+00	10	\N	6	81	2
163	2020-01-24 04:43:11.554414+00	2020-01-24 04:43:11.554433+00	2019-09-27 16:00:00+00	4	\N	6	82	2
164	2020-01-24 04:43:11.577954+00	2020-01-24 04:43:11.577979+00	2019-09-27 16:00:00+00	3	\N	6	82	2
165	2020-01-24 04:43:11.631295+00	2020-01-24 04:43:11.631313+00	2019-09-27 16:00:00+00	3	\N	6	83	2
166	2020-01-24 04:43:11.643899+00	2020-01-24 04:43:11.643915+00	2019-09-27 16:00:00+00	3	\N	6	83	2
167	2020-01-24 04:43:11.707742+00	2020-01-24 04:43:11.707761+00	2019-09-27 16:00:00+00	5	\N	5	84	2
168	2020-01-24 04:43:11.718186+00	2020-01-24 04:43:11.7182+00	2019-09-27 16:00:00+00	3	\N	5	84	2
169	2020-01-24 04:43:11.759735+00	2020-01-24 04:43:11.759754+00	2019-09-27 16:00:00+00	4	\N	6	85	2
170	2020-01-24 04:43:11.768138+00	2020-01-24 04:43:11.768156+00	2019-09-27 16:00:00+00	3	\N	6	85	2
171	2020-01-24 04:43:11.851033+00	2020-01-24 04:43:11.851052+00	2019-09-27 16:00:00+00	10	\N	5	86	2
172	2020-01-24 04:43:11.86504+00	2020-01-24 04:43:11.865056+00	2019-09-27 16:00:00+00	3	\N	5	86	2
173	2020-01-24 04:43:11.918132+00	2020-01-24 04:43:11.91815+00	2019-09-27 16:00:00+00	3	\N	6	87	2
174	2020-01-24 04:43:11.926029+00	2020-01-24 04:43:11.926041+00	2019-09-27 16:00:00+00	3	\N	6	87	2
175	2020-01-24 04:43:11.971204+00	2020-01-24 04:43:11.971225+00	2019-09-28 16:00:00+00	6	\N	6	88	2
176	2020-01-24 04:43:11.980518+00	2020-01-24 04:43:11.980531+00	2019-09-28 16:00:00+00	8	\N	6	88	2
177	2020-01-24 04:43:12.048149+00	2020-01-24 04:43:12.048169+00	2019-09-28 16:00:00+00	7	\N	6	89	2
178	2020-01-24 04:43:12.06057+00	2020-01-24 04:43:12.060588+00	2019-09-28 16:00:00+00	7	\N	6	89	2
179	2020-01-24 04:43:12.127871+00	2020-01-24 04:43:12.127888+00	2019-09-29 16:00:00+00	6	\N	5	90	3
180	2020-01-24 04:43:12.135918+00	2020-01-24 04:43:12.135929+00	2019-09-29 16:00:00+00	11	\N	5	90	3
181	2020-01-24 04:43:12.192992+00	2020-01-24 04:43:12.193012+00	2019-09-29 16:00:00+00	6	\N	8	91	3
182	2020-01-24 04:43:12.21012+00	2020-01-24 04:43:12.210135+00	2019-09-29 16:00:00+00	11	\N	8	91	3
183	2020-01-24 04:43:12.262574+00	2020-01-24 04:43:12.262593+00	2019-09-29 16:00:00+00	8	\N	4	92	3
184	2020-01-24 04:43:12.284185+00	2020-01-24 04:43:12.2842+00	2019-09-29 16:00:00+00	10	\N	4	92	3
185	2020-01-24 04:43:12.345015+00	2020-01-24 04:43:12.345036+00	2019-09-29 16:00:00+00	8	\N	5	93	3
186	2020-01-24 04:43:12.353155+00	2020-01-24 04:43:12.353167+00	2019-09-29 16:00:00+00	10	\N	5	93	3
187	2020-01-24 04:43:12.41519+00	2020-01-24 04:43:12.415209+00	2019-09-29 16:00:00+00	8	\N	6	94	3
188	2020-01-24 04:43:12.423861+00	2020-01-24 04:43:12.423875+00	2019-09-29 16:00:00+00	10	\N	6	94	3
189	2020-01-24 04:43:12.493106+00	2020-01-24 04:43:12.493128+00	2019-09-29 16:00:00+00	8	\N	4	95	3
190	2020-01-24 04:43:12.506564+00	2020-01-24 04:43:12.506582+00	2019-09-29 16:00:00+00	10	\N	4	95	3
191	2020-01-24 04:43:12.566234+00	2020-01-24 04:43:12.566254+00	2019-09-29 16:00:00+00	8	\N	6	96	3
192	2020-01-24 04:43:12.587375+00	2020-01-24 04:43:12.587391+00	2019-09-29 16:00:00+00	10	\N	6	96	3
193	2020-01-24 04:43:12.635975+00	2020-01-24 04:43:12.635993+00	2019-09-29 16:00:00+00	8	\N	6	97	3
194	2020-01-24 04:43:12.648192+00	2020-01-24 04:43:12.648205+00	2019-09-29 16:00:00+00	8	\N	6	97	3
195	2020-01-24 04:43:12.716848+00	2020-01-24 04:43:12.716867+00	2019-09-29 16:00:00+00	8	\N	8	98	3
196	2020-01-24 04:43:12.726904+00	2020-01-24 04:43:12.726924+00	2019-09-29 16:00:00+00	10	\N	8	98	3
197	2020-01-24 04:43:12.773728+00	2020-01-24 04:43:12.773744+00	2019-09-29 16:00:00+00	6	\N	7	99	3
198	2020-01-24 04:43:12.784264+00	2020-01-24 04:43:12.784277+00	2019-09-29 16:00:00+00	10	\N	7	99	3
199	2020-01-24 04:43:12.826329+00	2020-01-24 04:43:12.826348+00	2019-09-29 16:00:00+00	6	\N	6	100	3
200	2020-01-24 04:43:12.845759+00	2020-01-24 04:43:12.845778+00	2019-09-29 16:00:00+00	11	\N	6	100	3
201	2020-01-24 04:43:12.89154+00	2020-01-24 04:43:12.891559+00	2019-09-29 16:00:00+00	6	\N	8	101	3
202	2020-01-24 04:43:12.902869+00	2020-01-24 04:43:12.902883+00	2019-09-29 16:00:00+00	11	\N	8	101	3
203	2020-01-24 04:43:12.956897+00	2020-01-24 04:43:12.956916+00	2019-09-29 16:00:00+00	6	\N	6	102	3
204	2020-01-24 04:43:12.969004+00	2020-01-24 04:43:12.969018+00	2019-09-29 16:00:00+00	11	\N	6	102	3
205	2020-01-24 04:43:13.018743+00	2020-01-24 04:43:13.01876+00	2019-09-29 16:00:00+00	6	\N	6	103	3
206	2020-01-24 04:43:13.02654+00	2020-01-24 04:43:13.026552+00	2019-09-29 16:00:00+00	11	\N	6	103	3
207	2020-01-24 04:43:13.068837+00	2020-01-24 04:43:13.068855+00	2019-09-29 16:00:00+00	6	\N	6	104	3
208	2020-01-24 04:43:13.082633+00	2020-01-24 04:43:13.082645+00	2019-09-29 16:00:00+00	11	\N	6	104	3
209	2020-01-24 04:43:13.136469+00	2020-01-24 04:43:13.136486+00	2019-09-29 16:00:00+00	6	\N	4	105	3
210	2020-01-24 04:43:13.147232+00	2020-01-24 04:43:13.147247+00	2019-09-29 16:00:00+00	10	\N	4	105	3
211	2020-01-24 04:43:13.190891+00	2020-01-24 04:43:13.190909+00	2019-09-29 16:00:00+00	6	\N	4	106	3
212	2020-01-24 04:43:13.203022+00	2020-01-24 04:43:13.203035+00	2019-09-29 16:00:00+00	11	\N	4	106	3
213	2020-01-24 04:43:13.242928+00	2020-01-24 04:43:13.242948+00	2019-09-29 16:00:00+00	8	\N	5	107	3
214	2020-01-24 04:43:13.251423+00	2020-01-24 04:43:13.251435+00	2019-09-29 16:00:00+00	10	\N	5	107	3
215	2020-01-24 04:43:13.3092+00	2020-01-24 04:43:13.309218+00	2019-09-29 16:00:00+00	6	\N	4	108	3
216	2020-01-24 04:43:13.321177+00	2020-01-24 04:43:13.32119+00	2019-09-29 16:00:00+00	11	\N	4	108	3
217	2020-01-24 04:43:13.379686+00	2020-01-24 04:43:13.379705+00	2019-09-29 16:00:00+00	6	\N	4	109	3
218	2020-01-24 04:43:13.39252+00	2020-01-24 04:43:13.392537+00	2019-09-29 16:00:00+00	10	\N	4	109	3
219	2020-01-24 04:43:13.451601+00	2020-01-24 04:43:13.451618+00	2019-09-29 16:00:00+00	6	\N	5	110	3
220	2020-01-24 04:43:13.462135+00	2020-01-24 04:43:13.462151+00	2019-09-29 16:00:00+00	11	\N	5	110	3
221	2020-01-24 04:43:13.518042+00	2020-01-24 04:43:13.518062+00	2019-09-29 16:00:00+00	6	\N	4	111	3
222	2020-01-24 04:43:13.534026+00	2020-01-24 04:43:13.534048+00	2019-09-29 16:00:00+00	11	\N	4	111	3
223	2020-01-24 04:43:13.602842+00	2020-01-24 04:43:13.602862+00	2019-09-29 16:00:00+00	7	\N	5	112	3
224	2020-01-24 04:43:13.61629+00	2020-01-24 04:43:13.616305+00	2019-09-29 16:00:00+00	7	\N	5	112	3
225	2020-01-24 04:43:13.67424+00	2020-01-24 04:43:13.67427+00	2019-09-29 16:00:00+00	6	\N	5	113	3
226	2020-01-24 04:43:13.683808+00	2020-01-24 04:43:13.683822+00	2019-09-29 16:00:00+00	11	\N	5	113	3
227	2020-01-24 04:43:13.734309+00	2020-01-24 04:43:13.734327+00	2019-09-29 16:00:00+00	8	\N	6	114	3
228	2020-01-24 04:43:13.744133+00	2020-01-24 04:43:13.744147+00	2019-09-29 16:00:00+00	10	\N	6	114	3
229	2020-01-24 04:43:13.801765+00	2020-01-24 04:43:13.801784+00	2019-09-29 16:00:00+00	6	\N	5	115	3
230	2020-01-24 04:43:13.811161+00	2020-01-24 04:43:13.811173+00	2019-09-29 16:00:00+00	10	\N	5	115	3
231	2020-01-24 04:43:13.855046+00	2020-01-24 04:43:13.855064+00	2019-09-29 16:00:00+00	7	\N	8	116	3
232	2020-01-24 04:43:13.863867+00	2020-01-24 04:43:13.86388+00	2019-09-29 16:00:00+00	7	\N	8	116	3
233	2020-01-24 04:43:13.921262+00	2020-01-24 04:43:13.921281+00	2019-09-29 16:00:00+00	8	\N	5	117	3
234	2020-01-24 04:43:13.934341+00	2020-01-24 04:43:13.934356+00	2019-09-29 16:00:00+00	10	\N	5	117	3
235	2020-01-24 04:43:13.981713+00	2020-01-24 04:43:13.981732+00	2019-09-29 16:00:00+00	6	\N	5	118	3
236	2020-01-24 04:43:13.991636+00	2020-01-24 04:43:13.991653+00	2019-09-29 16:00:00+00	11	\N	5	118	3
237	2020-01-24 04:43:14.042056+00	2020-01-24 04:43:14.042074+00	2019-09-29 16:00:00+00	6	\N	5	119	3
238	2020-01-24 04:43:14.054346+00	2020-01-24 04:43:14.054359+00	2019-09-29 16:00:00+00	11	\N	5	119	3
239	2020-01-24 04:43:14.117358+00	2020-01-24 04:43:14.117377+00	2019-09-29 16:00:00+00	8	\N	5	120	3
240	2020-01-24 04:43:14.128307+00	2020-01-24 04:43:14.12832+00	2019-09-29 16:00:00+00	10	\N	5	120	3
241	2020-01-24 04:43:14.187038+00	2020-01-24 04:43:14.187056+00	2019-09-29 16:00:00+00	6	\N	6	121	3
242	2020-01-24 04:43:14.199748+00	2020-01-24 04:43:14.199762+00	2019-09-29 16:00:00+00	10	\N	6	121	3
243	2020-01-24 04:43:14.261804+00	2020-01-24 04:43:14.261824+00	2019-09-29 16:00:00+00	8	\N	7	122	3
244	2020-01-24 04:43:14.280318+00	2020-01-24 04:43:14.280339+00	2019-09-29 16:00:00+00	10	\N	7	122	3
245	2020-01-24 04:43:14.347334+00	2020-01-24 04:43:14.347353+00	2019-09-29 16:00:00+00	6	\N	5	123	3
246	2020-01-24 04:43:14.358+00	2020-01-24 04:43:14.358013+00	2019-09-29 16:00:00+00	11	\N	5	123	3
247	2020-01-24 04:43:14.418013+00	2020-01-24 04:43:14.418032+00	2019-09-29 16:00:00+00	6	\N	4	124	3
248	2020-01-24 04:43:14.428485+00	2020-01-24 04:43:14.428497+00	2019-09-29 16:00:00+00	11	\N	4	124	3
249	2020-01-24 04:43:14.476286+00	2020-01-24 04:43:14.476305+00	2019-09-29 16:00:00+00	6	\N	6	125	3
250	2020-01-24 04:43:14.487047+00	2020-01-24 04:43:14.487063+00	2019-09-29 16:00:00+00	11	\N	6	125	3
251	2020-01-24 04:43:14.549487+00	2020-01-24 04:43:14.549505+00	2019-09-29 16:00:00+00	6	\N	6	126	3
252	2020-01-24 04:43:14.557146+00	2020-01-24 04:43:14.55716+00	2019-09-29 16:00:00+00	11	\N	6	126	3
253	2020-01-24 04:43:14.60889+00	2020-01-24 04:43:14.608909+00	2019-09-29 16:00:00+00	8	\N	4	127	3
254	2020-01-24 04:43:14.615757+00	2020-01-24 04:43:14.615769+00	2019-09-29 16:00:00+00	10	\N	4	127	3
255	2020-01-24 04:43:14.680404+00	2020-01-24 04:43:14.680424+00	2019-09-29 16:00:00+00	6	\N	8	128	3
256	2020-01-24 04:43:14.694323+00	2020-01-24 04:43:14.694347+00	2019-09-29 16:00:00+00	10	\N	8	128	3
257	2020-01-24 04:43:14.735994+00	2020-01-24 04:43:14.736011+00	2019-09-29 16:00:00+00	6	\N	6	129	3
258	2020-01-24 04:43:14.743445+00	2020-01-24 04:43:14.743462+00	2019-09-29 16:00:00+00	11	\N	6	129	3
259	2020-01-24 04:43:14.795325+00	2020-01-24 04:43:14.795343+00	2019-09-29 16:00:00+00	7	\N	6	130	3
260	2020-01-24 04:43:14.808974+00	2020-01-24 04:43:14.808989+00	2019-09-29 16:00:00+00	7	\N	6	130	3
261	2020-01-24 04:43:14.855062+00	2020-01-24 04:43:14.855089+00	2019-09-29 16:00:00+00	6	\N	6	131	3
262	2020-01-24 04:43:14.862721+00	2020-01-24 04:43:14.862732+00	2019-09-29 16:00:00+00	8	\N	6	131	3
263	2020-01-24 04:43:14.903837+00	2020-01-24 04:43:14.903855+00	2019-09-30 16:00:00+00	10	\N	4	132	3
264	2020-01-24 04:43:14.916238+00	2020-01-24 04:43:14.916254+00	2019-09-30 16:00:00+00	5	\N	4	132	3
265	2020-01-24 04:43:14.986869+00	2020-01-24 04:43:14.986888+00	2019-09-30 16:00:00+00	10	\N	6	133	3
266	2020-01-24 04:43:15.001136+00	2020-01-24 04:43:15.001153+00	2019-09-30 16:00:00+00	11	\N	6	133	3
267	2020-01-24 04:43:15.054839+00	2020-01-24 04:43:15.054857+00	2019-09-30 16:00:00+00	10	\N	5	134	3
268	2020-01-24 04:43:15.068077+00	2020-01-24 04:43:15.068098+00	2019-09-30 16:00:00+00	11	\N	5	134	3
269	2020-01-24 04:43:15.116202+00	2020-01-24 04:43:15.116222+00	2019-09-30 16:00:00+00	10	\N	4	135	3
270	2020-01-24 04:43:15.124629+00	2020-01-24 04:43:15.124641+00	2019-09-30 16:00:00+00	11	\N	4	135	3
271	2020-01-24 04:43:15.17143+00	2020-01-24 04:43:15.17145+00	2019-09-30 16:00:00+00	10	\N	4	136	3
272	2020-01-24 04:43:15.184173+00	2020-01-24 04:43:15.184188+00	2019-09-30 16:00:00+00	5	\N	4	136	3
273	2020-01-24 04:43:15.239757+00	2020-01-24 04:43:15.239774+00	2019-10-01 16:00:00+00	5	\N	6	137	3
274	2020-01-24 04:43:15.251786+00	2020-01-24 04:43:15.251802+00	2019-10-01 16:00:00+00	5	\N	6	137	3
275	2020-01-24 04:43:15.296795+00	2020-01-24 04:43:15.296814+00	2019-10-01 16:00:00+00	11	\N	5	138	3
276	2020-01-24 04:43:15.30512+00	2020-01-24 04:43:15.305132+00	2019-10-01 16:00:00+00	5	\N	5	138	3
277	2020-01-24 04:43:15.349865+00	2020-01-24 04:43:15.349885+00	2019-10-01 16:00:00+00	5	\N	6	139	3
278	2020-01-24 04:43:15.362589+00	2020-01-24 04:43:15.362605+00	2019-10-01 16:00:00+00	5	\N	6	139	3
279	2020-01-24 04:43:15.426123+00	2020-01-24 04:43:15.426142+00	2019-10-01 16:00:00+00	5	\N	5	140	3
280	2020-01-24 04:43:15.438119+00	2020-01-24 04:43:15.438133+00	2019-10-01 16:00:00+00	5	\N	5	140	3
281	2020-01-24 04:43:15.480383+00	2020-01-24 04:43:15.480401+00	2019-10-01 16:00:00+00	5	\N	6	141	3
282	2020-01-24 04:43:15.489247+00	2020-01-24 04:43:15.489262+00	2019-10-01 16:00:00+00	5	\N	6	141	3
283	2020-01-24 04:43:15.536585+00	2020-01-24 04:43:15.536604+00	2019-10-01 16:00:00+00	3	\N	8	142	3
284	2020-01-24 04:43:15.54773+00	2020-01-24 04:43:15.547744+00	2019-10-01 16:00:00+00	5	\N	8	142	3
285	2020-01-24 04:43:15.592532+00	2020-01-24 04:43:15.592551+00	2019-10-01 16:00:00+00	5	\N	4	143	3
286	2020-01-24 04:43:15.600508+00	2020-01-24 04:43:15.60052+00	2019-10-01 16:00:00+00	5	\N	4	143	3
287	2020-01-24 04:43:15.637842+00	2020-01-24 04:43:15.637859+00	2019-10-01 16:00:00+00	5	\N	6	144	3
288	2020-01-24 04:43:15.651666+00	2020-01-24 04:43:15.65168+00	2019-10-01 16:00:00+00	5	\N	6	144	3
289	2020-01-24 04:43:15.71409+00	2020-01-24 04:43:15.714114+00	2019-10-02 16:00:00+00	4	\N	8	145	3
290	2020-01-24 04:43:15.727321+00	2020-01-24 04:43:15.727337+00	2019-10-02 16:00:00+00	3	\N	8	145	3
291	2020-01-24 04:43:15.764534+00	2020-01-24 04:43:15.76455+00	2019-10-02 16:00:00+00	5	\N	6	146	3
292	2020-01-24 04:43:15.778617+00	2020-01-24 04:43:15.77863+00	2019-10-02 16:00:00+00	4	\N	6	146	3
293	2020-01-24 04:43:15.836907+00	2020-01-24 04:43:15.836924+00	2019-10-02 16:00:00+00	5	\N	6	147	3
294	2020-01-24 04:43:15.849267+00	2020-01-24 04:43:15.849279+00	2019-10-02 16:00:00+00	4	\N	6	147	3
295	2020-01-24 04:43:15.888475+00	2020-01-24 04:43:15.88849+00	2019-10-02 16:00:00+00	5	\N	8	148	3
296	2020-01-24 04:43:15.896177+00	2020-01-24 04:43:15.89619+00	2019-10-02 16:00:00+00	4	\N	8	148	3
297	2020-01-24 04:43:15.938646+00	2020-01-24 04:43:15.938665+00	2019-10-03 16:00:00+00	4	\N	8	149	3
298	2020-01-24 04:43:15.950706+00	2020-01-24 04:43:15.950718+00	2019-10-03 16:00:00+00	4	\N	8	149	3
299	2020-01-24 04:43:16.012747+00	2020-01-24 04:43:16.012765+00	2019-10-03 16:00:00+00	4	\N	5	150	3
300	2020-01-24 04:43:16.023411+00	2020-01-24 04:43:16.023424+00	2019-10-03 16:00:00+00	4	\N	5	150	3
301	2020-01-24 04:43:16.089628+00	2020-01-24 04:43:16.089646+00	2019-10-03 16:00:00+00	4	\N	5	151	3
302	2020-01-24 04:43:16.103706+00	2020-01-24 04:43:16.103721+00	2019-10-03 16:00:00+00	4	\N	5	151	3
303	2020-01-24 04:43:16.156787+00	2020-01-24 04:43:16.156805+00	2019-10-03 16:00:00+00	4	\N	5	152	3
304	2020-01-24 04:43:16.170585+00	2020-01-24 04:43:16.170602+00	2019-10-03 16:00:00+00	4	\N	5	152	3
305	2020-01-24 04:43:16.233279+00	2020-01-24 04:43:16.233297+00	2019-10-03 16:00:00+00	3	\N	5	153	3
306	2020-01-24 04:43:16.247449+00	2020-01-24 04:43:16.247465+00	2019-10-03 16:00:00+00	4	\N	5	153	3
307	2020-01-24 04:43:16.31182+00	2020-01-24 04:43:16.31184+00	2019-10-04 16:00:00+00	4	\N	8	154	3
308	2020-01-24 04:43:16.325396+00	2020-01-24 04:43:16.32541+00	2019-10-04 16:00:00+00	3	\N	8	154	3
309	2020-01-24 04:43:16.371494+00	2020-01-24 04:43:16.371513+00	2019-10-04 16:00:00+00	4	\N	6	155	3
310	2020-01-24 04:43:16.384731+00	2020-01-24 04:43:16.384746+00	2019-10-04 16:00:00+00	3	\N	6	155	3
311	2020-01-24 04:43:16.446276+00	2020-01-24 04:43:16.446294+00	2019-10-04 16:00:00+00	5	\N	5	156	3
312	2020-01-24 04:43:16.459749+00	2020-01-24 04:43:16.459764+00	2019-10-04 16:00:00+00	3	\N	5	156	3
313	2020-01-24 04:43:16.524416+00	2020-01-24 04:43:16.524434+00	2019-10-04 16:00:00+00	4	\N	5	157	3
314	2020-01-24 04:43:16.53436+00	2020-01-24 04:43:16.534372+00	2019-10-04 16:00:00+00	3	\N	5	157	3
315	2020-01-24 04:43:16.596329+00	2020-01-24 04:43:16.596348+00	2019-10-04 16:00:00+00	4	\N	5	158	3
316	2020-01-24 04:43:16.610338+00	2020-01-24 04:43:16.610353+00	2019-10-04 16:00:00+00	3	\N	5	158	3
317	2020-01-24 04:43:16.673912+00	2020-01-24 04:43:16.673931+00	2019-10-04 16:00:00+00	4	\N	8	159	3
318	2020-01-24 04:43:16.686761+00	2020-01-24 04:43:16.686774+00	2019-10-04 16:00:00+00	3	\N	8	159	3
319	2020-01-24 04:43:16.745417+00	2020-01-24 04:43:16.745436+00	2019-10-04 16:00:00+00	3	\N	6	160	3
320	2020-01-24 04:43:16.758974+00	2020-01-24 04:43:16.758992+00	2019-10-04 16:00:00+00	3	\N	6	160	3
321	2020-01-24 04:43:16.830663+00	2020-01-24 04:43:16.830682+00	2019-10-04 16:00:00+00	4	\N	6	161	3
322	2020-01-24 04:43:16.843224+00	2020-01-24 04:43:16.843241+00	2019-10-04 16:00:00+00	3	\N	6	161	3
323	2020-01-24 04:43:16.883675+00	2020-01-24 04:43:16.883694+00	2019-10-04 16:00:00+00	4	\N	5	162	3
324	2020-01-24 04:43:16.891859+00	2020-01-24 04:43:16.891872+00	2019-10-04 16:00:00+00	3	\N	5	162	3
325	2020-01-24 04:43:16.952585+00	2020-01-24 04:43:16.952603+00	2019-10-04 16:00:00+00	4	\N	5	163	3
326	2020-01-24 04:43:16.966576+00	2020-01-24 04:43:16.966591+00	2019-10-04 16:00:00+00	3	\N	5	163	3
327	2020-01-24 04:43:17.027786+00	2020-01-24 04:43:17.027804+00	2019-10-04 16:00:00+00	4	\N	8	164	3
328	2020-01-24 04:43:17.039388+00	2020-01-24 04:43:17.0394+00	2019-10-04 16:00:00+00	3	\N	8	164	3
329	2020-01-24 04:43:17.07618+00	2020-01-24 04:43:17.0762+00	2019-10-04 16:00:00+00	4	\N	6	165	3
330	2020-01-24 04:43:17.083348+00	2020-01-24 04:43:17.08336+00	2019-10-04 16:00:00+00	3	\N	6	165	3
331	2020-01-24 04:43:17.15332+00	2020-01-24 04:43:17.153337+00	2019-10-06 16:00:00+00	12	\N	5	166	4
332	2020-01-24 04:43:17.166408+00	2020-01-24 04:43:17.166426+00	2019-10-06 16:00:00+00	12	\N	5	166	4
333	2020-01-24 04:43:17.212498+00	2020-01-24 04:43:17.212516+00	2019-10-06 16:00:00+00	8	\N	4	167	4
334	2020-01-24 04:43:17.220002+00	2020-01-24 04:43:17.220015+00	2019-10-06 16:00:00+00	3	\N	4	167	4
335	2020-01-24 04:43:17.259589+00	2020-01-24 04:43:17.259607+00	2019-10-06 16:00:00+00	6	\N	6	168	4
336	2020-01-24 04:43:17.273626+00	2020-01-24 04:43:17.273643+00	2019-10-06 16:00:00+00	3	\N	6	168	4
337	2020-01-24 04:43:17.337492+00	2020-01-24 04:43:17.33751+00	2019-10-06 16:00:00+00	6	\N	6	169	4
338	2020-01-24 04:43:17.35007+00	2020-01-24 04:43:17.350086+00	2019-10-06 16:00:00+00	3	\N	6	169	4
339	2020-01-24 04:43:17.395403+00	2020-01-24 04:43:17.395421+00	2019-10-06 16:00:00+00	8	\N	4	170	4
340	2020-01-24 04:43:17.402681+00	2020-01-24 04:43:17.402693+00	2019-10-06 16:00:00+00	3	\N	4	170	4
341	2020-01-24 04:43:17.447928+00	2020-01-24 04:43:17.447947+00	2019-10-06 16:00:00+00	3	\N	6	171	4
342	2020-01-24 04:43:17.461201+00	2020-01-24 04:43:17.461216+00	2019-10-06 16:00:00+00	6	\N	6	171	4
343	2020-01-24 04:43:17.522905+00	2020-01-24 04:43:17.522923+00	2019-10-06 16:00:00+00	8	\N	6	172	4
344	2020-01-24 04:43:17.536005+00	2020-01-24 04:43:17.536017+00	2019-10-06 16:00:00+00	3	\N	6	172	4
345	2020-01-24 04:43:17.591537+00	2020-01-24 04:43:17.591555+00	2019-10-06 16:00:00+00	6	\N	6	173	4
346	2020-01-24 04:43:17.59928+00	2020-01-24 04:43:17.599297+00	2019-10-06 16:00:00+00	6	\N	6	173	4
347	2020-01-24 04:43:17.644329+00	2020-01-24 04:43:17.644347+00	2019-10-06 16:00:00+00	3	\N	5	174	4
348	2020-01-24 04:43:17.657643+00	2020-01-24 04:43:17.657661+00	2019-10-06 16:00:00+00	6	\N	5	174	4
349	2020-01-24 04:43:17.727376+00	2020-01-24 04:43:17.727395+00	2019-10-06 16:00:00+00	3	\N	5	175	4
350	2020-01-24 04:43:17.740999+00	2020-01-24 04:43:17.741025+00	2019-10-06 16:00:00+00	6	\N	5	175	4
351	2020-01-24 04:43:17.784704+00	2020-01-24 04:43:17.784721+00	2019-10-06 16:00:00+00	6	\N	8	176	4
352	2020-01-24 04:43:17.792515+00	2020-01-24 04:43:17.792528+00	2019-10-06 16:00:00+00	3	\N	8	176	4
353	2020-01-24 04:43:17.848516+00	2020-01-24 04:43:17.848535+00	2019-10-06 16:00:00+00	12	\N	6	177	4
354	2020-01-24 04:43:17.862252+00	2020-01-24 04:43:17.862268+00	2019-10-06 16:00:00+00	12	\N	6	177	4
355	2020-01-24 04:43:17.926385+00	2020-01-24 04:43:17.926403+00	2019-10-06 16:00:00+00	8	\N	4	178	4
356	2020-01-24 04:43:17.939919+00	2020-01-24 04:43:17.939934+00	2019-10-06 16:00:00+00	6	\N	4	178	4
357	2020-01-24 04:43:17.989952+00	2020-01-24 04:43:17.989972+00	2019-10-06 16:00:00+00	8	\N	6	179	4
358	2020-01-24 04:43:18.002459+00	2020-01-24 04:43:18.002474+00	2019-10-06 16:00:00+00	3	\N	6	179	4
359	2020-01-24 04:43:18.060159+00	2020-01-24 04:43:18.060177+00	2019-10-06 16:00:00+00	6	\N	4	180	4
360	2020-01-24 04:43:18.07309+00	2020-01-24 04:43:18.073107+00	2019-10-06 16:00:00+00	3	\N	4	180	4
361	2020-01-24 04:43:18.12968+00	2020-01-24 04:43:18.1297+00	2019-10-06 16:00:00+00	8	\N	4	181	4
362	2020-01-24 04:43:18.141762+00	2020-01-24 04:43:18.141779+00	2019-10-06 16:00:00+00	3	\N	4	181	4
363	2020-01-24 04:43:18.194861+00	2020-01-24 04:43:18.194878+00	2019-10-06 16:00:00+00	3	\N	6	182	4
364	2020-01-24 04:43:18.202462+00	2020-01-24 04:43:18.202473+00	2019-10-06 16:00:00+00	6	\N	6	182	4
365	2020-01-24 04:43:18.256658+00	2020-01-24 04:43:18.256677+00	2019-10-06 16:00:00+00	6	\N	6	183	4
366	2020-01-24 04:43:18.27029+00	2020-01-24 04:43:18.270306+00	2019-10-06 16:00:00+00	3	\N	6	183	4
367	2020-01-24 04:43:18.33064+00	2020-01-24 04:43:18.330658+00	2019-10-06 16:00:00+00	8	\N	6	184	4
368	2020-01-24 04:43:18.340839+00	2020-01-24 04:43:18.340855+00	2019-10-06 16:00:00+00	6	\N	6	184	4
369	2020-01-24 04:43:18.395754+00	2020-01-24 04:43:18.395772+00	2019-10-06 16:00:00+00	8	\N	4	185	4
370	2020-01-24 04:43:18.403014+00	2020-01-24 04:43:18.403025+00	2019-10-06 16:00:00+00	3	\N	4	185	4
371	2020-01-24 04:43:18.45884+00	2020-01-24 04:43:18.458859+00	2019-10-06 16:00:00+00	6	\N	6	186	4
372	2020-01-24 04:43:18.471479+00	2020-01-24 04:43:18.471494+00	2019-10-06 16:00:00+00	6	\N	6	186	4
373	2020-01-24 04:43:18.527585+00	2020-01-24 04:43:18.527601+00	2019-10-06 16:00:00+00	8	\N	4	187	4
374	2020-01-24 04:43:18.537421+00	2020-01-24 04:43:18.537434+00	2019-10-06 16:00:00+00	3	\N	4	187	4
375	2020-01-24 04:43:18.598192+00	2020-01-24 04:43:18.598208+00	2019-10-06 16:00:00+00	8	\N	4	188	4
376	2020-01-24 04:43:18.611464+00	2020-01-24 04:43:18.611478+00	2019-10-06 16:00:00+00	3	\N	4	188	4
377	2020-01-24 04:43:18.665131+00	2020-01-24 04:43:18.665149+00	2019-10-06 16:00:00+00	6	\N	6	189	4
378	2020-01-24 04:43:18.678453+00	2020-01-24 04:43:18.678475+00	2019-10-06 16:00:00+00	3	\N	6	189	4
379	2020-01-24 04:43:18.733611+00	2020-01-24 04:43:18.733631+00	2019-10-06 16:00:00+00	6	\N	6	190	4
380	2020-01-24 04:43:18.744111+00	2020-01-24 04:43:18.744151+00	2019-10-06 16:00:00+00	3	\N	6	190	4
381	2020-01-24 04:43:18.819973+00	2020-01-24 04:43:18.819992+00	2019-10-06 16:00:00+00	8	\N	4	191	4
382	2020-01-24 04:43:18.831514+00	2020-01-24 04:43:18.831534+00	2019-10-06 16:00:00+00	3	\N	4	191	4
383	2020-01-24 04:43:18.890344+00	2020-01-24 04:43:18.890368+00	2019-10-06 16:00:00+00	8	\N	6	192	4
384	2020-01-24 04:43:18.898412+00	2020-01-24 04:43:18.898423+00	2019-10-06 16:00:00+00	3	\N	6	192	4
385	2020-01-24 04:43:18.957634+00	2020-01-24 04:43:18.957652+00	2019-10-06 16:00:00+00	6	\N	4	193	4
386	2020-01-24 04:43:18.968939+00	2020-01-24 04:43:18.968953+00	2019-10-06 16:00:00+00	3	\N	4	193	4
387	2020-01-24 04:43:19.026357+00	2020-01-24 04:43:19.026374+00	2019-10-06 16:00:00+00	6	\N	4	194	4
388	2020-01-24 04:43:19.033698+00	2020-01-24 04:43:19.033709+00	2019-10-06 16:00:00+00	3	\N	4	194	4
389	2020-01-24 04:43:19.074253+00	2020-01-24 04:43:19.074273+00	2019-10-06 16:00:00+00	3	\N	6	195	4
390	2020-01-24 04:43:19.083495+00	2020-01-24 04:43:19.083507+00	2019-10-06 16:00:00+00	6	\N	6	195	4
391	2020-01-24 04:43:19.144991+00	2020-01-24 04:43:19.14501+00	2019-10-06 16:00:00+00	8	\N	6	196	4
392	2020-01-24 04:43:19.158576+00	2020-01-24 04:43:19.158604+00	2019-10-06 16:00:00+00	3	\N	6	196	4
393	2020-01-24 04:43:19.228982+00	2020-01-24 04:43:19.229+00	2019-10-06 16:00:00+00	3	\N	5	197	4
394	2020-01-24 04:43:19.240663+00	2020-01-24 04:43:19.240679+00	2019-10-06 16:00:00+00	6	\N	5	197	4
395	2020-01-24 04:43:19.295051+00	2020-01-24 04:43:19.29507+00	2019-10-06 16:00:00+00	6	\N	4	198	4
396	2020-01-24 04:43:19.302867+00	2020-01-24 04:43:19.30288+00	2019-10-06 16:00:00+00	3	\N	4	198	4
397	2020-01-24 04:43:19.370532+00	2020-01-24 04:43:19.370553+00	2019-10-06 16:00:00+00	8	\N	6	199	4
398	2020-01-24 04:43:19.385799+00	2020-01-24 04:43:19.385816+00	2019-10-06 16:00:00+00	3	\N	6	199	4
399	2020-01-24 04:43:19.451635+00	2020-01-24 04:43:19.451653+00	2019-10-06 16:00:00+00	8	\N	4	200	4
400	2020-01-24 04:43:19.464654+00	2020-01-24 04:43:19.464669+00	2019-10-06 16:00:00+00	6	\N	4	200	4
401	2020-01-24 04:43:19.52295+00	2020-01-24 04:43:19.522991+00	2019-10-06 16:00:00+00	8	\N	4	201	4
402	2020-01-24 04:43:19.536639+00	2020-01-24 04:43:19.536656+00	2019-10-06 16:00:00+00	3	\N	4	201	4
403	2020-01-24 04:43:19.602741+00	2020-01-24 04:43:19.60276+00	2019-10-06 16:00:00+00	8	\N	6	202	4
404	2020-01-24 04:43:19.617729+00	2020-01-24 04:43:19.617747+00	2019-10-06 16:00:00+00	6	\N	6	202	4
405	2020-01-24 04:43:19.681456+00	2020-01-24 04:43:19.681476+00	2019-10-06 16:00:00+00	8	\N	6	203	4
406	2020-01-24 04:43:19.69071+00	2020-01-24 04:43:19.690725+00	2019-10-06 16:00:00+00	3	\N	6	203	4
407	2020-01-24 04:43:19.730906+00	2020-01-24 04:43:19.730923+00	2019-10-06 16:00:00+00	8	\N	6	204	4
408	2020-01-24 04:43:19.744975+00	2020-01-24 04:43:19.744989+00	2019-10-06 16:00:00+00	3	\N	6	204	4
409	2020-01-24 04:43:19.812035+00	2020-01-24 04:43:19.812053+00	2019-10-06 16:00:00+00	12	\N	4	205	4
410	2020-01-24 04:43:19.822543+00	2020-01-24 04:43:19.822557+00	2019-10-06 16:00:00+00	12	\N	4	205	4
411	2020-01-24 04:43:19.86632+00	2020-01-24 04:43:19.866338+00	2019-10-06 16:00:00+00	12	\N	6	206	4
412	2020-01-24 04:43:19.88117+00	2020-01-24 04:43:19.881189+00	2019-10-06 16:00:00+00	12	\N	6	206	4
413	2020-01-24 04:43:19.942328+00	2020-01-24 04:43:19.942348+00	2019-10-06 16:00:00+00	8	\N	4	207	4
414	2020-01-24 04:43:19.955826+00	2020-01-24 04:43:19.955842+00	2019-10-06 16:00:00+00	3	\N	4	207	4
415	2020-01-24 04:43:20.037657+00	2020-01-24 04:43:20.037675+00	2019-10-06 16:00:00+00	8	\N	4	208	4
416	2020-01-24 04:43:20.049162+00	2020-01-24 04:43:20.049178+00	2019-10-06 16:00:00+00	6	\N	4	208	4
417	2020-01-24 04:43:20.104611+00	2020-01-24 04:43:20.104631+00	2019-10-06 16:00:00+00	8	\N	4	209	4
418	2020-01-24 04:43:20.116227+00	2020-01-24 04:43:20.116239+00	2019-10-06 16:00:00+00	3	\N	4	209	4
419	2020-01-24 04:43:20.207664+00	2020-01-24 04:43:20.207682+00	2019-10-06 16:00:00+00	8	\N	4	210	4
420	2020-01-24 04:43:20.219998+00	2020-01-24 04:43:20.220013+00	2019-10-06 16:00:00+00	3	\N	4	210	4
421	2020-01-24 04:43:20.287905+00	2020-01-24 04:43:20.287928+00	2019-10-06 16:00:00+00	8	\N	6	211	4
422	2020-01-24 04:43:20.299047+00	2020-01-24 04:43:20.299266+00	2019-10-06 16:00:00+00	3	\N	6	211	4
423	2020-01-24 04:43:20.346523+00	2020-01-24 04:43:20.346545+00	2019-10-06 16:00:00+00	12	\N	6	212	4
424	2020-01-24 04:43:20.364368+00	2020-01-24 04:43:20.36439+00	2019-10-06 16:00:00+00	12	\N	6	212	4
425	2020-01-24 04:43:20.44849+00	2020-01-24 04:43:20.448513+00	2019-10-06 16:00:00+00	8	\N	6	213	4
426	2020-01-24 04:43:20.464358+00	2020-01-24 04:43:20.464379+00	2019-10-06 16:00:00+00	3	\N	6	213	4
427	2020-01-24 04:43:20.535493+00	2020-01-24 04:43:20.535514+00	2019-10-06 16:00:00+00	8	\N	6	214	4
428	2020-01-24 04:43:20.546415+00	2020-01-24 04:43:20.546431+00	2019-10-06 16:00:00+00	3	\N	6	214	4
429	2020-01-24 04:43:20.595312+00	2020-01-24 04:43:20.595332+00	2019-10-06 16:00:00+00	8	\N	6	215	4
430	2020-01-24 04:43:20.603774+00	2020-01-24 04:43:20.603791+00	2019-10-06 16:00:00+00	3	\N	6	215	4
431	2020-01-24 04:43:20.667577+00	2020-01-24 04:43:20.667596+00	2019-10-06 16:00:00+00	12	\N	4	216	4
432	2020-01-24 04:43:20.677547+00	2020-01-24 04:43:20.677564+00	2019-10-06 16:00:00+00	12	\N	4	216	4
433	2020-01-24 04:43:20.740157+00	2020-01-24 04:43:20.740176+00	2019-10-06 16:00:00+00	8	\N	4	217	4
434	2020-01-24 04:43:20.747609+00	2020-01-24 04:43:20.747622+00	2019-10-06 16:00:00+00	6	\N	4	217	4
435	2020-01-24 04:43:20.800669+00	2020-01-24 04:43:20.800687+00	2019-10-06 16:00:00+00	8	\N	6	218	4
436	2020-01-24 04:43:20.811501+00	2020-01-24 04:43:20.81152+00	2019-10-06 16:00:00+00	6	\N	6	218	4
437	2020-01-24 04:43:20.873122+00	2020-01-24 04:43:20.873141+00	2019-10-06 16:00:00+00	8	\N	4	219	4
438	2020-01-24 04:43:20.885981+00	2020-01-24 04:43:20.885998+00	2019-10-06 16:00:00+00	3	\N	4	219	4
439	2020-01-24 04:43:20.941914+00	2020-01-24 04:43:20.941933+00	2019-10-06 16:00:00+00	8	\N	6	220	4
440	2020-01-24 04:43:20.950134+00	2020-01-24 04:43:20.950146+00	2019-10-06 16:00:00+00	3	\N	6	220	4
441	2020-01-24 04:43:21.016217+00	2020-01-24 04:43:21.016238+00	2019-10-06 16:00:00+00	6	\N	4	221	4
442	2020-01-24 04:43:21.029754+00	2020-01-24 04:43:21.029771+00	2019-10-06 16:00:00+00	3	\N	4	221	4
443	2020-01-24 04:43:21.110394+00	2020-01-24 04:43:21.110413+00	2019-10-06 16:00:00+00	8	\N	6	222	4
444	2020-01-24 04:43:21.122179+00	2020-01-24 04:43:21.122192+00	2019-10-06 16:00:00+00	3	\N	6	222	4
445	2020-01-24 04:43:21.173217+00	2020-01-24 04:43:21.173235+00	2019-10-06 16:00:00+00	3	\N	6	223	4
446	2020-01-24 04:43:21.182078+00	2020-01-24 04:43:21.182092+00	2019-10-06 16:00:00+00	6	\N	6	223	4
447	2020-01-24 04:43:21.236789+00	2020-01-24 04:43:21.236809+00	2019-10-06 16:00:00+00	6	\N	6	224	4
448	2020-01-24 04:43:21.246993+00	2020-01-24 04:43:21.247009+00	2019-10-06 16:00:00+00	3	\N	6	224	4
449	2020-01-24 04:43:21.304166+00	2020-01-24 04:43:21.304185+00	2019-10-07 16:00:00+00	5	\N	8	225	4
450	2020-01-24 04:43:21.316065+00	2020-01-24 04:43:21.316078+00	2019-10-07 16:00:00+00	10	\N	8	225	4
451	2020-01-24 04:43:21.371678+00	2020-01-24 04:43:21.371696+00	2019-10-07 16:00:00+00	5	\N	8	226	4
452	2020-01-24 04:43:21.386573+00	2020-01-24 04:43:21.386589+00	2019-10-07 16:00:00+00	10	\N	8	226	4
453	2020-01-24 04:43:21.446449+00	2020-01-24 04:43:21.446467+00	2019-10-07 16:00:00+00	3	\N	8	227	4
454	2020-01-24 04:43:21.456543+00	2020-01-24 04:43:21.456557+00	2019-10-07 16:00:00+00	10	\N	8	227	4
455	2020-01-24 04:43:21.512904+00	2020-01-24 04:43:21.512922+00	2019-10-07 16:00:00+00	5	\N	4	228	4
456	2020-01-24 04:43:21.524958+00	2020-01-24 04:43:21.524975+00	2019-10-07 16:00:00+00	4	\N	4	228	4
457	2020-01-24 04:43:21.600315+00	2020-01-24 04:43:21.600334+00	2019-10-07 16:00:00+00	3	\N	5	229	4
458	2020-01-24 04:43:21.617457+00	2020-01-24 04:43:21.617471+00	2019-10-07 16:00:00+00	10	\N	5	229	4
459	2020-01-24 04:43:21.676416+00	2020-01-24 04:43:21.676436+00	2019-10-07 16:00:00+00	5	\N	4	230	4
460	2020-01-24 04:43:21.687479+00	2020-01-24 04:43:21.687497+00	2019-10-07 16:00:00+00	10	\N	4	230	4
461	2020-01-24 04:43:21.740486+00	2020-01-24 04:43:21.740505+00	2019-10-07 16:00:00+00	5	\N	5	231	4
462	2020-01-24 04:43:21.747495+00	2020-01-24 04:43:21.747508+00	2019-10-07 16:00:00+00	10	\N	5	231	4
463	2020-01-24 04:43:21.801918+00	2020-01-24 04:43:21.801937+00	2019-10-07 16:00:00+00	3	\N	6	232	4
464	2020-01-24 04:43:21.814278+00	2020-01-24 04:43:21.814293+00	2019-10-07 16:00:00+00	10	\N	6	232	4
465	2020-01-24 04:43:21.872073+00	2020-01-24 04:43:21.872092+00	2019-10-07 16:00:00+00	5	\N	8	233	4
466	2020-01-24 04:43:21.884376+00	2020-01-24 04:43:21.884393+00	2019-10-07 16:00:00+00	5	\N	8	233	4
467	2020-01-24 04:43:21.939611+00	2020-01-24 04:43:21.93963+00	2019-10-08 16:00:00+00	10	\N	8	234	4
468	2020-01-24 04:43:21.951908+00	2020-01-24 04:43:21.951922+00	2019-10-08 16:00:00+00	4	\N	8	234	4
469	2020-01-24 04:43:22.000079+00	2020-01-24 04:43:22.000099+00	2019-10-08 16:00:00+00	5	\N	5	235	4
470	2020-01-24 04:43:22.013978+00	2020-01-24 04:43:22.013998+00	2019-10-08 16:00:00+00	4	\N	5	235	4
471	2020-01-24 04:43:22.071931+00	2020-01-24 04:43:22.071949+00	2019-10-09 16:00:00+00	4	\N	5	236	4
472	2020-01-24 04:43:22.087382+00	2020-01-24 04:43:22.087402+00	2019-10-09 16:00:00+00	4	\N	5	236	4
473	2020-01-24 04:43:22.146704+00	2020-01-24 04:43:22.146722+00	2019-10-09 16:00:00+00	4	\N	6	237	4
474	2020-01-24 04:43:22.15881+00	2020-01-24 04:43:22.158829+00	2019-10-09 16:00:00+00	10	\N	6	237	4
475	2020-01-24 04:43:22.211543+00	2020-01-24 04:43:22.211561+00	2019-10-10 16:00:00+00	10	\N	8	238	4
476	2020-01-24 04:43:22.224321+00	2020-01-24 04:43:22.22434+00	2019-10-10 16:00:00+00	4	\N	8	238	4
477	2020-01-24 04:43:22.300376+00	2020-01-24 04:43:22.300396+00	2019-10-10 16:00:00+00	10	\N	4	239	4
478	2020-01-24 04:43:22.312848+00	2020-01-24 04:43:22.312862+00	2019-10-10 16:00:00+00	4	\N	4	239	4
479	2020-01-24 04:43:22.378682+00	2020-01-24 04:43:22.3787+00	2019-10-10 16:00:00+00	10	\N	8	240	4
480	2020-01-24 04:43:22.391881+00	2020-01-24 04:43:22.391898+00	2019-10-10 16:00:00+00	4	\N	8	240	4
\.


--
-- Data for Name: sows_events_sowfarrow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_sowfarrow (id, created_at, modified_at, date, alive_quantity, dead_quantity, mummy_quantity, initiator_id, piglets_group_id, sow_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_events_ultrasound; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_ultrasound (id, created_at, modified_at, date, result, initiator_id, sow_id, tour_id, u_type_id) FROM stdin;
1	2020-01-24 04:43:05.552535+00	2020-01-24 04:43:05.552554+00	2019-10-14 16:00:00+00	t	\N	1	1	1
2	2020-01-24 04:43:05.577405+00	2020-01-24 04:43:05.577423+00	2019-10-21 16:00:00+00	t	\N	1	1	2
3	2020-01-24 04:43:05.650146+00	2020-01-24 04:43:05.650165+00	2019-10-14 16:00:00+00	t	\N	2	1	1
4	2020-01-24 04:43:05.663433+00	2020-01-24 04:43:05.663453+00	2019-10-21 16:00:00+00	t	\N	2	1	2
5	2020-01-24 04:43:05.738001+00	2020-01-24 04:43:05.73802+00	2019-10-14 16:00:00+00	t	\N	3	1	1
6	2020-01-24 04:43:05.749218+00	2020-01-24 04:43:05.749235+00	2019-10-21 16:00:00+00	t	\N	3	1	2
7	2020-01-24 04:43:05.813343+00	2020-01-24 04:43:05.813358+00	2019-10-14 16:00:00+00	t	\N	4	1	1
8	2020-01-24 04:43:05.822932+00	2020-01-24 04:43:05.822945+00	2019-10-21 16:00:00+00	t	\N	4	1	2
9	2020-01-24 04:43:05.887997+00	2020-01-24 04:43:05.888016+00	2019-10-14 16:00:00+00	t	\N	5	1	1
10	2020-01-24 04:43:05.898081+00	2020-01-24 04:43:05.898096+00	2019-10-21 16:00:00+00	t	\N	5	1	2
11	2020-01-24 04:43:05.956683+00	2020-01-24 04:43:05.956698+00	2019-10-14 16:00:00+00	t	\N	6	1	1
12	2020-01-24 04:43:05.968087+00	2020-01-24 04:43:05.968168+00	2019-10-21 16:00:00+00	t	\N	6	1	2
13	2020-01-24 04:43:06.068747+00	2020-01-24 04:43:06.068767+00	2019-10-15 16:00:00+00	t	\N	7	1	1
14	2020-01-24 04:43:06.079997+00	2020-01-24 04:43:06.080011+00	2019-10-22 16:00:00+00	t	\N	7	1	2
15	2020-01-24 04:43:06.14067+00	2020-01-24 04:43:06.140685+00	2019-10-15 16:00:00+00	t	\N	8	1	1
16	2020-01-24 04:43:06.149999+00	2020-01-24 04:43:06.150014+00	2019-10-22 16:00:00+00	t	\N	8	1	2
17	2020-01-24 04:43:06.228349+00	2020-01-24 04:43:06.228365+00	2019-10-15 16:00:00+00	t	\N	9	1	1
18	2020-01-24 04:43:06.23846+00	2020-01-24 04:43:06.238476+00	2019-10-22 16:00:00+00	t	\N	9	1	2
19	2020-01-24 04:43:06.300034+00	2020-01-24 04:43:06.300047+00	2019-10-15 16:00:00+00	t	\N	10	1	1
20	2020-01-24 04:43:06.305236+00	2020-01-24 04:43:06.305248+00	2019-10-22 16:00:00+00	t	\N	10	1	2
21	2020-01-24 04:43:06.371833+00	2020-01-24 04:43:06.371851+00	2019-10-15 16:00:00+00	t	\N	11	1	1
22	2020-01-24 04:43:06.385387+00	2020-01-24 04:43:06.385403+00	2019-10-22 16:00:00+00	t	\N	11	1	2
23	2020-01-24 04:43:06.446359+00	2020-01-24 04:43:06.446375+00	2019-10-15 16:00:00+00	t	\N	12	1	1
24	2020-01-24 04:43:06.456379+00	2020-01-24 04:43:06.456394+00	2019-10-22 16:00:00+00	t	\N	12	1	2
25	2020-01-24 04:43:06.522831+00	2020-01-24 04:43:06.522846+00	2019-10-15 16:00:00+00	t	\N	13	1	1
26	2020-01-24 04:43:06.534332+00	2020-01-24 04:43:06.534352+00	2019-10-22 16:00:00+00	t	\N	13	1	2
27	2020-01-24 04:43:06.616638+00	2020-01-24 04:43:06.616655+00	2019-10-16 16:00:00+00	t	\N	14	1	1
28	2020-01-24 04:43:06.624594+00	2020-01-24 04:43:06.624608+00	2019-10-23 16:00:00+00	t	\N	14	1	2
29	2020-01-24 04:43:06.693653+00	2020-01-24 04:43:06.693676+00	2019-10-16 16:00:00+00	t	\N	15	1	1
30	2020-01-24 04:43:06.70233+00	2020-01-24 04:43:06.702344+00	2019-10-23 16:00:00+00	t	\N	15	1	2
31	2020-01-24 04:43:06.769476+00	2020-01-24 04:43:06.769495+00	2019-10-16 16:00:00+00	t	\N	16	1	1
32	2020-01-24 04:43:06.789762+00	2020-01-24 04:43:06.790052+00	2019-10-23 16:00:00+00	t	\N	16	1	2
33	2020-01-24 04:43:06.851317+00	2020-01-24 04:43:06.85133+00	2019-10-16 16:00:00+00	t	\N	17	1	1
34	2020-01-24 04:43:06.857121+00	2020-01-24 04:43:06.857134+00	2019-10-23 16:00:00+00	t	\N	17	1	2
35	2020-01-24 04:43:06.92149+00	2020-01-24 04:43:06.921508+00	2019-10-16 16:00:00+00	t	\N	18	1	1
36	2020-01-24 04:43:06.931376+00	2020-01-24 04:43:06.931391+00	2019-10-23 16:00:00+00	t	\N	18	1	2
37	2020-01-24 04:43:06.997409+00	2020-01-24 04:43:06.997426+00	2019-10-16 16:00:00+00	t	\N	19	1	1
38	2020-01-24 04:43:07.008153+00	2020-01-24 04:43:07.008173+00	2019-10-23 16:00:00+00	t	\N	19	1	2
39	2020-01-24 04:43:07.05293+00	2020-01-24 04:43:07.052945+00	2019-10-17 16:00:00+00	t	\N	20	1	1
40	2020-01-24 04:43:07.064236+00	2020-01-24 04:43:07.064253+00	2019-10-24 16:00:00+00	t	\N	20	1	2
41	2020-01-24 04:43:07.160441+00	2020-01-24 04:43:07.160458+00	2019-10-17 16:00:00+00	t	\N	21	1	1
42	2020-01-24 04:43:07.171291+00	2020-01-24 04:43:07.171337+00	2019-10-24 16:00:00+00	t	\N	21	1	2
43	2020-01-24 04:43:07.261622+00	2020-01-24 04:43:07.26178+00	2019-10-17 16:00:00+00	t	\N	22	1	1
44	2020-01-24 04:43:07.268595+00	2020-01-24 04:43:07.26861+00	2019-10-24 16:00:00+00	t	\N	22	1	2
45	2020-01-24 04:43:07.319019+00	2020-01-24 04:43:07.319033+00	2019-10-17 16:00:00+00	t	\N	23	1	1
46	2020-01-24 04:43:07.330451+00	2020-01-24 04:43:07.330521+00	2019-10-24 16:00:00+00	t	\N	23	1	2
47	2020-01-24 04:43:07.410997+00	2020-01-24 04:43:07.411016+00	2019-10-18 16:00:00+00	t	\N	24	1	1
48	2020-01-24 04:43:07.422388+00	2020-01-24 04:43:07.422405+00	2019-10-25 16:00:00+00	t	\N	24	1	2
49	2020-01-24 04:43:07.486947+00	2020-01-24 04:43:07.487+00	2019-10-20 16:00:00+00	t	\N	25	2	1
50	2020-01-24 04:43:07.504173+00	2020-01-24 04:43:07.504194+00	2019-10-27 16:00:00+00	t	\N	25	2	2
51	2020-01-24 04:43:07.573355+00	2020-01-24 04:43:07.573372+00	2019-10-20 16:00:00+00	t	\N	26	2	1
52	2020-01-24 04:43:07.591169+00	2020-01-24 04:43:07.59119+00	2019-10-27 16:00:00+00	t	\N	26	2	2
53	2020-01-24 04:43:07.666554+00	2020-01-24 04:43:07.666569+00	2019-10-20 16:00:00+00	t	\N	27	2	1
54	2020-01-24 04:43:07.672149+00	2020-01-24 04:43:07.672165+00	2019-10-27 16:00:00+00	t	\N	27	2	2
55	2020-01-24 04:43:07.726635+00	2020-01-24 04:43:07.726648+00	2019-10-20 16:00:00+00	t	\N	28	2	1
56	2020-01-24 04:43:07.732682+00	2020-01-24 04:43:07.732694+00	2019-10-27 16:00:00+00	t	\N	28	2	2
57	2020-01-24 04:43:07.794249+00	2020-01-24 04:43:07.794266+00	2019-10-20 16:00:00+00	t	\N	29	2	1
58	2020-01-24 04:43:07.80733+00	2020-01-24 04:43:07.807347+00	2019-10-27 16:00:00+00	t	\N	29	2	2
59	2020-01-24 04:43:07.858478+00	2020-01-24 04:43:07.858494+00	2019-10-20 16:00:00+00	t	\N	30	2	1
60	2020-01-24 04:43:07.864722+00	2020-01-24 04:43:07.864735+00	2019-10-27 16:00:00+00	t	\N	30	2	2
61	2020-01-24 04:43:07.945499+00	2020-01-24 04:43:07.945519+00	2019-10-20 16:00:00+00	t	\N	31	2	1
62	2020-01-24 04:43:07.959389+00	2020-01-24 04:43:07.959414+00	2019-10-27 16:00:00+00	t	\N	31	2	2
63	2020-01-24 04:43:08.066513+00	2020-01-24 04:43:08.066535+00	2019-10-20 16:00:00+00	t	\N	32	2	1
64	2020-01-24 04:43:08.080292+00	2020-01-24 04:43:08.080316+00	2019-10-27 16:00:00+00	t	\N	32	2	2
65	2020-01-24 04:43:08.158822+00	2020-01-24 04:43:08.158835+00	2019-10-20 16:00:00+00	t	\N	33	2	1
66	2020-01-24 04:43:08.164231+00	2020-01-24 04:43:08.164244+00	2019-10-27 16:00:00+00	t	\N	33	2	2
67	2020-01-24 04:43:08.220227+00	2020-01-24 04:43:08.220243+00	2019-10-20 16:00:00+00	t	\N	34	2	1
68	2020-01-24 04:43:08.241135+00	2020-01-24 04:43:08.241156+00	2019-10-27 16:00:00+00	t	\N	34	2	2
69	2020-01-24 04:43:08.306221+00	2020-01-24 04:43:08.30624+00	2019-10-20 16:00:00+00	t	\N	35	2	1
70	2020-01-24 04:43:08.317357+00	2020-01-24 04:43:08.317374+00	2019-10-27 16:00:00+00	t	\N	35	2	2
71	2020-01-24 04:43:08.356134+00	2020-01-24 04:43:08.356147+00	2019-10-20 16:00:00+00	t	\N	36	2	1
72	2020-01-24 04:43:08.365163+00	2020-01-24 04:43:08.365179+00	2019-10-27 16:00:00+00	t	\N	36	2	2
73	2020-01-24 04:43:08.460665+00	2020-01-24 04:43:08.460688+00	2019-10-20 16:00:00+00	t	\N	37	2	1
74	2020-01-24 04:43:08.471753+00	2020-01-24 04:43:08.471769+00	2019-10-27 16:00:00+00	t	\N	37	2	2
75	2020-01-24 04:43:08.527249+00	2020-01-24 04:43:08.527264+00	2019-10-20 16:00:00+00	t	\N	38	2	1
76	2020-01-24 04:43:08.533007+00	2020-01-24 04:43:08.533019+00	2019-10-27 16:00:00+00	t	\N	38	2	2
77	2020-01-24 04:43:08.584399+00	2020-01-24 04:43:08.584414+00	2019-10-20 16:00:00+00	t	\N	39	2	1
78	2020-01-24 04:43:08.594389+00	2020-01-24 04:43:08.594404+00	2019-10-27 16:00:00+00	t	\N	39	2	2
79	2020-01-24 04:43:08.652532+00	2020-01-24 04:43:08.652546+00	2019-10-20 16:00:00+00	t	\N	40	2	1
80	2020-01-24 04:43:08.657621+00	2020-01-24 04:43:08.657633+00	2019-10-27 16:00:00+00	t	\N	40	2	2
81	2020-01-24 04:43:08.705484+00	2020-01-24 04:43:08.705499+00	2019-10-20 16:00:00+00	t	\N	41	2	1
82	2020-01-24 04:43:08.722876+00	2020-01-24 04:43:08.722893+00	2019-10-27 16:00:00+00	t	\N	41	2	2
83	2020-01-24 04:43:08.783479+00	2020-01-24 04:43:08.783494+00	2019-10-20 16:00:00+00	t	\N	42	2	1
84	2020-01-24 04:43:08.79496+00	2020-01-24 04:43:08.794975+00	2019-10-27 16:00:00+00	t	\N	42	2	2
85	2020-01-24 04:43:08.909951+00	2020-01-24 04:43:08.909968+00	2019-10-20 16:00:00+00	t	\N	43	2	1
86	2020-01-24 04:43:08.923555+00	2020-01-24 04:43:08.923569+00	2019-10-27 16:00:00+00	t	\N	43	2	2
87	2020-01-24 04:43:08.985349+00	2020-01-24 04:43:08.985364+00	2019-10-20 16:00:00+00	t	\N	44	2	1
88	2020-01-24 04:43:08.994861+00	2020-01-24 04:43:08.994876+00	2019-10-27 16:00:00+00	t	\N	44	2	2
89	2020-01-24 04:43:09.043437+00	2020-01-24 04:43:09.04345+00	2019-10-20 16:00:00+00	t	\N	45	2	1
90	2020-01-24 04:43:09.048484+00	2020-01-24 04:43:09.048497+00	2019-10-27 16:00:00+00	t	\N	45	2	2
91	2020-01-24 04:43:09.101606+00	2020-01-24 04:43:09.101621+00	2019-10-20 16:00:00+00	t	\N	46	2	1
92	2020-01-24 04:43:09.11365+00	2020-01-24 04:43:09.113665+00	2019-10-27 16:00:00+00	t	\N	46	2	2
93	2020-01-24 04:43:09.173083+00	2020-01-24 04:43:09.173096+00	2019-10-20 16:00:00+00	t	\N	47	2	1
94	2020-01-24 04:43:09.177901+00	2020-01-24 04:43:09.177914+00	2019-10-27 16:00:00+00	t	\N	47	2	2
95	2020-01-24 04:43:09.223591+00	2020-01-24 04:43:09.223898+00	2019-10-20 16:00:00+00	t	\N	48	2	1
96	2020-01-24 04:43:09.242365+00	2020-01-24 04:43:09.242378+00	2019-10-27 16:00:00+00	t	\N	48	2	2
97	2020-01-24 04:43:09.300328+00	2020-01-24 04:43:09.300345+00	2019-10-20 16:00:00+00	t	\N	49	2	1
98	2020-01-24 04:43:09.309378+00	2020-01-24 04:43:09.309488+00	2019-10-27 16:00:00+00	t	\N	49	2	2
99	2020-01-24 04:43:09.368424+00	2020-01-24 04:43:09.36844+00	2019-10-20 16:00:00+00	t	\N	50	2	1
100	2020-01-24 04:43:09.378015+00	2020-01-24 04:43:09.37803+00	2019-10-27 16:00:00+00	t	\N	50	2	2
101	2020-01-24 04:43:09.441715+00	2020-01-24 04:43:09.441731+00	2019-10-20 16:00:00+00	t	\N	51	2	1
102	2020-01-24 04:43:09.448845+00	2020-01-24 04:43:09.448858+00	2019-10-27 16:00:00+00	t	\N	51	2	2
103	2020-01-24 04:43:09.51183+00	2020-01-24 04:43:09.511854+00	2019-10-20 16:00:00+00	t	\N	52	2	1
104	2020-01-24 04:43:09.521745+00	2020-01-24 04:43:09.52176+00	2019-10-27 16:00:00+00	t	\N	52	2	2
105	2020-01-24 04:43:09.580234+00	2020-01-24 04:43:09.58025+00	2019-10-20 16:00:00+00	t	\N	53	2	1
106	2020-01-24 04:43:09.590234+00	2020-01-24 04:43:09.590249+00	2019-10-27 16:00:00+00	t	\N	53	2	2
107	2020-01-24 04:43:09.653592+00	2020-01-24 04:43:09.653743+00	2019-10-20 16:00:00+00	t	\N	54	2	1
108	2020-01-24 04:43:09.664604+00	2020-01-24 04:43:09.66462+00	2019-10-27 16:00:00+00	t	\N	54	2	2
109	2020-01-24 04:43:09.72058+00	2020-01-24 04:43:09.720596+00	2019-10-20 16:00:00+00	t	\N	55	2	1
110	2020-01-24 04:43:09.732862+00	2020-01-24 04:43:09.732881+00	2019-10-27 16:00:00+00	t	\N	55	2	2
111	2020-01-24 04:43:09.785456+00	2020-01-24 04:43:09.785469+00	2019-10-20 16:00:00+00	t	\N	56	2	1
112	2020-01-24 04:43:09.793059+00	2020-01-24 04:43:09.793074+00	2019-10-27 16:00:00+00	t	\N	56	2	2
113	2020-01-24 04:43:09.847202+00	2020-01-24 04:43:09.847219+00	2019-10-20 16:00:00+00	t	\N	57	2	1
114	2020-01-24 04:43:09.858035+00	2020-01-24 04:43:09.858052+00	2019-10-27 16:00:00+00	t	\N	57	2	2
115	2020-01-24 04:43:09.924009+00	2020-01-24 04:43:09.924025+00	2019-10-20 16:00:00+00	t	\N	58	2	1
116	2020-01-24 04:43:09.934749+00	2020-01-24 04:43:09.934766+00	2019-10-27 16:00:00+00	t	\N	58	2	2
117	2020-01-24 04:43:09.98507+00	2020-01-24 04:43:09.985086+00	2019-10-20 16:00:00+00	t	\N	59	2	1
118	2020-01-24 04:43:09.993503+00	2020-01-24 04:43:09.993519+00	2019-10-27 16:00:00+00	t	\N	59	2	2
119	2020-01-24 04:43:10.051523+00	2020-01-24 04:43:10.05154+00	2019-10-20 16:00:00+00	t	\N	60	2	1
120	2020-01-24 04:43:10.062087+00	2020-01-24 04:43:10.062102+00	2019-10-27 16:00:00+00	t	\N	60	2	2
121	2020-01-24 04:43:10.118938+00	2020-01-24 04:43:10.118953+00	2019-10-20 16:00:00+00	t	\N	61	2	1
122	2020-01-24 04:43:10.141542+00	2020-01-24 04:43:10.141564+00	2019-10-27 16:00:00+00	t	\N	61	2	2
123	2020-01-24 04:43:10.206439+00	2020-01-24 04:43:10.206453+00	2019-10-22 16:00:00+00	t	\N	62	2	1
124	2020-01-24 04:43:10.216488+00	2020-01-24 04:43:10.216501+00	2019-10-29 16:00:00+00	t	\N	62	2	2
125	2020-01-24 04:43:10.277429+00	2020-01-24 04:43:10.277444+00	2019-10-22 16:00:00+00	t	\N	63	2	1
126	2020-01-24 04:43:10.288625+00	2020-01-24 04:43:10.28864+00	2019-10-29 16:00:00+00	t	\N	63	2	2
127	2020-01-24 04:43:10.35108+00	2020-01-24 04:43:10.351097+00	2019-10-22 16:00:00+00	t	\N	64	2	1
128	2020-01-24 04:43:10.365366+00	2020-01-24 04:43:10.365382+00	2019-10-29 16:00:00+00	t	\N	64	2	2
129	2020-01-24 04:43:10.430357+00	2020-01-24 04:43:10.430372+00	2019-10-22 16:00:00+00	t	\N	65	2	1
130	2020-01-24 04:43:10.44232+00	2020-01-24 04:43:10.44234+00	2019-10-29 16:00:00+00	t	\N	65	2	2
131	2020-01-24 04:43:10.506245+00	2020-01-24 04:43:10.506261+00	2019-10-22 16:00:00+00	t	\N	66	2	1
132	2020-01-24 04:43:10.516469+00	2020-01-24 04:43:10.516483+00	2019-10-29 16:00:00+00	t	\N	66	2	2
133	2020-01-24 04:43:10.573529+00	2020-01-24 04:43:10.573543+00	2019-10-22 16:00:00+00	t	\N	67	2	1
134	2020-01-24 04:43:10.583545+00	2020-01-24 04:43:10.583562+00	2019-10-29 16:00:00+00	t	\N	67	2	2
135	2020-01-24 04:43:10.651427+00	2020-01-24 04:43:10.651444+00	2019-10-22 16:00:00+00	t	\N	68	2	1
136	2020-01-24 04:43:10.661557+00	2020-01-24 04:43:10.66157+00	2019-10-29 16:00:00+00	t	\N	68	2	2
137	2020-01-24 04:43:10.720386+00	2020-01-24 04:43:10.7204+00	2019-10-22 16:00:00+00	t	\N	69	2	1
138	2020-01-24 04:43:10.730601+00	2020-01-24 04:43:10.730614+00	2019-10-29 16:00:00+00	t	\N	69	2	2
139	2020-01-24 04:43:10.789072+00	2020-01-24 04:43:10.789086+00	2019-10-23 16:00:00+00	t	\N	70	2	1
140	2020-01-24 04:43:10.800921+00	2020-01-24 04:43:10.800944+00	2019-10-30 16:00:00+00	t	\N	70	2	2
141	2020-01-24 04:43:10.861472+00	2020-01-24 04:43:10.861486+00	2019-10-23 16:00:00+00	t	\N	71	2	1
142	2020-01-24 04:43:10.870917+00	2020-01-24 04:43:10.87093+00	2019-10-30 16:00:00+00	t	\N	71	2	2
143	2020-01-24 04:43:10.933623+00	2020-01-24 04:43:10.933636+00	2019-10-23 16:00:00+00	t	\N	72	2	1
144	2020-01-24 04:43:10.943609+00	2020-01-24 04:43:10.943625+00	2019-10-30 16:00:00+00	t	\N	72	2	2
145	2020-01-24 04:43:10.99919+00	2020-01-24 04:43:10.999204+00	2019-10-23 16:00:00+00	t	\N	73	2	1
146	2020-01-24 04:43:11.00913+00	2020-01-24 04:43:11.009144+00	2019-10-30 16:00:00+00	t	\N	73	2	2
147	2020-01-24 04:43:11.066158+00	2020-01-24 04:43:11.066176+00	2019-10-23 16:00:00+00	t	\N	74	2	1
148	2020-01-24 04:43:11.076403+00	2020-01-24 04:43:11.076419+00	2019-10-30 16:00:00+00	t	\N	74	2	2
149	2020-01-24 04:43:11.137896+00	2020-01-24 04:43:11.137911+00	2019-10-23 16:00:00+00	t	\N	75	2	1
150	2020-01-24 04:43:11.148409+00	2020-01-24 04:43:11.148423+00	2019-10-30 16:00:00+00	t	\N	75	2	2
151	2020-01-24 04:43:11.20002+00	2020-01-24 04:43:11.200032+00	2019-10-24 16:00:00+00	t	\N	76	2	1
152	2020-01-24 04:43:11.207816+00	2020-01-24 04:43:11.20783+00	2019-10-31 16:00:00+00	t	\N	76	2	2
153	2020-01-24 04:43:11.265216+00	2020-01-24 04:43:11.265231+00	2019-10-24 16:00:00+00	t	\N	77	2	1
154	2020-01-24 04:43:11.275013+00	2020-01-24 04:43:11.275029+00	2019-10-31 16:00:00+00	t	\N	77	2	2
155	2020-01-24 04:43:11.325853+00	2020-01-24 04:43:11.325866+00	2019-10-24 16:00:00+00	t	\N	78	2	1
156	2020-01-24 04:43:11.331346+00	2020-01-24 04:43:11.331487+00	2019-10-31 16:00:00+00	t	\N	78	2	2
157	2020-01-24 04:43:11.373129+00	2020-01-24 04:43:11.373144+00	2019-10-24 16:00:00+00	t	\N	79	2	1
158	2020-01-24 04:43:11.378693+00	2020-01-24 04:43:11.378715+00	2019-10-31 16:00:00+00	t	\N	79	2	2
159	2020-01-24 04:43:11.440856+00	2020-01-24 04:43:11.440878+00	2019-10-24 16:00:00+00	t	\N	80	2	1
160	2020-01-24 04:43:11.451488+00	2020-01-24 04:43:11.451504+00	2019-10-31 16:00:00+00	t	\N	80	2	2
161	2020-01-24 04:43:11.522829+00	2020-01-24 04:43:11.522843+00	2019-10-24 16:00:00+00	t	\N	81	2	1
162	2020-01-24 04:43:11.528625+00	2020-01-24 04:43:11.528637+00	2019-10-31 16:00:00+00	t	\N	81	2	2
163	2020-01-24 04:43:11.586893+00	2020-01-24 04:43:11.586906+00	2019-10-25 16:00:00+00	t	\N	82	2	1
164	2020-01-24 04:43:11.597921+00	2020-01-24 04:43:11.597942+00	2019-11-01 16:00:00+00	t	\N	82	2	2
165	2020-01-24 04:43:11.658048+00	2020-01-24 04:43:11.658066+00	2019-10-25 16:00:00+00	t	\N	83	2	1
166	2020-01-24 04:43:11.674418+00	2020-01-24 04:43:11.674439+00	2019-11-01 16:00:00+00	t	\N	83	2	2
167	2020-01-24 04:43:11.727367+00	2020-01-24 04:43:11.727383+00	2019-10-25 16:00:00+00	t	\N	84	2	1
168	2020-01-24 04:43:11.733107+00	2020-01-24 04:43:11.73312+00	2019-11-01 16:00:00+00	t	\N	84	2	2
169	2020-01-24 04:43:11.801169+00	2020-01-24 04:43:11.801432+00	2019-10-25 16:00:00+00	t	\N	85	2	1
170	2020-01-24 04:43:11.814143+00	2020-01-24 04:43:11.814157+00	2019-11-01 16:00:00+00	t	\N	85	2	2
171	2020-01-24 04:43:11.881209+00	2020-01-24 04:43:11.881225+00	2019-10-25 16:00:00+00	t	\N	86	2	1
172	2020-01-24 04:43:11.887554+00	2020-01-24 04:43:11.887567+00	2019-11-01 16:00:00+00	t	\N	86	2	2
173	2020-01-24 04:43:11.938894+00	2020-01-24 04:43:11.938912+00	2019-10-25 16:00:00+00	t	\N	87	2	1
174	2020-01-24 04:43:11.945732+00	2020-01-24 04:43:11.945752+00	2019-11-01 16:00:00+00	t	\N	87	2	2
175	2020-01-24 04:43:11.993787+00	2020-01-24 04:43:11.993806+00	2019-10-26 16:00:00+00	t	\N	88	2	1
176	2020-01-24 04:43:12.000071+00	2020-01-24 04:43:12.000087+00	2019-11-02 16:00:00+00	t	\N	88	2	2
177	2020-01-24 04:43:12.076431+00	2020-01-24 04:43:12.076449+00	2019-10-26 16:00:00+00	t	\N	89	2	1
178	2020-01-24 04:43:12.086085+00	2020-01-24 04:43:12.086099+00	2019-11-02 16:00:00+00	t	\N	89	2	2
179	2020-01-24 04:43:12.144781+00	2020-01-24 04:43:12.144795+00	2019-10-27 16:00:00+00	t	\N	90	3	1
180	2020-01-24 04:43:12.150571+00	2020-01-24 04:43:12.150583+00	2019-11-03 16:00:00+00	t	\N	90	3	2
181	2020-01-24 04:43:12.219967+00	2020-01-24 04:43:12.219984+00	2019-10-27 16:00:00+00	t	\N	91	3	1
182	2020-01-24 04:43:12.227953+00	2020-01-24 04:43:12.227973+00	2019-11-03 16:00:00+00	t	\N	91	3	2
183	2020-01-24 04:43:12.298714+00	2020-01-24 04:43:12.298728+00	2019-10-27 16:00:00+00	t	\N	92	3	1
184	2020-01-24 04:43:12.309741+00	2020-01-24 04:43:12.309763+00	2019-11-03 16:00:00+00	t	\N	92	3	2
185	2020-01-24 04:43:12.375161+00	2020-01-24 04:43:12.375185+00	2019-10-27 16:00:00+00	t	\N	93	3	1
186	2020-01-24 04:43:12.382512+00	2020-01-24 04:43:12.382525+00	2019-11-03 16:00:00+00	t	\N	93	3	2
187	2020-01-24 04:43:12.433612+00	2020-01-24 04:43:12.433624+00	2019-10-27 16:00:00+00	t	\N	94	3	1
188	2020-01-24 04:43:12.443744+00	2020-01-24 04:43:12.443758+00	2019-11-03 16:00:00+00	t	\N	94	3	2
189	2020-01-24 04:43:12.521112+00	2020-01-24 04:43:12.521128+00	2019-10-27 16:00:00+00	t	\N	95	3	1
190	2020-01-24 04:43:12.53215+00	2020-01-24 04:43:12.532166+00	2019-11-03 16:00:00+00	t	\N	95	3	2
191	2020-01-24 04:43:12.59852+00	2020-01-24 04:43:12.598532+00	2019-10-27 16:00:00+00	t	\N	96	3	1
192	2020-01-24 04:43:12.604051+00	2020-01-24 04:43:12.604064+00	2019-11-03 16:00:00+00	t	\N	96	3	2
193	2020-01-24 04:43:12.66569+00	2020-01-24 04:43:12.665708+00	2019-10-27 16:00:00+00	t	\N	97	3	1
194	2020-01-24 04:43:12.68225+00	2020-01-24 04:43:12.682266+00	2019-11-03 16:00:00+00	t	\N	97	3	2
195	2020-01-24 04:43:12.736736+00	2020-01-24 04:43:12.736748+00	2019-10-27 16:00:00+00	t	\N	98	3	1
196	2020-01-24 04:43:12.742598+00	2020-01-24 04:43:12.742618+00	2019-11-03 16:00:00+00	t	\N	98	3	2
197	2020-01-24 04:43:12.796204+00	2020-01-24 04:43:12.796217+00	2019-10-27 16:00:00+00	t	\N	99	3	1
198	2020-01-24 04:43:12.801964+00	2020-01-24 04:43:12.801977+00	2019-11-03 16:00:00+00	t	\N	99	3	2
199	2020-01-24 04:43:12.854798+00	2020-01-24 04:43:12.854811+00	2019-10-27 16:00:00+00	t	\N	100	3	1
200	2020-01-24 04:43:12.860441+00	2020-01-24 04:43:12.860453+00	2019-11-03 16:00:00+00	t	\N	100	3	2
201	2020-01-24 04:43:12.915821+00	2020-01-24 04:43:12.915836+00	2019-10-27 16:00:00+00	t	\N	101	3	1
202	2020-01-24 04:43:12.925333+00	2020-01-24 04:43:12.925346+00	2019-11-03 16:00:00+00	t	\N	101	3	2
203	2020-01-24 04:43:12.989246+00	2020-01-24 04:43:12.989259+00	2019-10-27 16:00:00+00	t	\N	102	3	1
204	2020-01-24 04:43:12.995463+00	2020-01-24 04:43:12.995475+00	2019-11-03 16:00:00+00	t	\N	102	3	2
205	2020-01-24 04:43:13.035536+00	2020-01-24 04:43:13.035549+00	2019-10-27 16:00:00+00	t	\N	103	3	1
206	2020-01-24 04:43:13.040908+00	2020-01-24 04:43:13.04092+00	2019-11-03 16:00:00+00	t	\N	103	3	2
207	2020-01-24 04:43:13.096297+00	2020-01-24 04:43:13.096311+00	2019-10-27 16:00:00+00	t	\N	104	3	1
208	2020-01-24 04:43:13.105427+00	2020-01-24 04:43:13.10544+00	2019-11-03 16:00:00+00	t	\N	104	3	2
209	2020-01-24 04:43:13.157899+00	2020-01-24 04:43:13.157912+00	2019-10-27 16:00:00+00	t	\N	105	3	1
210	2020-01-24 04:43:13.16339+00	2020-01-24 04:43:13.163402+00	2019-11-03 16:00:00+00	t	\N	105	3	2
211	2020-01-24 04:43:13.211627+00	2020-01-24 04:43:13.211639+00	2019-10-27 16:00:00+00	t	\N	106	3	1
212	2020-01-24 04:43:13.21704+00	2020-01-24 04:43:13.217053+00	2019-11-03 16:00:00+00	t	\N	106	3	2
213	2020-01-24 04:43:13.260293+00	2020-01-24 04:43:13.260306+00	2019-10-27 16:00:00+00	t	\N	107	3	1
214	2020-01-24 04:43:13.265743+00	2020-01-24 04:43:13.265754+00	2019-11-03 16:00:00+00	t	\N	107	3	2
215	2020-01-24 04:43:13.334523+00	2020-01-24 04:43:13.334536+00	2019-10-27 16:00:00+00	t	\N	108	3	1
216	2020-01-24 04:43:13.344244+00	2020-01-24 04:43:13.344257+00	2019-11-03 16:00:00+00	t	\N	108	3	2
217	2020-01-24 04:43:13.405053+00	2020-01-24 04:43:13.405068+00	2019-10-27 16:00:00+00	t	\N	109	3	1
218	2020-01-24 04:43:13.412216+00	2020-01-24 04:43:13.412228+00	2019-11-03 16:00:00+00	t	\N	109	3	2
219	2020-01-24 04:43:13.476609+00	2020-01-24 04:43:13.476675+00	2019-10-27 16:00:00+00	t	\N	110	3	1
220	2020-01-24 04:43:13.483607+00	2020-01-24 04:43:13.483621+00	2019-11-03 16:00:00+00	t	\N	110	3	2
221	2020-01-24 04:43:13.550197+00	2020-01-24 04:43:13.550216+00	2019-10-27 16:00:00+00	t	\N	111	3	1
222	2020-01-24 04:43:13.56149+00	2020-01-24 04:43:13.561509+00	2019-11-03 16:00:00+00	t	\N	111	3	2
223	2020-01-24 04:43:13.636912+00	2020-01-24 04:43:13.636927+00	2019-10-27 16:00:00+00	t	\N	112	3	1
224	2020-01-24 04:43:13.644552+00	2020-01-24 04:43:13.644565+00	2019-11-03 16:00:00+00	t	\N	112	3	2
225	2020-01-24 04:43:13.69515+00	2020-01-24 04:43:13.695163+00	2019-10-27 16:00:00+00	t	\N	113	3	1
226	2020-01-24 04:43:13.701748+00	2020-01-24 04:43:13.70176+00	2019-11-03 16:00:00+00	t	\N	113	3	2
227	2020-01-24 04:43:13.756828+00	2020-01-24 04:43:13.756843+00	2019-10-27 16:00:00+00	t	\N	114	3	1
228	2020-01-24 04:43:13.766133+00	2020-01-24 04:43:13.766146+00	2019-11-03 16:00:00+00	t	\N	114	3	2
229	2020-01-24 04:43:13.821149+00	2020-01-24 04:43:13.821162+00	2019-10-27 16:00:00+00	t	\N	115	3	1
230	2020-01-24 04:43:13.828494+00	2020-01-24 04:43:13.828507+00	2019-11-03 16:00:00+00	t	\N	115	3	2
231	2020-01-24 04:43:13.87783+00	2020-01-24 04:43:13.877845+00	2019-10-27 16:00:00+00	t	\N	116	3	1
232	2020-01-24 04:43:13.887999+00	2020-01-24 04:43:13.888012+00	2019-11-03 16:00:00+00	t	\N	116	3	2
233	2020-01-24 04:43:13.944601+00	2020-01-24 04:43:13.944615+00	2019-10-27 16:00:00+00	t	\N	117	3	1
234	2020-01-24 04:43:13.951717+00	2020-01-24 04:43:13.95173+00	2019-11-03 16:00:00+00	t	\N	117	3	2
235	2020-01-24 04:43:14.002366+00	2020-01-24 04:43:14.002379+00	2019-10-27 16:00:00+00	t	\N	118	3	1
236	2020-01-24 04:43:14.009225+00	2020-01-24 04:43:14.009238+00	2019-11-03 16:00:00+00	t	\N	118	3	2
237	2020-01-24 04:43:14.068565+00	2020-01-24 04:43:14.068585+00	2019-10-27 16:00:00+00	t	\N	119	3	1
238	2020-01-24 04:43:14.083318+00	2020-01-24 04:43:14.083336+00	2019-11-03 16:00:00+00	t	\N	119	3	2
239	2020-01-24 04:43:14.138241+00	2020-01-24 04:43:14.138254+00	2019-10-27 16:00:00+00	t	\N	120	3	1
240	2020-01-24 04:43:14.155388+00	2020-01-24 04:43:14.155407+00	2019-11-03 16:00:00+00	t	\N	120	3	2
241	2020-01-24 04:43:14.215377+00	2020-01-24 04:43:14.215393+00	2019-10-27 16:00:00+00	t	\N	121	3	1
242	2020-01-24 04:43:14.223436+00	2020-01-24 04:43:14.223452+00	2019-11-03 16:00:00+00	t	\N	121	3	2
243	2020-01-24 04:43:14.296722+00	2020-01-24 04:43:14.296741+00	2019-10-27 16:00:00+00	t	\N	122	3	1
244	2020-01-24 04:43:14.311551+00	2020-01-24 04:43:14.31157+00	2019-11-03 16:00:00+00	t	\N	122	3	2
245	2020-01-24 04:43:14.371921+00	2020-01-24 04:43:14.37194+00	2019-10-27 16:00:00+00	t	\N	123	3	1
246	2020-01-24 04:43:14.382729+00	2020-01-24 04:43:14.382746+00	2019-11-03 16:00:00+00	t	\N	123	3	2
247	2020-01-24 04:43:14.437538+00	2020-01-24 04:43:14.437551+00	2019-10-27 16:00:00+00	t	\N	124	3	1
248	2020-01-24 04:43:14.443739+00	2020-01-24 04:43:14.443752+00	2019-11-03 16:00:00+00	t	\N	124	3	2
249	2020-01-24 04:43:14.501675+00	2020-01-24 04:43:14.501689+00	2019-10-27 16:00:00+00	t	\N	125	3	1
250	2020-01-24 04:43:14.513014+00	2020-01-24 04:43:14.51303+00	2019-11-03 16:00:00+00	t	\N	125	3	2
251	2020-01-24 04:43:14.56701+00	2020-01-24 04:43:14.567026+00	2019-10-27 16:00:00+00	t	\N	126	3	1
252	2020-01-24 04:43:14.575873+00	2020-01-24 04:43:14.575887+00	2019-11-03 16:00:00+00	t	\N	126	3	2
253	2020-01-24 04:43:14.629456+00	2020-01-24 04:43:14.629472+00	2019-10-27 16:00:00+00	t	\N	127	3	1
254	2020-01-24 04:43:14.639412+00	2020-01-24 04:43:14.639426+00	2019-11-03 16:00:00+00	t	\N	127	3	2
255	2020-01-24 04:43:14.703303+00	2020-01-24 04:43:14.703318+00	2019-10-27 16:00:00+00	t	\N	128	3	1
256	2020-01-24 04:43:14.708863+00	2020-01-24 04:43:14.708878+00	2019-11-03 16:00:00+00	t	\N	128	3	2
257	2020-01-24 04:43:14.754178+00	2020-01-24 04:43:14.75419+00	2019-10-27 16:00:00+00	t	\N	129	3	1
258	2020-01-24 04:43:14.760945+00	2020-01-24 04:43:14.760958+00	2019-11-03 16:00:00+00	t	\N	129	3	2
259	2020-01-24 04:43:14.822192+00	2020-01-24 04:43:14.822207+00	2019-10-27 16:00:00+00	t	\N	130	3	1
260	2020-01-24 04:43:14.830617+00	2020-01-24 04:43:14.830629+00	2019-11-03 16:00:00+00	t	\N	130	3	2
261	2020-01-24 04:43:14.872341+00	2020-01-24 04:43:14.872355+00	2019-10-27 16:00:00+00	t	\N	131	3	1
262	2020-01-24 04:43:14.877572+00	2020-01-24 04:43:14.877585+00	2019-11-03 16:00:00+00	t	\N	131	3	2
263	2020-01-24 04:43:14.929473+00	2020-01-24 04:43:14.929487+00	2019-10-28 16:00:00+00	t	\N	132	3	1
264	2020-01-24 04:43:14.939927+00	2020-01-24 04:43:14.939942+00	2019-11-04 16:00:00+00	t	\N	132	3	2
265	2020-01-24 04:43:15.015059+00	2020-01-24 04:43:15.015203+00	2019-10-28 16:00:00+00	t	\N	133	3	1
266	2020-01-24 04:43:15.023883+00	2020-01-24 04:43:15.023898+00	2019-11-04 16:00:00+00	t	\N	133	3	2
267	2020-01-24 04:43:15.080704+00	2020-01-24 04:43:15.080721+00	2019-10-28 16:00:00+00	t	\N	134	3	1
268	2020-01-24 04:43:15.086865+00	2020-01-24 04:43:15.086878+00	2019-11-04 16:00:00+00	t	\N	134	3	2
269	2020-01-24 04:43:15.134003+00	2020-01-24 04:43:15.134016+00	2019-10-28 16:00:00+00	t	\N	135	3	1
270	2020-01-24 04:43:15.140355+00	2020-01-24 04:43:15.14037+00	2019-11-04 16:00:00+00	t	\N	135	3	2
271	2020-01-24 04:43:15.197844+00	2020-01-24 04:43:15.197859+00	2019-10-28 16:00:00+00	t	\N	136	3	1
272	2020-01-24 04:43:15.207791+00	2020-01-24 04:43:15.207806+00	2019-11-04 16:00:00+00	t	\N	136	3	2
273	2020-01-24 04:43:15.260584+00	2020-01-24 04:43:15.260597+00	2019-10-29 16:00:00+00	t	\N	137	3	1
274	2020-01-24 04:43:15.269823+00	2020-01-24 04:43:15.269842+00	2019-11-05 16:00:00+00	t	\N	137	3	2
275	2020-01-24 04:43:15.314274+00	2020-01-24 04:43:15.314287+00	2019-10-29 16:00:00+00	t	\N	138	3	1
276	2020-01-24 04:43:15.320261+00	2020-01-24 04:43:15.320275+00	2019-11-05 16:00:00+00	t	\N	138	3	2
277	2020-01-24 04:43:15.38053+00	2020-01-24 04:43:15.380548+00	2019-10-29 16:00:00+00	t	\N	139	3	1
278	2020-01-24 04:43:15.390756+00	2020-01-24 04:43:15.390775+00	2019-11-05 16:00:00+00	t	\N	139	3	2
279	2020-01-24 04:43:15.446989+00	2020-01-24 04:43:15.447002+00	2019-10-29 16:00:00+00	t	\N	140	3	1
280	2020-01-24 04:43:15.452707+00	2020-01-24 04:43:15.452721+00	2019-11-05 16:00:00+00	t	\N	140	3	2
281	2020-01-24 04:43:15.500568+00	2020-01-24 04:43:15.500583+00	2019-10-29 16:00:00+00	t	\N	141	3	1
282	2020-01-24 04:43:15.505972+00	2020-01-24 04:43:15.505985+00	2019-11-05 16:00:00+00	t	\N	141	3	2
283	2020-01-24 04:43:15.561161+00	2020-01-24 04:43:15.561177+00	2019-10-29 16:00:00+00	t	\N	142	3	1
284	2020-01-24 04:43:15.569049+00	2020-01-24 04:43:15.569064+00	2019-11-05 16:00:00+00	t	\N	142	3	2
285	2020-01-24 04:43:15.609293+00	2020-01-24 04:43:15.609305+00	2019-10-29 16:00:00+00	t	\N	143	3	1
286	2020-01-24 04:43:15.61528+00	2020-01-24 04:43:15.615293+00	2019-11-05 16:00:00+00	t	\N	143	3	2
287	2020-01-24 04:43:15.666294+00	2020-01-24 04:43:15.666311+00	2019-10-29 16:00:00+00	t	\N	144	3	1
288	2020-01-24 04:43:15.678704+00	2020-01-24 04:43:15.67872+00	2019-11-05 16:00:00+00	t	\N	144	3	2
289	2020-01-24 04:43:15.736046+00	2020-01-24 04:43:15.736058+00	2019-10-30 16:00:00+00	t	\N	145	3	1
290	2020-01-24 04:43:15.741877+00	2020-01-24 04:43:15.741892+00	2019-11-06 16:00:00+00	t	\N	145	3	2
291	2020-01-24 04:43:15.791459+00	2020-01-24 04:43:15.791475+00	2019-10-30 16:00:00+00	t	\N	146	3	1
292	2020-01-24 04:43:15.802319+00	2020-01-24 04:43:15.802332+00	2019-11-06 16:00:00+00	t	\N	146	3	2
293	2020-01-24 04:43:15.860507+00	2020-01-24 04:43:15.86052+00	2019-10-30 16:00:00+00	t	\N	147	3	1
294	2020-01-24 04:43:15.865712+00	2020-01-24 04:43:15.865723+00	2019-11-06 16:00:00+00	t	\N	147	3	2
295	2020-01-24 04:43:15.904137+00	2020-01-24 04:43:15.904154+00	2019-10-30 16:00:00+00	t	\N	148	3	1
296	2020-01-24 04:43:15.909364+00	2020-01-24 04:43:15.909378+00	2019-11-06 16:00:00+00	t	\N	148	3	2
297	2020-01-24 04:43:15.966156+00	2020-01-24 04:43:15.96617+00	2019-10-31 16:00:00+00	t	\N	149	3	1
298	2020-01-24 04:43:15.974963+00	2020-01-24 04:43:15.974976+00	2019-11-07 16:00:00+00	t	\N	149	3	2
299	2020-01-24 04:43:16.038234+00	2020-01-24 04:43:16.038249+00	2019-10-31 16:00:00+00	t	\N	150	3	1
300	2020-01-24 04:43:16.049565+00	2020-01-24 04:43:16.04958+00	2019-11-07 16:00:00+00	t	\N	150	3	2
301	2020-01-24 04:43:16.118354+00	2020-01-24 04:43:16.118369+00	2019-10-31 16:00:00+00	t	\N	151	3	1
302	2020-01-24 04:43:16.127097+00	2020-01-24 04:43:16.127109+00	2019-11-07 16:00:00+00	t	\N	151	3	2
303	2020-01-24 04:43:16.185671+00	2020-01-24 04:43:16.185687+00	2019-10-31 16:00:00+00	t	\N	152	3	1
304	2020-01-24 04:43:16.197679+00	2020-01-24 04:43:16.197695+00	2019-11-07 16:00:00+00	t	\N	152	3	2
305	2020-01-24 04:43:16.26249+00	2020-01-24 04:43:16.262505+00	2019-10-31 16:00:00+00	t	\N	153	3	1
306	2020-01-24 04:43:16.274262+00	2020-01-24 04:43:16.274278+00	2019-11-07 16:00:00+00	t	\N	153	3	2
307	2020-01-24 04:43:16.337314+00	2020-01-24 04:43:16.337327+00	2019-11-01 16:00:00+00	t	\N	154	3	1
308	2020-01-24 04:43:16.342436+00	2020-01-24 04:43:16.342448+00	2019-11-08 16:00:00+00	t	\N	154	3	2
309	2020-01-24 04:43:16.399243+00	2020-01-24 04:43:16.399258+00	2019-11-01 16:00:00+00	t	\N	155	3	1
310	2020-01-24 04:43:16.410749+00	2020-01-24 04:43:16.410765+00	2019-11-08 16:00:00+00	t	\N	155	3	2
311	2020-01-24 04:43:16.478223+00	2020-01-24 04:43:16.478243+00	2019-11-01 16:00:00+00	t	\N	156	3	1
312	2020-01-24 04:43:16.492045+00	2020-01-24 04:43:16.492063+00	2019-11-08 16:00:00+00	t	\N	156	3	2
313	2020-01-24 04:43:16.549244+00	2020-01-24 04:43:16.549261+00	2019-11-01 16:00:00+00	t	\N	157	3	1
314	2020-01-24 04:43:16.558733+00	2020-01-24 04:43:16.558749+00	2019-11-08 16:00:00+00	t	\N	157	3	2
315	2020-01-24 04:43:16.624884+00	2020-01-24 04:43:16.624898+00	2019-11-01 16:00:00+00	t	\N	158	3	1
316	2020-01-24 04:43:16.636578+00	2020-01-24 04:43:16.636591+00	2019-11-08 16:00:00+00	t	\N	158	3	2
317	2020-01-24 04:43:16.697123+00	2020-01-24 04:43:16.697136+00	2019-11-01 16:00:00+00	t	\N	159	3	1
318	2020-01-24 04:43:16.706134+00	2020-01-24 04:43:16.706153+00	2019-11-08 16:00:00+00	t	\N	159	3	2
319	2020-01-24 04:43:16.777505+00	2020-01-24 04:43:16.777525+00	2019-11-01 16:00:00+00	t	\N	160	3	1
320	2020-01-24 04:43:16.790297+00	2020-01-24 04:43:16.790316+00	2019-11-08 16:00:00+00	t	\N	160	3	2
321	2020-01-24 04:43:16.854254+00	2020-01-24 04:43:16.854267+00	2019-11-01 16:00:00+00	t	\N	161	3	1
322	2020-01-24 04:43:16.859264+00	2020-01-24 04:43:16.859276+00	2019-11-08 16:00:00+00	t	\N	161	3	2
323	2020-01-24 04:43:16.899861+00	2020-01-24 04:43:16.899873+00	2019-11-01 16:00:00+00	t	\N	162	3	1
324	2020-01-24 04:43:16.908805+00	2020-01-24 04:43:16.908822+00	2019-11-08 16:00:00+00	t	\N	162	3	2
325	2020-01-24 04:43:16.982267+00	2020-01-24 04:43:16.982282+00	2019-11-01 16:00:00+00	t	\N	163	3	1
326	2020-01-24 04:43:16.994055+00	2020-01-24 04:43:16.994073+00	2019-11-08 16:00:00+00	t	\N	163	3	2
327	2020-01-24 04:43:17.047701+00	2020-01-24 04:43:17.047713+00	2019-11-01 16:00:00+00	t	\N	164	3	1
328	2020-01-24 04:43:17.052675+00	2020-01-24 04:43:17.052687+00	2019-11-08 16:00:00+00	t	\N	164	3	2
329	2020-01-24 04:43:17.098233+00	2020-01-24 04:43:17.098248+00	2019-11-01 16:00:00+00	t	\N	165	3	1
330	2020-01-24 04:43:17.109326+00	2020-01-24 04:43:17.109343+00	2019-11-08 16:00:00+00	t	\N	165	3	2
331	2020-01-24 04:43:17.180836+00	2020-01-24 04:43:17.180851+00	2019-11-03 16:00:00+00	t	\N	166	4	1
332	2020-01-24 04:43:17.189892+00	2020-01-24 04:43:17.189922+00	2019-11-10 16:00:00+00	t	\N	166	4	2
333	2020-01-24 04:43:17.228501+00	2020-01-24 04:43:17.228514+00	2019-11-03 16:00:00+00	t	\N	167	4	1
334	2020-01-24 04:43:17.233927+00	2020-01-24 04:43:17.23394+00	2019-11-10 16:00:00+00	t	\N	167	4	2
335	2020-01-24 04:43:17.288581+00	2020-01-24 04:43:17.288597+00	2019-11-03 16:00:00+00	t	\N	168	4	1
336	2020-01-24 04:43:17.299902+00	2020-01-24 04:43:17.299915+00	2019-11-10 16:00:00+00	t	\N	168	4	2
337	2020-01-24 04:43:17.364401+00	2020-01-24 04:43:17.364416+00	2019-11-03 16:00:00+00	t	\N	169	4	1
338	2020-01-24 04:43:17.371484+00	2020-01-24 04:43:17.3715+00	2019-11-10 16:00:00+00	t	\N	169	4	2
339	2020-01-24 04:43:17.410881+00	2020-01-24 04:43:17.410893+00	2019-11-03 16:00:00+00	t	\N	170	4	1
340	2020-01-24 04:43:17.415682+00	2020-01-24 04:43:17.415693+00	2019-11-10 16:00:00+00	t	\N	170	4	2
341	2020-01-24 04:43:17.477549+00	2020-01-24 04:43:17.477565+00	2019-11-03 16:00:00+00	t	\N	171	4	1
342	2020-01-24 04:43:17.488731+00	2020-01-24 04:43:17.488767+00	2019-11-10 16:00:00+00	t	\N	171	4	2
343	2020-01-24 04:43:17.549613+00	2020-01-24 04:43:17.549628+00	2019-11-03 16:00:00+00	t	\N	172	4	1
344	2020-01-24 04:43:17.556474+00	2020-01-24 04:43:17.556489+00	2019-11-10 16:00:00+00	t	\N	172	4	2
345	2020-01-24 04:43:17.607699+00	2020-01-24 04:43:17.607712+00	2019-11-03 16:00:00+00	t	\N	173	4	1
346	2020-01-24 04:43:17.612553+00	2020-01-24 04:43:17.612565+00	2019-11-10 16:00:00+00	t	\N	173	4	2
347	2020-01-24 04:43:17.68064+00	2020-01-24 04:43:17.680657+00	2019-11-03 16:00:00+00	t	\N	174	4	1
348	2020-01-24 04:43:17.692296+00	2020-01-24 04:43:17.692313+00	2019-11-10 16:00:00+00	t	\N	174	4	2
349	2020-01-24 04:43:17.755857+00	2020-01-24 04:43:17.755873+00	2019-11-03 16:00:00+00	t	\N	175	4	1
350	2020-01-24 04:43:17.761004+00	2020-01-24 04:43:17.761018+00	2019-11-10 16:00:00+00	t	\N	175	4	2
351	2020-01-24 04:43:17.805347+00	2020-01-24 04:43:17.805362+00	2019-11-03 16:00:00+00	t	\N	176	4	1
352	2020-01-24 04:43:17.814678+00	2020-01-24 04:43:17.814692+00	2019-11-10 16:00:00+00	t	\N	176	4	2
353	2020-01-24 04:43:17.876908+00	2020-01-24 04:43:17.876923+00	2019-11-03 16:00:00+00	t	\N	177	4	1
354	2020-01-24 04:43:17.888302+00	2020-01-24 04:43:17.888318+00	2019-11-10 16:00:00+00	t	\N	177	4	2
355	2020-01-24 04:43:17.949069+00	2020-01-24 04:43:17.949084+00	2019-11-03 16:00:00+00	t	\N	178	4	1
356	2020-01-24 04:43:17.957149+00	2020-01-24 04:43:17.957163+00	2019-11-10 16:00:00+00	t	\N	178	4	2
357	2020-01-24 04:43:18.016405+00	2020-01-24 04:43:18.016419+00	2019-11-03 16:00:00+00	t	\N	179	4	1
358	2020-01-24 04:43:18.026238+00	2020-01-24 04:43:18.026253+00	2019-11-10 16:00:00+00	t	\N	179	4	2
359	2020-01-24 04:43:18.084643+00	2020-01-24 04:43:18.084656+00	2019-11-03 16:00:00+00	t	\N	180	4	1
360	2020-01-24 04:43:18.096153+00	2020-01-24 04:43:18.096171+00	2019-11-10 16:00:00+00	t	\N	180	4	2
361	2020-01-24 04:43:18.154816+00	2020-01-24 04:43:18.154829+00	2019-11-03 16:00:00+00	t	\N	181	4	1
362	2020-01-24 04:43:18.165017+00	2020-01-24 04:43:18.16503+00	2019-11-10 16:00:00+00	t	\N	181	4	2
363	2020-01-24 04:43:18.210456+00	2020-01-24 04:43:18.210468+00	2019-11-03 16:00:00+00	t	\N	182	4	1
364	2020-01-24 04:43:18.221123+00	2020-01-24 04:43:18.221137+00	2019-11-10 16:00:00+00	t	\N	182	4	2
365	2020-01-24 04:43:18.285149+00	2020-01-24 04:43:18.285164+00	2019-11-03 16:00:00+00	t	\N	183	4	1
366	2020-01-24 04:43:18.296724+00	2020-01-24 04:43:18.296739+00	2019-11-10 16:00:00+00	t	\N	183	4	2
367	2020-01-24 04:43:18.353992+00	2020-01-24 04:43:18.354005+00	2019-11-03 16:00:00+00	t	\N	184	4	1
368	2020-01-24 04:43:18.363881+00	2020-01-24 04:43:18.363894+00	2019-11-10 16:00:00+00	t	\N	184	4	2
369	2020-01-24 04:43:18.414046+00	2020-01-24 04:43:18.414059+00	2019-11-03 16:00:00+00	t	\N	185	4	1
370	2020-01-24 04:43:18.424878+00	2020-01-24 04:43:18.424894+00	2019-11-10 16:00:00+00	t	\N	185	4	2
371	2020-01-24 04:43:18.486167+00	2020-01-24 04:43:18.486183+00	2019-11-03 16:00:00+00	t	\N	186	4	1
372	2020-01-24 04:43:18.497112+00	2020-01-24 04:43:18.497126+00	2019-11-10 16:00:00+00	t	\N	186	4	2
373	2020-01-24 04:43:18.553394+00	2020-01-24 04:43:18.553409+00	2019-11-03 16:00:00+00	t	\N	187	4	1
374	2020-01-24 04:43:18.562463+00	2020-01-24 04:43:18.562476+00	2019-11-10 16:00:00+00	t	\N	187	4	2
375	2020-01-24 04:43:18.62533+00	2020-01-24 04:43:18.625345+00	2019-11-03 16:00:00+00	t	\N	188	4	1
376	2020-01-24 04:43:18.63331+00	2020-01-24 04:43:18.633322+00	2019-11-10 16:00:00+00	t	\N	188	4	2
377	2020-01-24 04:43:18.692614+00	2020-01-24 04:43:18.692635+00	2019-11-03 16:00:00+00	t	\N	189	4	1
378	2020-01-24 04:43:18.702181+00	2020-01-24 04:43:18.702195+00	2019-11-10 16:00:00+00	t	\N	189	4	2
379	2020-01-24 04:43:18.756534+00	2020-01-24 04:43:18.756547+00	2019-11-03 16:00:00+00	t	\N	190	4	1
380	2020-01-24 04:43:18.767646+00	2020-01-24 04:43:18.767661+00	2019-11-10 16:00:00+00	t	\N	190	4	2
381	2020-01-24 04:43:18.844842+00	2020-01-24 04:43:18.844865+00	2019-11-03 16:00:00+00	t	\N	191	4	1
382	2020-01-24 04:43:18.854257+00	2020-01-24 04:43:18.854271+00	2019-11-10 16:00:00+00	t	\N	191	4	2
383	2020-01-24 04:43:18.909677+00	2020-01-24 04:43:18.909691+00	2019-11-03 16:00:00+00	t	\N	192	4	1
384	2020-01-24 04:43:18.920985+00	2020-01-24 04:43:18.921002+00	2019-11-10 16:00:00+00	t	\N	192	4	2
385	2020-01-24 04:43:18.985023+00	2020-01-24 04:43:18.985037+00	2019-11-03 16:00:00+00	t	\N	193	4	1
386	2020-01-24 04:43:18.998409+00	2020-01-24 04:43:18.998423+00	2019-11-10 16:00:00+00	t	\N	193	4	2
387	2020-01-24 04:43:19.041557+00	2020-01-24 04:43:19.04157+00	2019-11-03 16:00:00+00	t	\N	194	4	1
388	2020-01-24 04:43:19.046674+00	2020-01-24 04:43:19.046685+00	2019-11-10 16:00:00+00	t	\N	194	4	2
389	2020-01-24 04:43:19.099455+00	2020-01-24 04:43:19.099469+00	2019-11-03 16:00:00+00	t	\N	195	4	1
390	2020-01-24 04:43:19.108056+00	2020-01-24 04:43:19.108072+00	2019-11-10 16:00:00+00	t	\N	195	4	2
391	2020-01-24 04:43:19.1757+00	2020-01-24 04:43:19.175723+00	2019-11-03 16:00:00+00	t	\N	196	4	1
392	2020-01-24 04:43:19.18806+00	2020-01-24 04:43:19.188077+00	2019-11-10 16:00:00+00	t	\N	196	4	2
393	2020-01-24 04:43:19.253688+00	2020-01-24 04:43:19.253702+00	2019-11-03 16:00:00+00	t	\N	197	4	1
394	2020-01-24 04:43:19.265845+00	2020-01-24 04:43:19.265865+00	2019-11-10 16:00:00+00	t	\N	197	4	2
395	2020-01-24 04:43:19.318085+00	2020-01-24 04:43:19.31811+00	2019-11-03 16:00:00+00	t	\N	198	4	1
396	2020-01-24 04:43:19.329664+00	2020-01-24 04:43:19.32968+00	2019-11-10 16:00:00+00	t	\N	198	4	2
397	2020-01-24 04:43:19.405126+00	2020-01-24 04:43:19.405145+00	2019-11-03 16:00:00+00	t	\N	199	4	1
398	2020-01-24 04:43:19.417041+00	2020-01-24 04:43:19.417058+00	2019-11-10 16:00:00+00	t	\N	199	4	2
399	2020-01-24 04:43:19.480395+00	2020-01-24 04:43:19.480412+00	2019-11-03 16:00:00+00	t	\N	200	4	1
400	2020-01-24 04:43:19.490523+00	2020-01-24 04:43:19.490539+00	2019-11-10 16:00:00+00	t	\N	200	4	2
401	2020-01-24 04:43:19.552428+00	2020-01-24 04:43:19.552445+00	2019-11-03 16:00:00+00	t	\N	201	4	1
402	2020-01-24 04:43:19.564037+00	2020-01-24 04:43:19.564053+00	2019-11-10 16:00:00+00	t	\N	201	4	2
403	2020-01-24 04:43:19.632826+00	2020-01-24 04:43:19.632844+00	2019-11-03 16:00:00+00	t	\N	202	4	1
404	2020-01-24 04:43:19.643923+00	2020-01-24 04:43:19.64394+00	2019-11-10 16:00:00+00	t	\N	202	4	2
405	2020-01-24 04:43:19.700377+00	2020-01-24 04:43:19.700391+00	2019-11-03 16:00:00+00	t	\N	203	4	1
406	2020-01-24 04:43:19.70642+00	2020-01-24 04:43:19.706438+00	2019-11-10 16:00:00+00	t	\N	203	4	2
407	2020-01-24 04:43:19.759019+00	2020-01-24 04:43:19.759035+00	2019-11-03 16:00:00+00	t	\N	204	4	1
408	2020-01-24 04:43:19.775267+00	2020-01-24 04:43:19.775287+00	2019-11-10 16:00:00+00	t	\N	204	4	2
409	2020-01-24 04:43:19.83157+00	2020-01-24 04:43:19.831583+00	2019-11-03 16:00:00+00	t	\N	205	4	1
410	2020-01-24 04:43:19.836997+00	2020-01-24 04:43:19.83701+00	2019-11-10 16:00:00+00	t	\N	205	4	2
411	2020-01-24 04:43:19.895862+00	2020-01-24 04:43:19.895879+00	2019-11-03 16:00:00+00	t	\N	206	4	1
412	2020-01-24 04:43:19.905469+00	2020-01-24 04:43:19.905485+00	2019-11-10 16:00:00+00	t	\N	206	4	2
413	2020-01-24 04:43:19.972084+00	2020-01-24 04:43:19.972104+00	2019-11-03 16:00:00+00	t	\N	207	4	1
414	2020-01-24 04:43:19.986426+00	2020-01-24 04:43:19.986441+00	2019-11-10 16:00:00+00	t	\N	207	4	2
415	2020-01-24 04:43:20.058136+00	2020-01-24 04:43:20.058151+00	2019-11-03 16:00:00+00	t	\N	208	4	1
416	2020-01-24 04:43:20.063518+00	2020-01-24 04:43:20.063532+00	2019-11-10 16:00:00+00	t	\N	208	4	2
417	2020-01-24 04:43:20.130674+00	2020-01-24 04:43:20.130691+00	2019-11-03 16:00:00+00	t	\N	209	4	1
418	2020-01-24 04:43:20.140327+00	2020-01-24 04:43:20.140339+00	2019-11-10 16:00:00+00	t	\N	209	4	2
419	2020-01-24 04:43:20.2336+00	2020-01-24 04:43:20.233618+00	2019-11-03 16:00:00+00	t	\N	210	4	1
420	2020-01-24 04:43:20.244161+00	2020-01-24 04:43:20.24418+00	2019-11-10 16:00:00+00	t	\N	210	4	2
421	2020-01-24 04:43:20.310132+00	2020-01-24 04:43:20.310147+00	2019-11-03 16:00:00+00	t	\N	211	4	1
422	2020-01-24 04:43:20.317157+00	2020-01-24 04:43:20.317173+00	2019-11-10 16:00:00+00	t	\N	211	4	2
423	2020-01-24 04:43:20.39417+00	2020-01-24 04:43:20.394194+00	2019-11-03 16:00:00+00	t	\N	212	4	1
424	2020-01-24 04:43:20.406971+00	2020-01-24 04:43:20.406991+00	2019-11-10 16:00:00+00	t	\N	212	4	2
425	2020-01-24 04:43:20.487326+00	2020-01-24 04:43:20.487342+00	2019-11-03 16:00:00+00	t	\N	213	4	1
426	2020-01-24 04:43:20.499865+00	2020-01-24 04:43:20.499891+00	2019-11-10 16:00:00+00	t	\N	213	4	2
427	2020-01-24 04:43:20.556553+00	2020-01-24 04:43:20.556571+00	2019-11-03 16:00:00+00	t	\N	214	4	1
428	2020-01-24 04:43:20.563489+00	2020-01-24 04:43:20.563507+00	2019-11-10 16:00:00+00	t	\N	214	4	2
429	2020-01-24 04:43:20.621664+00	2020-01-24 04:43:20.621682+00	2019-11-03 16:00:00+00	t	\N	215	4	1
430	2020-01-24 04:43:20.632958+00	2020-01-24 04:43:20.632975+00	2019-11-10 16:00:00+00	t	\N	215	4	2
431	2020-01-24 04:43:20.691302+00	2020-01-24 04:43:20.69132+00	2019-11-03 16:00:00+00	t	\N	216	4	1
432	2020-01-24 04:43:20.703686+00	2020-01-24 04:43:20.703706+00	2019-11-10 16:00:00+00	t	\N	216	4	2
433	2020-01-24 04:43:20.757373+00	2020-01-24 04:43:20.75739+00	2019-11-03 16:00:00+00	t	\N	217	4	1
434	2020-01-24 04:43:20.762591+00	2020-01-24 04:43:20.762604+00	2019-11-10 16:00:00+00	t	\N	217	4	2
435	2020-01-24 04:43:20.825777+00	2020-01-24 04:43:20.825795+00	2019-11-03 16:00:00+00	t	\N	218	4	1
436	2020-01-24 04:43:20.836602+00	2020-01-24 04:43:20.836619+00	2019-11-10 16:00:00+00	t	\N	218	4	2
437	2020-01-24 04:43:20.900992+00	2020-01-24 04:43:20.901008+00	2019-11-03 16:00:00+00	t	\N	219	4	1
438	2020-01-24 04:43:20.911063+00	2020-01-24 04:43:20.911348+00	2019-11-10 16:00:00+00	t	\N	219	4	2
439	2020-01-24 04:43:20.961153+00	2020-01-24 04:43:20.96117+00	2019-11-03 16:00:00+00	t	\N	220	4	1
440	2020-01-24 04:43:20.972437+00	2020-01-24 04:43:20.972455+00	2019-11-10 16:00:00+00	t	\N	220	4	2
441	2020-01-24 04:43:21.044182+00	2020-01-24 04:43:21.044201+00	2019-11-03 16:00:00+00	t	\N	221	4	1
442	2020-01-24 04:43:21.05476+00	2020-01-24 04:43:21.054777+00	2019-11-10 16:00:00+00	t	\N	221	4	2
443	2020-01-24 04:43:21.135366+00	2020-01-24 04:43:21.13538+00	2019-11-03 16:00:00+00	t	\N	222	4	1
444	2020-01-24 04:43:21.145305+00	2020-01-24 04:43:21.14532+00	2019-11-10 16:00:00+00	t	\N	222	4	2
445	2020-01-24 04:43:21.193248+00	2020-01-24 04:43:21.193263+00	2019-11-03 16:00:00+00	t	\N	223	4	1
446	2020-01-24 04:43:21.203604+00	2020-01-24 04:43:21.203622+00	2019-11-10 16:00:00+00	t	\N	223	4	2
447	2020-01-24 04:43:21.260486+00	2020-01-24 04:43:21.2605+00	2019-11-03 16:00:00+00	t	\N	224	4	1
448	2020-01-24 04:43:21.270487+00	2020-01-24 04:43:21.270501+00	2019-11-10 16:00:00+00	t	\N	224	4	2
449	2020-01-24 04:43:21.328673+00	2020-01-24 04:43:21.328687+00	2019-11-04 16:00:00+00	t	\N	225	4	1
450	2020-01-24 04:43:21.338496+00	2020-01-24 04:43:21.33851+00	2019-11-11 16:00:00+00	t	\N	225	4	2
451	2020-01-24 04:43:21.402536+00	2020-01-24 04:43:21.402554+00	2019-11-04 16:00:00+00	t	\N	226	4	1
452	2020-01-24 04:43:21.41375+00	2020-01-24 04:43:21.413765+00	2019-11-11 16:00:00+00	t	\N	226	4	2
453	2020-01-24 04:43:21.469223+00	2020-01-24 04:43:21.469239+00	2019-11-04 16:00:00+00	t	\N	227	4	1
454	2020-01-24 04:43:21.480996+00	2020-01-24 04:43:21.481014+00	2019-11-11 16:00:00+00	t	\N	227	4	2
455	2020-01-24 04:43:21.553412+00	2020-01-24 04:43:21.553432+00	2019-11-04 16:00:00+00	t	\N	228	4	1
456	2020-01-24 04:43:21.564519+00	2020-01-24 04:43:21.564536+00	2019-11-11 16:00:00+00	t	\N	228	4	2
457	2020-01-24 04:43:21.631494+00	2020-01-24 04:43:21.631513+00	2019-11-04 16:00:00+00	t	\N	229	4	1
458	2020-01-24 04:43:21.642876+00	2020-01-24 04:43:21.642896+00	2019-11-11 16:00:00+00	t	\N	229	4	2
459	2020-01-24 04:43:21.69875+00	2020-01-24 04:43:21.698762+00	2019-11-04 16:00:00+00	t	\N	230	4	1
460	2020-01-24 04:43:21.708876+00	2020-01-24 04:43:21.708891+00	2019-11-11 16:00:00+00	t	\N	230	4	2
461	2020-01-24 04:43:21.760734+00	2020-01-24 04:43:21.760751+00	2019-11-04 16:00:00+00	t	\N	231	4	1
462	2020-01-24 04:43:21.770623+00	2020-01-24 04:43:21.77064+00	2019-11-11 16:00:00+00	t	\N	231	4	2
463	2020-01-24 04:43:21.82748+00	2020-01-24 04:43:21.827496+00	2019-11-04 16:00:00+00	t	\N	232	4	1
464	2020-01-24 04:43:21.837411+00	2020-01-24 04:43:21.837426+00	2019-11-11 16:00:00+00	t	\N	232	4	2
465	2020-01-24 04:43:21.897571+00	2020-01-24 04:43:21.897588+00	2019-11-04 16:00:00+00	t	\N	233	4	1
466	2020-01-24 04:43:21.906966+00	2020-01-24 04:43:21.906983+00	2019-11-11 16:00:00+00	t	\N	233	4	2
467	2020-01-24 04:43:21.963354+00	2020-01-24 04:43:21.963369+00	2019-11-05 16:00:00+00	t	\N	234	4	1
468	2020-01-24 04:43:21.969482+00	2020-01-24 04:43:21.969498+00	2019-11-12 16:00:00+00	t	\N	234	4	2
469	2020-01-24 04:43:22.027839+00	2020-01-24 04:43:22.027856+00	2019-11-05 16:00:00+00	t	\N	235	4	1
470	2020-01-24 04:43:22.037622+00	2020-01-24 04:43:22.037636+00	2019-11-12 16:00:00+00	t	\N	235	4	2
471	2020-01-24 04:43:22.103672+00	2020-01-24 04:43:22.103691+00	2019-11-06 16:00:00+00	t	\N	236	4	1
472	2020-01-24 04:43:22.113871+00	2020-01-24 04:43:22.113888+00	2019-11-13 16:00:00+00	t	\N	236	4	2
473	2020-01-24 04:43:22.171947+00	2020-01-24 04:43:22.172007+00	2019-11-06 16:00:00+00	t	\N	237	4	1
474	2020-01-24 04:43:22.180667+00	2020-01-24 04:43:22.180683+00	2019-11-13 16:00:00+00	t	\N	237	4	2
475	2020-01-24 04:43:22.25578+00	2020-01-24 04:43:22.255799+00	2019-11-07 16:00:00+00	t	\N	238	4	1
476	2020-01-24 04:43:22.266148+00	2020-01-24 04:43:22.266165+00	2019-11-14 16:00:00+00	t	\N	238	4	2
477	2020-01-24 04:43:22.326467+00	2020-01-24 04:43:22.326487+00	2019-11-07 16:00:00+00	t	\N	239	4	1
478	2020-01-24 04:43:22.34081+00	2020-01-24 04:43:22.340829+00	2019-11-14 16:00:00+00	t	\N	239	4	2
479	2020-01-24 04:43:22.402371+00	2020-01-24 04:43:22.402385+00	2019-11-07 16:00:00+00	t	\N	240	4	1
480	2020-01-24 04:43:22.407559+00	2020-01-24 04:43:22.407574+00	2019-11-14 16:00:00+00	t	\N	240	4	2
\.


--
-- Data for Name: sows_events_ultrasoundtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_ultrasoundtype (id, created_at, modified_at, title, days, final) FROM stdin;
1	2020-01-24 04:41:26.315814+00	2020-01-24 04:41:26.315831+00	\N	30	f
2	2020-01-24 04:41:26.31586+00	2020-01-24 04:41:26.315865+00	\N	60	t
\.


--
-- Data for Name: sows_events_weaningsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_weaningsow (id, created_at, modified_at, date, quantity, initiator_id, piglets_id, sow_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_gilt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_gilt (id, created_at, modified_at, birth_id, farrow_id, location_id, mother_sow_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_sow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_sow (id, created_at, modified_at, birth_id, farm_id, alive, location_id, status_id, tour_id) FROM stdin;
13	2020-01-24 04:43:06.477223+00	2020-01-24 05:27:58.260298+00	\N	19598	t	39	4	1
6	2020-01-24 04:43:05.91444+00	2020-01-24 05:47:15.590663+00	\N	2481	t	69	4	1
18	2020-01-24 04:43:06.868734+00	2020-01-24 06:27:43.420466+00	\N	18834	t	219	4	1
47	2020-01-24 04:43:09.134749+00	2020-01-24 06:33:51.572018+00	\N	19634	t	263	4	2
33	2020-01-24 04:43:08.122639+00	2020-01-24 06:35:17.949519+00	\N	18919	t	265	4	2
48	2020-01-24 04:43:09.187564+00	2020-01-24 06:38:02.752473+00	\N	19170	t	266	4	2
37	2020-01-24 04:43:08.383999+00	2020-01-24 06:38:16.103753+00	\N	19781	t	267	4	2
38	2020-01-24 04:43:08.488885+00	2020-01-24 06:39:17.881464+00	\N	19765	t	268	4	2
44	2020-01-24 04:43:08.941997+00	2020-01-24 06:39:33.648284+00	\N	19721	t	269	4	2
31	2020-01-24 04:43:07.875697+00	2020-01-24 06:40:44.014597+00	\N	19150	t	273	4	2
30	2020-01-24 04:43:07.826256+00	2020-01-24 06:41:26.360978+00	\N	20100	t	275	4	2
28	2020-01-24 04:43:07.684139+00	2020-01-24 06:41:35.650148+00	\N	20099	t	276	4	2
29	2020-01-24 04:43:07.751209+00	2020-01-24 06:41:59.173536+00	\N	20101	t	277	4	2
27	2020-01-24 04:43:07.62497+00	2020-01-24 06:42:27.104913+00	\N	20096	t	278	4	2
43	2020-01-24 04:43:08.828609+00	2020-01-24 06:42:36.049962+00	\N	19743	t	279	4	2
3	2020-01-24 04:43:05.692806+00	2020-01-24 04:43:05.763154+00	\N	20081	t	3	4	1
42	2020-01-24 04:43:08.742297+00	2020-01-24 06:43:08.092139+00	\N	19763	t	282	4	2
35	2020-01-24 04:43:08.262065+00	2020-01-24 06:43:23.024029+00	\N	19761	t	283	4	2
46	2020-01-24 04:43:09.060782+00	2020-01-24 06:43:48.839825+00	\N	19682	t	284	4	2
32	2020-01-24 04:43:07.981979+00	2020-01-24 06:43:57.138137+00	\N	19247	t	285	4	2
39	2020-01-24 04:43:08.549361+00	2020-01-24 06:44:05.709913+00	\N	2510	t	286	4	2
19	2020-01-24 04:43:06.950675+00	2020-01-24 06:45:38.976211+00	\N	20092	t	248	4	1
5	2020-01-24 04:43:05.839749+00	2020-01-24 06:45:48.244635+00	\N	20083	t	249	4	1
16	2020-01-24 04:43:06.725274+00	2020-01-24 06:45:59.7091+00	\N	19706	t	251	4	1
8	2020-01-24 04:43:06.099903+00	2020-01-24 06:46:09.750326+00	\N	20086	t	252	4	1
9	2020-01-24 04:43:06.168382+00	2020-01-24 06:46:23.384712+00	\N	20091	t	254	4	1
14	2020-01-24 04:43:06.557302+00	2020-01-24 06:46:31.199638+00	\N	20093	t	255	4	1
21	2020-01-24 04:43:07.114166+00	2020-01-24 06:46:59.381795+00	\N	20095	t	258	4	1
2	2020-01-24 04:43:05.598133+00	2020-01-24 06:47:13.354593+00	\N	20082	t	259	4	1
1	2020-01-24 04:43:05.481961+00	2020-01-24 06:47:24.011378+00	\N	20084	t	260	4	1
4	2020-01-24 04:43:05.772692+00	2020-01-24 06:47:33.171652+00	\N	20085	t	261	4	1
17	2020-01-24 04:43:06.803923+00	2020-01-24 06:48:04.550871+00	\N	19631	t	239	4	1
15	2020-01-24 04:43:06.636309+00	2020-01-24 06:48:32.046836+00	\N	20008	t	240	4	1
24	2020-01-24 04:43:07.350148+00	2020-01-24 06:49:13.056441+00	\N	20097	t	241	4	1
12	2020-01-24 04:43:06.403374+00	2020-01-24 06:49:49.408097+00	\N	20087	t	242	4	1
22	2020-01-24 04:43:07.210164+00	2020-01-24 06:50:05.843273+00	\N	19698	t	243	4	1
20	2020-01-24 04:43:07.018932+00	2020-01-24 06:50:29.932379+00	\N	20094	t	244	4	1
7	2020-01-24 04:43:06.002819+00	2020-01-24 04:43:06.08971+00	\N	20088	t	3	4	1
23	2020-01-24 04:43:07.281034+00	2020-01-24 06:50:46.236666+00	\N	5120	t	245	4	1
10	2020-01-24 04:43:06.256679+00	2020-01-24 04:43:06.319682+00	\N	20089	t	3	4	1
11	2020-01-24 04:43:06.329911+00	2020-01-24 04:43:06.396543+00	\N	20090	t	3	4	1
25	2020-01-24 04:43:07.440661+00	2020-01-24 04:43:07.51587+00	\N	2634	t	3	4	2
26	2020-01-24 04:43:07.521273+00	2020-01-24 04:43:07.620543+00	\N	20098	t	3	4	2
34	2020-01-24 04:43:08.174289+00	2020-01-24 04:43:08.255264+00	\N	2524	t	3	4	2
36	2020-01-24 04:43:08.328819+00	2020-01-24 04:43:08.377166+00	\N	19767	t	3	4	2
40	2020-01-24 04:43:08.612465+00	2020-01-24 04:43:08.663012+00	\N	18334	t	3	4	2
41	2020-01-24 04:43:08.667446+00	2020-01-24 04:43:08.735531+00	\N	19748	t	3	4	2
45	2020-01-24 04:43:09.008988+00	2020-01-24 04:43:09.054008+00	\N	2543	t	3	4	2
84	2020-01-24 04:43:11.69238+00	2020-01-24 05:21:18.606036+00	\N	20114	t	30	4	2
76	2020-01-24 04:43:11.169338+00	2020-01-24 05:21:29.748767+00	\N	20108	t	29	4	2
49	2020-01-24 04:43:09.25866+00	2020-01-24 04:43:09.315904+00	\N	19581	t	3	4	2
82	2020-01-24 04:43:11.5407+00	2020-01-24 05:21:59.421526+00	\N	20112	t	27	4	2
71	2020-01-24 04:43:10.819798+00	2020-01-24 05:22:11.215371+00	\N	20107	t	26	4	2
62	2020-01-24 04:43:10.162298+00	2020-01-24 05:22:21.085587+00	\N	20104	t	25	4	2
83	2020-01-24 04:43:11.616975+00	2020-01-24 05:26:39.19583+00	\N	20115	t	35	4	2
72	2020-01-24 04:43:10.888058+00	2020-01-24 05:26:49.886933+00	\N	20105	t	36	4	2
56	2020-01-24 04:43:09.750967+00	2020-01-24 06:39:53.425612+00	\N	18405	t	270	4	2
79	2020-01-24 04:43:11.341836+00	2020-01-24 05:27:18.480903+00	\N	19681	t	37	4	2
81	2020-01-24 04:43:11.478681+00	2020-01-24 05:28:11.304348+00	\N	20103	t	40	4	2
78	2020-01-24 04:43:11.29315+00	2020-01-24 05:32:15.495008+00	\N	19786	t	34	4	2
91	2020-01-24 04:43:12.16973+00	2020-01-24 05:33:34.231945+00	\N	17916	t	48	4	3
90	2020-01-24 04:43:12.104242+00	2020-01-24 05:36:20.924787+00	\N	19231	t	50	4	3
51	2020-01-24 04:43:09.395511+00	2020-01-24 04:43:09.456727+00	\N	20102	t	3	4	2
92	2020-01-24 04:43:12.245194+00	2020-01-24 05:39:00.304916+00	\N	20120	t	54	4	3
95	2020-01-24 04:43:12.460368+00	2020-01-24 05:42:15.307671+00	\N	20121	t	60	4	3
96	2020-01-24 04:43:12.549957+00	2020-01-24 05:43:42.593377+00	\N	20119	t	61	4	3
93	2020-01-24 04:43:12.327983+00	2020-01-24 05:46:16.796036+00	\N	20117	t	67	4	3
65	2020-01-24 04:43:10.386122+00	2020-01-24 06:32:29.738855+00	\N	19749	t	256	4	2
52	2020-01-24 04:43:09.464136+00	2020-01-24 04:43:09.533095+00	\N	18087	t	3	4	2
74	2020-01-24 04:43:11.026225+00	2020-01-24 06:33:36.502012+00	\N	19683	t	262	4	2
75	2020-01-24 04:43:11.096348+00	2020-01-24 06:35:00.046165+00	\N	18290	t	264	4	2
63	2020-01-24 04:43:10.234243+00	2020-01-24 06:35:41.206493+00	\N	19823	t	250	4	2
50	2020-01-24 04:43:09.324589+00	2020-01-24 06:36:06.304263+00	\N	18384	t	253	4	2
58	2020-01-24 04:43:09.882172+00	2020-01-24 06:40:17.359445+00	\N	19397	t	271	4	2
57	2020-01-24 04:43:09.806145+00	2020-01-24 06:40:30.630706+00	\N	5075	t	272	4	2
67	2020-01-24 04:43:10.534014+00	2020-01-24 06:41:03.829344+00	\N	20111	t	274	4	2
60	2020-01-24 04:43:10.00791+00	2020-01-24 06:42:47.05027+00	\N	19386	t	280	4	2
87	2020-01-24 04:43:11.905508+00	2020-01-24 06:42:55.377618+00	\N	5107	t	281	4	2
73	2020-01-24 04:43:10.962104+00	2020-01-24 06:44:12.656653+00	\N	19239	t	287	4	2
54	2020-01-24 04:43:09.606896+00	2020-01-24 04:43:09.672603+00	\N	19419	t	3	4	2
68	2020-01-24 04:43:10.602508+00	2020-01-24 06:44:23.238977+00	\N	19069	t	288	4	2
77	2020-01-24 04:43:11.224591+00	2020-01-24 06:44:39.866014+00	\N	20109	t	290	4	2
64	2020-01-24 04:43:10.30668+00	2020-01-24 06:44:49.358835+00	\N	2521	t	291	4	2
80	2020-01-24 04:43:11.398159+00	2020-01-24 06:45:01.414609+00	\N	20110	t	292	4	2
53	2020-01-24 04:43:09.539924+00	2020-01-24 06:51:22.03983+00	\N	19013	t	246	4	2
55	2020-01-24 04:43:09.679737+00	2020-01-24 04:43:09.744185+00	\N	18599	t	3	4	2
59	2020-01-24 04:43:09.952336+00	2020-01-24 04:43:10.00089+00	\N	19431	t	3	4	2
61	2020-01-24 04:43:10.077721+00	2020-01-24 04:43:10.155371+00	\N	2633	t	3	4	2
66	2020-01-24 04:43:10.464476+00	2020-01-24 04:43:10.526504+00	\N	19668	t	3	4	2
69	2020-01-24 04:43:10.679451+00	2020-01-24 04:43:10.741512+00	\N	2735	t	3	4	2
70	2020-01-24 04:43:10.753782+00	2020-01-24 04:43:10.812495+00	\N	20106	t	3	4	2
85	2020-01-24 04:43:11.745317+00	2020-01-24 04:43:11.825026+00	\N	20116	t	3	4	2
86	2020-01-24 04:43:11.832577+00	2020-01-24 04:43:11.900913+00	\N	20113	t	3	4	2
88	2020-01-24 04:43:11.958161+00	2020-01-24 04:43:12.01508+00	\N	19775	t	3	4	2
89	2020-01-24 04:43:12.022528+00	2020-01-24 04:43:12.096674+00	\N	2329	t	3	4	2
94	2020-01-24 04:43:12.400778+00	2020-01-24 04:43:12.452727+00	\N	20052	t	3	4	3
97	2020-01-24 04:43:12.6194+00	2020-01-24 04:43:12.693957+00	\N	20118	t	3	4	3
127	2020-01-24 04:43:14.595327+00	2020-01-24 05:21:06.44237+00	\N	19325	t	31	4	3
125	2020-01-24 04:43:14.4559+00	2020-01-24 05:21:44.865963+00	\N	19464	t	28	4	3
115	2020-01-24 04:43:13.786787+00	2020-01-24 05:22:33.80736+00	\N	19178	t	24	4	3
105	2020-01-24 04:43:13.121349+00	2020-01-24 05:22:42.253006+00	\N	19809	t	23	4	3
104	2020-01-24 04:43:13.0532+00	2020-01-24 05:28:35.782955+00	\N	19783	t	41	4	3
101	2020-01-24 04:43:12.876032+00	2020-01-24 06:44:30.126377+00	\N	19785	t	289	4	3
113	2020-01-24 04:43:13.658528+00	2020-01-24 05:28:54.233213+00	\N	18112	t	42	4	3
131	2020-01-24 04:43:14.842287+00	2020-01-24 05:29:10.165207+00	\N	18878	t	43	4	3
106	2020-01-24 04:43:13.175401+00	2020-01-24 05:29:24.061285+00	\N	19804	t	44	4	3
111	2020-01-24 04:43:13.501318+00	2020-01-24 05:30:34.924139+00	\N	19792	t	45	4	3
110	2020-01-24 04:43:13.43576+00	2020-01-24 05:31:52.439798+00	\N	19707	t	46	4	3
99	2020-01-24 04:43:12.757546+00	2020-01-24 04:43:12.808347+00	\N	19789	t	3	4	3
128	2020-01-24 04:43:14.65706+00	2020-01-24 05:33:19.185814+00	\N	18723	t	47	4	3
129	2020-01-24 04:43:14.719514+00	2020-01-24 05:33:53.959078+00	\N	18625	t	49	4	3
118	2020-01-24 04:43:13.964629+00	2020-01-24 05:37:32.037783+00	\N	18299	t	51	4	3
121	2020-01-24 04:43:14.170884+00	2020-01-24 05:38:08.858119+00	\N	18225	t	52	4	3
108	2020-01-24 04:43:13.284376+00	2020-01-24 05:38:35.876967+00	\N	19776	t	53	4	3
123	2020-01-24 04:43:14.33082+00	2020-01-24 05:39:52.520596+00	\N	19447	t	55	4	3
124	2020-01-24 04:43:14.40245+00	2020-01-24 05:40:22.719832+00	\N	19460	t	56	4	3
98	2020-01-24 04:43:12.701166+00	2020-01-24 05:40:52.000212+00	\N	19822	t	57	4	3
100	2020-01-24 04:43:12.813265+00	2020-01-24 05:41:23.035324+00	\N	19778	t	58	4	3
114	2020-01-24 04:43:13.718541+00	2020-01-24 05:41:46.365535+00	\N	19734	t	59	4	3
122	2020-01-24 04:43:14.242125+00	2020-01-24 05:44:00.13483+00	\N	19794	t	62	4	3
107	2020-01-24 04:43:13.227952+00	2020-01-24 05:44:15.181838+00	\N	19769	t	63	4	3
117	2020-01-24 04:43:13.90533+00	2020-01-24 05:45:21.874436+00	\N	19793	t	65	4	3
109	2020-01-24 04:43:13.360302+00	2020-01-24 05:45:39.679397+00	\N	19777	t	66	4	3
139	2020-01-24 04:43:15.334601+00	2020-01-24 06:00:54.96145+00	\N	20124	t	94	4	3
102	2020-01-24 04:43:12.941723+00	2020-01-24 04:43:13.001295+00	\N	19787	t	3	4	3
143	2020-01-24 04:43:15.580034+00	2020-01-24 06:01:13.950758+00	\N	2463	t	93	4	3
136	2020-01-24 04:43:15.155174+00	2020-01-24 06:04:04.023394+00	\N	2602	t	95	4	3
142	2020-01-24 04:43:15.522084+00	2020-01-24 06:04:25.334819+00	\N	18996	t	96	4	3
138	2020-01-24 04:43:15.282143+00	2020-01-24 06:11:20.1163+00	\N	20123	t	105	4	3
137	2020-01-24 04:43:15.224313+00	2020-01-24 06:12:07.599039+00	\N	20038	t	109	4	3
103	2020-01-24 04:43:13.006049+00	2020-01-24 04:43:13.046427+00	\N	19824	t	3	4	3
141	2020-01-24 04:43:15.464032+00	2020-01-24 06:12:50.002093+00	\N	18597	t	111	4	3
134	2020-01-24 04:43:15.03933+00	2020-01-24 06:13:03.364276+00	\N	19828	t	112	4	3
112	2020-01-24 04:43:13.582683+00	2020-01-24 04:43:13.653087+00	\N	2594	t	3	4	3
116	2020-01-24 04:43:13.841226+00	2020-01-24 04:43:13.898195+00	\N	2487	t	3	4	3
119	2020-01-24 04:43:14.02642+00	2020-01-24 04:43:14.093603+00	\N	18463	t	3	4	3
120	2020-01-24 04:43:14.101015+00	2020-01-24 04:43:14.163953+00	\N	19687	t	3	4	3
126	2020-01-24 04:43:14.531239+00	2020-01-24 04:43:14.586482+00	\N	19451	t	3	4	3
130	2020-01-24 04:43:14.778597+00	2020-01-24 04:43:14.837618+00	\N	2698	t	3	4	3
132	2020-01-24 04:43:14.888751+00	2020-01-24 04:43:14.964227+00	\N	20122	t	3	4	3
133	2020-01-24 04:43:14.971568+00	2020-01-24 04:43:15.032716+00	\N	19172	t	3	4	3
135	2020-01-24 04:43:15.100043+00	2020-01-24 04:43:15.148591+00	\N	2663	t	3	4	3
140	2020-01-24 04:43:15.409773+00	2020-01-24 04:43:15.458947+00	\N	2504	t	3	4	3
144	2020-01-24 04:43:15.62547+00	2020-01-24 04:43:15.690163+00	\N	20070	t	3	4	3
145	2020-01-24 04:43:15.697845+00	2020-01-24 04:43:15.748492+00	\N	19964	t	3	4	3
147	2020-01-24 04:43:15.821449+00	2020-01-24 05:25:20.023996+00	\N	19145	t	32	4	3
154	2020-01-24 04:43:16.295915+00	2020-01-24 05:25:35.099005+00	\N	20134	t	33	4	3
161	2020-01-24 04:43:16.810242+00	2020-01-24 05:27:40.752224+00	\N	20133	t	38	4	3
153	2020-01-24 04:43:16.217763+00	2020-01-24 05:44:57.946513+00	\N	20072	t	64	4	3
189	2020-01-24 04:43:18.650062+00	2020-01-24 05:47:00.035224+00	\N	19810	t	68	4	4
176	2020-01-24 04:43:17.771065+00	2020-01-24 05:47:36.227981+00	\N	2635	t	70	4	4
166	2020-01-24 04:43:17.128383+00	2020-01-24 05:51:33.059189+00	\N	2616	t	73	4	4
174	2020-01-24 04:43:17.628549+00	2020-01-24 05:52:08.559517+00	\N	20143	t	74	4	4
177	2020-01-24 04:43:17.832944+00	2020-01-24 05:56:56.392023+00	\N	2654	t	81	4	4
187	2020-01-24 04:43:18.515574+00	2020-01-24 05:57:07.531201+00	\N	19814	t	82	4	4
178	2020-01-24 04:43:17.910798+00	2020-01-24 06:00:29.691584+00	\N	19811	t	85	4	4
157	2020-01-24 04:43:16.511712+00	2020-01-24 06:01:25.490469+00	\N	20136	t	92	4	3
149	2020-01-24 04:43:15.922597+00	2020-01-24 06:01:39.823061+00	\N	20126	t	91	4	3
155	2020-01-24 04:43:16.355576+00	2020-01-24 06:01:51.225857+00	\N	20130	t	90	4	3
162	2020-01-24 04:43:16.870958+00	2020-01-24 06:02:01.853747+00	\N	20132	t	89	4	3
186	2020-01-24 04:43:18.443806+00	2020-01-24 06:02:13.744862+00	\N	19805	t	88	4	4
152	2020-01-24 04:43:16.141347+00	2020-01-24 06:04:39.275617+00	\N	19716	t	97	4	3
158	2020-01-24 04:43:16.580238+00	2020-01-24 06:04:52.230951+00	\N	20129	t	98	4	3
151	2020-01-24 04:43:16.072869+00	2020-01-24 06:05:10.556933+00	\N	19758	t	99	4	3
159	2020-01-24 04:43:16.656085+00	2020-01-24 06:07:47.787178+00	\N	20135	t	100	4	3
164	2020-01-24 04:43:17.013354+00	2020-01-24 06:08:27.36695+00	\N	19660	t	101	4	3
150	2020-01-24 04:43:15.994328+00	2020-01-24 06:08:44.333597+00	\N	20127	t	102	4	3
148	2020-01-24 04:43:15.876357+00	2020-01-24 06:08:57.747875+00	\N	20125	t	103	4	3
146	2020-01-24 04:43:15.752824+00	2020-01-24 06:10:01.056097+00	\N	19650	t	104	4	3
156	2020-01-24 04:43:16.430762+00	2020-01-24 06:11:32.213345+00	\N	20128	t	106	4	3
160	2020-01-24 04:43:16.729152+00	2020-01-24 06:11:43.881662+00	\N	20131	t	107	4	3
163	2020-01-24 04:43:16.930111+00	2020-01-24 06:11:54.40971+00	\N	19736	t	108	4	3
165	2020-01-24 04:43:17.063537+00	2020-01-24 06:12:23.973133+00	\N	5016	t	110	4	3
167	2020-01-24 04:43:17.200029+00	2020-01-24 04:43:17.239852+00	\N	2643	t	3	4	4
168	2020-01-24 04:43:17.244104+00	2020-01-24 04:43:17.311951+00	\N	20140	t	3	4	4
169	2020-01-24 04:43:17.321864+00	2020-01-24 04:43:17.378451+00	\N	20138	t	3	4	4
170	2020-01-24 04:43:17.382907+00	2020-01-24 04:43:17.425352+00	\N	5048	t	3	4	4
171	2020-01-24 04:43:17.431703+00	2020-01-24 04:43:17.500151+00	\N	20142	t	3	4	4
172	2020-01-24 04:43:17.507844+00	2020-01-24 04:43:17.569548+00	\N	19435	t	3	4	4
173	2020-01-24 04:43:17.578577+00	2020-01-24 04:43:17.622148+00	\N	20139	t	3	4	4
175	2020-01-24 04:43:17.711655+00	2020-01-24 04:43:17.766479+00	\N	20071	t	3	4	4
179	2020-01-24 04:43:17.974171+00	2020-01-24 04:43:18.037355+00	\N	18842	t	3	4	4
180	2020-01-24 04:43:18.04476+00	2020-01-24 04:43:18.106695+00	\N	19813	t	3	4	4
181	2020-01-24 04:43:18.114384+00	2020-01-24 04:43:18.175531+00	\N	19799	t	3	4	4
182	2020-01-24 04:43:18.182525+00	2020-01-24 04:43:18.233318+00	\N	19779	t	3	4	4
183	2020-01-24 04:43:18.241141+00	2020-01-24 04:43:18.308464+00	\N	19797	t	3	4	4
184	2020-01-24 04:43:18.315985+00	2020-01-24 04:43:18.374579+00	\N	19806	t	3	4	4
185	2020-01-24 04:43:18.382099+00	2020-01-24 04:43:18.436634+00	\N	19800	t	3	4	4
188	2020-01-24 04:43:18.582405+00	2020-01-24 04:43:18.642771+00	\N	19219	t	3	4	4
190	2020-01-24 04:43:18.718707+00	2020-01-24 04:43:18.781708+00	\N	19817	t	3	4	4
191	2020-01-24 04:43:18.789256+00	2020-01-24 04:43:18.864361+00	\N	19825	t	3	4	4
192	2020-01-24 04:43:18.873089+00	2020-01-24 04:43:18.932715+00	\N	19798	t	3	4	4
193	2020-01-24 04:43:18.940656+00	2020-01-24 04:43:19.009727+00	\N	19670	t	3	4	4
194	2020-01-24 04:43:19.014176+00	2020-01-24 04:43:19.052383+00	\N	19725	t	3	4	4
216	2020-01-24 04:43:20.651952+00	2020-01-24 05:50:31.90157+00	\N	2729	t	71	4	4
201	2020-01-24 04:43:19.505894+00	2020-01-24 05:50:48.480202+00	\N	19456	t	72	4	4
223	2020-01-24 04:43:21.160439+00	2020-01-24 05:52:38.193595+00	\N	19272	t	75	4	4
214	2020-01-24 04:43:20.51841+00	2020-01-24 05:52:56.306546+00	\N	19410	t	76	4	4
204	2020-01-24 04:43:19.716948+00	2020-01-24 05:55:15.183096+00	\N	5049	t	77	4	4
195	2020-01-24 04:43:19.05718+00	2020-01-24 04:43:19.120494+00	\N	19712	t	3	4	4
202	2020-01-24 04:43:19.585111+00	2020-01-24 05:55:28.551102+00	\N	18422	t	78	4	4
209	2020-01-24 04:43:20.085426+00	2020-01-24 05:55:40.200198+00	\N	19474	t	79	4	4
218	2020-01-24 04:43:20.784691+00	2020-01-24 05:56:45.881548+00	\N	18277	t	80	4	4
210	2020-01-24 04:43:20.160766+00	2020-01-24 05:57:19.25628+00	\N	19423	t	83	4	4
206	2020-01-24 04:43:19.850252+00	2020-01-24 05:58:37.568274+00	\N	2320	t	84	4	4
196	2020-01-24 04:43:19.128394+00	2020-01-24 04:43:19.203462+00	\N	17895	t	3	4	4
203	2020-01-24 04:43:19.661607+00	2020-01-24 06:02:30.237292+00	\N	19455	t	87	4	4
200	2020-01-24 04:43:19.435979+00	2020-01-24 06:13:42.273658+00	\N	19481	t	113	4	4
197	2020-01-24 04:43:19.210461+00	2020-01-24 04:43:19.276295+00	\N	19575	t	3	4	4
198	2020-01-24 04:43:19.281383+00	2020-01-24 04:43:19.342349+00	\N	19478	t	3	4	4
199	2020-01-24 04:43:19.350243+00	2020-01-24 04:43:19.428806+00	\N	18428	t	3	4	4
205	2020-01-24 04:43:19.795493+00	2020-01-24 04:43:19.843608+00	\N	2624	t	3	4	4
207	2020-01-24 04:43:19.925395+00	2020-01-24 04:43:20.012422+00	\N	19467	t	3	4	4
208	2020-01-24 04:43:20.020358+00	2020-01-24 04:43:20.077979+00	\N	19489	t	3	4	4
211	2020-01-24 04:43:20.262959+00	2020-01-24 04:43:20.323797+00	\N	2733	t	3	4	4
212	2020-01-24 04:43:20.330595+00	2020-01-24 04:43:20.421147+00	\N	2736	t	3	4	4
213	2020-01-24 04:43:20.430601+00	2020-01-24 04:43:20.513287+00	\N	5028	t	3	4	4
215	2020-01-24 04:43:20.581839+00	2020-01-24 04:43:20.64433+00	\N	5100	t	3	4	4
217	2020-01-24 04:43:20.724056+00	2020-01-24 04:43:20.776886+00	\N	18839	t	3	4	4
219	2020-01-24 04:43:20.856948+00	2020-01-24 04:43:20.922828+00	\N	5088	t	3	4	4
220	2020-01-24 04:43:20.929007+00	2020-01-24 04:43:20.986041+00	\N	5001	t	3	4	4
221	2020-01-24 04:43:20.998744+00	2020-01-24 04:43:21.068049+00	\N	20137	t	3	4	4
222	2020-01-24 04:43:21.094894+00	2020-01-24 04:43:21.155553+00	\N	19308	t	3	4	4
224	2020-01-24 04:43:21.221419+00	2020-01-24 04:43:21.281828+00	\N	19312	t	3	4	4
225	2020-01-24 04:43:21.288755+00	2020-01-24 04:43:21.348819+00	\N	20144	t	3	4	4
226	2020-01-24 04:43:21.356057+00	2020-01-24 04:43:21.424626+00	\N	20146	t	3	4	4
227	2020-01-24 04:43:21.431592+00	2020-01-24 04:43:21.491372+00	\N	19746	t	3	4	4
228	2020-01-24 04:43:21.498118+00	2020-01-24 04:43:21.576438+00	\N	18322	t	3	4	4
229	2020-01-24 04:43:21.584485+00	2020-01-24 04:43:21.654385+00	\N	18234	t	3	4	4
230	2020-01-24 04:43:21.661396+00	2020-01-24 04:43:21.718899+00	\N	19022	t	3	4	4
231	2020-01-24 04:43:21.7258+00	2020-01-24 04:43:21.77763+00	\N	20145	t	3	4	4
232	2020-01-24 04:43:21.786336+00	2020-01-24 04:43:21.84897+00	\N	19400	t	3	4	4
233	2020-01-24 04:43:21.856658+00	2020-01-24 04:43:21.917344+00	\N	2726	t	3	4	4
234	2020-01-24 04:43:21.92471+00	2020-01-24 04:43:21.97722+00	\N	20147	t	3	4	4
235	2020-01-24 04:43:21.984266+00	2020-01-24 04:43:22.049002+00	\N	19711	t	3	4	4
236	2020-01-24 04:43:22.056562+00	2020-01-24 04:43:22.123944+00	\N	20148	t	3	4	4
237	2020-01-24 04:43:22.131144+00	2020-01-24 04:43:22.188743+00	\N	19679	t	3	4	4
238	2020-01-24 04:43:22.196593+00	2020-01-24 04:43:22.278215+00	\N	2637	t	3	4	4
239	2020-01-24 04:43:22.284497+00	2020-01-24 04:43:22.350807+00	\N	20153	t	3	4	4
240	2020-01-24 04:43:22.362861+00	2020-01-24 04:43:22.418591+00	\N	20150	t	3	4	4
\.


--
-- Data for Name: sows_sowstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_sowstatus (id, created_at, modified_at, title) FROM stdin;
1	2020-01-24 04:41:23.589949+00	2020-01-24 04:41:23.590001+00	Осеменена 1
2	2020-01-24 04:41:23.590015+00	2020-01-24 04:41:23.590021+00	Осеменена 2
3	2020-01-24 04:41:23.590029+00	2020-01-24 04:41:23.590033+00	Супорос 28
4	2020-01-24 04:41:23.590041+00	2020-01-24 04:41:23.590045+00	Супорос 35
5	2020-01-24 04:41:23.590103+00	2020-01-24 04:41:23.590109+00	Прохолост
6	2020-01-24 04:41:23.590117+00	2020-01-24 04:41:23.590121+00	Аборт
7	2020-01-24 04:41:23.590129+00	2020-01-24 04:41:23.590134+00	Отъем
8	2020-01-24 04:41:23.590141+00	2020-01-24 04:41:23.590146+00	Брак
9	2020-01-24 04:41:23.590153+00	2020-01-24 04:41:23.590158+00	Опоросилась
10	2020-01-24 04:41:23.590165+00	2020-01-24 04:41:23.59019+00	Кормилица
11	2020-01-24 04:41:23.590199+00	2020-01-24 04:41:23.590204+00	Ожидает осеменения
\.


--
-- Data for Name: staff_workshopemployee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY staff_workshopemployee (id, created_at, modified_at, farm_name, is_officer, is_seminator, user_id, workshop_id) FROM stdin;
1	2020-01-24 04:41:23.932733+00	2020-01-24 04:41:23.932748+00	АДМ	t	t	2	1
2	2020-01-24 04:41:24.089967+00	2020-01-24 04:41:24.089981+00	ОФИЦЕР	t	t	3	1
3	2020-01-24 04:41:24.243368+00	2020-01-24 04:41:24.243384+00	ШМЫГИ	f	t	4	1
4	2020-01-24 04:41:24.39735+00	2020-01-24 04:41:24.397365+00	БОРИС	f	t	5	1
5	2020-01-24 04:41:24.555874+00	2020-01-24 04:41:24.55589+00	СЕМЕН	f	t	6	1
6	2020-01-24 04:41:24.725781+00	2020-01-24 04:41:24.725849+00	ГАРИ	t	t	7	1
7	2020-01-24 04:41:24.887354+00	2020-01-24 04:41:24.887425+00	ИВАНО	f	t	8	1
8	2020-01-24 04:41:25.157866+00	2020-01-24 04:41:25.157881+00	СТУДЕ	f	t	9	1
9	2020-01-24 04:41:25.317544+00	2020-01-24 04:41:25.317563+00	ИВАНО	f	f	10	1
10	2020-01-24 04:41:25.493777+00	2020-01-24 04:41:25.493801+00	ИВАНО	f	f	11	2
11	2020-01-24 04:41:25.652563+00	2020-01-24 04:41:25.652579+00	ИВАНО	f	f	12	3
12	2020-01-24 04:41:25.809308+00	2020-01-24 04:41:25.809325+00	ИВАНО	f	f	13	4
13	2020-01-24 04:41:25.967902+00	2020-01-24 04:41:25.967919+00	ИВАНО	f	f	14	5
14	2020-01-24 04:41:26.137629+00	2020-01-24 04:41:26.137645+00	ИВАНО	f	f	15	6
15	2020-01-24 04:41:26.295815+00	2020-01-24 04:41:26.295832+00	ИВАНО	f	f	16	7
\.


--
-- Data for Name: tours_metatour; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tours_metatour (id, created_at, modified_at, piglets_id) FROM stdin;
\.


--
-- Data for Name: tours_metatourrecord; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tours_metatourrecord (id, created_at, modified_at, quantity, percentage, metatour_id, tour_id) FROM stdin;
\.


--
-- Data for Name: tours_tour; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tours_tour (id, created_at, modified_at, start_date, week_number, year) FROM stdin;
1	2020-01-24 04:43:05.485901+00	2020-01-24 04:43:05.485913+00	2020-01-24 04:43:05.485657+00	38	2019
2	2020-01-24 04:43:07.446364+00	2020-01-24 04:43:07.446377+00	2020-01-24 04:43:07.446148+00	39	2019
3	2020-01-24 04:43:12.109213+00	2020-01-24 04:43:12.109227+00	2020-01-24 04:43:12.108997+00	40	2019
4	2020-01-24 04:43:17.133728+00	2020-01-24 04:43:17.133741+00	2020-01-24 04:43:17.133522+00	41	2019
\.


--
-- Data for Name: transactions_pigletstransaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transactions_pigletstransaction (id, created_at, modified_at, date, from_location_id, initiator_id, piglets_group_id, to_location_id) FROM stdin;
\.


--
-- Data for Name: transactions_sowtransaction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY transactions_sowtransaction (id, created_at, modified_at, date, from_location_id, initiator_id, sow_id, to_location_id) FROM stdin;
1	2020-01-24 05:21:06.432753+00	2020-01-24 05:21:06.432772+00	2020-01-24 05:21:06.431297+00	3	12	127	31
2	2020-01-24 05:21:18.60344+00	2020-01-24 05:21:18.60346+00	2020-01-24 05:21:18.601665+00	3	12	84	30
3	2020-01-24 05:21:29.743358+00	2020-01-24 05:21:29.743377+00	2020-01-24 05:21:29.741488+00	3	12	76	29
4	2020-01-24 05:21:44.863261+00	2020-01-24 05:21:44.863282+00	2020-01-24 05:21:44.861918+00	3	12	125	28
5	2020-01-24 05:21:59.419311+00	2020-01-24 05:21:59.419329+00	2020-01-24 05:21:59.417712+00	3	12	82	27
6	2020-01-24 05:22:11.211431+00	2020-01-24 05:22:11.211451+00	2020-01-24 05:22:11.209943+00	3	12	71	26
7	2020-01-24 05:22:21.080812+00	2020-01-24 05:22:21.080878+00	2020-01-24 05:22:21.071577+00	3	12	62	25
8	2020-01-24 05:22:33.804958+00	2020-01-24 05:22:33.804975+00	2020-01-24 05:22:33.803626+00	3	12	115	24
9	2020-01-24 05:22:42.250606+00	2020-01-24 05:22:42.250625+00	2020-01-24 05:22:42.249166+00	3	12	105	23
10	2020-01-24 05:25:20.0214+00	2020-01-24 05:25:20.021417+00	2020-01-24 05:25:20.020153+00	3	12	147	32
11	2020-01-24 05:25:35.092639+00	2020-01-24 05:25:35.092663+00	2020-01-24 05:25:35.087405+00	3	12	154	33
12	2020-01-24 05:26:39.189338+00	2020-01-24 05:26:39.189364+00	2020-01-24 05:26:39.187846+00	3	12	83	35
13	2020-01-24 05:26:49.884312+00	2020-01-24 05:26:49.884331+00	2020-01-24 05:26:49.882789+00	3	12	72	36
14	2020-01-24 05:27:18.478074+00	2020-01-24 05:27:18.478093+00	2020-01-24 05:27:18.476736+00	3	12	79	37
15	2020-01-24 05:27:40.741866+00	2020-01-24 05:27:40.741902+00	2020-01-24 05:27:40.733811+00	3	12	161	38
16	2020-01-24 05:27:58.253773+00	2020-01-24 05:27:58.253791+00	2020-01-24 05:27:58.252485+00	3	12	13	39
17	2020-01-24 05:28:11.301549+00	2020-01-24 05:28:11.301569+00	2020-01-24 05:28:11.299646+00	3	12	81	40
18	2020-01-24 05:28:35.778808+00	2020-01-24 05:28:35.778829+00	2020-01-24 05:28:35.776188+00	3	12	104	41
19	2020-01-24 05:28:54.23082+00	2020-01-24 05:28:54.230838+00	2020-01-24 05:28:54.229544+00	3	12	113	42
20	2020-01-24 05:29:10.160437+00	2020-01-24 05:29:10.160456+00	2020-01-24 05:29:10.158806+00	3	12	131	43
21	2020-01-24 05:29:24.057765+00	2020-01-24 05:29:24.057785+00	2020-01-24 05:29:24.055354+00	3	12	106	44
22	2020-01-24 05:30:34.921295+00	2020-01-24 05:30:34.921316+00	2020-01-24 05:30:34.918563+00	3	12	111	45
23	2020-01-24 05:31:52.436222+00	2020-01-24 05:31:52.43625+00	2020-01-24 05:31:52.430082+00	3	12	110	46
24	2020-01-24 05:32:15.491294+00	2020-01-24 05:32:15.491314+00	2020-01-24 05:32:15.489595+00	3	12	78	34
25	2020-01-24 05:33:19.174921+00	2020-01-24 05:33:19.174941+00	2020-01-24 05:33:19.173351+00	3	12	128	47
26	2020-01-24 05:33:34.227889+00	2020-01-24 05:33:34.22791+00	2020-01-24 05:33:34.226057+00	3	12	91	48
27	2020-01-24 05:33:53.956509+00	2020-01-24 05:33:53.956532+00	2020-01-24 05:33:53.947752+00	3	12	129	49
28	2020-01-24 05:36:20.921823+00	2020-01-24 05:36:20.921841+00	2020-01-24 05:36:20.920469+00	3	12	90	50
29	2020-01-24 05:37:32.035231+00	2020-01-24 05:37:32.035251+00	2020-01-24 05:37:32.03375+00	3	12	118	51
30	2020-01-24 05:38:08.855875+00	2020-01-24 05:38:08.855893+00	2020-01-24 05:38:08.85428+00	3	12	121	52
31	2020-01-24 05:38:35.874347+00	2020-01-24 05:38:35.874365+00	2020-01-24 05:38:35.872978+00	3	12	108	53
32	2020-01-24 05:39:00.301781+00	2020-01-24 05:39:00.301799+00	2020-01-24 05:39:00.300414+00	3	12	92	54
33	2020-01-24 05:39:52.517031+00	2020-01-24 05:39:52.517052+00	2020-01-24 05:39:52.515008+00	3	12	123	55
34	2020-01-24 05:40:22.717176+00	2020-01-24 05:40:22.717199+00	2020-01-24 05:40:22.714561+00	3	12	124	56
35	2020-01-24 05:40:51.997659+00	2020-01-24 05:40:51.997677+00	2020-01-24 05:40:51.995675+00	3	12	98	57
36	2020-01-24 05:41:23.0168+00	2020-01-24 05:41:23.01682+00	2020-01-24 05:41:23.01516+00	3	12	100	58
37	2020-01-24 05:41:46.362546+00	2020-01-24 05:41:46.362566+00	2020-01-24 05:41:46.361184+00	3	12	114	59
38	2020-01-24 05:42:15.303121+00	2020-01-24 05:42:15.303142+00	2020-01-24 05:42:15.299069+00	3	12	95	60
39	2020-01-24 05:43:42.583298+00	2020-01-24 05:43:42.583321+00	2020-01-24 05:43:42.579949+00	3	12	96	61
40	2020-01-24 05:44:00.12853+00	2020-01-24 05:44:00.128671+00	2020-01-24 05:44:00.126896+00	3	12	122	62
41	2020-01-24 05:44:15.177665+00	2020-01-24 05:44:15.177685+00	2020-01-24 05:44:15.176374+00	3	12	107	63
42	2020-01-24 05:44:57.943555+00	2020-01-24 05:44:57.943588+00	2020-01-24 05:44:57.94211+00	3	12	153	64
43	2020-01-24 05:45:21.870025+00	2020-01-24 05:45:21.870144+00	2020-01-24 05:45:21.863442+00	3	12	117	65
44	2020-01-24 05:45:39.676976+00	2020-01-24 05:45:39.676995+00	2020-01-24 05:45:39.675647+00	3	12	109	66
45	2020-01-24 05:46:16.792387+00	2020-01-24 05:46:16.792406+00	2020-01-24 05:46:16.790883+00	3	12	93	67
46	2020-01-24 05:47:00.03032+00	2020-01-24 05:47:00.030345+00	2020-01-24 05:47:00.028734+00	3	12	189	68
47	2020-01-24 05:47:15.587954+00	2020-01-24 05:47:15.587974+00	2020-01-24 05:47:15.586651+00	3	12	6	69
48	2020-01-24 05:47:36.21331+00	2020-01-24 05:47:36.21333+00	2020-01-24 05:47:36.209659+00	3	12	176	70
49	2020-01-24 05:50:31.897795+00	2020-01-24 05:50:31.897819+00	2020-01-24 05:50:31.895797+00	3	12	216	71
50	2020-01-24 05:50:48.477852+00	2020-01-24 05:50:48.47787+00	2020-01-24 05:50:48.476563+00	3	12	201	72
51	2020-01-24 05:51:33.056239+00	2020-01-24 05:51:33.05626+00	2020-01-24 05:51:33.054077+00	3	12	166	73
52	2020-01-24 05:52:08.557293+00	2020-01-24 05:52:08.557311+00	2020-01-24 05:52:08.555945+00	3	12	174	74
53	2020-01-24 05:52:38.190988+00	2020-01-24 05:52:38.191006+00	2020-01-24 05:52:38.189681+00	3	12	223	75
54	2020-01-24 05:52:56.30164+00	2020-01-24 05:52:56.301659+00	2020-01-24 05:52:56.299733+00	3	12	214	76
55	2020-01-24 05:55:15.180588+00	2020-01-24 05:55:15.180608+00	2020-01-24 05:55:15.17924+00	3	12	204	77
56	2020-01-24 05:55:28.546517+00	2020-01-24 05:55:28.546536+00	2020-01-24 05:55:28.544942+00	3	12	202	78
57	2020-01-24 05:55:40.194948+00	2020-01-24 05:55:40.194967+00	2020-01-24 05:55:40.1936+00	3	12	209	79
58	2020-01-24 05:56:45.871649+00	2020-01-24 05:56:45.87168+00	2020-01-24 05:56:45.868979+00	3	12	218	80
59	2020-01-24 05:56:56.386584+00	2020-01-24 05:56:56.386607+00	2020-01-24 05:56:56.383083+00	3	12	177	81
60	2020-01-24 05:57:07.526581+00	2020-01-24 05:57:07.526598+00	2020-01-24 05:57:07.525281+00	3	12	187	82
61	2020-01-24 05:57:19.253673+00	2020-01-24 05:57:19.253692+00	2020-01-24 05:57:19.252049+00	3	12	210	83
62	2020-01-24 05:58:37.56199+00	2020-01-24 05:58:37.562016+00	2020-01-24 05:58:37.558564+00	3	12	206	84
63	2020-01-24 06:00:29.689009+00	2020-01-24 06:00:29.689028+00	2020-01-24 06:00:29.687689+00	3	12	178	85
64	2020-01-24 06:00:54.953551+00	2020-01-24 06:00:54.953573+00	2020-01-24 06:00:54.951146+00	3	12	139	94
65	2020-01-24 06:01:13.944837+00	2020-01-24 06:01:13.944859+00	2020-01-24 06:01:13.941697+00	3	12	143	93
66	2020-01-24 06:01:25.487792+00	2020-01-24 06:01:25.487811+00	2020-01-24 06:01:25.4861+00	3	12	157	92
67	2020-01-24 06:01:39.820535+00	2020-01-24 06:01:39.820556+00	2020-01-24 06:01:39.818927+00	3	12	149	91
68	2020-01-24 06:01:51.221669+00	2020-01-24 06:01:51.22169+00	2020-01-24 06:01:51.219683+00	3	12	155	90
69	2020-01-24 06:02:01.841574+00	2020-01-24 06:02:01.8416+00	2020-01-24 06:02:01.835654+00	3	12	162	89
70	2020-01-24 06:02:13.742572+00	2020-01-24 06:02:13.74259+00	2020-01-24 06:02:13.741311+00	3	12	186	88
71	2020-01-24 06:02:30.231525+00	2020-01-24 06:02:30.231547+00	2020-01-24 06:02:30.229819+00	3	12	203	87
72	2020-01-24 06:04:04.020545+00	2020-01-24 06:04:04.020564+00	2020-01-24 06:04:04.018303+00	3	12	136	95
73	2020-01-24 06:04:25.332517+00	2020-01-24 06:04:25.332535+00	2020-01-24 06:04:25.330832+00	3	12	142	96
74	2020-01-24 06:04:39.273172+00	2020-01-24 06:04:39.273189+00	2020-01-24 06:04:39.271688+00	3	12	152	97
75	2020-01-24 06:04:52.228723+00	2020-01-24 06:04:52.228741+00	2020-01-24 06:04:52.227366+00	3	12	158	98
76	2020-01-24 06:05:10.554543+00	2020-01-24 06:05:10.554561+00	2020-01-24 06:05:10.55325+00	3	12	151	99
77	2020-01-24 06:07:47.784304+00	2020-01-24 06:07:47.784322+00	2020-01-24 06:07:47.783016+00	3	12	159	100
78	2020-01-24 06:08:27.364527+00	2020-01-24 06:08:27.364544+00	2020-01-24 06:08:27.362991+00	3	12	164	101
79	2020-01-24 06:08:44.331117+00	2020-01-24 06:08:44.331134+00	2020-01-24 06:08:44.329801+00	3	12	150	102
80	2020-01-24 06:08:57.745678+00	2020-01-24 06:08:57.745708+00	2020-01-24 06:08:57.74396+00	3	12	148	103
81	2020-01-24 06:10:01.05215+00	2020-01-24 06:10:01.052176+00	2020-01-24 06:10:01.049189+00	3	12	146	104
82	2020-01-24 06:11:20.113378+00	2020-01-24 06:11:20.113396+00	2020-01-24 06:11:20.112093+00	3	12	138	105
83	2020-01-24 06:11:32.21077+00	2020-01-24 06:11:32.210788+00	2020-01-24 06:11:32.209478+00	3	12	156	106
84	2020-01-24 06:11:43.876158+00	2020-01-24 06:11:43.876178+00	2020-01-24 06:11:43.874802+00	3	12	160	107
85	2020-01-24 06:11:54.406383+00	2020-01-24 06:11:54.4064+00	2020-01-24 06:11:54.404959+00	3	12	163	108
86	2020-01-24 06:12:07.596757+00	2020-01-24 06:12:07.596777+00	2020-01-24 06:12:07.594324+00	3	12	137	109
87	2020-01-24 06:12:23.969818+00	2020-01-24 06:12:23.969837+00	2020-01-24 06:12:23.96843+00	3	12	165	110
88	2020-01-24 06:12:49.997922+00	2020-01-24 06:12:49.997945+00	2020-01-24 06:12:49.996077+00	3	12	141	111
89	2020-01-24 06:13:03.359574+00	2020-01-24 06:13:03.359591+00	2020-01-24 06:13:03.358147+00	3	12	134	112
90	2020-01-24 06:13:42.270429+00	2020-01-24 06:13:42.270446+00	2020-01-24 06:13:42.269087+00	3	12	200	113
91	2020-01-24 06:27:43.41554+00	2020-01-24 06:27:43.415558+00	2020-01-24 06:27:43.414092+00	3	12	18	219
92	2020-01-24 06:32:29.735589+00	2020-01-24 06:32:29.735607+00	2020-01-24 06:32:29.732329+00	3	12	65	256
93	2020-01-24 06:33:36.499467+00	2020-01-24 06:33:36.499487+00	2020-01-24 06:33:36.498031+00	3	12	74	262
94	2020-01-24 06:33:51.569188+00	2020-01-24 06:33:51.569218+00	2020-01-24 06:33:51.567625+00	3	12	47	263
95	2020-01-24 06:35:00.042772+00	2020-01-24 06:35:00.042791+00	2020-01-24 06:35:00.040868+00	3	12	75	264
96	2020-01-24 06:35:17.945939+00	2020-01-24 06:35:17.945957+00	2020-01-24 06:35:17.944367+00	3	12	33	265
97	2020-01-24 06:35:41.203953+00	2020-01-24 06:35:41.203976+00	2020-01-24 06:35:41.201837+00	3	12	63	250
98	2020-01-24 06:36:06.301773+00	2020-01-24 06:36:06.301796+00	2020-01-24 06:36:06.299472+00	3	12	50	253
99	2020-01-24 06:38:02.747183+00	2020-01-24 06:38:02.747205+00	2020-01-24 06:38:02.738917+00	3	12	48	266
100	2020-01-24 06:38:16.098899+00	2020-01-24 06:38:16.098988+00	2020-01-24 06:38:16.09559+00	3	12	37	267
101	2020-01-24 06:39:17.878915+00	2020-01-24 06:39:17.878934+00	2020-01-24 06:39:17.877606+00	3	12	38	268
102	2020-01-24 06:39:33.643952+00	2020-01-24 06:39:33.644213+00	2020-01-24 06:39:33.639122+00	3	12	44	269
103	2020-01-24 06:39:53.423239+00	2020-01-24 06:39:53.423281+00	2020-01-24 06:39:53.421293+00	3	12	56	270
104	2020-01-24 06:40:17.332355+00	2020-01-24 06:40:17.332374+00	2020-01-24 06:40:17.3309+00	3	12	58	271
105	2020-01-24 06:40:30.628058+00	2020-01-24 06:40:30.628077+00	2020-01-24 06:40:30.626633+00	3	12	57	272
106	2020-01-24 06:40:44.010639+00	2020-01-24 06:40:44.010655+00	2020-01-24 06:40:44.009375+00	3	12	31	273
107	2020-01-24 06:41:03.826903+00	2020-01-24 06:41:03.826923+00	2020-01-24 06:41:03.824841+00	3	12	67	274
108	2020-01-24 06:41:26.35643+00	2020-01-24 06:41:26.356447+00	2020-01-24 06:41:26.355135+00	3	12	30	275
109	2020-01-24 06:41:35.64404+00	2020-01-24 06:41:35.644061+00	2020-01-24 06:41:35.640939+00	3	12	28	276
110	2020-01-24 06:41:59.170783+00	2020-01-24 06:41:59.170805+00	2020-01-24 06:41:59.167895+00	3	12	29	277
111	2020-01-24 06:42:27.102516+00	2020-01-24 06:42:27.102534+00	2020-01-24 06:42:27.10081+00	3	12	27	278
112	2020-01-24 06:42:36.047285+00	2020-01-24 06:42:36.047302+00	2020-01-24 06:42:36.046046+00	3	12	43	279
113	2020-01-24 06:42:47.047033+00	2020-01-24 06:42:47.047051+00	2020-01-24 06:42:47.0449+00	3	12	60	280
114	2020-01-24 06:42:55.374958+00	2020-01-24 06:42:55.374978+00	2020-01-24 06:42:55.371851+00	3	12	87	281
115	2020-01-24 06:43:08.088954+00	2020-01-24 06:43:08.088975+00	2020-01-24 06:43:08.086384+00	3	12	42	282
116	2020-01-24 06:43:23.019774+00	2020-01-24 06:43:23.019795+00	2020-01-24 06:43:23.009883+00	3	12	35	283
117	2020-01-24 06:43:48.833809+00	2020-01-24 06:43:48.833827+00	2020-01-24 06:43:48.832388+00	3	12	46	284
118	2020-01-24 06:43:57.135491+00	2020-01-24 06:43:57.135511+00	2020-01-24 06:43:57.134126+00	3	12	32	285
119	2020-01-24 06:44:05.69964+00	2020-01-24 06:44:05.699678+00	2020-01-24 06:44:05.689009+00	3	12	39	286
120	2020-01-24 06:44:12.653681+00	2020-01-24 06:44:12.653703+00	2020-01-24 06:44:12.651736+00	3	12	73	287
121	2020-01-24 06:44:23.23458+00	2020-01-24 06:44:23.234599+00	2020-01-24 06:44:23.232961+00	3	12	68	288
122	2020-01-24 06:44:30.123325+00	2020-01-24 06:44:30.123345+00	2020-01-24 06:44:30.121803+00	3	12	101	289
123	2020-01-24 06:44:39.862323+00	2020-01-24 06:44:39.862344+00	2020-01-24 06:44:39.860633+00	3	12	77	290
124	2020-01-24 06:44:49.356311+00	2020-01-24 06:44:49.356327+00	2020-01-24 06:44:49.355002+00	3	12	64	291
125	2020-01-24 06:45:01.408104+00	2020-01-24 06:45:01.408152+00	2020-01-24 06:45:01.394973+00	3	12	80	292
126	2020-01-24 06:45:38.973083+00	2020-01-24 06:45:38.973101+00	2020-01-24 06:45:38.97171+00	3	12	19	248
127	2020-01-24 06:45:48.242219+00	2020-01-24 06:45:48.242236+00	2020-01-24 06:45:48.240715+00	3	12	5	249
128	2020-01-24 06:45:59.706604+00	2020-01-24 06:45:59.706624+00	2020-01-24 06:45:59.704971+00	3	12	16	251
129	2020-01-24 06:46:09.74784+00	2020-01-24 06:46:09.747859+00	2020-01-24 06:46:09.746176+00	3	12	8	252
130	2020-01-24 06:46:23.382539+00	2020-01-24 06:46:23.382559+00	2020-01-24 06:46:23.381258+00	3	12	9	254
131	2020-01-24 06:46:31.197106+00	2020-01-24 06:46:31.197124+00	2020-01-24 06:46:31.195675+00	3	12	14	255
132	2020-01-24 06:46:59.378779+00	2020-01-24 06:46:59.378798+00	2020-01-24 06:46:59.376771+00	3	12	21	258
133	2020-01-24 06:47:13.352173+00	2020-01-24 06:47:13.352192+00	2020-01-24 06:47:13.350801+00	3	12	2	259
134	2020-01-24 06:47:24.006618+00	2020-01-24 06:47:24.00664+00	2020-01-24 06:47:24.001918+00	3	12	1	260
135	2020-01-24 06:47:33.169231+00	2020-01-24 06:47:33.169427+00	2020-01-24 06:47:33.167893+00	3	12	4	261
136	2020-01-24 06:48:04.546696+00	2020-01-24 06:48:04.546723+00	2020-01-24 06:48:04.544681+00	3	12	17	239
137	2020-01-24 06:48:32.044299+00	2020-01-24 06:48:32.044316+00	2020-01-24 06:48:32.042949+00	3	12	15	240
138	2020-01-24 06:49:13.054134+00	2020-01-24 06:49:13.054152+00	2020-01-24 06:49:13.052847+00	3	12	24	241
139	2020-01-24 06:49:49.405905+00	2020-01-24 06:49:49.405923+00	2020-01-24 06:49:49.404394+00	3	12	12	242
140	2020-01-24 06:50:05.839196+00	2020-01-24 06:50:05.839215+00	2020-01-24 06:50:05.837321+00	3	12	22	243
141	2020-01-24 06:50:29.928238+00	2020-01-24 06:50:29.928257+00	2020-01-24 06:50:29.926872+00	3	12	20	244
142	2020-01-24 06:50:46.234332+00	2020-01-24 06:50:46.23435+00	2020-01-24 06:50:46.232708+00	3	12	23	245
143	2020-01-24 06:51:22.037145+00	2020-01-24 06:51:22.037169+00	2020-01-24 06:51:22.03577+00	3	12	53	246
\.


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_permission_id_seq', 148, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 16, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 1, false);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 37, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_migrations_id_seq', 30, true);


--
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_location_id_seq', 425, true);


--
-- Name: locations_pigletsgroupcell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_pigletsgroupcell_id_seq', 106, true);


--
-- Name: locations_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_section_id_seq', 38, true);


--
-- Name: locations_sowandpigletscell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowandpigletscell_id_seq', 270, true);


--
-- Name: locations_sowgroupcell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowgroupcell_id_seq', 1, false);


--
-- Name: locations_sowgroupcell_sows_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowgroupcell_sows_id_seq', 1, false);


--
-- Name: locations_sowsinglecell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowsinglecell_id_seq', 1, false);


--
-- Name: locations_workshop_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_workshop_id_seq', 11, true);


--
-- Name: piglets_events_cullingpiglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_cullingpiglets_id_seq', 1, false);


--
-- Name: piglets_events_pigletsmerger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_pigletsmerger_id_seq', 1, false);


--
-- Name: piglets_events_pigletssplit_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_pigletssplit_id_seq', 1, false);


--
-- Name: piglets_events_weighingpiglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_weighingpiglets_id_seq', 1, false);


--
-- Name: piglets_piglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_piglets_id_seq', 1, false);


--
-- Name: piglets_pigletsstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_pigletsstatus_id_seq', 5, true);


--
-- Name: sows_boar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_boar_id_seq', 12, true);


--
-- Name: sows_events_abortionsow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_abortionsow_id_seq', 1, false);


--
-- Name: sows_events_cullingsow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_cullingsow_id_seq', 1, false);


--
-- Name: sows_events_semination_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_semination_id_seq', 480, true);


--
-- Name: sows_events_sowfarrow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_sowfarrow_id_seq', 1, false);


--
-- Name: sows_events_ultrasound_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_ultrasound_id_seq', 480, true);


--
-- Name: sows_events_ultrasoundtype_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_ultrasoundtype_id_seq', 2, true);


--
-- Name: sows_events_weaningsow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_weaningsow_id_seq', 1, false);


--
-- Name: sows_gilt_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_gilt_id_seq', 1, false);


--
-- Name: sows_sow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_sow_id_seq', 240, true);


--
-- Name: sows_sowstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_sowstatus_id_seq', 11, true);


--
-- Name: staff_workshopemployee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('staff_workshopemployee_id_seq', 15, true);


--
-- Name: tours_metatour_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tours_metatour_id_seq', 1, false);


--
-- Name: tours_metatourrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tours_metatourrecord_id_seq', 1, false);


--
-- Name: tours_tour_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tours_tour_id_seq', 4, true);


--
-- Name: transactions_pigletstransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transactions_pigletstransaction_id_seq', 1, false);


--
-- Name: transactions_sowtransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transactions_sowtransaction_id_seq', 143, true);


--
-- Name: auth_group auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions auth_group_permissions_group_id_permission_id_0cd325b0_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_permission_id_0cd325b0_uniq UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_permission auth_permission_content_type_id_codename_01ab375a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_codename_01ab375a_uniq UNIQUE (content_type_id, codename);


--
-- Name: auth_permission auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups auth_user_groups_user_id_group_id_94350c0c_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_group_id_94350c0c_uniq UNIQUE (user_id, group_id);


--
-- Name: auth_user auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_permission_id_14a6b632_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_permission_id_14a6b632_uniq UNIQUE (user_id, permission_id);


--
-- Name: auth_user auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: authtoken_token authtoken_token_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_pkey PRIMARY KEY (key);


--
-- Name: authtoken_token authtoken_token_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_key UNIQUE (user_id);


--
-- Name: django_admin_log django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_content_type django_content_type_app_label_model_76bd3d3b_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_model_76bd3d3b_uniq UNIQUE (app_label, model);


--
-- Name: django_content_type django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_migrations django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: django_session django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: locations_location locations_location_pigletsGroupCell_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_pigletsGroupCell_id_key" UNIQUE ("pigletsGroupCell_id");


--
-- Name: locations_location locations_location_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT locations_location_pkey PRIMARY KEY (id);


--
-- Name: locations_location locations_location_section_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT locations_location_section_id_key UNIQUE (section_id);


--
-- Name: locations_location locations_location_sowAndPigletsCell_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowAndPigletsCell_id_key" UNIQUE ("sowAndPigletsCell_id");


--
-- Name: locations_location locations_location_sowGroupCell_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowGroupCell_id_key" UNIQUE ("sowGroupCell_id");


--
-- Name: locations_location locations_location_sowSingleCell_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowSingleCell_id_key" UNIQUE ("sowSingleCell_id");


--
-- Name: locations_location locations_location_workshop_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT locations_location_workshop_id_key UNIQUE (workshop_id);


--
-- Name: locations_pigletsgroupcell locations_pigletsgroupcell_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_pigletsgroupcell
    ADD CONSTRAINT locations_pigletsgroupcell_pkey PRIMARY KEY (id);


--
-- Name: locations_section locations_section_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_section
    ADD CONSTRAINT locations_section_pkey PRIMARY KEY (id);


--
-- Name: locations_sowandpigletscell locations_sowandpigletscell_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowandpigletscell
    ADD CONSTRAINT locations_sowandpigletscell_pkey PRIMARY KEY (id);


--
-- Name: locations_sowgroupcell locations_sowgroupcell_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell
    ADD CONSTRAINT locations_sowgroupcell_pkey PRIMARY KEY (id);


--
-- Name: locations_sowgroupcell_sows locations_sowgroupcell_s_sowgroupcell_id_sow_id_a10f9e7a_uniq; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell_sows
    ADD CONSTRAINT locations_sowgroupcell_s_sowgroupcell_id_sow_id_a10f9e7a_uniq UNIQUE (sowgroupcell_id, sow_id);


--
-- Name: locations_sowgroupcell_sows locations_sowgroupcell_sows_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell_sows
    ADD CONSTRAINT locations_sowgroupcell_sows_pkey PRIMARY KEY (id);


--
-- Name: locations_sowsinglecell locations_sowsinglecell_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowsinglecell
    ADD CONSTRAINT locations_sowsinglecell_pkey PRIMARY KEY (id);


--
-- Name: locations_workshop locations_workshop_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_workshop
    ADD CONSTRAINT locations_workshop_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_cullingpiglets piglets_events_cullingpiglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingpiglets
    ADD CONSTRAINT piglets_events_cullingpiglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_pigletsmerger piglets_events_pigletsmerger_created_piglets_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletsmerger
    ADD CONSTRAINT piglets_events_pigletsmerger_created_piglets_id_key UNIQUE (created_piglets_id);


--
-- Name: piglets_events_pigletsmerger piglets_events_pigletsmerger_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletsmerger
    ADD CONSTRAINT piglets_events_pigletsmerger_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_pigletssplit piglets_events_pigletssplit_parent_piglets_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletssplit
    ADD CONSTRAINT piglets_events_pigletssplit_parent_piglets_id_key UNIQUE (parent_piglets_id);


--
-- Name: piglets_events_pigletssplit piglets_events_pigletssplit_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletssplit
    ADD CONSTRAINT piglets_events_pigletssplit_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_weighingpiglets piglets_events_weighingpiglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weighingpiglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_piglets piglets_piglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets
    ADD CONSTRAINT piglets_piglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_pigletsstatus piglets_pigletsstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_pigletsstatus
    ADD CONSTRAINT piglets_pigletsstatus_pkey PRIMARY KEY (id);


--
-- Name: sows_boar sows_boar_birth_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_boar
    ADD CONSTRAINT sows_boar_birth_id_key UNIQUE (birth_id);


--
-- Name: sows_boar sows_boar_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_boar
    ADD CONSTRAINT sows_boar_pkey PRIMARY KEY (id);


--
-- Name: sows_events_abortionsow sows_events_abortionsow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_abortionsow
    ADD CONSTRAINT sows_events_abortionsow_pkey PRIMARY KEY (id);


--
-- Name: sows_events_cullingsow sows_events_cullingsow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_cullingsow
    ADD CONSTRAINT sows_events_cullingsow_pkey PRIMARY KEY (id);


--
-- Name: sows_events_semination sows_events_semination_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_semination_pkey PRIMARY KEY (id);


--
-- Name: sows_events_sowfarrow sows_events_sowfarrow_piglets_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarrow_piglets_group_id_key UNIQUE (piglets_group_id);


--
-- Name: sows_events_sowfarrow sows_events_sowfarrow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarrow_pkey PRIMARY KEY (id);


--
-- Name: sows_events_ultrasound sows_events_ultrasound_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound
    ADD CONSTRAINT sows_events_ultrasound_pkey PRIMARY KEY (id);


--
-- Name: sows_events_ultrasoundtype sows_events_ultrasoundtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasoundtype
    ADD CONSTRAINT sows_events_ultrasoundtype_pkey PRIMARY KEY (id);


--
-- Name: sows_events_weaningsow sows_events_weaningsow_piglets_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weaningsow_piglets_id_key UNIQUE (piglets_id);


--
-- Name: sows_events_weaningsow sows_events_weaningsow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weaningsow_pkey PRIMARY KEY (id);


--
-- Name: sows_gilt sows_gilt_birth_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_birth_id_key UNIQUE (birth_id);


--
-- Name: sows_gilt sows_gilt_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_pkey PRIMARY KEY (id);


--
-- Name: sows_sow sows_sow_birth_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_birth_id_key UNIQUE (birth_id);


--
-- Name: sows_sow sows_sow_farm_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_farm_id_key UNIQUE (farm_id);


--
-- Name: sows_sow sows_sow_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_pkey PRIMARY KEY (id);


--
-- Name: sows_sowstatus sows_sowstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sowstatus
    ADD CONSTRAINT sows_sowstatus_pkey PRIMARY KEY (id);


--
-- Name: staff_workshopemployee staff_workshopemployee_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY staff_workshopemployee
    ADD CONSTRAINT staff_workshopemployee_pkey PRIMARY KEY (id);


--
-- Name: staff_workshopemployee staff_workshopemployee_user_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY staff_workshopemployee
    ADD CONSTRAINT staff_workshopemployee_user_id_key UNIQUE (user_id);


--
-- Name: tours_metatour tours_metatour_piglets_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatour
    ADD CONSTRAINT tours_metatour_piglets_id_key UNIQUE (piglets_id);


--
-- Name: tours_metatour tours_metatour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatour
    ADD CONSTRAINT tours_metatour_pkey PRIMARY KEY (id);


--
-- Name: tours_metatourrecord tours_metatourrecord_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatourrecord
    ADD CONSTRAINT tours_metatourrecord_pkey PRIMARY KEY (id);


--
-- Name: tours_tour tours_tour_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_tour
    ADD CONSTRAINT tours_tour_pkey PRIMARY KEY (id);


--
-- Name: transactions_pigletstransaction transactions_pigletstransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_pigletstransaction_pkey PRIMARY KEY (id);


--
-- Name: transactions_sowtransaction transactions_sowtransaction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction
    ADD CONSTRAINT transactions_sowtransaction_pkey PRIMARY KEY (id);


--
-- Name: auth_group_name_a6ea08ec_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_name_a6ea08ec_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- Name: auth_group_permissions_group_id_b120cbf9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_group_id_b120cbf9 ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id_84c5c92e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_group_permissions_permission_id_84c5c92e ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_permission_content_type_id_2f476e4b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_permission_content_type_id_2f476e4b ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id_97559544; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_group_id_97559544 ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id_6a12ed8b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_groups_user_id_6a12ed8b ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id_1fbb5f2c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_permission_id_1fbb5f2c ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id_a95ead1b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_user_permissions_user_id_a95ead1b ON auth_user_user_permissions USING btree (user_id);


--
-- Name: auth_user_username_6821ab7c_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX auth_user_username_6821ab7c_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- Name: authtoken_token_key_10f0b77e_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX authtoken_token_key_10f0b77e_like ON authtoken_token USING btree (key varchar_pattern_ops);


--
-- Name: django_admin_log_content_type_id_c4bce8eb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_content_type_id_c4bce8eb ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id_c564eba6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_admin_log_user_id_c564eba6 ON django_admin_log USING btree (user_id);


--
-- Name: django_session_expire_date_a5c62663; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_expire_date_a5c62663 ON django_session USING btree (expire_date);


--
-- Name: django_session_session_key_c0390e0f_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX django_session_session_key_c0390e0f_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- Name: locations_pigletsgroupcell_section_id_0315849e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_pigletsgroupcell_section_id_0315849e ON locations_pigletsgroupcell USING btree (section_id);


--
-- Name: locations_pigletsgroupcell_workshop_id_e9d418d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_pigletsgroupcell_workshop_id_e9d418d8 ON locations_pigletsgroupcell USING btree (workshop_id);


--
-- Name: locations_section_workshop_id_d60c8a54; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_section_workshop_id_d60c8a54 ON locations_section USING btree (workshop_id);


--
-- Name: locations_sowandpigletscell_section_id_bc1867f6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowandpigletscell_section_id_bc1867f6 ON locations_sowandpigletscell USING btree (section_id);


--
-- Name: locations_sowandpigletscell_workshop_id_f8e825fa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowandpigletscell_workshop_id_f8e825fa ON locations_sowandpigletscell USING btree (workshop_id);


--
-- Name: locations_sowgroupcell_section_id_87cc2210; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowgroupcell_section_id_87cc2210 ON locations_sowgroupcell USING btree (section_id);


--
-- Name: locations_sowgroupcell_sows_sow_id_f7a10471; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowgroupcell_sows_sow_id_f7a10471 ON locations_sowgroupcell_sows USING btree (sow_id);


--
-- Name: locations_sowgroupcell_sows_sowgroupcell_id_55244781; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowgroupcell_sows_sowgroupcell_id_55244781 ON locations_sowgroupcell_sows USING btree (sowgroupcell_id);


--
-- Name: locations_sowgroupcell_workshop_id_68e38656; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowgroupcell_workshop_id_68e38656 ON locations_sowgroupcell USING btree (workshop_id);


--
-- Name: locations_sowsinglecell_section_id_8aa2503a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowsinglecell_section_id_8aa2503a ON locations_sowsinglecell USING btree (section_id);


--
-- Name: locations_sowsinglecell_workshop_id_94626905; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX locations_sowsinglecell_workshop_id_94626905 ON locations_sowsinglecell USING btree (workshop_id);


--
-- Name: piglets_events_cullingpiglets_initiator_id_0b6011c5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingpiglets_initiator_id_0b6011c5 ON piglets_events_cullingpiglets USING btree (initiator_id);


--
-- Name: piglets_events_cullingpiglets_piglets_group_id_90a9d8b8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingpiglets_piglets_group_id_90a9d8b8 ON piglets_events_cullingpiglets USING btree (piglets_group_id);


--
-- Name: piglets_events_pigletsmerger_initiator_id_7af11e75; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_pigletsmerger_initiator_id_7af11e75 ON piglets_events_pigletsmerger USING btree (initiator_id);


--
-- Name: piglets_events_pigletssplit_initiator_id_f1f2b796; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_pigletssplit_initiator_id_f1f2b796 ON piglets_events_pigletssplit USING btree (initiator_id);


--
-- Name: piglets_events_weighingpiglets_initiator_id_bf3278d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_weighingpiglets_initiator_id_bf3278d7 ON piglets_events_weighingpiglets USING btree (initiator_id);


--
-- Name: piglets_events_weighingpiglets_piglets_group_id_e55cd7f7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_weighingpiglets_piglets_group_id_e55cd7f7 ON piglets_events_weighingpiglets USING btree (piglets_group_id);


--
-- Name: piglets_piglets_location_id_41c43483; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_piglets_location_id_41c43483 ON piglets_piglets USING btree (location_id);


--
-- Name: piglets_piglets_merger_as_parent_id_6e0e878e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_piglets_merger_as_parent_id_6e0e878e ON piglets_piglets USING btree (merger_as_parent_id);


--
-- Name: piglets_piglets_split_as_child_id_67816971; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_piglets_split_as_child_id_67816971 ON piglets_piglets USING btree (split_as_child_id);


--
-- Name: piglets_piglets_status_id_f9ba9ddb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_piglets_status_id_f9ba9ddb ON piglets_piglets USING btree (status_id);


--
-- Name: sows_boar_birth_id_9bb34e60_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_boar_birth_id_9bb34e60_like ON sows_boar USING btree (birth_id varchar_pattern_ops);


--
-- Name: sows_boar_location_id_66e07edc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_boar_location_id_66e07edc ON sows_boar USING btree (location_id);


--
-- Name: sows_events_abortionsow_initiator_id_8f16cdfb; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_abortionsow_initiator_id_8f16cdfb ON sows_events_abortionsow USING btree (initiator_id);


--
-- Name: sows_events_abortionsow_sow_id_17cd54a0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_abortionsow_sow_id_17cd54a0 ON sows_events_abortionsow USING btree (sow_id);


--
-- Name: sows_events_abortionsow_tour_id_947f8443; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_abortionsow_tour_id_947f8443 ON sows_events_abortionsow USING btree (tour_id);


--
-- Name: sows_events_cullingsow_initiator_id_8dbf7b28; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_cullingsow_initiator_id_8dbf7b28 ON sows_events_cullingsow USING btree (initiator_id);


--
-- Name: sows_events_cullingsow_sow_id_e8f1fb9b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_cullingsow_sow_id_e8f1fb9b ON sows_events_cullingsow USING btree (sow_id);


--
-- Name: sows_events_cullingsow_tour_id_d68d3087; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_cullingsow_tour_id_d68d3087 ON sows_events_cullingsow USING btree (tour_id);


--
-- Name: sows_events_semination_boar_id_6a0563e9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_semination_boar_id_6a0563e9 ON sows_events_semination USING btree (boar_id);


--
-- Name: sows_events_semination_initiator_id_c82c01b6; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_semination_initiator_id_c82c01b6 ON sows_events_semination USING btree (initiator_id);


--
-- Name: sows_events_semination_semination_employee_id_ba91bce0; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_semination_semination_employee_id_ba91bce0 ON sows_events_semination USING btree (semination_employee_id);


--
-- Name: sows_events_semination_sow_id_08d9607f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_semination_sow_id_08d9607f ON sows_events_semination USING btree (sow_id);


--
-- Name: sows_events_semination_tour_id_7b291b50; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_semination_tour_id_7b291b50 ON sows_events_semination USING btree (tour_id);


--
-- Name: sows_events_sowfarrow_initiator_id_4105b54e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_sowfarrow_initiator_id_4105b54e ON sows_events_sowfarrow USING btree (initiator_id);


--
-- Name: sows_events_sowfarrow_sow_id_ea9c38dc; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_sowfarrow_sow_id_ea9c38dc ON sows_events_sowfarrow USING btree (sow_id);


--
-- Name: sows_events_sowfarrow_tour_id_0eee5089; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_sowfarrow_tour_id_0eee5089 ON sows_events_sowfarrow USING btree (tour_id);


--
-- Name: sows_events_ultrasound_initiator_id_0279649b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_ultrasound_initiator_id_0279649b ON sows_events_ultrasound USING btree (initiator_id);


--
-- Name: sows_events_ultrasound_sow_id_d4f99510; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_ultrasound_sow_id_d4f99510 ON sows_events_ultrasound USING btree (sow_id);


--
-- Name: sows_events_ultrasound_tour_id_81c2a5f4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_ultrasound_tour_id_81c2a5f4 ON sows_events_ultrasound USING btree (tour_id);


--
-- Name: sows_events_ultrasound_u_type_id_65718203; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_ultrasound_u_type_id_65718203 ON sows_events_ultrasound USING btree (u_type_id);


--
-- Name: sows_events_weaningsow_initiator_id_d98a966b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_weaningsow_initiator_id_d98a966b ON sows_events_weaningsow USING btree (initiator_id);


--
-- Name: sows_events_weaningsow_sow_id_0808d94a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_weaningsow_sow_id_0808d94a ON sows_events_weaningsow USING btree (sow_id);


--
-- Name: sows_events_weaningsow_tour_id_4abf0271; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_weaningsow_tour_id_4abf0271 ON sows_events_weaningsow USING btree (tour_id);


--
-- Name: sows_gilt_birth_id_a4289b2d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_birth_id_a4289b2d_like ON sows_gilt USING btree (birth_id varchar_pattern_ops);


--
-- Name: sows_gilt_farrow_id_703f6faa; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_farrow_id_703f6faa ON sows_gilt USING btree (farrow_id);


--
-- Name: sows_gilt_location_id_6e9d5445; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_location_id_6e9d5445 ON sows_gilt USING btree (location_id);


--
-- Name: sows_gilt_mother_sow_id_c2fedd8a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_mother_sow_id_c2fedd8a ON sows_gilt USING btree (mother_sow_id);


--
-- Name: sows_gilt_tour_id_aaac4830; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_tour_id_aaac4830 ON sows_gilt USING btree (tour_id);


--
-- Name: sows_sow_birth_id_5e9ed45a_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_sow_birth_id_5e9ed45a_like ON sows_sow USING btree (birth_id varchar_pattern_ops);


--
-- Name: sows_sow_location_id_873dece9; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_sow_location_id_873dece9 ON sows_sow USING btree (location_id);


--
-- Name: sows_sow_status_id_8e1b436b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_sow_status_id_8e1b436b ON sows_sow USING btree (status_id);


--
-- Name: sows_sow_tour_id_dd35d078; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_sow_tour_id_dd35d078 ON sows_sow USING btree (tour_id);


--
-- Name: staff_workshopemployee_workshop_id_2e6d9791; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX staff_workshopemployee_workshop_id_2e6d9791 ON staff_workshopemployee USING btree (workshop_id);


--
-- Name: tours_metatourrecord_metatour_id_ba0ab56b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tours_metatourrecord_metatour_id_ba0ab56b ON tours_metatourrecord USING btree (metatour_id);


--
-- Name: tours_metatourrecord_tour_id_11a5df6e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX tours_metatourrecord_tour_id_11a5df6e ON tours_metatourrecord USING btree (tour_id);


--
-- Name: transactions_pigletstransaction_from_location_id_2e739f33; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_pigletstransaction_from_location_id_2e739f33 ON transactions_pigletstransaction USING btree (from_location_id);


--
-- Name: transactions_pigletstransaction_initiator_id_d1e1316b; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_pigletstransaction_initiator_id_d1e1316b ON transactions_pigletstransaction USING btree (initiator_id);


--
-- Name: transactions_pigletstransaction_piglets_group_id_dd2560ba; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_pigletstransaction_piglets_group_id_dd2560ba ON transactions_pigletstransaction USING btree (piglets_group_id);


--
-- Name: transactions_pigletstransaction_to_location_id_f30c13c1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_pigletstransaction_to_location_id_f30c13c1 ON transactions_pigletstransaction USING btree (to_location_id);


--
-- Name: transactions_sowtransaction_from_location_id_824e5868; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_sowtransaction_from_location_id_824e5868 ON transactions_sowtransaction USING btree (from_location_id);


--
-- Name: transactions_sowtransaction_initiator_id_e793f821; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_sowtransaction_initiator_id_e793f821 ON transactions_sowtransaction USING btree (initiator_id);


--
-- Name: transactions_sowtransaction_sow_id_b0c6d7e4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_sowtransaction_sow_id_b0c6d7e4 ON transactions_sowtransaction USING btree (sow_id);


--
-- Name: transactions_sowtransaction_to_location_id_472c5009; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX transactions_sowtransaction_to_location_id_472c5009 ON transactions_sowtransaction USING btree (to_location_id);


--
-- Name: auth_group_permissions auth_group_permissio_permission_id_84c5c92e_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissio_permission_id_84c5c92e_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions auth_group_permissions_group_id_b120cbf9_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_b120cbf9_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_permission auth_permission_content_type_id_2f476e4b_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_2f476e4b_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_group_id_97559544_fk_auth_group_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_97559544_fk_auth_group_id FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups auth_user_groups_user_id_6a12ed8b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_6a12ed8b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: authtoken_token authtoken_token_user_id_35299eff_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY authtoken_token
    ADD CONSTRAINT authtoken_token_user_id_35299eff_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_content_type_id_c4bce8eb_fk_django_co; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_c4bce8eb_fk_django_co FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log django_admin_log_user_id_c564eba6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_c564eba6_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_pigletsGroupCell_id_9f0ca444_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_pigletsGroupCell_id_9f0ca444_fk_locations" FOREIGN KEY ("pigletsGroupCell_id") REFERENCES locations_pigletsgroupcell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_section_id_d43f02ad_fk_locations_section_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT locations_location_section_id_d43f02ad_fk_locations_section_id FOREIGN KEY (section_id) REFERENCES locations_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_sowAndPigletsCell_id_5fff4421_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowAndPigletsCell_id_5fff4421_fk_locations" FOREIGN KEY ("sowAndPigletsCell_id") REFERENCES locations_sowandpigletscell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_sowGroupCell_id_d78d2421_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowGroupCell_id_d78d2421_fk_locations" FOREIGN KEY ("sowGroupCell_id") REFERENCES locations_sowgroupcell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_sowSingleCell_id_36fd69a4_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT "locations_location_sowSingleCell_id_36fd69a4_fk_locations" FOREIGN KEY ("sowSingleCell_id") REFERENCES locations_sowsinglecell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_location locations_location_workshop_id_b9257cf5_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_location
    ADD CONSTRAINT locations_location_workshop_id_b9257cf5_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_pigletsgroupcell locations_pigletsgro_section_id_0315849e_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_pigletsgroupcell
    ADD CONSTRAINT locations_pigletsgro_section_id_0315849e_fk_locations FOREIGN KEY (section_id) REFERENCES locations_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_pigletsgroupcell locations_pigletsgro_workshop_id_e9d418d8_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_pigletsgroupcell
    ADD CONSTRAINT locations_pigletsgro_workshop_id_e9d418d8_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_section locations_section_workshop_id_d60c8a54_fk_locations_workshop_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_section
    ADD CONSTRAINT locations_section_workshop_id_d60c8a54_fk_locations_workshop_id FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowandpigletscell locations_sowandpigl_section_id_bc1867f6_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowandpigletscell
    ADD CONSTRAINT locations_sowandpigl_section_id_bc1867f6_fk_locations FOREIGN KEY (section_id) REFERENCES locations_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowandpigletscell locations_sowandpigl_workshop_id_f8e825fa_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowandpigletscell
    ADD CONSTRAINT locations_sowandpigl_workshop_id_f8e825fa_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowgroupcell locations_sowgroupce_section_id_87cc2210_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell
    ADD CONSTRAINT locations_sowgroupce_section_id_87cc2210_fk_locations FOREIGN KEY (section_id) REFERENCES locations_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowgroupcell_sows locations_sowgroupce_sowgroupcell_id_55244781_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell_sows
    ADD CONSTRAINT locations_sowgroupce_sowgroupcell_id_55244781_fk_locations FOREIGN KEY (sowgroupcell_id) REFERENCES locations_sowgroupcell(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowgroupcell locations_sowgroupce_workshop_id_68e38656_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell
    ADD CONSTRAINT locations_sowgroupce_workshop_id_68e38656_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowgroupcell_sows locations_sowgroupcell_sows_sow_id_f7a10471_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowgroupcell_sows
    ADD CONSTRAINT locations_sowgroupcell_sows_sow_id_f7a10471_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowsinglecell locations_sowsinglec_section_id_8aa2503a_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowsinglecell
    ADD CONSTRAINT locations_sowsinglec_section_id_8aa2503a_fk_locations FOREIGN KEY (section_id) REFERENCES locations_section(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: locations_sowsinglecell locations_sowsinglec_workshop_id_94626905_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY locations_sowsinglecell
    ADD CONSTRAINT locations_sowsinglec_workshop_id_94626905_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_cullingpiglets piglets_events_culli_initiator_id_0b6011c5_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingpiglets
    ADD CONSTRAINT piglets_events_culli_initiator_id_0b6011c5_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_cullingpiglets piglets_events_culli_piglets_group_id_90a9d8b8_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingpiglets
    ADD CONSTRAINT piglets_events_culli_piglets_group_id_90a9d8b8_fk_piglets_p FOREIGN KEY (piglets_group_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_pigletsmerger piglets_events_pigle_created_piglets_id_ce2a075e_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletsmerger
    ADD CONSTRAINT piglets_events_pigle_created_piglets_id_ce2a075e_fk_piglets_p FOREIGN KEY (created_piglets_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_pigletsmerger piglets_events_pigle_initiator_id_7af11e75_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletsmerger
    ADD CONSTRAINT piglets_events_pigle_initiator_id_7af11e75_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_pigletssplit piglets_events_pigle_initiator_id_f1f2b796_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletssplit
    ADD CONSTRAINT piglets_events_pigle_initiator_id_f1f2b796_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_pigletssplit piglets_events_pigle_parent_piglets_id_2d39bdd5_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_pigletssplit
    ADD CONSTRAINT piglets_events_pigle_parent_piglets_id_2d39bdd5_fk_piglets_p FOREIGN KEY (parent_piglets_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_weighingpiglets piglets_events_weigh_initiator_id_bf3278d7_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weigh_initiator_id_bf3278d7_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_weighingpiglets piglets_events_weigh_piglets_group_id_e55cd7f7_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weigh_piglets_group_id_e55cd7f7_fk_piglets_p FOREIGN KEY (piglets_group_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_piglets piglets_piglets_location_id_41c43483_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets
    ADD CONSTRAINT piglets_piglets_location_id_41c43483_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_piglets piglets_piglets_merger_as_parent_id_6e0e878e_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets
    ADD CONSTRAINT piglets_piglets_merger_as_parent_id_6e0e878e_fk_piglets_e FOREIGN KEY (merger_as_parent_id) REFERENCES piglets_events_pigletsmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_piglets piglets_piglets_split_as_child_id_67816971_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets
    ADD CONSTRAINT piglets_piglets_split_as_child_id_67816971_fk_piglets_e FOREIGN KEY (split_as_child_id) REFERENCES piglets_events_pigletssplit(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_piglets piglets_piglets_status_id_f9ba9ddb_fk_piglets_pigletsstatus_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_piglets
    ADD CONSTRAINT piglets_piglets_status_id_f9ba9ddb_fk_piglets_pigletsstatus_id FOREIGN KEY (status_id) REFERENCES piglets_pigletsstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_boar sows_boar_location_id_66e07edc_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_boar
    ADD CONSTRAINT sows_boar_location_id_66e07edc_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_abortionsow sows_events_abortionsow_initiator_id_8f16cdfb_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_abortionsow
    ADD CONSTRAINT sows_events_abortionsow_initiator_id_8f16cdfb_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_abortionsow sows_events_abortionsow_sow_id_17cd54a0_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_abortionsow
    ADD CONSTRAINT sows_events_abortionsow_sow_id_17cd54a0_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_abortionsow sows_events_abortionsow_tour_id_947f8443_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_abortionsow
    ADD CONSTRAINT sows_events_abortionsow_tour_id_947f8443_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_cullingsow sows_events_cullingsow_initiator_id_8dbf7b28_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_cullingsow
    ADD CONSTRAINT sows_events_cullingsow_initiator_id_8dbf7b28_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_cullingsow sows_events_cullingsow_sow_id_e8f1fb9b_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_cullingsow
    ADD CONSTRAINT sows_events_cullingsow_sow_id_e8f1fb9b_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_cullingsow sows_events_cullingsow_tour_id_d68d3087_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_cullingsow
    ADD CONSTRAINT sows_events_cullingsow_tour_id_d68d3087_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_semination sows_events_seminati_semination_employee__ba91bce0_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_seminati_semination_employee__ba91bce0_fk_auth_user FOREIGN KEY (semination_employee_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_semination sows_events_semination_boar_id_6a0563e9_fk_sows_boar_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_semination_boar_id_6a0563e9_fk_sows_boar_id FOREIGN KEY (boar_id) REFERENCES sows_boar(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_semination sows_events_semination_initiator_id_c82c01b6_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_semination_initiator_id_c82c01b6_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_semination sows_events_semination_sow_id_08d9607f_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_semination_sow_id_08d9607f_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_semination sows_events_semination_tour_id_7b291b50_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_semination
    ADD CONSTRAINT sows_events_semination_tour_id_7b291b50_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_sowfarrow sows_events_sowfarro_piglets_group_id_36c6886e_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarro_piglets_group_id_36c6886e_fk_piglets_p FOREIGN KEY (piglets_group_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_sowfarrow sows_events_sowfarrow_initiator_id_4105b54e_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarrow_initiator_id_4105b54e_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_sowfarrow sows_events_sowfarrow_sow_id_ea9c38dc_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarrow_sow_id_ea9c38dc_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_sowfarrow sows_events_sowfarrow_tour_id_0eee5089_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarrow_tour_id_0eee5089_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_ultrasound sows_events_ultrasou_u_type_id_65718203_fk_sows_even; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound
    ADD CONSTRAINT sows_events_ultrasou_u_type_id_65718203_fk_sows_even FOREIGN KEY (u_type_id) REFERENCES sows_events_ultrasoundtype(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_ultrasound sows_events_ultrasound_initiator_id_0279649b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound
    ADD CONSTRAINT sows_events_ultrasound_initiator_id_0279649b_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_ultrasound sows_events_ultrasound_sow_id_d4f99510_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound
    ADD CONSTRAINT sows_events_ultrasound_sow_id_d4f99510_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_ultrasound sows_events_ultrasound_tour_id_81c2a5f4_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_ultrasound
    ADD CONSTRAINT sows_events_ultrasound_tour_id_81c2a5f4_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_weaningsow sows_events_weanings_piglets_id_ebeedc21_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weanings_piglets_id_ebeedc21_fk_piglets_p FOREIGN KEY (piglets_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_weaningsow sows_events_weaningsow_initiator_id_d98a966b_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weaningsow_initiator_id_d98a966b_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_weaningsow sows_events_weaningsow_sow_id_0808d94a_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weaningsow_sow_id_0808d94a_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_events_weaningsow sows_events_weaningsow_tour_id_4abf0271_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weaningsow_tour_id_4abf0271_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_farrow_id_703f6faa_fk_sows_events_sowfarrow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_farrow_id_703f6faa_fk_sows_events_sowfarrow_id FOREIGN KEY (farrow_id) REFERENCES sows_events_sowfarrow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_location_id_6e9d5445_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_location_id_6e9d5445_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_mother_sow_id_c2fedd8a_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_mother_sow_id_c2fedd8a_fk_sows_sow_id FOREIGN KEY (mother_sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_tour_id_aaac4830_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_tour_id_aaac4830_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_sow sows_sow_location_id_873dece9_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_location_id_873dece9_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_sow sows_sow_status_id_8e1b436b_fk_sows_sowstatus_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_status_id_8e1b436b_fk_sows_sowstatus_id FOREIGN KEY (status_id) REFERENCES sows_sowstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_sow sows_sow_tour_id_dd35d078_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_sow
    ADD CONSTRAINT sows_sow_tour_id_dd35d078_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: staff_workshopemployee staff_workshopemploy_workshop_id_2e6d9791_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY staff_workshopemployee
    ADD CONSTRAINT staff_workshopemploy_workshop_id_2e6d9791_fk_locations FOREIGN KEY (workshop_id) REFERENCES locations_workshop(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: staff_workshopemployee staff_workshopemployee_user_id_4f6b5c3f_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY staff_workshopemployee
    ADD CONSTRAINT staff_workshopemployee_user_id_4f6b5c3f_fk_auth_user_id FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tours_metatour tours_metatour_piglets_id_9f8a0fb6_fk_piglets_piglets_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatour
    ADD CONSTRAINT tours_metatour_piglets_id_9f8a0fb6_fk_piglets_piglets_id FOREIGN KEY (piglets_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tours_metatourrecord tours_metatourrecord_metatour_id_ba0ab56b_fk_tours_metatour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatourrecord
    ADD CONSTRAINT tours_metatourrecord_metatour_id_ba0ab56b_fk_tours_metatour_id FOREIGN KEY (metatour_id) REFERENCES tours_metatour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tours_metatourrecord tours_metatourrecord_tour_id_11a5df6e_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tours_metatourrecord
    ADD CONSTRAINT tours_metatourrecord_tour_id_11a5df6e_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_pigletstransaction transactions_piglets_from_location_id_2e739f33_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_piglets_from_location_id_2e739f33_fk_locations FOREIGN KEY (from_location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_pigletstransaction transactions_piglets_initiator_id_d1e1316b_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_piglets_initiator_id_d1e1316b_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_pigletstransaction transactions_piglets_piglets_group_id_dd2560ba_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_piglets_piglets_group_id_dd2560ba_fk_piglets_p FOREIGN KEY (piglets_group_id) REFERENCES piglets_piglets(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_pigletstransaction transactions_piglets_to_location_id_f30c13c1_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_piglets_to_location_id_f30c13c1_fk_locations FOREIGN KEY (to_location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_sowtransaction transactions_sowtran_from_location_id_824e5868_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction
    ADD CONSTRAINT transactions_sowtran_from_location_id_824e5868_fk_locations FOREIGN KEY (from_location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_sowtransaction transactions_sowtran_initiator_id_e793f821_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction
    ADD CONSTRAINT transactions_sowtran_initiator_id_e793f821_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_sowtransaction transactions_sowtran_to_location_id_472c5009_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction
    ADD CONSTRAINT transactions_sowtran_to_location_id_472c5009_fk_locations FOREIGN KEY (to_location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: transactions_sowtransaction transactions_sowtransaction_sow_id_b0c6d7e4_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_sowtransaction
    ADD CONSTRAINT transactions_sowtransaction_sow_id_b0c6d7e4_fk_sows_sow_id FOREIGN KEY (sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

