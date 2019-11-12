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
-- Name: gilts_events_castinglisttosevenfiveevent; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE gilts_events_castinglisttosevenfiveevent (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer
);


ALTER TABLE gilts_events_castinglisttosevenfiveevent OWNER TO postgres;

--
-- Name: gilts_events_castinglisttosevenfiveevent_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE gilts_events_castinglisttosevenfiveevent_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE gilts_events_castinglisttosevenfiveevent_id_seq OWNER TO postgres;

--
-- Name: gilts_events_castinglisttosevenfiveevent_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE gilts_events_castinglisttosevenfiveevent_id_seq OWNED BY gilts_events_castinglisttosevenfiveevent.id;


--
-- Name: gilts_events_giltmerger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE gilts_events_giltmerger (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer,
    nomad_group_id integer
);


ALTER TABLE gilts_events_giltmerger OWNER TO postgres;

--
-- Name: gilts_events_giltmerger_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE gilts_events_giltmerger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE gilts_events_giltmerger_id_seq OWNER TO postgres;

--
-- Name: gilts_events_giltmerger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE gilts_events_giltmerger_id_seq OWNED BY gilts_events_giltmerger.id;


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
-- Name: piglets_events_cullingnewbornpiglets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_cullingnewbornpiglets (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    culling_type character varying(50) NOT NULL,
    quantity integer NOT NULL,
    reason character varying(200),
    is_it_gilt boolean NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_cullingnewbornpiglets OWNER TO postgres;

--
-- Name: piglets_events_cullingnewbornpiglets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_cullingnewbornpiglets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_cullingnewbornpiglets_id_seq OWNER TO postgres;

--
-- Name: piglets_events_cullingnewbornpiglets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_cullingnewbornpiglets_id_seq OWNED BY piglets_events_cullingnewbornpiglets.id;


--
-- Name: piglets_events_cullingnomadpiglets; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_cullingnomadpiglets (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    culling_type character varying(50) NOT NULL,
    quantity integer NOT NULL,
    reason character varying(200),
    is_it_gilt boolean NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_cullingnomadpiglets OWNER TO postgres;

--
-- Name: piglets_events_cullingnomadpiglets_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_cullingnomadpiglets_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_cullingnomadpiglets_id_seq OWNER TO postgres;

--
-- Name: piglets_events_cullingnomadpiglets_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_cullingnomadpiglets_id_seq OWNED BY piglets_events_cullingnomadpiglets.id;


--
-- Name: piglets_events_newbornmergerrecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_newbornmergerrecord (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    percentage double precision NOT NULL,
    merger_id integer NOT NULL,
    tour_id integer
);


ALTER TABLE piglets_events_newbornmergerrecord OWNER TO postgres;

--
-- Name: piglets_events_newbornmergerrecord_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_newbornmergerrecord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_newbornmergerrecord_id_seq OWNER TO postgres;

--
-- Name: piglets_events_newbornmergerrecord_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_newbornmergerrecord_id_seq OWNED BY piglets_events_newbornmergerrecord.id;


--
-- Name: piglets_events_newbornpigletsgrouprecount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_newbornpigletsgrouprecount (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    quantity_before integer NOT NULL,
    quantity_after integer NOT NULL,
    balance integer NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_newbornpigletsgrouprecount OWNER TO postgres;

--
-- Name: piglets_events_newbornpigletsgrouprecount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_newbornpigletsgrouprecount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_newbornpigletsgrouprecount_id_seq OWNER TO postgres;

--
-- Name: piglets_events_newbornpigletsgrouprecount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_newbornpigletsgrouprecount_id_seq OWNED BY piglets_events_newbornpigletsgrouprecount.id;


--
-- Name: piglets_events_newbornpigletsmerger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_newbornpigletsmerger (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    part_number integer,
    initiator_id integer,
    nomad_group_id integer
);


ALTER TABLE piglets_events_newbornpigletsmerger OWNER TO postgres;

--
-- Name: piglets_events_newbornpigletsmerger_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_newbornpigletsmerger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_newbornpigletsmerger_id_seq OWNER TO postgres;

--
-- Name: piglets_events_newbornpigletsmerger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_newbornpigletsmerger_id_seq OWNED BY piglets_events_newbornpigletsmerger.id;


--
-- Name: piglets_events_nomadmergerrecord; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_nomadmergerrecord (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    quantity integer NOT NULL,
    percentage double precision NOT NULL,
    merger_id integer NOT NULL,
    nomad_group_id integer
);


ALTER TABLE piglets_events_nomadmergerrecord OWNER TO postgres;

--
-- Name: piglets_events_nomadmergerrecord_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_nomadmergerrecord_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_nomadmergerrecord_id_seq OWNER TO postgres;

--
-- Name: piglets_events_nomadmergerrecord_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_nomadmergerrecord_id_seq OWNED BY piglets_events_nomadmergerrecord.id;


--
-- Name: piglets_events_nomadpigletsgroupmerger; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_nomadpigletsgroupmerger (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer,
    new_location_id integer,
    nomad_group_id integer
);


ALTER TABLE piglets_events_nomadpigletsgroupmerger OWNER TO postgres;

--
-- Name: piglets_events_nomadpigletsgroupmerger_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_nomadpigletsgroupmerger_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_nomadpigletsgroupmerger_id_seq OWNER TO postgres;

--
-- Name: piglets_events_nomadpigletsgroupmerger_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_nomadpigletsgroupmerger_id_seq OWNED BY piglets_events_nomadpigletsgroupmerger.id;


--
-- Name: piglets_events_nomadpigletsgrouprecount; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_nomadpigletsgrouprecount (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    quantity_before integer NOT NULL,
    quantity_after integer NOT NULL,
    balance integer NOT NULL,
    initiator_id integer,
    piglets_group_id integer NOT NULL
);


ALTER TABLE piglets_events_nomadpigletsgrouprecount OWNER TO postgres;

--
-- Name: piglets_events_nomadpigletsgrouprecount_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_nomadpigletsgrouprecount_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_nomadpigletsgrouprecount_id_seq OWNER TO postgres;

--
-- Name: piglets_events_nomadpigletsgrouprecount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_nomadpigletsgrouprecount_id_seq OWNED BY piglets_events_nomadpigletsgrouprecount.id;


--
-- Name: piglets_events_splitnomadpigletsgroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_events_splitnomadpigletsgroup (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    date timestamp with time zone,
    initiator_id integer,
    parent_group_id integer
);


ALTER TABLE piglets_events_splitnomadpigletsgroup OWNER TO postgres;

--
-- Name: piglets_events_splitnomadpigletsgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_events_splitnomadpigletsgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_events_splitnomadpigletsgroup_id_seq OWNER TO postgres;

--
-- Name: piglets_events_splitnomadpigletsgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_events_splitnomadpigletsgroup_id_seq OWNED BY piglets_events_splitnomadpigletsgroup.id;


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
-- Name: piglets_newbornpigletsgroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_newbornpigletsgroup (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    start_quantity integer NOT NULL,
    quantity integer NOT NULL,
    active boolean NOT NULL,
    transfer_label boolean NOT NULL,
    gilts_quantity integer NOT NULL,
    size_label character varying(1),
    location_id integer,
    merger_id integer,
    status_id integer,
    tour_id integer
);


ALTER TABLE piglets_newbornpigletsgroup OWNER TO postgres;

--
-- Name: piglets_newbornpigletsgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_newbornpigletsgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_newbornpigletsgroup_id_seq OWNER TO postgres;

--
-- Name: piglets_newbornpigletsgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_newbornpigletsgroup_id_seq OWNED BY piglets_newbornpigletsgroup.id;


--
-- Name: piglets_nomadpigletsgroup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE piglets_nomadpigletsgroup (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    start_quantity integer NOT NULL,
    quantity integer NOT NULL,
    active boolean NOT NULL,
    transfer_label boolean NOT NULL,
    gilts_quantity integer NOT NULL,
    groups_merger_id integer,
    location_id integer,
    split_record_id integer,
    status_id integer
);


ALTER TABLE piglets_nomadpigletsgroup OWNER TO postgres;

--
-- Name: piglets_nomadpigletsgroup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE piglets_nomadpigletsgroup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE piglets_nomadpigletsgroup_id_seq OWNER TO postgres;

--
-- Name: piglets_nomadpigletsgroup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE piglets_nomadpigletsgroup_id_seq OWNED BY piglets_nomadpigletsgroup.id;


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
    new_born_piglets_group_id integer,
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
    initiator_id integer,
    sow_id integer NOT NULL,
    tour_id integer,
    transaction_id integer
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
    casting_list_to_seven_five_id integer,
    location_id integer,
    merger_id integer,
    mother_sow_id integer,
    new_born_group_id integer,
    status_id integer,
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
-- Name: sows_giltstatus; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE sows_giltstatus (
    id integer NOT NULL,
    created_at timestamp with time zone NOT NULL,
    modified_at timestamp with time zone NOT NULL,
    title character varying(100) NOT NULL
);


ALTER TABLE sows_giltstatus OWNER TO postgres;

--
-- Name: sows_giltstatus_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE sows_giltstatus_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE sows_giltstatus_id_seq OWNER TO postgres;

--
-- Name: sows_giltstatus_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE sows_giltstatus_id_seq OWNED BY sows_giltstatus.id;


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
    is_officer boolean NOT NULL,
    is_seminator boolean NOT NULL,
    user_id integer NOT NULL,
    workshop_id integer,
    farm_name character varying(20) NOT NULL
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
-- Name: gilts_events_castinglisttosevenfiveevent id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_castinglisttosevenfiveevent ALTER COLUMN id SET DEFAULT nextval('gilts_events_castinglisttosevenfiveevent_id_seq'::regclass);


--
-- Name: gilts_events_giltmerger id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_giltmerger ALTER COLUMN id SET DEFAULT nextval('gilts_events_giltmerger_id_seq'::regclass);


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
-- Name: piglets_events_cullingnewbornpiglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnewbornpiglets ALTER COLUMN id SET DEFAULT nextval('piglets_events_cullingnewbornpiglets_id_seq'::regclass);


--
-- Name: piglets_events_cullingnomadpiglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnomadpiglets ALTER COLUMN id SET DEFAULT nextval('piglets_events_cullingnomadpiglets_id_seq'::regclass);


--
-- Name: piglets_events_newbornmergerrecord id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornmergerrecord ALTER COLUMN id SET DEFAULT nextval('piglets_events_newbornmergerrecord_id_seq'::regclass);


--
-- Name: piglets_events_newbornpigletsgrouprecount id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsgrouprecount ALTER COLUMN id SET DEFAULT nextval('piglets_events_newbornpigletsgrouprecount_id_seq'::regclass);


--
-- Name: piglets_events_newbornpigletsmerger id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsmerger ALTER COLUMN id SET DEFAULT nextval('piglets_events_newbornpigletsmerger_id_seq'::regclass);


--
-- Name: piglets_events_nomadmergerrecord id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadmergerrecord ALTER COLUMN id SET DEFAULT nextval('piglets_events_nomadmergerrecord_id_seq'::regclass);


--
-- Name: piglets_events_nomadpigletsgroupmerger id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger ALTER COLUMN id SET DEFAULT nextval('piglets_events_nomadpigletsgroupmerger_id_seq'::regclass);


--
-- Name: piglets_events_nomadpigletsgrouprecount id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgrouprecount ALTER COLUMN id SET DEFAULT nextval('piglets_events_nomadpigletsgrouprecount_id_seq'::regclass);


--
-- Name: piglets_events_splitnomadpigletsgroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_splitnomadpigletsgroup ALTER COLUMN id SET DEFAULT nextval('piglets_events_splitnomadpigletsgroup_id_seq'::regclass);


--
-- Name: piglets_events_weighingpiglets id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets ALTER COLUMN id SET DEFAULT nextval('piglets_events_weighingpiglets_id_seq'::regclass);


--
-- Name: piglets_newbornpigletsgroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup ALTER COLUMN id SET DEFAULT nextval('piglets_newbornpigletsgroup_id_seq'::regclass);


--
-- Name: piglets_nomadpigletsgroup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup ALTER COLUMN id SET DEFAULT nextval('piglets_nomadpigletsgroup_id_seq'::regclass);


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
-- Name: sows_giltstatus id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_giltstatus ALTER COLUMN id SET DEFAULT nextval('sows_giltstatus_id_seq'::regclass);


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
53	Can add gilt status	14	add_giltstatus
54	Can change gilt status	14	change_giltstatus
55	Can delete gilt status	14	delete_giltstatus
56	Can view gilt status	14	view_giltstatus
57	Can add sow status	15	add_sowstatus
58	Can change sow status	15	change_sowstatus
59	Can delete sow status	15	delete_sowstatus
60	Can view sow status	15	view_sowstatus
61	Can add sow	16	add_sow
62	Can change sow	16	change_sow
63	Can delete sow	16	delete_sow
64	Can view sow	16	view_sow
65	Can add gilt	17	add_gilt
66	Can change gilt	17	change_gilt
67	Can delete gilt	17	delete_gilt
68	Can view gilt	17	view_gilt
69	Can add boar	18	add_boar
70	Can change boar	18	change_boar
71	Can delete boar	18	delete_boar
72	Can view boar	18	view_boar
73	Can add new born piglets group	19	add_newbornpigletsgroup
74	Can change new born piglets group	19	change_newbornpigletsgroup
75	Can delete new born piglets group	19	delete_newbornpigletsgroup
76	Can view new born piglets group	19	view_newbornpigletsgroup
77	Can add nomad piglets group	20	add_nomadpigletsgroup
78	Can change nomad piglets group	20	change_nomadpigletsgroup
79	Can delete nomad piglets group	20	delete_nomadpigletsgroup
80	Can view nomad piglets group	20	view_nomadpigletsgroup
81	Can add piglets status	21	add_pigletsstatus
82	Can change piglets status	21	change_pigletsstatus
83	Can delete piglets status	21	delete_pigletsstatus
84	Can view piglets status	21	view_pigletsstatus
85	Can add ultrasound type	22	add_ultrasoundtype
86	Can change ultrasound type	22	change_ultrasoundtype
87	Can delete ultrasound type	22	delete_ultrasoundtype
88	Can view ultrasound type	22	view_ultrasoundtype
89	Can add weaning sow	23	add_weaningsow
90	Can change weaning sow	23	change_weaningsow
91	Can delete weaning sow	23	delete_weaningsow
92	Can view weaning sow	23	view_weaningsow
93	Can add ultrasound	24	add_ultrasound
94	Can change ultrasound	24	change_ultrasound
95	Can delete ultrasound	24	delete_ultrasound
96	Can view ultrasound	24	view_ultrasound
97	Can add sow farrow	25	add_sowfarrow
98	Can change sow farrow	25	change_sowfarrow
99	Can delete sow farrow	25	delete_sowfarrow
100	Can view sow farrow	25	view_sowfarrow
101	Can add semination	26	add_semination
102	Can change semination	26	change_semination
103	Can delete semination	26	delete_semination
104	Can view semination	26	view_semination
105	Can add culling sow	27	add_cullingsow
106	Can change culling sow	27	change_cullingsow
107	Can delete culling sow	27	delete_cullingsow
108	Can view culling sow	27	view_cullingsow
109	Can add abortion sow	28	add_abortionsow
110	Can change abortion sow	28	change_abortionsow
111	Can delete abortion sow	28	delete_abortionsow
112	Can view abortion sow	28	view_abortionsow
113	Can add weighing piglets	29	add_weighingpiglets
114	Can change weighing piglets	29	change_weighingpiglets
115	Can delete weighing piglets	29	delete_weighingpiglets
116	Can view weighing piglets	29	view_weighingpiglets
117	Can add split nomad piglets group	30	add_splitnomadpigletsgroup
118	Can change split nomad piglets group	30	change_splitnomadpigletsgroup
119	Can delete split nomad piglets group	30	delete_splitnomadpigletsgroup
120	Can view split nomad piglets group	30	view_splitnomadpigletsgroup
121	Can add nomad piglets group recount	31	add_nomadpigletsgrouprecount
122	Can change nomad piglets group recount	31	change_nomadpigletsgrouprecount
123	Can delete nomad piglets group recount	31	delete_nomadpigletsgrouprecount
124	Can view nomad piglets group recount	31	view_nomadpigletsgrouprecount
125	Can add nomad piglets group merger	32	add_nomadpigletsgroupmerger
126	Can change nomad piglets group merger	32	change_nomadpigletsgroupmerger
127	Can delete nomad piglets group merger	32	delete_nomadpigletsgroupmerger
128	Can view nomad piglets group merger	32	view_nomadpigletsgroupmerger
129	Can add nomad merger record	33	add_nomadmergerrecord
130	Can change nomad merger record	33	change_nomadmergerrecord
131	Can delete nomad merger record	33	delete_nomadmergerrecord
132	Can view nomad merger record	33	view_nomadmergerrecord
133	Can add new born piglets merger	34	add_newbornpigletsmerger
134	Can change new born piglets merger	34	change_newbornpigletsmerger
135	Can delete new born piglets merger	34	delete_newbornpigletsmerger
136	Can view new born piglets merger	34	view_newbornpigletsmerger
137	Can add new born piglets group recount	35	add_newbornpigletsgrouprecount
138	Can change new born piglets group recount	35	change_newbornpigletsgrouprecount
139	Can delete new born piglets group recount	35	delete_newbornpigletsgrouprecount
140	Can view new born piglets group recount	35	view_newbornpigletsgrouprecount
141	Can add new born merger record	36	add_newbornmergerrecord
142	Can change new born merger record	36	change_newbornmergerrecord
143	Can delete new born merger record	36	delete_newbornmergerrecord
144	Can view new born merger record	36	view_newbornmergerrecord
145	Can add culling nomad piglets	37	add_cullingnomadpiglets
146	Can change culling nomad piglets	37	change_cullingnomadpiglets
147	Can delete culling nomad piglets	37	delete_cullingnomadpiglets
148	Can view culling nomad piglets	37	view_cullingnomadpiglets
149	Can add culling new born piglets	38	add_cullingnewbornpiglets
150	Can change culling new born piglets	38	change_cullingnewbornpiglets
151	Can delete culling new born piglets	38	delete_cullingnewbornpiglets
152	Can view culling new born piglets	38	view_cullingnewbornpiglets
153	Can add casting list to seven five event	39	add_castinglisttosevenfiveevent
154	Can change casting list to seven five event	39	change_castinglisttosevenfiveevent
155	Can delete casting list to seven five event	39	delete_castinglisttosevenfiveevent
156	Can view casting list to seven five event	39	view_castinglisttosevenfiveevent
157	Can add gilt merger	40	add_giltmerger
158	Can change gilt merger	40	change_giltmerger
159	Can delete gilt merger	40	delete_giltmerger
160	Can view gilt merger	40	view_giltmerger
161	Can add sow transaction	41	add_sowtransaction
162	Can change sow transaction	41	change_sowtransaction
163	Can delete sow transaction	41	delete_sowtransaction
164	Can view sow transaction	41	view_sowtransaction
165	Can add piglets transaction	42	add_pigletstransaction
166	Can change piglets transaction	42	change_pigletstransaction
167	Can delete piglets transaction	42	delete_pigletstransaction
168	Can view piglets transaction	42	view_pigletstransaction
169	Can add tour	43	add_tour
170	Can change tour	43	change_tour
171	Can delete tour	43	delete_tour
172	Can view tour	43	view_tour
173	Can add work shop employee	44	add_workshopemployee
174	Can change work shop employee	44	change_workshopemployee
175	Can delete work shop employee	44	delete_workshopemployee
176	Can view work shop employee	44	view_workshopemployee
177	Can add Token	45	add_token
178	Can change Token	45	change_token
179	Can delete Token	45	delete_token
180	Can view Token	45	view_token
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY auth_user (id, password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined) FROM stdin;
1	pbkdf2_sha256$150000$Dbh2ihachZwO$4kuqmpO7e/86KiqFM6YOvFfr7xo1YFNlaYHHfcd9eUM=	\N	f	test_seminator			t@t.ru	f	t	2019-10-17 13:28:57.788099+00
9	pbkdf2_sha256$150000$KjFFkDtsnJtH$0NWwvFG0+kTFb6VwGbUXmSEQGrvde377tM9IDflKdqI=	\N	f	d.perfiliev	Дмитрий	Перфильев		f	t	2019-10-21 06:18:44+00
7	pbkdf2_sha256$150000$r08plwYAkj4k$fXZUhEeXP4W2gnlWEeA4vWJK/Vz4DxDdlA+JVrFNDYY=	\N	f	borisov_seminator		3 Борисов		f	t	2019-10-21 05:56:31+00
5	pbkdf2_sha256$150000$5sibB2j926ao$7KzI6czOK0+rVGPc6K0fDqP2wODCbNMiT6c8fUoVDpk=	\N	f	semenova		1 Семенова		f	t	2019-10-21 05:55:14+00
6	pbkdf2_sha256$150000$ZB8lPCRvvDL6$GIpHaLcN37jyMsPmKJrHovXWxBmJuusBJN3XxmswfkU=	\N	f	ivanov_semenator		2 Иванов		f	t	2019-10-21 05:55:39+00
4	pbkdf2_sha256$150000$T2JkRiuqJcIS$lcxeEvj89b4W8BuXuB8JI6ucCBX43HRmi1nFxrG2lKQ=	\N	f	v.shmigina	Валентина	4 Шмыгина		f	t	2019-10-21 05:46:56+00
10	pbkdf2_sha256$150000$wvPRMlCjnFYg$PuH+uu2BJnSbWzwL00zwXVBJcelMVxev/UmI7/k30Po=	\N	f	gary		5 Гари		f	t	2019-10-21 07:30:51+00
2	pbkdf2_sha256$150000$Hy5iYce7OLUI$wP4jtqQ1zZU9hQxaGVwdn5FEDEHRUZVcc+pPUAkKWZg=	2019-11-04 08:25:41.781155+00	t	smileman			kzrster@gmail.com	t	t	2019-10-21 05:36:32.165661+00
8	pbkdf2_sha256$150000$Um9MhrHlrnCT$rGqjP5BC9DzL0oT6F1Up1bWwuTS1GePF9k/8pLcS2m4=	\N	f	test_admin				t	t	2019-10-21 06:16:27+00
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
1	2019-10-21 05:40:47.215688+00	3	v.shmigina	1	[{"added": {}}]	4	2
2	2019-10-21 05:41:32.936273+00	3	v.shmigina	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	4	2
3	2019-10-21 05:41:54.291575+00	3	v.shmigina	3		4	2
4	2019-10-21 05:46:56.207658+00	4	v.shmigina	1	[{"added": {}}]	4	2
5	2019-10-21 05:47:15.624996+00	4	v.shmigina	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	4	2
6	2019-10-21 05:48:04.183057+00	2	Employee v.shmigina 	1	[{"added": {}}]	44	2
7	2019-10-21 05:50:01.457644+00	3	Boar object (3)	1	[{"added": {}}]	18	2
8	2019-10-21 05:50:14.958743+00	4	Boar object (4)	1	[{"added": {}}]	18	2
9	2019-10-21 05:50:27.307161+00	5	Boar object (5)	1	[{"added": {}}]	18	2
10	2019-10-21 05:50:35.487662+00	6	Boar object (6)	1	[{"added": {}}]	18	2
11	2019-10-21 05:50:45.165868+00	7	Boar object (7)	1	[{"added": {}}]	18	2
12	2019-10-21 05:50:57.534846+00	8	Boar object (8)	1	[{"added": {}}]	18	2
13	2019-10-21 05:51:07.91922+00	9	Boar object (9)	1	[{"added": {}}]	18	2
14	2019-10-21 05:51:16.330869+00	10	Boar object (10)	1	[{"added": {}}]	18	2
15	2019-10-21 05:51:31.080817+00	11	Boar object (11)	1	[{"added": {}}]	18	2
16	2019-10-21 05:51:38.664374+00	12	Boar object (12)	1	[{"added": {}}]	18	2
17	2019-10-21 05:55:14.61221+00	5	semenova	1	[{"added": {}}]	4	2
18	2019-10-21 05:55:39.707683+00	6	ivanov_semenator	1	[{"added": {}}]	4	2
19	2019-10-21 05:56:31.704315+00	7	borisov_seminator	1	[{"added": {}}]	4	2
20	2019-10-21 05:56:36.587706+00	7	borisov_seminator	2	[]	4	2
21	2019-10-21 05:57:10.45968+00	2	Employee v.shmigina 	2	[{"changed": {"fields": ["is_seminator"]}}]	44	2
22	2019-10-21 05:57:22.596313+00	3	Employee semenova 	1	[{"added": {}}]	44	2
23	2019-10-21 05:57:28.996103+00	4	Employee borisov_seminator 	1	[{"added": {}}]	44	2
24	2019-10-21 05:57:35.758977+00	5	Employee ivanov_semenator 	1	[{"added": {}}]	44	2
25	2019-10-21 05:59:43.901903+00	4	Employee borisov_seminator 	2	[{"changed": {"fields": ["is_officer", "is_seminator"]}}]	44	2
26	2019-10-21 06:03:58.62821+00	1	Employee test_seminator 	3		44	2
27	2019-10-21 06:06:11.545941+00	1	Boar object (1)	3		18	2
28	2019-10-21 06:06:21.669653+00	2	Boar object (2)	3		18	2
29	2019-10-21 06:09:42.995521+00	5	semenova	2	[{"changed": {"fields": ["last_name"]}}]	4	2
30	2019-10-21 06:09:59.99052+00	7	borisov_seminator	2	[{"changed": {"fields": ["last_name"]}}]	4	2
31	2019-10-21 06:10:14.101939+00	6	ivanov_semenator	2	[{"changed": {"fields": ["last_name"]}}]	4	2
32	2019-10-21 06:16:27.243949+00	8	test_admin	1	[{"added": {}}]	4	2
33	2019-10-21 06:16:50.052832+00	8	test_admin	2	[{"changed": {"fields": ["is_staff"]}}]	4	2
34	2019-10-21 06:17:07.380004+00	6	Employee test_admin 	1	[{"added": {}}]	44	2
35	2019-10-21 06:18:44.17773+00	9	d.perfiliev	1	[{"added": {}}]	4	2
36	2019-10-21 06:19:01.596287+00	9	d.perfiliev	2	[{"changed": {"fields": ["first_name", "last_name"]}}]	4	2
37	2019-10-21 06:19:31.454665+00	7	Employee d.perfiliev 	1	[{"added": {}}]	44	2
38	2019-10-21 06:40:30.125+00	79	Sow #2618	3		16	2
39	2019-10-21 07:29:45.875878+00	7	borisov_seminator	2	[{"changed": {"fields": ["last_name"]}}]	4	2
40	2019-10-21 07:29:56.038684+00	6	ivanov_semenator	2	[{"changed": {"fields": ["last_name"]}}]	4	2
41	2019-10-21 07:30:06.951533+00	5	semenova	2	[{"changed": {"fields": ["last_name"]}}]	4	2
42	2019-10-21 07:30:15.764126+00	6	ivanov_semenator	2	[{"changed": {"fields": ["last_name"]}}]	4	2
43	2019-10-21 07:30:30.806807+00	4	v.shmigina	2	[{"changed": {"fields": ["last_name"]}}]	4	2
44	2019-10-21 07:30:51.643618+00	10	gary	1	[{"added": {}}]	4	2
45	2019-10-21 07:31:04.889606+00	10	gary	2	[{"changed": {"fields": ["last_name"]}}]	4	2
46	2019-10-21 07:31:22.125941+00	8	Employee gary 	1	[{"added": {}}]	44	2
47	2019-10-25 04:33:42.436354+00	2	Employee v.shmigina 	2	[{"changed": {"fields": ["farm_name"]}}]	44	2
48	2019-10-25 04:33:54.645715+00	3	Employee semenova 	2	[{"changed": {"fields": ["farm_name"]}}]	44	2
49	2019-10-25 04:34:09.848149+00	4	Employee borisov_seminator 	2	[{"changed": {"fields": ["farm_name"]}}]	44	2
50	2019-10-25 04:34:29.27736+00	5	Employee ivanov_semenator 	2	[{"changed": {"fields": ["farm_name"]}}]	44	2
51	2019-10-25 04:34:42.035085+00	8	Employee gary 	2	[{"changed": {"fields": ["farm_name"]}}]	44	2
52	2019-10-25 10:58:27.771694+00	6	Employee test_admin 	2	[{"changed": {"fields": ["farm_name", "is_seminator"]}}]	44	2
53	2019-10-30 10:09:13.08097+00	4	Супорос 35	2	[{"changed": {"fields": ["title"]}}]	15	2
54	2019-10-30 10:09:20.550881+00	3	Супорос 28	2	[{"changed": {"fields": ["title"]}}]	15	2
55	2019-11-04 08:29:31.915478+00	256	Sow #19465	2	[{"changed": {"fields": ["birth_id", "farm_id"]}}]	16	2
56	2019-11-05 07:17:23.442671+00	8	test_admin	2	[{"changed": {"fields": ["password"]}}]	4	2
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
14	sows	giltstatus
15	sows	sowstatus
16	sows	sow
17	sows	gilt
18	sows	boar
19	piglets	newbornpigletsgroup
20	piglets	nomadpigletsgroup
21	piglets	pigletsstatus
22	sows_events	ultrasoundtype
23	sows_events	weaningsow
24	sows_events	ultrasound
25	sows_events	sowfarrow
26	sows_events	semination
27	sows_events	cullingsow
28	sows_events	abortionsow
29	piglets_events	weighingpiglets
30	piglets_events	splitnomadpigletsgroup
31	piglets_events	nomadpigletsgrouprecount
32	piglets_events	nomadpigletsgroupmerger
33	piglets_events	nomadmergerrecord
34	piglets_events	newbornpigletsmerger
35	piglets_events	newbornpigletsgrouprecount
36	piglets_events	newbornmergerrecord
37	piglets_events	cullingnomadpiglets
38	piglets_events	cullingnewbornpiglets
39	gilts_events	castinglisttosevenfiveevent
40	gilts_events	giltmerger
41	transactions	sowtransaction
42	transactions	pigletstransaction
43	tours	tour
44	staff	workshopemployee
45	authtoken	token
\.


--
-- Data for Name: django_migrations; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_migrations (id, app, name, applied) FROM stdin;
1	contenttypes	0001_initial	2019-10-17 12:51:42.577366+00
2	auth	0001_initial	2019-10-17 12:51:42.643696+00
3	admin	0001_initial	2019-10-17 12:51:42.740355+00
4	admin	0002_logentry_remove_auto_add	2019-10-17 12:51:42.760839+00
5	admin	0003_logentry_add_action_flag_choices	2019-10-17 12:51:42.774073+00
6	contenttypes	0002_remove_content_type_name	2019-10-17 12:51:42.834791+00
7	auth	0002_alter_permission_name_max_length	2019-10-17 12:51:42.844374+00
8	auth	0003_alter_user_email_max_length	2019-10-17 12:51:42.856606+00
9	auth	0004_alter_user_username_opts	2019-10-17 12:51:42.869131+00
10	auth	0005_alter_user_last_login_null	2019-10-17 12:51:42.879647+00
11	auth	0006_require_contenttypes_0002	2019-10-17 12:51:42.882844+00
12	auth	0007_alter_validators_add_error_messages	2019-10-17 12:51:42.893959+00
13	auth	0008_alter_user_username_max_length	2019-10-17 12:51:42.909393+00
14	auth	0009_alter_user_last_name_max_length	2019-10-17 12:51:42.921853+00
15	auth	0010_alter_group_name_max_length	2019-10-17 12:51:42.93394+00
16	auth	0011_update_proxy_permissions	2019-10-17 12:51:42.945783+00
17	authtoken	0001_initial	2019-10-17 12:51:42.970003+00
18	authtoken	0002_auto_20160226_1747	2019-10-17 12:51:43.010917+00
19	piglets	0001_initial	2019-10-17 12:51:43.045112+00
20	gilts_events	0001_initial	2019-10-17 12:51:43.067829+00
21	gilts_events	0002_auto_20191017_2051	2019-10-17 12:51:43.096572+00
22	tours	0001_initial	2019-10-17 12:51:43.113419+00
23	locations	0001_initial	2019-10-17 12:51:43.183786+00
24	sows	0001_initial	2019-10-17 12:51:43.315337+00
25	locations	0002_auto_20191017_2051	2019-10-17 12:51:43.713908+00
26	piglets_events	0001_initial	2019-10-17 12:51:44.204445+00
27	piglets	0002_auto_20191017_2051	2019-10-17 12:51:44.596428+00
28	sessions	0001_initial	2019-10-17 12:51:44.652588+00
29	transactions	0001_initial	2019-10-17 12:51:44.831512+00
30	sows_events	0001_initial	2019-10-17 12:51:45.184446+00
31	staff	0001_initial	2019-10-17 12:51:45.370188+00
32	staff	0002_workshopemployee_farm_name	2019-10-25 04:32:32.62857+00
33	gilts_events	0003_auto_20191025_1555	2019-10-25 07:55:14.293896+00
34	piglets_events	0002_auto_20191025_1555	2019-10-25 07:55:14.593723+00
35	sows_events	0002_auto_20191025_1555	2019-10-25 07:55:14.925489+00
36	transactions	0002_auto_20191025_1555	2019-10-25 07:55:15.013497+00
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
6makjowmv2axz5j18ljrk7otokr97co2	ODlhYWI1NGRmNWVmZWY3ZmY1MWQ5ZTNlZTMwMjRjNmE3ZTU3MTljNjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5ZGRiMTk5MzBjZGQ1MTRmZTVhMmE0ODc2MDcxMjliZGY1ZTM0ZmQ4In0=	2019-11-04 06:39:41.685164+00
fnkk44vvtffdul9ga6a6uf8iv6jfskua	ODlhYWI1NGRmNWVmZWY3ZmY1MWQ5ZTNlZTMwMjRjNmE3ZTU3MTljNjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5ZGRiMTk5MzBjZGQ1MTRmZTVhMmE0ODc2MDcxMjliZGY1ZTM0ZmQ4In0=	2019-11-18 08:25:41.789553+00
hctexgv43o0natnvjnghywg7fwgebqi7	ODlhYWI1NGRmNWVmZWY3ZmY1MWQ5ZTNlZTMwMjRjNmE3ZTU3MTljNjp7Il9hdXRoX3VzZXJfaWQiOiIyIiwiX2F1dGhfdXNlcl9iYWNrZW5kIjoiZGphbmdvLmNvbnRyaWIuYXV0aC5iYWNrZW5kcy5Nb2RlbEJhY2tlbmQiLCJfYXV0aF91c2VyX2hhc2giOiI5ZGRiMTk5MzBjZGQ1MTRmZTVhMmE0ODc2MDcxMjliZGY1ZTM0ZmQ4In0=	2019-11-19 07:17:23.529089+00
\.


--
-- Data for Name: gilts_events_castinglisttosevenfiveevent; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY gilts_events_castinglisttosevenfiveevent (id, created_at, modified_at, date, initiator_id) FROM stdin;
\.


--
-- Data for Name: gilts_events_giltmerger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY gilts_events_giltmerger (id, created_at, modified_at, date, initiator_id, nomad_group_id) FROM stdin;
\.


--
-- Data for Name: locations_location; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_location (id, created_at, modified_at, "pigletsGroupCell_id", section_id, "sowAndPigletsCell_id", "sowGroupCell_id", "sowSingleCell_id", workshop_id) FROM stdin;
1	2019-10-17 13:28:57.266424+00	2019-10-17 13:28:57.266442+00	\N	\N	\N	\N	\N	1
2	2019-10-17 13:28:57.266487+00	2019-10-17 13:28:57.266496+00	\N	\N	\N	\N	\N	2
3	2019-10-17 13:28:57.266519+00	2019-10-17 13:28:57.266527+00	\N	\N	\N	\N	\N	3
4	2019-10-17 13:28:57.266548+00	2019-10-17 13:28:57.266555+00	\N	\N	\N	\N	\N	4
5	2019-10-17 13:28:57.266575+00	2019-10-17 13:28:57.266583+00	\N	\N	\N	\N	\N	5
6	2019-10-17 13:28:57.266603+00	2019-10-17 13:28:57.26661+00	\N	\N	\N	\N	\N	6
7	2019-10-17 13:28:57.266631+00	2019-10-17 13:28:57.266638+00	\N	\N	\N	\N	\N	7
8	2019-10-17 13:28:57.266676+00	2019-10-17 13:28:57.266684+00	\N	\N	\N	\N	\N	8
9	2019-10-17 13:28:57.266705+00	2019-10-17 13:28:57.266712+00	\N	\N	\N	\N	\N	9
10	2019-10-17 13:28:57.266733+00	2019-10-17 13:28:57.26674+00	\N	\N	\N	\N	\N	10
11	2019-10-17 13:28:57.279649+00	2019-10-17 13:28:57.279668+00	\N	1	\N	\N	\N	\N
12	2019-10-17 13:28:57.2797+00	2019-10-17 13:28:57.279709+00	\N	2	\N	\N	\N	\N
13	2019-10-17 13:28:57.279731+00	2019-10-17 13:28:57.279739+00	\N	3	\N	\N	\N	\N
14	2019-10-17 13:28:57.290717+00	2019-10-17 13:28:57.290736+00	\N	4	\N	\N	\N	\N
15	2019-10-17 13:28:57.290771+00	2019-10-17 13:28:57.29078+00	\N	5	\N	\N	\N	\N
16	2019-10-17 13:28:57.303637+00	2019-10-17 13:28:57.303656+00	\N	\N	\N	1	\N	\N
17	2019-10-17 13:28:57.30369+00	2019-10-17 13:28:57.303699+00	\N	\N	\N	2	\N	\N
18	2019-10-17 13:28:57.303722+00	2019-10-17 13:28:57.30373+00	\N	\N	\N	3	\N	\N
19	2019-10-17 13:28:57.303751+00	2019-10-17 13:28:57.303768+00	\N	\N	\N	4	\N	\N
20	2019-10-17 13:28:57.303804+00	2019-10-17 13:28:57.303814+00	\N	\N	\N	5	\N	\N
21	2019-10-17 13:28:57.303842+00	2019-10-17 13:28:57.303851+00	\N	\N	\N	6	\N	\N
22	2019-10-17 13:28:57.318539+00	2019-10-17 13:28:57.318566+00	\N	\N	\N	7	\N	\N
23	2019-10-17 13:28:57.3186+00	2019-10-17 13:28:57.318609+00	\N	\N	\N	8	\N	\N
24	2019-10-17 13:28:57.31864+00	2019-10-17 13:28:57.318648+00	\N	\N	\N	9	\N	\N
25	2019-10-17 13:28:57.318674+00	2019-10-17 13:28:57.318682+00	\N	\N	\N	10	\N	\N
26	2019-10-17 13:28:57.318703+00	2019-10-17 13:28:57.31871+00	\N	\N	\N	11	\N	\N
27	2019-10-17 13:28:57.318731+00	2019-10-17 13:28:57.318738+00	\N	\N	\N	12	\N	\N
28	2019-10-17 13:28:57.331432+00	2019-10-17 13:28:57.331451+00	\N	6	\N	\N	\N	\N
29	2019-10-17 13:28:57.331484+00	2019-10-17 13:28:57.331493+00	\N	7	\N	\N	\N	\N
30	2019-10-17 13:28:57.331515+00	2019-10-17 13:28:57.331524+00	\N	8	\N	\N	\N	\N
31	2019-10-17 13:28:57.331545+00	2019-10-17 13:28:57.331553+00	\N	9	\N	\N	\N	\N
32	2019-10-17 13:28:57.331573+00	2019-10-17 13:28:57.331581+00	\N	10	\N	\N	\N	\N
33	2019-10-17 13:28:57.331601+00	2019-10-17 13:28:57.331608+00	\N	11	\N	\N	\N	\N
34	2019-10-17 13:28:57.351318+00	2019-10-17 13:28:57.351341+00	\N	\N	1	\N	\N	\N
35	2019-10-17 13:28:57.351375+00	2019-10-17 13:28:57.351384+00	\N	\N	2	\N	\N	\N
36	2019-10-17 13:28:57.351406+00	2019-10-17 13:28:57.351414+00	\N	\N	3	\N	\N	\N
37	2019-10-17 13:28:57.351435+00	2019-10-17 13:28:57.351443+00	\N	\N	4	\N	\N	\N
38	2019-10-17 13:28:57.351463+00	2019-10-17 13:28:57.351471+00	\N	\N	5	\N	\N	\N
39	2019-10-17 13:28:57.351491+00	2019-10-17 13:28:57.351499+00	\N	\N	6	\N	\N	\N
40	2019-10-17 13:28:57.351519+00	2019-10-17 13:28:57.351527+00	\N	\N	7	\N	\N	\N
41	2019-10-17 13:28:57.351547+00	2019-10-17 13:28:57.351555+00	\N	\N	8	\N	\N	\N
42	2019-10-17 13:28:57.351575+00	2019-10-17 13:28:57.351582+00	\N	\N	9	\N	\N	\N
43	2019-10-17 13:28:57.351603+00	2019-10-17 13:28:57.35161+00	\N	\N	10	\N	\N	\N
44	2019-10-17 13:28:57.351631+00	2019-10-17 13:28:57.351638+00	\N	\N	11	\N	\N	\N
45	2019-10-17 13:28:57.351658+00	2019-10-17 13:28:57.351666+00	\N	\N	12	\N	\N	\N
46	2019-10-17 13:28:57.351686+00	2019-10-17 13:28:57.351693+00	\N	\N	13	\N	\N	\N
47	2019-10-17 13:28:57.351713+00	2019-10-17 13:28:57.35172+00	\N	\N	14	\N	\N	\N
48	2019-10-17 13:28:57.35174+00	2019-10-17 13:28:57.351747+00	\N	\N	15	\N	\N	\N
49	2019-10-17 13:28:57.351768+00	2019-10-17 13:28:57.351775+00	\N	\N	16	\N	\N	\N
50	2019-10-17 13:28:57.351795+00	2019-10-17 13:28:57.351802+00	\N	\N	17	\N	\N	\N
51	2019-10-17 13:28:57.351822+00	2019-10-17 13:28:57.351829+00	\N	\N	18	\N	\N	\N
52	2019-10-17 13:28:57.35185+00	2019-10-17 13:28:57.351857+00	\N	\N	19	\N	\N	\N
53	2019-10-17 13:28:57.351889+00	2019-10-17 13:28:57.351898+00	\N	\N	20	\N	\N	\N
54	2019-10-17 13:28:57.35192+00	2019-10-17 13:28:57.351928+00	\N	\N	21	\N	\N	\N
55	2019-10-17 13:28:57.351948+00	2019-10-17 13:28:57.351956+00	\N	\N	22	\N	\N	\N
56	2019-10-17 13:28:57.351976+00	2019-10-17 13:28:57.351983+00	\N	\N	23	\N	\N	\N
57	2019-10-17 13:28:57.352003+00	2019-10-17 13:28:57.352011+00	\N	\N	24	\N	\N	\N
58	2019-10-17 13:28:57.352031+00	2019-10-17 13:28:57.352038+00	\N	\N	25	\N	\N	\N
59	2019-10-17 13:28:57.352058+00	2019-10-17 13:28:57.352065+00	\N	\N	26	\N	\N	\N
60	2019-10-17 13:28:57.352085+00	2019-10-17 13:28:57.352093+00	\N	\N	27	\N	\N	\N
61	2019-10-17 13:28:57.352113+00	2019-10-17 13:28:57.35212+00	\N	\N	28	\N	\N	\N
62	2019-10-17 13:28:57.352141+00	2019-10-17 13:28:57.352148+00	\N	\N	29	\N	\N	\N
63	2019-10-17 13:28:57.352168+00	2019-10-17 13:28:57.352176+00	\N	\N	30	\N	\N	\N
64	2019-10-17 13:28:57.352196+00	2019-10-17 13:28:57.352203+00	\N	\N	31	\N	\N	\N
65	2019-10-17 13:28:57.352224+00	2019-10-17 13:28:57.352231+00	\N	\N	32	\N	\N	\N
66	2019-10-17 13:28:57.352251+00	2019-10-17 13:28:57.352259+00	\N	\N	33	\N	\N	\N
67	2019-10-17 13:28:57.352279+00	2019-10-17 13:28:57.352286+00	\N	\N	34	\N	\N	\N
68	2019-10-17 13:28:57.352318+00	2019-10-17 13:28:57.352326+00	\N	\N	35	\N	\N	\N
69	2019-10-17 13:28:57.352347+00	2019-10-17 13:28:57.352354+00	\N	\N	36	\N	\N	\N
70	2019-10-17 13:28:57.352374+00	2019-10-17 13:28:57.352389+00	\N	\N	37	\N	\N	\N
71	2019-10-17 13:28:57.352411+00	2019-10-17 13:28:57.352419+00	\N	\N	38	\N	\N	\N
72	2019-10-17 13:28:57.352439+00	2019-10-17 13:28:57.352446+00	\N	\N	39	\N	\N	\N
73	2019-10-17 13:28:57.352466+00	2019-10-17 13:28:57.352474+00	\N	\N	40	\N	\N	\N
74	2019-10-17 13:28:57.352494+00	2019-10-17 13:28:57.352501+00	\N	\N	41	\N	\N	\N
75	2019-10-17 13:28:57.352522+00	2019-10-17 13:28:57.352529+00	\N	\N	42	\N	\N	\N
76	2019-10-17 13:28:57.352549+00	2019-10-17 13:28:57.352556+00	\N	\N	43	\N	\N	\N
77	2019-10-17 13:28:57.352576+00	2019-10-17 13:28:57.352584+00	\N	\N	44	\N	\N	\N
78	2019-10-17 13:28:57.352604+00	2019-10-17 13:28:57.352611+00	\N	\N	45	\N	\N	\N
79	2019-10-17 13:28:57.369332+00	2019-10-17 13:28:57.369351+00	\N	\N	46	\N	\N	\N
80	2019-10-17 13:28:57.369385+00	2019-10-17 13:28:57.369393+00	\N	\N	47	\N	\N	\N
81	2019-10-17 13:28:57.369417+00	2019-10-17 13:28:57.369424+00	\N	\N	48	\N	\N	\N
82	2019-10-17 13:28:57.369446+00	2019-10-17 13:28:57.369453+00	\N	\N	49	\N	\N	\N
83	2019-10-17 13:28:57.369474+00	2019-10-17 13:28:57.369482+00	\N	\N	50	\N	\N	\N
84	2019-10-17 13:28:57.369511+00	2019-10-17 13:28:57.36952+00	\N	\N	51	\N	\N	\N
85	2019-10-17 13:28:57.369543+00	2019-10-17 13:28:57.36955+00	\N	\N	52	\N	\N	\N
86	2019-10-17 13:28:57.369571+00	2019-10-17 13:28:57.369579+00	\N	\N	53	\N	\N	\N
87	2019-10-17 13:28:57.3696+00	2019-10-17 13:28:57.369607+00	\N	\N	54	\N	\N	\N
88	2019-10-17 13:28:57.369628+00	2019-10-17 13:28:57.369636+00	\N	\N	55	\N	\N	\N
89	2019-10-17 13:28:57.369656+00	2019-10-17 13:28:57.369663+00	\N	\N	56	\N	\N	\N
90	2019-10-17 13:28:57.369684+00	2019-10-17 13:28:57.369691+00	\N	\N	57	\N	\N	\N
91	2019-10-17 13:28:57.369711+00	2019-10-17 13:28:57.369719+00	\N	\N	58	\N	\N	\N
92	2019-10-17 13:28:57.369739+00	2019-10-17 13:28:57.369746+00	\N	\N	59	\N	\N	\N
93	2019-10-17 13:28:57.369767+00	2019-10-17 13:28:57.369774+00	\N	\N	60	\N	\N	\N
94	2019-10-17 13:28:57.369794+00	2019-10-17 13:28:57.369801+00	\N	\N	61	\N	\N	\N
95	2019-10-17 13:28:57.369821+00	2019-10-17 13:28:57.369828+00	\N	\N	62	\N	\N	\N
96	2019-10-17 13:28:57.369849+00	2019-10-17 13:28:57.369856+00	\N	\N	63	\N	\N	\N
97	2019-10-17 13:28:57.369877+00	2019-10-17 13:28:57.369884+00	\N	\N	64	\N	\N	\N
98	2019-10-17 13:28:57.369904+00	2019-10-17 13:28:57.369911+00	\N	\N	65	\N	\N	\N
99	2019-10-17 13:28:57.369932+00	2019-10-17 13:28:57.369939+00	\N	\N	66	\N	\N	\N
100	2019-10-17 13:28:57.369959+00	2019-10-17 13:28:57.369966+00	\N	\N	67	\N	\N	\N
101	2019-10-17 13:28:57.369987+00	2019-10-17 13:28:57.369994+00	\N	\N	68	\N	\N	\N
102	2019-10-17 13:28:57.370014+00	2019-10-17 13:28:57.370022+00	\N	\N	69	\N	\N	\N
103	2019-10-17 13:28:57.370042+00	2019-10-17 13:28:57.370049+00	\N	\N	70	\N	\N	\N
104	2019-10-17 13:28:57.370069+00	2019-10-17 13:28:57.370077+00	\N	\N	71	\N	\N	\N
105	2019-10-17 13:28:57.370097+00	2019-10-17 13:28:57.370104+00	\N	\N	72	\N	\N	\N
106	2019-10-17 13:28:57.370124+00	2019-10-17 13:28:57.370132+00	\N	\N	73	\N	\N	\N
107	2019-10-17 13:28:57.370152+00	2019-10-17 13:28:57.370159+00	\N	\N	74	\N	\N	\N
108	2019-10-17 13:28:57.370179+00	2019-10-17 13:28:57.370186+00	\N	\N	75	\N	\N	\N
109	2019-10-17 13:28:57.370207+00	2019-10-17 13:28:57.370221+00	\N	\N	76	\N	\N	\N
110	2019-10-17 13:28:57.370244+00	2019-10-17 13:28:57.370251+00	\N	\N	77	\N	\N	\N
111	2019-10-17 13:28:57.370271+00	2019-10-17 13:28:57.370279+00	\N	\N	78	\N	\N	\N
112	2019-10-17 13:28:57.370299+00	2019-10-17 13:28:57.370306+00	\N	\N	79	\N	\N	\N
113	2019-10-17 13:28:57.370327+00	2019-10-17 13:28:57.370334+00	\N	\N	80	\N	\N	\N
114	2019-10-17 13:28:57.370355+00	2019-10-17 13:28:57.370362+00	\N	\N	81	\N	\N	\N
115	2019-10-17 13:28:57.370382+00	2019-10-17 13:28:57.37039+00	\N	\N	82	\N	\N	\N
116	2019-10-17 13:28:57.37041+00	2019-10-17 13:28:57.370417+00	\N	\N	83	\N	\N	\N
117	2019-10-17 13:28:57.370438+00	2019-10-17 13:28:57.370445+00	\N	\N	84	\N	\N	\N
118	2019-10-17 13:28:57.370465+00	2019-10-17 13:28:57.370473+00	\N	\N	85	\N	\N	\N
119	2019-10-17 13:28:57.370493+00	2019-10-17 13:28:57.370501+00	\N	\N	86	\N	\N	\N
120	2019-10-17 13:28:57.370521+00	2019-10-17 13:28:57.370529+00	\N	\N	87	\N	\N	\N
121	2019-10-17 13:28:57.370549+00	2019-10-17 13:28:57.370557+00	\N	\N	88	\N	\N	\N
122	2019-10-17 13:28:57.370577+00	2019-10-17 13:28:57.370584+00	\N	\N	89	\N	\N	\N
123	2019-10-17 13:28:57.370605+00	2019-10-17 13:28:57.370612+00	\N	\N	90	\N	\N	\N
124	2019-10-17 13:28:57.386992+00	2019-10-17 13:28:57.387012+00	\N	\N	91	\N	\N	\N
125	2019-10-17 13:28:57.387046+00	2019-10-17 13:28:57.387055+00	\N	\N	92	\N	\N	\N
126	2019-10-17 13:28:57.387078+00	2019-10-17 13:28:57.387086+00	\N	\N	93	\N	\N	\N
127	2019-10-17 13:28:57.387107+00	2019-10-17 13:28:57.387115+00	\N	\N	94	\N	\N	\N
128	2019-10-17 13:28:57.387136+00	2019-10-17 13:28:57.387144+00	\N	\N	95	\N	\N	\N
129	2019-10-17 13:28:57.387165+00	2019-10-17 13:28:57.387172+00	\N	\N	96	\N	\N	\N
130	2019-10-17 13:28:57.387193+00	2019-10-17 13:28:57.3872+00	\N	\N	97	\N	\N	\N
131	2019-10-17 13:28:57.387221+00	2019-10-17 13:28:57.387229+00	\N	\N	98	\N	\N	\N
132	2019-10-17 13:28:57.38725+00	2019-10-17 13:28:57.387286+00	\N	\N	99	\N	\N	\N
133	2019-10-17 13:28:57.387312+00	2019-10-17 13:28:57.38732+00	\N	\N	100	\N	\N	\N
134	2019-10-17 13:28:57.387341+00	2019-10-17 13:28:57.387348+00	\N	\N	101	\N	\N	\N
135	2019-10-17 13:28:57.387369+00	2019-10-17 13:28:57.387376+00	\N	\N	102	\N	\N	\N
136	2019-10-17 13:28:57.387396+00	2019-10-17 13:28:57.387404+00	\N	\N	103	\N	\N	\N
137	2019-10-17 13:28:57.387424+00	2019-10-17 13:28:57.387431+00	\N	\N	104	\N	\N	\N
138	2019-10-17 13:28:57.387452+00	2019-10-17 13:28:57.387459+00	\N	\N	105	\N	\N	\N
139	2019-10-17 13:28:57.387479+00	2019-10-17 13:28:57.387487+00	\N	\N	106	\N	\N	\N
140	2019-10-17 13:28:57.387507+00	2019-10-17 13:28:57.387514+00	\N	\N	107	\N	\N	\N
141	2019-10-17 13:28:57.387535+00	2019-10-17 13:28:57.387542+00	\N	\N	108	\N	\N	\N
142	2019-10-17 13:28:57.387563+00	2019-10-17 13:28:57.38757+00	\N	\N	109	\N	\N	\N
143	2019-10-17 13:28:57.387591+00	2019-10-17 13:28:57.387598+00	\N	\N	110	\N	\N	\N
144	2019-10-17 13:28:57.387618+00	2019-10-17 13:28:57.387626+00	\N	\N	111	\N	\N	\N
145	2019-10-17 13:28:57.387646+00	2019-10-17 13:28:57.387653+00	\N	\N	112	\N	\N	\N
146	2019-10-17 13:28:57.387673+00	2019-10-17 13:28:57.387681+00	\N	\N	113	\N	\N	\N
147	2019-10-17 13:28:57.387701+00	2019-10-17 13:28:57.387709+00	\N	\N	114	\N	\N	\N
148	2019-10-17 13:28:57.387729+00	2019-10-17 13:28:57.387745+00	\N	\N	115	\N	\N	\N
149	2019-10-17 13:28:57.387768+00	2019-10-17 13:28:57.387776+00	\N	\N	116	\N	\N	\N
150	2019-10-17 13:28:57.387797+00	2019-10-17 13:28:57.387804+00	\N	\N	117	\N	\N	\N
151	2019-10-17 13:28:57.387825+00	2019-10-17 13:28:57.387833+00	\N	\N	118	\N	\N	\N
152	2019-10-17 13:28:57.387854+00	2019-10-17 13:28:57.387862+00	\N	\N	119	\N	\N	\N
153	2019-10-17 13:28:57.387882+00	2019-10-17 13:28:57.387889+00	\N	\N	120	\N	\N	\N
154	2019-10-17 13:28:57.38791+00	2019-10-17 13:28:57.387917+00	\N	\N	121	\N	\N	\N
155	2019-10-17 13:28:57.387938+00	2019-10-17 13:28:57.387945+00	\N	\N	122	\N	\N	\N
156	2019-10-17 13:28:57.387966+00	2019-10-17 13:28:57.387973+00	\N	\N	123	\N	\N	\N
157	2019-10-17 13:28:57.387994+00	2019-10-17 13:28:57.388002+00	\N	\N	124	\N	\N	\N
158	2019-10-17 13:28:57.388022+00	2019-10-17 13:28:57.388029+00	\N	\N	125	\N	\N	\N
159	2019-10-17 13:28:57.38805+00	2019-10-17 13:28:57.388057+00	\N	\N	126	\N	\N	\N
160	2019-10-17 13:28:57.388077+00	2019-10-17 13:28:57.388085+00	\N	\N	127	\N	\N	\N
161	2019-10-17 13:28:57.388105+00	2019-10-17 13:28:57.388112+00	\N	\N	128	\N	\N	\N
162	2019-10-17 13:28:57.388133+00	2019-10-17 13:28:57.38814+00	\N	\N	129	\N	\N	\N
163	2019-10-17 13:28:57.388161+00	2019-10-17 13:28:57.388168+00	\N	\N	130	\N	\N	\N
164	2019-10-17 13:28:57.388188+00	2019-10-17 13:28:57.388195+00	\N	\N	131	\N	\N	\N
165	2019-10-17 13:28:57.388216+00	2019-10-17 13:28:57.388223+00	\N	\N	132	\N	\N	\N
166	2019-10-17 13:28:57.388243+00	2019-10-17 13:28:57.38825+00	\N	\N	133	\N	\N	\N
167	2019-10-17 13:28:57.38827+00	2019-10-17 13:28:57.388278+00	\N	\N	134	\N	\N	\N
168	2019-10-17 13:28:57.388308+00	2019-10-17 13:28:57.388317+00	\N	\N	135	\N	\N	\N
169	2019-10-17 13:28:57.404476+00	2019-10-17 13:28:57.404504+00	\N	\N	136	\N	\N	\N
170	2019-10-17 13:28:57.40454+00	2019-10-17 13:28:57.404549+00	\N	\N	137	\N	\N	\N
171	2019-10-17 13:28:57.404572+00	2019-10-17 13:28:57.40458+00	\N	\N	138	\N	\N	\N
172	2019-10-17 13:28:57.404601+00	2019-10-17 13:28:57.404608+00	\N	\N	139	\N	\N	\N
173	2019-10-17 13:28:57.404629+00	2019-10-17 13:28:57.404636+00	\N	\N	140	\N	\N	\N
174	2019-10-17 13:28:57.404657+00	2019-10-17 13:28:57.404664+00	\N	\N	141	\N	\N	\N
175	2019-10-17 13:28:57.404694+00	2019-10-17 13:28:57.404703+00	\N	\N	142	\N	\N	\N
176	2019-10-17 13:28:57.404725+00	2019-10-17 13:28:57.404733+00	\N	\N	143	\N	\N	\N
177	2019-10-17 13:28:57.404753+00	2019-10-17 13:28:57.40476+00	\N	\N	144	\N	\N	\N
178	2019-10-17 13:28:57.404781+00	2019-10-17 13:28:57.404789+00	\N	\N	145	\N	\N	\N
179	2019-10-17 13:28:57.404809+00	2019-10-17 13:28:57.404817+00	\N	\N	146	\N	\N	\N
180	2019-10-17 13:28:57.404837+00	2019-10-17 13:28:57.404844+00	\N	\N	147	\N	\N	\N
181	2019-10-17 13:28:57.404865+00	2019-10-17 13:28:57.404872+00	\N	\N	148	\N	\N	\N
182	2019-10-17 13:28:57.404902+00	2019-10-17 13:28:57.404911+00	\N	\N	149	\N	\N	\N
183	2019-10-17 13:28:57.404932+00	2019-10-17 13:28:57.404939+00	\N	\N	150	\N	\N	\N
184	2019-10-17 13:28:57.40496+00	2019-10-17 13:28:57.404967+00	\N	\N	151	\N	\N	\N
185	2019-10-17 13:28:57.404988+00	2019-10-17 13:28:57.404995+00	\N	\N	152	\N	\N	\N
186	2019-10-17 13:28:57.405016+00	2019-10-17 13:28:57.405023+00	\N	\N	153	\N	\N	\N
187	2019-10-17 13:28:57.405044+00	2019-10-17 13:28:57.405059+00	\N	\N	154	\N	\N	\N
188	2019-10-17 13:28:57.405082+00	2019-10-17 13:28:57.405089+00	\N	\N	155	\N	\N	\N
189	2019-10-17 13:28:57.40512+00	2019-10-17 13:28:57.405128+00	\N	\N	156	\N	\N	\N
190	2019-10-17 13:28:57.405149+00	2019-10-17 13:28:57.405156+00	\N	\N	157	\N	\N	\N
191	2019-10-17 13:28:57.405176+00	2019-10-17 13:28:57.405184+00	\N	\N	158	\N	\N	\N
192	2019-10-17 13:28:57.405204+00	2019-10-17 13:28:57.405211+00	\N	\N	159	\N	\N	\N
193	2019-10-17 13:28:57.405232+00	2019-10-17 13:28:57.405239+00	\N	\N	160	\N	\N	\N
194	2019-10-17 13:28:57.40526+00	2019-10-17 13:28:57.405267+00	\N	\N	161	\N	\N	\N
195	2019-10-17 13:28:57.405295+00	2019-10-17 13:28:57.405304+00	\N	\N	162	\N	\N	\N
196	2019-10-17 13:28:57.405327+00	2019-10-17 13:28:57.405334+00	\N	\N	163	\N	\N	\N
197	2019-10-17 13:28:57.405355+00	2019-10-17 13:28:57.405362+00	\N	\N	164	\N	\N	\N
198	2019-10-17 13:28:57.405383+00	2019-10-17 13:28:57.40539+00	\N	\N	165	\N	\N	\N
199	2019-10-17 13:28:57.405411+00	2019-10-17 13:28:57.405419+00	\N	\N	166	\N	\N	\N
200	2019-10-17 13:28:57.40544+00	2019-10-17 13:28:57.405447+00	\N	\N	167	\N	\N	\N
201	2019-10-17 13:28:57.405467+00	2019-10-17 13:28:57.405475+00	\N	\N	168	\N	\N	\N
202	2019-10-17 13:28:57.405507+00	2019-10-17 13:28:57.405516+00	\N	\N	169	\N	\N	\N
203	2019-10-17 13:28:57.405536+00	2019-10-17 13:28:57.405544+00	\N	\N	170	\N	\N	\N
204	2019-10-17 13:28:57.405564+00	2019-10-17 13:28:57.405572+00	\N	\N	171	\N	\N	\N
205	2019-10-17 13:28:57.405593+00	2019-10-17 13:28:57.4056+00	\N	\N	172	\N	\N	\N
206	2019-10-17 13:28:57.405621+00	2019-10-17 13:28:57.405628+00	\N	\N	173	\N	\N	\N
207	2019-10-17 13:28:57.405649+00	2019-10-17 13:28:57.405656+00	\N	\N	174	\N	\N	\N
208	2019-10-17 13:28:57.405676+00	2019-10-17 13:28:57.405692+00	\N	\N	175	\N	\N	\N
209	2019-10-17 13:28:57.405715+00	2019-10-17 13:28:57.405723+00	\N	\N	176	\N	\N	\N
210	2019-10-17 13:28:57.405743+00	2019-10-17 13:28:57.40575+00	\N	\N	177	\N	\N	\N
211	2019-10-17 13:28:57.40577+00	2019-10-17 13:28:57.405777+00	\N	\N	178	\N	\N	\N
212	2019-10-17 13:28:57.405798+00	2019-10-17 13:28:57.405805+00	\N	\N	179	\N	\N	\N
213	2019-10-17 13:28:57.405825+00	2019-10-17 13:28:57.405832+00	\N	\N	180	\N	\N	\N
214	2019-10-17 13:28:57.424705+00	2019-10-17 13:28:57.424723+00	\N	\N	181	\N	\N	\N
215	2019-10-17 13:28:57.424756+00	2019-10-17 13:28:57.424765+00	\N	\N	182	\N	\N	\N
216	2019-10-17 13:28:57.424788+00	2019-10-17 13:28:57.424796+00	\N	\N	183	\N	\N	\N
217	2019-10-17 13:28:57.424817+00	2019-10-17 13:28:57.424824+00	\N	\N	184	\N	\N	\N
218	2019-10-17 13:28:57.424856+00	2019-10-17 13:28:57.424865+00	\N	\N	185	\N	\N	\N
219	2019-10-17 13:28:57.424888+00	2019-10-17 13:28:57.424895+00	\N	\N	186	\N	\N	\N
220	2019-10-17 13:28:57.424916+00	2019-10-17 13:28:57.424923+00	\N	\N	187	\N	\N	\N
221	2019-10-17 13:28:57.424944+00	2019-10-17 13:28:57.424951+00	\N	\N	188	\N	\N	\N
222	2019-10-17 13:28:57.424972+00	2019-10-17 13:28:57.42498+00	\N	\N	189	\N	\N	\N
223	2019-10-17 13:28:57.425001+00	2019-10-17 13:28:57.425008+00	\N	\N	190	\N	\N	\N
224	2019-10-17 13:28:57.425029+00	2019-10-17 13:28:57.425036+00	\N	\N	191	\N	\N	\N
225	2019-10-17 13:28:57.425057+00	2019-10-17 13:28:57.425064+00	\N	\N	192	\N	\N	\N
226	2019-10-17 13:28:57.425084+00	2019-10-17 13:28:57.425099+00	\N	\N	193	\N	\N	\N
227	2019-10-17 13:28:57.425128+00	2019-10-17 13:28:57.425138+00	\N	\N	194	\N	\N	\N
228	2019-10-17 13:28:57.425161+00	2019-10-17 13:28:57.425168+00	\N	\N	195	\N	\N	\N
229	2019-10-17 13:28:57.425189+00	2019-10-17 13:28:57.425196+00	\N	\N	196	\N	\N	\N
230	2019-10-17 13:28:57.425216+00	2019-10-17 13:28:57.425223+00	\N	\N	197	\N	\N	\N
231	2019-10-17 13:28:57.425244+00	2019-10-17 13:28:57.425251+00	\N	\N	198	\N	\N	\N
232	2019-10-17 13:28:57.425272+00	2019-10-17 13:28:57.425279+00	\N	\N	199	\N	\N	\N
233	2019-10-17 13:28:57.425299+00	2019-10-17 13:28:57.425307+00	\N	\N	200	\N	\N	\N
234	2019-10-17 13:28:57.425337+00	2019-10-17 13:28:57.425346+00	\N	\N	201	\N	\N	\N
235	2019-10-17 13:28:57.425366+00	2019-10-17 13:28:57.425374+00	\N	\N	202	\N	\N	\N
236	2019-10-17 13:28:57.425394+00	2019-10-17 13:28:57.425401+00	\N	\N	203	\N	\N	\N
237	2019-10-17 13:28:57.425421+00	2019-10-17 13:28:57.425429+00	\N	\N	204	\N	\N	\N
238	2019-10-17 13:28:57.425449+00	2019-10-17 13:28:57.425456+00	\N	\N	205	\N	\N	\N
239	2019-10-17 13:28:57.425476+00	2019-10-17 13:28:57.425483+00	\N	\N	206	\N	\N	\N
240	2019-10-17 13:28:57.425504+00	2019-10-17 13:28:57.425511+00	\N	\N	207	\N	\N	\N
241	2019-10-17 13:28:57.425531+00	2019-10-17 13:28:57.425538+00	\N	\N	208	\N	\N	\N
242	2019-10-17 13:28:57.425558+00	2019-10-17 13:28:57.425566+00	\N	\N	209	\N	\N	\N
243	2019-10-17 13:28:57.425586+00	2019-10-17 13:28:57.425593+00	\N	\N	210	\N	\N	\N
244	2019-10-17 13:28:57.425613+00	2019-10-17 13:28:57.425621+00	\N	\N	211	\N	\N	\N
245	2019-10-17 13:28:57.425641+00	2019-10-17 13:28:57.425648+00	\N	\N	212	\N	\N	\N
246	2019-10-17 13:28:57.425668+00	2019-10-17 13:28:57.425675+00	\N	\N	213	\N	\N	\N
247	2019-10-17 13:28:57.425695+00	2019-10-17 13:28:57.425703+00	\N	\N	214	\N	\N	\N
248	2019-10-17 13:28:57.425723+00	2019-10-17 13:28:57.42573+00	\N	\N	215	\N	\N	\N
249	2019-10-17 13:28:57.425758+00	2019-10-17 13:28:57.425767+00	\N	\N	216	\N	\N	\N
250	2019-10-17 13:28:57.42579+00	2019-10-17 13:28:57.425797+00	\N	\N	217	\N	\N	\N
251	2019-10-17 13:28:57.425818+00	2019-10-17 13:28:57.425825+00	\N	\N	218	\N	\N	\N
252	2019-10-17 13:28:57.425846+00	2019-10-17 13:28:57.425853+00	\N	\N	219	\N	\N	\N
253	2019-10-17 13:28:57.425873+00	2019-10-17 13:28:57.42588+00	\N	\N	220	\N	\N	\N
254	2019-10-17 13:28:57.425901+00	2019-10-17 13:28:57.425908+00	\N	\N	221	\N	\N	\N
255	2019-10-17 13:28:57.425928+00	2019-10-17 13:28:57.425935+00	\N	\N	222	\N	\N	\N
256	2019-10-17 13:28:57.425956+00	2019-10-17 13:28:57.425963+00	\N	\N	223	\N	\N	\N
257	2019-10-17 13:28:57.425983+00	2019-10-17 13:28:57.42599+00	\N	\N	224	\N	\N	\N
258	2019-10-17 13:28:57.426011+00	2019-10-17 13:28:57.426018+00	\N	\N	225	\N	\N	\N
259	2019-10-17 13:28:57.444317+00	2019-10-17 13:28:57.444336+00	\N	\N	226	\N	\N	\N
260	2019-10-17 13:28:57.44437+00	2019-10-17 13:28:57.444379+00	\N	\N	227	\N	\N	\N
261	2019-10-17 13:28:57.444402+00	2019-10-17 13:28:57.444409+00	\N	\N	228	\N	\N	\N
262	2019-10-17 13:28:57.444431+00	2019-10-17 13:28:57.444438+00	\N	\N	229	\N	\N	\N
263	2019-10-17 13:28:57.444459+00	2019-10-17 13:28:57.444466+00	\N	\N	230	\N	\N	\N
264	2019-10-17 13:28:57.444487+00	2019-10-17 13:28:57.444494+00	\N	\N	231	\N	\N	\N
265	2019-10-17 13:28:57.444515+00	2019-10-17 13:28:57.44453+00	\N	\N	232	\N	\N	\N
266	2019-10-17 13:28:57.444554+00	2019-10-17 13:28:57.444561+00	\N	\N	233	\N	\N	\N
267	2019-10-17 13:28:57.444582+00	2019-10-17 13:28:57.444589+00	\N	\N	234	\N	\N	\N
268	2019-10-17 13:28:57.44461+00	2019-10-17 13:28:57.444617+00	\N	\N	235	\N	\N	\N
269	2019-10-17 13:28:57.444638+00	2019-10-17 13:28:57.444645+00	\N	\N	236	\N	\N	\N
270	2019-10-17 13:28:57.444666+00	2019-10-17 13:28:57.444673+00	\N	\N	237	\N	\N	\N
271	2019-10-17 13:28:57.444694+00	2019-10-17 13:28:57.444701+00	\N	\N	238	\N	\N	\N
272	2019-10-17 13:28:57.444722+00	2019-10-17 13:28:57.444729+00	\N	\N	239	\N	\N	\N
273	2019-10-17 13:28:57.444749+00	2019-10-17 13:28:57.444757+00	\N	\N	240	\N	\N	\N
274	2019-10-17 13:28:57.444777+00	2019-10-17 13:28:57.444784+00	\N	\N	241	\N	\N	\N
275	2019-10-17 13:28:57.444805+00	2019-10-17 13:28:57.444812+00	\N	\N	242	\N	\N	\N
276	2019-10-17 13:28:57.444833+00	2019-10-17 13:28:57.44484+00	\N	\N	243	\N	\N	\N
277	2019-10-17 13:28:57.444861+00	2019-10-17 13:28:57.444868+00	\N	\N	244	\N	\N	\N
278	2019-10-17 13:28:57.444888+00	2019-10-17 13:28:57.444896+00	\N	\N	245	\N	\N	\N
279	2019-10-17 13:28:57.444916+00	2019-10-17 13:28:57.444924+00	\N	\N	246	\N	\N	\N
280	2019-10-17 13:28:57.444952+00	2019-10-17 13:28:57.444961+00	\N	\N	247	\N	\N	\N
281	2019-10-17 13:28:57.444983+00	2019-10-17 13:28:57.444991+00	\N	\N	248	\N	\N	\N
282	2019-10-17 13:28:57.445011+00	2019-10-17 13:28:57.445019+00	\N	\N	249	\N	\N	\N
283	2019-10-17 13:28:57.44504+00	2019-10-17 13:28:57.445047+00	\N	\N	250	\N	\N	\N
284	2019-10-17 13:28:57.445068+00	2019-10-17 13:28:57.445075+00	\N	\N	251	\N	\N	\N
285	2019-10-17 13:28:57.445096+00	2019-10-17 13:28:57.445103+00	\N	\N	252	\N	\N	\N
286	2019-10-17 13:28:57.445124+00	2019-10-17 13:28:57.445131+00	\N	\N	253	\N	\N	\N
287	2019-10-17 13:28:57.445152+00	2019-10-17 13:28:57.44516+00	\N	\N	254	\N	\N	\N
288	2019-10-17 13:28:57.445181+00	2019-10-17 13:28:57.445188+00	\N	\N	255	\N	\N	\N
289	2019-10-17 13:28:57.445209+00	2019-10-17 13:28:57.445216+00	\N	\N	256	\N	\N	\N
290	2019-10-17 13:28:57.445237+00	2019-10-17 13:28:57.445244+00	\N	\N	257	\N	\N	\N
291	2019-10-17 13:28:57.445265+00	2019-10-17 13:28:57.445272+00	\N	\N	258	\N	\N	\N
292	2019-10-17 13:28:57.445292+00	2019-10-17 13:28:57.4453+00	\N	\N	259	\N	\N	\N
293	2019-10-17 13:28:57.44532+00	2019-10-17 13:28:57.445328+00	\N	\N	260	\N	\N	\N
294	2019-10-17 13:28:57.445348+00	2019-10-17 13:28:57.445356+00	\N	\N	261	\N	\N	\N
295	2019-10-17 13:28:57.445376+00	2019-10-17 13:28:57.445384+00	\N	\N	262	\N	\N	\N
296	2019-10-17 13:28:57.445404+00	2019-10-17 13:28:57.445412+00	\N	\N	263	\N	\N	\N
297	2019-10-17 13:28:57.445432+00	2019-10-17 13:28:57.445439+00	\N	\N	264	\N	\N	\N
298	2019-10-17 13:28:57.44546+00	2019-10-17 13:28:57.445467+00	\N	\N	265	\N	\N	\N
299	2019-10-17 13:28:57.445487+00	2019-10-17 13:28:57.445495+00	\N	\N	266	\N	\N	\N
300	2019-10-17 13:28:57.445515+00	2019-10-17 13:28:57.445523+00	\N	\N	267	\N	\N	\N
301	2019-10-17 13:28:57.445543+00	2019-10-17 13:28:57.44555+00	\N	\N	268	\N	\N	\N
302	2019-10-17 13:28:57.445571+00	2019-10-17 13:28:57.445578+00	\N	\N	269	\N	\N	\N
303	2019-10-17 13:28:57.445599+00	2019-10-17 13:28:57.445606+00	\N	\N	270	\N	\N	\N
304	2019-10-17 13:28:57.456009+00	2019-10-17 13:28:57.456026+00	\N	12	\N	\N	\N	\N
305	2019-10-17 13:28:57.456059+00	2019-10-17 13:28:57.456068+00	\N	13	\N	\N	\N	\N
306	2019-10-17 13:28:57.456091+00	2019-10-17 13:28:57.456099+00	\N	14	\N	\N	\N	\N
307	2019-10-17 13:28:57.45612+00	2019-10-17 13:28:57.456127+00	\N	15	\N	\N	\N	\N
308	2019-10-17 13:28:57.456148+00	2019-10-17 13:28:57.456156+00	\N	16	\N	\N	\N	\N
309	2019-10-17 13:28:57.46922+00	2019-10-17 13:28:57.469239+00	1	\N	\N	\N	\N	\N
310	2019-10-17 13:28:57.469272+00	2019-10-17 13:28:57.469281+00	2	\N	\N	\N	\N	\N
311	2019-10-17 13:28:57.469303+00	2019-10-17 13:28:57.469311+00	3	\N	\N	\N	\N	\N
312	2019-10-17 13:28:57.469332+00	2019-10-17 13:28:57.469339+00	4	\N	\N	\N	\N	\N
313	2019-10-17 13:28:57.46936+00	2019-10-17 13:28:57.469368+00	5	\N	\N	\N	\N	\N
314	2019-10-17 13:28:57.469389+00	2019-10-17 13:28:57.469396+00	6	\N	\N	\N	\N	\N
315	2019-10-17 13:28:57.477672+00	2019-10-17 13:28:57.477695+00	7	\N	\N	\N	\N	\N
316	2019-10-17 13:28:57.477729+00	2019-10-17 13:28:57.477738+00	8	\N	\N	\N	\N	\N
317	2019-10-17 13:28:57.477761+00	2019-10-17 13:28:57.477768+00	9	\N	\N	\N	\N	\N
318	2019-10-17 13:28:57.47779+00	2019-10-17 13:28:57.477797+00	10	\N	\N	\N	\N	\N
319	2019-10-17 13:28:57.477818+00	2019-10-17 13:28:57.477825+00	11	\N	\N	\N	\N	\N
320	2019-10-17 13:28:57.477846+00	2019-10-17 13:28:57.477853+00	12	\N	\N	\N	\N	\N
321	2019-10-17 13:28:57.48416+00	2019-10-17 13:28:57.484177+00	13	\N	\N	\N	\N	\N
322	2019-10-17 13:28:57.484209+00	2019-10-17 13:28:57.484218+00	14	\N	\N	\N	\N	\N
323	2019-10-17 13:28:57.484251+00	2019-10-17 13:28:57.48426+00	15	\N	\N	\N	\N	\N
324	2019-10-17 13:28:57.48429+00	2019-10-17 13:28:57.484363+00	16	\N	\N	\N	\N	\N
325	2019-10-17 13:28:57.484389+00	2019-10-17 13:28:57.484396+00	17	\N	\N	\N	\N	\N
326	2019-10-17 13:28:57.484417+00	2019-10-17 13:28:57.484424+00	18	\N	\N	\N	\N	\N
327	2019-10-17 13:28:57.490874+00	2019-10-17 13:28:57.490891+00	19	\N	\N	\N	\N	\N
328	2019-10-17 13:28:57.490923+00	2019-10-17 13:28:57.490931+00	20	\N	\N	\N	\N	\N
329	2019-10-17 13:28:57.490954+00	2019-10-17 13:28:57.490961+00	21	\N	\N	\N	\N	\N
330	2019-10-17 13:28:57.490982+00	2019-10-17 13:28:57.49099+00	22	\N	\N	\N	\N	\N
331	2019-10-17 13:28:57.491011+00	2019-10-17 13:28:57.491019+00	23	\N	\N	\N	\N	\N
332	2019-10-17 13:28:57.49104+00	2019-10-17 13:28:57.491048+00	24	\N	\N	\N	\N	\N
333	2019-10-17 13:28:57.497802+00	2019-10-17 13:28:57.497818+00	25	\N	\N	\N	\N	\N
334	2019-10-17 13:28:57.49785+00	2019-10-17 13:28:57.497858+00	26	\N	\N	\N	\N	\N
335	2019-10-17 13:28:57.497881+00	2019-10-17 13:28:57.497888+00	27	\N	\N	\N	\N	\N
336	2019-10-17 13:28:57.49791+00	2019-10-17 13:28:57.497918+00	28	\N	\N	\N	\N	\N
337	2019-10-17 13:28:57.497939+00	2019-10-17 13:28:57.497947+00	29	\N	\N	\N	\N	\N
338	2019-10-17 13:28:57.497968+00	2019-10-17 13:28:57.497975+00	30	\N	\N	\N	\N	\N
339	2019-10-17 13:28:57.503613+00	2019-10-17 13:28:57.50363+00	\N	17	\N	\N	\N	\N
340	2019-10-17 13:28:57.503662+00	2019-10-17 13:28:57.503671+00	\N	18	\N	\N	\N	\N
341	2019-10-17 13:28:57.503694+00	2019-10-17 13:28:57.503702+00	\N	19	\N	\N	\N	\N
342	2019-10-17 13:28:57.503723+00	2019-10-17 13:28:57.50373+00	\N	20	\N	\N	\N	\N
343	2019-10-17 13:28:57.503751+00	2019-10-17 13:28:57.503759+00	\N	21	\N	\N	\N	\N
344	2019-10-17 13:28:57.510843+00	2019-10-17 13:28:57.51086+00	31	\N	\N	\N	\N	\N
345	2019-10-17 13:28:57.510893+00	2019-10-17 13:28:57.510902+00	32	\N	\N	\N	\N	\N
346	2019-10-17 13:28:57.510925+00	2019-10-17 13:28:57.510933+00	33	\N	\N	\N	\N	\N
347	2019-10-17 13:28:57.510955+00	2019-10-17 13:28:57.510962+00	34	\N	\N	\N	\N	\N
348	2019-10-17 13:28:57.510995+00	2019-10-17 13:28:57.511004+00	35	\N	\N	\N	\N	\N
349	2019-10-17 13:28:57.511026+00	2019-10-17 13:28:57.511033+00	36	\N	\N	\N	\N	\N
350	2019-10-17 13:28:57.522482+00	2019-10-17 13:28:57.5225+00	37	\N	\N	\N	\N	\N
351	2019-10-17 13:28:57.522538+00	2019-10-17 13:28:57.522547+00	38	\N	\N	\N	\N	\N
352	2019-10-17 13:28:57.52257+00	2019-10-17 13:28:57.522578+00	39	\N	\N	\N	\N	\N
353	2019-10-17 13:28:57.522599+00	2019-10-17 13:28:57.522606+00	40	\N	\N	\N	\N	\N
354	2019-10-17 13:28:57.522626+00	2019-10-17 13:28:57.522634+00	41	\N	\N	\N	\N	\N
355	2019-10-17 13:28:57.522654+00	2019-10-17 13:28:57.522661+00	42	\N	\N	\N	\N	\N
356	2019-10-17 13:28:57.533844+00	2019-10-17 13:28:57.533862+00	43	\N	\N	\N	\N	\N
357	2019-10-17 13:28:57.533895+00	2019-10-17 13:28:57.533904+00	44	\N	\N	\N	\N	\N
358	2019-10-17 13:28:57.533927+00	2019-10-17 13:28:57.533934+00	45	\N	\N	\N	\N	\N
359	2019-10-17 13:28:57.533955+00	2019-10-17 13:28:57.533962+00	46	\N	\N	\N	\N	\N
360	2019-10-17 13:28:57.533984+00	2019-10-17 13:28:57.533991+00	47	\N	\N	\N	\N	\N
361	2019-10-17 13:28:57.534011+00	2019-10-17 13:28:57.534019+00	48	\N	\N	\N	\N	\N
362	2019-10-17 13:28:57.545514+00	2019-10-17 13:28:57.545534+00	49	\N	\N	\N	\N	\N
363	2019-10-17 13:28:57.545568+00	2019-10-17 13:28:57.545577+00	50	\N	\N	\N	\N	\N
364	2019-10-17 13:28:57.5456+00	2019-10-17 13:28:57.545607+00	51	\N	\N	\N	\N	\N
365	2019-10-17 13:28:57.545629+00	2019-10-17 13:28:57.545636+00	52	\N	\N	\N	\N	\N
366	2019-10-17 13:28:57.545657+00	2019-10-17 13:28:57.545664+00	53	\N	\N	\N	\N	\N
367	2019-10-17 13:28:57.545685+00	2019-10-17 13:28:57.545692+00	54	\N	\N	\N	\N	\N
368	2019-10-17 13:28:57.583458+00	2019-10-17 13:28:57.583475+00	55	\N	\N	\N	\N	\N
369	2019-10-17 13:28:57.583508+00	2019-10-17 13:28:57.583517+00	56	\N	\N	\N	\N	\N
370	2019-10-17 13:28:57.583539+00	2019-10-17 13:28:57.583547+00	57	\N	\N	\N	\N	\N
371	2019-10-17 13:28:57.583568+00	2019-10-17 13:28:57.583575+00	58	\N	\N	\N	\N	\N
372	2019-10-17 13:28:57.583596+00	2019-10-17 13:28:57.583604+00	59	\N	\N	\N	\N	\N
373	2019-10-17 13:28:57.583625+00	2019-10-17 13:28:57.583632+00	60	\N	\N	\N	\N	\N
374	2019-10-17 13:28:57.591469+00	2019-10-17 13:28:57.591489+00	\N	22	\N	\N	\N	\N
375	2019-10-17 13:28:57.591522+00	2019-10-17 13:28:57.591531+00	\N	23	\N	\N	\N	\N
376	2019-10-17 13:28:57.591554+00	2019-10-17 13:28:57.591562+00	\N	24	\N	\N	\N	\N
377	2019-10-17 13:28:57.591583+00	2019-10-17 13:28:57.59159+00	\N	25	\N	\N	\N	\N
378	2019-10-17 13:28:57.591611+00	2019-10-17 13:28:57.59163+00	\N	26	\N	\N	\N	\N
379	2019-10-17 13:28:57.603334+00	2019-10-17 13:28:57.603352+00	61	\N	\N	\N	\N	\N
380	2019-10-17 13:28:57.603386+00	2019-10-17 13:28:57.603394+00	62	\N	\N	\N	\N	\N
381	2019-10-17 13:28:57.603417+00	2019-10-17 13:28:57.603425+00	63	\N	\N	\N	\N	\N
382	2019-10-17 13:28:57.603446+00	2019-10-17 13:28:57.603454+00	64	\N	\N	\N	\N	\N
383	2019-10-17 13:28:57.603475+00	2019-10-17 13:28:57.603483+00	65	\N	\N	\N	\N	\N
384	2019-10-17 13:28:57.603503+00	2019-10-17 13:28:57.603511+00	66	\N	\N	\N	\N	\N
385	2019-10-17 13:28:57.614592+00	2019-10-17 13:28:57.614612+00	67	\N	\N	\N	\N	\N
386	2019-10-17 13:28:57.614646+00	2019-10-17 13:28:57.614655+00	68	\N	\N	\N	\N	\N
387	2019-10-17 13:28:57.614688+00	2019-10-17 13:28:57.614698+00	69	\N	\N	\N	\N	\N
388	2019-10-17 13:28:57.614721+00	2019-10-17 13:28:57.614729+00	70	\N	\N	\N	\N	\N
389	2019-10-17 13:28:57.61475+00	2019-10-17 13:28:57.614757+00	71	\N	\N	\N	\N	\N
390	2019-10-17 13:28:57.614778+00	2019-10-17 13:28:57.614785+00	72	\N	\N	\N	\N	\N
391	2019-10-17 13:28:57.625816+00	2019-10-17 13:28:57.625834+00	73	\N	\N	\N	\N	\N
392	2019-10-17 13:28:57.625867+00	2019-10-17 13:28:57.625876+00	74	\N	\N	\N	\N	\N
393	2019-10-17 13:28:57.625899+00	2019-10-17 13:28:57.625907+00	75	\N	\N	\N	\N	\N
394	2019-10-17 13:28:57.625928+00	2019-10-17 13:28:57.625935+00	76	\N	\N	\N	\N	\N
395	2019-10-17 13:28:57.625956+00	2019-10-17 13:28:57.625964+00	77	\N	\N	\N	\N	\N
396	2019-10-17 13:28:57.625984+00	2019-10-17 13:28:57.625992+00	78	\N	\N	\N	\N	\N
397	2019-10-17 13:28:57.632487+00	2019-10-17 13:28:57.632506+00	79	\N	\N	\N	\N	\N
398	2019-10-17 13:28:57.632539+00	2019-10-17 13:28:57.632548+00	80	\N	\N	\N	\N	\N
399	2019-10-17 13:28:57.632571+00	2019-10-17 13:28:57.632579+00	81	\N	\N	\N	\N	\N
400	2019-10-17 13:28:57.6326+00	2019-10-17 13:28:57.632608+00	82	\N	\N	\N	\N	\N
401	2019-10-17 13:28:57.632629+00	2019-10-17 13:28:57.632636+00	83	\N	\N	\N	\N	\N
402	2019-10-17 13:28:57.632657+00	2019-10-17 13:28:57.632665+00	84	\N	\N	\N	\N	\N
403	2019-10-17 13:28:57.643061+00	2019-10-17 13:28:57.643078+00	85	\N	\N	\N	\N	\N
404	2019-10-17 13:28:57.643111+00	2019-10-17 13:28:57.64312+00	86	\N	\N	\N	\N	\N
405	2019-10-17 13:28:57.643144+00	2019-10-17 13:28:57.643152+00	87	\N	\N	\N	\N	\N
406	2019-10-17 13:28:57.643173+00	2019-10-17 13:28:57.643181+00	88	\N	\N	\N	\N	\N
407	2019-10-17 13:28:57.643202+00	2019-10-17 13:28:57.643209+00	89	\N	\N	\N	\N	\N
408	2019-10-17 13:28:57.64323+00	2019-10-17 13:28:57.643238+00	90	\N	\N	\N	\N	\N
409	2019-10-17 13:28:57.654262+00	2019-10-17 13:28:57.654283+00	\N	27	\N	\N	\N	\N
410	2019-10-17 13:28:57.654317+00	2019-10-17 13:28:57.654326+00	\N	28	\N	\N	\N	\N
411	2019-10-17 13:28:57.654348+00	2019-10-17 13:28:57.654356+00	\N	29	\N	\N	\N	\N
412	2019-10-17 13:28:57.654377+00	2019-10-17 13:28:57.654385+00	\N	30	\N	\N	\N	\N
413	2019-10-17 13:28:57.654405+00	2019-10-17 13:28:57.654413+00	\N	31	\N	\N	\N	\N
414	2019-10-17 13:28:57.665971+00	2019-10-17 13:28:57.665989+00	91	\N	\N	\N	\N	\N
415	2019-10-17 13:28:57.666022+00	2019-10-17 13:28:57.666031+00	92	\N	\N	\N	\N	\N
416	2019-10-17 13:28:57.666054+00	2019-10-17 13:28:57.666062+00	93	\N	\N	\N	\N	\N
417	2019-10-17 13:28:57.666083+00	2019-10-17 13:28:57.66609+00	94	\N	\N	\N	\N	\N
418	2019-10-17 13:28:57.666111+00	2019-10-17 13:28:57.666118+00	95	\N	\N	\N	\N	\N
419	2019-10-17 13:28:57.666139+00	2019-10-17 13:28:57.666146+00	96	\N	\N	\N	\N	\N
420	2019-10-17 13:28:57.677083+00	2019-10-17 13:28:57.677102+00	97	\N	\N	\N	\N	\N
421	2019-10-17 13:28:57.677136+00	2019-10-17 13:28:57.677145+00	98	\N	\N	\N	\N	\N
422	2019-10-17 13:28:57.677168+00	2019-10-17 13:28:57.677176+00	99	\N	\N	\N	\N	\N
423	2019-10-17 13:28:57.677198+00	2019-10-17 13:28:57.677205+00	100	\N	\N	\N	\N	\N
424	2019-10-17 13:28:57.677226+00	2019-10-17 13:28:57.677233+00	101	\N	\N	\N	\N	\N
425	2019-10-17 13:28:57.677255+00	2019-10-17 13:28:57.677262+00	102	\N	\N	\N	\N	\N
426	2019-10-17 13:28:57.688069+00	2019-10-17 13:28:57.688087+00	103	\N	\N	\N	\N	\N
427	2019-10-17 13:28:57.68812+00	2019-10-17 13:28:57.688129+00	104	\N	\N	\N	\N	\N
428	2019-10-17 13:28:57.688152+00	2019-10-17 13:28:57.68816+00	105	\N	\N	\N	\N	\N
429	2019-10-17 13:28:57.688181+00	2019-10-17 13:28:57.688189+00	106	\N	\N	\N	\N	\N
430	2019-10-17 13:28:57.68821+00	2019-10-17 13:28:57.688218+00	107	\N	\N	\N	\N	\N
431	2019-10-17 13:28:57.688238+00	2019-10-17 13:28:57.688246+00	108	\N	\N	\N	\N	\N
432	2019-10-17 13:28:57.699342+00	2019-10-17 13:28:57.69936+00	109	\N	\N	\N	\N	\N
433	2019-10-17 13:28:57.699393+00	2019-10-17 13:28:57.699402+00	110	\N	\N	\N	\N	\N
434	2019-10-17 13:28:57.699426+00	2019-10-17 13:28:57.699434+00	111	\N	\N	\N	\N	\N
435	2019-10-17 13:28:57.699455+00	2019-10-17 13:28:57.699463+00	112	\N	\N	\N	\N	\N
436	2019-10-17 13:28:57.699484+00	2019-10-17 13:28:57.699492+00	113	\N	\N	\N	\N	\N
437	2019-10-17 13:28:57.699512+00	2019-10-17 13:28:57.69952+00	114	\N	\N	\N	\N	\N
438	2019-10-17 13:28:57.707886+00	2019-10-17 13:28:57.707903+00	115	\N	\N	\N	\N	\N
439	2019-10-17 13:28:57.707937+00	2019-10-17 13:28:57.707946+00	116	\N	\N	\N	\N	\N
440	2019-10-17 13:28:57.707969+00	2019-10-17 13:28:57.707977+00	117	\N	\N	\N	\N	\N
441	2019-10-17 13:28:57.707998+00	2019-10-17 13:28:57.708006+00	118	\N	\N	\N	\N	\N
442	2019-10-17 13:28:57.708027+00	2019-10-17 13:28:57.708035+00	119	\N	\N	\N	\N	\N
443	2019-10-17 13:28:57.708056+00	2019-10-17 13:28:57.708063+00	120	\N	\N	\N	\N	\N
444	2019-10-17 13:28:57.718432+00	2019-10-17 13:28:57.718452+00	\N	32	\N	\N	\N	\N
445	2019-10-17 13:28:57.718485+00	2019-10-17 13:28:57.718493+00	\N	33	\N	\N	\N	\N
446	2019-10-17 13:28:57.718516+00	2019-10-17 13:28:57.718524+00	\N	34	\N	\N	\N	\N
447	2019-10-17 13:28:57.718545+00	2019-10-17 13:28:57.718552+00	\N	35	\N	\N	\N	\N
448	2019-10-17 13:28:57.718573+00	2019-10-17 13:28:57.71858+00	\N	36	\N	\N	\N	\N
449	2019-10-17 13:28:57.732086+00	2019-10-17 13:28:57.732108+00	121	\N	\N	\N	\N	\N
450	2019-10-17 13:28:57.732144+00	2019-10-17 13:28:57.732153+00	122	\N	\N	\N	\N	\N
451	2019-10-17 13:28:57.732176+00	2019-10-17 13:28:57.732184+00	123	\N	\N	\N	\N	\N
452	2019-10-17 13:28:57.732205+00	2019-10-17 13:28:57.732213+00	124	\N	\N	\N	\N	\N
453	2019-10-17 13:28:57.732233+00	2019-10-17 13:28:57.732241+00	125	\N	\N	\N	\N	\N
454	2019-10-17 13:28:57.732262+00	2019-10-17 13:28:57.732269+00	126	\N	\N	\N	\N	\N
455	2019-10-17 13:28:57.743137+00	2019-10-17 13:28:57.743155+00	127	\N	\N	\N	\N	\N
456	2019-10-17 13:28:57.743188+00	2019-10-17 13:28:57.743197+00	128	\N	\N	\N	\N	\N
457	2019-10-17 13:28:57.74322+00	2019-10-17 13:28:57.743227+00	129	\N	\N	\N	\N	\N
458	2019-10-17 13:28:57.743248+00	2019-10-17 13:28:57.743285+00	130	\N	\N	\N	\N	\N
459	2019-10-17 13:28:57.743312+00	2019-10-17 13:28:57.743319+00	131	\N	\N	\N	\N	\N
460	2019-10-17 13:28:57.74334+00	2019-10-17 13:28:57.743348+00	132	\N	\N	\N	\N	\N
461	2019-10-17 13:28:57.754083+00	2019-10-17 13:28:57.754102+00	133	\N	\N	\N	\N	\N
462	2019-10-17 13:28:57.754136+00	2019-10-17 13:28:57.754145+00	134	\N	\N	\N	\N	\N
463	2019-10-17 13:28:57.754168+00	2019-10-17 13:28:57.754175+00	135	\N	\N	\N	\N	\N
464	2019-10-17 13:28:57.754196+00	2019-10-17 13:28:57.754203+00	136	\N	\N	\N	\N	\N
465	2019-10-17 13:28:57.754224+00	2019-10-17 13:28:57.754231+00	137	\N	\N	\N	\N	\N
466	2019-10-17 13:28:57.754252+00	2019-10-17 13:28:57.754259+00	138	\N	\N	\N	\N	\N
467	2019-10-17 13:28:57.765353+00	2019-10-17 13:28:57.765373+00	139	\N	\N	\N	\N	\N
468	2019-10-17 13:28:57.765406+00	2019-10-17 13:28:57.765414+00	140	\N	\N	\N	\N	\N
469	2019-10-17 13:28:57.765437+00	2019-10-17 13:28:57.765445+00	141	\N	\N	\N	\N	\N
470	2019-10-17 13:28:57.765466+00	2019-10-17 13:28:57.765473+00	142	\N	\N	\N	\N	\N
471	2019-10-17 13:28:57.765494+00	2019-10-17 13:28:57.765502+00	143	\N	\N	\N	\N	\N
472	2019-10-17 13:28:57.765522+00	2019-10-17 13:28:57.765529+00	144	\N	\N	\N	\N	\N
473	2019-10-17 13:28:57.776003+00	2019-10-17 13:28:57.77602+00	145	\N	\N	\N	\N	\N
474	2019-10-17 13:28:57.776054+00	2019-10-17 13:28:57.776063+00	146	\N	\N	\N	\N	\N
475	2019-10-17 13:28:57.776087+00	2019-10-17 13:28:57.776094+00	147	\N	\N	\N	\N	\N
476	2019-10-17 13:28:57.776129+00	2019-10-17 13:28:57.776137+00	148	\N	\N	\N	\N	\N
477	2019-10-17 13:28:57.776158+00	2019-10-17 13:28:57.776166+00	149	\N	\N	\N	\N	\N
478	2019-10-17 13:28:57.776187+00	2019-10-17 13:28:57.776194+00	150	\N	\N	\N	\N	\N
\.


--
-- Data for Name: locations_pigletsgroupcell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_pigletsgroupcell (id, created_at, modified_at, number, section_id, workshop_id) FROM stdin;
1	2019-10-17 13:28:57.462111+00	2019-10-17 13:28:57.462129+00	1	12	4
2	2019-10-17 13:28:57.462166+00	2019-10-17 13:28:57.462175+00	2	12	4
3	2019-10-17 13:28:57.4622+00	2019-10-17 13:28:57.462208+00	3	12	4
4	2019-10-17 13:28:57.462232+00	2019-10-17 13:28:57.462239+00	4	12	4
5	2019-10-17 13:28:57.462262+00	2019-10-17 13:28:57.462269+00	5	12	4
6	2019-10-17 13:28:57.462292+00	2019-10-17 13:28:57.4623+00	6	12	4
7	2019-10-17 13:28:57.474678+00	2019-10-17 13:28:57.474696+00	1	13	4
8	2019-10-17 13:28:57.474733+00	2019-10-17 13:28:57.474742+00	2	13	4
9	2019-10-17 13:28:57.474766+00	2019-10-17 13:28:57.474773+00	3	13	4
10	2019-10-17 13:28:57.474796+00	2019-10-17 13:28:57.474804+00	4	13	4
11	2019-10-17 13:28:57.474826+00	2019-10-17 13:28:57.474834+00	5	13	4
12	2019-10-17 13:28:57.474856+00	2019-10-17 13:28:57.474863+00	6	13	4
13	2019-10-17 13:28:57.480841+00	2019-10-17 13:28:57.480857+00	1	14	4
14	2019-10-17 13:28:57.480894+00	2019-10-17 13:28:57.480903+00	2	14	4
15	2019-10-17 13:28:57.480927+00	2019-10-17 13:28:57.480934+00	3	14	4
16	2019-10-17 13:28:57.480957+00	2019-10-17 13:28:57.480965+00	4	14	4
17	2019-10-17 13:28:57.480987+00	2019-10-17 13:28:57.480995+00	5	14	4
18	2019-10-17 13:28:57.481017+00	2019-10-17 13:28:57.481024+00	6	14	4
19	2019-10-17 13:28:57.48723+00	2019-10-17 13:28:57.487246+00	1	15	4
20	2019-10-17 13:28:57.48731+00	2019-10-17 13:28:57.48732+00	2	15	4
21	2019-10-17 13:28:57.487344+00	2019-10-17 13:28:57.487352+00	3	15	4
22	2019-10-17 13:28:57.487374+00	2019-10-17 13:28:57.487382+00	4	15	4
23	2019-10-17 13:28:57.487404+00	2019-10-17 13:28:57.487412+00	5	15	4
24	2019-10-17 13:28:57.487434+00	2019-10-17 13:28:57.487442+00	6	15	4
25	2019-10-17 13:28:57.494587+00	2019-10-17 13:28:57.494604+00	1	16	4
26	2019-10-17 13:28:57.494641+00	2019-10-17 13:28:57.49465+00	2	16	4
27	2019-10-17 13:28:57.494674+00	2019-10-17 13:28:57.494682+00	3	16	4
28	2019-10-17 13:28:57.494706+00	2019-10-17 13:28:57.494713+00	4	16	4
29	2019-10-17 13:28:57.494736+00	2019-10-17 13:28:57.494743+00	5	16	4
30	2019-10-17 13:28:57.494766+00	2019-10-17 13:28:57.494773+00	6	16	4
31	2019-10-17 13:28:57.507452+00	2019-10-17 13:28:57.50747+00	1	17	6
32	2019-10-17 13:28:57.507506+00	2019-10-17 13:28:57.507515+00	2	17	6
33	2019-10-17 13:28:57.507539+00	2019-10-17 13:28:57.507547+00	3	17	6
34	2019-10-17 13:28:57.50757+00	2019-10-17 13:28:57.507577+00	4	17	6
35	2019-10-17 13:28:57.5076+00	2019-10-17 13:28:57.507607+00	5	17	6
36	2019-10-17 13:28:57.50763+00	2019-10-17 13:28:57.507637+00	6	17	6
37	2019-10-17 13:28:57.516845+00	2019-10-17 13:28:57.516862+00	1	18	6
38	2019-10-17 13:28:57.5169+00	2019-10-17 13:28:57.516909+00	2	18	6
39	2019-10-17 13:28:57.516933+00	2019-10-17 13:28:57.516941+00	3	18	6
40	2019-10-17 13:28:57.516964+00	2019-10-17 13:28:57.516971+00	4	18	6
41	2019-10-17 13:28:57.516994+00	2019-10-17 13:28:57.517002+00	5	18	6
42	2019-10-17 13:28:57.517038+00	2019-10-17 13:28:57.517047+00	6	18	6
43	2019-10-17 13:28:57.527994+00	2019-10-17 13:28:57.528013+00	1	19	6
44	2019-10-17 13:28:57.528053+00	2019-10-17 13:28:57.528064+00	2	19	6
45	2019-10-17 13:28:57.528088+00	2019-10-17 13:28:57.528096+00	3	19	6
46	2019-10-17 13:28:57.528119+00	2019-10-17 13:28:57.528126+00	4	19	6
47	2019-10-17 13:28:57.528149+00	2019-10-17 13:28:57.528157+00	5	19	6
48	2019-10-17 13:28:57.528179+00	2019-10-17 13:28:57.528187+00	6	19	6
49	2019-10-17 13:28:57.53947+00	2019-10-17 13:28:57.539487+00	1	20	6
50	2019-10-17 13:28:57.539525+00	2019-10-17 13:28:57.539534+00	2	20	6
51	2019-10-17 13:28:57.539558+00	2019-10-17 13:28:57.539566+00	3	20	6
52	2019-10-17 13:28:57.539589+00	2019-10-17 13:28:57.539597+00	4	20	6
53	2019-10-17 13:28:57.53962+00	2019-10-17 13:28:57.539627+00	5	20	6
54	2019-10-17 13:28:57.53965+00	2019-10-17 13:28:57.539658+00	6	20	6
55	2019-10-17 13:28:57.577521+00	2019-10-17 13:28:57.577544+00	1	21	6
56	2019-10-17 13:28:57.577584+00	2019-10-17 13:28:57.577592+00	2	21	6
57	2019-10-17 13:28:57.577617+00	2019-10-17 13:28:57.577625+00	3	21	6
58	2019-10-17 13:28:57.577648+00	2019-10-17 13:28:57.577655+00	4	21	6
59	2019-10-17 13:28:57.577678+00	2019-10-17 13:28:57.577685+00	5	21	6
60	2019-10-17 13:28:57.577708+00	2019-10-17 13:28:57.577715+00	6	21	6
61	2019-10-17 13:28:57.597832+00	2019-10-17 13:28:57.597851+00	1	22	7
62	2019-10-17 13:28:57.597889+00	2019-10-17 13:28:57.597899+00	2	22	7
63	2019-10-17 13:28:57.597923+00	2019-10-17 13:28:57.597931+00	3	22	7
64	2019-10-17 13:28:57.597954+00	2019-10-17 13:28:57.597962+00	4	22	7
65	2019-10-17 13:28:57.597984+00	2019-10-17 13:28:57.597992+00	5	22	7
66	2019-10-17 13:28:57.598015+00	2019-10-17 13:28:57.598023+00	6	22	7
67	2019-10-17 13:28:57.608633+00	2019-10-17 13:28:57.608653+00	1	23	7
68	2019-10-17 13:28:57.608693+00	2019-10-17 13:28:57.608702+00	2	23	7
69	2019-10-17 13:28:57.608726+00	2019-10-17 13:28:57.608734+00	3	23	7
70	2019-10-17 13:28:57.608757+00	2019-10-17 13:28:57.608765+00	4	23	7
71	2019-10-17 13:28:57.608788+00	2019-10-17 13:28:57.608796+00	5	23	7
72	2019-10-17 13:28:57.608818+00	2019-10-17 13:28:57.608826+00	6	23	7
73	2019-10-17 13:28:57.62018+00	2019-10-17 13:28:57.620199+00	1	24	7
74	2019-10-17 13:28:57.620236+00	2019-10-17 13:28:57.620245+00	2	24	7
75	2019-10-17 13:28:57.62027+00	2019-10-17 13:28:57.620278+00	3	24	7
76	2019-10-17 13:28:57.620372+00	2019-10-17 13:28:57.620381+00	4	24	7
77	2019-10-17 13:28:57.620406+00	2019-10-17 13:28:57.620414+00	5	24	7
78	2019-10-17 13:28:57.620441+00	2019-10-17 13:28:57.62045+00	6	24	7
79	2019-10-17 13:28:57.628933+00	2019-10-17 13:28:57.62896+00	1	25	7
80	2019-10-17 13:28:57.629+00	2019-10-17 13:28:57.629009+00	2	25	7
81	2019-10-17 13:28:57.629034+00	2019-10-17 13:28:57.629042+00	3	25	7
82	2019-10-17 13:28:57.629065+00	2019-10-17 13:28:57.629072+00	4	25	7
83	2019-10-17 13:28:57.629094+00	2019-10-17 13:28:57.629102+00	5	25	7
84	2019-10-17 13:28:57.629124+00	2019-10-17 13:28:57.629148+00	6	25	7
85	2019-10-17 13:28:57.637832+00	2019-10-17 13:28:57.63785+00	1	26	7
86	2019-10-17 13:28:57.637887+00	2019-10-17 13:28:57.637897+00	2	26	7
87	2019-10-17 13:28:57.637922+00	2019-10-17 13:28:57.63793+00	3	26	7
88	2019-10-17 13:28:57.637953+00	2019-10-17 13:28:57.63796+00	4	26	7
89	2019-10-17 13:28:57.637983+00	2019-10-17 13:28:57.637991+00	5	26	7
90	2019-10-17 13:28:57.638014+00	2019-10-17 13:28:57.638021+00	6	26	7
91	2019-10-17 13:28:57.660248+00	2019-10-17 13:28:57.660266+00	1	27	8
92	2019-10-17 13:28:57.660318+00	2019-10-17 13:28:57.660329+00	2	27	8
93	2019-10-17 13:28:57.660354+00	2019-10-17 13:28:57.660362+00	3	27	8
94	2019-10-17 13:28:57.660385+00	2019-10-17 13:28:57.660393+00	4	27	8
95	2019-10-17 13:28:57.660416+00	2019-10-17 13:28:57.660423+00	5	27	8
96	2019-10-17 13:28:57.660446+00	2019-10-17 13:28:57.660453+00	6	27	8
97	2019-10-17 13:28:57.671197+00	2019-10-17 13:28:57.671215+00	1	28	8
98	2019-10-17 13:28:57.671267+00	2019-10-17 13:28:57.671291+00	2	28	8
99	2019-10-17 13:28:57.671321+00	2019-10-17 13:28:57.671329+00	3	28	8
100	2019-10-17 13:28:57.671352+00	2019-10-17 13:28:57.671359+00	4	28	8
101	2019-10-17 13:28:57.671382+00	2019-10-17 13:28:57.671389+00	5	28	8
102	2019-10-17 13:28:57.671412+00	2019-10-17 13:28:57.671419+00	6	28	8
103	2019-10-17 13:28:57.682728+00	2019-10-17 13:28:57.682746+00	1	29	8
104	2019-10-17 13:28:57.682784+00	2019-10-17 13:28:57.682793+00	2	29	8
105	2019-10-17 13:28:57.682818+00	2019-10-17 13:28:57.682826+00	3	29	8
106	2019-10-17 13:28:57.682849+00	2019-10-17 13:28:57.682856+00	4	29	8
107	2019-10-17 13:28:57.68288+00	2019-10-17 13:28:57.682887+00	5	29	8
108	2019-10-17 13:28:57.68291+00	2019-10-17 13:28:57.682918+00	6	29	8
109	2019-10-17 13:28:57.693583+00	2019-10-17 13:28:57.693601+00	1	30	8
110	2019-10-17 13:28:57.693639+00	2019-10-17 13:28:57.693648+00	2	30	8
111	2019-10-17 13:28:57.693672+00	2019-10-17 13:28:57.69368+00	3	30	8
112	2019-10-17 13:28:57.693703+00	2019-10-17 13:28:57.693711+00	4	30	8
113	2019-10-17 13:28:57.693733+00	2019-10-17 13:28:57.693741+00	5	30	8
114	2019-10-17 13:28:57.693764+00	2019-10-17 13:28:57.693771+00	6	30	8
115	2019-10-17 13:28:57.702372+00	2019-10-17 13:28:57.70239+00	1	31	8
116	2019-10-17 13:28:57.702427+00	2019-10-17 13:28:57.702437+00	2	31	8
117	2019-10-17 13:28:57.702461+00	2019-10-17 13:28:57.702469+00	3	31	8
118	2019-10-17 13:28:57.702492+00	2019-10-17 13:28:57.7025+00	4	31	8
119	2019-10-17 13:28:57.702523+00	2019-10-17 13:28:57.702531+00	5	31	8
120	2019-10-17 13:28:57.702553+00	2019-10-17 13:28:57.702561+00	6	31	8
121	2019-10-17 13:28:57.724685+00	2019-10-17 13:28:57.724705+00	1	32	5
122	2019-10-17 13:28:57.724743+00	2019-10-17 13:28:57.724753+00	2	32	5
123	2019-10-17 13:28:57.724777+00	2019-10-17 13:28:57.724785+00	3	32	5
124	2019-10-17 13:28:57.724808+00	2019-10-17 13:28:57.724816+00	4	32	5
125	2019-10-17 13:28:57.724839+00	2019-10-17 13:28:57.724846+00	5	32	5
126	2019-10-17 13:28:57.724869+00	2019-10-17 13:28:57.724877+00	6	32	5
127	2019-10-17 13:28:57.737697+00	2019-10-17 13:28:57.737716+00	1	33	5
128	2019-10-17 13:28:57.737754+00	2019-10-17 13:28:57.737763+00	2	33	5
129	2019-10-17 13:28:57.737787+00	2019-10-17 13:28:57.737795+00	3	33	5
130	2019-10-17 13:28:57.737818+00	2019-10-17 13:28:57.737825+00	4	33	5
131	2019-10-17 13:28:57.737848+00	2019-10-17 13:28:57.737855+00	5	33	5
132	2019-10-17 13:28:57.737877+00	2019-10-17 13:28:57.737885+00	6	33	5
133	2019-10-17 13:28:57.748412+00	2019-10-17 13:28:57.74843+00	1	34	5
134	2019-10-17 13:28:57.748467+00	2019-10-17 13:28:57.748477+00	2	34	5
135	2019-10-17 13:28:57.748501+00	2019-10-17 13:28:57.748509+00	3	34	5
136	2019-10-17 13:28:57.748531+00	2019-10-17 13:28:57.748539+00	4	34	5
137	2019-10-17 13:28:57.748561+00	2019-10-17 13:28:57.748568+00	5	34	5
138	2019-10-17 13:28:57.74859+00	2019-10-17 13:28:57.748598+00	6	34	5
139	2019-10-17 13:28:57.759365+00	2019-10-17 13:28:57.759383+00	1	35	5
140	2019-10-17 13:28:57.759421+00	2019-10-17 13:28:57.759431+00	2	35	5
141	2019-10-17 13:28:57.759455+00	2019-10-17 13:28:57.759463+00	3	35	5
142	2019-10-17 13:28:57.759486+00	2019-10-17 13:28:57.759494+00	4	35	5
143	2019-10-17 13:28:57.759516+00	2019-10-17 13:28:57.759524+00	5	35	5
144	2019-10-17 13:28:57.759546+00	2019-10-17 13:28:57.759554+00	6	35	5
145	2019-10-17 13:28:57.770575+00	2019-10-17 13:28:57.770593+00	1	36	5
146	2019-10-17 13:28:57.770629+00	2019-10-17 13:28:57.770638+00	2	36	5
147	2019-10-17 13:28:57.770663+00	2019-10-17 13:28:57.77067+00	3	36	5
148	2019-10-17 13:28:57.770694+00	2019-10-17 13:28:57.770701+00	4	36	5
149	2019-10-17 13:28:57.770723+00	2019-10-17 13:28:57.77073+00	5	36	5
150	2019-10-17 13:28:57.770752+00	2019-10-17 13:28:57.77076+00	6	36	5
\.


--
-- Data for Name: locations_section; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_section (id, created_at, modified_at, name, number, workshop_id) FROM stdin;
1	2019-10-17 13:28:57.27368+00	2019-10-17 13:28:57.273698+00	Змейка	1	1
2	2019-10-17 13:28:57.273739+00	2019-10-17 13:28:57.273749+00	Ряд осеменения	2	1
3	2019-10-17 13:28:57.273781+00	2019-10-17 13:28:57.273789+00	Групповые клетки	3	1
4	2019-10-17 13:28:57.285471+00	2019-10-17 13:28:57.285489+00	Секция 2-1	1	2
5	2019-10-17 13:28:57.285521+00	2019-10-17 13:28:57.28553+00	Секция 2-2	2	2
6	2019-10-17 13:28:57.32573+00	2019-10-17 13:28:57.32575+00	Секция 3-1	1	3
7	2019-10-17 13:28:57.325782+00	2019-10-17 13:28:57.325791+00	Секция 3-2	2	3
8	2019-10-17 13:28:57.325817+00	2019-10-17 13:28:57.325824+00	Секция 3-3	3	3
9	2019-10-17 13:28:57.325844+00	2019-10-17 13:28:57.325851+00	Секция 3-4	4	3
10	2019-10-17 13:28:57.32587+00	2019-10-17 13:28:57.325878+00	Секция 3-5	5	3
11	2019-10-17 13:28:57.325897+00	2019-10-17 13:28:57.325905+00	Секция 3-6	6	3
12	2019-10-17 13:28:57.451006+00	2019-10-17 13:28:57.451023+00	Секция 4-1	1	4
13	2019-10-17 13:28:57.451055+00	2019-10-17 13:28:57.451063+00	Секция 4-2	2	4
14	2019-10-17 13:28:57.451084+00	2019-10-17 13:28:57.451092+00	Секция 4-3	3	4
15	2019-10-17 13:28:57.451112+00	2019-10-17 13:28:57.451119+00	Секция 4-4	4	4
16	2019-10-17 13:28:57.451138+00	2019-10-17 13:28:57.451145+00	Секция 4-5	5	4
17	2019-10-17 13:28:57.500681+00	2019-10-17 13:28:57.500699+00	Секция 5-1	1	6
18	2019-10-17 13:28:57.500731+00	2019-10-17 13:28:57.50074+00	Секция 5-2	2	6
19	2019-10-17 13:28:57.500762+00	2019-10-17 13:28:57.50077+00	Секция 5-3	3	6
20	2019-10-17 13:28:57.50079+00	2019-10-17 13:28:57.500797+00	Секция 5-4	4	6
21	2019-10-17 13:28:57.500816+00	2019-10-17 13:28:57.500824+00	Секция 5-5	5	6
22	2019-10-17 13:28:57.586404+00	2019-10-17 13:28:57.586423+00	Секция 6-1	1	7
23	2019-10-17 13:28:57.586456+00	2019-10-17 13:28:57.586465+00	Секция 6-2	2	7
24	2019-10-17 13:28:57.586486+00	2019-10-17 13:28:57.586494+00	Секция 6-3	3	7
25	2019-10-17 13:28:57.586513+00	2019-10-17 13:28:57.58652+00	Секция 6-4	4	7
26	2019-10-17 13:28:57.586539+00	2019-10-17 13:28:57.586546+00	Секция 6-5	5	7
27	2019-10-17 13:28:57.649047+00	2019-10-17 13:28:57.649066+00	Секция 7-1	1	8
28	2019-10-17 13:28:57.649099+00	2019-10-17 13:28:57.649109+00	Секция 7-2	2	8
29	2019-10-17 13:28:57.64913+00	2019-10-17 13:28:57.649137+00	Секция 7-3	3	8
30	2019-10-17 13:28:57.649157+00	2019-10-17 13:28:57.649164+00	Секция 7-4	4	8
31	2019-10-17 13:28:57.649183+00	2019-10-17 13:28:57.649191+00	Секция 7-5	5	8
32	2019-10-17 13:28:57.713188+00	2019-10-17 13:28:57.713206+00	Секция 8-1	1	5
33	2019-10-17 13:28:57.713238+00	2019-10-17 13:28:57.713247+00	Секция 8-2	2	5
34	2019-10-17 13:28:57.713268+00	2019-10-17 13:28:57.713276+00	Секция 8-3	3	5
35	2019-10-17 13:28:57.713295+00	2019-10-17 13:28:57.713303+00	Секция 8-4	4	5
36	2019-10-17 13:28:57.713322+00	2019-10-17 13:28:57.713329+00	Секция 8-5	5	5
\.


--
-- Data for Name: locations_sowandpigletscell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowandpigletscell (id, created_at, modified_at, number, section_id, workshop_id) FROM stdin;
1	2019-10-17 13:28:57.338068+00	2019-10-17 13:28:57.338086+00	1	6	3
2	2019-10-17 13:28:57.338125+00	2019-10-17 13:28:57.338134+00	2	6	3
3	2019-10-17 13:28:57.338158+00	2019-10-17 13:28:57.338166+00	3	6	3
4	2019-10-17 13:28:57.338189+00	2019-10-17 13:28:57.338196+00	4	6	3
5	2019-10-17 13:28:57.338219+00	2019-10-17 13:28:57.338226+00	5	6	3
6	2019-10-17 13:28:57.338249+00	2019-10-17 13:28:57.338257+00	6	6	3
7	2019-10-17 13:28:57.33828+00	2019-10-17 13:28:57.338287+00	7	6	3
8	2019-10-17 13:28:57.338309+00	2019-10-17 13:28:57.338317+00	8	6	3
9	2019-10-17 13:28:57.338339+00	2019-10-17 13:28:57.338355+00	9	6	3
10	2019-10-17 13:28:57.338383+00	2019-10-17 13:28:57.338391+00	10	6	3
11	2019-10-17 13:28:57.338414+00	2019-10-17 13:28:57.338422+00	11	6	3
12	2019-10-17 13:28:57.338444+00	2019-10-17 13:28:57.338452+00	12	6	3
13	2019-10-17 13:28:57.338474+00	2019-10-17 13:28:57.338482+00	13	6	3
14	2019-10-17 13:28:57.338504+00	2019-10-17 13:28:57.338512+00	14	6	3
15	2019-10-17 13:28:57.338534+00	2019-10-17 13:28:57.338541+00	15	6	3
16	2019-10-17 13:28:57.338563+00	2019-10-17 13:28:57.338578+00	16	6	3
17	2019-10-17 13:28:57.338629+00	2019-10-17 13:28:57.338639+00	17	6	3
18	2019-10-17 13:28:57.338663+00	2019-10-17 13:28:57.338671+00	18	6	3
19	2019-10-17 13:28:57.338694+00	2019-10-17 13:28:57.338701+00	19	6	3
20	2019-10-17 13:28:57.338724+00	2019-10-17 13:28:57.338731+00	20	6	3
21	2019-10-17 13:28:57.338754+00	2019-10-17 13:28:57.338761+00	21	6	3
22	2019-10-17 13:28:57.338784+00	2019-10-17 13:28:57.338791+00	22	6	3
23	2019-10-17 13:28:57.338814+00	2019-10-17 13:28:57.338821+00	23	6	3
24	2019-10-17 13:28:57.338844+00	2019-10-17 13:28:57.338851+00	24	6	3
25	2019-10-17 13:28:57.338883+00	2019-10-17 13:28:57.338891+00	25	6	3
26	2019-10-17 13:28:57.338915+00	2019-10-17 13:28:57.338923+00	26	6	3
27	2019-10-17 13:28:57.338945+00	2019-10-17 13:28:57.338953+00	27	6	3
28	2019-10-17 13:28:57.338975+00	2019-10-17 13:28:57.338982+00	28	6	3
29	2019-10-17 13:28:57.339005+00	2019-10-17 13:28:57.339012+00	29	6	3
30	2019-10-17 13:28:57.339034+00	2019-10-17 13:28:57.339042+00	30	6	3
31	2019-10-17 13:28:57.339064+00	2019-10-17 13:28:57.339071+00	31	6	3
32	2019-10-17 13:28:57.339094+00	2019-10-17 13:28:57.339101+00	32	6	3
33	2019-10-17 13:28:57.339123+00	2019-10-17 13:28:57.339131+00	33	6	3
34	2019-10-17 13:28:57.339153+00	2019-10-17 13:28:57.33916+00	34	6	3
35	2019-10-17 13:28:57.339182+00	2019-10-17 13:28:57.33919+00	35	6	3
36	2019-10-17 13:28:57.339212+00	2019-10-17 13:28:57.339219+00	36	6	3
37	2019-10-17 13:28:57.339242+00	2019-10-17 13:28:57.33925+00	37	6	3
38	2019-10-17 13:28:57.339296+00	2019-10-17 13:28:57.339304+00	38	6	3
39	2019-10-17 13:28:57.339327+00	2019-10-17 13:28:57.339334+00	39	6	3
40	2019-10-17 13:28:57.339357+00	2019-10-17 13:28:57.339364+00	40	6	3
41	2019-10-17 13:28:57.339387+00	2019-10-17 13:28:57.339394+00	41	6	3
42	2019-10-17 13:28:57.339416+00	2019-10-17 13:28:57.339423+00	42	6	3
43	2019-10-17 13:28:57.339446+00	2019-10-17 13:28:57.339453+00	43	6	3
44	2019-10-17 13:28:57.339475+00	2019-10-17 13:28:57.339483+00	44	6	3
45	2019-10-17 13:28:57.339505+00	2019-10-17 13:28:57.339512+00	45	6	3
46	2019-10-17 13:28:57.360757+00	2019-10-17 13:28:57.360781+00	1	7	3
47	2019-10-17 13:28:57.360822+00	2019-10-17 13:28:57.360832+00	2	7	3
48	2019-10-17 13:28:57.360856+00	2019-10-17 13:28:57.360864+00	3	7	3
49	2019-10-17 13:28:57.360887+00	2019-10-17 13:28:57.360894+00	4	7	3
50	2019-10-17 13:28:57.360917+00	2019-10-17 13:28:57.360925+00	5	7	3
51	2019-10-17 13:28:57.360948+00	2019-10-17 13:28:57.360956+00	6	7	3
52	2019-10-17 13:28:57.360978+00	2019-10-17 13:28:57.360986+00	7	7	3
53	2019-10-17 13:28:57.361009+00	2019-10-17 13:28:57.361016+00	8	7	3
54	2019-10-17 13:28:57.361038+00	2019-10-17 13:28:57.361046+00	9	7	3
55	2019-10-17 13:28:57.361069+00	2019-10-17 13:28:57.361086+00	10	7	3
56	2019-10-17 13:28:57.361112+00	2019-10-17 13:28:57.361121+00	11	7	3
57	2019-10-17 13:28:57.361143+00	2019-10-17 13:28:57.361151+00	12	7	3
58	2019-10-17 13:28:57.361173+00	2019-10-17 13:28:57.361181+00	13	7	3
59	2019-10-17 13:28:57.361203+00	2019-10-17 13:28:57.36121+00	14	7	3
60	2019-10-17 13:28:57.361233+00	2019-10-17 13:28:57.36124+00	15	7	3
61	2019-10-17 13:28:57.361262+00	2019-10-17 13:28:57.36127+00	16	7	3
62	2019-10-17 13:28:57.361292+00	2019-10-17 13:28:57.361299+00	17	7	3
63	2019-10-17 13:28:57.36133+00	2019-10-17 13:28:57.361338+00	18	7	3
64	2019-10-17 13:28:57.361362+00	2019-10-17 13:28:57.361373+00	19	7	3
65	2019-10-17 13:28:57.361396+00	2019-10-17 13:28:57.361404+00	20	7	3
66	2019-10-17 13:28:57.361426+00	2019-10-17 13:28:57.361433+00	21	7	3
67	2019-10-17 13:28:57.361455+00	2019-10-17 13:28:57.361462+00	22	7	3
68	2019-10-17 13:28:57.361485+00	2019-10-17 13:28:57.361492+00	23	7	3
69	2019-10-17 13:28:57.361514+00	2019-10-17 13:28:57.361522+00	24	7	3
70	2019-10-17 13:28:57.361544+00	2019-10-17 13:28:57.361551+00	25	7	3
71	2019-10-17 13:28:57.361574+00	2019-10-17 13:28:57.361581+00	26	7	3
72	2019-10-17 13:28:57.361603+00	2019-10-17 13:28:57.361611+00	27	7	3
73	2019-10-17 13:28:57.361633+00	2019-10-17 13:28:57.36164+00	28	7	3
74	2019-10-17 13:28:57.361662+00	2019-10-17 13:28:57.36167+00	29	7	3
75	2019-10-17 13:28:57.361692+00	2019-10-17 13:28:57.3617+00	30	7	3
76	2019-10-17 13:28:57.361722+00	2019-10-17 13:28:57.361729+00	31	7	3
77	2019-10-17 13:28:57.361751+00	2019-10-17 13:28:57.361759+00	32	7	3
78	2019-10-17 13:28:57.361781+00	2019-10-17 13:28:57.361789+00	33	7	3
79	2019-10-17 13:28:57.361811+00	2019-10-17 13:28:57.361826+00	34	7	3
80	2019-10-17 13:28:57.361857+00	2019-10-17 13:28:57.361865+00	35	7	3
81	2019-10-17 13:28:57.361887+00	2019-10-17 13:28:57.361894+00	36	7	3
82	2019-10-17 13:28:57.361917+00	2019-10-17 13:28:57.361924+00	37	7	3
83	2019-10-17 13:28:57.361946+00	2019-10-17 13:28:57.361954+00	38	7	3
84	2019-10-17 13:28:57.361976+00	2019-10-17 13:28:57.361983+00	39	7	3
85	2019-10-17 13:28:57.362006+00	2019-10-17 13:28:57.362013+00	40	7	3
86	2019-10-17 13:28:57.362035+00	2019-10-17 13:28:57.362042+00	41	7	3
87	2019-10-17 13:28:57.362064+00	2019-10-17 13:28:57.362072+00	42	7	3
88	2019-10-17 13:28:57.362094+00	2019-10-17 13:28:57.362101+00	43	7	3
89	2019-10-17 13:28:57.362123+00	2019-10-17 13:28:57.36213+00	44	7	3
90	2019-10-17 13:28:57.362152+00	2019-10-17 13:28:57.36216+00	45	7	3
91	2019-10-17 13:28:57.376037+00	2019-10-17 13:28:57.376056+00	1	8	3
92	2019-10-17 13:28:57.376094+00	2019-10-17 13:28:57.376103+00	2	8	3
93	2019-10-17 13:28:57.376127+00	2019-10-17 13:28:57.376135+00	3	8	3
94	2019-10-17 13:28:57.376158+00	2019-10-17 13:28:57.376166+00	4	8	3
95	2019-10-17 13:28:57.37619+00	2019-10-17 13:28:57.376198+00	5	8	3
96	2019-10-17 13:28:57.376231+00	2019-10-17 13:28:57.37624+00	6	8	3
97	2019-10-17 13:28:57.376263+00	2019-10-17 13:28:57.376271+00	7	8	3
98	2019-10-17 13:28:57.376293+00	2019-10-17 13:28:57.376311+00	8	8	3
99	2019-10-17 13:28:57.376336+00	2019-10-17 13:28:57.376343+00	9	8	3
100	2019-10-17 13:28:57.376366+00	2019-10-17 13:28:57.376374+00	10	8	3
101	2019-10-17 13:28:57.376396+00	2019-10-17 13:28:57.376404+00	11	8	3
102	2019-10-17 13:28:57.376426+00	2019-10-17 13:28:57.376434+00	12	8	3
103	2019-10-17 13:28:57.376456+00	2019-10-17 13:28:57.376464+00	13	8	3
104	2019-10-17 13:28:57.376486+00	2019-10-17 13:28:57.376493+00	14	8	3
105	2019-10-17 13:28:57.376516+00	2019-10-17 13:28:57.376523+00	15	8	3
106	2019-10-17 13:28:57.376545+00	2019-10-17 13:28:57.376553+00	16	8	3
107	2019-10-17 13:28:57.376575+00	2019-10-17 13:28:57.376582+00	17	8	3
108	2019-10-17 13:28:57.376605+00	2019-10-17 13:28:57.376612+00	18	8	3
109	2019-10-17 13:28:57.376634+00	2019-10-17 13:28:57.376641+00	19	8	3
110	2019-10-17 13:28:57.376664+00	2019-10-17 13:28:57.376671+00	20	8	3
111	2019-10-17 13:28:57.376693+00	2019-10-17 13:28:57.3767+00	21	8	3
112	2019-10-17 13:28:57.376722+00	2019-10-17 13:28:57.37673+00	22	8	3
113	2019-10-17 13:28:57.376752+00	2019-10-17 13:28:57.376759+00	23	8	3
114	2019-10-17 13:28:57.376781+00	2019-10-17 13:28:57.376789+00	24	8	3
115	2019-10-17 13:28:57.376811+00	2019-10-17 13:28:57.376818+00	25	8	3
116	2019-10-17 13:28:57.37684+00	2019-10-17 13:28:57.376847+00	26	8	3
117	2019-10-17 13:28:57.37687+00	2019-10-17 13:28:57.376877+00	27	8	3
118	2019-10-17 13:28:57.376899+00	2019-10-17 13:28:57.376915+00	28	8	3
119	2019-10-17 13:28:57.37694+00	2019-10-17 13:28:57.376948+00	29	8	3
120	2019-10-17 13:28:57.376978+00	2019-10-17 13:28:57.376986+00	30	8	3
121	2019-10-17 13:28:57.377009+00	2019-10-17 13:28:57.377016+00	31	8	3
122	2019-10-17 13:28:57.377039+00	2019-10-17 13:28:57.377046+00	32	8	3
123	2019-10-17 13:28:57.377068+00	2019-10-17 13:28:57.377076+00	33	8	3
124	2019-10-17 13:28:57.377098+00	2019-10-17 13:28:57.377105+00	34	8	3
125	2019-10-17 13:28:57.377127+00	2019-10-17 13:28:57.377134+00	35	8	3
126	2019-10-17 13:28:57.377156+00	2019-10-17 13:28:57.377164+00	36	8	3
127	2019-10-17 13:28:57.377186+00	2019-10-17 13:28:57.377193+00	37	8	3
128	2019-10-17 13:28:57.377215+00	2019-10-17 13:28:57.377222+00	38	8	3
129	2019-10-17 13:28:57.377245+00	2019-10-17 13:28:57.377252+00	39	8	3
130	2019-10-17 13:28:57.377274+00	2019-10-17 13:28:57.377281+00	40	8	3
131	2019-10-17 13:28:57.377303+00	2019-10-17 13:28:57.37731+00	41	8	3
132	2019-10-17 13:28:57.377332+00	2019-10-17 13:28:57.37734+00	42	8	3
133	2019-10-17 13:28:57.377362+00	2019-10-17 13:28:57.377369+00	43	8	3
134	2019-10-17 13:28:57.377391+00	2019-10-17 13:28:57.377398+00	44	8	3
135	2019-10-17 13:28:57.37742+00	2019-10-17 13:28:57.377428+00	45	8	3
136	2019-10-17 13:28:57.396183+00	2019-10-17 13:28:57.396203+00	1	9	3
137	2019-10-17 13:28:57.396254+00	2019-10-17 13:28:57.396265+00	2	9	3
138	2019-10-17 13:28:57.396292+00	2019-10-17 13:28:57.39636+00	3	9	3
139	2019-10-17 13:28:57.396388+00	2019-10-17 13:28:57.396396+00	4	9	3
140	2019-10-17 13:28:57.396419+00	2019-10-17 13:28:57.396427+00	5	9	3
141	2019-10-17 13:28:57.39645+00	2019-10-17 13:28:57.396458+00	6	9	3
142	2019-10-17 13:28:57.396481+00	2019-10-17 13:28:57.396488+00	7	9	3
143	2019-10-17 13:28:57.396511+00	2019-10-17 13:28:57.396519+00	8	9	3
144	2019-10-17 13:28:57.396542+00	2019-10-17 13:28:57.39655+00	9	9	3
145	2019-10-17 13:28:57.396573+00	2019-10-17 13:28:57.396581+00	10	9	3
146	2019-10-17 13:28:57.396605+00	2019-10-17 13:28:57.396612+00	11	9	3
147	2019-10-17 13:28:57.396635+00	2019-10-17 13:28:57.396642+00	12	9	3
148	2019-10-17 13:28:57.396665+00	2019-10-17 13:28:57.396673+00	13	9	3
149	2019-10-17 13:28:57.396695+00	2019-10-17 13:28:57.396703+00	14	9	3
150	2019-10-17 13:28:57.396726+00	2019-10-17 13:28:57.396733+00	15	9	3
151	2019-10-17 13:28:57.396755+00	2019-10-17 13:28:57.396763+00	16	9	3
152	2019-10-17 13:28:57.396786+00	2019-10-17 13:28:57.396793+00	17	9	3
153	2019-10-17 13:28:57.396816+00	2019-10-17 13:28:57.396823+00	18	9	3
154	2019-10-17 13:28:57.396845+00	2019-10-17 13:28:57.396853+00	19	9	3
155	2019-10-17 13:28:57.396875+00	2019-10-17 13:28:57.396883+00	20	9	3
156	2019-10-17 13:28:57.396905+00	2019-10-17 13:28:57.396913+00	21	9	3
157	2019-10-17 13:28:57.396935+00	2019-10-17 13:28:57.396952+00	22	9	3
158	2019-10-17 13:28:57.396977+00	2019-10-17 13:28:57.396985+00	23	9	3
159	2019-10-17 13:28:57.397007+00	2019-10-17 13:28:57.397015+00	24	9	3
160	2019-10-17 13:28:57.397045+00	2019-10-17 13:28:57.397053+00	25	9	3
161	2019-10-17 13:28:57.397077+00	2019-10-17 13:28:57.397085+00	26	9	3
162	2019-10-17 13:28:57.397107+00	2019-10-17 13:28:57.397115+00	27	9	3
163	2019-10-17 13:28:57.397137+00	2019-10-17 13:28:57.397145+00	28	9	3
164	2019-10-17 13:28:57.397167+00	2019-10-17 13:28:57.397175+00	29	9	3
165	2019-10-17 13:28:57.397197+00	2019-10-17 13:28:57.397205+00	30	9	3
166	2019-10-17 13:28:57.397227+00	2019-10-17 13:28:57.397235+00	31	9	3
167	2019-10-17 13:28:57.397257+00	2019-10-17 13:28:57.397265+00	32	9	3
168	2019-10-17 13:28:57.397287+00	2019-10-17 13:28:57.397295+00	33	9	3
169	2019-10-17 13:28:57.397317+00	2019-10-17 13:28:57.397325+00	34	9	3
170	2019-10-17 13:28:57.397347+00	2019-10-17 13:28:57.397354+00	35	9	3
171	2019-10-17 13:28:57.397377+00	2019-10-17 13:28:57.397384+00	36	9	3
172	2019-10-17 13:28:57.397407+00	2019-10-17 13:28:57.397414+00	37	9	3
173	2019-10-17 13:28:57.397437+00	2019-10-17 13:28:57.397444+00	38	9	3
174	2019-10-17 13:28:57.397467+00	2019-10-17 13:28:57.397474+00	39	9	3
175	2019-10-17 13:28:57.397497+00	2019-10-17 13:28:57.397504+00	40	9	3
176	2019-10-17 13:28:57.397527+00	2019-10-17 13:28:57.397534+00	41	9	3
177	2019-10-17 13:28:57.397556+00	2019-10-17 13:28:57.397564+00	42	9	3
178	2019-10-17 13:28:57.397586+00	2019-10-17 13:28:57.397594+00	43	9	3
179	2019-10-17 13:28:57.397616+00	2019-10-17 13:28:57.397624+00	44	9	3
180	2019-10-17 13:28:57.397646+00	2019-10-17 13:28:57.397653+00	45	9	3
181	2019-10-17 13:28:57.413715+00	2019-10-17 13:28:57.413733+00	1	10	3
182	2019-10-17 13:28:57.413771+00	2019-10-17 13:28:57.413779+00	2	10	3
183	2019-10-17 13:28:57.413816+00	2019-10-17 13:28:57.413825+00	3	10	3
184	2019-10-17 13:28:57.413849+00	2019-10-17 13:28:57.413856+00	4	10	3
185	2019-10-17 13:28:57.413878+00	2019-10-17 13:28:57.413886+00	5	10	3
186	2019-10-17 13:28:57.413909+00	2019-10-17 13:28:57.413916+00	6	10	3
187	2019-10-17 13:28:57.413938+00	2019-10-17 13:28:57.413946+00	7	10	3
188	2019-10-17 13:28:57.413968+00	2019-10-17 13:28:57.413975+00	8	10	3
189	2019-10-17 13:28:57.414009+00	2019-10-17 13:28:57.414016+00	9	10	3
190	2019-10-17 13:28:57.414039+00	2019-10-17 13:28:57.414046+00	10	10	3
191	2019-10-17 13:28:57.414069+00	2019-10-17 13:28:57.414076+00	11	10	3
192	2019-10-17 13:28:57.414099+00	2019-10-17 13:28:57.414106+00	12	10	3
193	2019-10-17 13:28:57.414128+00	2019-10-17 13:28:57.414136+00	13	10	3
194	2019-10-17 13:28:57.414158+00	2019-10-17 13:28:57.414172+00	14	10	3
195	2019-10-17 13:28:57.414198+00	2019-10-17 13:28:57.414206+00	15	10	3
196	2019-10-17 13:28:57.414228+00	2019-10-17 13:28:57.414243+00	16	10	3
197	2019-10-17 13:28:57.414267+00	2019-10-17 13:28:57.414274+00	17	10	3
198	2019-10-17 13:28:57.414296+00	2019-10-17 13:28:57.414303+00	18	10	3
199	2019-10-17 13:28:57.414325+00	2019-10-17 13:28:57.414333+00	19	10	3
200	2019-10-17 13:28:57.414361+00	2019-10-17 13:28:57.414376+00	20	10	3
201	2019-10-17 13:28:57.414403+00	2019-10-17 13:28:57.41441+00	21	10	3
202	2019-10-17 13:28:57.414433+00	2019-10-17 13:28:57.41444+00	22	10	3
203	2019-10-17 13:28:57.414462+00	2019-10-17 13:28:57.414469+00	23	10	3
204	2019-10-17 13:28:57.414491+00	2019-10-17 13:28:57.414498+00	24	10	3
205	2019-10-17 13:28:57.414521+00	2019-10-17 13:28:57.414528+00	25	10	3
206	2019-10-17 13:28:57.41456+00	2019-10-17 13:28:57.414569+00	26	10	3
207	2019-10-17 13:28:57.414592+00	2019-10-17 13:28:57.414599+00	27	10	3
208	2019-10-17 13:28:57.414621+00	2019-10-17 13:28:57.414628+00	28	10	3
209	2019-10-17 13:28:57.41465+00	2019-10-17 13:28:57.414657+00	29	10	3
210	2019-10-17 13:28:57.414679+00	2019-10-17 13:28:57.414687+00	30	10	3
211	2019-10-17 13:28:57.414709+00	2019-10-17 13:28:57.414716+00	31	10	3
212	2019-10-17 13:28:57.414747+00	2019-10-17 13:28:57.414756+00	32	10	3
213	2019-10-17 13:28:57.414779+00	2019-10-17 13:28:57.414786+00	33	10	3
214	2019-10-17 13:28:57.414808+00	2019-10-17 13:28:57.414816+00	34	10	3
215	2019-10-17 13:28:57.414838+00	2019-10-17 13:28:57.414845+00	35	10	3
216	2019-10-17 13:28:57.414867+00	2019-10-17 13:28:57.414874+00	36	10	3
217	2019-10-17 13:28:57.414896+00	2019-10-17 13:28:57.414904+00	37	10	3
218	2019-10-17 13:28:57.414933+00	2019-10-17 13:28:57.414942+00	38	10	3
219	2019-10-17 13:28:57.414966+00	2019-10-17 13:28:57.414974+00	39	10	3
220	2019-10-17 13:28:57.414996+00	2019-10-17 13:28:57.415003+00	40	10	3
221	2019-10-17 13:28:57.415025+00	2019-10-17 13:28:57.415033+00	41	10	3
222	2019-10-17 13:28:57.415055+00	2019-10-17 13:28:57.415062+00	42	10	3
223	2019-10-17 13:28:57.415084+00	2019-10-17 13:28:57.415091+00	43	10	3
224	2019-10-17 13:28:57.41512+00	2019-10-17 13:28:57.415135+00	44	10	3
225	2019-10-17 13:28:57.41516+00	2019-10-17 13:28:57.415167+00	45	10	3
226	2019-10-17 13:28:57.433485+00	2019-10-17 13:28:57.43352+00	1	11	3
227	2019-10-17 13:28:57.43356+00	2019-10-17 13:28:57.433569+00	2	11	3
228	2019-10-17 13:28:57.433594+00	2019-10-17 13:28:57.433601+00	3	11	3
229	2019-10-17 13:28:57.433624+00	2019-10-17 13:28:57.433632+00	4	11	3
230	2019-10-17 13:28:57.433654+00	2019-10-17 13:28:57.433662+00	5	11	3
231	2019-10-17 13:28:57.433695+00	2019-10-17 13:28:57.433704+00	6	11	3
232	2019-10-17 13:28:57.433727+00	2019-10-17 13:28:57.433735+00	7	11	3
233	2019-10-17 13:28:57.433757+00	2019-10-17 13:28:57.433765+00	8	11	3
234	2019-10-17 13:28:57.433787+00	2019-10-17 13:28:57.433795+00	9	11	3
235	2019-10-17 13:28:57.433818+00	2019-10-17 13:28:57.433832+00	10	11	3
236	2019-10-17 13:28:57.433858+00	2019-10-17 13:28:57.433866+00	11	11	3
237	2019-10-17 13:28:57.433896+00	2019-10-17 13:28:57.433905+00	12	11	3
238	2019-10-17 13:28:57.43393+00	2019-10-17 13:28:57.433937+00	13	11	3
239	2019-10-17 13:28:57.43396+00	2019-10-17 13:28:57.433967+00	14	11	3
240	2019-10-17 13:28:57.43399+00	2019-10-17 13:28:57.433997+00	15	11	3
241	2019-10-17 13:28:57.434021+00	2019-10-17 13:28:57.434035+00	16	11	3
242	2019-10-17 13:28:57.434061+00	2019-10-17 13:28:57.434068+00	17	11	3
243	2019-10-17 13:28:57.43409+00	2019-10-17 13:28:57.434098+00	18	11	3
244	2019-10-17 13:28:57.43412+00	2019-10-17 13:28:57.434127+00	19	11	3
245	2019-10-17 13:28:57.434149+00	2019-10-17 13:28:57.434156+00	20	11	3
246	2019-10-17 13:28:57.434178+00	2019-10-17 13:28:57.434186+00	21	11	3
247	2019-10-17 13:28:57.434208+00	2019-10-17 13:28:57.434215+00	22	11	3
248	2019-10-17 13:28:57.434237+00	2019-10-17 13:28:57.434244+00	23	11	3
249	2019-10-17 13:28:57.434267+00	2019-10-17 13:28:57.434274+00	24	11	3
250	2019-10-17 13:28:57.434296+00	2019-10-17 13:28:57.434303+00	25	11	3
251	2019-10-17 13:28:57.434326+00	2019-10-17 13:28:57.434333+00	26	11	3
252	2019-10-17 13:28:57.434355+00	2019-10-17 13:28:57.434363+00	27	11	3
253	2019-10-17 13:28:57.434385+00	2019-10-17 13:28:57.434392+00	28	11	3
254	2019-10-17 13:28:57.434414+00	2019-10-17 13:28:57.434422+00	29	11	3
255	2019-10-17 13:28:57.434444+00	2019-10-17 13:28:57.434451+00	30	11	3
256	2019-10-17 13:28:57.434473+00	2019-10-17 13:28:57.434488+00	31	11	3
257	2019-10-17 13:28:57.434515+00	2019-10-17 13:28:57.434522+00	32	11	3
258	2019-10-17 13:28:57.434545+00	2019-10-17 13:28:57.434552+00	33	11	3
259	2019-10-17 13:28:57.434574+00	2019-10-17 13:28:57.434581+00	34	11	3
260	2019-10-17 13:28:57.434604+00	2019-10-17 13:28:57.434611+00	35	11	3
261	2019-10-17 13:28:57.434633+00	2019-10-17 13:28:57.43464+00	36	11	3
262	2019-10-17 13:28:57.434663+00	2019-10-17 13:28:57.43467+00	37	11	3
263	2019-10-17 13:28:57.434692+00	2019-10-17 13:28:57.4347+00	38	11	3
264	2019-10-17 13:28:57.434732+00	2019-10-17 13:28:57.434741+00	39	11	3
265	2019-10-17 13:28:57.434764+00	2019-10-17 13:28:57.434778+00	40	11	3
266	2019-10-17 13:28:57.434802+00	2019-10-17 13:28:57.43481+00	41	11	3
267	2019-10-17 13:28:57.434832+00	2019-10-17 13:28:57.434839+00	42	11	3
268	2019-10-17 13:28:57.434861+00	2019-10-17 13:28:57.434868+00	43	11	3
269	2019-10-17 13:28:57.434891+00	2019-10-17 13:28:57.434898+00	44	11	3
270	2019-10-17 13:28:57.43492+00	2019-10-17 13:28:57.434927+00	45	11	3
\.


--
-- Data for Name: locations_sowgroupcell; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY locations_sowgroupcell (id, created_at, modified_at, number, sows_quantity, section_id, workshop_id) FROM stdin;
1	2019-10-17 13:28:57.296189+00	2019-10-17 13:28:57.296208+00	1	0	4	2
2	2019-10-17 13:28:57.29625+00	2019-10-17 13:28:57.296259+00	2	0	4	2
3	2019-10-17 13:28:57.296286+00	2019-10-17 13:28:57.29637+00	3	0	4	2
4	2019-10-17 13:28:57.296406+00	2019-10-17 13:28:57.296414+00	4	0	4	2
5	2019-10-17 13:28:57.296439+00	2019-10-17 13:28:57.296447+00	5	0	4	2
6	2019-10-17 13:28:57.296472+00	2019-10-17 13:28:57.296492+00	6	0	4	2
7	2019-10-17 13:28:57.311862+00	2019-10-17 13:28:57.311893+00	1	0	5	2
8	2019-10-17 13:28:57.311947+00	2019-10-17 13:28:57.311957+00	2	0	5	2
9	2019-10-17 13:28:57.311984+00	2019-10-17 13:28:57.311992+00	3	0	5	2
10	2019-10-17 13:28:57.312024+00	2019-10-17 13:28:57.312032+00	4	0	5	2
11	2019-10-17 13:28:57.312058+00	2019-10-17 13:28:57.312065+00	5	0	5	2
12	2019-10-17 13:28:57.31209+00	2019-10-17 13:28:57.312098+00	6	0	5	2
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
1	2019-10-17 13:28:57.26252+00	2019-10-17 13:28:57.26256+00	1	Цех 1 Осеменение
2	2019-10-17 13:28:57.262584+00	2019-10-17 13:28:57.262592+00	2	Цех 2 Ожидание родов
3	2019-10-17 13:28:57.262605+00	2019-10-17 13:28:57.262612+00	3	Цех 3 Маточник
4	2019-10-17 13:28:57.262633+00	2019-10-17 13:28:57.26264+00	4	Цех 4 Доращивание 4
5	2019-10-17 13:28:57.262653+00	2019-10-17 13:28:57.26266+00	8	Цех 8 Доращивание 8
6	2019-10-17 13:28:57.262672+00	2019-10-17 13:28:57.262686+00	5	Цех 5 Откорм 5
7	2019-10-17 13:28:57.262707+00	2019-10-17 13:28:57.262714+00	6	Цех 6 Откорм 6
8	2019-10-17 13:28:57.262727+00	2019-10-17 13:28:57.262733+00	7	Цех 7 Откорм 7
9	2019-10-17 13:28:57.262746+00	2019-10-17 13:28:57.262753+00	9	Цех 9 Убойный цех
10	2019-10-17 13:28:57.262765+00	2019-10-17 13:28:57.262772+00	10	Цех 10 Крематорий
\.


--
-- Data for Name: piglets_events_cullingnewbornpiglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_cullingnewbornpiglets (id, created_at, modified_at, date, culling_type, quantity, reason, is_it_gilt, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_cullingnomadpiglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_cullingnomadpiglets (id, created_at, modified_at, date, culling_type, quantity, reason, is_it_gilt, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_newbornmergerrecord; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_newbornmergerrecord (id, created_at, modified_at, quantity, percentage, merger_id, tour_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_newbornpigletsgrouprecount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_newbornpigletsgrouprecount (id, created_at, modified_at, date, quantity_before, quantity_after, balance, initiator_id, piglets_group_id) FROM stdin;
1	2019-11-04 09:00:52.402016+00	2019-11-04 09:00:52.402035+00	2019-11-04 09:00:52.401626+00	32	16	-16	4	2
2	2019-11-04 09:01:15.400154+00	2019-11-04 09:01:15.400171+00	2019-11-04 09:01:15.399907+00	24	12	-12	4	1
3	2019-11-04 09:01:39.237475+00	2019-11-04 09:01:39.237493+00	2019-11-04 09:01:39.237123+00	30	15	-15	4	4
4	2019-11-04 09:01:51.749841+00	2019-11-04 09:01:51.749868+00	2019-11-04 09:01:51.749454+00	24	12	-12	4	5
5	2019-11-04 09:03:59.826605+00	2019-11-04 09:03:59.826623+00	2019-11-04 09:03:59.826318+00	24	12	-12	4	6
6	2019-11-04 09:04:12.853904+00	2019-11-04 09:04:12.853932+00	2019-11-04 09:04:12.853455+00	22	11	-11	4	7
7	2019-11-04 09:04:32.480892+00	2019-11-04 09:04:32.480911+00	2019-11-04 09:04:32.480621+00	30	15	-15	4	8
\.


--
-- Data for Name: piglets_events_newbornpigletsmerger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_newbornpigletsmerger (id, created_at, modified_at, date, part_number, initiator_id, nomad_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_nomadmergerrecord; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_nomadmergerrecord (id, created_at, modified_at, quantity, percentage, merger_id, nomad_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_nomadpigletsgroupmerger; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_nomadpigletsgroupmerger (id, created_at, modified_at, date, initiator_id, new_location_id, nomad_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_nomadpigletsgrouprecount; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_nomadpigletsgrouprecount (id, created_at, modified_at, date, quantity_before, quantity_after, balance, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_splitnomadpigletsgroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_splitnomadpigletsgroup (id, created_at, modified_at, date, initiator_id, parent_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_events_weighingpiglets; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_events_weighingpiglets (id, created_at, modified_at, date, total_weight, average_weight, piglets_quantity, place, initiator_id, piglets_group_id) FROM stdin;
\.


--
-- Data for Name: piglets_newbornpigletsgroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_newbornpigletsgroup (id, created_at, modified_at, start_quantity, quantity, active, transfer_label, gilts_quantity, size_label, location_id, merger_id, status_id, tour_id) FROM stdin;
12	2019-10-29 08:14:38.149579+00	2019-10-29 08:14:38.149604+00	13	13	t	f	0	\N	169	\N	\N	2
13	2019-10-29 08:16:17.36444+00	2019-10-29 08:16:17.364462+00	3	3	t	f	0	\N	170	\N	\N	2
14	2019-10-29 08:16:56.723488+00	2019-10-29 08:17:14.223869+00	12	13	t	f	0	\N	171	\N	\N	2
15	2019-10-29 08:18:07.198938+00	2019-10-29 08:18:07.198961+00	12	12	t	f	0	\N	172	\N	\N	2
16	2019-10-29 08:18:35.131464+00	2019-10-29 08:18:35.131485+00	16	16	t	f	0	\N	173	\N	\N	2
17	2019-10-29 08:19:42.471028+00	2019-10-29 08:19:42.471178+00	12	12	t	f	0	\N	174	\N	\N	2
18	2019-10-29 08:19:57.382379+00	2019-10-29 08:19:57.382406+00	17	17	t	f	0	\N	175	\N	\N	2
19	2019-10-29 08:20:16.513052+00	2019-10-29 08:20:16.513079+00	10	10	t	f	0	\N	176	\N	\N	2
20	2019-10-29 08:20:35.765884+00	2019-10-29 08:20:35.765923+00	13	13	t	f	0	\N	177	\N	\N	2
21	2019-10-29 08:21:15.424224+00	2019-10-29 08:21:15.424247+00	10	10	t	f	0	\N	186	\N	\N	2
22	2019-10-29 08:21:48.663456+00	2019-10-29 08:21:48.663476+00	15	15	t	f	0	\N	185	\N	\N	2
23	2019-10-29 08:22:20.623333+00	2019-10-29 08:22:20.623363+00	12	12	t	f	0	\N	184	\N	\N	2
24	2019-10-29 08:22:33.072821+00	2019-10-29 08:22:33.072845+00	9	9	t	f	0	\N	183	\N	\N	2
25	2019-10-29 08:22:44.98207+00	2019-10-29 08:22:44.982091+00	12	12	t	f	0	\N	182	\N	\N	2
26	2019-10-29 08:23:06.645011+00	2019-10-29 08:23:06.645033+00	12	12	t	f	0	\N	181	\N	\N	2
27	2019-10-29 08:23:24.239607+00	2019-10-29 08:23:24.239635+00	7	7	t	f	0	\N	180	\N	\N	2
28	2019-10-29 08:24:01.548686+00	2019-10-29 08:24:01.548722+00	9	9	t	f	0	\N	179	\N	\N	2
29	2019-10-29 08:24:19.128992+00	2019-10-29 08:24:19.129014+00	12	12	t	f	0	\N	178	\N	\N	2
85	2019-11-04 09:01:31.722319+00	2019-11-04 09:01:31.722343+00	7	7	t	f	0	\N	250	\N	\N	2
73	2019-11-04 08:57:22.740667+00	2019-11-04 08:57:22.74069+00	16	16	t	f	0	\N	238	\N	\N	2
4	2019-10-29 07:31:06.197941+00	2019-11-04 09:01:39.266476+00	15	15	t	f	0	\N	190	\N	\N	2
30	2019-10-29 08:25:41.166885+00	2019-10-29 08:25:41.166907+00	15	15	t	f	0	\N	189	\N	\N	1
86	2019-11-04 09:02:14.840478+00	2019-11-04 09:02:14.840497+00	6	6	t	f	0	\N	252	\N	\N	2
87	2019-11-04 09:02:27.335011+00	2019-11-04 09:02:27.335036+00	12	12	t	f	0	\N	253	\N	\N	2
7	2019-10-29 07:32:27.030677+00	2019-11-04 09:04:12.856914+00	11	11	t	f	0	\N	194	\N	\N	2
93	2019-11-04 09:04:18.138956+00	2019-11-04 09:04:18.138983+00	11	11	t	f	0	\N	260	\N	\N	2
31	2019-10-29 08:28:21.085415+00	2019-10-29 08:28:21.08544+00	12	12	t	f	0	\N	195	\N	\N	2
94	2019-11-04 09:04:34.398426+00	2019-11-04 09:04:34.398447+00	12	12	t	f	0	\N	261	\N	\N	2
96	2019-11-04 09:05:02.959393+00	2019-11-04 09:05:02.959416+00	13	13	t	f	0	\N	263	\N	\N	2
74	2019-11-04 08:57:51.063886+00	2019-11-04 08:57:51.063903+00	9	9	t	f	0	\N	239	\N	\N	2
10	2019-10-29 07:33:46.521293+00	2019-10-29 08:30:27.581945+00	12	12	t	f	0	\N	199	\N	\N	2
3	2019-10-29 07:30:28.718782+00	2019-11-04 09:05:54.591974+00	12	12	t	f	0	\N	201	\N	\N	2
32	2019-10-29 08:31:36.731347+00	2019-11-04 09:06:30.795564+00	15	17	t	f	0	\N	202	\N	\N	2
34	2019-10-29 08:32:57.217344+00	2019-10-29 08:32:57.217367+00	9	9	t	f	0	\N	167	\N	\N	2
35	2019-10-29 08:34:12.31715+00	2019-10-29 08:34:12.317172+00	11	11	t	f	0	\N	166	\N	\N	2
36	2019-10-29 08:37:33.834727+00	2019-10-29 08:37:33.834748+00	10	10	t	f	0	\N	165	\N	\N	2
37	2019-10-29 08:37:54.005193+00	2019-10-29 08:37:54.005214+00	11	11	t	f	0	\N	164	\N	\N	2
38	2019-10-29 08:38:11.853054+00	2019-10-29 08:38:11.853071+00	11	11	t	f	0	\N	163	\N	\N	2
39	2019-10-29 08:38:40.430181+00	2019-10-29 08:38:40.430202+00	15	15	t	f	0	\N	162	\N	\N	2
40	2019-10-29 08:39:01.045088+00	2019-10-29 08:39:01.045142+00	9	9	t	f	0	\N	161	\N	\N	2
41	2019-10-29 08:39:26.284836+00	2019-10-29 08:39:26.284857+00	8	8	t	f	0	\N	160	\N	\N	2
42	2019-10-29 08:39:44.192767+00	2019-10-29 08:39:44.192786+00	14	14	t	f	0	\N	159	\N	\N	2
43	2019-10-29 08:39:58.344676+00	2019-10-29 08:40:09.930169+00	0	12	t	f	0	\N	158	\N	\N	2
44	2019-10-29 08:40:31.050741+00	2019-10-29 08:40:31.050778+00	15	15	t	f	0	\N	157	\N	\N	2
45	2019-10-29 08:40:44.732962+00	2019-10-29 08:40:44.732991+00	15	15	t	f	0	\N	156	\N	\N	2
46	2019-10-29 08:40:54.126041+00	2019-10-29 08:40:54.126064+00	11	11	t	f	0	\N	155	\N	\N	2
47	2019-10-29 08:41:07.409021+00	2019-10-29 08:41:07.409042+00	8	8	t	f	0	\N	154	\N	\N	2
48	2019-10-29 08:41:22.654471+00	2019-10-29 08:41:22.654493+00	8	8	t	f	0	\N	153	\N	\N	2
49	2019-10-29 08:41:36.776195+00	2019-10-29 08:41:36.776213+00	14	14	t	f	0	\N	152	\N	\N	2
50	2019-11-04 08:46:27.781406+00	2019-11-04 08:46:27.781433+00	12	12	t	f	0	\N	214	\N	\N	2
51	2019-11-04 08:46:39.310248+00	2019-11-04 08:46:39.310267+00	14	14	t	f	0	\N	215	\N	\N	2
52	2019-11-04 08:46:49.764182+00	2019-11-04 08:46:49.764202+00	12	12	t	f	0	\N	216	\N	\N	2
53	2019-11-04 08:47:01.147489+00	2019-11-04 08:47:01.147512+00	12	12	t	f	0	\N	217	\N	\N	2
54	2019-11-04 08:47:14.238909+00	2019-11-04 08:47:14.238928+00	10	10	t	f	0	\N	218	\N	\N	2
56	2019-11-04 08:47:39.661928+00	2019-11-04 08:47:39.661953+00	14	14	t	f	0	\N	220	\N	\N	2
57	2019-11-04 08:47:53.53572+00	2019-11-04 08:47:53.535736+00	9	9	t	f	0	\N	221	\N	\N	2
58	2019-11-04 08:48:10.421918+00	2019-11-04 08:48:10.421939+00	13	13	t	f	0	\N	222	\N	\N	2
59	2019-11-04 08:48:30.618328+00	2019-11-04 08:48:30.618353+00	14	14	t	f	0	\N	223	\N	\N	2
60	2019-11-04 08:52:44.408392+00	2019-11-04 08:52:44.408418+00	16	16	t	f	0	\N	224	\N	\N	2
61	2019-11-04 08:53:03.1578+00	2019-11-04 08:53:03.157826+00	12	12	t	f	0	\N	225	\N	\N	2
62	2019-11-04 08:53:16.468979+00	2019-11-04 08:53:16.468998+00	5	5	t	f	0	\N	226	\N	\N	2
63	2019-11-04 08:53:29.842327+00	2019-11-04 08:53:29.842352+00	13	13	t	f	0	\N	227	\N	\N	2
64	2019-11-04 08:54:21.656689+00	2019-11-04 08:54:21.65671+00	11	11	t	f	0	\N	228	\N	\N	2
55	2019-11-04 08:47:27.208965+00	2019-11-04 08:54:42.709072+00	12	17	t	f	0	\N	219	\N	\N	2
65	2019-11-04 08:54:56.580844+00	2019-11-04 08:54:56.580871+00	11	11	t	f	0	\N	230	\N	\N	2
66	2019-11-04 08:55:12.556059+00	2019-11-04 08:55:12.556081+00	7	7	t	f	0	\N	231	\N	\N	2
67	2019-11-04 08:55:35.523015+00	2019-11-04 08:55:35.523033+00	12	12	t	f	0	\N	232	\N	\N	2
68	2019-11-04 08:55:49.715138+00	2019-11-04 08:55:49.715445+00	14	14	t	f	0	\N	233	\N	\N	2
69	2019-11-04 08:56:07.852293+00	2019-11-04 08:56:07.85231+00	16	16	t	f	0	\N	234	\N	\N	2
70	2019-11-04 08:56:28.030096+00	2019-11-04 08:56:28.030124+00	10	10	t	f	0	\N	235	\N	\N	2
71	2019-11-04 08:56:50.531586+00	2019-11-04 08:56:50.531608+00	13	13	t	f	0	\N	236	\N	\N	2
72	2019-11-04 08:57:06.89947+00	2019-11-04 08:57:06.899492+00	11	11	t	f	0	\N	237	\N	\N	2
75	2019-11-04 08:58:09.72204+00	2019-11-04 08:58:09.722063+00	8	8	t	f	0	\N	240	\N	\N	2
76	2019-11-04 08:58:24.552086+00	2019-11-04 08:58:24.552113+00	9	9	t	f	0	\N	241	\N	\N	2
77	2019-11-04 08:58:36.807376+00	2019-11-04 08:58:36.807398+00	9	9	t	f	0	\N	242	\N	\N	2
78	2019-11-04 08:58:51.559113+00	2019-11-04 08:59:06.441216+00	13	13	t	f	0	\N	243	\N	\N	2
79	2019-11-04 08:59:24.640231+00	2019-11-04 08:59:24.640254+00	16	16	t	f	0	\N	244	\N	\N	2
80	2019-11-04 08:59:43.296748+00	2019-11-04 08:59:43.296768+00	11	11	t	f	0	\N	245	\N	\N	2
81	2019-11-04 09:00:04.929915+00	2019-11-04 09:00:04.931166+00	10	10	t	f	0	\N	246	\N	\N	2
82	2019-11-04 09:00:24.590149+00	2019-11-04 09:00:24.590173+00	8	8	t	f	0	\N	247	\N	\N	2
83	2019-11-04 09:00:41.897163+00	2019-11-04 09:00:41.897183+00	18	18	t	f	0	\N	248	\N	\N	2
2	2019-10-29 07:29:48.86969+00	2019-11-04 09:00:52.40913+00	16	16	t	f	0	\N	187	\N	\N	2
84	2019-11-04 09:00:57.443932+00	2019-11-04 09:00:57.44395+00	5	5	t	f	0	\N	249	\N	\N	2
1	2019-10-29 07:29:08.036217+00	2019-11-04 09:01:15.402276+00	12	12	t	f	0	\N	188	\N	\N	2
5	2019-10-29 07:31:36.874424+00	2019-11-04 09:01:51.753366+00	12	12	t	f	0	\N	191	\N	\N	2
88	2019-11-04 09:02:38.335766+00	2019-11-04 09:02:38.335787+00	5	5	t	f	0	\N	254	\N	\N	2
89	2019-11-04 09:02:42.142726+00	2019-11-04 09:02:42.142752+00	10	10	t	f	0	\N	192	\N	\N	2
90	2019-11-04 09:02:56.422509+00	2019-11-04 09:02:56.42261+00	11	11	t	f	0	\N	256	\N	\N	2
91	2019-11-04 09:03:11.886727+00	2019-11-04 09:03:11.886752+00	3	3	t	f	0	\N	257	\N	\N	4
92	2019-11-04 09:03:59.620896+00	2019-11-04 09:03:59.620918+00	12	12	t	f	0	\N	259	\N	\N	2
6	2019-10-29 07:32:05.310141+00	2019-11-04 09:03:59.829261+00	12	12	t	f	0	\N	193	\N	\N	2
8	2019-10-29 07:32:55.949786+00	2019-11-04 09:04:32.484641+00	15	15	t	f	0	\N	196	\N	\N	2
95	2019-11-04 09:04:45.694006+00	2019-11-04 09:04:45.694028+00	10	10	t	f	0	\N	262	\N	\N	2
9	2019-10-29 07:33:21.074069+00	2019-11-04 09:04:48.958706+00	12	12	t	f	0	\N	197	\N	\N	2
33	2019-10-29 08:32:39.567442+00	2019-11-04 09:09:56.222535+00	12	12	t	f	0	\N	168	\N	\N	2
97	2019-11-04 09:05:18.861123+00	2019-11-04 09:05:18.861203+00	8	8	t	f	0	\N	264	\N	\N	2
98	2019-11-04 09:05:19.773346+00	2019-11-04 09:05:19.77337+00	15	15	t	f	0	\N	198	\N	\N	2
11	2019-10-29 07:34:04.454258+00	2019-11-04 09:05:39.185898+00	10	10	t	f	0	\N	200	\N	\N	2
99	2019-11-04 09:06:21.558809+00	2019-11-04 09:06:21.558833+00	14	14	t	f	0	\N	205	\N	\N	2
100	2019-11-04 09:06:42.644318+00	2019-11-04 09:06:42.644342+00	5	5	t	f	0	\N	206	\N	\N	2
101	2019-11-04 09:06:49.896368+00	2019-11-04 09:06:49.89639+00	11	11	t	f	0	\N	203	\N	\N	2
102	2019-11-04 09:07:00.344215+00	2019-11-04 09:07:00.344236+00	12	12	t	f	0	\N	207	\N	\N	2
103	2019-11-04 09:07:04.524215+00	2019-11-04 09:07:04.52424+00	16	16	t	f	0	\N	204	\N	\N	2
104	2019-11-04 09:07:10.53732+00	2019-11-04 09:07:10.537341+00	11	11	t	f	0	\N	208	\N	\N	2
105	2019-11-04 09:07:22.143857+00	2019-11-04 09:07:22.143884+00	17	17	t	f	0	\N	209	\N	\N	2
106	2019-11-04 09:07:38.21924+00	2019-11-04 09:07:38.219263+00	12	12	t	f	0	\N	210	\N	\N	2
107	2019-11-04 09:07:48.656068+00	2019-11-04 09:07:48.656084+00	13	13	t	f	0	\N	211	\N	\N	2
108	2019-11-04 09:08:01.600314+00	2019-11-04 09:08:01.600395+00	10	10	t	f	0	\N	212	\N	\N	2
109	2019-11-04 09:08:14.062258+00	2019-11-04 09:08:14.062331+00	12	12	t	f	0	\N	213	\N	\N	2
110	2019-11-04 09:11:47.786374+00	2019-11-04 09:11:47.786397+00	14	14	t	f	0	\N	151	\N	\N	2
111	2019-11-04 09:12:26.950657+00	2019-11-04 09:12:26.950673+00	12	12	t	f	0	\N	150	\N	\N	2
112	2019-11-04 09:12:50.608388+00	2019-11-04 09:12:50.608409+00	15	15	t	f	0	\N	149	\N	\N	2
113	2019-11-04 09:12:57.480001+00	2019-11-04 09:12:57.48002+00	15	15	t	f	0	\N	142	\N	\N	2
114	2019-11-04 09:13:13.65607+00	2019-11-04 09:13:13.656089+00	14	14	t	f	0	\N	143	\N	\N	2
115	2019-11-04 09:13:16.078011+00	2019-11-04 09:13:16.078041+00	13	13	t	f	0	\N	148	\N	\N	2
116	2019-11-04 09:13:29.583929+00	2019-11-04 09:13:29.583954+00	15	15	t	f	0	\N	147	\N	\N	2
117	2019-11-04 09:13:31.937827+00	2019-11-04 09:13:31.937846+00	10	10	t	f	0	\N	144	\N	\N	2
118	2019-11-04 09:13:42.861857+00	2019-11-04 09:13:42.861882+00	13	13	t	f	0	\N	146	\N	\N	2
119	2019-11-04 09:13:44.6417+00	2019-11-04 09:13:44.641723+00	6	6	t	f	0	\N	145	\N	\N	2
120	2019-11-04 09:14:13.970234+00	2019-11-04 09:14:13.970249+00	9	9	t	f	0	\N	139	\N	\N	2
\.


--
-- Data for Name: piglets_nomadpigletsgroup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_nomadpigletsgroup (id, created_at, modified_at, start_quantity, quantity, active, transfer_label, gilts_quantity, groups_merger_id, location_id, split_record_id, status_id) FROM stdin;
\.


--
-- Data for Name: piglets_pigletsstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY piglets_pigletsstatus (id, created_at, modified_at, title) FROM stdin;
1	2019-10-17 13:28:57.786068+00	2019-10-17 13:28:57.786086+00	Родились, кормятся
2	2019-10-17 13:28:57.7861+00	2019-10-17 13:28:57.786108+00	Готовы ко взвешиванию
3	2019-10-17 13:28:57.786118+00	2019-10-17 13:28:57.786125+00	Взвешены, готовы к заселению
4	2019-10-17 13:28:57.786135+00	2019-10-17 13:28:57.786142+00	Кормятся
5	2019-10-17 13:28:57.786152+00	2019-10-17 13:28:57.786159+00	Объединены с другой группой
\.


--
-- Data for Name: sows_boar; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_boar (id, created_at, modified_at, birth_id, location_id) FROM stdin;
3	2019-10-21 05:50:01.432709+00	2019-10-21 05:50:01.432754+00	017	1
4	2019-10-21 05:50:14.957832+00	2019-10-21 05:50:14.95797+00	018	1
5	2019-10-21 05:50:27.306186+00	2019-10-21 05:50:27.306216+00	019	1
6	2019-10-21 05:50:35.486347+00	2019-10-21 05:50:35.486375+00	020	1
7	2019-10-21 05:50:45.16501+00	2019-10-21 05:50:45.165043+00	021	1
8	2019-10-21 05:50:57.523223+00	2019-10-21 05:50:57.533611+00	022	1
9	2019-10-21 05:51:07.918011+00	2019-10-21 05:51:07.918046+00	011	1
10	2019-10-21 05:51:16.329727+00	2019-10-21 05:51:16.329763+00	416	1
11	2019-10-21 05:51:31.079943+00	2019-10-21 05:51:31.079973+00	417	1
12	2019-10-21 05:51:38.66361+00	2019-10-21 05:51:38.663639+00	216	1
13	2019-10-25 06:51:31.085936+00	2019-10-25 06:51:31.085981+00	19	1
14	2019-10-25 06:51:31.092311+00	2019-10-25 06:51:31.092333+00	18	1
15	2019-10-25 06:51:31.133084+00	2019-10-25 06:51:31.133131+00	17	1
16	2019-10-25 06:51:31.323709+00	2019-10-25 06:51:31.323735+00	21	1
17	2019-10-25 06:51:33.628738+00	2019-10-25 06:51:33.628765+00	22	1
18	2019-10-25 06:51:33.64103+00	2019-10-25 06:51:33.641055+00	20	1
\.


--
-- Data for Name: sows_events_abortionsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_abortionsow (id, created_at, modified_at, date, initiator_id, sow_id, tour_id) FROM stdin;
1	2019-11-04 08:08:05.494157+00	2019-11-04 08:08:05.494181+00	\N	9	272	4
\.


--
-- Data for Name: sows_events_cullingsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_cullingsow (id, created_at, modified_at, date, culling_type, reason, initiator_id, sow_id, tour_id) FROM stdin;
1	2019-11-04 08:06:57.472922+00	2019-11-04 08:06:57.473711+00	2019-11-04 08:06:57.469088+00	padej	padej	9	272	4
2	2019-11-04 08:07:03.977397+00	2019-11-04 08:07:03.977457+00	2019-11-04 08:07:03.976738+00	padej	padej	9	272	4
3	2019-11-04 08:07:29.801971+00	2019-11-04 08:07:29.802061+00	2019-11-04 08:07:29.801685+00	padej	padej	9	272	4
4	2019-11-04 08:07:32.305777+00	2019-11-04 08:07:32.3058+00	2019-11-04 08:07:32.304876+00	padej	padej	9	272	4
5	2019-11-04 08:08:27.958536+00	2019-11-04 08:08:27.958555+00	2019-11-04 08:08:27.957862+00	padej	padej	9	272	\N
6	2019-11-04 08:08:40.62509+00	2019-11-04 08:08:40.62514+00	2019-11-04 08:08:40.624779+00	padej	padej	9	272	\N
7	2019-11-04 08:08:44.54215+00	2019-11-04 08:08:44.542171+00	2019-11-04 08:08:44.54094+00	padej	padej	9	272	\N
\.


--
-- Data for Name: sows_events_semination; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_semination (id, created_at, modified_at, date, boar_id, initiator_id, semination_employee_id, sow_id, tour_id) FROM stdin;
1	2019-10-18 03:44:16.366805+00	2019-10-18 03:44:16.366823+00	2019-10-18 03:44:16.366832+00	\N	1	1	1	1
2	2019-10-18 03:44:16.389361+00	2019-10-18 03:44:16.38938+00	2019-10-18 03:44:16.389389+00	\N	1	1	1	1
3	2019-10-18 03:51:17.799836+00	2019-10-18 03:51:17.799866+00	2019-10-18 03:51:17.799875+00	\N	1	1	2	2
4	2019-10-18 03:51:17.799932+00	2019-10-18 03:51:17.799942+00	2019-10-18 03:51:17.799949+00	\N	1	1	3	2
5	2019-10-18 03:51:17.799984+00	2019-10-18 03:51:17.799992+00	2019-10-18 03:51:17.799999+00	\N	1	1	4	2
6	2019-10-18 03:51:17.800033+00	2019-10-18 03:51:17.800041+00	2019-10-18 03:51:17.800049+00	\N	1	1	5	2
7	2019-10-18 03:51:17.800082+00	2019-10-18 03:51:17.80009+00	2019-10-18 03:51:17.800097+00	\N	1	1	6	2
8	2019-10-18 03:51:17.800135+00	2019-10-18 03:51:17.800143+00	2019-10-18 03:51:17.80015+00	\N	1	1	7	2
9	2019-10-18 03:51:17.800183+00	2019-10-18 03:51:17.800191+00	2019-10-18 03:51:17.800205+00	\N	1	1	8	2
10	2019-10-18 03:51:17.800238+00	2019-10-18 03:51:17.800245+00	2019-10-18 03:51:17.800252+00	\N	1	1	9	2
11	2019-10-18 03:51:17.800342+00	2019-10-18 03:51:17.800351+00	2019-10-18 03:51:17.800358+00	\N	1	1	10	2
12	2019-10-18 03:51:17.800391+00	2019-10-18 03:51:17.800405+00	2019-10-18 03:51:17.800412+00	\N	1	1	11	2
13	2019-10-18 03:51:17.800445+00	2019-10-18 03:51:17.800453+00	2019-10-18 03:51:17.80046+00	\N	1	1	12	2
14	2019-10-18 03:51:17.800493+00	2019-10-18 03:51:17.800503+00	2019-10-18 03:51:17.800512+00	\N	1	1	13	2
15	2019-10-18 03:51:17.800552+00	2019-10-18 03:51:17.80056+00	2019-10-18 03:51:17.800567+00	\N	1	1	14	2
16	2019-10-18 03:51:17.800601+00	2019-10-18 03:51:17.800608+00	2019-10-18 03:51:17.800615+00	\N	1	1	15	2
17	2019-10-18 03:51:17.800648+00	2019-10-18 03:51:17.800656+00	2019-10-18 03:51:17.800662+00	\N	1	1	16	2
18	2019-10-18 03:51:17.800695+00	2019-10-18 03:51:17.800709+00	2019-10-18 03:51:17.800716+00	\N	1	1	17	2
19	2019-10-18 03:51:17.800749+00	2019-10-18 03:51:17.800757+00	2019-10-18 03:51:17.800764+00	\N	1	1	18	2
20	2019-10-18 03:51:17.800796+00	2019-10-18 03:51:17.800804+00	2019-10-18 03:51:17.800811+00	\N	1	1	19	2
21	2019-10-18 03:51:17.800844+00	2019-10-18 03:51:17.800852+00	2019-10-18 03:51:17.800859+00	\N	1	1	20	2
22	2019-10-18 03:51:17.800891+00	2019-10-18 03:51:17.800899+00	2019-10-18 03:51:17.800906+00	\N	1	1	21	2
23	2019-10-18 03:51:17.800938+00	2019-10-18 03:51:17.800946+00	2019-10-18 03:51:17.800952+00	\N	1	1	22	2
24	2019-10-18 03:51:17.800985+00	2019-10-18 03:51:17.800993+00	2019-10-18 03:51:17.800999+00	\N	1	1	23	2
25	2019-10-18 03:51:17.801032+00	2019-10-18 03:51:17.80104+00	2019-10-18 03:51:17.801047+00	\N	1	1	24	2
26	2019-10-18 03:51:17.80108+00	2019-10-18 03:51:17.801087+00	2019-10-18 03:51:17.801094+00	\N	1	1	25	2
27	2019-10-18 03:51:17.801127+00	2019-10-18 03:51:17.801135+00	2019-10-18 03:51:17.801142+00	\N	1	1	26	2
28	2019-10-18 03:51:17.801175+00	2019-10-18 03:51:17.801182+00	2019-10-18 03:51:17.801189+00	\N	1	1	27	2
29	2019-10-18 03:51:17.801229+00	2019-10-18 03:51:17.801237+00	2019-10-18 03:51:17.801244+00	\N	1	1	28	2
30	2019-10-18 03:51:17.801277+00	2019-10-18 03:51:17.801285+00	2019-10-18 03:51:17.801291+00	\N	1	1	29	2
31	2019-10-18 03:51:17.801338+00	2019-10-18 03:51:17.801347+00	2019-10-18 03:51:17.801354+00	\N	1	1	30	2
32	2019-10-18 03:51:17.801388+00	2019-10-18 03:51:17.801396+00	2019-10-18 03:51:17.801403+00	\N	1	1	31	2
33	2019-10-18 03:51:17.801437+00	2019-10-18 03:51:17.801444+00	2019-10-18 03:51:17.801451+00	\N	1	1	32	2
34	2019-10-18 03:51:17.801484+00	2019-10-18 03:51:17.801492+00	2019-10-18 03:51:17.801499+00	\N	1	1	33	2
35	2019-10-18 03:51:17.801532+00	2019-10-18 03:51:17.80154+00	2019-10-18 03:51:17.801547+00	\N	1	1	34	2
36	2019-10-18 03:51:17.80158+00	2019-10-18 03:51:17.801588+00	2019-10-18 03:51:17.801594+00	\N	1	1	35	2
37	2019-10-18 03:51:17.801628+00	2019-10-18 03:51:17.801635+00	2019-10-18 03:51:17.801642+00	\N	1	1	36	2
38	2019-10-18 03:51:17.801676+00	2019-10-18 03:51:17.801683+00	2019-10-18 03:51:17.80169+00	\N	1	1	37	2
39	2019-10-18 03:51:17.801724+00	2019-10-18 03:51:17.801731+00	2019-10-18 03:51:17.801738+00	\N	1	1	38	2
40	2019-10-18 03:51:17.801771+00	2019-10-18 03:51:17.801779+00	2019-10-18 03:51:17.801786+00	\N	1	1	39	2
41	2019-10-18 03:51:17.801819+00	2019-10-18 03:51:17.801827+00	2019-10-18 03:51:17.801834+00	\N	1	1	40	2
42	2019-10-18 03:51:17.801867+00	2019-10-18 03:51:17.801874+00	2019-10-18 03:51:17.801881+00	\N	1	1	41	2
43	2019-10-18 03:51:17.801914+00	2019-10-18 03:51:17.801922+00	2019-10-18 03:51:17.801929+00	\N	1	1	42	2
44	2019-10-18 03:51:17.801962+00	2019-10-18 03:51:17.801969+00	2019-10-18 03:51:17.801976+00	\N	1	1	43	2
45	2019-10-18 03:51:17.802009+00	2019-10-18 03:51:17.802017+00	2019-10-18 03:51:17.802024+00	\N	1	1	44	2
46	2019-10-18 03:51:17.802057+00	2019-10-18 03:51:17.802064+00	2019-10-18 03:51:17.802071+00	\N	1	1	45	2
47	2019-10-18 03:51:17.802104+00	2019-10-18 03:51:17.802111+00	2019-10-18 03:51:17.802118+00	\N	1	1	46	2
48	2019-10-18 03:51:17.802151+00	2019-10-18 03:51:17.802159+00	2019-10-18 03:51:17.802166+00	\N	1	1	47	2
49	2019-10-18 03:51:17.802199+00	2019-10-18 03:51:17.802206+00	2019-10-18 03:51:17.802213+00	\N	1	1	48	2
50	2019-10-18 03:51:17.802246+00	2019-10-18 03:51:17.802254+00	2019-10-18 03:51:17.802261+00	\N	1	1	49	2
51	2019-10-18 03:51:17.802294+00	2019-10-18 03:51:17.802302+00	2019-10-18 03:51:17.802309+00	\N	1	1	50	2
52	2019-10-18 03:51:17.802342+00	2019-10-18 03:51:17.802349+00	2019-10-18 03:51:17.802356+00	\N	1	1	51	2
53	2019-10-18 03:51:17.802434+00	2019-10-18 03:51:17.802443+00	2019-10-18 03:51:17.80245+00	\N	1	1	52	2
54	2019-10-18 03:51:17.80249+00	2019-10-18 03:51:17.802498+00	2019-10-18 03:51:17.802505+00	\N	1	1	53	2
55	2019-10-18 03:51:17.802538+00	2019-10-18 03:51:17.802545+00	2019-10-18 03:51:17.802552+00	\N	1	1	54	2
56	2019-10-18 03:51:17.802585+00	2019-10-18 03:51:17.802593+00	2019-10-18 03:51:17.8026+00	\N	1	1	55	2
57	2019-10-18 03:51:17.802632+00	2019-10-18 03:51:17.80264+00	2019-10-18 03:51:17.802647+00	\N	1	1	56	2
58	2019-10-18 03:51:17.802687+00	2019-10-18 03:51:17.802696+00	2019-10-18 03:51:17.802704+00	\N	1	1	57	2
59	2019-10-18 03:51:17.802737+00	2019-10-18 03:51:17.802745+00	2019-10-18 03:51:17.802752+00	\N	1	1	58	2
60	2019-10-18 03:51:17.802786+00	2019-10-18 03:51:17.802794+00	2019-10-18 03:51:17.802801+00	\N	1	1	59	2
61	2019-10-18 03:51:17.802835+00	2019-10-18 03:51:17.802843+00	2019-10-18 03:51:17.802849+00	\N	1	1	60	2
62	2019-10-18 03:51:17.802913+00	2019-10-18 03:51:17.802924+00	2019-10-18 03:51:17.802931+00	\N	1	1	61	2
63	2019-10-18 03:51:17.802965+00	2019-10-18 03:51:17.802972+00	2019-10-18 03:51:17.802979+00	\N	1	1	62	2
64	2019-10-18 03:51:17.803012+00	2019-10-18 03:51:17.80302+00	2019-10-18 03:51:17.803027+00	\N	1	1	63	2
65	2019-10-18 03:51:17.80306+00	2019-10-18 03:51:17.803068+00	2019-10-18 03:51:17.803075+00	\N	1	1	64	2
66	2019-10-18 03:51:17.851639+00	2019-10-18 03:51:17.851667+00	2019-10-18 03:51:17.851676+00	\N	1	1	2	2
67	2019-10-18 03:51:17.851724+00	2019-10-18 03:51:17.851733+00	2019-10-18 03:51:17.85174+00	\N	1	1	3	2
68	2019-10-18 03:51:17.851775+00	2019-10-18 03:51:17.851783+00	2019-10-18 03:51:17.85179+00	\N	1	1	4	2
69	2019-10-18 03:51:17.851823+00	2019-10-18 03:51:17.851831+00	2019-10-18 03:51:17.851838+00	\N	1	1	5	2
70	2019-10-18 03:51:17.85187+00	2019-10-18 03:51:17.851878+00	2019-10-18 03:51:17.851885+00	\N	1	1	6	2
71	2019-10-18 03:51:17.851918+00	2019-10-18 03:51:17.851926+00	2019-10-18 03:51:17.851933+00	\N	1	1	7	2
72	2019-10-18 03:51:17.851967+00	2019-10-18 03:51:17.851981+00	2019-10-18 03:51:17.851987+00	\N	1	1	8	2
73	2019-10-18 03:51:17.852023+00	2019-10-18 03:51:17.85203+00	2019-10-18 03:51:17.852037+00	\N	1	1	9	2
74	2019-10-18 03:51:17.85207+00	2019-10-18 03:51:17.852078+00	2019-10-18 03:51:17.852085+00	\N	1	1	10	2
75	2019-10-18 03:51:17.852118+00	2019-10-18 03:51:17.852126+00	2019-10-18 03:51:17.852133+00	\N	1	1	11	2
76	2019-10-18 03:51:17.852166+00	2019-10-18 03:51:17.852173+00	2019-10-18 03:51:17.85218+00	\N	1	1	12	2
77	2019-10-18 03:51:17.852213+00	2019-10-18 03:51:17.852221+00	2019-10-18 03:51:17.852228+00	\N	1	1	13	2
78	2019-10-18 03:51:17.852261+00	2019-10-18 03:51:17.852268+00	2019-10-18 03:51:17.852275+00	\N	1	1	14	2
79	2019-10-18 03:51:17.852308+00	2019-10-18 03:51:17.852316+00	2019-10-18 03:51:17.852323+00	\N	1	1	15	2
80	2019-10-18 03:51:17.852356+00	2019-10-18 03:51:17.852363+00	2019-10-18 03:51:17.85237+00	\N	1	1	16	2
81	2019-10-18 03:51:17.852403+00	2019-10-18 03:51:17.852411+00	2019-10-18 03:51:17.852418+00	\N	1	1	17	2
82	2019-10-18 03:51:17.85245+00	2019-10-18 03:51:17.852458+00	2019-10-18 03:51:17.852465+00	\N	1	1	18	2
83	2019-10-18 03:51:17.852498+00	2019-10-18 03:51:17.852506+00	2019-10-18 03:51:17.852513+00	\N	1	1	19	2
84	2019-10-18 03:51:17.852546+00	2019-10-18 03:51:17.852553+00	2019-10-18 03:51:17.85256+00	\N	1	1	20	2
85	2019-10-18 03:51:17.852593+00	2019-10-18 03:51:17.852601+00	2019-10-18 03:51:17.852607+00	\N	1	1	21	2
86	2019-10-18 03:51:17.852641+00	2019-10-18 03:51:17.852648+00	2019-10-18 03:51:17.852655+00	\N	1	1	22	2
87	2019-10-18 03:51:17.852688+00	2019-10-18 03:51:17.852695+00	2019-10-18 03:51:17.852702+00	\N	1	1	23	2
88	2019-10-18 03:51:17.852735+00	2019-10-18 03:51:17.852742+00	2019-10-18 03:51:17.852749+00	\N	1	1	24	2
89	2019-10-18 03:51:17.852782+00	2019-10-18 03:51:17.852789+00	2019-10-18 03:51:17.852796+00	\N	1	1	25	2
90	2019-10-18 03:51:17.852829+00	2019-10-18 03:51:17.852837+00	2019-10-18 03:51:17.852844+00	\N	1	1	26	2
91	2019-10-18 03:51:17.852876+00	2019-10-18 03:51:17.852884+00	2019-10-18 03:51:17.852891+00	\N	1	1	27	2
92	2019-10-18 03:51:17.852924+00	2019-10-18 03:51:17.852932+00	2019-10-18 03:51:17.852939+00	\N	1	1	28	2
93	2019-10-18 03:51:17.852972+00	2019-10-18 03:51:17.85298+00	2019-10-18 03:51:17.852987+00	\N	1	1	29	2
94	2019-10-18 03:51:17.85302+00	2019-10-18 03:51:17.853027+00	2019-10-18 03:51:17.853035+00	\N	1	1	30	2
95	2019-10-18 03:51:17.853068+00	2019-10-18 03:51:17.853076+00	2019-10-18 03:51:17.853083+00	\N	1	1	31	2
96	2019-10-18 03:51:17.853116+00	2019-10-18 03:51:17.853123+00	2019-10-18 03:51:17.85313+00	\N	1	1	32	2
97	2019-10-18 03:51:17.853163+00	2019-10-18 03:51:17.853171+00	2019-10-18 03:51:17.853178+00	\N	1	1	33	2
98	2019-10-18 03:51:17.853211+00	2019-10-18 03:51:17.853218+00	2019-10-18 03:51:17.853225+00	\N	1	1	34	2
99	2019-10-18 03:51:17.853258+00	2019-10-18 03:51:17.853265+00	2019-10-18 03:51:17.853272+00	\N	1	1	35	2
100	2019-10-18 03:51:17.853305+00	2019-10-18 03:51:17.853312+00	2019-10-18 03:51:17.853319+00	\N	1	1	36	2
101	2019-10-18 03:51:17.853352+00	2019-10-18 03:51:17.85336+00	2019-10-18 03:51:17.853367+00	\N	1	1	37	2
102	2019-10-18 03:51:17.8534+00	2019-10-18 03:51:17.853407+00	2019-10-18 03:51:17.853414+00	\N	1	1	38	2
103	2019-10-18 03:51:17.853447+00	2019-10-18 03:51:17.853455+00	2019-10-18 03:51:17.85348+00	\N	1	1	39	2
104	2019-10-18 03:51:17.853529+00	2019-10-18 03:51:17.853536+00	2019-10-18 03:51:17.853543+00	\N	1	1	40	2
105	2019-10-18 03:51:17.853576+00	2019-10-18 03:51:17.853584+00	2019-10-18 03:51:17.853591+00	\N	1	1	41	2
106	2019-10-18 03:51:17.853624+00	2019-10-18 03:51:17.853631+00	2019-10-18 03:51:17.853638+00	\N	1	1	42	2
107	2019-10-18 03:51:17.853671+00	2019-10-18 03:51:17.853679+00	2019-10-18 03:51:17.853685+00	\N	1	1	43	2
108	2019-10-18 03:51:17.853718+00	2019-10-18 03:51:17.853726+00	2019-10-18 03:51:17.853733+00	\N	1	1	44	2
109	2019-10-18 03:51:17.853766+00	2019-10-18 03:51:17.853773+00	2019-10-18 03:51:17.85378+00	\N	1	1	45	2
110	2019-10-18 03:51:17.853813+00	2019-10-18 03:51:17.85382+00	2019-10-18 03:51:17.853827+00	\N	1	1	46	2
111	2019-10-18 03:51:17.85386+00	2019-10-18 03:51:17.853868+00	2019-10-18 03:51:17.853875+00	\N	1	1	47	2
112	2019-10-18 03:51:17.853907+00	2019-10-18 03:51:17.853915+00	2019-10-18 03:51:17.853922+00	\N	1	1	48	2
113	2019-10-18 03:51:17.853955+00	2019-10-18 03:51:17.853963+00	2019-10-18 03:51:17.85397+00	\N	1	1	49	2
114	2019-10-18 03:51:17.854003+00	2019-10-18 03:51:17.85401+00	2019-10-18 03:51:17.854017+00	\N	1	1	50	2
115	2019-10-18 03:51:17.85405+00	2019-10-18 03:51:17.854058+00	2019-10-18 03:51:17.854065+00	\N	1	1	51	2
116	2019-10-18 03:51:17.854097+00	2019-10-18 03:51:17.854105+00	2019-10-18 03:51:17.854112+00	\N	1	1	52	2
117	2019-10-18 03:51:17.854145+00	2019-10-18 03:51:17.854152+00	2019-10-18 03:51:17.85416+00	\N	1	1	53	2
118	2019-10-18 03:51:17.854192+00	2019-10-18 03:51:17.8542+00	2019-10-18 03:51:17.854207+00	\N	1	1	54	2
119	2019-10-18 03:51:17.85424+00	2019-10-18 03:51:17.854247+00	2019-10-18 03:51:17.854254+00	\N	1	1	55	2
120	2019-10-18 03:51:17.854287+00	2019-10-18 03:51:17.854294+00	2019-10-18 03:51:17.854301+00	\N	1	1	56	2
121	2019-10-18 03:51:17.854334+00	2019-10-18 03:51:17.854342+00	2019-10-18 03:51:17.854348+00	\N	1	1	57	2
122	2019-10-18 03:51:17.854393+00	2019-10-18 03:51:17.854401+00	2019-10-18 03:51:17.854408+00	\N	1	1	58	2
123	2019-10-18 03:51:17.854441+00	2019-10-18 03:51:17.854448+00	2019-10-18 03:51:17.854455+00	\N	1	1	59	2
124	2019-10-18 03:51:17.854488+00	2019-10-18 03:51:17.854496+00	2019-10-18 03:51:17.854502+00	\N	1	1	60	2
125	2019-10-18 03:51:17.854536+00	2019-10-18 03:51:17.854544+00	2019-10-18 03:51:17.85455+00	\N	1	1	61	2
126	2019-10-18 03:51:17.854583+00	2019-10-18 03:51:17.854591+00	2019-10-18 03:51:17.854598+00	\N	1	1	62	2
127	2019-10-18 03:51:17.854631+00	2019-10-18 03:51:17.854638+00	2019-10-18 03:51:17.854645+00	\N	1	1	63	2
128	2019-10-18 03:51:17.854678+00	2019-10-18 03:51:17.854685+00	2019-10-18 03:51:17.854692+00	\N	1	1	64	2
417	2019-11-01 04:33:38.237912+00	2019-11-01 04:33:38.237938+00	2019-11-01 04:33:38.219486+00	\N	4	4	256	4
418	2019-11-01 04:33:38.237997+00	2019-11-01 04:33:38.238003+00	2019-11-01 04:33:38.219486+00	\N	4	4	257	4
419	2019-11-01 04:33:38.23804+00	2019-11-01 04:33:38.238046+00	2019-11-01 04:33:38.219486+00	\N	4	4	258	4
420	2019-11-01 04:33:38.238081+00	2019-11-01 04:33:38.238087+00	2019-11-01 04:33:38.219486+00	\N	4	4	259	4
421	2019-11-01 04:33:38.238122+00	2019-11-01 04:33:38.238128+00	2019-11-01 04:33:38.219486+00	\N	4	4	260	4
422	2019-11-01 04:33:38.238164+00	2019-11-01 04:33:38.238169+00	2019-11-01 04:33:38.219486+00	\N	4	4	261	4
423	2019-11-01 04:33:38.238204+00	2019-11-01 04:33:38.238209+00	2019-11-01 04:33:38.219486+00	\N	4	4	262	4
424	2019-11-01 04:33:38.238245+00	2019-11-01 04:33:38.23825+00	2019-11-01 04:33:38.219486+00	\N	4	4	263	4
425	2019-11-01 04:33:38.238286+00	2019-11-01 04:33:38.238291+00	2019-11-01 04:33:38.219486+00	\N	4	4	264	4
426	2019-11-01 04:33:38.238326+00	2019-11-01 04:33:38.238332+00	2019-11-01 04:33:38.219486+00	\N	4	4	265	4
427	2019-11-01 04:33:38.238367+00	2019-11-01 04:33:38.238372+00	2019-11-01 04:33:38.219486+00	\N	4	4	266	4
428	2019-11-01 04:33:38.238408+00	2019-11-01 04:33:38.238413+00	2019-11-01 04:33:38.219486+00	\N	4	4	267	4
429	2019-11-01 04:33:38.238448+00	2019-11-01 04:33:38.238453+00	2019-11-01 04:33:38.219486+00	\N	4	4	268	4
430	2019-11-01 04:33:38.238514+00	2019-11-01 04:33:38.23852+00	2019-11-01 04:33:38.219486+00	\N	4	4	269	4
431	2019-11-01 04:33:38.238558+00	2019-11-01 04:33:38.238563+00	2019-11-01 04:33:38.219486+00	\N	4	4	270	4
432	2019-11-01 04:33:38.238599+00	2019-11-01 04:33:38.238604+00	2019-11-01 04:33:38.219486+00	\N	4	4	271	4
433	2019-11-01 04:33:38.23864+00	2019-11-01 04:33:38.238645+00	2019-11-01 04:33:38.219486+00	\N	4	4	272	4
434	2019-11-01 04:33:38.238681+00	2019-11-01 04:33:38.238686+00	2019-11-01 04:33:38.219486+00	\N	4	4	273	4
435	2019-11-01 04:33:38.238721+00	2019-11-01 04:33:38.238727+00	2019-11-01 04:33:38.219486+00	\N	4	4	274	4
436	2019-11-01 04:33:38.238772+00	2019-11-01 04:33:38.238777+00	2019-11-01 04:33:38.219486+00	\N	4	4	275	4
437	2019-11-01 04:33:38.238813+00	2019-11-01 04:33:38.238821+00	2019-11-01 04:33:38.219486+00	\N	4	4	276	4
438	2019-11-01 04:33:38.238865+00	2019-11-01 04:33:38.238872+00	2019-11-01 04:33:38.219486+00	\N	4	4	277	4
439	2019-11-01 04:33:38.238914+00	2019-11-01 04:33:38.23892+00	2019-11-01 04:33:38.219486+00	\N	4	4	278	4
440	2019-11-01 04:33:38.238962+00	2019-11-01 04:33:38.238969+00	2019-11-01 04:33:38.219486+00	\N	4	4	279	4
441	2019-11-01 04:33:38.239011+00	2019-11-01 04:33:38.239018+00	2019-11-01 04:33:38.219486+00	\N	4	4	280	4
442	2019-11-01 04:33:38.23906+00	2019-11-01 04:33:38.239066+00	2019-11-01 04:33:38.219486+00	\N	4	4	281	4
443	2019-11-01 04:33:38.239108+00	2019-11-01 04:33:38.239115+00	2019-11-01 04:33:38.219486+00	\N	4	4	282	4
444	2019-11-01 04:33:38.239163+00	2019-11-01 04:33:38.23917+00	2019-11-01 04:33:38.219486+00	\N	4	4	283	4
445	2019-11-01 04:33:38.239211+00	2019-11-01 04:33:38.239217+00	2019-11-01 04:33:38.219486+00	\N	4	4	284	4
446	2019-11-01 04:33:38.239253+00	2019-11-01 04:33:38.239259+00	2019-11-01 04:33:38.219486+00	\N	4	4	285	4
447	2019-11-01 04:33:38.239294+00	2019-11-01 04:33:38.2393+00	2019-11-01 04:33:38.219486+00	\N	4	4	286	4
448	2019-11-01 04:33:38.239335+00	2019-11-01 04:33:38.23934+00	2019-11-01 04:33:38.219486+00	\N	4	4	287	4
449	2019-11-01 04:33:38.239376+00	2019-11-01 04:33:38.239381+00	2019-11-01 04:33:38.219486+00	\N	4	4	288	4
450	2019-11-01 04:33:38.239416+00	2019-11-01 04:33:38.239421+00	2019-11-01 04:33:38.219486+00	\N	4	4	289	4
451	2019-11-01 04:33:38.239456+00	2019-11-01 04:33:38.239462+00	2019-11-01 04:33:38.219486+00	\N	4	4	290	4
452	2019-11-01 04:33:38.239497+00	2019-11-01 04:33:38.239502+00	2019-11-01 04:33:38.219486+00	\N	4	4	291	4
163	2019-10-25 05:24:14.987849+00	2019-10-25 05:24:14.987874+00	2019-10-25 05:24:14.987883+00	\N	4	4	195	2
164	2019-10-25 05:24:14.987932+00	2019-10-25 05:24:14.98794+00	2019-10-25 05:24:14.987948+00	\N	4	4	196	2
165	2019-10-25 05:24:15.014265+00	2019-10-25 05:24:15.01429+00	2019-10-25 05:24:15.014299+00	\N	4	4	195	2
166	2019-10-25 05:24:15.014346+00	2019-10-25 05:24:15.014355+00	2019-10-25 05:24:15.014362+00	\N	4	4	196	2
167	2019-10-25 05:33:20.652054+00	2019-10-25 05:33:20.652093+00	2019-10-25 05:33:20.652102+00	\N	4	4	197	2
168	2019-10-25 05:33:20.652174+00	2019-10-25 05:33:20.652183+00	2019-10-25 05:33:20.65219+00	\N	4	4	198	2
169	2019-10-25 05:33:20.652225+00	2019-10-25 05:33:20.652233+00	2019-10-25 05:33:20.65224+00	\N	4	4	199	2
170	2019-10-25 05:33:20.652274+00	2019-10-25 05:33:20.652282+00	2019-10-25 05:33:20.652289+00	\N	4	4	200	2
171	2019-10-25 05:33:20.652323+00	2019-10-25 05:33:20.652331+00	2019-10-25 05:33:20.652338+00	\N	4	4	201	2
172	2019-10-25 05:33:20.652372+00	2019-10-25 05:33:20.652379+00	2019-10-25 05:33:20.652386+00	\N	4	4	202	2
173	2019-10-25 05:33:20.65242+00	2019-10-25 05:33:20.652428+00	2019-10-25 05:33:20.652435+00	\N	4	4	203	2
174	2019-10-25 05:33:20.652469+00	2019-10-25 05:33:20.652476+00	2019-10-25 05:33:20.652483+00	\N	4	4	204	2
175	2019-10-25 05:33:20.652517+00	2019-10-25 05:33:20.652524+00	2019-10-25 05:33:20.652531+00	\N	4	4	205	2
176	2019-10-25 05:33:20.652565+00	2019-10-25 05:33:20.652583+00	2019-10-25 05:33:20.652592+00	\N	4	4	206	2
177	2019-10-25 05:33:20.652627+00	2019-10-25 05:33:20.652635+00	2019-10-25 05:33:20.652642+00	\N	4	4	207	2
178	2019-10-25 05:33:20.652675+00	2019-10-25 05:33:20.652683+00	2019-10-25 05:33:20.65269+00	\N	4	4	208	2
179	2019-10-25 05:33:20.652724+00	2019-10-25 05:33:20.652732+00	2019-10-25 05:33:20.652739+00	\N	4	4	209	2
180	2019-10-25 05:33:20.652772+00	2019-10-25 05:33:20.65278+00	2019-10-25 05:33:20.652787+00	\N	4	4	210	2
181	2019-10-25 05:33:20.65282+00	2019-10-25 05:33:20.652828+00	2019-10-25 05:33:20.652835+00	\N	4	4	211	2
182	2019-10-25 05:33:20.652869+00	2019-10-25 05:33:20.652877+00	2019-10-25 05:33:20.652884+00	\N	4	4	212	2
183	2019-10-25 05:33:20.652971+00	2019-10-25 05:33:20.652983+00	2019-10-25 05:33:20.652991+00	\N	4	4	213	2
184	2019-10-25 05:33:20.653027+00	2019-10-25 05:33:20.653035+00	2019-10-25 05:33:20.653042+00	\N	4	4	214	2
185	2019-10-25 05:33:20.653076+00	2019-10-25 05:33:20.653083+00	2019-10-25 05:33:20.65309+00	\N	4	4	215	2
186	2019-10-25 05:33:20.653166+00	2019-10-25 05:33:20.653175+00	2019-10-25 05:33:20.653182+00	\N	4	4	216	2
187	2019-10-25 05:33:20.653216+00	2019-10-25 05:33:20.653224+00	2019-10-25 05:33:20.653231+00	\N	4	4	217	2
188	2019-10-25 05:33:20.653265+00	2019-10-25 05:33:20.653272+00	2019-10-25 05:33:20.653279+00	\N	4	4	218	2
189	2019-10-25 05:33:20.653313+00	2019-10-25 05:33:20.653321+00	2019-10-25 05:33:20.653328+00	\N	4	4	219	2
190	2019-10-25 05:33:20.653361+00	2019-10-25 05:33:20.653369+00	2019-10-25 05:33:20.653376+00	\N	4	4	220	2
191	2019-10-25 05:33:20.65341+00	2019-10-25 05:33:20.653417+00	2019-10-25 05:33:20.653424+00	\N	4	4	221	2
192	2019-10-25 05:33:20.653458+00	2019-10-25 05:33:20.653466+00	2019-10-25 05:33:20.653473+00	\N	4	4	222	2
193	2019-10-25 05:33:20.653507+00	2019-10-25 05:33:20.653515+00	2019-10-25 05:33:20.653522+00	\N	4	4	223	2
194	2019-10-25 05:33:20.653556+00	2019-10-25 05:33:20.653563+00	2019-10-25 05:33:20.65357+00	\N	4	4	224	2
195	2019-10-25 05:33:20.653604+00	2019-10-25 05:33:20.653612+00	2019-10-25 05:33:20.653619+00	\N	4	4	225	2
196	2019-10-25 05:33:20.653671+00	2019-10-25 05:33:20.65368+00	2019-10-25 05:33:20.653687+00	\N	4	4	226	2
197	2019-10-25 05:33:20.653721+00	2019-10-25 05:33:20.653729+00	2019-10-25 05:33:20.653736+00	\N	4	4	227	2
198	2019-10-25 05:33:20.65377+00	2019-10-25 05:33:20.653777+00	2019-10-25 05:33:20.653784+00	\N	4	4	228	2
199	2019-10-25 05:33:20.653818+00	2019-10-25 05:33:20.653826+00	2019-10-25 05:33:20.653833+00	\N	4	4	229	2
200	2019-10-25 05:33:20.653867+00	2019-10-25 05:33:20.653874+00	2019-10-25 05:33:20.653881+00	\N	4	4	230	2
201	2019-10-25 05:33:20.653915+00	2019-10-25 05:33:20.653923+00	2019-10-25 05:33:20.65393+00	\N	4	4	231	2
202	2019-10-25 05:33:20.65402+00	2019-10-25 05:33:20.65403+00	2019-10-25 05:33:20.654037+00	\N	4	4	232	2
203	2019-10-25 05:33:20.654072+00	2019-10-25 05:33:20.65408+00	2019-10-25 05:33:20.654088+00	\N	4	4	233	2
204	2019-10-25 05:33:20.654121+00	2019-10-25 05:33:20.654129+00	2019-10-25 05:33:20.654136+00	\N	4	4	234	2
205	2019-10-25 05:33:20.65417+00	2019-10-25 05:33:20.654178+00	2019-10-25 05:33:20.654185+00	\N	4	4	235	2
206	2019-10-25 05:33:20.654219+00	2019-10-25 05:33:20.654227+00	2019-10-25 05:33:20.654234+00	\N	4	4	236	2
207	2019-10-25 05:33:20.654269+00	2019-10-25 05:33:20.654277+00	2019-10-25 05:33:20.654284+00	\N	4	4	237	2
208	2019-10-25 05:33:20.654319+00	2019-10-25 05:33:20.654327+00	2019-10-25 05:33:20.654334+00	\N	4	4	238	2
209	2019-10-25 05:33:20.654368+00	2019-10-25 05:33:20.654376+00	2019-10-25 05:33:20.654383+00	\N	4	4	239	2
210	2019-10-25 05:33:20.654416+00	2019-10-25 05:33:20.654424+00	2019-10-25 05:33:20.654431+00	\N	4	4	240	2
211	2019-10-25 05:33:20.654465+00	2019-10-25 05:33:20.654473+00	2019-10-25 05:33:20.65448+00	\N	4	4	241	2
212	2019-10-25 05:33:20.654529+00	2019-10-25 05:33:20.65454+00	2019-10-25 05:33:20.654547+00	\N	4	4	242	2
213	2019-10-25 05:33:20.654581+00	2019-10-25 05:33:20.654589+00	2019-10-25 05:33:20.654596+00	\N	4	4	243	2
214	2019-10-25 05:33:20.654631+00	2019-10-25 05:33:20.654639+00	2019-10-25 05:33:20.654646+00	\N	4	4	244	2
215	2019-10-25 05:33:20.654679+00	2019-10-25 05:33:20.654687+00	2019-10-25 05:33:20.654694+00	\N	4	4	245	2
216	2019-10-25 05:33:20.654727+00	2019-10-25 05:33:20.654735+00	2019-10-25 05:33:20.654742+00	\N	4	4	246	2
217	2019-10-25 05:33:20.654775+00	2019-10-25 05:33:20.654782+00	2019-10-25 05:33:20.654789+00	\N	4	4	247	2
218	2019-10-25 05:33:20.654823+00	2019-10-25 05:33:20.65483+00	2019-10-25 05:33:20.654837+00	\N	4	4	248	2
219	2019-10-25 05:33:20.654871+00	2019-10-25 05:33:20.654878+00	2019-10-25 05:33:20.654885+00	\N	4	4	249	2
220	2019-10-25 05:33:20.654919+00	2019-10-25 05:33:20.654927+00	2019-10-25 05:33:20.654934+00	\N	4	4	250	2
221	2019-10-25 05:33:20.655012+00	2019-10-25 05:33:20.655024+00	2019-10-25 05:33:20.655031+00	\N	4	4	251	2
222	2019-10-25 05:33:20.655067+00	2019-10-25 05:33:20.655075+00	2019-10-25 05:33:20.655082+00	\N	4	4	252	2
223	2019-10-25 05:33:20.655116+00	2019-10-25 05:33:20.655124+00	2019-10-25 05:33:20.655131+00	\N	4	4	253	2
224	2019-10-25 05:33:20.65518+00	2019-10-25 05:33:20.655188+00	2019-10-25 05:33:20.655195+00	\N	4	4	254	2
225	2019-10-25 05:33:20.655229+00	2019-10-25 05:33:20.655237+00	2019-10-25 05:33:20.655244+00	\N	4	4	255	2
226	2019-10-25 05:33:20.775524+00	2019-10-25 05:33:20.775549+00	2019-10-25 05:33:20.775558+00	\N	4	4	208	2
227	2019-10-25 05:33:20.775606+00	2019-10-25 05:33:20.775615+00	2019-10-25 05:33:20.775623+00	\N	4	4	209	2
228	2019-10-25 05:33:20.775657+00	2019-10-25 05:33:20.775665+00	2019-10-25 05:33:20.775672+00	\N	4	4	210	2
229	2019-10-25 05:33:20.775705+00	2019-10-25 05:33:20.775713+00	2019-10-25 05:33:20.77572+00	\N	4	4	211	2
230	2019-10-25 05:33:20.775753+00	2019-10-25 05:33:20.775761+00	2019-10-25 05:33:20.775768+00	\N	4	4	212	2
231	2019-10-25 05:33:20.775801+00	2019-10-25 05:33:20.775809+00	2019-10-25 05:33:20.775816+00	\N	4	4	213	2
232	2019-10-25 05:33:20.77585+00	2019-10-25 05:33:20.775858+00	2019-10-25 05:33:20.775865+00	\N	4	4	214	2
233	2019-10-25 05:33:20.775899+00	2019-10-25 05:33:20.775906+00	2019-10-25 05:33:20.775913+00	\N	4	4	215	2
234	2019-10-25 05:33:20.775947+00	2019-10-25 05:33:20.775954+00	2019-10-25 05:33:20.775961+00	\N	4	4	216	2
235	2019-10-25 05:33:20.775995+00	2019-10-25 05:33:20.776003+00	2019-10-25 05:33:20.77601+00	\N	4	4	217	2
236	2019-10-25 05:33:20.776043+00	2019-10-25 05:33:20.776051+00	2019-10-25 05:33:20.776058+00	\N	4	4	218	2
237	2019-10-25 05:33:20.776091+00	2019-10-25 05:33:20.776098+00	2019-10-25 05:33:20.776105+00	\N	4	4	219	2
238	2019-10-25 05:33:20.776139+00	2019-10-25 05:33:20.776146+00	2019-10-25 05:33:20.776153+00	\N	4	4	220	2
239	2019-10-25 05:33:20.776186+00	2019-10-25 05:33:20.776193+00	2019-10-25 05:33:20.7762+00	\N	4	4	197	2
240	2019-10-25 05:33:20.776233+00	2019-10-25 05:33:20.776241+00	2019-10-25 05:33:20.776248+00	\N	4	4	198	2
241	2019-10-25 05:33:20.776281+00	2019-10-25 05:33:20.776288+00	2019-10-25 05:33:20.776295+00	\N	4	4	199	2
242	2019-10-25 05:33:20.776328+00	2019-10-25 05:33:20.776336+00	2019-10-25 05:33:20.776343+00	\N	4	4	200	2
243	2019-10-25 05:33:20.776376+00	2019-10-25 05:33:20.776384+00	2019-10-25 05:33:20.776391+00	\N	4	4	201	2
244	2019-10-25 05:33:20.776424+00	2019-10-25 05:33:20.776431+00	2019-10-25 05:33:20.776438+00	\N	4	4	202	2
245	2019-10-25 05:33:20.776472+00	2019-10-25 05:33:20.776479+00	2019-10-25 05:33:20.776486+00	\N	4	4	203	2
246	2019-10-25 05:33:20.776519+00	2019-10-25 05:33:20.776527+00	2019-10-25 05:33:20.776534+00	\N	4	4	204	2
247	2019-10-25 05:33:20.776567+00	2019-10-25 05:33:20.776586+00	2019-10-25 05:33:20.776594+00	\N	4	4	205	2
248	2019-10-25 05:33:20.776629+00	2019-10-25 05:33:20.776636+00	2019-10-25 05:33:20.776643+00	\N	4	4	206	2
249	2019-10-25 05:33:20.776677+00	2019-10-25 05:33:20.776684+00	2019-10-25 05:33:20.776691+00	\N	4	4	207	2
250	2019-10-25 05:33:20.776725+00	2019-10-25 05:33:20.776732+00	2019-10-25 05:33:20.776739+00	\N	4	4	221	2
251	2019-10-25 05:33:20.776773+00	2019-10-25 05:33:20.77678+00	2019-10-25 05:33:20.776787+00	\N	4	4	222	2
252	2019-10-25 05:33:20.776821+00	2019-10-25 05:33:20.776828+00	2019-10-25 05:33:20.776835+00	\N	4	4	223	2
253	2019-10-25 05:33:20.776869+00	2019-10-25 05:33:20.776877+00	2019-10-25 05:33:20.776884+00	\N	4	4	224	2
254	2019-10-25 05:33:20.776916+00	2019-10-25 05:33:20.776924+00	2019-10-25 05:33:20.776931+00	\N	4	4	225	2
255	2019-10-25 05:33:20.776964+00	2019-10-25 05:33:20.776971+00	2019-10-25 05:33:20.776978+00	\N	4	4	226	2
256	2019-10-25 05:33:20.777011+00	2019-10-25 05:33:20.777019+00	2019-10-25 05:33:20.777025+00	\N	4	4	227	2
257	2019-10-25 05:33:20.777058+00	2019-10-25 05:33:20.777066+00	2019-10-25 05:33:20.777073+00	\N	4	4	228	2
258	2019-10-25 05:33:20.777129+00	2019-10-25 05:33:20.777139+00	2019-10-25 05:33:20.777146+00	\N	4	4	229	2
259	2019-10-25 05:33:20.777179+00	2019-10-25 05:33:20.777187+00	2019-10-25 05:33:20.777194+00	\N	4	4	230	2
260	2019-10-25 05:33:20.777226+00	2019-10-25 05:33:20.777234+00	2019-10-25 05:33:20.777241+00	\N	4	4	231	2
261	2019-10-25 05:33:20.777274+00	2019-10-25 05:33:20.777281+00	2019-10-25 05:33:20.777288+00	\N	4	4	232	2
262	2019-10-25 05:33:20.777322+00	2019-10-25 05:33:20.777329+00	2019-10-25 05:33:20.777336+00	\N	4	4	233	2
263	2019-10-25 05:33:20.777369+00	2019-10-25 05:33:20.777376+00	2019-10-25 05:33:20.777383+00	\N	4	4	234	2
264	2019-10-25 05:33:20.777416+00	2019-10-25 05:33:20.777424+00	2019-10-25 05:33:20.77743+00	\N	4	4	235	2
265	2019-10-25 05:33:20.777463+00	2019-10-25 05:33:20.777471+00	2019-10-25 05:33:20.777478+00	\N	4	4	236	2
266	2019-10-25 05:33:20.77751+00	2019-10-25 05:33:20.777518+00	2019-10-25 05:33:20.777524+00	\N	4	4	237	2
267	2019-10-25 05:33:20.777558+00	2019-10-25 05:33:20.777565+00	2019-10-25 05:33:20.777572+00	\N	4	4	238	2
268	2019-10-25 05:33:20.777605+00	2019-10-25 05:33:20.777612+00	2019-10-25 05:33:20.777619+00	\N	4	4	239	2
269	2019-10-25 05:33:20.777652+00	2019-10-25 05:33:20.777659+00	2019-10-25 05:33:20.777666+00	\N	4	4	240	2
270	2019-10-25 05:33:20.7777+00	2019-10-25 05:33:20.777707+00	2019-10-25 05:33:20.777714+00	\N	4	4	241	2
271	2019-10-25 05:33:20.777747+00	2019-10-25 05:33:20.777754+00	2019-10-25 05:33:20.777762+00	\N	4	4	242	2
272	2019-10-25 05:33:20.777794+00	2019-10-25 05:33:20.777802+00	2019-10-25 05:33:20.777809+00	\N	4	4	243	2
273	2019-10-25 05:33:20.777942+00	2019-10-25 05:33:20.777951+00	2019-10-25 05:33:20.777959+00	\N	4	4	244	2
274	2019-10-25 05:33:20.777991+00	2019-10-25 05:33:20.777999+00	2019-10-25 05:33:20.778006+00	\N	4	4	245	2
275	2019-10-25 05:33:20.778039+00	2019-10-25 05:33:20.778047+00	2019-10-25 05:33:20.778053+00	\N	4	4	246	2
276	2019-10-25 05:33:20.778086+00	2019-10-25 05:33:20.778094+00	2019-10-25 05:33:20.778101+00	\N	4	4	247	2
277	2019-10-25 05:33:20.778133+00	2019-10-25 05:33:20.778141+00	2019-10-25 05:33:20.778148+00	\N	4	4	248	2
278	2019-10-25 05:33:20.77818+00	2019-10-25 05:33:20.778188+00	2019-10-25 05:33:20.778194+00	\N	4	4	249	2
279	2019-10-25 05:33:20.778227+00	2019-10-25 05:33:20.778234+00	2019-10-25 05:33:20.778241+00	\N	4	4	250	2
280	2019-10-25 05:33:20.778274+00	2019-10-25 05:33:20.778281+00	2019-10-25 05:33:20.778288+00	\N	4	4	251	2
281	2019-10-25 05:33:20.778321+00	2019-10-25 05:33:20.778328+00	2019-10-25 05:33:20.778335+00	\N	4	4	252	2
282	2019-10-25 05:33:20.778367+00	2019-10-25 05:33:20.778375+00	2019-10-25 05:33:20.778382+00	\N	4	4	253	2
283	2019-10-25 05:33:20.778414+00	2019-10-25 05:33:20.778422+00	2019-10-25 05:33:20.778429+00	\N	4	4	254	2
284	2019-10-25 05:33:20.778462+00	2019-10-25 05:33:20.77847+00	2019-10-25 05:33:20.778477+00	\N	4	4	255	2
453	2019-11-01 04:33:38.239538+00	2019-11-01 04:33:38.239543+00	2019-11-01 04:33:38.219486+00	\N	4	4	292	4
454	2019-11-01 04:33:38.239578+00	2019-11-01 04:33:38.239584+00	2019-11-01 04:33:38.219486+00	\N	4	4	293	4
455	2019-11-01 04:33:38.239619+00	2019-11-01 04:33:38.239624+00	2019-11-01 04:33:38.219486+00	\N	4	4	294	4
456	2019-11-01 04:33:38.239659+00	2019-11-01 04:33:38.239665+00	2019-11-01 04:33:38.219486+00	\N	4	4	295	4
457	2019-11-01 04:33:38.2397+00	2019-11-01 04:33:38.239705+00	2019-11-01 04:33:38.219486+00	\N	4	4	296	4
458	2019-11-01 04:33:38.239739+00	2019-11-01 04:33:38.239745+00	2019-11-01 04:33:38.219486+00	\N	4	4	297	4
459	2019-11-01 04:33:38.23978+00	2019-11-01 04:33:38.239785+00	2019-11-01 04:33:38.219486+00	\N	4	4	298	4
460	2019-11-01 04:33:38.239819+00	2019-11-01 04:33:38.239825+00	2019-11-01 04:33:38.219486+00	\N	4	4	299	4
461	2019-11-01 04:33:38.23986+00	2019-11-01 04:33:38.239865+00	2019-11-01 04:33:38.219486+00	\N	4	4	300	4
462	2019-11-01 04:33:38.2399+00	2019-11-01 04:33:38.239905+00	2019-11-01 04:33:38.219486+00	\N	4	4	301	4
463	2019-11-01 04:33:38.23994+00	2019-11-01 04:33:38.239946+00	2019-11-01 04:33:38.219486+00	\N	4	4	302	4
464	2019-11-01 04:33:38.239981+00	2019-11-01 04:33:38.239986+00	2019-11-01 04:33:38.219486+00	\N	4	4	303	4
465	2019-11-01 04:33:38.240021+00	2019-11-01 04:33:38.240026+00	2019-11-01 04:33:38.219486+00	\N	4	4	304	4
466	2019-11-01 04:33:38.240061+00	2019-11-01 04:33:38.240067+00	2019-11-01 04:33:38.219486+00	\N	4	4	305	4
467	2019-11-01 04:33:38.240102+00	2019-11-01 04:33:38.240107+00	2019-11-01 04:33:38.219486+00	\N	4	4	306	4
468	2019-11-01 04:33:38.240142+00	2019-11-01 04:33:38.240147+00	2019-11-01 04:33:38.219486+00	\N	4	4	307	4
469	2019-11-01 04:33:38.240182+00	2019-11-01 04:33:38.240188+00	2019-11-01 04:33:38.219486+00	\N	4	4	308	4
470	2019-11-01 04:33:38.240222+00	2019-11-01 04:33:38.240228+00	2019-11-01 04:33:38.219486+00	\N	4	4	309	4
471	2019-11-01 04:33:38.240263+00	2019-11-01 04:33:38.240268+00	2019-11-01 04:33:38.219486+00	\N	4	4	310	4
472	2019-11-01 04:33:38.240303+00	2019-11-01 04:33:38.240308+00	2019-11-01 04:33:38.219486+00	\N	4	4	311	4
473	2019-11-01 04:33:38.240343+00	2019-11-01 04:33:38.240349+00	2019-11-01 04:33:38.219486+00	\N	4	4	312	4
474	2019-11-01 04:33:38.240384+00	2019-11-01 04:33:38.240389+00	2019-11-01 04:33:38.219486+00	\N	4	4	313	4
475	2019-11-01 04:33:38.240424+00	2019-11-01 04:33:38.24043+00	2019-11-01 04:33:38.219486+00	\N	4	4	314	4
476	2019-11-01 04:33:38.240465+00	2019-11-01 04:33:38.240471+00	2019-11-01 04:33:38.219486+00	\N	4	4	315	4
477	2019-11-01 04:33:38.240506+00	2019-11-01 04:33:38.240512+00	2019-11-01 04:33:38.219486+00	\N	4	4	316	4
478	2019-11-01 04:33:38.240547+00	2019-11-01 04:33:38.240552+00	2019-11-01 04:33:38.219486+00	\N	4	4	317	4
479	2019-11-01 04:33:38.240587+00	2019-11-01 04:33:38.240592+00	2019-11-01 04:33:38.219486+00	\N	4	4	318	4
480	2019-11-01 04:33:38.240628+00	2019-11-01 04:33:38.240633+00	2019-11-01 04:33:38.219486+00	\N	4	4	319	4
481	2019-11-01 04:33:38.305265+00	2019-11-01 04:33:38.30529+00	2019-11-01 04:33:38.299336+00	\N	4	4	256	4
482	2019-11-01 04:33:38.30535+00	2019-11-01 04:33:38.305356+00	2019-11-01 04:33:38.299336+00	\N	4	4	257	4
483	2019-11-01 04:33:38.305394+00	2019-11-01 04:33:38.305399+00	2019-11-01 04:33:38.299336+00	\N	4	4	258	4
484	2019-11-01 04:33:38.30544+00	2019-11-01 04:33:38.305445+00	2019-11-01 04:33:38.299336+00	\N	4	4	259	4
485	2019-11-01 04:33:38.305481+00	2019-11-01 04:33:38.305486+00	2019-11-01 04:33:38.299336+00	\N	4	4	260	4
486	2019-11-01 04:33:38.305522+00	2019-11-01 04:33:38.305527+00	2019-11-01 04:33:38.299336+00	\N	4	4	261	4
487	2019-11-01 04:33:38.305563+00	2019-11-01 04:33:38.305569+00	2019-11-01 04:33:38.299336+00	\N	4	4	262	4
488	2019-11-01 04:33:38.305628+00	2019-11-01 04:33:38.305635+00	2019-11-01 04:33:38.299336+00	\N	4	4	263	4
489	2019-11-01 04:33:38.30567+00	2019-11-01 04:33:38.305676+00	2019-11-01 04:33:38.299336+00	\N	4	4	264	4
490	2019-11-01 04:33:38.305711+00	2019-11-01 04:33:38.305717+00	2019-11-01 04:33:38.299336+00	\N	4	4	265	4
491	2019-11-01 04:33:38.305752+00	2019-11-01 04:33:38.305757+00	2019-11-01 04:33:38.299336+00	\N	4	4	266	4
492	2019-11-01 04:33:38.305793+00	2019-11-01 04:33:38.305798+00	2019-11-01 04:33:38.299336+00	\N	4	4	267	4
493	2019-11-01 04:33:38.305833+00	2019-11-01 04:33:38.305838+00	2019-11-01 04:33:38.299336+00	\N	4	4	268	4
494	2019-11-01 04:33:38.305873+00	2019-11-01 04:33:38.305878+00	2019-11-01 04:33:38.299336+00	\N	4	4	269	4
495	2019-11-01 04:33:38.305913+00	2019-11-01 04:33:38.305919+00	2019-11-01 04:33:38.299336+00	\N	4	4	270	4
496	2019-11-01 04:33:38.305954+00	2019-11-01 04:33:38.30596+00	2019-11-01 04:33:38.299336+00	\N	4	4	271	4
497	2019-11-01 04:33:38.305995+00	2019-11-01 04:33:38.306+00	2019-11-01 04:33:38.299336+00	\N	4	4	272	4
498	2019-11-01 04:33:38.306035+00	2019-11-01 04:33:38.306041+00	2019-11-01 04:33:38.299336+00	\N	4	4	273	4
499	2019-11-01 04:33:38.306094+00	2019-11-01 04:33:38.3061+00	2019-11-01 04:33:38.299336+00	\N	4	4	274	4
500	2019-11-01 04:33:38.306136+00	2019-11-01 04:33:38.306141+00	2019-11-01 04:33:38.299336+00	\N	4	4	275	4
501	2019-11-01 04:33:38.306176+00	2019-11-01 04:33:38.306181+00	2019-11-01 04:33:38.299336+00	\N	4	4	276	4
502	2019-11-01 04:33:38.306216+00	2019-11-01 04:33:38.306221+00	2019-11-01 04:33:38.299336+00	\N	4	4	277	4
503	2019-11-01 04:33:38.306256+00	2019-11-01 04:33:38.306261+00	2019-11-01 04:33:38.299336+00	\N	4	4	278	4
504	2019-11-01 04:33:38.306296+00	2019-11-01 04:33:38.306302+00	2019-11-01 04:33:38.299336+00	\N	4	4	279	4
505	2019-11-01 04:33:38.306341+00	2019-11-01 04:33:38.306346+00	2019-11-01 04:33:38.299336+00	\N	4	4	280	4
506	2019-11-01 04:33:38.306381+00	2019-11-01 04:33:38.306386+00	2019-11-01 04:33:38.299336+00	\N	4	4	281	4
507	2019-11-01 04:33:38.306422+00	2019-11-01 04:33:38.306427+00	2019-11-01 04:33:38.299336+00	\N	4	4	282	4
508	2019-11-01 04:33:38.306462+00	2019-11-01 04:33:38.306468+00	2019-11-01 04:33:38.299336+00	\N	4	4	283	4
509	2019-11-01 04:33:38.306512+00	2019-11-01 04:33:38.306517+00	2019-11-01 04:33:38.299336+00	\N	4	4	284	4
510	2019-11-01 04:33:38.306552+00	2019-11-01 04:33:38.306557+00	2019-11-01 04:33:38.299336+00	\N	4	4	285	4
511	2019-11-01 04:33:38.306593+00	2019-11-01 04:33:38.306598+00	2019-11-01 04:33:38.299336+00	\N	4	4	286	4
512	2019-11-01 04:33:38.306633+00	2019-11-01 04:33:38.306638+00	2019-11-01 04:33:38.299336+00	\N	4	4	287	4
513	2019-11-01 04:33:38.306673+00	2019-11-01 04:33:38.306679+00	2019-11-01 04:33:38.299336+00	\N	4	4	288	4
514	2019-11-01 04:33:38.306714+00	2019-11-01 04:33:38.306719+00	2019-11-01 04:33:38.299336+00	\N	4	4	289	4
515	2019-11-01 04:33:38.306755+00	2019-11-01 04:33:38.306761+00	2019-11-01 04:33:38.299336+00	\N	4	4	290	4
516	2019-11-01 04:33:38.306797+00	2019-11-01 04:33:38.306804+00	2019-11-01 04:33:38.299336+00	\N	4	4	291	4
517	2019-11-01 04:33:38.306849+00	2019-11-01 04:33:38.306856+00	2019-11-01 04:33:38.299336+00	\N	4	4	292	4
518	2019-11-01 04:33:38.306899+00	2019-11-01 04:33:38.306905+00	2019-11-01 04:33:38.299336+00	\N	4	4	293	4
519	2019-11-01 04:33:38.306947+00	2019-11-01 04:33:38.306954+00	2019-11-01 04:33:38.299336+00	\N	4	4	294	4
520	2019-11-01 04:33:38.306996+00	2019-11-01 04:33:38.307002+00	2019-11-01 04:33:38.299336+00	\N	4	4	295	4
521	2019-11-01 04:33:38.307044+00	2019-11-01 04:33:38.307051+00	2019-11-01 04:33:38.299336+00	\N	4	4	296	4
522	2019-11-01 04:33:38.307092+00	2019-11-01 04:33:38.307098+00	2019-11-01 04:33:38.299336+00	\N	4	4	297	4
523	2019-11-01 04:33:38.30714+00	2019-11-01 04:33:38.307146+00	2019-11-01 04:33:38.299336+00	\N	4	4	298	4
524	2019-11-01 04:33:38.307188+00	2019-11-01 04:33:38.307195+00	2019-11-01 04:33:38.299336+00	\N	4	4	299	4
525	2019-11-01 04:33:38.307236+00	2019-11-01 04:33:38.307243+00	2019-11-01 04:33:38.299336+00	\N	4	4	300	4
526	2019-11-01 04:33:38.307284+00	2019-11-01 04:33:38.307291+00	2019-11-01 04:33:38.299336+00	\N	4	4	301	4
527	2019-11-01 04:33:38.307332+00	2019-11-01 04:33:38.307339+00	2019-11-01 04:33:38.299336+00	\N	4	4	302	4
528	2019-11-01 04:33:38.307381+00	2019-11-01 04:33:38.307387+00	2019-11-01 04:33:38.299336+00	\N	4	4	303	4
529	2019-11-01 04:33:38.307429+00	2019-11-01 04:33:38.307436+00	2019-11-01 04:33:38.299336+00	\N	4	4	304	4
530	2019-11-01 04:33:38.307478+00	2019-11-01 04:33:38.307484+00	2019-11-01 04:33:38.299336+00	\N	4	4	305	4
531	2019-11-01 04:33:38.307525+00	2019-11-01 04:33:38.307532+00	2019-11-01 04:33:38.299336+00	\N	4	4	306	4
532	2019-11-01 04:33:38.307568+00	2019-11-01 04:33:38.307573+00	2019-11-01 04:33:38.299336+00	\N	4	4	307	4
533	2019-11-01 04:33:38.307609+00	2019-11-01 04:33:38.307614+00	2019-11-01 04:33:38.299336+00	\N	4	4	308	4
534	2019-11-01 04:33:38.30765+00	2019-11-01 04:33:38.307656+00	2019-11-01 04:33:38.299336+00	\N	4	4	309	4
535	2019-11-01 04:33:38.307691+00	2019-11-01 04:33:38.307696+00	2019-11-01 04:33:38.299336+00	\N	4	4	310	4
536	2019-11-01 04:33:38.307732+00	2019-11-01 04:33:38.307737+00	2019-11-01 04:33:38.299336+00	\N	4	4	311	4
537	2019-11-01 04:33:38.307773+00	2019-11-01 04:33:38.307778+00	2019-11-01 04:33:38.299336+00	\N	4	4	312	4
538	2019-11-01 04:33:38.307813+00	2019-11-01 04:33:38.307819+00	2019-11-01 04:33:38.299336+00	\N	4	4	313	4
539	2019-11-01 04:33:38.307854+00	2019-11-01 04:33:38.307859+00	2019-11-01 04:33:38.299336+00	\N	4	4	314	4
540	2019-11-01 04:33:38.307896+00	2019-11-01 04:33:38.307901+00	2019-11-01 04:33:38.299336+00	\N	4	4	315	4
541	2019-11-01 04:33:38.307936+00	2019-11-01 04:33:38.307941+00	2019-11-01 04:33:38.299336+00	\N	4	4	316	4
542	2019-11-01 04:33:38.307977+00	2019-11-01 04:33:38.307983+00	2019-11-01 04:33:38.299336+00	\N	4	4	317	4
543	2019-11-01 04:33:38.308018+00	2019-11-01 04:33:38.308024+00	2019-11-01 04:33:38.299336+00	\N	4	4	318	4
544	2019-11-01 04:33:38.308059+00	2019-11-01 04:33:38.308065+00	2019-11-01 04:33:38.299336+00	\N	4	4	319	4
545	2019-11-09 03:32:56.825488+00	2019-11-09 03:32:56.825507+00	2019-11-09 03:32:56.808263+00	\N	4	4	320	5
546	2019-11-09 03:32:56.825567+00	2019-11-09 03:32:56.825575+00	2019-11-09 03:32:56.808263+00	\N	4	4	321	5
547	2019-11-09 03:32:56.825618+00	2019-11-09 03:32:56.825624+00	2019-11-09 03:32:56.808263+00	\N	4	4	322	5
548	2019-11-09 03:32:56.825666+00	2019-11-09 03:32:56.825672+00	2019-11-09 03:32:56.808263+00	\N	4	4	323	5
549	2019-11-09 03:32:56.825708+00	2019-11-09 03:32:56.825714+00	2019-11-09 03:32:56.808263+00	\N	4	4	324	5
550	2019-11-09 03:32:56.825749+00	2019-11-09 03:32:56.825754+00	2019-11-09 03:32:56.808263+00	\N	4	4	325	5
551	2019-11-09 03:32:56.825789+00	2019-11-09 03:32:56.825794+00	2019-11-09 03:32:56.808263+00	\N	4	4	326	5
552	2019-11-09 03:32:56.825829+00	2019-11-09 03:32:56.825834+00	2019-11-09 03:32:56.808263+00	\N	4	4	327	5
553	2019-11-09 03:32:56.825869+00	2019-11-09 03:32:56.825874+00	2019-11-09 03:32:56.808263+00	\N	4	4	328	5
554	2019-11-09 03:32:56.825909+00	2019-11-09 03:32:56.825914+00	2019-11-09 03:32:56.808263+00	\N	4	4	329	5
555	2019-11-09 03:32:56.825949+00	2019-11-09 03:32:56.825954+00	2019-11-09 03:32:56.808263+00	\N	4	4	330	5
556	2019-11-09 03:32:56.825989+00	2019-11-09 03:32:56.825994+00	2019-11-09 03:32:56.808263+00	\N	4	4	331	5
557	2019-11-09 03:32:56.826029+00	2019-11-09 03:32:56.826034+00	2019-11-09 03:32:56.808263+00	\N	4	4	332	5
558	2019-11-09 03:32:56.826069+00	2019-11-09 03:32:56.826074+00	2019-11-09 03:32:56.808263+00	\N	4	4	333	5
559	2019-11-09 03:32:56.826109+00	2019-11-09 03:32:56.826114+00	2019-11-09 03:32:56.808263+00	\N	4	4	334	5
560	2019-11-09 03:32:56.82615+00	2019-11-09 03:32:56.826155+00	2019-11-09 03:32:56.808263+00	\N	4	4	335	5
561	2019-11-09 03:32:56.826191+00	2019-11-09 03:32:56.826196+00	2019-11-09 03:32:56.808263+00	\N	4	4	336	5
562	2019-11-09 03:32:56.826231+00	2019-11-09 03:32:56.826236+00	2019-11-09 03:32:56.808263+00	\N	4	4	337	5
563	2019-11-09 03:32:56.826271+00	2019-11-09 03:32:56.826276+00	2019-11-09 03:32:56.808263+00	\N	4	4	338	5
564	2019-11-09 03:32:56.826311+00	2019-11-09 03:32:56.826316+00	2019-11-09 03:32:56.808263+00	\N	4	4	339	5
565	2019-11-09 03:32:56.82635+00	2019-11-09 03:32:56.826356+00	2019-11-09 03:32:56.808263+00	\N	4	4	340	5
566	2019-11-09 03:32:56.826391+00	2019-11-09 03:32:56.826396+00	2019-11-09 03:32:56.808263+00	\N	4	4	341	5
567	2019-11-09 03:32:56.826431+00	2019-11-09 03:32:56.826436+00	2019-11-09 03:32:56.808263+00	\N	4	4	342	5
568	2019-11-09 03:32:56.82647+00	2019-11-09 03:32:56.826475+00	2019-11-09 03:32:56.808263+00	\N	4	4	343	5
569	2019-11-09 03:32:56.82651+00	2019-11-09 03:32:56.826516+00	2019-11-09 03:32:56.808263+00	\N	4	4	344	5
570	2019-11-09 03:32:56.82655+00	2019-11-09 03:32:56.826555+00	2019-11-09 03:32:56.808263+00	\N	4	4	345	5
571	2019-11-09 03:32:56.82659+00	2019-11-09 03:32:56.826596+00	2019-11-09 03:32:56.808263+00	\N	4	4	346	5
572	2019-11-09 03:32:56.82663+00	2019-11-09 03:32:56.826635+00	2019-11-09 03:32:56.808263+00	\N	4	4	347	5
573	2019-11-09 03:32:56.82667+00	2019-11-09 03:32:56.826675+00	2019-11-09 03:32:56.808263+00	\N	4	4	348	5
574	2019-11-09 03:32:56.82671+00	2019-11-09 03:32:56.826715+00	2019-11-09 03:32:56.808263+00	\N	4	4	349	5
575	2019-11-09 03:32:56.82675+00	2019-11-09 03:32:56.826755+00	2019-11-09 03:32:56.808263+00	\N	4	4	350	5
576	2019-11-09 03:32:56.82679+00	2019-11-09 03:32:56.826795+00	2019-11-09 03:32:56.808263+00	\N	4	4	351	5
577	2019-11-09 03:32:56.82683+00	2019-11-09 03:32:56.826835+00	2019-11-09 03:32:56.808263+00	\N	4	4	352	5
578	2019-11-09 03:32:56.82687+00	2019-11-09 03:32:56.826875+00	2019-11-09 03:32:56.808263+00	\N	4	4	353	5
579	2019-11-09 03:32:56.82691+00	2019-11-09 03:32:56.826915+00	2019-11-09 03:32:56.808263+00	\N	4	4	354	5
580	2019-11-09 03:32:56.82695+00	2019-11-09 03:32:56.826955+00	2019-11-09 03:32:56.808263+00	\N	4	4	355	5
581	2019-11-09 03:32:56.82699+00	2019-11-09 03:32:56.826995+00	2019-11-09 03:32:56.808263+00	\N	4	4	356	5
582	2019-11-09 03:32:56.82703+00	2019-11-09 03:32:56.827035+00	2019-11-09 03:32:56.808263+00	\N	4	4	357	5
583	2019-11-09 03:32:56.827069+00	2019-11-09 03:32:56.827075+00	2019-11-09 03:32:56.808263+00	\N	4	4	358	5
584	2019-11-09 03:32:56.827109+00	2019-11-09 03:32:56.827115+00	2019-11-09 03:32:56.808263+00	\N	4	4	359	5
585	2019-11-09 03:32:56.827149+00	2019-11-09 03:32:56.827155+00	2019-11-09 03:32:56.808263+00	\N	4	4	360	5
586	2019-11-09 03:32:56.82719+00	2019-11-09 03:32:56.827195+00	2019-11-09 03:32:56.808263+00	\N	4	4	361	5
587	2019-11-09 03:32:56.827244+00	2019-11-09 03:32:56.827251+00	2019-11-09 03:32:56.808263+00	\N	4	4	362	5
588	2019-11-09 03:32:56.827286+00	2019-11-09 03:32:56.827291+00	2019-11-09 03:32:56.808263+00	\N	4	4	363	5
589	2019-11-09 03:32:56.827338+00	2019-11-09 03:32:56.827344+00	2019-11-09 03:32:56.808263+00	\N	4	4	364	5
590	2019-11-09 03:32:56.827379+00	2019-11-09 03:32:56.827384+00	2019-11-09 03:32:56.808263+00	\N	4	4	365	5
591	2019-11-09 03:32:56.827419+00	2019-11-09 03:32:56.827425+00	2019-11-09 03:32:56.808263+00	\N	4	4	366	5
592	2019-11-09 03:32:56.82746+00	2019-11-09 03:32:56.827465+00	2019-11-09 03:32:56.808263+00	\N	4	4	367	5
593	2019-11-09 03:32:56.8275+00	2019-11-09 03:32:56.827505+00	2019-11-09 03:32:56.808263+00	\N	4	4	368	5
594	2019-11-09 03:32:56.82754+00	2019-11-09 03:32:56.827545+00	2019-11-09 03:32:56.808263+00	\N	4	4	369	5
595	2019-11-09 03:32:56.82758+00	2019-11-09 03:32:56.827585+00	2019-11-09 03:32:56.808263+00	\N	4	4	370	5
596	2019-11-09 03:32:56.82762+00	2019-11-09 03:32:56.827625+00	2019-11-09 03:32:56.808263+00	\N	4	4	371	5
597	2019-11-09 03:32:56.82766+00	2019-11-09 03:32:56.827665+00	2019-11-09 03:32:56.808263+00	\N	4	4	372	5
598	2019-11-09 03:32:56.8277+00	2019-11-09 03:32:56.827705+00	2019-11-09 03:32:56.808263+00	\N	4	4	373	5
599	2019-11-09 03:32:56.827739+00	2019-11-09 03:32:56.827745+00	2019-11-09 03:32:56.808263+00	\N	4	4	374	5
600	2019-11-09 03:32:56.870578+00	2019-11-09 03:32:56.870598+00	2019-11-09 03:32:56.866118+00	\N	4	4	320	5
601	2019-11-09 03:32:56.870652+00	2019-11-09 03:32:56.870658+00	2019-11-09 03:32:56.866118+00	\N	4	4	321	5
602	2019-11-09 03:32:56.870694+00	2019-11-09 03:32:56.870699+00	2019-11-09 03:32:56.866118+00	\N	4	4	322	5
603	2019-11-09 03:32:56.870735+00	2019-11-09 03:32:56.87074+00	2019-11-09 03:32:56.866118+00	\N	4	4	323	5
604	2019-11-09 03:32:56.870775+00	2019-11-09 03:32:56.87078+00	2019-11-09 03:32:56.866118+00	\N	4	4	324	5
605	2019-11-09 03:32:56.870815+00	2019-11-09 03:32:56.870821+00	2019-11-09 03:32:56.866118+00	\N	4	4	325	5
606	2019-11-09 03:32:56.870856+00	2019-11-09 03:32:56.870862+00	2019-11-09 03:32:56.866118+00	\N	4	4	326	5
607	2019-11-09 03:32:56.870897+00	2019-11-09 03:32:56.870902+00	2019-11-09 03:32:56.866118+00	\N	4	4	327	5
608	2019-11-09 03:32:56.870936+00	2019-11-09 03:32:56.870942+00	2019-11-09 03:32:56.866118+00	\N	4	4	328	5
609	2019-11-09 03:32:56.870976+00	2019-11-09 03:32:56.870982+00	2019-11-09 03:32:56.866118+00	\N	4	4	329	5
610	2019-11-09 03:32:56.871017+00	2019-11-09 03:32:56.871022+00	2019-11-09 03:32:56.866118+00	\N	4	4	330	5
611	2019-11-09 03:32:56.871056+00	2019-11-09 03:32:56.871062+00	2019-11-09 03:32:56.866118+00	\N	4	4	331	5
612	2019-11-09 03:32:56.871096+00	2019-11-09 03:32:56.871102+00	2019-11-09 03:32:56.866118+00	\N	4	4	332	5
613	2019-11-09 03:32:56.871136+00	2019-11-09 03:32:56.871142+00	2019-11-09 03:32:56.866118+00	\N	4	4	333	5
614	2019-11-09 03:32:56.871176+00	2019-11-09 03:32:56.871182+00	2019-11-09 03:32:56.866118+00	\N	4	4	334	5
615	2019-11-09 03:32:56.871216+00	2019-11-09 03:32:56.871221+00	2019-11-09 03:32:56.866118+00	\N	4	4	335	5
616	2019-11-09 03:32:56.871256+00	2019-11-09 03:32:56.871261+00	2019-11-09 03:32:56.866118+00	\N	4	4	336	5
617	2019-11-09 03:32:56.871296+00	2019-11-09 03:32:56.871301+00	2019-11-09 03:32:56.866118+00	\N	4	4	337	5
618	2019-11-09 03:32:56.871348+00	2019-11-09 03:32:56.871354+00	2019-11-09 03:32:56.866118+00	\N	4	4	338	5
619	2019-11-09 03:32:56.871388+00	2019-11-09 03:32:56.871394+00	2019-11-09 03:32:56.866118+00	\N	4	4	339	5
620	2019-11-09 03:32:56.871429+00	2019-11-09 03:32:56.871434+00	2019-11-09 03:32:56.866118+00	\N	4	4	340	5
621	2019-11-09 03:32:56.871469+00	2019-11-09 03:32:56.871474+00	2019-11-09 03:32:56.866118+00	\N	4	4	341	5
622	2019-11-09 03:32:56.871509+00	2019-11-09 03:32:56.871514+00	2019-11-09 03:32:56.866118+00	\N	4	4	342	5
623	2019-11-09 03:32:56.871549+00	2019-11-09 03:32:56.871555+00	2019-11-09 03:32:56.866118+00	\N	4	4	343	5
624	2019-11-09 03:32:56.87159+00	2019-11-09 03:32:56.871595+00	2019-11-09 03:32:56.866118+00	\N	4	4	344	5
625	2019-11-09 03:32:56.87163+00	2019-11-09 03:32:56.871635+00	2019-11-09 03:32:56.866118+00	\N	4	4	345	5
626	2019-11-09 03:32:56.87167+00	2019-11-09 03:32:56.871676+00	2019-11-09 03:32:56.866118+00	\N	4	4	346	5
627	2019-11-09 03:32:56.87171+00	2019-11-09 03:32:56.871716+00	2019-11-09 03:32:56.866118+00	\N	4	4	347	5
628	2019-11-09 03:32:56.87175+00	2019-11-09 03:32:56.871756+00	2019-11-09 03:32:56.866118+00	\N	4	4	348	5
629	2019-11-09 03:32:56.871791+00	2019-11-09 03:32:56.871796+00	2019-11-09 03:32:56.866118+00	\N	4	4	349	5
630	2019-11-09 03:32:56.871831+00	2019-11-09 03:32:56.871837+00	2019-11-09 03:32:56.866118+00	\N	4	4	350	5
631	2019-11-09 03:32:56.871871+00	2019-11-09 03:32:56.871877+00	2019-11-09 03:32:56.866118+00	\N	4	4	351	5
632	2019-11-09 03:32:56.871912+00	2019-11-09 03:32:56.871917+00	2019-11-09 03:32:56.866118+00	\N	4	4	352	5
633	2019-11-09 03:32:56.871952+00	2019-11-09 03:32:56.871957+00	2019-11-09 03:32:56.866118+00	\N	4	4	353	5
634	2019-11-09 03:32:56.871992+00	2019-11-09 03:32:56.871997+00	2019-11-09 03:32:56.866118+00	\N	4	4	354	5
635	2019-11-09 03:32:56.872032+00	2019-11-09 03:32:56.872037+00	2019-11-09 03:32:56.866118+00	\N	4	4	355	5
636	2019-11-09 03:32:56.872072+00	2019-11-09 03:32:56.872078+00	2019-11-09 03:32:56.866118+00	\N	4	4	356	5
637	2019-11-09 03:32:56.872113+00	2019-11-09 03:32:56.872118+00	2019-11-09 03:32:56.866118+00	\N	4	4	357	5
638	2019-11-09 03:32:56.872153+00	2019-11-09 03:32:56.872158+00	2019-11-09 03:32:56.866118+00	\N	4	4	358	5
639	2019-11-09 03:32:56.872193+00	2019-11-09 03:32:56.872199+00	2019-11-09 03:32:56.866118+00	\N	4	4	359	5
640	2019-11-09 03:32:56.872233+00	2019-11-09 03:32:56.872239+00	2019-11-09 03:32:56.866118+00	\N	4	4	360	5
641	2019-11-09 03:32:56.872274+00	2019-11-09 03:32:56.872279+00	2019-11-09 03:32:56.866118+00	\N	4	4	361	5
642	2019-11-09 03:32:56.872314+00	2019-11-09 03:32:56.87232+00	2019-11-09 03:32:56.866118+00	\N	4	4	362	5
643	2019-11-09 03:32:56.872354+00	2019-11-09 03:32:56.87236+00	2019-11-09 03:32:56.866118+00	\N	4	4	363	5
644	2019-11-09 03:32:56.872395+00	2019-11-09 03:32:56.8724+00	2019-11-09 03:32:56.866118+00	\N	4	4	364	5
645	2019-11-09 03:32:56.872435+00	2019-11-09 03:32:56.87244+00	2019-11-09 03:32:56.866118+00	\N	4	4	365	5
646	2019-11-09 03:32:56.872475+00	2019-11-09 03:32:56.87248+00	2019-11-09 03:32:56.866118+00	\N	4	4	366	5
647	2019-11-09 03:32:56.872516+00	2019-11-09 03:32:56.872521+00	2019-11-09 03:32:56.866118+00	\N	4	4	367	5
648	2019-11-09 03:32:56.872556+00	2019-11-09 03:32:56.872562+00	2019-11-09 03:32:56.866118+00	\N	4	4	368	5
649	2019-11-09 03:32:56.872596+00	2019-11-09 03:32:56.872602+00	2019-11-09 03:32:56.866118+00	\N	4	4	369	5
650	2019-11-09 03:32:56.872636+00	2019-11-09 03:32:56.872642+00	2019-11-09 03:32:56.866118+00	\N	4	4	370	5
651	2019-11-09 03:32:56.872676+00	2019-11-09 03:32:56.872682+00	2019-11-09 03:32:56.866118+00	\N	4	4	371	5
652	2019-11-09 03:32:56.872717+00	2019-11-09 03:32:56.872722+00	2019-11-09 03:32:56.866118+00	\N	4	4	372	5
653	2019-11-09 03:32:56.872757+00	2019-11-09 03:32:56.872763+00	2019-11-09 03:32:56.866118+00	\N	4	4	373	5
654	2019-11-09 03:32:56.872797+00	2019-11-09 03:32:56.872803+00	2019-11-09 03:32:56.866118+00	\N	4	4	374	5
\.


--
-- Data for Name: sows_events_sowfarrow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_sowfarrow (id, created_at, modified_at, date, alive_quantity, dead_quantity, mummy_quantity, initiator_id, new_born_piglets_group_id, sow_id, tour_id) FROM stdin;
1	2019-10-29 07:29:08.058147+00	2019-10-29 07:29:08.05819+00	2019-10-29 07:29:08.056801+00	12	0	0	4	1	34	2
2	2019-10-29 07:29:48.875172+00	2019-10-29 07:29:48.875195+00	2019-10-29 07:29:48.874677+00	16	0	0	4	2	50	2
3	2019-10-29 07:30:28.723572+00	2019-10-29 07:30:28.723586+00	2019-10-29 07:30:28.723275+00	12	0	0	4	3	35	2
4	2019-10-29 07:31:06.203356+00	2019-10-29 07:31:06.203372+00	2019-10-29 07:31:06.203038+00	15	0	0	4	4	4	2
5	2019-10-29 07:31:36.880229+00	2019-10-29 07:31:36.880316+00	2019-10-29 07:31:36.879282+00	12	0	0	4	5	37	2
6	2019-10-29 07:32:05.315755+00	2019-10-29 07:32:05.315778+00	2019-10-29 07:32:05.31521+00	12	0	0	4	6	40	2
7	2019-10-29 07:32:27.037048+00	2019-10-29 07:32:27.037063+00	2019-10-29 07:32:27.03675+00	11	0	0	4	7	43	2
8	2019-10-29 07:32:55.957915+00	2019-10-29 07:32:55.957935+00	2019-10-29 07:32:55.956993+00	15	0	0	4	8	21	2
9	2019-10-29 07:33:21.079306+00	2019-10-29 07:33:21.07932+00	2019-10-29 07:33:21.078987+00	12	0	0	4	9	18	2
10	2019-10-29 07:33:46.526207+00	2019-10-29 07:33:46.526221+00	2019-10-29 07:33:46.525932+00	12	0	0	4	10	58	2
11	2019-10-29 07:34:04.460985+00	2019-10-29 07:34:04.461004+00	2019-10-29 07:34:04.460573+00	10	0	0	4	11	64	2
12	2019-10-29 08:14:38.16403+00	2019-10-29 08:14:38.164107+00	2019-10-29 08:14:38.159045+00	13	0	1	4	12	38	2
13	2019-10-29 08:16:17.368592+00	2019-10-29 08:16:17.36861+00	2019-10-29 08:16:17.367646+00	3	0	0	4	13	5	2
14	2019-10-29 08:16:56.730613+00	2019-10-29 08:16:56.730632+00	2019-10-29 08:16:56.7301+00	12	0	0	4	14	28	2
15	2019-10-29 08:17:14.23826+00	2019-10-29 08:17:14.238279+00	2019-10-29 08:17:14.237839+00	1	0	0	4	14	28	2
16	2019-10-29 08:18:07.206872+00	2019-10-29 08:18:07.206894+00	2019-10-29 08:18:07.20486+00	12	0	0	4	15	45	2
17	2019-10-29 08:18:35.14057+00	2019-10-29 08:18:35.140589+00	2019-10-29 08:18:35.140051+00	16	0	0	4	16	3	2
18	2019-10-29 08:19:42.480866+00	2019-10-29 08:19:42.480884+00	2019-10-29 08:19:42.480304+00	12	0	0	4	17	51	2
19	2019-10-29 08:19:57.38587+00	2019-10-29 08:19:57.385887+00	2019-10-29 08:19:57.385496+00	17	0	0	4	18	12	2
20	2019-10-29 08:20:16.565226+00	2019-10-29 08:20:16.56525+00	2019-10-29 08:20:16.56296+00	10	0	0	4	19	23	2
21	2019-10-29 08:20:35.777171+00	2019-10-29 08:20:35.777193+00	2019-10-29 08:20:35.775588+00	13	2	0	4	20	39	2
22	2019-10-29 08:21:15.432431+00	2019-10-29 08:21:15.432557+00	2019-10-29 08:21:15.429933+00	10	0	0	4	21	61	2
23	2019-10-29 08:21:48.670745+00	2019-10-29 08:21:48.670764+00	2019-10-29 08:21:48.669886+00	15	0	0	4	22	16	2
24	2019-10-29 08:22:20.638005+00	2019-10-29 08:22:20.638042+00	2019-10-29 08:22:20.633914+00	12	0	0	4	23	32	2
25	2019-10-29 08:22:33.081492+00	2019-10-29 08:22:33.081515+00	2019-10-29 08:22:33.080862+00	9	2	0	4	24	10	2
26	2019-10-29 08:22:44.989015+00	2019-10-29 08:22:44.989162+00	2019-10-29 08:22:44.9879+00	12	0	0	4	25	33	2
27	2019-10-29 08:23:06.662989+00	2019-10-29 08:23:06.663026+00	2019-10-29 08:23:06.652526+00	12	0	0	4	26	30	2
28	2019-10-29 08:23:24.249819+00	2019-10-29 08:23:24.249851+00	2019-10-29 08:23:24.247316+00	7	9	0	4	27	22	2
29	2019-10-29 08:24:01.575932+00	2019-10-29 08:24:01.575954+00	2019-10-29 08:24:01.575458+00	9	0	0	4	28	27	2
30	2019-10-29 08:24:19.134621+00	2019-10-29 08:24:19.134638+00	2019-10-29 08:24:19.134277+00	12	2	0	4	29	62	2
31	2019-10-29 08:25:01.384312+00	2019-10-29 08:25:01.384333+00	2019-10-29 08:25:01.383235+00	16	0	0	4	2	50	2
32	2019-10-29 08:25:11.443855+00	2019-10-29 08:25:11.443874+00	2019-10-29 08:25:11.443362+00	0	0	0	4	1	34	2
33	2019-10-29 08:25:24.91137+00	2019-10-29 08:25:24.911394+00	2019-10-29 08:25:24.9104+00	12	0	0	4	1	34	2
34	2019-10-29 08:25:41.170286+00	2019-10-29 08:25:41.170302+00	2019-10-29 08:25:41.169995+00	15	0	0	4	30	1	1
35	2019-10-29 08:25:57.298383+00	2019-10-29 08:25:57.298411+00	2019-10-29 08:25:57.296181+00	15	0	0	4	4	4	2
36	2019-10-29 08:26:11.001709+00	2019-10-29 08:26:11.001827+00	2019-10-29 08:26:11.000763+00	12	0	0	4	5	37	2
37	2019-10-29 08:27:03.422305+00	2019-10-29 08:27:03.422337+00	2019-10-29 08:27:03.421579+00	12	0	0	4	6	40	2
38	2019-10-29 08:27:28.200347+00	2019-10-29 08:27:28.200371+00	2019-10-29 08:27:28.199768+00	11	0	0	4	7	43	2
39	2019-10-29 08:28:21.093388+00	2019-10-29 08:28:21.093412+00	2019-10-29 08:28:21.091785+00	12	0	0	4	31	48	2
40	2019-10-29 08:29:13.774622+00	2019-10-29 08:29:13.774636+00	2019-10-29 08:29:13.774342+00	15	0	0	4	8	21	2
41	2019-10-29 08:29:24.195851+00	2019-10-29 08:29:24.195868+00	2019-10-29 08:29:24.195379+00	12	0	0	4	9	18	2
42	2019-10-29 08:30:07.668706+00	2019-10-29 08:30:07.668724+00	2019-10-29 08:30:07.668302+00	11	0	0	4	10	58	2
43	2019-10-29 08:30:27.592626+00	2019-10-29 08:30:27.592643+00	2019-10-29 08:30:27.59217+00	-11	0	0	4	10	58	2
44	2019-10-29 08:30:51.878488+00	2019-10-29 08:30:51.878505+00	2019-10-29 08:30:51.877977+00	10	0	0	4	11	64	2
45	2019-10-29 08:31:18.91062+00	2019-10-29 08:31:18.910643+00	2019-10-29 08:31:18.909968+00	12	0	0	4	3	35	2
46	2019-10-29 08:31:36.734214+00	2019-10-29 08:31:36.734227+00	2019-10-29 08:31:36.733939+00	15	0	0	4	32	42	2
47	2019-10-29 08:32:39.573569+00	2019-10-29 08:32:39.573591+00	2019-10-29 08:32:39.573067+00	12	1	0	4	33	59	2
48	2019-10-29 08:32:57.221659+00	2019-10-29 08:32:57.221675+00	2019-10-29 08:32:57.221312+00	9	0	0	4	34	60	2
49	2019-10-29 08:34:12.322468+00	2019-10-29 08:34:12.322482+00	2019-10-29 08:34:12.322147+00	11	0	0	4	35	14	2
50	2019-10-29 08:37:33.841275+00	2019-10-29 08:37:33.841293+00	2019-10-29 08:37:33.840832+00	10	0	0	4	36	8	2
51	2019-10-29 08:37:54.012467+00	2019-10-29 08:37:54.012544+00	2019-10-29 08:37:54.010576+00	11	0	0	4	37	44	2
52	2019-10-29 08:38:11.858727+00	2019-10-29 08:38:11.858742+00	2019-10-29 08:38:11.858431+00	11	0	0	4	38	15	2
53	2019-10-29 08:38:40.440083+00	2019-10-29 08:38:40.440102+00	2019-10-29 08:38:40.438702+00	15	3	0	4	39	20	2
54	2019-10-29 08:39:01.067444+00	2019-10-29 08:39:01.067475+00	2019-10-29 08:39:01.066065+00	9	5	0	4	40	52	2
55	2019-10-29 08:39:26.290556+00	2019-10-29 08:39:26.290575+00	2019-10-29 08:39:26.290113+00	8	0	0	4	41	24	2
56	2019-10-29 08:39:44.197798+00	2019-10-29 08:39:44.197816+00	2019-10-29 08:39:44.197459+00	14	1	0	4	42	53	2
57	2019-10-29 08:39:58.347967+00	2019-10-29 08:39:58.347982+00	2019-10-29 08:39:58.347658+00	0	0	0	4	43	2	2
58	2019-10-29 08:40:09.937508+00	2019-10-29 08:40:09.937529+00	2019-10-29 08:40:09.936596+00	12	0	0	4	43	2	2
59	2019-10-29 08:40:31.055322+00	2019-10-29 08:40:31.055337+00	2019-10-29 08:40:31.054905+00	15	0	0	4	44	9	2
60	2019-10-29 08:40:44.74709+00	2019-10-29 08:40:44.74711+00	2019-10-29 08:40:44.746648+00	15	0	0	4	45	6	2
61	2019-10-29 08:40:54.137622+00	2019-10-29 08:40:54.137667+00	2019-10-29 08:40:54.133737+00	11	0	0	4	46	7	2
62	2019-10-29 08:41:07.416401+00	2019-10-29 08:41:07.416418+00	2019-10-29 08:41:07.41609+00	8	1	0	4	47	17	2
63	2019-10-29 08:41:22.668982+00	2019-10-29 08:41:22.669003+00	2019-10-29 08:41:22.668457+00	8	0	0	4	48	19	2
64	2019-10-29 08:41:36.781702+00	2019-10-29 08:41:36.78172+00	2019-10-29 08:41:36.781371+00	14	0	0	4	49	56	2
65	2019-11-04 08:46:27.793777+00	2019-11-04 08:46:27.793796+00	2019-11-04 08:46:27.793275+00	12	0	0	9	50	220	2
66	2019-11-04 08:46:39.315868+00	2019-11-04 08:46:39.315893+00	2019-11-04 08:46:39.315402+00	14	0	0	9	51	253	2
67	2019-11-04 08:46:49.769471+00	2019-11-04 08:46:49.769486+00	2019-11-04 08:46:49.769217+00	12	0	0	9	52	198	2
68	2019-11-04 08:47:01.149862+00	2019-11-04 08:47:01.149874+00	2019-11-04 08:47:01.14963+00	12	0	0	9	53	221	2
69	2019-11-04 08:47:14.244002+00	2019-11-04 08:47:14.244015+00	2019-11-04 08:47:14.243745+00	10	0	0	9	54	210	2
70	2019-11-04 08:47:27.211733+00	2019-11-04 08:47:27.211758+00	2019-11-04 08:47:27.211402+00	12	0	0	9	55	207	2
71	2019-11-04 08:47:39.668156+00	2019-11-04 08:47:39.66819+00	2019-11-04 08:47:39.667221+00	14	0	0	9	56	243	2
72	2019-11-04 08:47:53.540354+00	2019-11-04 08:47:53.540368+00	2019-11-04 08:47:53.540104+00	9	0	0	9	57	212	2
73	2019-11-04 08:48:10.42759+00	2019-11-04 08:48:10.427611+00	2019-11-04 08:48:10.426884+00	13	0	0	9	58	245	2
74	2019-11-04 08:48:30.627555+00	2019-11-04 08:48:30.627586+00	2019-11-04 08:48:30.624797+00	14	0	0	9	59	213	2
75	2019-11-04 08:52:44.413988+00	2019-11-04 08:52:44.414005+00	2019-11-04 08:52:44.413627+00	16	0	0	9	60	255	2
76	2019-11-04 08:53:03.161594+00	2019-11-04 08:53:03.161614+00	2019-11-04 08:53:03.16119+00	12	0	0	9	61	204	2
77	2019-11-04 08:53:16.474423+00	2019-11-04 08:53:16.474439+00	2019-11-04 08:53:16.474077+00	5	1	0	9	62	197	2
78	2019-11-04 08:53:29.847909+00	2019-11-04 08:53:29.847924+00	2019-11-04 08:53:29.847603+00	13	0	0	9	63	246	2
79	2019-11-04 08:54:21.662175+00	2019-11-04 08:54:21.66219+00	2019-11-04 08:54:21.661876+00	11	2	0	9	64	252	2
80	2019-11-04 08:54:42.719454+00	2019-11-04 08:54:42.719475+00	2019-11-04 08:54:42.718801+00	5	2	0	9	55	207	2
81	2019-11-04 08:54:56.585358+00	2019-11-04 08:54:56.585375+00	2019-11-04 08:54:56.584968+00	11	0	0	9	65	203	2
82	2019-11-04 08:55:12.56171+00	2019-11-04 08:55:12.561724+00	2019-11-04 08:55:12.561446+00	7	2	0	9	66	229	2
83	2019-11-04 08:55:35.528181+00	2019-11-04 08:55:35.528198+00	2019-11-04 08:55:35.527863+00	12	0	0	9	67	217	2
84	2019-11-04 08:55:49.718078+00	2019-11-04 08:55:49.718091+00	2019-11-04 08:55:49.717821+00	14	0	0	9	68	247	2
85	2019-11-04 08:56:07.857451+00	2019-11-04 08:56:07.857466+00	2019-11-04 08:56:07.857166+00	16	0	0	9	69	216	2
86	2019-11-04 08:56:28.03558+00	2019-11-04 08:56:28.035598+00	2019-11-04 08:56:28.035013+00	10	2	-1	9	70	250	2
87	2019-11-04 08:56:50.535904+00	2019-11-04 08:56:50.535918+00	2019-11-04 08:56:50.535599+00	13	0	0	9	71	224	2
88	2019-11-04 08:57:06.906765+00	2019-11-04 08:57:06.906784+00	2019-11-04 08:57:06.90638+00	11	1	0	9	72	249	2
89	2019-11-04 08:57:22.745966+00	2019-11-04 08:57:22.745983+00	2019-11-04 08:57:22.745631+00	16	0	0	9	73	248	2
90	2019-11-04 08:57:51.068639+00	2019-11-04 08:57:51.068656+00	2019-11-04 08:57:51.068319+00	9	0	1	9	74	227	2
91	2019-11-04 08:58:09.727433+00	2019-11-04 08:58:09.727454+00	2019-11-04 08:58:09.726529+00	8	0	0	9	75	202	2
92	2019-11-04 08:58:24.556017+00	2019-11-04 08:58:24.556032+00	2019-11-04 08:58:24.555683+00	9	0	0	9	76	205	2
93	2019-11-04 08:58:36.812014+00	2019-11-04 08:58:36.812029+00	2019-11-04 08:58:36.811726+00	9	3	0	9	77	199	2
94	2019-11-04 08:58:51.567417+00	2019-11-04 08:58:51.567442+00	2019-11-04 08:58:51.566718+00	13	3	0	9	78	215	2
95	2019-11-04 08:59:06.449555+00	2019-11-04 08:59:06.449578+00	2019-11-04 08:59:06.449015+00	0	0	2	9	78	215	2
96	2019-11-04 08:59:24.645702+00	2019-11-04 08:59:24.645717+00	2019-11-04 08:59:24.645382+00	16	0	0	9	79	222	2
97	2019-11-04 08:59:43.301737+00	2019-11-04 08:59:43.301752+00	2019-11-04 08:59:43.301432+00	11	3	0	9	80	228	2
98	2019-11-04 09:00:05.019459+00	2019-11-04 09:00:05.019482+00	2019-11-04 09:00:05.017824+00	10	6	0	9	81	208	2
99	2019-11-04 09:00:24.594987+00	2019-11-04 09:00:24.595004+00	2019-11-04 09:00:24.594667+00	8	2	0	9	82	209	2
100	2019-11-04 09:00:41.899348+00	2019-11-04 09:00:41.89936+00	2019-11-04 09:00:41.899102+00	18	0	0	9	83	214	2
101	2019-11-04 09:00:57.449258+00	2019-11-04 09:00:57.449274+00	2019-11-04 09:00:57.448764+00	5	1	2	9	84	218	2
102	2019-11-04 09:01:31.724661+00	2019-11-04 09:01:31.724674+00	2019-11-04 09:01:31.724316+00	7	1	0	9	85	235	2
103	2019-11-04 09:02:14.845086+00	2019-11-04 09:02:14.845127+00	2019-11-04 09:02:14.844825+00	6	0	0	9	86	200	2
104	2019-11-04 09:02:27.340418+00	2019-11-04 09:02:27.340442+00	2019-11-04 09:02:27.340071+00	12	0	0	9	87	230	2
105	2019-11-04 09:02:38.340537+00	2019-11-04 09:02:38.340553+00	2019-11-04 09:02:38.340197+00	5	1	0	9	88	211	2
106	2019-11-04 09:02:42.148351+00	2019-11-04 09:02:42.14837+00	2019-11-04 09:02:42.147962+00	10	0	0	4	89	41	2
107	2019-11-04 09:02:56.427743+00	2019-11-04 09:02:56.427764+00	2019-11-04 09:02:56.427171+00	11	0	0	9	90	239	2
108	2019-11-04 09:03:11.890081+00	2019-11-04 09:03:11.890097+00	2019-11-04 09:03:11.889757+00	3	6	0	9	91	273	4
109	2019-11-04 09:03:59.628477+00	2019-11-04 09:03:59.628506+00	2019-11-04 09:03:59.627955+00	12	0	0	9	92	201	2
110	2019-11-04 09:04:18.147847+00	2019-11-04 09:04:18.147875+00	2019-11-04 09:04:18.146965+00	11	1	0	9	93	233	2
111	2019-11-04 09:04:34.401566+00	2019-11-04 09:04:34.401588+00	2019-11-04 09:04:34.401253+00	12	0	0	9	94	219	2
112	2019-11-04 09:04:45.699781+00	2019-11-04 09:04:45.699799+00	2019-11-04 09:04:45.699185+00	10	0	0	9	95	237	2
113	2019-11-04 09:04:48.964934+00	2019-11-04 09:04:48.965001+00	2019-11-04 09:04:48.964234+00	-12	0	0	4	9	18	2
114	2019-11-04 09:05:02.995344+00	2019-11-04 09:05:02.995369+00	2019-11-04 09:05:02.994431+00	13	0	0	9	96	240	2
115	2019-11-04 09:05:18.875954+00	2019-11-04 09:05:18.876028+00	2019-11-04 09:05:18.874246+00	8	0	0	9	97	242	2
116	2019-11-04 09:05:19.778805+00	2019-11-04 09:05:19.778824+00	2019-11-04 09:05:19.778471+00	15	0	0	4	98	47	2
117	2019-11-04 09:05:39.203619+00	2019-11-04 09:05:39.203645+00	2019-11-04 09:05:39.203181+00	-10	0	0	4	11	64	2
118	2019-11-04 09:05:54.610428+00	2019-11-04 09:05:54.610452+00	2019-11-04 09:05:54.609771+00	-12	0	0	4	3	35	2
119	2019-11-04 09:06:21.566344+00	2019-11-04 09:06:21.566363+00	2019-11-04 09:06:21.565648+00	14	0	0	9	99	196	2
120	2019-11-04 09:06:30.80404+00	2019-11-04 09:06:30.804064+00	2019-11-04 09:06:30.802804+00	2	0	0	4	32	42	2
121	2019-11-04 09:06:42.650526+00	2019-11-04 09:06:42.650547+00	2019-11-04 09:06:42.650066+00	5	0	0	9	100	231	2
122	2019-11-04 09:06:49.912283+00	2019-11-04 09:06:49.912316+00	2019-11-04 09:06:49.907633+00	11	0	0	4	101	11	2
123	2019-11-04 09:07:00.351447+00	2019-11-04 09:07:00.351466+00	2019-11-04 09:07:00.350924+00	12	0	0	9	102	254	2
124	2019-11-04 09:07:04.527853+00	2019-11-04 09:07:04.52789+00	2019-11-04 09:07:04.527447+00	16	0	0	4	103	49	2
125	2019-11-04 09:07:10.539951+00	2019-11-04 09:07:10.539964+00	2019-11-04 09:07:10.539714+00	11	0	0	9	104	223	2
126	2019-11-04 09:07:22.14987+00	2019-11-04 09:07:22.149944+00	2019-11-04 09:07:22.149308+00	17	0	0	9	105	195	2
127	2019-11-04 09:07:38.224385+00	2019-11-04 09:07:38.2244+00	2019-11-04 09:07:38.224101+00	12	0	0	9	106	225	2
128	2019-11-04 09:07:48.658593+00	2019-11-04 09:07:48.65861+00	2019-11-04 09:07:48.658309+00	13	0	0	9	107	251	2
129	2019-11-04 09:08:01.609393+00	2019-11-04 09:08:01.609413+00	2019-11-04 09:08:01.608946+00	10	0	0	9	108	244	2
130	2019-11-04 09:08:14.071036+00	2019-11-04 09:08:14.071191+00	2019-11-04 09:08:14.070338+00	12	0	0	9	109	226	2
131	2019-11-04 09:09:56.22487+00	2019-11-04 09:09:56.224886+00	2019-11-04 09:09:56.224523+00	0	1	0	9	33	59	2
132	2019-11-04 09:11:47.790317+00	2019-11-04 09:11:47.790341+00	2019-11-04 09:11:47.79004+00	14	0	0	9	110	25	2
133	2019-11-04 09:12:26.958259+00	2019-11-04 09:12:26.958294+00	2019-11-04 09:12:26.957386+00	12	0	0	4	111	54	2
134	2019-11-04 09:12:50.613551+00	2019-11-04 09:12:50.613565+00	2019-11-04 09:12:50.613262+00	15	0	0	4	112	36	2
135	2019-11-04 09:12:57.484901+00	2019-11-04 09:12:57.484916+00	2019-11-04 09:12:57.484618+00	15	0	0	9	113	26	2
136	2019-11-04 09:13:13.660976+00	2019-11-04 09:13:13.66099+00	2019-11-04 09:13:13.6607+00	14	0	0	9	114	29	2
137	2019-11-04 09:13:16.083094+00	2019-11-04 09:13:16.083116+00	2019-11-04 09:13:16.082331+00	13	0	0	4	115	63	2
138	2019-11-04 09:13:29.589793+00	2019-11-04 09:13:29.58983+00	2019-11-04 09:13:29.589295+00	15	0	0	4	116	13	2
139	2019-11-04 09:13:31.947514+00	2019-11-04 09:13:31.947535+00	2019-11-04 09:13:31.947017+00	10	0	0	9	117	57	2
140	2019-11-04 09:13:42.871049+00	2019-11-04 09:13:42.871069+00	2019-11-04 09:13:42.870605+00	13	0	0	4	118	55	2
141	2019-11-04 09:13:44.648059+00	2019-11-04 09:13:44.648082+00	2019-11-04 09:13:44.647197+00	6	2	0	9	119	31	2
142	2019-11-04 09:14:13.977278+00	2019-11-04 09:14:13.977298+00	2019-11-04 09:14:13.976881+00	9	3	0	4	120	46	2
\.


--
-- Data for Name: sows_events_ultrasound; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_ultrasound (id, created_at, modified_at, date, result, initiator_id, sow_id, tour_id, u_type_id) FROM stdin;
1	2019-10-18 03:44:16.409156+00	2019-10-18 03:44:16.409175+00	2019-10-18 03:44:16.409184+00	t	1	1	1	1
2	2019-10-18 03:44:16.422008+00	2019-10-18 03:44:16.422027+00	2019-10-18 03:44:16.422035+00	t	1	1	1	2
3	2019-10-18 03:51:17.946135+00	2019-10-18 03:51:17.946161+00	2019-10-18 03:51:17.94617+00	t	1	2	2	1
4	2019-10-18 03:51:17.946225+00	2019-10-18 03:51:17.946234+00	2019-10-18 03:51:17.946241+00	t	1	3	2	1
5	2019-10-18 03:51:17.946278+00	2019-10-18 03:51:17.946285+00	2019-10-18 03:51:17.946292+00	t	1	4	2	1
6	2019-10-18 03:51:17.946327+00	2019-10-18 03:51:17.946335+00	2019-10-18 03:51:17.946341+00	t	1	5	2	1
7	2019-10-18 03:51:17.946387+00	2019-10-18 03:51:17.946396+00	2019-10-18 03:51:17.946403+00	t	1	6	2	1
8	2019-10-18 03:51:17.946438+00	2019-10-18 03:51:17.946445+00	2019-10-18 03:51:17.946452+00	t	1	7	2	1
9	2019-10-18 03:51:17.946487+00	2019-10-18 03:51:17.946495+00	2019-10-18 03:51:17.946502+00	t	1	8	2	1
10	2019-10-18 03:51:17.946536+00	2019-10-18 03:51:17.946544+00	2019-10-18 03:51:17.946551+00	t	1	9	2	1
11	2019-10-18 03:51:17.946586+00	2019-10-18 03:51:17.946594+00	2019-10-18 03:51:17.946601+00	t	1	10	2	1
12	2019-10-18 03:51:17.946635+00	2019-10-18 03:51:17.946643+00	2019-10-18 03:51:17.94665+00	t	1	11	2	1
13	2019-10-18 03:51:17.946685+00	2019-10-18 03:51:17.946693+00	2019-10-18 03:51:17.946699+00	t	1	12	2	1
14	2019-10-18 03:51:17.946734+00	2019-10-18 03:51:17.946742+00	2019-10-18 03:51:17.946749+00	t	1	13	2	1
15	2019-10-18 03:51:17.946783+00	2019-10-18 03:51:17.946791+00	2019-10-18 03:51:17.946798+00	t	1	14	2	1
16	2019-10-18 03:51:17.946832+00	2019-10-18 03:51:17.94684+00	2019-10-18 03:51:17.946846+00	t	1	15	2	1
17	2019-10-18 03:51:17.946881+00	2019-10-18 03:51:17.946888+00	2019-10-18 03:51:17.946895+00	t	1	16	2	1
18	2019-10-18 03:51:17.946929+00	2019-10-18 03:51:17.946937+00	2019-10-18 03:51:17.946944+00	t	1	17	2	1
19	2019-10-18 03:51:17.946978+00	2019-10-18 03:51:17.946986+00	2019-10-18 03:51:17.946992+00	t	1	18	2	1
20	2019-10-18 03:51:17.947027+00	2019-10-18 03:51:17.947034+00	2019-10-18 03:51:17.947041+00	t	1	19	2	1
21	2019-10-18 03:51:17.947076+00	2019-10-18 03:51:17.947083+00	2019-10-18 03:51:17.94709+00	t	1	20	2	1
22	2019-10-18 03:51:17.947124+00	2019-10-18 03:51:17.947132+00	2019-10-18 03:51:17.947139+00	t	1	21	2	1
23	2019-10-18 03:51:17.947173+00	2019-10-18 03:51:17.947181+00	2019-10-18 03:51:17.947188+00	t	1	22	2	1
24	2019-10-18 03:51:17.947222+00	2019-10-18 03:51:17.947229+00	2019-10-18 03:51:17.947236+00	t	1	23	2	1
25	2019-10-18 03:51:17.947299+00	2019-10-18 03:51:17.94731+00	2019-10-18 03:51:17.947317+00	t	1	24	2	1
26	2019-10-18 03:51:17.947352+00	2019-10-18 03:51:17.94736+00	2019-10-18 03:51:17.947367+00	t	1	25	2	1
27	2019-10-18 03:51:17.947401+00	2019-10-18 03:51:17.947408+00	2019-10-18 03:51:17.947415+00	t	1	26	2	1
28	2019-10-18 03:51:17.947449+00	2019-10-18 03:51:17.947457+00	2019-10-18 03:51:17.947463+00	t	1	27	2	1
29	2019-10-18 03:51:17.947498+00	2019-10-18 03:51:17.947505+00	2019-10-18 03:51:17.947512+00	t	1	37	2	1
30	2019-10-18 03:51:17.947547+00	2019-10-18 03:51:17.947554+00	2019-10-18 03:51:17.947561+00	t	1	38	2	1
31	2019-10-18 03:51:17.947595+00	2019-10-18 03:51:17.947603+00	2019-10-18 03:51:17.947609+00	t	1	39	2	1
32	2019-10-18 03:51:17.947643+00	2019-10-18 03:51:17.947651+00	2019-10-18 03:51:17.947658+00	t	1	40	2	1
33	2019-10-18 03:51:17.947692+00	2019-10-18 03:51:17.9477+00	2019-10-18 03:51:17.947706+00	t	1	41	2	1
34	2019-10-18 03:51:17.947741+00	2019-10-18 03:51:17.947748+00	2019-10-18 03:51:17.947755+00	t	1	42	2	1
35	2019-10-18 03:51:17.947789+00	2019-10-18 03:51:17.947797+00	2019-10-18 03:51:17.947804+00	t	1	43	2	1
36	2019-10-18 03:51:17.947838+00	2019-10-18 03:51:17.947845+00	2019-10-18 03:51:17.947852+00	t	1	44	2	1
37	2019-10-18 03:51:17.947886+00	2019-10-18 03:51:17.947894+00	2019-10-18 03:51:17.9479+00	t	1	45	2	1
38	2019-10-18 03:51:17.947934+00	2019-10-18 03:51:17.947942+00	2019-10-18 03:51:17.947949+00	t	1	46	2	1
39	2019-10-18 03:51:17.948014+00	2019-10-18 03:51:17.948023+00	2019-10-18 03:51:17.94803+00	t	1	47	2	1
40	2019-10-18 03:51:17.948065+00	2019-10-18 03:51:17.948072+00	2019-10-18 03:51:17.948079+00	t	1	48	2	1
41	2019-10-18 03:51:17.948113+00	2019-10-18 03:51:17.948121+00	2019-10-18 03:51:17.948128+00	t	1	49	2	1
42	2019-10-18 03:51:17.948162+00	2019-10-18 03:51:17.948169+00	2019-10-18 03:51:17.948176+00	t	1	50	2	1
43	2019-10-18 03:51:17.94821+00	2019-10-18 03:51:17.948217+00	2019-10-18 03:51:17.948224+00	t	1	51	2	1
44	2019-10-18 03:51:17.948258+00	2019-10-18 03:51:17.948266+00	2019-10-18 03:51:17.948273+00	t	1	52	2	1
45	2019-10-18 03:51:17.948307+00	2019-10-18 03:51:17.948315+00	2019-10-18 03:51:17.948321+00	t	1	53	2	1
46	2019-10-18 03:51:17.948355+00	2019-10-18 03:51:17.948363+00	2019-10-18 03:51:17.94837+00	t	1	54	2	1
47	2019-10-18 03:51:17.948404+00	2019-10-18 03:51:17.948411+00	2019-10-18 03:51:17.948418+00	t	1	55	2	1
48	2019-10-18 03:51:17.948452+00	2019-10-18 03:51:17.94846+00	2019-10-18 03:51:17.948466+00	t	1	56	2	1
49	2019-10-18 03:51:17.948501+00	2019-10-18 03:51:17.948508+00	2019-10-18 03:51:17.948515+00	t	1	57	2	1
50	2019-10-18 03:51:17.948549+00	2019-10-18 03:51:17.948557+00	2019-10-18 03:51:17.948564+00	t	1	58	2	1
51	2019-10-18 03:51:17.948598+00	2019-10-18 03:51:17.948605+00	2019-10-18 03:51:17.948612+00	t	1	59	2	1
52	2019-10-18 03:51:17.948646+00	2019-10-18 03:51:17.948654+00	2019-10-18 03:51:17.948661+00	t	1	60	2	1
53	2019-10-18 03:51:17.948695+00	2019-10-18 03:51:17.948703+00	2019-10-18 03:51:17.94871+00	t	1	61	2	1
54	2019-10-18 03:51:17.948744+00	2019-10-18 03:51:17.948751+00	2019-10-18 03:51:17.948758+00	t	1	62	2	1
55	2019-10-18 03:51:17.948792+00	2019-10-18 03:51:17.9488+00	2019-10-18 03:51:17.948807+00	t	1	63	2	1
56	2019-10-18 03:51:17.948841+00	2019-10-18 03:51:17.948848+00	2019-10-18 03:51:17.948855+00	t	1	64	2	1
57	2019-10-18 03:51:17.948895+00	2019-10-18 03:51:17.948902+00	2019-10-18 03:51:17.948909+00	t	1	28	2	1
58	2019-10-18 03:51:17.94895+00	2019-10-18 03:51:17.948958+00	2019-10-18 03:51:17.948965+00	t	1	29	2	1
59	2019-10-18 03:51:17.948999+00	2019-10-18 03:51:17.949006+00	2019-10-18 03:51:17.949013+00	t	1	30	2	1
60	2019-10-18 03:51:17.949047+00	2019-10-18 03:51:17.949054+00	2019-10-18 03:51:17.949061+00	t	1	31	2	1
61	2019-10-18 03:51:17.949096+00	2019-10-18 03:51:17.949103+00	2019-10-18 03:51:17.94911+00	t	1	32	2	1
62	2019-10-18 03:51:17.949145+00	2019-10-18 03:51:17.949152+00	2019-10-18 03:51:17.949159+00	t	1	33	2	1
63	2019-10-18 03:51:17.949194+00	2019-10-18 03:51:17.949201+00	2019-10-18 03:51:17.949208+00	t	1	34	2	1
64	2019-10-18 03:51:17.949242+00	2019-10-18 03:51:17.94925+00	2019-10-18 03:51:17.949257+00	t	1	35	2	1
65	2019-10-18 03:51:17.949291+00	2019-10-18 03:51:17.949299+00	2019-10-18 03:51:17.949306+00	t	1	36	2	1
66	2019-10-18 03:51:18.029302+00	2019-10-18 03:51:18.029342+00	2019-10-18 03:51:18.029351+00	t	1	2	2	2
67	2019-10-18 03:51:18.029406+00	2019-10-18 03:51:18.029415+00	2019-10-18 03:51:18.029423+00	t	1	3	2	2
68	2019-10-18 03:51:18.029466+00	2019-10-18 03:51:18.029474+00	2019-10-18 03:51:18.029481+00	t	1	4	2	2
69	2019-10-18 03:51:18.029516+00	2019-10-18 03:51:18.029523+00	2019-10-18 03:51:18.02953+00	t	1	5	2	2
70	2019-10-18 03:51:18.029565+00	2019-10-18 03:51:18.029573+00	2019-10-18 03:51:18.02958+00	t	1	6	2	2
71	2019-10-18 03:51:18.029614+00	2019-10-18 03:51:18.029622+00	2019-10-18 03:51:18.029629+00	t	1	7	2	2
72	2019-10-18 03:51:18.029663+00	2019-10-18 03:51:18.029672+00	2019-10-18 03:51:18.029678+00	t	1	8	2	2
73	2019-10-18 03:51:18.029714+00	2019-10-18 03:51:18.029721+00	2019-10-18 03:51:18.029728+00	t	1	9	2	2
74	2019-10-18 03:51:18.029762+00	2019-10-18 03:51:18.02977+00	2019-10-18 03:51:18.029777+00	t	1	10	2	2
75	2019-10-18 03:51:18.029822+00	2019-10-18 03:51:18.02983+00	2019-10-18 03:51:18.029837+00	t	1	11	2	2
76	2019-10-18 03:51:18.029891+00	2019-10-18 03:51:18.0299+00	2019-10-18 03:51:18.029907+00	t	1	12	2	2
77	2019-10-18 03:51:18.029942+00	2019-10-18 03:51:18.02995+00	2019-10-18 03:51:18.029957+00	t	1	13	2	2
78	2019-10-18 03:51:18.029991+00	2019-10-18 03:51:18.029999+00	2019-10-18 03:51:18.030006+00	t	1	14	2	2
79	2019-10-18 03:51:18.03004+00	2019-10-18 03:51:18.030048+00	2019-10-18 03:51:18.030055+00	t	1	15	2	2
80	2019-10-18 03:51:18.030089+00	2019-10-18 03:51:18.030097+00	2019-10-18 03:51:18.030104+00	t	1	16	2	2
81	2019-10-18 03:51:18.030156+00	2019-10-18 03:51:18.030165+00	2019-10-18 03:51:18.030172+00	t	1	17	2	2
82	2019-10-18 03:51:18.030206+00	2019-10-18 03:51:18.030214+00	2019-10-18 03:51:18.030221+00	t	1	18	2	2
83	2019-10-18 03:51:18.030256+00	2019-10-18 03:51:18.030263+00	2019-10-18 03:51:18.03027+00	t	1	19	2	2
84	2019-10-18 03:51:18.030305+00	2019-10-18 03:51:18.030312+00	2019-10-18 03:51:18.030319+00	t	1	20	2	2
85	2019-10-18 03:51:18.030375+00	2019-10-18 03:51:18.030385+00	2019-10-18 03:51:18.030392+00	t	1	21	2	2
86	2019-10-18 03:51:18.030428+00	2019-10-18 03:51:18.030436+00	2019-10-18 03:51:18.030442+00	t	1	22	2	2
87	2019-10-18 03:51:18.030477+00	2019-10-18 03:51:18.030485+00	2019-10-18 03:51:18.030492+00	t	1	23	2	2
88	2019-10-18 03:51:18.030526+00	2019-10-18 03:51:18.030534+00	2019-10-18 03:51:18.030541+00	t	1	24	2	2
89	2019-10-18 03:51:18.030576+00	2019-10-18 03:51:18.030583+00	2019-10-18 03:51:18.03059+00	t	1	25	2	2
90	2019-10-18 03:51:18.03065+00	2019-10-18 03:51:18.030661+00	2019-10-18 03:51:18.030668+00	t	1	26	2	2
91	2019-10-18 03:51:18.030704+00	2019-10-18 03:51:18.030712+00	2019-10-18 03:51:18.030719+00	t	1	27	2	2
92	2019-10-18 03:51:18.030753+00	2019-10-18 03:51:18.030761+00	2019-10-18 03:51:18.030768+00	t	1	37	2	2
93	2019-10-18 03:51:18.030802+00	2019-10-18 03:51:18.03081+00	2019-10-18 03:51:18.030817+00	t	1	38	2	2
94	2019-10-18 03:51:18.030851+00	2019-10-18 03:51:18.030858+00	2019-10-18 03:51:18.030865+00	t	1	39	2	2
95	2019-10-18 03:51:18.030899+00	2019-10-18 03:51:18.030907+00	2019-10-18 03:51:18.030914+00	t	1	40	2	2
96	2019-10-18 03:51:18.030948+00	2019-10-18 03:51:18.030955+00	2019-10-18 03:51:18.030962+00	t	1	41	2	2
97	2019-10-18 03:51:18.030996+00	2019-10-18 03:51:18.031004+00	2019-10-18 03:51:18.03101+00	t	1	42	2	2
98	2019-10-18 03:51:18.031045+00	2019-10-18 03:51:18.031052+00	2019-10-18 03:51:18.031059+00	t	1	43	2	2
99	2019-10-18 03:51:18.031094+00	2019-10-18 03:51:18.031101+00	2019-10-18 03:51:18.031108+00	t	1	44	2	2
100	2019-10-18 03:51:18.031142+00	2019-10-18 03:51:18.03115+00	2019-10-18 03:51:18.031157+00	t	1	45	2	2
101	2019-10-18 03:51:18.031191+00	2019-10-18 03:51:18.031199+00	2019-10-18 03:51:18.031205+00	t	1	46	2	2
102	2019-10-18 03:51:18.03124+00	2019-10-18 03:51:18.031248+00	2019-10-18 03:51:18.031285+00	t	1	47	2	2
103	2019-10-18 03:51:18.031347+00	2019-10-18 03:51:18.031357+00	2019-10-18 03:51:18.031364+00	t	1	48	2	2
104	2019-10-18 03:51:18.031405+00	2019-10-18 03:51:18.031413+00	2019-10-18 03:51:18.03142+00	t	1	49	2	2
105	2019-10-18 03:51:18.031458+00	2019-10-18 03:51:18.031466+00	2019-10-18 03:51:18.031473+00	t	1	50	2	2
106	2019-10-18 03:51:18.031508+00	2019-10-18 03:51:18.031516+00	2019-10-18 03:51:18.031522+00	t	1	51	2	2
107	2019-10-18 03:51:18.031557+00	2019-10-18 03:51:18.031565+00	2019-10-18 03:51:18.031571+00	t	1	52	2	2
108	2019-10-18 03:51:18.031605+00	2019-10-18 03:51:18.031613+00	2019-10-18 03:51:18.03162+00	t	1	53	2	2
109	2019-10-18 03:51:18.031654+00	2019-10-18 03:51:18.031661+00	2019-10-18 03:51:18.031668+00	t	1	54	2	2
110	2019-10-18 03:51:18.031703+00	2019-10-18 03:51:18.03171+00	2019-10-18 03:51:18.031717+00	t	1	55	2	2
111	2019-10-18 03:51:18.031751+00	2019-10-18 03:51:18.031759+00	2019-10-18 03:51:18.031766+00	t	1	56	2	2
112	2019-10-18 03:51:18.0318+00	2019-10-18 03:51:18.031807+00	2019-10-18 03:51:18.031814+00	t	1	57	2	2
113	2019-10-18 03:51:18.031849+00	2019-10-18 03:51:18.031856+00	2019-10-18 03:51:18.031863+00	t	1	58	2	2
114	2019-10-18 03:51:18.031898+00	2019-10-18 03:51:18.031905+00	2019-10-18 03:51:18.031912+00	t	1	59	2	2
115	2019-10-18 03:51:18.031947+00	2019-10-18 03:51:18.031955+00	2019-10-18 03:51:18.031962+00	t	1	60	2	2
116	2019-10-18 03:51:18.031996+00	2019-10-18 03:51:18.032003+00	2019-10-18 03:51:18.03201+00	t	1	61	2	2
117	2019-10-18 03:51:18.032045+00	2019-10-18 03:51:18.032053+00	2019-10-18 03:51:18.032059+00	t	1	62	2	2
118	2019-10-18 03:51:18.032094+00	2019-10-18 03:51:18.032101+00	2019-10-18 03:51:18.032108+00	t	1	63	2	2
119	2019-10-18 03:51:18.032143+00	2019-10-18 03:51:18.03215+00	2019-10-18 03:51:18.032157+00	t	1	64	2	2
120	2019-10-18 03:51:18.032192+00	2019-10-18 03:51:18.0322+00	2019-10-18 03:51:18.032207+00	t	1	28	2	2
121	2019-10-18 03:51:18.032242+00	2019-10-18 03:51:18.032249+00	2019-10-18 03:51:18.032256+00	t	1	29	2	2
122	2019-10-18 03:51:18.03229+00	2019-10-18 03:51:18.032297+00	2019-10-18 03:51:18.032304+00	t	1	30	2	2
123	2019-10-18 03:51:18.032339+00	2019-10-18 03:51:18.032346+00	2019-10-18 03:51:18.032353+00	t	1	31	2	2
124	2019-10-18 03:51:18.032387+00	2019-10-18 03:51:18.032395+00	2019-10-18 03:51:18.032402+00	t	1	32	2	2
125	2019-10-18 03:51:18.032437+00	2019-10-18 03:51:18.032445+00	2019-10-18 03:51:18.032452+00	t	1	33	2	2
126	2019-10-18 03:51:18.032486+00	2019-10-18 03:51:18.032494+00	2019-10-18 03:51:18.0325+00	t	1	34	2	2
127	2019-10-18 03:51:18.032535+00	2019-10-18 03:51:18.032543+00	2019-10-18 03:51:18.03255+00	t	1	35	2	2
128	2019-10-18 03:51:18.032584+00	2019-10-18 03:51:18.032592+00	2019-10-18 03:51:18.032598+00	t	1	36	2	2
130	2019-10-25 05:24:15.03589+00	2019-10-25 05:24:15.035913+00	2019-10-25 05:24:15.035922+00	t	4	195	2	1
131	2019-10-25 05:24:15.035975+00	2019-10-25 05:24:15.035984+00	2019-10-25 05:24:15.035992+00	t	4	196	2	1
132	2019-10-25 05:24:15.091361+00	2019-10-25 05:24:15.091384+00	2019-10-25 05:24:15.091393+00	t	4	195	2	2
133	2019-10-25 05:24:15.091448+00	2019-10-25 05:24:15.091457+00	2019-10-25 05:24:15.091465+00	t	4	196	2	2
134	2019-10-25 05:33:20.863341+00	2019-10-25 05:33:20.863365+00	2019-10-25 05:33:20.863373+00	t	4	208	2	1
135	2019-10-25 05:33:20.863427+00	2019-10-25 05:33:20.863436+00	2019-10-25 05:33:20.863444+00	t	4	209	2	1
136	2019-10-25 05:33:20.86348+00	2019-10-25 05:33:20.863489+00	2019-10-25 05:33:20.863496+00	t	4	210	2	1
137	2019-10-25 05:33:20.863532+00	2019-10-25 05:33:20.86354+00	2019-10-25 05:33:20.863547+00	t	4	211	2	1
138	2019-10-25 05:33:20.863583+00	2019-10-25 05:33:20.863591+00	2019-10-25 05:33:20.863598+00	t	4	212	2	1
139	2019-10-25 05:33:20.863633+00	2019-10-25 05:33:20.863641+00	2019-10-25 05:33:20.863648+00	t	4	213	2	1
140	2019-10-25 05:33:20.863684+00	2019-10-25 05:33:20.863691+00	2019-10-25 05:33:20.863698+00	t	4	214	2	1
141	2019-10-25 05:33:20.863734+00	2019-10-25 05:33:20.863741+00	2019-10-25 05:33:20.863748+00	t	4	215	2	1
142	2019-10-25 05:33:20.863783+00	2019-10-25 05:33:20.863791+00	2019-10-25 05:33:20.863798+00	t	4	216	2	1
143	2019-10-25 05:33:20.863833+00	2019-10-25 05:33:20.863841+00	2019-10-25 05:33:20.863848+00	t	4	217	2	1
144	2019-10-25 05:33:20.863884+00	2019-10-25 05:33:20.863892+00	2019-10-25 05:33:20.863899+00	t	4	218	2	1
145	2019-10-25 05:33:20.863935+00	2019-10-25 05:33:20.863942+00	2019-10-25 05:33:20.863949+00	t	4	219	2	1
146	2019-10-25 05:33:20.863985+00	2019-10-25 05:33:20.863993+00	2019-10-25 05:33:20.864+00	t	4	220	2	1
147	2019-10-25 05:33:20.864035+00	2019-10-25 05:33:20.864043+00	2019-10-25 05:33:20.86405+00	t	4	197	2	1
148	2019-10-25 05:33:20.864085+00	2019-10-25 05:33:20.864092+00	2019-10-25 05:33:20.864099+00	t	4	198	2	1
149	2019-10-25 05:33:20.864135+00	2019-10-25 05:33:20.864142+00	2019-10-25 05:33:20.864149+00	t	4	199	2	1
150	2019-10-25 05:33:20.864185+00	2019-10-25 05:33:20.864193+00	2019-10-25 05:33:20.864199+00	t	4	200	2	1
151	2019-10-25 05:33:20.864235+00	2019-10-25 05:33:20.864243+00	2019-10-25 05:33:20.86425+00	t	4	201	2	1
152	2019-10-25 05:33:20.864285+00	2019-10-25 05:33:20.864293+00	2019-10-25 05:33:20.8643+00	t	4	202	2	1
153	2019-10-25 05:33:20.864335+00	2019-10-25 05:33:20.864342+00	2019-10-25 05:33:20.864349+00	t	4	203	2	1
154	2019-10-25 05:33:20.864385+00	2019-10-25 05:33:20.864393+00	2019-10-25 05:33:20.864399+00	t	4	204	2	1
155	2019-10-25 05:33:20.864434+00	2019-10-25 05:33:20.864442+00	2019-10-25 05:33:20.864449+00	t	4	205	2	1
156	2019-10-25 05:33:20.864484+00	2019-10-25 05:33:20.864491+00	2019-10-25 05:33:20.864498+00	t	4	206	2	1
157	2019-10-25 05:33:20.864533+00	2019-10-25 05:33:20.864541+00	2019-10-25 05:33:20.864548+00	t	4	207	2	1
158	2019-10-25 05:33:20.864597+00	2019-10-25 05:33:20.864606+00	2019-10-25 05:33:20.864613+00	t	4	221	2	1
159	2019-10-25 05:33:20.864649+00	2019-10-25 05:33:20.864657+00	2019-10-25 05:33:20.864664+00	t	4	222	2	1
160	2019-10-25 05:33:20.8647+00	2019-10-25 05:33:20.864708+00	2019-10-25 05:33:20.864714+00	t	4	223	2	1
161	2019-10-25 05:33:20.86475+00	2019-10-25 05:33:20.864758+00	2019-10-25 05:33:20.864765+00	t	4	224	2	1
162	2019-10-25 05:33:20.8648+00	2019-10-25 05:33:20.864808+00	2019-10-25 05:33:20.864815+00	t	4	225	2	1
163	2019-10-25 05:33:20.86485+00	2019-10-25 05:33:20.864858+00	2019-10-25 05:33:20.864865+00	t	4	226	2	1
164	2019-10-25 05:33:20.8649+00	2019-10-25 05:33:20.864908+00	2019-10-25 05:33:20.864915+00	t	4	227	2	1
165	2019-10-25 05:33:20.864951+00	2019-10-25 05:33:20.864958+00	2019-10-25 05:33:20.864965+00	t	4	228	2	1
166	2019-10-25 05:33:20.865+00	2019-10-25 05:33:20.865008+00	2019-10-25 05:33:20.865015+00	t	4	229	2	1
167	2019-10-25 05:33:20.86505+00	2019-10-25 05:33:20.865058+00	2019-10-25 05:33:20.865065+00	t	4	230	2	1
168	2019-10-25 05:33:20.865132+00	2019-10-25 05:33:20.865143+00	2019-10-25 05:33:20.86515+00	t	4	231	2	1
169	2019-10-25 05:33:20.865187+00	2019-10-25 05:33:20.865195+00	2019-10-25 05:33:20.865202+00	t	4	232	2	1
170	2019-10-25 05:33:20.865238+00	2019-10-25 05:33:20.865245+00	2019-10-25 05:33:20.865252+00	t	4	233	2	1
171	2019-10-25 05:33:20.865287+00	2019-10-25 05:33:20.865295+00	2019-10-25 05:33:20.865302+00	t	4	234	2	1
172	2019-10-25 05:33:20.865336+00	2019-10-25 05:33:20.865344+00	2019-10-25 05:33:20.865351+00	t	4	235	2	1
173	2019-10-25 05:33:20.865386+00	2019-10-25 05:33:20.865394+00	2019-10-25 05:33:20.865401+00	t	4	236	2	1
174	2019-10-25 05:33:20.865436+00	2019-10-25 05:33:20.865444+00	2019-10-25 05:33:20.86545+00	t	4	237	2	1
175	2019-10-25 05:33:20.865485+00	2019-10-25 05:33:20.865493+00	2019-10-25 05:33:20.8655+00	t	4	238	2	1
176	2019-10-25 05:33:20.865535+00	2019-10-25 05:33:20.865542+00	2019-10-25 05:33:20.865549+00	t	4	239	2	1
177	2019-10-25 05:33:20.865585+00	2019-10-25 05:33:20.865592+00	2019-10-25 05:33:20.865599+00	t	4	240	2	1
178	2019-10-25 05:33:20.865635+00	2019-10-25 05:33:20.865642+00	2019-10-25 05:33:20.865649+00	t	4	241	2	1
179	2019-10-25 05:33:20.865685+00	2019-10-25 05:33:20.865692+00	2019-10-25 05:33:20.865699+00	t	4	242	2	1
180	2019-10-25 05:33:20.865734+00	2019-10-25 05:33:20.865742+00	2019-10-25 05:33:20.865749+00	t	4	243	2	1
181	2019-10-25 05:33:20.865785+00	2019-10-25 05:33:20.865792+00	2019-10-25 05:33:20.865799+00	t	4	244	2	1
182	2019-10-25 05:33:20.865834+00	2019-10-25 05:33:20.865842+00	2019-10-25 05:33:20.865849+00	t	4	245	2	1
183	2019-10-25 05:33:20.865884+00	2019-10-25 05:33:20.865892+00	2019-10-25 05:33:20.865899+00	t	4	246	2	1
184	2019-10-25 05:33:20.865934+00	2019-10-25 05:33:20.865941+00	2019-10-25 05:33:20.865948+00	t	4	247	2	1
185	2019-10-25 05:33:20.865983+00	2019-10-25 05:33:20.865991+00	2019-10-25 05:33:20.865998+00	t	4	248	2	1
186	2019-10-25 05:33:20.866033+00	2019-10-25 05:33:20.86604+00	2019-10-25 05:33:20.866047+00	t	4	249	2	1
187	2019-10-25 05:33:20.866083+00	2019-10-25 05:33:20.86609+00	2019-10-25 05:33:20.866097+00	t	4	250	2	1
188	2019-10-25 05:33:20.866133+00	2019-10-25 05:33:20.86614+00	2019-10-25 05:33:20.866147+00	t	4	251	2	1
189	2019-10-25 05:33:20.866183+00	2019-10-25 05:33:20.86619+00	2019-10-25 05:33:20.866197+00	t	4	252	2	1
190	2019-10-25 05:33:20.866233+00	2019-10-25 05:33:20.866241+00	2019-10-25 05:33:20.866247+00	t	4	253	2	1
191	2019-10-25 05:33:20.866283+00	2019-10-25 05:33:20.86629+00	2019-10-25 05:33:20.866297+00	t	4	254	2	1
192	2019-10-25 05:33:20.866333+00	2019-10-25 05:33:20.866341+00	2019-10-25 05:33:20.866347+00	t	4	255	2	1
193	2019-10-25 05:33:20.947975+00	2019-10-25 05:33:20.947998+00	2019-10-25 05:33:20.948007+00	t	4	208	2	2
194	2019-10-25 05:33:20.948061+00	2019-10-25 05:33:20.94807+00	2019-10-25 05:33:20.948077+00	t	4	209	2	2
195	2019-10-25 05:33:20.948114+00	2019-10-25 05:33:20.948122+00	2019-10-25 05:33:20.94813+00	t	4	210	2	2
196	2019-10-25 05:33:20.948166+00	2019-10-25 05:33:20.948174+00	2019-10-25 05:33:20.948181+00	t	4	211	2	2
197	2019-10-25 05:33:20.948217+00	2019-10-25 05:33:20.948225+00	2019-10-25 05:33:20.948232+00	t	4	212	2	2
198	2019-10-25 05:33:20.94833+00	2019-10-25 05:33:20.948338+00	2019-10-25 05:33:20.948345+00	t	4	213	2	2
199	2019-10-25 05:33:20.948381+00	2019-10-25 05:33:20.948389+00	2019-10-25 05:33:20.948397+00	t	4	214	2	2
200	2019-10-25 05:33:20.94848+00	2019-10-25 05:33:20.948493+00	2019-10-25 05:33:20.9485+00	t	4	215	2	2
201	2019-10-25 05:33:20.948539+00	2019-10-25 05:33:20.948547+00	2019-10-25 05:33:20.94856+00	t	4	216	2	2
202	2019-10-25 05:33:20.948892+00	2019-10-25 05:33:20.948904+00	2019-10-25 05:33:20.948912+00	t	4	217	2	2
203	2019-10-25 05:33:20.948949+00	2019-10-25 05:33:20.948957+00	2019-10-25 05:33:20.948964+00	t	4	218	2	2
204	2019-10-25 05:33:20.949+00	2019-10-25 05:33:20.949008+00	2019-10-25 05:33:20.949015+00	t	4	219	2	2
205	2019-10-25 05:33:20.949051+00	2019-10-25 05:33:20.949059+00	2019-10-25 05:33:20.949066+00	t	4	220	2	2
206	2019-10-25 05:33:20.949126+00	2019-10-25 05:33:20.949136+00	2019-10-25 05:33:20.949143+00	t	4	197	2	2
207	2019-10-25 05:33:20.949185+00	2019-10-25 05:33:20.949193+00	2019-10-25 05:33:20.9492+00	t	4	198	2	2
208	2019-10-25 05:33:20.949236+00	2019-10-25 05:33:20.949244+00	2019-10-25 05:33:20.949251+00	t	4	199	2	2
209	2019-10-25 05:33:20.949295+00	2019-10-25 05:33:20.949303+00	2019-10-25 05:33:20.94931+00	t	4	200	2	2
210	2019-10-25 05:33:20.949346+00	2019-10-25 05:33:20.949354+00	2019-10-25 05:33:20.949361+00	t	4	201	2	2
211	2019-10-25 05:33:20.949396+00	2019-10-25 05:33:20.949404+00	2019-10-25 05:33:20.949411+00	t	4	202	2	2
212	2019-10-25 05:33:20.949447+00	2019-10-25 05:33:20.949455+00	2019-10-25 05:33:20.949467+00	t	4	203	2	2
213	2019-10-25 05:33:20.949505+00	2019-10-25 05:33:20.949513+00	2019-10-25 05:33:20.94952+00	t	4	204	2	2
214	2019-10-25 05:33:20.949556+00	2019-10-25 05:33:20.949564+00	2019-10-25 05:33:20.949571+00	t	4	205	2	2
215	2019-10-25 05:33:20.949606+00	2019-10-25 05:33:20.949614+00	2019-10-25 05:33:20.949621+00	t	4	206	2	2
216	2019-10-25 05:33:20.949656+00	2019-10-25 05:33:20.949664+00	2019-10-25 05:33:20.949671+00	t	4	207	2	2
217	2019-10-25 05:33:20.949706+00	2019-10-25 05:33:20.949714+00	2019-10-25 05:33:20.949721+00	t	4	221	2	2
218	2019-10-25 05:33:20.949756+00	2019-10-25 05:33:20.949764+00	2019-10-25 05:33:20.949771+00	t	4	222	2	2
219	2019-10-25 05:33:20.949806+00	2019-10-25 05:33:20.949814+00	2019-10-25 05:33:20.949821+00	t	4	223	2	2
220	2019-10-25 05:33:20.949857+00	2019-10-25 05:33:20.949865+00	2019-10-25 05:33:20.949872+00	t	4	224	2	2
221	2019-10-25 05:33:20.949907+00	2019-10-25 05:33:20.949915+00	2019-10-25 05:33:20.949921+00	t	4	225	2	2
222	2019-10-25 05:33:20.949956+00	2019-10-25 05:33:20.949964+00	2019-10-25 05:33:20.949971+00	t	4	226	2	2
223	2019-10-25 05:33:20.950006+00	2019-10-25 05:33:20.950014+00	2019-10-25 05:33:20.950021+00	t	4	227	2	2
224	2019-10-25 05:33:20.950057+00	2019-10-25 05:33:20.950065+00	2019-10-25 05:33:20.950072+00	t	4	228	2	2
225	2019-10-25 05:33:20.950107+00	2019-10-25 05:33:20.950115+00	2019-10-25 05:33:20.950122+00	t	4	229	2	2
226	2019-10-25 05:33:20.950157+00	2019-10-25 05:33:20.950165+00	2019-10-25 05:33:20.950172+00	t	4	230	2	2
227	2019-10-25 05:33:20.950207+00	2019-10-25 05:33:20.950215+00	2019-10-25 05:33:20.950222+00	t	4	231	2	2
228	2019-10-25 05:33:20.950257+00	2019-10-25 05:33:20.950265+00	2019-10-25 05:33:20.950272+00	t	4	232	2	2
229	2019-10-25 05:33:20.950308+00	2019-10-25 05:33:20.950316+00	2019-10-25 05:33:20.950322+00	t	4	233	2	2
230	2019-10-25 05:33:20.950359+00	2019-10-25 05:33:20.950366+00	2019-10-25 05:33:20.950373+00	t	4	234	2	2
231	2019-10-25 05:33:20.950409+00	2019-10-25 05:33:20.950417+00	2019-10-25 05:33:20.950424+00	t	4	235	2	2
232	2019-10-25 05:33:20.950459+00	2019-10-25 05:33:20.950467+00	2019-10-25 05:33:20.950474+00	t	4	236	2	2
233	2019-10-25 05:33:20.95051+00	2019-10-25 05:33:20.950518+00	2019-10-25 05:33:20.950525+00	t	4	237	2	2
234	2019-10-25 05:33:20.95056+00	2019-10-25 05:33:20.950568+00	2019-10-25 05:33:20.950575+00	t	4	238	2	2
235	2019-10-25 05:33:20.950611+00	2019-10-25 05:33:20.950618+00	2019-10-25 05:33:20.950625+00	t	4	239	2	2
236	2019-10-25 05:33:20.950661+00	2019-10-25 05:33:20.950669+00	2019-10-25 05:33:20.950675+00	t	4	240	2	2
237	2019-10-25 05:33:20.950711+00	2019-10-25 05:33:20.950719+00	2019-10-25 05:33:20.950726+00	t	4	241	2	2
238	2019-10-25 05:33:20.950761+00	2019-10-25 05:33:20.950769+00	2019-10-25 05:33:20.950776+00	t	4	242	2	2
239	2019-10-25 05:33:20.950811+00	2019-10-25 05:33:20.950819+00	2019-10-25 05:33:20.950826+00	t	4	243	2	2
240	2019-10-25 05:33:20.950871+00	2019-10-25 05:33:20.95088+00	2019-10-25 05:33:20.950887+00	t	4	244	2	2
241	2019-10-25 05:33:20.950922+00	2019-10-25 05:33:20.95093+00	2019-10-25 05:33:20.950937+00	t	4	245	2	2
242	2019-10-25 05:33:20.950972+00	2019-10-25 05:33:20.950979+00	2019-10-25 05:33:20.950986+00	t	4	246	2	2
243	2019-10-25 05:33:20.951021+00	2019-10-25 05:33:20.951029+00	2019-10-25 05:33:20.951036+00	t	4	247	2	2
244	2019-10-25 05:33:20.951071+00	2019-10-25 05:33:20.951078+00	2019-10-25 05:33:20.951085+00	t	4	248	2	2
245	2019-10-25 05:33:20.95112+00	2019-10-25 05:33:20.951128+00	2019-10-25 05:33:20.951135+00	t	4	249	2	2
246	2019-10-25 05:33:20.95117+00	2019-10-25 05:33:20.951178+00	2019-10-25 05:33:20.951184+00	t	4	250	2	2
247	2019-10-25 05:33:20.951219+00	2019-10-25 05:33:20.951227+00	2019-10-25 05:33:20.951234+00	t	4	251	2	2
248	2019-10-25 05:33:20.951269+00	2019-10-25 05:33:20.951277+00	2019-10-25 05:33:20.951284+00	t	4	252	2	2
249	2019-10-25 05:33:20.951319+00	2019-10-25 05:33:20.951326+00	2019-10-25 05:33:20.951333+00	t	4	253	2	2
250	2019-10-25 05:33:20.951369+00	2019-10-25 05:33:20.951376+00	2019-10-25 05:33:20.951383+00	t	4	254	2	2
251	2019-10-25 05:33:20.951419+00	2019-10-25 05:33:20.951426+00	2019-10-25 05:33:20.951433+00	t	4	255	2	2
252	2019-11-01 04:33:38.430872+00	2019-11-01 04:33:38.430911+00	2019-11-01 04:33:38.35262+00	t	4	256	4	1
253	2019-11-01 04:33:38.430996+00	2019-11-01 04:33:38.431002+00	2019-11-01 04:33:38.353671+00	t	4	257	4	1
254	2019-11-01 04:33:38.431042+00	2019-11-01 04:33:38.431047+00	2019-11-01 04:33:38.354817+00	t	4	258	4	1
255	2019-11-01 04:33:38.431084+00	2019-11-01 04:33:38.43109+00	2019-11-01 04:33:38.356614+00	t	4	259	4	1
256	2019-11-01 04:33:38.431126+00	2019-11-01 04:33:38.431132+00	2019-11-01 04:33:38.357681+00	t	4	260	4	1
257	2019-11-01 04:33:38.431169+00	2019-11-01 04:33:38.431174+00	2019-11-01 04:33:38.358612+00	t	4	261	4	1
258	2019-11-01 04:33:38.431211+00	2019-11-01 04:33:38.431216+00	2019-11-01 04:33:38.359514+00	t	4	262	4	1
259	2019-11-01 04:33:38.431253+00	2019-11-01 04:33:38.431258+00	2019-11-01 04:33:38.360542+00	t	4	263	4	1
260	2019-11-01 04:33:38.431295+00	2019-11-01 04:33:38.431301+00	2019-11-01 04:33:38.361562+00	t	4	264	4	1
261	2019-11-01 04:33:38.431337+00	2019-11-01 04:33:38.431343+00	2019-11-01 04:33:38.363664+00	t	4	265	4	1
262	2019-11-01 04:33:38.43138+00	2019-11-01 04:33:38.431385+00	2019-11-01 04:33:38.364642+00	t	4	266	4	1
263	2019-11-01 04:33:38.431422+00	2019-11-01 04:33:38.431427+00	2019-11-01 04:33:38.365587+00	t	4	267	4	1
264	2019-11-01 04:33:38.431464+00	2019-11-01 04:33:38.43147+00	2019-11-01 04:33:38.366464+00	t	4	268	4	1
265	2019-11-01 04:33:38.431506+00	2019-11-01 04:33:38.431511+00	2019-11-01 04:33:38.367494+00	t	4	269	4	1
266	2019-11-01 04:33:38.431548+00	2019-11-01 04:33:38.431554+00	2019-11-01 04:33:38.368482+00	t	4	270	4	1
267	2019-11-01 04:33:38.43159+00	2019-11-01 04:33:38.431595+00	2019-11-01 04:33:38.36948+00	t	4	271	4	1
268	2019-11-01 04:33:38.431632+00	2019-11-01 04:33:38.431638+00	2019-11-01 04:33:38.37033+00	t	4	272	4	1
269	2019-11-01 04:33:38.431675+00	2019-11-01 04:33:38.43168+00	2019-11-01 04:33:38.371402+00	t	4	273	4	1
270	2019-11-01 04:33:38.431717+00	2019-11-01 04:33:38.431722+00	2019-11-01 04:33:38.372236+00	t	4	274	4	1
271	2019-11-01 04:33:38.431758+00	2019-11-01 04:33:38.431764+00	2019-11-01 04:33:38.373153+00	t	4	275	4	1
272	2019-11-01 04:33:38.431805+00	2019-11-01 04:33:38.431811+00	2019-11-01 04:33:38.374047+00	t	4	276	4	1
273	2019-11-01 04:33:38.431849+00	2019-11-01 04:33:38.431855+00	2019-11-01 04:33:38.375124+00	t	4	277	4	1
274	2019-11-01 04:33:38.431892+00	2019-11-01 04:33:38.431897+00	2019-11-01 04:33:38.376188+00	t	4	278	4	1
275	2019-11-01 04:33:38.431934+00	2019-11-01 04:33:38.431939+00	2019-11-01 04:33:38.377033+00	t	4	279	4	1
276	2019-11-01 04:33:38.431976+00	2019-11-01 04:33:38.431981+00	2019-11-01 04:33:38.389123+00	t	4	280	4	1
277	2019-11-01 04:33:38.432018+00	2019-11-01 04:33:38.432023+00	2019-11-01 04:33:38.39015+00	t	4	281	4	1
278	2019-11-01 04:33:38.432061+00	2019-11-01 04:33:38.432066+00	2019-11-01 04:33:38.391002+00	t	4	282	4	1
279	2019-11-01 04:33:38.432103+00	2019-11-01 04:33:38.432108+00	2019-11-01 04:33:38.391834+00	t	4	283	4	1
280	2019-11-01 04:33:38.432145+00	2019-11-01 04:33:38.43215+00	2019-11-01 04:33:38.392766+00	t	4	284	4	1
281	2019-11-01 04:33:38.432187+00	2019-11-01 04:33:38.432192+00	2019-11-01 04:33:38.393776+00	t	4	285	4	1
282	2019-11-01 04:33:38.432229+00	2019-11-01 04:33:38.432234+00	2019-11-01 04:33:38.395313+00	t	4	286	4	1
283	2019-11-01 04:33:38.432271+00	2019-11-01 04:33:38.432276+00	2019-11-01 04:33:38.39631+00	t	4	287	4	1
284	2019-11-01 04:33:38.432313+00	2019-11-01 04:33:38.432318+00	2019-11-01 04:33:38.397218+00	t	4	288	4	1
285	2019-11-01 04:33:38.432355+00	2019-11-01 04:33:38.43236+00	2019-11-01 04:33:38.399023+00	t	4	289	4	1
286	2019-11-01 04:33:38.432398+00	2019-11-01 04:33:38.432403+00	2019-11-01 04:33:38.4007+00	t	4	290	4	1
287	2019-11-01 04:33:38.43244+00	2019-11-01 04:33:38.432445+00	2019-11-01 04:33:38.401694+00	t	4	291	4	1
288	2019-11-01 04:33:38.432482+00	2019-11-01 04:33:38.432488+00	2019-11-01 04:33:38.402848+00	t	4	292	4	1
289	2019-11-01 04:33:38.432525+00	2019-11-01 04:33:38.43253+00	2019-11-01 04:33:38.403759+00	t	4	293	4	1
290	2019-11-01 04:33:38.432567+00	2019-11-01 04:33:38.432572+00	2019-11-01 04:33:38.404915+00	t	4	294	4	1
291	2019-11-01 04:33:38.432609+00	2019-11-01 04:33:38.432614+00	2019-11-01 04:33:38.406828+00	t	4	295	4	1
292	2019-11-01 04:33:38.432651+00	2019-11-01 04:33:38.432657+00	2019-11-01 04:33:38.408827+00	t	4	296	4	1
293	2019-11-01 04:33:38.432694+00	2019-11-01 04:33:38.432699+00	2019-11-01 04:33:38.410083+00	t	4	297	4	1
294	2019-11-01 04:33:38.432736+00	2019-11-01 04:33:38.432741+00	2019-11-01 04:33:38.411302+00	t	4	298	4	1
295	2019-11-01 04:33:38.432779+00	2019-11-01 04:33:38.432784+00	2019-11-01 04:33:38.412212+00	t	4	299	4	1
296	2019-11-01 04:33:38.432821+00	2019-11-01 04:33:38.432826+00	2019-11-01 04:33:38.413183+00	t	4	300	4	1
297	2019-11-01 04:33:38.432863+00	2019-11-01 04:33:38.432868+00	2019-11-01 04:33:38.414021+00	t	4	301	4	1
298	2019-11-01 04:33:38.432905+00	2019-11-01 04:33:38.432911+00	2019-11-01 04:33:38.414992+00	t	4	302	4	1
299	2019-11-01 04:33:38.432952+00	2019-11-01 04:33:38.432959+00	2019-11-01 04:33:38.41581+00	t	4	303	4	1
300	2019-11-01 04:33:38.432996+00	2019-11-01 04:33:38.433002+00	2019-11-01 04:33:38.416636+00	t	4	304	4	1
301	2019-11-01 04:33:38.433038+00	2019-11-01 04:33:38.433043+00	2019-11-01 04:33:38.417467+00	t	4	305	4	1
302	2019-11-01 04:33:38.433081+00	2019-11-01 04:33:38.433086+00	2019-11-01 04:33:38.418262+00	t	4	306	4	1
303	2019-11-01 04:33:38.433156+00	2019-11-01 04:33:38.433163+00	2019-11-01 04:33:38.419109+00	t	4	307	4	1
304	2019-11-01 04:33:38.4332+00	2019-11-01 04:33:38.433205+00	2019-11-01 04:33:38.420072+00	t	4	308	4	1
305	2019-11-01 04:33:38.433242+00	2019-11-01 04:33:38.433247+00	2019-11-01 04:33:38.421133+00	t	4	309	4	1
306	2019-11-01 04:33:38.433283+00	2019-11-01 04:33:38.433289+00	2019-11-01 04:33:38.422091+00	t	4	310	4	1
307	2019-11-01 04:33:38.433326+00	2019-11-01 04:33:38.433331+00	2019-11-01 04:33:38.42319+00	t	4	311	4	1
308	2019-11-01 04:33:38.433368+00	2019-11-01 04:33:38.433373+00	2019-11-01 04:33:38.42406+00	t	4	312	4	1
309	2019-11-01 04:33:38.433409+00	2019-11-01 04:33:38.433415+00	2019-11-01 04:33:38.424943+00	t	4	313	4	1
310	2019-11-01 04:33:38.433451+00	2019-11-01 04:33:38.433457+00	2019-11-01 04:33:38.425819+00	t	4	314	4	1
311	2019-11-01 04:33:38.433494+00	2019-11-01 04:33:38.433499+00	2019-11-01 04:33:38.42666+00	t	4	315	4	1
312	2019-11-01 04:33:38.433536+00	2019-11-01 04:33:38.433543+00	2019-11-01 04:33:38.427527+00	t	4	316	4	1
313	2019-11-01 04:33:38.433589+00	2019-11-01 04:33:38.433596+00	2019-11-01 04:33:38.428354+00	t	4	317	4	1
314	2019-11-01 04:33:38.433637+00	2019-11-01 04:33:38.433643+00	2019-11-01 04:33:38.429248+00	t	4	318	4	1
315	2019-11-01 04:33:38.43368+00	2019-11-01 04:33:38.433685+00	2019-11-01 04:33:38.430128+00	t	4	319	4	1
316	2019-11-01 04:33:38.537835+00	2019-11-01 04:33:38.537854+00	2019-11-01 04:33:38.470737+00	t	4	256	4	2
317	2019-11-01 04:33:38.537916+00	2019-11-01 04:33:38.537921+00	2019-11-01 04:33:38.471755+00	t	4	257	4	2
318	2019-11-01 04:33:38.53796+00	2019-11-01 04:33:38.537965+00	2019-11-01 04:33:38.473915+00	t	4	258	4	2
319	2019-11-01 04:33:38.538002+00	2019-11-01 04:33:38.538007+00	2019-11-01 04:33:38.475476+00	t	4	259	4	2
320	2019-11-01 04:33:38.538045+00	2019-11-01 04:33:38.53805+00	2019-11-01 04:33:38.476392+00	t	4	260	4	2
321	2019-11-01 04:33:38.538088+00	2019-11-01 04:33:38.538093+00	2019-11-01 04:33:38.477255+00	t	4	261	4	2
322	2019-11-01 04:33:38.53813+00	2019-11-01 04:33:38.538135+00	2019-11-01 04:33:38.478145+00	t	4	262	4	2
323	2019-11-01 04:33:38.538173+00	2019-11-01 04:33:38.538178+00	2019-11-01 04:33:38.479742+00	t	4	263	4	2
324	2019-11-01 04:33:38.538215+00	2019-11-01 04:33:38.53822+00	2019-11-01 04:33:38.480653+00	t	4	264	4	2
325	2019-11-01 04:33:38.538257+00	2019-11-01 04:33:38.538263+00	2019-11-01 04:33:38.481565+00	t	4	265	4	2
326	2019-11-01 04:33:38.5383+00	2019-11-01 04:33:38.538305+00	2019-11-01 04:33:38.482628+00	t	4	266	4	2
327	2019-11-01 04:33:38.538342+00	2019-11-01 04:33:38.53839+00	2019-11-01 04:33:38.483881+00	t	4	267	4	2
328	2019-11-01 04:33:38.538436+00	2019-11-01 04:33:38.538442+00	2019-11-01 04:33:38.484922+00	t	4	268	4	2
329	2019-11-01 04:33:38.53848+00	2019-11-01 04:33:38.538666+00	2019-11-01 04:33:38.486844+00	t	4	269	4	2
330	2019-11-01 04:33:38.538713+00	2019-11-01 04:33:38.538719+00	2019-11-01 04:33:38.487889+00	t	4	270	4	2
331	2019-11-01 04:33:38.538756+00	2019-11-01 04:33:38.538785+00	2019-11-01 04:33:38.488914+00	t	4	271	4	2
332	2019-11-01 04:33:38.538828+00	2019-11-01 04:33:38.538834+00	2019-11-01 04:33:38.490016+00	t	4	272	4	2
333	2019-11-01 04:33:38.53894+00	2019-11-01 04:33:38.538948+00	2019-11-01 04:33:38.490988+00	t	4	273	4	2
334	2019-11-01 04:33:38.538989+00	2019-11-01 04:33:38.538994+00	2019-11-01 04:33:38.491849+00	t	4	274	4	2
335	2019-11-01 04:33:38.539032+00	2019-11-01 04:33:38.539084+00	2019-11-01 04:33:38.492705+00	t	4	282	4	2
336	2019-11-01 04:33:38.53913+00	2019-11-01 04:33:38.539136+00	2019-11-01 04:33:38.493853+00	t	4	283	4	2
337	2019-11-01 04:33:38.539173+00	2019-11-01 04:33:38.539179+00	2019-11-01 04:33:38.494957+00	t	4	284	4	2
338	2019-11-01 04:33:38.539216+00	2019-11-01 04:33:38.539221+00	2019-11-01 04:33:38.495827+00	t	4	285	4	2
339	2019-11-01 04:33:38.539258+00	2019-11-01 04:33:38.539263+00	2019-11-01 04:33:38.496666+00	t	4	286	4	2
340	2019-11-01 04:33:38.539354+00	2019-11-01 04:33:38.539361+00	2019-11-01 04:33:38.497548+00	t	4	287	4	2
341	2019-11-01 04:33:38.539399+00	2019-11-01 04:33:38.539404+00	2019-11-01 04:33:38.498391+00	t	4	288	4	2
342	2019-11-01 04:33:38.539442+00	2019-11-01 04:33:38.539448+00	2019-11-01 04:33:38.499741+00	t	4	289	4	2
343	2019-11-01 04:33:38.539485+00	2019-11-01 04:33:38.539491+00	2019-11-01 04:33:38.500634+00	t	4	290	4	2
344	2019-11-01 04:33:38.539527+00	2019-11-01 04:33:38.539533+00	2019-11-01 04:33:38.501479+00	t	4	291	4	2
345	2019-11-01 04:33:38.53957+00	2019-11-01 04:33:38.539576+00	2019-11-01 04:33:38.502303+00	t	4	292	4	2
346	2019-11-01 04:33:38.539613+00	2019-11-01 04:33:38.539618+00	2019-11-01 04:33:38.503349+00	t	4	275	4	2
347	2019-11-01 04:33:38.539656+00	2019-11-01 04:33:38.539661+00	2019-11-01 04:33:38.504225+00	t	4	276	4	2
348	2019-11-01 04:33:38.539699+00	2019-11-01 04:33:38.539704+00	2019-11-01 04:33:38.505344+00	t	4	277	4	2
349	2019-11-01 04:33:38.539741+00	2019-11-01 04:33:38.539747+00	2019-11-01 04:33:38.506292+00	t	4	278	4	2
350	2019-11-01 04:33:38.539784+00	2019-11-01 04:33:38.53979+00	2019-11-01 04:33:38.507337+00	t	4	279	4	2
351	2019-11-01 04:33:38.539827+00	2019-11-01 04:33:38.539832+00	2019-11-01 04:33:38.508265+00	t	4	280	4	2
352	2019-11-01 04:33:38.53987+00	2019-11-01 04:33:38.539875+00	2019-11-01 04:33:38.509142+00	t	4	281	4	2
353	2019-11-01 04:33:38.539912+00	2019-11-01 04:33:38.539917+00	2019-11-01 04:33:38.510255+00	t	4	293	4	2
354	2019-11-01 04:33:38.539954+00	2019-11-01 04:33:38.539959+00	2019-11-01 04:33:38.51145+00	t	4	294	4	2
355	2019-11-01 04:33:38.539996+00	2019-11-01 04:33:38.540002+00	2019-11-01 04:33:38.512415+00	t	4	295	4	2
356	2019-11-01 04:33:38.540038+00	2019-11-01 04:33:38.540044+00	2019-11-01 04:33:38.513391+00	t	4	296	4	2
357	2019-11-01 04:33:38.540081+00	2019-11-01 04:33:38.540086+00	2019-11-01 04:33:38.514477+00	t	4	297	4	2
358	2019-11-01 04:33:38.540123+00	2019-11-01 04:33:38.540129+00	2019-11-01 04:33:38.515366+00	t	4	298	4	2
359	2019-11-01 04:33:38.540165+00	2019-11-01 04:33:38.540171+00	2019-11-01 04:33:38.516227+00	t	4	299	4	2
360	2019-11-01 04:33:38.540208+00	2019-11-01 04:33:38.540213+00	2019-11-01 04:33:38.517085+00	t	4	300	4	2
361	2019-11-01 04:33:38.54025+00	2019-11-01 04:33:38.540255+00	2019-11-01 04:33:38.518208+00	t	4	301	4	2
362	2019-11-01 04:33:38.540292+00	2019-11-01 04:33:38.540297+00	2019-11-01 04:33:38.519168+00	t	4	302	4	2
363	2019-11-01 04:33:38.540335+00	2019-11-01 04:33:38.54034+00	2019-11-01 04:33:38.52+00	t	4	303	4	2
364	2019-11-01 04:33:38.540376+00	2019-11-01 04:33:38.540382+00	2019-11-01 04:33:38.520842+00	t	4	304	4	2
365	2019-11-01 04:33:38.540419+00	2019-11-01 04:33:38.540424+00	2019-11-01 04:33:38.521731+00	t	4	305	4	2
366	2019-11-01 04:33:38.54046+00	2019-11-01 04:33:38.540466+00	2019-11-01 04:33:38.522579+00	t	4	306	4	2
367	2019-11-01 04:33:38.540503+00	2019-11-01 04:33:38.540508+00	2019-11-01 04:33:38.523445+00	t	4	307	4	2
368	2019-11-01 04:33:38.540545+00	2019-11-01 04:33:38.54055+00	2019-11-01 04:33:38.524426+00	t	4	308	4	2
369	2019-11-01 04:33:38.540587+00	2019-11-01 04:33:38.540593+00	2019-11-01 04:33:38.52544+00	t	4	309	4	2
370	2019-11-01 04:33:38.54063+00	2019-11-01 04:33:38.540635+00	2019-11-01 04:33:38.526301+00	t	4	310	4	2
371	2019-11-01 04:33:38.540672+00	2019-11-01 04:33:38.540678+00	2019-11-01 04:33:38.527196+00	t	4	311	4	2
372	2019-11-01 04:33:38.540715+00	2019-11-01 04:33:38.54072+00	2019-11-01 04:33:38.528297+00	t	4	312	4	2
373	2019-11-01 04:33:38.540758+00	2019-11-01 04:33:38.540763+00	2019-11-01 04:33:38.529393+00	t	4	313	4	2
374	2019-11-01 04:33:38.5408+00	2019-11-01 04:33:38.540805+00	2019-11-01 04:33:38.530453+00	t	4	314	4	2
375	2019-11-01 04:33:38.540843+00	2019-11-01 04:33:38.540849+00	2019-11-01 04:33:38.53304+00	t	4	315	4	2
376	2019-11-01 04:33:38.540887+00	2019-11-01 04:33:38.540892+00	2019-11-01 04:33:38.534014+00	t	4	316	4	2
377	2019-11-01 04:33:38.54093+00	2019-11-01 04:33:38.540935+00	2019-11-01 04:33:38.535564+00	t	4	317	4	2
378	2019-11-01 04:33:38.540973+00	2019-11-01 04:33:38.540978+00	2019-11-01 04:33:38.536547+00	t	4	318	4	2
379	2019-11-01 04:33:38.541015+00	2019-11-01 04:33:38.54102+00	2019-11-01 04:33:38.53746+00	t	4	319	4	2
380	2019-11-09 03:32:56.960372+00	2019-11-09 03:32:56.960389+00	2019-11-09 03:32:56.910463+00	t	4	320	5	1
381	2019-11-09 03:32:56.960451+00	2019-11-09 03:32:56.960457+00	2019-11-09 03:32:56.911651+00	t	4	321	5	1
382	2019-11-09 03:32:56.960496+00	2019-11-09 03:32:56.960502+00	2019-11-09 03:32:56.912496+00	t	4	322	5	1
383	2019-11-09 03:32:56.960539+00	2019-11-09 03:32:56.960545+00	2019-11-09 03:32:56.913394+00	t	4	323	5	1
384	2019-11-09 03:32:56.960582+00	2019-11-09 03:32:56.960587+00	2019-11-09 03:32:56.914213+00	t	4	324	5	1
385	2019-11-09 03:32:56.960644+00	2019-11-09 03:32:56.960652+00	2019-11-09 03:32:56.915032+00	t	4	325	5	1
386	2019-11-09 03:32:56.960692+00	2019-11-09 03:32:56.960697+00	2019-11-09 03:32:56.916024+00	t	4	326	5	1
387	2019-11-09 03:32:56.960734+00	2019-11-09 03:32:56.960739+00	2019-11-09 03:32:56.916844+00	t	4	327	5	1
388	2019-11-09 03:32:56.960775+00	2019-11-09 03:32:56.960781+00	2019-11-09 03:32:56.917679+00	t	4	328	5	1
389	2019-11-09 03:32:56.960817+00	2019-11-09 03:32:56.960823+00	2019-11-09 03:32:56.918489+00	t	4	329	5	1
390	2019-11-09 03:32:56.960859+00	2019-11-09 03:32:56.960865+00	2019-11-09 03:32:56.919297+00	t	4	330	5	1
391	2019-11-09 03:32:56.960902+00	2019-11-09 03:32:56.960907+00	2019-11-09 03:32:56.920224+00	t	4	331	5	1
392	2019-11-09 03:32:56.960944+00	2019-11-09 03:32:56.960949+00	2019-11-09 03:32:56.921043+00	t	4	332	5	1
393	2019-11-09 03:32:56.960985+00	2019-11-09 03:32:56.960991+00	2019-11-09 03:32:56.921894+00	t	4	333	5	1
394	2019-11-09 03:32:56.961027+00	2019-11-09 03:32:56.961033+00	2019-11-09 03:32:56.922943+00	t	4	335	5	1
395	2019-11-09 03:32:56.961069+00	2019-11-09 03:32:56.961074+00	2019-11-09 03:32:56.924077+00	t	4	336	5	1
396	2019-11-09 03:32:56.961155+00	2019-11-09 03:32:56.961161+00	2019-11-09 03:32:56.924911+00	t	4	337	5	1
397	2019-11-09 03:32:56.961198+00	2019-11-09 03:32:56.961203+00	2019-11-09 03:32:56.925781+00	t	4	338	5	1
398	2019-11-09 03:32:56.96124+00	2019-11-09 03:32:56.961245+00	2019-11-09 03:32:56.926593+00	t	4	339	5	1
399	2019-11-09 03:32:56.961281+00	2019-11-09 03:32:56.961286+00	2019-11-09 03:32:56.927584+00	t	4	340	5	1
400	2019-11-09 03:32:56.961323+00	2019-11-09 03:32:56.961328+00	2019-11-09 03:32:56.928393+00	t	4	341	5	1
401	2019-11-09 03:32:56.961364+00	2019-11-09 03:32:56.961369+00	2019-11-09 03:32:56.929277+00	t	4	342	5	1
402	2019-11-09 03:32:56.961406+00	2019-11-09 03:32:56.961411+00	2019-11-09 03:32:56.930163+00	t	4	343	5	1
403	2019-11-09 03:32:56.961448+00	2019-11-09 03:32:56.961453+00	2019-11-09 03:32:56.931157+00	t	4	344	5	1
404	2019-11-09 03:32:56.96149+00	2019-11-09 03:32:56.961495+00	2019-11-09 03:32:56.932289+00	t	4	345	5	1
405	2019-11-09 03:32:56.961533+00	2019-11-09 03:32:56.961538+00	2019-11-09 03:32:56.933145+00	t	4	346	5	1
406	2019-11-09 03:32:56.961595+00	2019-11-09 03:32:56.961601+00	2019-11-09 03:32:56.933995+00	t	4	347	5	1
407	2019-11-09 03:32:56.961638+00	2019-11-09 03:32:56.961643+00	2019-11-09 03:32:56.934812+00	t	4	348	5	1
408	2019-11-09 03:32:56.96168+00	2019-11-09 03:32:56.961685+00	2019-11-09 03:32:56.935648+00	t	4	349	5	1
409	2019-11-09 03:32:56.961721+00	2019-11-09 03:32:56.961726+00	2019-11-09 03:32:56.936458+00	t	4	350	5	1
410	2019-11-09 03:32:56.961763+00	2019-11-09 03:32:56.961769+00	2019-11-09 03:32:56.937311+00	t	4	351	5	1
411	2019-11-09 03:32:56.961805+00	2019-11-09 03:32:56.96181+00	2019-11-09 03:32:56.938132+00	t	4	352	5	1
412	2019-11-09 03:32:56.961847+00	2019-11-09 03:32:56.961852+00	2019-11-09 03:32:56.938938+00	t	4	353	5	1
413	2019-11-09 03:32:56.961888+00	2019-11-09 03:32:56.961893+00	2019-11-09 03:32:56.940536+00	t	4	354	5	1
414	2019-11-09 03:32:56.961929+00	2019-11-09 03:32:56.961934+00	2019-11-09 03:32:56.94143+00	t	4	355	5	1
415	2019-11-09 03:32:56.961971+00	2019-11-09 03:32:56.961976+00	2019-11-09 03:32:56.942258+00	t	4	356	5	1
416	2019-11-09 03:32:56.962032+00	2019-11-09 03:32:56.962038+00	2019-11-09 03:32:56.943148+00	t	4	357	5	1
417	2019-11-09 03:32:56.962076+00	2019-11-09 03:32:56.962081+00	2019-11-09 03:32:56.944218+00	t	4	358	5	1
418	2019-11-09 03:32:56.962118+00	2019-11-09 03:32:56.962123+00	2019-11-09 03:32:56.945082+00	t	4	359	5	1
419	2019-11-09 03:32:56.96216+00	2019-11-09 03:32:56.962166+00	2019-11-09 03:32:56.946055+00	t	4	360	5	1
420	2019-11-09 03:32:56.962202+00	2019-11-09 03:32:56.962208+00	2019-11-09 03:32:56.946903+00	t	4	361	5	1
421	2019-11-09 03:32:56.962244+00	2019-11-09 03:32:56.962249+00	2019-11-09 03:32:56.947887+00	t	4	362	5	1
422	2019-11-09 03:32:56.962286+00	2019-11-09 03:32:56.962291+00	2019-11-09 03:32:56.948915+00	t	4	363	5	1
423	2019-11-09 03:32:56.962327+00	2019-11-09 03:32:56.962333+00	2019-11-09 03:32:56.949821+00	t	4	364	5	1
424	2019-11-09 03:32:56.962369+00	2019-11-09 03:32:56.962374+00	2019-11-09 03:32:56.950644+00	t	4	334	5	1
425	2019-11-09 03:32:56.962411+00	2019-11-09 03:32:56.962416+00	2019-11-09 03:32:56.9517+00	t	4	367	5	1
426	2019-11-09 03:32:56.962452+00	2019-11-09 03:32:56.962458+00	2019-11-09 03:32:56.952526+00	t	4	368	5	1
427	2019-11-09 03:32:56.962513+00	2019-11-09 03:32:56.96252+00	2019-11-09 03:32:56.953394+00	t	4	369	5	1
428	2019-11-09 03:32:56.962557+00	2019-11-09 03:32:56.962562+00	2019-11-09 03:32:56.9543+00	t	4	370	5	1
429	2019-11-09 03:32:56.962599+00	2019-11-09 03:32:56.962604+00	2019-11-09 03:32:56.955217+00	t	4	371	5	1
430	2019-11-09 03:32:56.96264+00	2019-11-09 03:32:56.962645+00	2019-11-09 03:32:56.956499+00	t	4	372	5	1
431	2019-11-09 03:32:56.962681+00	2019-11-09 03:32:56.962687+00	2019-11-09 03:32:56.957385+00	t	4	373	5	1
432	2019-11-09 03:32:56.962723+00	2019-11-09 03:32:56.962728+00	2019-11-09 03:32:56.958219+00	t	4	374	5	1
433	2019-11-09 03:32:56.962765+00	2019-11-09 03:32:56.96277+00	2019-11-09 03:32:56.959045+00	t	4	365	5	1
434	2019-11-09 03:32:56.962807+00	2019-11-09 03:32:56.962812+00	2019-11-09 03:32:56.960031+00	t	4	366	5	1
435	2019-11-09 03:32:57.045387+00	2019-11-09 03:32:57.045405+00	2019-11-09 03:32:56.989898+00	t	4	320	5	2
436	2019-11-09 03:32:57.045467+00	2019-11-09 03:32:57.045473+00	2019-11-09 03:32:56.990796+00	t	4	321	5	2
437	2019-11-09 03:32:57.045511+00	2019-11-09 03:32:57.045517+00	2019-11-09 03:32:56.992149+00	t	4	322	5	2
438	2019-11-09 03:32:57.045562+00	2019-11-09 03:32:57.045568+00	2019-11-09 03:32:56.993275+00	t	4	323	5	2
439	2019-11-09 03:32:57.04561+00	2019-11-09 03:32:57.045616+00	2019-11-09 03:32:56.99502+00	t	4	324	5	2
440	2019-11-09 03:32:57.045654+00	2019-11-09 03:32:57.04566+00	2019-11-09 03:32:56.996265+00	t	4	325	5	2
441	2019-11-09 03:32:57.045696+00	2019-11-09 03:32:57.045701+00	2019-11-09 03:32:56.99764+00	t	4	326	5	2
442	2019-11-09 03:32:57.045744+00	2019-11-09 03:32:57.04575+00	2019-11-09 03:32:56.998559+00	t	4	327	5	2
443	2019-11-09 03:32:57.045787+00	2019-11-09 03:32:57.045792+00	2019-11-09 03:32:56.999585+00	t	4	328	5	2
444	2019-11-09 03:32:57.045835+00	2019-11-09 03:32:57.045841+00	2019-11-09 03:32:57.000942+00	t	4	329	5	2
445	2019-11-09 03:32:57.045878+00	2019-11-09 03:32:57.045883+00	2019-11-09 03:32:57.001876+00	t	4	330	5	2
446	2019-11-09 03:32:57.04592+00	2019-11-09 03:32:57.045926+00	2019-11-09 03:32:57.002745+00	t	4	331	5	2
447	2019-11-09 03:32:57.045962+00	2019-11-09 03:32:57.045967+00	2019-11-09 03:32:57.003618+00	t	4	332	5	2
448	2019-11-09 03:32:57.046004+00	2019-11-09 03:32:57.046009+00	2019-11-09 03:32:57.005298+00	t	4	333	5	2
449	2019-11-09 03:32:57.046046+00	2019-11-09 03:32:57.046051+00	2019-11-09 03:32:57.006329+00	t	4	335	5	2
450	2019-11-09 03:32:57.046087+00	2019-11-09 03:32:57.046093+00	2019-11-09 03:32:57.007203+00	t	4	336	5	2
451	2019-11-09 03:32:57.046129+00	2019-11-09 03:32:57.046135+00	2019-11-09 03:32:57.008369+00	t	4	337	5	2
452	2019-11-09 03:32:57.046171+00	2019-11-09 03:32:57.046177+00	2019-11-09 03:32:57.009301+00	t	4	338	5	2
453	2019-11-09 03:32:57.046213+00	2019-11-09 03:32:57.046218+00	2019-11-09 03:32:57.010178+00	t	4	339	5	2
454	2019-11-09 03:32:57.046255+00	2019-11-09 03:32:57.04626+00	2019-11-09 03:32:57.011257+00	t	4	340	5	2
455	2019-11-09 03:32:57.046296+00	2019-11-09 03:32:57.046302+00	2019-11-09 03:32:57.012332+00	t	4	341	5	2
456	2019-11-09 03:32:57.046346+00	2019-11-09 03:32:57.046352+00	2019-11-09 03:32:57.01322+00	t	4	342	5	2
457	2019-11-09 03:32:57.046389+00	2019-11-09 03:32:57.046395+00	2019-11-09 03:32:57.014173+00	t	4	343	5	2
458	2019-11-09 03:32:57.046431+00	2019-11-09 03:32:57.046436+00	2019-11-09 03:32:57.015054+00	t	4	344	5	2
459	2019-11-09 03:32:57.046473+00	2019-11-09 03:32:57.046478+00	2019-11-09 03:32:57.015952+00	t	4	345	5	2
460	2019-11-09 03:32:57.046514+00	2019-11-09 03:32:57.04652+00	2019-11-09 03:32:57.016903+00	t	4	346	5	2
461	2019-11-09 03:32:57.046565+00	2019-11-09 03:32:57.046571+00	2019-11-09 03:32:57.017937+00	t	4	347	5	2
462	2019-11-09 03:32:57.046607+00	2019-11-09 03:32:57.046612+00	2019-11-09 03:32:57.019067+00	t	4	348	5	2
463	2019-11-09 03:32:57.046649+00	2019-11-09 03:32:57.046654+00	2019-11-09 03:32:57.020444+00	t	4	349	5	2
464	2019-11-09 03:32:57.046691+00	2019-11-09 03:32:57.046696+00	2019-11-09 03:32:57.021625+00	t	4	350	5	2
465	2019-11-09 03:32:57.046733+00	2019-11-09 03:32:57.046738+00	2019-11-09 03:32:57.022578+00	t	4	351	5	2
466	2019-11-09 03:32:57.046775+00	2019-11-09 03:32:57.04678+00	2019-11-09 03:32:57.023726+00	t	4	352	5	2
467	2019-11-09 03:32:57.046833+00	2019-11-09 03:32:57.046839+00	2019-11-09 03:32:57.024681+00	t	4	353	5	2
468	2019-11-09 03:32:57.046876+00	2019-11-09 03:32:57.046881+00	2019-11-09 03:32:57.025555+00	t	4	354	5	2
469	2019-11-09 03:32:57.046918+00	2019-11-09 03:32:57.046923+00	2019-11-09 03:32:57.026364+00	t	4	355	5	2
470	2019-11-09 03:32:57.04696+00	2019-11-09 03:32:57.046965+00	2019-11-09 03:32:57.027204+00	t	4	356	5	2
471	2019-11-09 03:32:57.047002+00	2019-11-09 03:32:57.047007+00	2019-11-09 03:32:57.028155+00	t	4	357	5	2
472	2019-11-09 03:32:57.047044+00	2019-11-09 03:32:57.047049+00	2019-11-09 03:32:57.028964+00	t	4	358	5	2
473	2019-11-09 03:32:57.047086+00	2019-11-09 03:32:57.047091+00	2019-11-09 03:32:57.029808+00	t	4	359	5	2
474	2019-11-09 03:32:57.047128+00	2019-11-09 03:32:57.047133+00	2019-11-09 03:32:57.030614+00	t	4	360	5	2
475	2019-11-09 03:32:57.04717+00	2019-11-09 03:32:57.047175+00	2019-11-09 03:32:57.031551+00	t	4	361	5	2
476	2019-11-09 03:32:57.047212+00	2019-11-09 03:32:57.047217+00	2019-11-09 03:32:57.032375+00	t	4	362	5	2
477	2019-11-09 03:32:57.047253+00	2019-11-09 03:32:57.047259+00	2019-11-09 03:32:57.033243+00	t	4	363	5	2
478	2019-11-09 03:32:57.047295+00	2019-11-09 03:32:57.0473+00	2019-11-09 03:32:57.034078+00	t	4	364	5	2
479	2019-11-09 03:32:57.047347+00	2019-11-09 03:32:57.047352+00	2019-11-09 03:32:57.035024+00	t	4	334	5	2
480	2019-11-09 03:32:57.047388+00	2019-11-09 03:32:57.047394+00	2019-11-09 03:32:57.035975+00	t	4	367	5	2
481	2019-11-09 03:32:57.04743+00	2019-11-09 03:32:57.047435+00	2019-11-09 03:32:57.036799+00	t	4	368	5	2
482	2019-11-09 03:32:57.047472+00	2019-11-09 03:32:57.047477+00	2019-11-09 03:32:57.037654+00	t	4	369	5	2
483	2019-11-09 03:32:57.047514+00	2019-11-09 03:32:57.047519+00	2019-11-09 03:32:57.038489+00	t	4	370	5	2
484	2019-11-09 03:32:57.047556+00	2019-11-09 03:32:57.047561+00	2019-11-09 03:32:57.039292+00	t	4	371	5	2
485	2019-11-09 03:32:57.047598+00	2019-11-09 03:32:57.047604+00	2019-11-09 03:32:57.041147+00	t	4	372	5	2
486	2019-11-09 03:32:57.04764+00	2019-11-09 03:32:57.047645+00	2019-11-09 03:32:57.042074+00	t	4	373	5	2
487	2019-11-09 03:32:57.047681+00	2019-11-09 03:32:57.047687+00	2019-11-09 03:32:57.042957+00	t	4	374	5	2
488	2019-11-09 03:32:57.047732+00	2019-11-09 03:32:57.047737+00	2019-11-09 03:32:57.044083+00	t	4	365	5	2
489	2019-11-09 03:32:57.047774+00	2019-11-09 03:32:57.047779+00	2019-11-09 03:32:57.045008+00	t	4	366	5	2
\.


--
-- Data for Name: sows_events_ultrasoundtype; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_ultrasoundtype (id, created_at, modified_at, title, days, final) FROM stdin;
1	2019-10-17 13:28:57.962697+00	2019-10-17 13:28:57.962714+00	\N	30	f
2	2019-10-17 13:28:57.962737+00	2019-10-17 13:28:57.962745+00	\N	60	t
\.


--
-- Data for Name: sows_events_weaningsow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_events_weaningsow (id, created_at, modified_at, date, initiator_id, sow_id, tour_id, transaction_id) FROM stdin;
\.


--
-- Data for Name: sows_gilt; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_gilt (id, created_at, modified_at, birth_id, casting_list_to_seven_five_id, location_id, merger_id, mother_sow_id, new_born_group_id, status_id, tour_id) FROM stdin;
\.


--
-- Data for Name: sows_giltstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_giltstatus (id, created_at, modified_at, title) FROM stdin;
\.


--
-- Data for Name: sows_sow; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_sow (id, created_at, modified_at, birth_id, farm_id, alive, location_id, status_id, tour_id) FROM stdin;
325	2019-11-09 03:32:56.616798+00	2019-11-11 07:13:04.988225+00	\N	19084	t	62	4	5
333	2019-11-09 03:32:56.646169+00	2019-11-11 07:13:56.507618+00	\N	5020	t	64	4	5
9	2019-10-18 03:51:17.589518+00	2019-10-29 08:40:31.03284+00	\N	18724	t	157	9	2
324	2019-11-09 03:32:56.612971+00	2019-11-11 07:14:26.993158+00	\N	19595	t	65	4	5
320	2019-11-09 03:32:56.580882+00	2019-11-11 07:15:06.413736+00	\N	5122	t	66	4	5
322	2019-11-09 03:32:56.604439+00	2019-11-11 07:16:21.651566+00	\N	19593	t	67	4	5
326	2019-11-09 03:32:56.620658+00	2019-11-11 07:16:42.573047+00	\N	19341	t	68	4	5
327	2019-11-09 03:32:56.624383+00	2019-11-11 07:16:58.942656+00	\N	18956	t	69	4	5
332	2019-11-09 03:32:56.642113+00	2019-11-11 07:18:25.34317+00	\N	19603	t	76	4	5
5	2019-10-18 03:51:17.572087+00	2019-10-29 08:16:17.351469+00	\N	18195	t	170	9	2
258	2019-11-01 04:33:37.927625+00	2019-11-04 07:13:47.234595+00	\N	2568	t	278	4	4
260	2019-11-01 04:33:37.936655+00	2019-11-04 07:16:43.710371+00	\N	19218	t	284	4	4
257	2019-11-01 04:33:37.923331+00	2019-11-04 07:36:17.026966+00	\N	18951	t	298	4	4
6	2019-10-18 03:51:17.576303+00	2019-10-29 08:40:44.715918+00	\N	5144	t	156	9	2
7	2019-10-18 03:51:17.580569+00	2019-10-29 08:40:54.114262+00	\N	18456	t	155	9	2
261	2019-11-01 04:33:37.941016+00	2019-11-04 07:54:59.612781+00	\N	19223	t	35	4	4
259	2019-11-01 04:33:37.932239+00	2019-11-04 08:00:04.817987+00	\N	18702	t	58	4	4
217	2019-10-25 05:33:20.494587+00	2019-11-04 08:55:35.51619+00	\N	19263	t	232	9	2
256	2019-11-01 04:33:37.907456+00	2019-11-04 08:29:50.846745+00	B0675	19465	t	55	4	4
220	2019-10-25 05:33:20.501039+00	2019-11-04 08:46:27.772277+00	\N	18128	t	214	9	2
210	2019-10-25 05:33:20.47104+00	2019-11-04 08:47:14.230093+00	\N	18595	t	218	9	2
329	2019-11-09 03:32:56.63179+00	2019-11-11 07:18:52.481256+00	\N	19599	t	78	4	5
3	2019-10-18 03:51:17.5631+00	2019-10-29 08:18:35.088628+00	\N	19076	t	173	9	2
12	2019-10-18 03:51:17.602621+00	2019-10-29 08:19:57.369853+00	\N	19241	t	175	9	2
10	2019-10-18 03:51:17.594071+00	2019-10-29 08:22:33.051454+00	\N	2598	t	183	9	2
1	2019-10-18 03:44:16.351245+00	2019-10-29 08:25:41.148975+00	\N	911	t	189	9	1
4	2019-10-18 03:51:17.56745+00	2019-10-29 08:25:57.27839+00	\N	19080	t	190	9	2
321	2019-11-09 03:32:56.600562+00	2019-11-11 07:26:01.413255+00	\N	19336	t	81	4	5
8	2019-10-18 03:51:17.584847+00	2019-10-29 08:37:33.82292+00	\N	19105	t	165	9	2
330	2019-11-09 03:32:56.634681+00	2019-11-11 07:29:31.616917+00	\N	913	t	89	4	5
2	2019-10-18 03:51:17.559771+00	2019-10-29 08:40:09.905001+00	\N	19200	t	158	9	2
212	2019-10-25 05:33:20.480319+00	2019-11-04 08:47:53.529188+00	\N	18346	t	221	9	2
213	2019-10-25 05:33:20.484895+00	2019-11-04 08:48:30.606875+00	\N	18858	t	223	9	2
216	2019-10-25 05:33:20.491164+00	2019-11-04 08:56:07.844842+00	\N	19003	t	234	9	2
215	2019-10-25 05:33:20.489251+00	2019-11-04 08:59:06.435118+00	\N	19126	t	243	9	2
323	2019-11-09 03:32:56.608567+00	2019-11-11 07:29:46.600765+00	\N	19338	t	90	4	5
208	2019-10-25 05:33:20.4596+00	2019-11-04 09:00:04.765273+00	\N	18590	t	246	9	2
209	2019-10-25 05:33:20.465797+00	2019-11-04 09:00:24.573817+00	\N	19872	t	247	9	2
214	2019-10-25 05:33:20.487288+00	2019-11-04 09:00:41.889305+00	\N	19244	t	248	9	2
218	2019-10-25 05:33:20.497297+00	2019-11-04 09:00:57.43709+00	\N	19137	t	249	9	2
211	2019-10-25 05:33:20.475858+00	2019-11-04 09:02:38.327967+00	\N	19494	t	254	9	2
219	2019-10-25 05:33:20.499233+00	2019-11-04 09:04:34.388263+00	\N	19935	t	261	9	2
196	2019-10-25 05:24:14.965904+00	2019-11-04 09:06:21.54457+00	\N	18524	t	205	9	2
11	2019-10-18 03:51:17.598302+00	2019-11-04 09:06:49.885998+00	\N	18885	t	203	9	2
195	2019-10-25 05:24:14.95488+00	2019-11-04 09:07:22.131444+00	\N	5002	t	209	9	2
331	2019-11-09 03:32:56.638307+00	2019-11-11 07:30:19.276984+00	\N	19601	t	92	4	5
328	2019-11-09 03:32:56.62807+00	2019-11-09 03:32:57.171937+00	\N	19215	t	3	4	5
338	2019-11-09 03:32:56.665421+00	2019-11-11 07:17:22.893644+00	\N	19125	t	71	4	5
38	2019-10-18 03:51:17.696868+00	2019-10-29 08:14:38.121898+00	\N	18643	t	169	9	2
45	2019-10-18 03:51:17.728887+00	2019-10-29 08:18:07.17747+00	\N	19162	t	172	9	2
51	2019-10-18 03:51:17.750547+00	2019-10-29 08:19:42.455983+00	\N	2657	t	174	9	2
39	2019-10-18 03:51:17.701534+00	2019-10-29 08:20:35.756834+00	\N	19284	t	177	9	2
50	2019-10-18 03:51:17.748284+00	2019-10-29 08:25:01.35188+00	\N	19168	t	187	9	2
343	2019-11-09 03:32:56.685735+00	2019-11-11 07:19:24.427005+00	\N	19265	t	60	4	5
272	2019-11-01 04:33:37.992233+00	2019-11-11 07:25:30.846193+00	\N	19514	f	80	8	\N
341	2019-11-09 03:32:56.678085+00	2019-11-11 07:27:03.420396+00	\N	18749	t	82	4	5
267	2019-11-01 04:33:37.971368+00	2019-11-04 07:14:46.38723+00	\N	2345	t	280	4	4
56	2019-10-18 03:51:17.760345+00	2019-10-29 08:41:36.768389+00	\N	19561	t	152	9	2
271	2019-11-01 04:33:37.987906+00	2019-11-04 07:15:30.329013+00	\N	2359	t	290	4	4
269	2019-11-01 04:33:37.980296+00	2019-11-04 07:35:50.775487+00	\N	18482	t	296	4	4
264	2019-11-01 04:33:37.956984+00	2019-11-04 07:45:15.508513+00	\N	2588	t	302	4	4
268	2019-11-01 04:33:37.976093+00	2019-11-04 07:51:07.994187+00	\N	2606	t	268	4	4
263	2019-11-01 04:33:37.951987+00	2019-11-04 07:54:51.519661+00	\N	19226	t	34	4	4
266	2019-11-01 04:33:37.966125+00	2019-11-04 07:55:27.261651+00	\N	2600	t	38	4	4
274	2019-11-01 04:33:37.999234+00	2019-11-04 07:55:58.879286+00	\N	2628	t	41	4	4
270	2019-11-01 04:33:37.98458+00	2019-11-04 07:56:06.665491+00	\N	18740	t	42	4	4
345	2019-11-09 03:32:56.693779+00	2019-11-11 07:28:42.025425+00	\N	17989	t	87	4	5
262	2019-11-01 04:33:37.946024+00	2019-11-04 07:57:10.045698+00	\N	18967	t	46	4	4
265	2019-11-01 04:33:37.961525+00	2019-11-04 07:57:31.956181+00	\N	18718	t	48	4	4
41	2019-10-18 03:51:17.710526+00	2019-11-04 09:02:42.132888+00	\N	19923	t	192	9	2
342	2019-11-09 03:32:56.681851+00	2019-11-11 07:30:03.866922+00	\N	960	t	91	4	5
273	2019-11-01 04:33:37.996246+00	2019-11-04 09:03:11.876465+00	\N	2370	t	257	9	4
37	2019-10-18 03:51:17.692574+00	2019-10-29 08:26:10.986096+00	\N	19921	t	191	9	2
40	2019-10-18 03:51:17.706007+00	2019-10-29 08:27:03.407207+00	\N	19924	t	193	9	2
43	2019-10-18 03:51:17.719437+00	2019-10-29 08:27:28.179889+00	\N	19919	t	194	9	2
48	2019-10-18 03:51:17.742255+00	2019-10-29 08:28:21.07394+00	\N	19927	t	195	9	2
44	2019-10-18 03:51:17.724431+00	2019-10-29 08:37:53.997749+00	\N	2393	t	164	9	2
52	2019-10-18 03:51:17.752802+00	2019-10-29 08:39:00.993341+00	\N	18912	t	161	9	2
53	2019-10-18 03:51:17.75474+00	2019-10-29 08:39:44.186117+00	\N	19296	t	159	9	2
47	2019-10-18 03:51:17.737704+00	2019-11-04 09:05:19.765596+00	\N	19926	t	198	9	2
42	2019-10-18 03:51:17.714853+00	2019-11-04 09:06:30.773693+00	\N	19925	t	202	9	2
49	2019-10-18 03:51:17.745357+00	2019-11-04 09:07:04.498377+00	\N	19023	t	204	9	2
54	2019-10-18 03:51:17.75655+00	2019-11-04 09:12:26.942839+00	\N	19555	t	150	9	2
337	2019-11-09 03:32:56.66149+00	2019-11-11 07:30:33.876235+00	\N	19124	t	93	4	5
55	2019-10-18 03:51:17.758474+00	2019-11-04 09:13:42.854434+00	\N	19558	t	146	9	2
46	2019-10-18 03:51:17.733243+00	2019-11-04 09:14:13.963695+00	\N	18267	t	139	9	2
335	2019-11-09 03:32:56.653831+00	2019-11-09 03:32:57.238479+00	\N	19502	t	3	4	5
336	2019-11-09 03:32:56.657597+00	2019-11-09 03:32:57.247304+00	\N	18735	t	3	4	5
339	2019-11-09 03:32:56.669848+00	2019-11-09 03:32:57.27653+00	\N	19510	t	3	4	5
340	2019-11-09 03:32:56.674088+00	2019-11-09 03:32:57.285769+00	\N	18107	t	3	4	5
344	2019-11-09 03:32:56.689886+00	2019-11-09 03:32:57.336055+00	\N	19269	t	3	4	5
17	2019-10-18 03:51:17.624012+00	2019-10-29 08:41:07.40074+00	\N	19249	t	154	9	2
19	2019-10-18 03:51:17.632562+00	2019-10-29 08:41:22.645634+00	\N	2745	t	153	9	2
363	2019-11-09 03:32:56.76057+00	2019-11-11 07:12:31.259768+00	\N	19181	t	61	4	5
348	2019-11-09 03:32:56.705338+00	2019-11-11 07:13:36.5579+00	\N	19277	t	63	4	5
360	2019-11-09 03:32:56.751204+00	2019-11-11 07:17:10.355774+00	\N	19046	t	70	4	5
206	2019-10-25 05:33:20.443958+00	2019-10-25 06:04:57.484484+00	\N	19229	t	255	4	2
207	2019-10-25 05:33:20.451213+00	2019-11-04 08:54:42.702856+00	\N	19486	t	219	9	2
349	2019-11-09 03:32:56.70907+00	2019-11-11 07:17:36.621374+00	\N	18510	t	72	4	5
286	2019-11-01 04:33:38.055067+00	2019-11-04 07:20:24.321177+00	\N	19568	t	286	4	4
289	2019-11-01 04:33:38.068883+00	2019-11-04 07:44:53.634631+00	\N	19580	t	300	4	4
290	2019-11-01 04:33:38.073688+00	2019-11-04 07:49:26.987256+00	\N	19582	t	275	4	4
203	2019-10-25 05:33:20.426266+00	2019-11-04 08:54:56.568237+00	\N	19480	t	230	9	2
356	2019-11-09 03:32:56.735637+00	2019-11-11 07:18:14.6934+00	\N	19163	t	75	4	5
202	2019-10-25 05:33:20.421814+00	2019-11-04 08:58:09.713596+00	\N	2583	t	240	9	2
353	2019-11-09 03:32:56.724255+00	2019-11-11 07:25:03.513579+00	\N	19672	t	79	4	5
357	2019-11-09 03:32:56.739512+00	2019-11-11 07:28:01.144882+00	\N	4565	t	85	4	5
350	2019-11-09 03:32:56.712819+00	2019-11-11 07:29:17.472218+00	\N	19285	t	88	4	5
205	2019-10-25 05:33:20.437389+00	2019-11-04 08:58:24.540441+00	\N	2586	t	241	9	2
285	2019-11-01 04:33:38.049729+00	2019-11-04 07:49:55.079369+00	\N	2411	t	273	4	4
287	2019-11-01 04:33:38.059719+00	2019-11-04 07:50:40.232064+00	\N	19318	t	270	4	4
288	2019-11-01 04:33:38.06429+00	2019-11-04 07:55:08.819911+00	\N	19578	t	36	4	4
282	2019-11-01 04:33:38.035265+00	2019-11-04 07:56:40.739273+00	\N	19037	t	43	4	4
291	2019-11-01 04:33:38.078396+00	2019-11-04 07:56:49.555016+00	\N	19586	t	44	4	4
292	2019-11-01 04:33:38.084917+00	2019-11-04 07:57:19.149334+00	\N	19588	t	47	4	4
283	2019-11-01 04:33:38.039555+00	2019-11-04 07:59:55.929995+00	\N	19294	t	57	4	4
284	2019-11-01 04:33:38.044549+00	2019-11-04 08:34:28.9271+00	\N	19556	t	39	4	4
198	2019-10-25 05:33:20.404266+00	2019-11-04 08:46:49.755601+00	\N	18443	t	216	9	2
204	2019-10-25 05:33:20.430931+00	2019-11-04 08:53:03.148437+00	\N	18144	t	225	9	2
197	2019-10-25 05:33:20.401536+00	2019-11-04 08:53:16.461524+00	\N	2697	t	226	9	2
199	2019-10-25 05:33:20.409254+00	2019-11-04 08:58:36.799799+00	\N	5004	t	242	9	2
200	2019-10-25 05:33:20.41336+00	2019-11-04 09:02:14.833896+00	\N	19214	t	252	9	2
201	2019-10-25 05:33:20.417404+00	2019-11-04 09:03:59.609553+00	\N	19602	t	259	9	2
18	2019-10-18 03:51:17.628439+00	2019-11-04 09:04:48.939173+00	\N	19636	t	197	9	2
64	2019-10-18 03:51:17.784222+00	2019-11-04 09:05:39.176074+00	\N	19920	t	200	9	2
35	2019-10-18 03:51:17.684258+00	2019-11-04 09:05:54.585451+00	\N	19918	t	201	9	2
59	2019-10-18 03:51:17.766163+00	2019-11-04 09:09:56.215853+00	\N	755	t	168	9	2
28	2019-10-18 03:51:17.659215+00	2019-10-29 08:17:14.206265+00	\N	18505	t	171	9	2
23	2019-10-18 03:51:17.64852+00	2019-10-29 08:20:16.493664+00	\N	2497	t	176	9	2
61	2019-10-18 03:51:17.770737+00	2019-10-29 08:21:15.403121+00	\N	18934	t	186	9	2
16	2019-10-18 03:51:17.61975+00	2019-10-29 08:21:48.655156+00	\N	19248	t	185	9	2
32	2019-10-18 03:51:17.670704+00	2019-10-29 08:22:20.599594+00	\N	18381	t	184	9	2
33	2019-10-18 03:51:17.67552+00	2019-10-29 08:22:44.969206+00	\N	18509	t	182	9	2
30	2019-10-18 03:51:17.663751+00	2019-10-29 08:23:06.620077+00	\N	19913	t	181	9	2
22	2019-10-18 03:51:17.644564+00	2019-10-29 08:23:24.22339+00	\N	19006	t	180	9	2
27	2019-10-18 03:51:17.657097+00	2019-10-29 08:24:01.271824+00	\N	19912	t	179	9	2
62	2019-10-18 03:51:17.775354+00	2019-10-29 08:24:19.117174+00	\N	18425	t	178	9	2
25	2019-10-18 03:51:17.652834+00	2019-11-04 09:11:47.76257+00	\N	19909	t	151	9	2
34	2019-10-18 03:51:17.679941+00	2019-10-29 08:25:24.890165+00	\N	19915	t	188	9	2
21	2019-10-18 03:51:17.640507+00	2019-10-29 08:29:13.758308+00	\N	19525	t	196	9	2
36	2019-10-18 03:51:17.68845+00	2019-11-04 09:12:50.598569+00	\N	2385	t	149	9	2
58	2019-10-18 03:51:17.764234+00	2019-10-29 08:30:27.571005+00	\N	19917	t	199	9	2
60	2019-10-18 03:51:17.768343+00	2019-10-29 08:32:57.203092+00	\N	18035	t	167	9	2
14	2019-10-18 03:51:17.611184+00	2019-10-29 08:34:12.304934+00	\N	18731	t	166	9	2
15	2019-10-18 03:51:17.615421+00	2019-10-29 08:38:11.845997+00	\N	4524	t	163	9	2
20	2019-10-18 03:51:17.636634+00	2019-10-29 08:38:40.413092+00	\N	2620	t	162	9	2
24	2019-10-18 03:51:17.650647+00	2019-10-29 08:39:26.273889+00	\N	18501	t	160	9	2
26	2019-10-18 03:51:17.655022+00	2019-11-04 09:12:57.473569+00	\N	19910	t	142	9	2
29	2019-10-18 03:51:17.661388+00	2019-11-04 09:13:13.648394+00	\N	19914	t	143	9	2
63	2019-10-18 03:51:17.779729+00	2019-11-04 09:13:16.067867+00	\N	18941	t	148	9	2
13	2019-10-18 03:51:17.606866+00	2019-11-04 09:13:29.576322+00	\N	2474	t	147	9	2
57	2019-10-18 03:51:17.762223+00	2019-11-04 09:13:31.924791+00	\N	19564	t	144	9	2
31	2019-10-18 03:51:17.666014+00	2019-11-04 09:13:44.624524+00	\N	19916	t	145	9	2
346	2019-11-09 03:32:56.697588+00	2019-11-09 03:32:57.35705+00	\N	2379	t	3	4	5
347	2019-11-09 03:32:56.701471+00	2019-11-09 03:32:57.369707+00	\N	19403	t	3	4	5
351	2019-11-09 03:32:56.716678+00	2019-11-09 03:32:57.416641+00	\N	18902	t	3	4	5
352	2019-11-09 03:32:56.72056+00	2019-11-09 03:32:57.425761+00	\N	19031	t	3	4	5
354	2019-11-09 03:32:56.728048+00	2019-11-09 03:32:57.443946+00	\N	19416	t	3	4	5
355	2019-11-09 03:32:56.731853+00	2019-11-09 03:32:57.455531+00	\N	19963	t	3	4	5
358	2019-11-09 03:32:56.743473+00	2019-11-09 03:32:57.489404+00	\N	19965	t	3	4	5
359	2019-11-09 03:32:56.747182+00	2019-11-09 03:32:57.500464+00	\N	19045	t	3	4	5
361	2019-11-09 03:32:56.754972+00	2019-11-09 03:32:57.525703+00	\N	19559	t	3	4	5
362	2019-11-09 03:32:56.758712+00	2019-11-09 03:32:57.535791+00	\N	5096	t	3	4	5
364	2019-11-09 03:32:56.764594+00	2019-11-09 03:32:57.554053+00	\N	19311	t	3	4	5
372	2019-11-09 03:32:56.796373+00	2019-11-11 07:17:48.99973+00	\N	2683	t	73	4	5
365	2019-11-09 03:32:56.768907+00	2019-11-11 07:18:03.398064+00	\N	19313	t	74	4	5
368	2019-11-09 03:32:56.781046+00	2019-11-11 07:27:21.182776+00	\N	19959	t	83	4	5
366	2019-11-09 03:32:56.773002+00	2019-11-11 07:27:46.924523+00	\N	19059	t	84	4	5
236	2019-10-25 05:33:20.577759+00	2019-10-25 06:03:43.906578+00	\N	19941	t	251	4	2
373	2019-11-09 03:32:56.800191+00	2019-11-11 07:28:21.460416+00	\N	19197	t	86	4	5
229	2019-10-25 05:33:20.525713+00	2019-11-04 08:55:12.547922+00	\N	18270	t	231	9	2
238	2019-10-25 05:33:20.586692+00	2019-10-25 06:06:21.035808+00	\N	19943	t	258	4	2
224	2019-10-25 05:33:20.510124+00	2019-11-04 08:56:50.520353+00	\N	19929	t	236	9	2
227	2019-10-25 05:33:20.517756+00	2019-11-04 08:57:51.057159+00	\N	2396	t	239	9	2
232	2019-10-25 05:33:20.554553+00	2019-10-29 07:17:20.833258+00	\N	19553	t	229	4	2
241	2019-10-25 05:33:20.602186+00	2019-10-29 07:43:04.485923+00	\N	19946	t	265	4	2
281	2019-11-01 04:33:38.031323+00	2019-11-04 07:13:10.668142+00	\N	19549	t	277	4	4
297	2019-11-01 04:33:38.111313+00	2019-11-04 07:13:33.566008+00	\N	19090	t	294	4	4
305	2019-11-01 04:33:38.14291+00	2019-11-04 07:13:59.373986+00	\N	4573	t	293	4	4
298	2019-11-01 04:33:38.116186+00	2019-11-04 07:14:18.17949+00	\N	19106	t	279	4	4
316	2019-11-01 04:33:38.184266+00	2019-11-04 07:14:31.439925+00	\N	19443	t	292	4	4
222	2019-10-25 05:33:20.505951+00	2019-11-04 08:59:24.63099+00	\N	18769	t	244	9	2
301	2019-11-01 04:33:38.127244+00	2019-11-04 07:15:19.81618+00	\N	707	t	281	4	4
299	2019-11-01 04:33:38.119183+00	2019-11-04 07:15:42.51314+00	\N	18340	t	282	4	4
276	2019-11-01 04:33:38.01412+00	2019-11-04 07:15:56.18853+00	\N	19024	t	289	4	4
279	2019-11-01 04:33:38.024031+00	2019-11-04 07:16:08.609364+00	\N	18261	t	283	4	4
309	2019-11-01 04:33:38.154885+00	2019-11-04 07:16:19.61671+00	\N	5094	t	288	4	4
308	2019-11-01 04:33:38.1516+00	2019-11-04 07:18:34.91966+00	\N	18915	t	291	4	4
278	2019-11-01 04:33:38.021148+00	2019-11-04 07:19:35.474501+00	\N	19541	t	287	4	4
300	2019-11-01 04:33:38.122255+00	2019-11-04 07:19:50.915107+00	\N	19120	t	285	4	4
304	2019-11-01 04:33:38.139728+00	2019-11-04 07:35:34.652511+00	\N	19161	t	295	4	4
277	2019-11-01 04:33:38.017531+00	2019-11-04 07:36:04.373724+00	\N	19025	t	297	4	4
312	2019-11-01 04:33:38.166674+00	2019-11-04 07:44:41.881961+00	\N	19951	t	299	4	4
306	2019-11-01 04:33:38.145647+00	2019-11-04 07:45:02.522615+00	\N	18913	t	301	4	4
313	2019-11-01 04:33:38.171117+00	2019-11-04 07:45:30.279122+00	\N	19952	t	303	4	4
307	2019-11-01 04:33:38.14865+00	2019-11-04 07:49:11.214129+00	\N	18146	t	276	4	4
302	2019-11-01 04:33:38.130087+00	2019-11-04 07:49:38.259775+00	\N	18373	t	274	4	4
275	2019-11-01 04:33:38.002239+00	2019-11-04 07:50:11.407055+00	\N	18766	t	272	4	4
294	2019-11-01 04:33:38.095828+00	2019-11-04 07:50:28.619493+00	\N	2701	t	271	4	4
310	2019-11-01 04:33:38.157612+00	2019-11-04 07:50:56.036949+00	\N	19949	t	269	4	4
311	2019-11-01 04:33:38.162422+00	2019-11-04 07:51:22.90408+00	\N	19950	t	267	4	4
303	2019-11-01 04:33:38.135918+00	2019-11-04 07:55:18.692657+00	\N	4557	t	37	4	4
228	2019-10-25 05:33:20.521649+00	2019-11-04 08:59:43.288293+00	\N	19933	t	245	9	2
280	2019-11-01 04:33:38.02699+00	2019-11-04 07:55:50.526214+00	\N	19546	t	40	4	4
296	2019-11-01 04:33:38.10535+00	2019-11-04 07:56:59.640012+00	\N	18321	t	45	4	4
317	2019-11-01 04:33:38.188761+00	2019-11-04 07:57:41.495411+00	\N	19955	t	49	4	4
314	2019-11-01 04:33:38.175747+00	2019-11-04 07:57:59.831647+00	\N	19953	t	50	4	4
318	2019-11-01 04:33:38.202371+00	2019-11-04 07:58:11.101505+00	\N	19957	t	52	4	4
295	2019-11-01 04:33:38.100324+00	2019-11-04 07:58:19.871793+00	\N	19854	t	53	4	4
315	2019-11-01 04:33:38.18005+00	2019-11-04 07:58:36.568703+00	\N	19954	t	54	4	4
293	2019-11-01 04:33:38.09141+00	2019-11-04 08:00:17.969189+00	\N	19590	t	59	4	4
234	2019-10-25 05:33:20.566675+00	2019-11-04 08:21:50.011094+00	\N	19939	t	124	4	2
319	2019-11-01 04:33:38.211939+00	2019-11-04 08:34:17.271443+00	\N	19956	t	56	4	4
221	2019-10-25 05:33:20.503509+00	2019-11-04 08:47:01.14082+00	\N	19408	t	217	9	2
243	2019-10-25 05:33:20.611118+00	2019-11-04 08:47:39.653747+00	\N	19309	t	220	9	2
235	2019-10-25 05:33:20.571432+00	2019-11-04 09:01:31.711497+00	\N	19940	t	250	9	2
230	2019-10-25 05:33:20.531886+00	2019-11-04 09:02:27.324666+00	\N	19934	t	253	9	2
239	2019-10-25 05:33:20.591356+00	2019-11-04 09:02:56.415114+00	\N	19944	t	256	9	2
233	2019-10-25 05:33:20.561063+00	2019-11-04 09:04:18.127934+00	\N	19837	t	260	9	2
237	2019-10-25 05:33:20.582422+00	2019-11-04 09:04:45.68312+00	\N	19937	t	262	9	2
240	2019-10-25 05:33:20.596051+00	2019-11-04 09:05:02.932635+00	\N	19945	t	263	9	2
242	2019-10-25 05:33:20.606838+00	2019-11-04 09:05:18.844016+00	\N	19947	t	264	9	2
231	2019-10-25 05:33:20.547494+00	2019-11-04 09:06:42.630537+00	\N	2656	t	206	9	2
223	2019-10-25 05:33:20.507913+00	2019-11-04 09:07:10.528879+00	\N	19928	t	208	9	2
225	2019-10-25 05:33:20.511976+00	2019-11-04 09:07:38.209031+00	\N	19930	t	210	9	2
244	2019-10-25 05:33:20.613307+00	2019-11-04 09:08:01.592018+00	\N	19566	t	212	9	2
226	2019-10-25 05:33:20.514002+00	2019-11-04 09:08:14.04238+00	\N	19931	t	213	9	2
334	2019-11-09 03:32:56.650058+00	2019-11-09 03:32:57.5627+00	\N	5031	t	3	4	5
367	2019-11-09 03:32:56.777294+00	2019-11-09 03:32:57.5709+00	\N	19315	t	3	4	5
369	2019-11-09 03:32:56.784796+00	2019-11-09 03:32:57.595261+00	\N	19960	t	3	4	5
370	2019-11-09 03:32:56.788649+00	2019-11-09 03:32:57.61493+00	\N	19961	t	3	4	5
371	2019-11-09 03:32:56.792477+00	2019-11-09 03:32:57.627218+00	\N	19962	t	3	4	5
374	2019-11-09 03:32:56.803894+00	2019-11-09 03:32:57.659851+00	\N	19454	t	3	4	5
253	2019-10-25 05:33:20.632342+00	2019-11-04 08:46:39.302567+00	\N	19579	t	215	9	2
252	2019-10-25 05:33:20.630515+00	2019-11-04 08:54:21.646788+00	\N	19577	t	228	9	2
247	2019-10-25 05:33:20.619588+00	2019-11-04 08:55:49.70138+00	\N	2285	t	233	9	2
250	2019-10-25 05:33:20.626833+00	2019-11-04 08:56:28.020929+00	\N	19574	t	235	9	2
249	2019-10-25 05:33:20.624481+00	2019-11-04 08:57:06.89215+00	\N	18285	t	237	9	2
245	2019-10-25 05:33:20.615753+00	2019-11-04 08:48:10.41487+00	\N	19182	t	222	9	2
255	2019-10-25 05:33:20.637196+00	2019-11-04 08:52:44.397611+00	\N	5118	t	224	9	2
246	2019-10-25 05:33:20.617589+00	2019-11-04 08:53:29.835248+00	\N	19567	t	227	9	2
248	2019-10-25 05:33:20.622337+00	2019-11-04 08:57:22.732768+00	\N	18927	t	238	9	2
254	2019-10-25 05:33:20.634354+00	2019-11-04 09:07:00.334234+00	\N	18301	t	207	9	2
251	2019-10-25 05:33:20.628658+00	2019-11-04 09:07:48.65001+00	\N	19576	t	211	9	2
\.


--
-- Data for Name: sows_sowstatus; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY sows_sowstatus (id, created_at, modified_at, title) FROM stdin;
1	2019-10-17 13:28:57.781045+00	2019-10-17 13:28:57.781063+00	Осеменена 1
2	2019-10-17 13:28:57.781078+00	2019-10-17 13:28:57.781086+00	Осеменена 2
5	2019-10-17 13:28:57.78113+00	2019-10-17 13:28:57.781137+00	Прохолост
6	2019-10-17 13:28:57.781147+00	2019-10-17 13:28:57.781154+00	Аборт
7	2019-10-17 13:28:57.781164+00	2019-10-17 13:28:57.781171+00	Отъем
8	2019-10-17 13:28:57.781181+00	2019-10-17 13:28:57.781188+00	Брак
9	2019-10-17 13:28:57.781197+00	2019-10-17 13:28:57.781204+00	Опоросилась
10	2019-10-17 13:28:57.781214+00	2019-10-17 13:28:57.781221+00	Ожидает осеменения
4	2019-10-17 13:28:57.781113+00	2019-10-30 10:09:13.076057+00	Супорос 35
3	2019-10-17 13:28:57.781096+00	2019-10-30 10:09:20.549586+00	Супорос 28
\.


--
-- Data for Name: staff_workshopemployee; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY staff_workshopemployee (id, created_at, modified_at, is_officer, is_seminator, user_id, workshop_id, farm_name) FROM stdin;
7	2019-10-21 06:19:31.453627+00	2019-10-21 06:19:31.453658+00	f	f	9	3	
2	2019-10-21 05:48:04.17407+00	2019-10-25 04:33:42.434305+00	t	t	4	1	ШМЫГИ
3	2019-10-21 05:57:22.594333+00	2019-10-25 04:33:54.644336+00	f	t	5	1	СЕМЕН
4	2019-10-21 05:57:28.995169+00	2019-10-25 04:34:09.847003+00	f	t	7	1	БОРИС
5	2019-10-21 05:57:35.75781+00	2019-10-25 04:34:29.275554+00	f	t	6	1	ИВАНО
8	2019-10-21 07:31:22.123973+00	2019-10-25 04:34:42.033816+00	t	t	10	1	ГАРИ
6	2019-10-21 06:17:07.377471+00	2019-10-25 10:58:27.770364+00	t	t	8	1	АДМИН
\.


--
-- Data for Name: tours_tour; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY tours_tour (id, created_at, modified_at, start_date, week_number, year) FROM stdin;
1	2019-10-18 03:44:16.361511+00	2019-10-18 03:44:16.361531+00	2019-10-18 03:44:16.361143+00	27	2019
2	2019-10-18 03:51:17.79095+00	2019-10-18 03:51:17.790975+00	2019-10-18 03:51:17.790658+00	28	2019
3	2019-10-18 03:57:51.456645+00	2019-10-18 03:57:51.456672+00	2019-10-18 03:57:51.456449+00	42	2019
4	2019-11-01 04:33:38.227316+00	2019-11-01 04:33:38.227336+00	2019-11-01 04:33:38.226782+00	29	2019
5	2019-11-09 03:32:56.810383+00	2019-11-09 03:32:56.810396+00	2019-11-09 03:32:56.810113+00	30	2019
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
1	2019-10-18 03:44:16.434474+00	2019-10-18 03:44:16.434495+00	2019-10-18 03:44:16.434505+00	2	1	1	3
2	2019-10-18 03:51:18.054519+00	2019-10-18 03:51:18.054539+00	2019-10-18 03:51:18.054549+00	2	1	2	3
3	2019-10-18 03:51:18.065711+00	2019-10-18 03:51:18.065736+00	2019-10-18 03:51:18.065746+00	2	1	3	3
4	2019-10-18 03:51:18.077127+00	2019-10-18 03:51:18.077145+00	2019-10-18 03:51:18.077154+00	2	1	4	3
5	2019-10-18 03:51:18.08853+00	2019-10-18 03:51:18.088548+00	2019-10-18 03:51:18.088558+00	2	1	5	3
6	2019-10-18 03:51:18.099918+00	2019-10-18 03:51:18.099936+00	2019-10-18 03:51:18.099946+00	2	1	6	3
7	2019-10-18 03:51:18.11114+00	2019-10-18 03:51:18.111158+00	2019-10-18 03:51:18.111167+00	2	1	7	3
8	2019-10-18 03:51:18.123339+00	2019-10-18 03:51:18.123359+00	2019-10-18 03:51:18.123368+00	2	1	8	3
9	2019-10-18 03:51:18.134568+00	2019-10-18 03:51:18.134586+00	2019-10-18 03:51:18.134595+00	2	1	9	3
10	2019-10-18 03:51:18.146124+00	2019-10-18 03:51:18.146142+00	2019-10-18 03:51:18.146151+00	2	1	10	3
11	2019-10-18 03:51:18.157296+00	2019-10-18 03:51:18.157334+00	2019-10-18 03:51:18.157345+00	2	1	11	3
12	2019-10-18 03:51:18.170012+00	2019-10-18 03:51:18.170031+00	2019-10-18 03:51:18.17004+00	2	1	12	3
13	2019-10-18 03:51:18.181463+00	2019-10-18 03:51:18.181482+00	2019-10-18 03:51:18.181491+00	2	1	37	3
14	2019-10-18 03:51:18.188582+00	2019-10-18 03:51:18.188599+00	2019-10-18 03:51:18.188609+00	2	1	38	3
15	2019-10-18 03:51:18.195529+00	2019-10-18 03:51:18.195546+00	2019-10-18 03:51:18.195555+00	2	1	39	3
16	2019-10-18 03:51:18.205307+00	2019-10-18 03:51:18.205324+00	2019-10-18 03:51:18.205333+00	2	1	40	3
17	2019-10-18 03:51:18.2163+00	2019-10-18 03:51:18.216318+00	2019-10-18 03:51:18.216327+00	2	1	41	3
18	2019-10-18 03:51:18.228279+00	2019-10-18 03:51:18.228296+00	2019-10-18 03:51:18.228305+00	2	1	42	3
19	2019-10-18 03:51:18.239465+00	2019-10-18 03:51:18.239484+00	2019-10-18 03:51:18.239493+00	2	1	43	3
20	2019-10-18 03:51:18.250471+00	2019-10-18 03:51:18.250489+00	2019-10-18 03:51:18.250498+00	2	1	44	3
21	2019-10-18 03:51:18.261512+00	2019-10-18 03:51:18.26153+00	2019-10-18 03:51:18.261539+00	2	1	45	3
22	2019-10-18 03:51:18.272641+00	2019-10-18 03:51:18.27266+00	2019-10-18 03:51:18.272686+00	2	1	46	3
23	2019-10-18 03:51:18.284325+00	2019-10-18 03:51:18.284349+00	2019-10-18 03:51:18.284359+00	2	1	47	3
24	2019-10-18 03:51:18.295363+00	2019-10-18 03:51:18.295384+00	2019-10-18 03:51:18.295398+00	2	1	48	3
25	2019-10-18 03:51:18.306622+00	2019-10-18 03:51:18.30664+00	2019-10-18 03:51:18.30665+00	2	1	49	3
26	2019-10-18 03:51:18.317866+00	2019-10-18 03:51:18.317904+00	2019-10-18 03:51:18.317915+00	2	1	50	3
27	2019-10-18 03:51:18.330894+00	2019-10-18 03:51:18.330912+00	2019-10-18 03:51:18.330921+00	2	1	51	3
28	2019-10-18 03:51:18.341945+00	2019-10-18 03:51:18.341963+00	2019-10-18 03:51:18.341972+00	2	1	52	3
29	2019-10-18 03:51:18.349137+00	2019-10-18 03:51:18.349155+00	2019-10-18 03:51:18.349165+00	2	1	53	3
30	2019-10-18 03:51:18.356113+00	2019-10-18 03:51:18.356131+00	2019-10-18 03:51:18.35614+00	2	1	54	3
31	2019-10-18 03:51:18.365417+00	2019-10-18 03:51:18.365435+00	2019-10-18 03:51:18.365444+00	2	1	55	3
32	2019-10-18 03:51:18.37669+00	2019-10-18 03:51:18.376708+00	2019-10-18 03:51:18.376717+00	2	1	56	3
33	2019-10-18 03:51:18.387914+00	2019-10-18 03:51:18.387931+00	2019-10-18 03:51:18.38794+00	2	1	13	3
34	2019-10-18 03:51:18.398928+00	2019-10-18 03:51:18.398945+00	2019-10-18 03:51:18.398954+00	2	1	14	3
35	2019-10-18 03:51:18.410115+00	2019-10-18 03:51:18.410133+00	2019-10-18 03:51:18.410142+00	2	1	15	3
36	2019-10-18 03:51:18.421289+00	2019-10-18 03:51:18.421316+00	2019-10-18 03:51:18.421326+00	2	1	16	3
37	2019-10-18 03:51:18.432324+00	2019-10-18 03:51:18.432342+00	2019-10-18 03:51:18.432351+00	2	1	17	3
38	2019-10-18 03:51:18.443169+00	2019-10-18 03:51:18.443187+00	2019-10-18 03:51:18.443196+00	2	1	18	3
39	2019-10-18 03:51:18.454689+00	2019-10-18 03:51:18.454709+00	2019-10-18 03:51:18.454718+00	2	1	19	3
40	2019-10-18 03:51:18.465873+00	2019-10-18 03:51:18.465891+00	2019-10-18 03:51:18.4659+00	2	1	20	3
41	2019-10-18 03:51:18.478035+00	2019-10-18 03:51:18.478054+00	2019-10-18 03:51:18.478064+00	2	1	21	3
42	2019-10-18 03:51:18.491439+00	2019-10-18 03:51:18.491457+00	2019-10-18 03:51:18.491467+00	2	1	22	3
43	2019-10-18 03:51:18.504216+00	2019-10-18 03:51:18.504234+00	2019-10-18 03:51:18.504244+00	2	1	23	3
44	2019-10-18 03:51:18.517306+00	2019-10-18 03:51:18.517325+00	2019-10-18 03:51:18.517334+00	2	1	24	3
45	2019-10-18 03:51:18.530787+00	2019-10-18 03:51:18.530806+00	2019-10-18 03:51:18.530815+00	2	1	25	3
46	2019-10-18 03:51:18.54316+00	2019-10-18 03:51:18.543178+00	2019-10-18 03:51:18.543188+00	2	1	26	3
47	2019-10-18 03:51:18.556059+00	2019-10-18 03:51:18.556078+00	2019-10-18 03:51:18.556087+00	2	1	27	3
48	2019-10-18 03:51:18.569182+00	2019-10-18 03:51:18.5692+00	2019-10-18 03:51:18.569209+00	2	1	57	3
49	2019-10-18 03:51:18.586615+00	2019-10-18 03:51:18.586634+00	2019-10-18 03:51:18.586643+00	2	1	58	3
50	2019-10-18 03:51:18.593467+00	2019-10-18 03:51:18.593484+00	2019-10-18 03:51:18.593494+00	2	1	59	3
51	2019-10-18 03:51:18.60049+00	2019-10-18 03:51:18.600508+00	2019-10-18 03:51:18.600517+00	2	1	60	3
52	2019-10-18 03:51:18.607393+00	2019-10-18 03:51:18.607411+00	2019-10-18 03:51:18.60742+00	2	1	61	3
53	2019-10-18 03:51:18.614082+00	2019-10-18 03:51:18.614099+00	2019-10-18 03:51:18.614108+00	2	1	62	3
54	2019-10-18 03:51:18.62066+00	2019-10-18 03:51:18.620678+00	2019-10-18 03:51:18.620687+00	2	1	63	3
55	2019-10-18 03:51:18.627427+00	2019-10-18 03:51:18.627444+00	2019-10-18 03:51:18.627454+00	2	1	64	3
56	2019-10-18 03:51:18.634014+00	2019-10-18 03:51:18.634031+00	2019-10-18 03:51:18.634041+00	2	1	28	3
57	2019-10-18 03:51:18.650169+00	2019-10-18 03:51:18.650188+00	2019-10-18 03:51:18.650197+00	2	1	29	3
58	2019-10-18 03:51:18.662769+00	2019-10-18 03:51:18.662787+00	2019-10-18 03:51:18.662797+00	2	1	30	3
59	2019-10-18 03:51:18.675848+00	2019-10-18 03:51:18.67587+00	2019-10-18 03:51:18.67588+00	2	1	31	3
60	2019-10-18 03:51:18.688476+00	2019-10-18 03:51:18.688495+00	2019-10-18 03:51:18.688504+00	2	1	32	3
61	2019-10-18 03:51:18.700398+00	2019-10-18 03:51:18.700417+00	2019-10-18 03:51:18.700426+00	2	1	33	3
62	2019-10-18 03:51:18.713104+00	2019-10-18 03:51:18.713121+00	2019-10-18 03:51:18.71313+00	2	1	34	3
63	2019-10-18 03:51:18.727849+00	2019-10-18 03:51:18.727868+00	2019-10-18 03:51:18.727877+00	2	1	35	3
64	2019-10-18 03:51:18.74032+00	2019-10-18 03:51:18.740337+00	2019-10-18 03:51:18.740346+00	2	1	36	3
65	2019-10-18 05:18:03.475867+00	2019-10-18 05:18:03.475896+00	2019-10-18 05:18:03.475906+00	3	1	46	139
66	2019-10-18 05:31:50.175671+00	2019-10-18 05:31:50.175704+00	2019-10-18 05:31:50.175715+00	3	1	26	142
67	2019-10-18 05:32:08.442522+00	2019-10-18 05:32:08.442552+00	2019-10-18 05:32:08.442563+00	3	1	29	143
68	2019-10-18 05:32:26.115232+00	2019-10-18 05:32:26.115284+00	2019-10-18 05:32:26.11531+00	3	1	57	144
69	2019-10-18 05:32:43.706786+00	2019-10-18 05:32:43.706813+00	2019-10-18 05:32:43.706823+00	3	1	31	145
70	2019-10-18 05:34:21.425045+00	2019-10-18 05:34:21.425085+00	2019-10-18 05:34:21.425095+00	3	1	55	146
71	2019-10-18 05:34:55.379671+00	2019-10-18 05:34:55.379704+00	2019-10-18 05:34:55.379714+00	3	1	13	147
72	2019-10-18 05:35:19.014094+00	2019-10-18 05:35:19.014154+00	2019-10-18 05:35:19.014167+00	3	1	63	148
73	2019-10-18 05:35:48.701247+00	2019-10-18 05:35:48.70129+00	2019-10-18 05:35:48.701301+00	3	1	36	149
74	2019-10-18 05:36:09.893093+00	2019-10-18 05:36:09.893119+00	2019-10-18 05:36:09.893129+00	3	1	54	150
75	2019-10-18 05:36:40.477139+00	2019-10-18 05:36:40.477186+00	2019-10-18 05:36:40.477197+00	3	1	25	151
76	2019-10-18 05:37:12.915171+00	2019-10-18 05:37:12.915198+00	2019-10-18 05:37:12.915208+00	3	1	56	152
77	2019-10-18 05:38:00.598455+00	2019-10-18 05:38:00.598506+00	2019-10-18 05:38:00.598519+00	3	1	19	153
78	2019-10-18 05:38:23.887542+00	2019-10-18 05:38:23.887581+00	2019-10-18 05:38:23.887592+00	3	1	17	154
79	2019-10-18 05:38:44.573977+00	2019-10-18 05:38:44.574004+00	2019-10-18 05:38:44.574014+00	3	1	7	155
80	2019-10-18 05:39:02.505839+00	2019-10-18 05:39:02.505884+00	2019-10-18 05:39:02.505895+00	3	1	6	156
81	2019-10-18 05:39:23.693973+00	2019-10-18 05:39:23.694004+00	2019-10-18 05:39:23.694014+00	3	1	9	157
82	2019-10-18 05:40:03.402174+00	2019-10-18 05:40:03.402227+00	2019-10-18 05:40:03.402239+00	3	1	2	158
83	2019-10-18 05:40:23.586858+00	2019-10-18 05:40:23.586896+00	2019-10-18 05:40:23.586908+00	3	1	53	159
84	2019-10-18 05:40:44.240921+00	2019-10-18 05:40:44.240947+00	2019-10-18 05:40:44.240957+00	3	1	24	160
85	2019-10-18 05:41:12.285121+00	2019-10-18 05:41:12.285148+00	2019-10-18 05:41:12.285158+00	3	1	52	161
86	2019-10-18 05:41:36.109986+00	2019-10-18 05:41:36.11002+00	2019-10-18 05:41:36.110031+00	3	1	20	162
87	2019-10-18 05:41:53.80883+00	2019-10-18 05:41:53.808859+00	2019-10-18 05:41:53.808878+00	3	1	15	149
88	2019-10-18 05:42:20.175457+00	2019-10-18 05:42:20.175488+00	2019-10-18 05:42:20.1755+00	3	1	44	164
89	2019-10-18 05:46:23.792127+00	2019-10-18 05:46:23.792158+00	2019-10-18 05:46:23.792169+00	3	1	8	165
90	2019-10-18 05:47:02.09034+00	2019-10-18 05:47:02.090385+00	2019-10-18 05:47:02.090396+00	3	1	14	166
91	2019-10-18 05:47:19.750179+00	2019-10-18 05:47:19.750216+00	2019-10-18 05:47:19.750227+00	3	1	60	167
92	2019-10-18 05:47:37.544152+00	2019-10-18 05:47:37.544178+00	2019-10-18 05:47:37.544187+00	3	1	59	168
93	2019-10-18 05:54:20.49206+00	2019-10-18 05:54:20.492115+00	2019-10-18 05:54:20.492126+00	149	1	36	141
94	2019-10-18 05:54:40.631567+00	2019-10-18 05:54:40.631617+00	2019-10-18 05:54:40.631633+00	149	1	15	163
95	2019-10-18 05:54:51.412905+00	2019-10-18 05:54:51.412956+00	2019-10-18 05:54:51.412966+00	141	1	36	149
96	2019-10-18 05:58:28.562057+00	2019-10-18 05:58:28.562089+00	2019-10-18 05:58:28.5621+00	3	1	38	169
97	2019-10-18 05:58:54.935395+00	2019-10-18 05:58:54.935482+00	2019-10-18 05:58:54.935496+00	3	1	5	170
98	2019-10-18 05:59:15.830276+00	2019-10-18 05:59:15.830311+00	2019-10-18 05:59:15.830321+00	3	1	28	171
99	2019-10-18 05:59:32.176645+00	2019-10-18 05:59:32.176677+00	2019-10-18 05:59:32.176688+00	3	1	45	172
100	2019-10-18 05:59:55.126579+00	2019-10-18 05:59:55.126621+00	2019-10-18 05:59:55.126632+00	3	1	3	173
101	2019-10-18 06:00:11.50364+00	2019-10-18 06:00:11.503683+00	2019-10-18 06:00:11.503694+00	3	1	51	174
102	2019-10-18 06:00:40.648329+00	2019-10-18 06:00:40.648353+00	2019-10-18 06:00:40.648363+00	3	1	12	175
103	2019-10-18 06:01:08.203539+00	2019-10-18 06:01:08.203571+00	2019-10-18 06:01:08.203582+00	3	1	23	176
104	2019-10-18 06:01:27.412264+00	2019-10-18 06:01:27.412292+00	2019-10-18 06:01:27.412302+00	3	1	39	177
105	2019-10-18 06:01:51.222063+00	2019-10-18 06:01:51.222091+00	2019-10-18 06:01:51.222101+00	3	1	61	186
106	2019-10-18 06:02:13.356533+00	2019-10-18 06:02:13.356559+00	2019-10-18 06:02:13.356569+00	3	1	16	185
107	2019-10-18 06:02:42.859073+00	2019-10-18 06:02:42.859108+00	2019-10-18 06:02:42.859198+00	3	1	32	184
108	2019-10-18 06:03:06.187473+00	2019-10-18 06:03:06.187503+00	2019-10-18 06:03:06.187513+00	3	1	10	183
109	2019-10-18 06:03:19.295645+00	2019-10-18 06:03:19.295677+00	2019-10-18 06:03:19.295688+00	3	1	33	182
110	2019-10-18 06:04:47.663629+00	2019-10-18 06:04:47.663659+00	2019-10-18 06:04:47.663669+00	3	1	30	181
111	2019-10-18 06:05:47.718996+00	2019-10-18 06:05:47.719038+00	2019-10-18 06:05:47.71905+00	3	1	22	180
112	2019-10-18 06:06:04.488179+00	2019-10-18 06:06:04.488208+00	2019-10-18 06:06:04.488218+00	3	1	27	179
113	2019-10-18 06:06:25.358497+00	2019-10-18 06:06:25.358525+00	2019-10-18 06:06:25.358535+00	3	1	62	178
114	2019-10-18 06:23:45.993838+00	2019-10-18 06:23:45.993869+00	2019-10-18 06:23:45.99388+00	3	1	50	187
115	2019-10-18 06:24:05.048984+00	2019-10-18 06:24:05.049033+00	2019-10-18 06:24:05.049044+00	3	1	34	188
116	2019-10-18 06:24:20.708315+00	2019-10-18 06:24:20.70834+00	2019-10-18 06:24:20.70835+00	3	1	1	189
117	2019-10-18 06:24:44.985637+00	2019-10-18 06:24:44.985689+00	2019-10-18 06:24:44.9857+00	3	1	4	190
118	2019-10-18 06:25:09.138312+00	2019-10-18 06:25:09.138356+00	2019-10-18 06:25:09.138367+00	3	1	37	191
119	2019-10-18 06:25:25.552852+00	2019-10-18 06:25:25.552884+00	2019-10-18 06:25:25.552894+00	3	1	41	192
120	2019-10-18 06:25:37.405472+00	2019-10-18 06:25:37.405503+00	2019-10-18 06:25:37.405513+00	3	1	40	193
121	2019-10-18 06:25:49.154257+00	2019-10-18 06:25:49.154286+00	2019-10-18 06:25:49.154296+00	3	1	43	194
122	2019-10-18 06:26:04.131309+00	2019-10-18 06:26:04.131358+00	2019-10-18 06:26:04.131369+00	3	1	48	195
123	2019-10-18 06:26:19.525474+00	2019-10-18 06:26:19.525509+00	2019-10-18 06:26:19.52552+00	3	1	21	196
124	2019-10-18 06:26:34.532719+00	2019-10-18 06:26:34.532752+00	2019-10-18 06:26:34.532764+00	3	1	18	197
125	2019-10-18 06:26:48.628596+00	2019-10-18 06:26:48.628646+00	2019-10-18 06:26:48.628658+00	3	1	47	198
126	2019-10-18 06:27:10.735345+00	2019-10-18 06:27:10.735374+00	2019-10-18 06:27:10.735384+00	3	1	58	199
127	2019-10-18 06:27:27.954391+00	2019-10-18 06:27:27.954421+00	2019-10-18 06:27:27.954431+00	3	1	64	200
128	2019-10-18 06:27:39.738105+00	2019-10-18 06:27:39.738131+00	2019-10-18 06:27:39.738141+00	3	1	35	201
129	2019-10-18 06:27:54.787108+00	2019-10-18 06:27:54.787156+00	2019-10-18 06:27:54.787167+00	3	1	42	188
130	2019-10-18 06:28:32.188388+00	2019-10-18 06:28:32.188415+00	2019-10-18 06:28:32.188425+00	3	1	11	203
131	2019-10-18 06:28:49.77054+00	2019-10-18 06:28:49.770572+00	2019-10-18 06:28:49.770582+00	3	1	49	204
132	2019-10-18 06:36:33.070854+00	2019-10-18 06:36:33.070906+00	2019-10-18 06:36:33.070917+00	188	1	42	202
133	2019-10-25 05:24:15.107057+00	2019-10-25 05:24:15.107081+00	2019-10-25 05:24:15.10709+00	2	4	195	3
134	2019-10-25 05:24:15.133803+00	2019-10-25 05:24:15.133832+00	2019-10-25 05:24:15.133841+00	2	4	196	3
135	2019-10-25 05:33:20.978811+00	2019-10-25 05:33:20.978836+00	2019-10-25 05:33:20.978846+00	2	4	208	3
136	2019-10-25 05:33:20.9904+00	2019-10-25 05:33:20.990418+00	2019-10-25 05:33:20.990427+00	2	4	209	3
137	2019-10-25 05:33:20.997299+00	2019-10-25 05:33:20.997317+00	2019-10-25 05:33:20.997326+00	2	4	210	3
138	2019-10-25 05:33:21.005596+00	2019-10-25 05:33:21.00562+00	2019-10-25 05:33:21.00563+00	2	4	211	3
139	2019-10-25 05:33:21.014785+00	2019-10-25 05:33:21.014804+00	2019-10-25 05:33:21.014814+00	2	4	212	3
140	2019-10-25 05:33:21.022+00	2019-10-25 05:33:21.022019+00	2019-10-25 05:33:21.022029+00	2	4	213	3
141	2019-10-25 05:33:21.03035+00	2019-10-25 05:33:21.030369+00	2019-10-25 05:33:21.030378+00	2	4	214	3
142	2019-10-25 05:33:21.052071+00	2019-10-25 05:33:21.052091+00	2019-10-25 05:33:21.052099+00	2	4	215	3
143	2019-10-25 05:33:21.064163+00	2019-10-25 05:33:21.064185+00	2019-10-25 05:33:21.064194+00	2	4	216	3
144	2019-10-25 05:33:21.076461+00	2019-10-25 05:33:21.07648+00	2019-10-25 05:33:21.076489+00	2	4	217	3
145	2019-10-25 05:33:21.091543+00	2019-10-25 05:33:21.091563+00	2019-10-25 05:33:21.091572+00	2	4	218	3
146	2019-10-25 05:33:21.106016+00	2019-10-25 05:33:21.106042+00	2019-10-25 05:33:21.106051+00	2	4	219	3
147	2019-10-25 05:33:21.118951+00	2019-10-25 05:33:21.118971+00	2019-10-25 05:33:21.11898+00	2	4	220	3
148	2019-10-25 05:33:21.130547+00	2019-10-25 05:33:21.130565+00	2019-10-25 05:33:21.130574+00	2	4	197	3
149	2019-10-25 05:33:21.146412+00	2019-10-25 05:33:21.146438+00	2019-10-25 05:33:21.146447+00	2	4	198	3
150	2019-10-25 05:33:21.163859+00	2019-10-25 05:33:21.163881+00	2019-10-25 05:33:21.16389+00	2	4	199	3
151	2019-10-25 05:33:21.174277+00	2019-10-25 05:33:21.174294+00	2019-10-25 05:33:21.174303+00	2	4	200	3
152	2019-10-25 05:33:21.182722+00	2019-10-25 05:33:21.182745+00	2019-10-25 05:33:21.182754+00	2	4	201	3
153	2019-10-25 05:33:21.190469+00	2019-10-25 05:33:21.190486+00	2019-10-25 05:33:21.190495+00	2	4	202	3
154	2019-10-25 05:33:21.198313+00	2019-10-25 05:33:21.198331+00	2019-10-25 05:33:21.198341+00	2	4	203	3
155	2019-10-25 05:33:21.206137+00	2019-10-25 05:33:21.206155+00	2019-10-25 05:33:21.206164+00	2	4	204	3
156	2019-10-25 05:33:21.215693+00	2019-10-25 05:33:21.215712+00	2019-10-25 05:33:21.215721+00	2	4	205	3
157	2019-10-25 05:33:21.227347+00	2019-10-25 05:33:21.227374+00	2019-10-25 05:33:21.227383+00	2	4	206	3
158	2019-10-25 05:33:21.245481+00	2019-10-25 05:33:21.245617+00	2019-10-25 05:33:21.245641+00	2	4	207	3
159	2019-10-25 05:33:21.269284+00	2019-10-25 05:33:21.269305+00	2019-10-25 05:33:21.269314+00	2	4	221	3
160	2019-10-25 05:33:21.281034+00	2019-10-25 05:33:21.281053+00	2019-10-25 05:33:21.281062+00	2	4	222	3
161	2019-10-25 05:33:21.292097+00	2019-10-25 05:33:21.292114+00	2019-10-25 05:33:21.292123+00	2	4	223	3
162	2019-10-25 05:33:21.305928+00	2019-10-25 05:33:21.305948+00	2019-10-25 05:33:21.305957+00	2	4	224	3
163	2019-10-25 05:33:21.317981+00	2019-10-25 05:33:21.318001+00	2019-10-25 05:33:21.31801+00	2	4	225	3
164	2019-10-25 05:33:21.330464+00	2019-10-25 05:33:21.330483+00	2019-10-25 05:33:21.330493+00	2	4	226	3
165	2019-10-25 05:33:21.342519+00	2019-10-25 05:33:21.342539+00	2019-10-25 05:33:21.342548+00	2	4	227	3
166	2019-10-25 05:33:21.353813+00	2019-10-25 05:33:21.353832+00	2019-10-25 05:33:21.353841+00	2	4	228	3
167	2019-10-25 05:33:21.362649+00	2019-10-25 05:33:21.362681+00	2019-10-25 05:33:21.36269+00	2	4	229	3
168	2019-10-25 05:33:21.370376+00	2019-10-25 05:33:21.370394+00	2019-10-25 05:33:21.370402+00	2	4	230	3
169	2019-10-25 05:33:21.377198+00	2019-10-25 05:33:21.377217+00	2019-10-25 05:33:21.377226+00	2	4	231	3
170	2019-10-25 05:33:21.384412+00	2019-10-25 05:33:21.38443+00	2019-10-25 05:33:21.384439+00	2	4	232	3
171	2019-10-25 05:33:21.396192+00	2019-10-25 05:33:21.396219+00	2019-10-25 05:33:21.396228+00	2	4	233	3
172	2019-10-25 05:33:21.415439+00	2019-10-25 05:33:21.415457+00	2019-10-25 05:33:21.415466+00	2	4	234	3
173	2019-10-25 05:33:21.427665+00	2019-10-25 05:33:21.427683+00	2019-10-25 05:33:21.427692+00	2	4	235	3
174	2019-10-25 05:33:21.439754+00	2019-10-25 05:33:21.439775+00	2019-10-25 05:33:21.439784+00	2	4	236	3
175	2019-10-25 05:33:21.454226+00	2019-10-25 05:33:21.454245+00	2019-10-25 05:33:21.454254+00	2	4	237	3
176	2019-10-25 05:33:21.46692+00	2019-10-25 05:33:21.466938+00	2019-10-25 05:33:21.466947+00	2	4	238	3
177	2019-10-25 05:33:21.478628+00	2019-10-25 05:33:21.478649+00	2019-10-25 05:33:21.478657+00	2	4	239	3
178	2019-10-25 05:33:21.490894+00	2019-10-25 05:33:21.490916+00	2019-10-25 05:33:21.490925+00	2	4	240	3
179	2019-10-25 05:33:21.502545+00	2019-10-25 05:33:21.502564+00	2019-10-25 05:33:21.502573+00	2	4	241	3
180	2019-10-25 05:33:21.513932+00	2019-10-25 05:33:21.513951+00	2019-10-25 05:33:21.513959+00	2	4	242	3
181	2019-10-25 05:33:21.523069+00	2019-10-25 05:33:21.523087+00	2019-10-25 05:33:21.523096+00	2	4	243	3
182	2019-10-25 05:33:21.529908+00	2019-10-25 05:33:21.529924+00	2019-10-25 05:33:21.529933+00	2	4	244	3
183	2019-10-25 05:33:21.537855+00	2019-10-25 05:33:21.537879+00	2019-10-25 05:33:21.537888+00	2	4	245	3
184	2019-10-25 05:33:21.546841+00	2019-10-25 05:33:21.54686+00	2019-10-25 05:33:21.546869+00	2	4	246	3
185	2019-10-25 05:33:21.560159+00	2019-10-25 05:33:21.560181+00	2019-10-25 05:33:21.560191+00	2	4	247	3
186	2019-10-25 05:33:21.572532+00	2019-10-25 05:33:21.57255+00	2019-10-25 05:33:21.572559+00	2	4	248	3
187	2019-10-25 05:33:21.583916+00	2019-10-25 05:33:21.583934+00	2019-10-25 05:33:21.583942+00	2	4	249	3
188	2019-10-25 05:33:21.594894+00	2019-10-25 05:33:21.594912+00	2019-10-25 05:33:21.594921+00	2	4	250	3
189	2019-10-25 05:33:21.606627+00	2019-10-25 05:33:21.606648+00	2019-10-25 05:33:21.606657+00	2	4	251	3
190	2019-10-25 05:33:21.619517+00	2019-10-25 05:33:21.619539+00	2019-10-25 05:33:21.619548+00	2	4	252	3
191	2019-10-25 05:33:21.632409+00	2019-10-25 05:33:21.632432+00	2019-10-25 05:33:21.632447+00	2	4	253	3
192	2019-10-25 05:33:21.657757+00	2019-10-25 05:33:21.657783+00	2019-10-25 05:33:21.657792+00	2	4	254	3
193	2019-10-25 05:33:21.670059+00	2019-10-25 05:33:21.670077+00	2019-10-25 05:33:21.670086+00	2	4	255	3
194	2019-10-25 05:56:25.413999+00	2019-10-25 05:56:25.414031+00	2019-10-25 05:56:25.414042+00	3	9	217	232
195	2019-10-25 05:56:43.479234+00	2019-10-25 05:56:43.479266+00	2019-10-25 05:56:43.479277+00	3	9	196	233
196	2019-10-25 05:57:02.291639+00	2019-10-25 05:57:02.291672+00	2019-10-25 05:57:02.291683+00	3	9	216	234
197	2019-10-25 05:57:27.980636+00	2019-10-25 05:57:27.980662+00	2019-10-25 05:57:27.980672+00	3	9	250	235
198	2019-10-25 05:57:51.125531+00	2019-10-25 05:57:51.125565+00	2019-10-25 05:57:51.125576+00	3	9	224	236
199	2019-10-25 05:58:09.774639+00	2019-10-25 05:58:09.774672+00	2019-10-25 05:58:09.774686+00	3	9	249	237
200	2019-10-25 05:58:27.288489+00	2019-10-25 05:58:27.288527+00	2019-10-25 05:58:27.288539+00	3	9	248	238
201	2019-10-25 05:58:44.044856+00	2019-10-25 05:58:44.044882+00	2019-10-25 05:58:44.044892+00	3	9	255	239
202	2019-10-25 05:58:59.956694+00	2019-10-25 05:58:59.956727+00	2019-10-25 05:58:59.956737+00	3	9	202	240
203	2019-10-25 05:59:16.453354+00	2019-10-25 05:59:16.453528+00	2019-10-25 05:59:16.453546+00	3	9	205	241
204	2019-10-25 05:59:43.865917+00	2019-10-25 05:59:43.865942+00	2019-10-25 05:59:43.865952+00	3	9	199	242
205	2019-10-25 06:00:37.836671+00	2019-10-25 06:00:37.836697+00	2019-10-25 06:00:37.836707+00	3	9	215	243
206	2019-10-25 06:00:56.128435+00	2019-10-25 06:00:56.128472+00	2019-10-25 06:00:56.128482+00	3	9	222	244
207	2019-10-25 06:01:41.356337+00	2019-10-25 06:01:41.356364+00	2019-10-25 06:01:41.356374+00	3	9	228	245
208	2019-10-25 06:02:04.313287+00	2019-10-25 06:02:04.313314+00	2019-10-25 06:02:04.313323+00	3	9	208	246
209	2019-10-25 06:02:24.721394+00	2019-10-25 06:02:24.721427+00	2019-10-25 06:02:24.721438+00	3	9	209	247
210	2019-10-25 06:02:43.966689+00	2019-10-25 06:02:43.966714+00	2019-10-25 06:02:43.966724+00	3	9	214	248
211	2019-10-25 06:02:58.803756+00	2019-10-25 06:02:58.803789+00	2019-10-25 06:02:58.803799+00	3	9	218	249
212	2019-10-25 06:03:26.802934+00	2019-10-25 06:03:26.80296+00	2019-10-25 06:03:26.80297+00	3	9	235	250
213	2019-10-25 06:03:43.900274+00	2019-10-25 06:03:43.900299+00	2019-10-25 06:03:43.900309+00	3	9	236	251
214	2019-10-25 06:04:00.66083+00	2019-10-25 06:04:00.660857+00	2019-10-25 06:04:00.660867+00	3	9	211	252
215	2019-10-25 06:04:14.213006+00	2019-10-25 06:04:14.213048+00	2019-10-25 06:04:14.213059+00	3	9	230	253
216	2019-10-25 06:04:57.47844+00	2019-10-25 06:04:57.478482+00	2019-10-25 06:04:57.478493+00	3	9	206	255
217	2019-10-25 06:05:27.927954+00	2019-10-25 06:05:27.92798+00	2019-10-25 06:05:27.92799+00	3	9	239	256
218	2019-10-25 06:05:46.568404+00	2019-10-25 06:05:46.56843+00	2019-10-25 06:05:46.56844+00	3	9	234	257
219	2019-10-25 06:06:21.02953+00	2019-10-25 06:06:21.029558+00	2019-10-25 06:06:21.029568+00	3	9	238	258
220	2019-10-25 06:10:26.200132+00	2019-10-25 06:10:26.20016+00	2019-10-25 06:10:26.200174+00	252	8	211	254
221	2019-10-25 06:13:50.816568+00	2019-10-25 06:13:50.816602+00	2019-10-25 06:13:50.816613+00	3	9	219	252
222	2019-10-25 06:19:54.984042+00	2019-10-25 06:19:54.984075+00	2019-10-25 06:19:54.984086+00	252	9	219	261
223	2019-10-25 06:22:15.135822+00	2019-10-25 06:22:15.135847+00	2019-10-25 06:22:15.135856+00	3	9	231	206
224	2019-10-25 06:22:37.767242+00	2019-10-25 06:22:37.767279+00	2019-10-25 06:22:37.76729+00	3	9	254	207
225	2019-10-25 06:22:59.93033+00	2019-10-25 06:22:59.930359+00	2019-10-25 06:22:59.930387+00	3	9	223	208
226	2019-10-25 06:23:24.917386+00	2019-10-25 06:23:24.917411+00	2019-10-25 06:23:24.91742+00	3	9	195	209
227	2019-10-25 06:23:39.622384+00	2019-10-25 06:23:39.622425+00	2019-10-25 06:23:39.622436+00	3	9	225	210
228	2019-10-25 06:23:55.525518+00	2019-10-25 06:23:55.525545+00	2019-10-25 06:23:55.525555+00	3	9	251	211
229	2019-10-25 06:24:08.435008+00	2019-10-25 06:24:08.435042+00	2019-10-25 06:24:08.435052+00	3	9	244	212
230	2019-10-25 06:24:22.272986+00	2019-10-25 06:24:22.273014+00	2019-10-25 06:24:22.273023+00	3	9	226	213
231	2019-10-25 06:25:10.402924+00	2019-10-25 06:25:10.402952+00	2019-10-25 06:25:10.402962+00	3	9	220	214
232	2019-10-25 06:25:28.706543+00	2019-10-25 06:25:28.706594+00	2019-10-25 06:25:28.706614+00	3	9	253	215
233	2019-10-25 06:25:47.770098+00	2019-10-25 06:25:47.77013+00	2019-10-25 06:25:47.77014+00	3	9	198	216
234	2019-10-25 06:30:55.033414+00	2019-10-25 06:30:55.033438+00	2019-10-25 06:30:55.033447+00	3	9	221	217
235	2019-10-25 06:31:08.545329+00	2019-10-25 06:31:08.545364+00	2019-10-25 06:31:08.545375+00	3	9	210	218
236	2019-10-25 06:31:27.20431+00	2019-10-25 06:31:27.204343+00	2019-10-25 06:31:27.204354+00	3	9	207	219
237	2019-10-25 06:31:40.707822+00	2019-10-25 06:31:40.707867+00	2019-10-25 06:31:40.707879+00	3	9	243	220
238	2019-10-25 06:32:05.213802+00	2019-10-25 06:32:05.213829+00	2019-10-25 06:32:05.213839+00	3	9	212	221
239	2019-10-25 06:32:20.808809+00	2019-10-25 06:32:20.80884+00	2019-10-25 06:32:20.80885+00	3	9	245	222
240	2019-10-25 06:32:35.520924+00	2019-10-25 06:32:35.52095+00	2019-10-25 06:32:35.52096+00	3	9	213	223
241	2019-10-29 07:16:14.322816+00	2019-10-29 07:16:14.322836+00	2019-10-29 07:16:14.3205+00	3	4	200	252
242	2019-10-29 07:16:53.530818+00	2019-10-29 07:16:53.530843+00	2019-10-29 07:16:53.529468+00	3	4	229	231
243	2019-10-29 07:17:05.991045+00	2019-10-29 07:17:05.991068+00	2019-10-29 07:17:05.987551+00	3	4	203	230
244	2019-10-29 07:17:20.819034+00	2019-10-29 07:17:20.819057+00	2019-10-29 07:17:20.816764+00	3	4	232	229
245	2019-10-29 07:17:28.231535+00	2019-10-29 07:17:28.231553+00	2019-10-29 07:17:28.229961+00	3	4	252	228
246	2019-10-29 07:17:42.447633+00	2019-10-29 07:17:42.447651+00	2019-10-29 07:17:42.446326+00	3	4	246	227
247	2019-10-29 07:17:50.995479+00	2019-10-29 07:17:50.995508+00	2019-10-29 07:17:50.992631+00	3	4	197	226
248	2019-10-29 07:18:00.10416+00	2019-10-29 07:18:00.104351+00	2019-10-29 07:18:00.085572+00	3	4	204	225
249	2019-10-29 07:23:49.500755+00	2019-10-29 07:23:49.500786+00	2019-10-29 07:23:49.498848+00	239	4	255	224
250	2019-10-29 07:24:31.785502+00	2019-10-29 07:24:31.785532+00	2019-10-29 07:24:31.783817+00	3	4	227	239
251	2019-10-29 07:41:59.588784+00	2019-10-29 07:41:59.588808+00	2019-10-29 07:41:59.587435+00	3	4	201	259
252	2019-10-29 07:42:12.291494+00	2019-10-29 07:42:12.291514+00	2019-10-29 07:42:12.290191+00	3	4	233	260
253	2019-10-29 07:42:31.796638+00	2019-10-29 07:42:31.796663+00	2019-10-29 07:42:31.794875+00	3	4	237	262
254	2019-10-29 07:42:43.721202+00	2019-10-29 07:42:43.721225+00	2019-10-29 07:42:43.719519+00	3	4	240	263
255	2019-10-29 07:42:52.20622+00	2019-10-29 07:42:52.206241+00	2019-10-29 07:42:52.204978+00	3	4	242	264
256	2019-10-29 07:43:04.457501+00	2019-10-29 07:43:04.45752+00	2019-10-29 07:43:04.456235+00	3	4	241	265
257	2019-10-29 07:49:53.438079+00	2019-10-29 07:49:53.438106+00	2019-10-29 07:49:53.4357+00	233	4	196	205
258	2019-10-29 07:51:22.284256+00	2019-10-29 07:51:22.284285+00	2019-10-29 07:51:22.282821+00	3	4	247	233
259	2019-11-01 04:33:38.575473+00	2019-11-01 04:33:38.575511+00	2019-11-01 04:33:38.573123+00	2	4	256	3
260	2019-11-01 04:33:38.599398+00	2019-11-01 04:33:38.59942+00	2019-11-01 04:33:38.596714+00	2	4	257	3
261	2019-11-01 04:33:38.616194+00	2019-11-01 04:33:38.616223+00	2019-11-01 04:33:38.6148+00	2	4	258	3
262	2019-11-01 04:33:38.632011+00	2019-11-01 04:33:38.632034+00	2019-11-01 04:33:38.629488+00	2	4	259	3
263	2019-11-01 04:33:38.64599+00	2019-11-01 04:33:38.646006+00	2019-11-01 04:33:38.644552+00	2	4	260	3
264	2019-11-01 04:33:38.664314+00	2019-11-01 04:33:38.664338+00	2019-11-01 04:33:38.661808+00	2	4	261	3
265	2019-11-01 04:33:38.679501+00	2019-11-01 04:33:38.679522+00	2019-11-01 04:33:38.677317+00	2	4	262	3
266	2019-11-01 04:33:38.694094+00	2019-11-01 04:33:38.694113+00	2019-11-01 04:33:38.692093+00	2	4	263	3
267	2019-11-01 04:33:38.712176+00	2019-11-01 04:33:38.712197+00	2019-11-01 04:33:38.70856+00	2	4	264	3
268	2019-11-01 04:33:38.720536+00	2019-11-01 04:33:38.720553+00	2019-11-01 04:33:38.719088+00	2	4	265	3
269	2019-11-01 04:33:38.72853+00	2019-11-01 04:33:38.728545+00	2019-11-01 04:33:38.727169+00	2	4	266	3
270	2019-11-01 04:33:38.746385+00	2019-11-01 04:33:38.746404+00	2019-11-01 04:33:38.74463+00	2	4	267	3
271	2019-11-01 04:33:38.756438+00	2019-11-01 04:33:38.756456+00	2019-11-01 04:33:38.754012+00	2	4	268	3
272	2019-11-01 04:33:38.770008+00	2019-11-01 04:33:38.770024+00	2019-11-01 04:33:38.76766+00	2	4	269	3
273	2019-11-01 04:33:38.78546+00	2019-11-01 04:33:38.785483+00	2019-11-01 04:33:38.782753+00	2	4	270	3
274	2019-11-01 04:33:38.799132+00	2019-11-01 04:33:38.799152+00	2019-11-01 04:33:38.797057+00	2	4	271	3
275	2019-11-01 04:33:38.818382+00	2019-11-01 04:33:38.818402+00	2019-11-01 04:33:38.816263+00	2	4	272	3
276	2019-11-01 04:33:38.833973+00	2019-11-01 04:33:38.833988+00	2019-11-01 04:33:38.832572+00	2	4	273	3
277	2019-11-01 04:33:38.850078+00	2019-11-01 04:33:38.850099+00	2019-11-01 04:33:38.848347+00	2	4	274	3
278	2019-11-01 04:33:38.863505+00	2019-11-01 04:33:38.863519+00	2019-11-01 04:33:38.862093+00	2	4	282	3
279	2019-11-01 04:33:38.876527+00	2019-11-01 04:33:38.876544+00	2019-11-01 04:33:38.875083+00	2	4	283	3
280	2019-11-01 04:33:38.887204+00	2019-11-01 04:33:38.887219+00	2019-11-01 04:33:38.885643+00	2	4	284	3
281	2019-11-01 04:33:38.897267+00	2019-11-01 04:33:38.897284+00	2019-11-01 04:33:38.895787+00	2	4	285	3
282	2019-11-01 04:33:38.905569+00	2019-11-01 04:33:38.905582+00	2019-11-01 04:33:38.904267+00	2	4	286	3
283	2019-11-01 04:33:38.919122+00	2019-11-01 04:33:38.919141+00	2019-11-01 04:33:38.917148+00	2	4	287	3
284	2019-11-01 04:33:38.933261+00	2019-11-01 04:33:38.933276+00	2019-11-01 04:33:38.931824+00	2	4	288	3
285	2019-11-01 04:33:38.945796+00	2019-11-01 04:33:38.945813+00	2019-11-01 04:33:38.944284+00	2	4	289	3
286	2019-11-01 04:33:38.960095+00	2019-11-01 04:33:38.960112+00	2019-11-01 04:33:38.958437+00	2	4	290	3
287	2019-11-01 04:33:38.975973+00	2019-11-01 04:33:38.975992+00	2019-11-01 04:33:38.974091+00	2	4	291	3
288	2019-11-01 04:33:38.989731+00	2019-11-01 04:33:38.989748+00	2019-11-01 04:33:38.988264+00	2	4	292	3
289	2019-11-01 04:33:39.005123+00	2019-11-01 04:33:39.005148+00	2019-11-01 04:33:39.002848+00	2	4	275	3
290	2019-11-01 04:33:39.023153+00	2019-11-01 04:33:39.023172+00	2019-11-01 04:33:39.021341+00	2	4	276	3
291	2019-11-01 04:33:39.036289+00	2019-11-01 04:33:39.036305+00	2019-11-01 04:33:39.034786+00	2	4	277	3
292	2019-11-01 04:33:39.049571+00	2019-11-01 04:33:39.049596+00	2019-11-01 04:33:39.047501+00	2	4	278	3
293	2019-11-01 04:33:39.063708+00	2019-11-01 04:33:39.06373+00	2019-11-01 04:33:39.061654+00	2	4	279	3
294	2019-11-01 04:33:39.077295+00	2019-11-01 04:33:39.077314+00	2019-11-01 04:33:39.07548+00	2	4	280	3
295	2019-11-01 04:33:39.089058+00	2019-11-01 04:33:39.089075+00	2019-11-01 04:33:39.087344+00	2	4	281	3
296	2019-11-01 04:33:39.102743+00	2019-11-01 04:33:39.102758+00	2019-11-01 04:33:39.101285+00	2	4	293	3
297	2019-11-01 04:33:39.112563+00	2019-11-01 04:33:39.112581+00	2019-11-01 04:33:39.110451+00	2	4	294	3
298	2019-11-01 04:33:39.130324+00	2019-11-01 04:33:39.130341+00	2019-11-01 04:33:39.12856+00	2	4	295	3
299	2019-11-01 04:33:39.146269+00	2019-11-01 04:33:39.146285+00	2019-11-01 04:33:39.144458+00	2	4	296	3
300	2019-11-01 04:33:39.160154+00	2019-11-01 04:33:39.160167+00	2019-11-01 04:33:39.158868+00	2	4	297	3
301	2019-11-01 04:33:39.180901+00	2019-11-01 04:33:39.180926+00	2019-11-01 04:33:39.176822+00	2	4	298	3
302	2019-11-01 04:33:39.197466+00	2019-11-01 04:33:39.197484+00	2019-11-01 04:33:39.195863+00	2	4	299	3
303	2019-11-01 04:33:39.211218+00	2019-11-01 04:33:39.211242+00	2019-11-01 04:33:39.209544+00	2	4	300	3
304	2019-11-01 04:33:39.226155+00	2019-11-01 04:33:39.226177+00	2019-11-01 04:33:39.224295+00	2	4	301	3
305	2019-11-01 04:33:39.239106+00	2019-11-01 04:33:39.239121+00	2019-11-01 04:33:39.237625+00	2	4	302	3
306	2019-11-01 04:33:39.251443+00	2019-11-01 04:33:39.251457+00	2019-11-01 04:33:39.250179+00	2	4	303	3
307	2019-11-01 04:33:39.267403+00	2019-11-01 04:33:39.267421+00	2019-11-01 04:33:39.2656+00	2	4	304	3
308	2019-11-01 04:33:39.279623+00	2019-11-01 04:33:39.279637+00	2019-11-01 04:33:39.27838+00	2	4	305	3
309	2019-11-01 04:33:39.310251+00	2019-11-01 04:33:39.31027+00	2019-11-01 04:33:39.308491+00	2	4	306	3
310	2019-11-01 04:33:39.318857+00	2019-11-01 04:33:39.318877+00	2019-11-01 04:33:39.316932+00	2	4	307	3
311	2019-11-01 04:33:39.330869+00	2019-11-01 04:33:39.330881+00	2019-11-01 04:33:39.329566+00	2	4	308	3
312	2019-11-01 04:33:39.338154+00	2019-11-01 04:33:39.338167+00	2019-11-01 04:33:39.33695+00	2	4	309	3
313	2019-11-01 04:33:39.349004+00	2019-11-01 04:33:39.349018+00	2019-11-01 04:33:39.347634+00	2	4	310	3
314	2019-11-01 04:33:39.361345+00	2019-11-01 04:33:39.361362+00	2019-11-01 04:33:39.359947+00	2	4	311	3
315	2019-11-01 04:33:39.372867+00	2019-11-01 04:33:39.37288+00	2019-11-01 04:33:39.371721+00	2	4	312	3
316	2019-11-01 04:33:39.385936+00	2019-11-01 04:33:39.385955+00	2019-11-01 04:33:39.384056+00	2	4	313	3
317	2019-11-01 04:33:39.399469+00	2019-11-01 04:33:39.399489+00	2019-11-01 04:33:39.397213+00	2	4	314	3
318	2019-11-01 04:33:39.412384+00	2019-11-01 04:33:39.412399+00	2019-11-01 04:33:39.411088+00	2	4	315	3
319	2019-11-01 04:33:39.42797+00	2019-11-01 04:33:39.427994+00	2019-11-01 04:33:39.425001+00	2	4	316	3
320	2019-11-01 04:33:39.441775+00	2019-11-01 04:33:39.441793+00	2019-11-01 04:33:39.440093+00	2	4	317	3
321	2019-11-01 04:33:39.457716+00	2019-11-01 04:33:39.457736+00	2019-11-01 04:33:39.455454+00	2	4	318	3
322	2019-11-01 04:33:39.472701+00	2019-11-01 04:33:39.472719+00	2019-11-01 04:33:39.471022+00	2	4	319	3
323	2019-11-04 07:13:10.651376+00	2019-11-04 07:13:10.651401+00	2019-11-04 07:13:10.649211+00	3	4	281	277
324	2019-11-04 07:13:33.55947+00	2019-11-04 07:13:33.559491+00	2019-11-04 07:13:33.55799+00	3	4	297	294
325	2019-11-04 07:13:47.225526+00	2019-11-04 07:13:47.225552+00	2019-11-04 07:13:47.224012+00	3	4	258	278
326	2019-11-04 07:13:59.362328+00	2019-11-04 07:13:59.362347+00	2019-11-04 07:13:59.360916+00	3	4	305	293
327	2019-11-04 07:14:18.171241+00	2019-11-04 07:14:18.171266+00	2019-11-04 07:14:18.169173+00	3	4	298	279
328	2019-11-04 07:14:31.431927+00	2019-11-04 07:14:31.431953+00	2019-11-04 07:14:31.430305+00	3	4	316	292
329	2019-11-04 07:14:46.378023+00	2019-11-04 07:14:46.378046+00	2019-11-04 07:14:46.376602+00	3	4	267	280
330	2019-11-04 07:15:00.04889+00	2019-11-04 07:15:00.048914+00	2019-11-04 07:15:00.047526+00	3	4	308	287
331	2019-11-04 07:15:19.809927+00	2019-11-04 07:15:19.809946+00	2019-11-04 07:15:19.808674+00	3	4	301	281
332	2019-11-04 07:15:30.317406+00	2019-11-04 07:15:30.317432+00	2019-11-04 07:15:30.315661+00	3	4	271	290
333	2019-11-04 07:15:42.506508+00	2019-11-04 07:15:42.506526+00	2019-11-04 07:15:42.505197+00	3	4	299	282
334	2019-11-04 07:15:56.178423+00	2019-11-04 07:15:56.178454+00	2019-11-04 07:15:56.176033+00	3	4	276	289
335	2019-11-04 07:16:08.60096+00	2019-11-04 07:16:08.601016+00	2019-11-04 07:16:08.598395+00	3	4	279	283
336	2019-11-04 07:16:19.608985+00	2019-11-04 07:16:19.609005+00	2019-11-04 07:16:19.606551+00	3	4	309	288
337	2019-11-04 07:16:43.699826+00	2019-11-04 07:16:43.699845+00	2019-11-04 07:16:43.698465+00	3	4	260	284
338	2019-11-04 07:18:34.9123+00	2019-11-04 07:18:34.912327+00	2019-11-04 07:18:34.910797+00	287	4	308	291
339	2019-11-04 07:19:35.467796+00	2019-11-04 07:19:35.467827+00	2019-11-04 07:19:35.465692+00	3	4	278	287
340	2019-11-04 07:19:50.905939+00	2019-11-04 07:19:50.905966+00	2019-11-04 07:19:50.904589+00	3	4	300	285
341	2019-11-04 07:20:24.304769+00	2019-11-04 07:20:24.304789+00	2019-11-04 07:20:24.303436+00	3	4	286	286
342	2019-11-04 07:35:34.643277+00	2019-11-04 07:35:34.6433+00	2019-11-04 07:35:34.641535+00	3	9	304	295
343	2019-11-04 07:35:50.766536+00	2019-11-04 07:35:50.766565+00	2019-11-04 07:35:50.764878+00	3	9	269	296
344	2019-11-04 07:36:04.36353+00	2019-11-04 07:36:04.363548+00	2019-11-04 07:36:04.361961+00	3	9	277	297
345	2019-11-04 07:36:17.019088+00	2019-11-04 07:36:17.019117+00	2019-11-04 07:36:17.017489+00	3	9	257	298
346	2019-11-04 07:44:41.868366+00	2019-11-04 07:44:41.868601+00	2019-11-04 07:44:41.864953+00	3	9	312	299
347	2019-11-04 07:44:53.621555+00	2019-11-04 07:44:53.621573+00	2019-11-04 07:44:53.620329+00	3	9	289	300
348	2019-11-04 07:45:02.449854+00	2019-11-04 07:45:02.449938+00	2019-11-04 07:45:02.435917+00	3	9	306	301
349	2019-11-04 07:45:15.501685+00	2019-11-04 07:45:15.501708+00	2019-11-04 07:45:15.500319+00	3	9	264	302
350	2019-11-04 07:45:30.269131+00	2019-11-04 07:45:30.269152+00	2019-11-04 07:45:30.267487+00	3	9	313	303
351	2019-11-04 07:49:11.206169+00	2019-11-04 07:49:11.206195+00	2019-11-04 07:49:11.203351+00	3	9	307	276
352	2019-11-04 07:49:26.973811+00	2019-11-04 07:49:26.973849+00	2019-11-04 07:49:26.969642+00	3	9	290	275
353	2019-11-04 07:49:38.25116+00	2019-11-04 07:49:38.251192+00	2019-11-04 07:49:38.249499+00	3	9	302	274
354	2019-11-04 07:49:55.061877+00	2019-11-04 07:49:55.061905+00	2019-11-04 07:49:55.058014+00	3	9	285	273
355	2019-11-04 07:50:11.391441+00	2019-11-04 07:50:11.391468+00	2019-11-04 07:50:11.389301+00	3	9	275	272
356	2019-11-04 07:50:28.612045+00	2019-11-04 07:50:28.612071+00	2019-11-04 07:50:28.61003+00	3	9	294	271
357	2019-11-04 07:50:40.224496+00	2019-11-04 07:50:40.224521+00	2019-11-04 07:50:40.223143+00	3	9	287	270
358	2019-11-04 07:50:56.029725+00	2019-11-04 07:50:56.029752+00	2019-11-04 07:50:56.028398+00	3	9	310	269
359	2019-11-04 07:51:07.985943+00	2019-11-04 07:51:07.985961+00	2019-11-04 07:51:07.983959+00	3	9	268	268
360	2019-11-04 07:51:22.897467+00	2019-11-04 07:51:22.897485+00	2019-11-04 07:51:22.896251+00	3	9	311	267
361	2019-11-04 07:54:51.512181+00	2019-11-04 07:54:51.512207+00	2019-11-04 07:54:51.510799+00	3	9	263	34
362	2019-11-04 07:54:59.602852+00	2019-11-04 07:54:59.602879+00	2019-11-04 07:54:59.601202+00	3	9	261	35
363	2019-11-04 07:55:08.810142+00	2019-11-04 07:55:08.81016+00	2019-11-04 07:55:08.808926+00	3	9	288	36
364	2019-11-04 07:55:18.684562+00	2019-11-04 07:55:18.684583+00	2019-11-04 07:55:18.682962+00	3	9	303	37
365	2019-11-04 07:55:27.251264+00	2019-11-04 07:55:27.251285+00	2019-11-04 07:55:27.249601+00	3	9	266	38
366	2019-11-04 07:55:37.472492+00	2019-11-04 07:55:37.472515+00	2019-11-04 07:55:37.471269+00	3	9	319	39
367	2019-11-04 07:55:50.519283+00	2019-11-04 07:55:50.519308+00	2019-11-04 07:55:50.516964+00	3	9	280	40
368	2019-11-04 07:55:58.869893+00	2019-11-04 07:55:58.869912+00	2019-11-04 07:55:58.868607+00	3	9	274	41
369	2019-11-04 07:56:06.659425+00	2019-11-04 07:56:06.659445+00	2019-11-04 07:56:06.658156+00	3	9	270	42
370	2019-11-04 07:56:40.732835+00	2019-11-04 07:56:40.732857+00	2019-11-04 07:56:40.731486+00	3	9	282	43
371	2019-11-04 07:56:49.547108+00	2019-11-04 07:56:49.547137+00	2019-11-04 07:56:49.545811+00	3	9	291	44
372	2019-11-04 07:56:59.631777+00	2019-11-04 07:56:59.631795+00	2019-11-04 07:56:59.630279+00	3	9	296	45
373	2019-11-04 07:57:10.03745+00	2019-11-04 07:57:10.037526+00	2019-11-04 07:57:10.035613+00	3	9	262	46
374	2019-11-04 07:57:19.142266+00	2019-11-04 07:57:19.142291+00	2019-11-04 07:57:19.140786+00	3	9	292	47
375	2019-11-04 07:57:31.948316+00	2019-11-04 07:57:31.948342+00	2019-11-04 07:57:31.946939+00	3	9	265	48
376	2019-11-04 07:57:41.488861+00	2019-11-04 07:57:41.488882+00	2019-11-04 07:57:41.486793+00	3	9	317	49
377	2019-11-04 07:57:59.824238+00	2019-11-04 07:57:59.824262+00	2019-11-04 07:57:59.822862+00	3	9	314	50
378	2019-11-04 07:58:11.095166+00	2019-11-04 07:58:11.095185+00	2019-11-04 07:58:11.093967+00	3	9	318	52
379	2019-11-04 07:58:19.863206+00	2019-11-04 07:58:19.863234+00	2019-11-04 07:58:19.861175+00	3	9	295	53
380	2019-11-04 07:58:36.557893+00	2019-11-04 07:58:36.557913+00	2019-11-04 07:58:36.556601+00	3	9	315	54
381	2019-11-04 07:59:55.918194+00	2019-11-04 07:59:55.918219+00	2019-11-04 07:59:55.916462+00	3	9	283	57
382	2019-11-04 08:00:04.776913+00	2019-11-04 08:00:04.776939+00	2019-11-04 08:00:04.773618+00	3	9	259	58
383	2019-11-04 08:00:17.948881+00	2019-11-04 08:00:17.9489+00	2019-11-04 08:00:17.947642+00	3	9	293	59
384	2019-11-04 08:21:49.992533+00	2019-11-04 08:21:49.992562+00	2019-11-04 08:21:49.991123+00	257	9	234	124
385	2019-11-04 08:22:08.492179+00	2019-11-04 08:22:08.49308+00	2019-11-04 08:22:08.488546+00	3	9	273	257
386	2019-11-04 08:29:50.827672+00	2019-11-04 08:29:50.827703+00	2019-11-04 08:29:50.82517+00	3	9	256	55
387	2019-11-04 08:34:17.261173+00	2019-11-04 08:34:17.261205+00	2019-11-04 08:34:17.259543+00	39	9	319	56
388	2019-11-04 08:34:28.916474+00	2019-11-04 08:34:28.916493+00	2019-11-04 08:34:28.914822+00	3	9	284	39
389	2019-11-09 03:32:57.072386+00	2019-11-09 03:32:57.072404+00	2019-11-09 03:32:57.07101+00	2	4	320	3
390	2019-11-09 03:32:57.094699+00	2019-11-09 03:32:57.094716+00	2019-11-09 03:32:57.092989+00	2	4	321	3
391	2019-11-09 03:32:57.106141+00	2019-11-09 03:32:57.106157+00	2019-11-09 03:32:57.104209+00	2	4	322	3
392	2019-11-09 03:32:57.116912+00	2019-11-09 03:32:57.11693+00	2019-11-09 03:32:57.114792+00	2	4	323	3
393	2019-11-09 03:32:57.129772+00	2019-11-09 03:32:57.129787+00	2019-11-09 03:32:57.12823+00	2	4	324	3
394	2019-11-09 03:32:57.141275+00	2019-11-09 03:32:57.14129+00	2019-11-09 03:32:57.139807+00	2	4	325	3
395	2019-11-09 03:32:57.150397+00	2019-11-09 03:32:57.15041+00	2019-11-09 03:32:57.149158+00	2	4	326	3
396	2019-11-09 03:32:57.158292+00	2019-11-09 03:32:57.158306+00	2019-11-09 03:32:57.156794+00	2	4	327	3
397	2019-11-09 03:32:57.167603+00	2019-11-09 03:32:57.167619+00	2019-11-09 03:32:57.165953+00	2	4	328	3
398	2019-11-09 03:32:57.175191+00	2019-11-09 03:32:57.175204+00	2019-11-09 03:32:57.173924+00	2	4	329	3
399	2019-11-09 03:32:57.183159+00	2019-11-09 03:32:57.183244+00	2019-11-09 03:32:57.181432+00	2	4	330	3
400	2019-11-09 03:32:57.192977+00	2019-11-09 03:32:57.19299+00	2019-11-09 03:32:57.191301+00	2	4	331	3
401	2019-11-09 03:32:57.20524+00	2019-11-09 03:32:57.205255+00	2019-11-09 03:32:57.203838+00	2	4	332	3
402	2019-11-09 03:32:57.217152+00	2019-11-09 03:32:57.217167+00	2019-11-09 03:32:57.215763+00	2	4	333	3
403	2019-11-09 03:32:57.231855+00	2019-11-09 03:32:57.23187+00	2019-11-09 03:32:57.230174+00	2	4	335	3
404	2019-11-09 03:32:57.242548+00	2019-11-09 03:32:57.242561+00	2019-11-09 03:32:57.241362+00	2	4	336	3
405	2019-11-09 03:32:57.251915+00	2019-11-09 03:32:57.251929+00	2019-11-09 03:32:57.250174+00	2	4	337	3
406	2019-11-09 03:32:57.261748+00	2019-11-09 03:32:57.261763+00	2019-11-09 03:32:57.260283+00	2	4	338	3
407	2019-11-09 03:32:57.271601+00	2019-11-09 03:32:57.271616+00	2019-11-09 03:32:57.269935+00	2	4	339	3
408	2019-11-09 03:32:57.280389+00	2019-11-09 03:32:57.280402+00	2019-11-09 03:32:57.279125+00	2	4	340	3
409	2019-11-09 03:32:57.290878+00	2019-11-09 03:32:57.290895+00	2019-11-09 03:32:57.289338+00	2	4	341	3
410	2019-11-09 03:32:57.301963+00	2019-11-09 03:32:57.301978+00	2019-11-09 03:32:57.300477+00	2	4	342	3
411	2019-11-09 03:32:57.317878+00	2019-11-09 03:32:57.317895+00	2019-11-09 03:32:57.314905+00	2	4	343	3
412	2019-11-09 03:32:57.329522+00	2019-11-09 03:32:57.329535+00	2019-11-09 03:32:57.328205+00	2	4	344	3
413	2019-11-09 03:32:57.341161+00	2019-11-09 03:32:57.341176+00	2019-11-09 03:32:57.339875+00	2	4	345	3
414	2019-11-09 03:32:57.350974+00	2019-11-09 03:32:57.350987+00	2019-11-09 03:32:57.349832+00	2	4	346	3
415	2019-11-09 03:32:57.361292+00	2019-11-09 03:32:57.361307+00	2019-11-09 03:32:57.359808+00	2	4	347	3
416	2019-11-09 03:32:57.377057+00	2019-11-09 03:32:57.377075+00	2019-11-09 03:32:57.375282+00	2	4	348	3
417	2019-11-09 03:32:57.388478+00	2019-11-09 03:32:57.388492+00	2019-11-09 03:32:57.387037+00	2	4	349	3
418	2019-11-09 03:32:57.398265+00	2019-11-09 03:32:57.398279+00	2019-11-09 03:32:57.396876+00	2	4	350	3
419	2019-11-09 03:32:57.410341+00	2019-11-09 03:32:57.410357+00	2019-11-09 03:32:57.408537+00	2	4	351	3
420	2019-11-09 03:32:57.420924+00	2019-11-09 03:32:57.420938+00	2019-11-09 03:32:57.419677+00	2	4	352	3
421	2019-11-09 03:32:57.429775+00	2019-11-09 03:32:57.429788+00	2019-11-09 03:32:57.428493+00	2	4	353	3
422	2019-11-09 03:32:57.438848+00	2019-11-09 03:32:57.438862+00	2019-11-09 03:32:57.437488+00	2	4	354	3
423	2019-11-09 03:32:57.449517+00	2019-11-09 03:32:57.44953+00	2019-11-09 03:32:57.448105+00	2	4	355	3
424	2019-11-09 03:32:57.460763+00	2019-11-09 03:32:57.460778+00	2019-11-09 03:32:57.459122+00	2	4	356	3
425	2019-11-09 03:32:57.472058+00	2019-11-09 03:32:57.472071+00	2019-11-09 03:32:57.470715+00	2	4	357	3
426	2019-11-09 03:32:57.483457+00	2019-11-09 03:32:57.483473+00	2019-11-09 03:32:57.481941+00	2	4	358	3
427	2019-11-09 03:32:57.494417+00	2019-11-09 03:32:57.49443+00	2019-11-09 03:32:57.493248+00	2	4	359	3
428	2019-11-09 03:32:57.506817+00	2019-11-09 03:32:57.506833+00	2019-11-09 03:32:57.504862+00	2	4	360	3
429	2019-11-09 03:32:57.518827+00	2019-11-09 03:32:57.518842+00	2019-11-09 03:32:57.517412+00	2	4	361	3
430	2019-11-09 03:32:57.530606+00	2019-11-09 03:32:57.530619+00	2019-11-09 03:32:57.529437+00	2	4	362	3
431	2019-11-09 03:32:57.540038+00	2019-11-09 03:32:57.540052+00	2019-11-09 03:32:57.538611+00	2	4	363	3
432	2019-11-09 03:32:57.549152+00	2019-11-09 03:32:57.549168+00	2019-11-09 03:32:57.547862+00	2	4	364	3
433	2019-11-09 03:32:57.557467+00	2019-11-09 03:32:57.55748+00	2019-11-09 03:32:57.556213+00	2	4	334	3
434	2019-11-09 03:32:57.566305+00	2019-11-09 03:32:57.566319+00	2019-11-09 03:32:57.56499+00	2	4	367	3
435	2019-11-09 03:32:57.57702+00	2019-11-09 03:32:57.577035+00	2019-11-09 03:32:57.575627+00	2	4	368	3
436	2019-11-09 03:32:57.588682+00	2019-11-09 03:32:57.588696+00	2019-11-09 03:32:57.587432+00	2	4	369	3
437	2019-11-09 03:32:57.608131+00	2019-11-09 03:32:57.608149+00	2019-11-09 03:32:57.606323+00	2	4	370	3
438	2019-11-09 03:32:57.620916+00	2019-11-09 03:32:57.620931+00	2019-11-09 03:32:57.619272+00	2	4	371	3
439	2019-11-09 03:32:57.632773+00	2019-11-09 03:32:57.632786+00	2019-11-09 03:32:57.631538+00	2	4	372	3
440	2019-11-09 03:32:57.645075+00	2019-11-09 03:32:57.645089+00	2019-11-09 03:32:57.643727+00	2	4	373	3
441	2019-11-09 03:32:57.654752+00	2019-11-09 03:32:57.654764+00	2019-11-09 03:32:57.653617+00	2	4	374	3
442	2019-11-09 03:32:57.664622+00	2019-11-09 03:32:57.664644+00	2019-11-09 03:32:57.662349+00	2	4	365	3
443	2019-11-09 03:32:57.672977+00	2019-11-09 03:32:57.67299+00	2019-11-09 03:32:57.671685+00	2	4	366	3
444	2019-11-11 07:12:31.248383+00	2019-11-11 07:12:31.248414+00	2019-11-11 07:12:31.245766+00	3	4	363	61
445	2019-11-11 07:13:04.973953+00	2019-11-11 07:13:04.973982+00	2019-11-11 07:13:04.97249+00	3	4	325	62
446	2019-11-11 07:13:36.550713+00	2019-11-11 07:13:36.550747+00	2019-11-11 07:13:36.54908+00	3	4	348	63
447	2019-11-11 07:13:56.497285+00	2019-11-11 07:13:56.497309+00	2019-11-11 07:13:56.493335+00	3	4	333	64
448	2019-11-11 07:14:26.97605+00	2019-11-11 07:14:26.976125+00	2019-11-11 07:14:26.973894+00	3	4	324	65
449	2019-11-11 07:15:06.396123+00	2019-11-11 07:15:06.396161+00	2019-11-11 07:15:06.394228+00	3	4	320	66
450	2019-11-11 07:16:21.638979+00	2019-11-11 07:16:21.639017+00	2019-11-11 07:16:21.637385+00	3	4	322	67
451	2019-11-11 07:16:42.56461+00	2019-11-11 07:16:42.564639+00	2019-11-11 07:16:42.5629+00	3	4	326	68
452	2019-11-11 07:16:58.936101+00	2019-11-11 07:16:58.93612+00	2019-11-11 07:16:58.93457+00	3	4	327	69
453	2019-11-11 07:17:10.344753+00	2019-11-11 07:17:10.344775+00	2019-11-11 07:17:10.340569+00	3	4	360	70
454	2019-11-11 07:17:22.881062+00	2019-11-11 07:17:22.881087+00	2019-11-11 07:17:22.879586+00	3	4	338	71
455	2019-11-11 07:17:36.613457+00	2019-11-11 07:17:36.61349+00	2019-11-11 07:17:36.611842+00	3	4	349	72
456	2019-11-11 07:17:48.989139+00	2019-11-11 07:17:48.98916+00	2019-11-11 07:17:48.987049+00	3	4	372	73
457	2019-11-11 07:18:03.380126+00	2019-11-11 07:18:03.380147+00	2019-11-11 07:18:03.378636+00	3	4	365	74
458	2019-11-11 07:18:14.684566+00	2019-11-11 07:18:14.684586+00	2019-11-11 07:18:14.683007+00	3	4	356	75
459	2019-11-11 07:18:25.33597+00	2019-11-11 07:18:25.335992+00	2019-11-11 07:18:25.334427+00	3	4	332	76
460	2019-11-11 07:18:52.472147+00	2019-11-11 07:18:52.472192+00	2019-11-11 07:18:52.470246+00	3	4	329	78
461	2019-11-11 07:19:24.416859+00	2019-11-11 07:19:24.41689+00	2019-11-11 07:19:24.410651+00	3	4	343	60
462	2019-11-11 07:25:03.495695+00	2019-11-11 07:25:03.495729+00	2019-11-11 07:25:03.488946+00	3	4	353	79
463	2019-11-11 07:25:30.838498+00	2019-11-11 07:25:30.838517+00	2019-11-11 07:25:30.837256+00	3	4	272	80
464	2019-11-11 07:26:01.405557+00	2019-11-11 07:26:01.405623+00	2019-11-11 07:26:01.404149+00	3	4	321	81
465	2019-11-11 07:27:03.389276+00	2019-11-11 07:27:03.389296+00	2019-11-11 07:27:03.386161+00	3	4	341	82
466	2019-11-11 07:27:21.176357+00	2019-11-11 07:27:21.176382+00	2019-11-11 07:27:21.175129+00	3	4	368	83
467	2019-11-11 07:27:46.909898+00	2019-11-11 07:27:46.909917+00	2019-11-11 07:27:46.908026+00	3	4	366	84
468	2019-11-11 07:28:01.126204+00	2019-11-11 07:28:01.126232+00	2019-11-11 07:28:01.124805+00	3	4	357	85
469	2019-11-11 07:28:21.446496+00	2019-11-11 07:28:21.446516+00	2019-11-11 07:28:21.444216+00	3	4	373	86
470	2019-11-11 07:28:42.017508+00	2019-11-11 07:28:42.017534+00	2019-11-11 07:28:42.015947+00	3	4	345	87
471	2019-11-11 07:29:17.462176+00	2019-11-11 07:29:17.462211+00	2019-11-11 07:29:17.456487+00	3	4	350	88
472	2019-11-11 07:29:31.607682+00	2019-11-11 07:29:31.607701+00	2019-11-11 07:29:31.606187+00	3	4	330	89
473	2019-11-11 07:29:46.587874+00	2019-11-11 07:29:46.5879+00	2019-11-11 07:29:46.58433+00	3	4	323	90
474	2019-11-11 07:30:03.778925+00	2019-11-11 07:30:03.778952+00	2019-11-11 07:30:03.761971+00	3	4	342	91
475	2019-11-11 07:30:19.259865+00	2019-11-11 07:30:19.259894+00	2019-11-11 07:30:19.256625+00	3	4	331	92
476	2019-11-11 07:30:33.863923+00	2019-11-11 07:30:33.863944+00	2019-11-11 07:30:33.862574+00	3	4	337	93
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

SELECT pg_catalog.setval('auth_permission_id_seq', 180, true);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_id_seq', 10, true);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 56, true);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_content_type_id_seq', 45, true);


--
-- Name: django_migrations_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('django_migrations_id_seq', 36, true);


--
-- Name: gilts_events_castinglisttosevenfiveevent_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('gilts_events_castinglisttosevenfiveevent_id_seq', 1, false);


--
-- Name: gilts_events_giltmerger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('gilts_events_giltmerger_id_seq', 1, false);


--
-- Name: locations_location_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_location_id_seq', 478, true);


--
-- Name: locations_pigletsgroupcell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_pigletsgroupcell_id_seq', 150, true);


--
-- Name: locations_section_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_section_id_seq', 36, true);


--
-- Name: locations_sowandpigletscell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowandpigletscell_id_seq', 270, true);


--
-- Name: locations_sowgroupcell_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('locations_sowgroupcell_id_seq', 12, true);


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

SELECT pg_catalog.setval('locations_workshop_id_seq', 10, true);


--
-- Name: piglets_events_cullingnewbornpiglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_cullingnewbornpiglets_id_seq', 1, false);


--
-- Name: piglets_events_cullingnomadpiglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_cullingnomadpiglets_id_seq', 1, false);


--
-- Name: piglets_events_newbornmergerrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_newbornmergerrecord_id_seq', 1, false);


--
-- Name: piglets_events_newbornpigletsgrouprecount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_newbornpigletsgrouprecount_id_seq', 7, true);


--
-- Name: piglets_events_newbornpigletsmerger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_newbornpigletsmerger_id_seq', 1, false);


--
-- Name: piglets_events_nomadmergerrecord_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_nomadmergerrecord_id_seq', 1, false);


--
-- Name: piglets_events_nomadpigletsgroupmerger_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_nomadpigletsgroupmerger_id_seq', 1, false);


--
-- Name: piglets_events_nomadpigletsgrouprecount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_nomadpigletsgrouprecount_id_seq', 1, false);


--
-- Name: piglets_events_splitnomadpigletsgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_splitnomadpigletsgroup_id_seq', 1, false);


--
-- Name: piglets_events_weighingpiglets_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_events_weighingpiglets_id_seq', 1, false);


--
-- Name: piglets_newbornpigletsgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_newbornpigletsgroup_id_seq', 120, true);


--
-- Name: piglets_nomadpigletsgroup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_nomadpigletsgroup_id_seq', 1, false);


--
-- Name: piglets_pigletsstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('piglets_pigletsstatus_id_seq', 5, true);


--
-- Name: sows_boar_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_boar_id_seq', 18, true);


--
-- Name: sows_events_abortionsow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_abortionsow_id_seq', 1, true);


--
-- Name: sows_events_cullingsow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_cullingsow_id_seq', 7, true);


--
-- Name: sows_events_semination_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_semination_id_seq', 654, true);


--
-- Name: sows_events_sowfarrow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_sowfarrow_id_seq', 142, true);


--
-- Name: sows_events_ultrasound_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_events_ultrasound_id_seq', 489, true);


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
-- Name: sows_giltstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_giltstatus_id_seq', 1, false);


--
-- Name: sows_sow_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_sow_id_seq', 374, true);


--
-- Name: sows_sowstatus_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('sows_sowstatus_id_seq', 10, true);


--
-- Name: staff_workshopemployee_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('staff_workshopemployee_id_seq', 8, true);


--
-- Name: tours_tour_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('tours_tour_id_seq', 5, true);


--
-- Name: transactions_pigletstransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transactions_pigletstransaction_id_seq', 1, false);


--
-- Name: transactions_sowtransaction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('transactions_sowtransaction_id_seq', 476, true);


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
-- Name: gilts_events_castinglisttosevenfiveevent gilts_events_castinglisttosevenfiveevent_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_castinglisttosevenfiveevent
    ADD CONSTRAINT gilts_events_castinglisttosevenfiveevent_pkey PRIMARY KEY (id);


--
-- Name: gilts_events_giltmerger gilts_events_giltmerger_nomad_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_giltmerger
    ADD CONSTRAINT gilts_events_giltmerger_nomad_group_id_key UNIQUE (nomad_group_id);


--
-- Name: gilts_events_giltmerger gilts_events_giltmerger_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_giltmerger
    ADD CONSTRAINT gilts_events_giltmerger_pkey PRIMARY KEY (id);


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
-- Name: piglets_events_cullingnewbornpiglets piglets_events_cullingnewbornpiglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnewbornpiglets
    ADD CONSTRAINT piglets_events_cullingnewbornpiglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_cullingnomadpiglets piglets_events_cullingnomadpiglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnomadpiglets
    ADD CONSTRAINT piglets_events_cullingnomadpiglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_newbornmergerrecord piglets_events_newbornmergerrecord_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornmergerrecord
    ADD CONSTRAINT piglets_events_newbornmergerrecord_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_newbornpigletsgrouprecount piglets_events_newbornpigletsgrouprecount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsgrouprecount
    ADD CONSTRAINT piglets_events_newbornpigletsgrouprecount_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_newbornpigletsmerger piglets_events_newbornpigletsmerger_nomad_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsmerger
    ADD CONSTRAINT piglets_events_newbornpigletsmerger_nomad_group_id_key UNIQUE (nomad_group_id);


--
-- Name: piglets_events_newbornpigletsmerger piglets_events_newbornpigletsmerger_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsmerger
    ADD CONSTRAINT piglets_events_newbornpigletsmerger_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_nomadmergerrecord piglets_events_nomadmergerrecord_nomad_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadmergerrecord
    ADD CONSTRAINT piglets_events_nomadmergerrecord_nomad_group_id_key UNIQUE (nomad_group_id);


--
-- Name: piglets_events_nomadmergerrecord piglets_events_nomadmergerrecord_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadmergerrecord
    ADD CONSTRAINT piglets_events_nomadmergerrecord_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_nomadpigletsgroupmerger piglets_events_nomadpigletsgroupmerger_nomad_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger
    ADD CONSTRAINT piglets_events_nomadpigletsgroupmerger_nomad_group_id_key UNIQUE (nomad_group_id);


--
-- Name: piglets_events_nomadpigletsgroupmerger piglets_events_nomadpigletsgroupmerger_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger
    ADD CONSTRAINT piglets_events_nomadpigletsgroupmerger_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_nomadpigletsgrouprecount piglets_events_nomadpigletsgrouprecount_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgrouprecount
    ADD CONSTRAINT piglets_events_nomadpigletsgrouprecount_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_splitnomadpigletsgroup piglets_events_splitnomadpigletsgroup_parent_group_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_splitnomadpigletsgroup
    ADD CONSTRAINT piglets_events_splitnomadpigletsgroup_parent_group_id_key UNIQUE (parent_group_id);


--
-- Name: piglets_events_splitnomadpigletsgroup piglets_events_splitnomadpigletsgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_splitnomadpigletsgroup
    ADD CONSTRAINT piglets_events_splitnomadpigletsgroup_pkey PRIMARY KEY (id);


--
-- Name: piglets_events_weighingpiglets piglets_events_weighingpiglets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weighingpiglets_pkey PRIMARY KEY (id);


--
-- Name: piglets_newbornpigletsgroup piglets_newbornpigletsgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup
    ADD CONSTRAINT piglets_newbornpigletsgroup_pkey PRIMARY KEY (id);


--
-- Name: piglets_nomadpigletsgroup piglets_nomadpigletsgroup_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup
    ADD CONSTRAINT piglets_nomadpigletsgroup_pkey PRIMARY KEY (id);


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
-- Name: sows_giltstatus sows_giltstatus_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_giltstatus
    ADD CONSTRAINT sows_giltstatus_pkey PRIMARY KEY (id);


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
-- Name: gilts_events_castinglisttosevenfiveevent_initiator_id_5c06bf5e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gilts_events_castinglisttosevenfiveevent_initiator_id_5c06bf5e ON gilts_events_castinglisttosevenfiveevent USING btree (initiator_id);


--
-- Name: gilts_events_giltmerger_initiator_id_49f4e90a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX gilts_events_giltmerger_initiator_id_49f4e90a ON gilts_events_giltmerger USING btree (initiator_id);


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
-- Name: piglets_events_cullingnewbornpiglets_initiator_id_8bafe4e7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingnewbornpiglets_initiator_id_8bafe4e7 ON piglets_events_cullingnewbornpiglets USING btree (initiator_id);


--
-- Name: piglets_events_cullingnewbornpiglets_piglets_group_id_089a7796; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingnewbornpiglets_piglets_group_id_089a7796 ON piglets_events_cullingnewbornpiglets USING btree (piglets_group_id);


--
-- Name: piglets_events_cullingnomadpiglets_initiator_id_eec93a2d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingnomadpiglets_initiator_id_eec93a2d ON piglets_events_cullingnomadpiglets USING btree (initiator_id);


--
-- Name: piglets_events_cullingnomadpiglets_piglets_group_id_3f9a1f84; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_cullingnomadpiglets_piglets_group_id_3f9a1f84 ON piglets_events_cullingnomadpiglets USING btree (piglets_group_id);


--
-- Name: piglets_events_newbornmergerrecord_merger_id_fd4326e1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_newbornmergerrecord_merger_id_fd4326e1 ON piglets_events_newbornmergerrecord USING btree (merger_id);


--
-- Name: piglets_events_newbornmergerrecord_tour_id_36366dbd; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_newbornmergerrecord_tour_id_36366dbd ON piglets_events_newbornmergerrecord USING btree (tour_id);


--
-- Name: piglets_events_newbornpigl_piglets_group_id_a7336c97; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_newbornpigl_piglets_group_id_a7336c97 ON piglets_events_newbornpigletsgrouprecount USING btree (piglets_group_id);


--
-- Name: piglets_events_newbornpigletsgrouprecount_initiator_id_8f77e311; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_newbornpigletsgrouprecount_initiator_id_8f77e311 ON piglets_events_newbornpigletsgrouprecount USING btree (initiator_id);


--
-- Name: piglets_events_newbornpigletsmerger_initiator_id_b1b82d84; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_newbornpigletsmerger_initiator_id_b1b82d84 ON piglets_events_newbornpigletsmerger USING btree (initiator_id);


--
-- Name: piglets_events_nomadmergerrecord_merger_id_bd71c2d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_nomadmergerrecord_merger_id_bd71c2d7 ON piglets_events_nomadmergerrecord USING btree (merger_id);


--
-- Name: piglets_events_nomadpiglet_piglets_group_id_a85656da; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_nomadpiglet_piglets_group_id_a85656da ON piglets_events_nomadpigletsgrouprecount USING btree (piglets_group_id);


--
-- Name: piglets_events_nomadpigletsgroupmerger_initiator_id_71c250ff; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_nomadpigletsgroupmerger_initiator_id_71c250ff ON piglets_events_nomadpigletsgroupmerger USING btree (initiator_id);


--
-- Name: piglets_events_nomadpigletsgroupmerger_new_location_id_3a1b522d; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_nomadpigletsgroupmerger_new_location_id_3a1b522d ON piglets_events_nomadpigletsgroupmerger USING btree (new_location_id);


--
-- Name: piglets_events_nomadpigletsgrouprecount_initiator_id_64298381; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_nomadpigletsgrouprecount_initiator_id_64298381 ON piglets_events_nomadpigletsgrouprecount USING btree (initiator_id);


--
-- Name: piglets_events_splitnomadpigletsgroup_initiator_id_5f577a20; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_splitnomadpigletsgroup_initiator_id_5f577a20 ON piglets_events_splitnomadpigletsgroup USING btree (initiator_id);


--
-- Name: piglets_events_weighingpiglets_initiator_id_bf3278d7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_weighingpiglets_initiator_id_bf3278d7 ON piglets_events_weighingpiglets USING btree (initiator_id);


--
-- Name: piglets_events_weighingpiglets_piglets_group_id_e55cd7f7; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_events_weighingpiglets_piglets_group_id_e55cd7f7 ON piglets_events_weighingpiglets USING btree (piglets_group_id);


--
-- Name: piglets_newbornpigletsgroup_location_id_32ceba9c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_newbornpigletsgroup_location_id_32ceba9c ON piglets_newbornpigletsgroup USING btree (location_id);


--
-- Name: piglets_newbornpigletsgroup_merger_id_758f45d8; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_newbornpigletsgroup_merger_id_758f45d8 ON piglets_newbornpigletsgroup USING btree (merger_id);


--
-- Name: piglets_newbornpigletsgroup_status_id_c51ed2db; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_newbornpigletsgroup_status_id_c51ed2db ON piglets_newbornpigletsgroup USING btree (status_id);


--
-- Name: piglets_newbornpigletsgroup_tour_id_5dcff7ec; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_newbornpigletsgroup_tour_id_5dcff7ec ON piglets_newbornpigletsgroup USING btree (tour_id);


--
-- Name: piglets_nomadpigletsgroup_groups_merger_id_11a8d0d1; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_nomadpigletsgroup_groups_merger_id_11a8d0d1 ON piglets_nomadpigletsgroup USING btree (groups_merger_id);


--
-- Name: piglets_nomadpigletsgroup_location_id_140aacae; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_nomadpigletsgroup_location_id_140aacae ON piglets_nomadpigletsgroup USING btree (location_id);


--
-- Name: piglets_nomadpigletsgroup_split_record_id_25fba887; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_nomadpigletsgroup_split_record_id_25fba887 ON piglets_nomadpigletsgroup USING btree (split_record_id);


--
-- Name: piglets_nomadpigletsgroup_status_id_6190ec1c; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX piglets_nomadpigletsgroup_status_id_6190ec1c ON piglets_nomadpigletsgroup USING btree (status_id);


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
-- Name: sows_events_sowfarrow_new_born_piglets_group_id_3ce96d73; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_sowfarrow_new_born_piglets_group_id_3ce96d73 ON sows_events_sowfarrow USING btree (new_born_piglets_group_id);


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
-- Name: sows_events_weaningsow_transaction_id_969218f5; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_events_weaningsow_transaction_id_969218f5 ON sows_events_weaningsow USING btree (transaction_id);


--
-- Name: sows_gilt_birth_id_a4289b2d_like; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_birth_id_a4289b2d_like ON sows_gilt USING btree (birth_id varchar_pattern_ops);


--
-- Name: sows_gilt_casting_list_to_seven_five_id_c604ae8f; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_casting_list_to_seven_five_id_c604ae8f ON sows_gilt USING btree (casting_list_to_seven_five_id);


--
-- Name: sows_gilt_location_id_6e9d5445; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_location_id_6e9d5445 ON sows_gilt USING btree (location_id);


--
-- Name: sows_gilt_merger_id_874a8dc3; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_merger_id_874a8dc3 ON sows_gilt USING btree (merger_id);


--
-- Name: sows_gilt_mother_sow_id_c2fedd8a; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_mother_sow_id_c2fedd8a ON sows_gilt USING btree (mother_sow_id);


--
-- Name: sows_gilt_new_born_group_id_a94b121e; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_new_born_group_id_a94b121e ON sows_gilt USING btree (new_born_group_id);


--
-- Name: sows_gilt_status_id_9bf9b3a4; Type: INDEX; Schema: public; Owner: postgres
--

CREATE INDEX sows_gilt_status_id_9bf9b3a4 ON sows_gilt USING btree (status_id);


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
-- Name: gilts_events_castinglisttosevenfiveevent gilts_events_casting_initiator_id_5c06bf5e_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_castinglisttosevenfiveevent
    ADD CONSTRAINT gilts_events_casting_initiator_id_5c06bf5e_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gilts_events_giltmerger gilts_events_giltmer_nomad_group_id_68bd4e72_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_giltmerger
    ADD CONSTRAINT gilts_events_giltmer_nomad_group_id_68bd4e72_fk_piglets_n FOREIGN KEY (nomad_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: gilts_events_giltmerger gilts_events_giltmerger_initiator_id_49f4e90a_fk_auth_user_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY gilts_events_giltmerger
    ADD CONSTRAINT gilts_events_giltmerger_initiator_id_49f4e90a_fk_auth_user_id FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: piglets_events_cullingnewbornpiglets piglets_events_culli_initiator_id_8bafe4e7_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnewbornpiglets
    ADD CONSTRAINT piglets_events_culli_initiator_id_8bafe4e7_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_cullingnomadpiglets piglets_events_culli_initiator_id_eec93a2d_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnomadpiglets
    ADD CONSTRAINT piglets_events_culli_initiator_id_eec93a2d_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_cullingnewbornpiglets piglets_events_culli_piglets_group_id_089a7796_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnewbornpiglets
    ADD CONSTRAINT piglets_events_culli_piglets_group_id_089a7796_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_newbornpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_cullingnomadpiglets piglets_events_culli_piglets_group_id_3f9a1f84_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_cullingnomadpiglets
    ADD CONSTRAINT piglets_events_culli_piglets_group_id_3f9a1f84_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornpigletsgrouprecount piglets_events_newbo_initiator_id_8f77e311_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsgrouprecount
    ADD CONSTRAINT piglets_events_newbo_initiator_id_8f77e311_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornpigletsmerger piglets_events_newbo_initiator_id_b1b82d84_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsmerger
    ADD CONSTRAINT piglets_events_newbo_initiator_id_b1b82d84_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornmergerrecord piglets_events_newbo_merger_id_fd4326e1_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornmergerrecord
    ADD CONSTRAINT piglets_events_newbo_merger_id_fd4326e1_fk_piglets_e FOREIGN KEY (merger_id) REFERENCES piglets_events_newbornpigletsmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornpigletsmerger piglets_events_newbo_nomad_group_id_25804e95_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsmerger
    ADD CONSTRAINT piglets_events_newbo_nomad_group_id_25804e95_fk_piglets_n FOREIGN KEY (nomad_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornpigletsgrouprecount piglets_events_newbo_piglets_group_id_a7336c97_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornpigletsgrouprecount
    ADD CONSTRAINT piglets_events_newbo_piglets_group_id_a7336c97_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_newbornpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_newbornmergerrecord piglets_events_newbo_tour_id_36366dbd_fk_tours_tou; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_newbornmergerrecord
    ADD CONSTRAINT piglets_events_newbo_tour_id_36366dbd_fk_tours_tou FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadpigletsgrouprecount piglets_events_nomad_initiator_id_64298381_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgrouprecount
    ADD CONSTRAINT piglets_events_nomad_initiator_id_64298381_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadpigletsgroupmerger piglets_events_nomad_initiator_id_71c250ff_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger
    ADD CONSTRAINT piglets_events_nomad_initiator_id_71c250ff_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadmergerrecord piglets_events_nomad_merger_id_bd71c2d7_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadmergerrecord
    ADD CONSTRAINT piglets_events_nomad_merger_id_bd71c2d7_fk_piglets_e FOREIGN KEY (merger_id) REFERENCES piglets_events_nomadpigletsgroupmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadpigletsgroupmerger piglets_events_nomad_new_location_id_3a1b522d_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger
    ADD CONSTRAINT piglets_events_nomad_new_location_id_3a1b522d_fk_locations FOREIGN KEY (new_location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadpigletsgroupmerger piglets_events_nomad_nomad_group_id_130bd590_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgroupmerger
    ADD CONSTRAINT piglets_events_nomad_nomad_group_id_130bd590_fk_piglets_n FOREIGN KEY (nomad_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadmergerrecord piglets_events_nomad_nomad_group_id_2d706dad_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadmergerrecord
    ADD CONSTRAINT piglets_events_nomad_nomad_group_id_2d706dad_fk_piglets_n FOREIGN KEY (nomad_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_nomadpigletsgrouprecount piglets_events_nomad_piglets_group_id_a85656da_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_nomadpigletsgrouprecount
    ADD CONSTRAINT piglets_events_nomad_piglets_group_id_a85656da_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_splitnomadpigletsgroup piglets_events_split_initiator_id_5f577a20_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_splitnomadpigletsgroup
    ADD CONSTRAINT piglets_events_split_initiator_id_5f577a20_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_splitnomadpigletsgroup piglets_events_split_parent_group_id_f9f72610_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_splitnomadpigletsgroup
    ADD CONSTRAINT piglets_events_split_parent_group_id_f9f72610_fk_piglets_n FOREIGN KEY (parent_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_weighingpiglets piglets_events_weigh_initiator_id_bf3278d7_fk_auth_user; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weigh_initiator_id_bf3278d7_fk_auth_user FOREIGN KEY (initiator_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_events_weighingpiglets piglets_events_weigh_piglets_group_id_e55cd7f7_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_events_weighingpiglets
    ADD CONSTRAINT piglets_events_weigh_piglets_group_id_e55cd7f7_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_newbornpigletsgroup piglets_newbornpigle_location_id_32ceba9c_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup
    ADD CONSTRAINT piglets_newbornpigle_location_id_32ceba9c_fk_locations FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_newbornpigletsgroup piglets_newbornpigle_merger_id_758f45d8_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup
    ADD CONSTRAINT piglets_newbornpigle_merger_id_758f45d8_fk_piglets_e FOREIGN KEY (merger_id) REFERENCES piglets_events_newbornpigletsmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_newbornpigletsgroup piglets_newbornpigle_status_id_c51ed2db_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup
    ADD CONSTRAINT piglets_newbornpigle_status_id_c51ed2db_fk_piglets_p FOREIGN KEY (status_id) REFERENCES piglets_pigletsstatus(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_newbornpigletsgroup piglets_newbornpigletsgroup_tour_id_5dcff7ec_fk_tours_tour_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_newbornpigletsgroup
    ADD CONSTRAINT piglets_newbornpigletsgroup_tour_id_5dcff7ec_fk_tours_tour_id FOREIGN KEY (tour_id) REFERENCES tours_tour(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_nomadpigletsgroup piglets_nomadpiglets_groups_merger_id_11a8d0d1_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup
    ADD CONSTRAINT piglets_nomadpiglets_groups_merger_id_11a8d0d1_fk_piglets_e FOREIGN KEY (groups_merger_id) REFERENCES piglets_events_nomadpigletsgroupmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_nomadpigletsgroup piglets_nomadpiglets_location_id_140aacae_fk_locations; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup
    ADD CONSTRAINT piglets_nomadpiglets_location_id_140aacae_fk_locations FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_nomadpigletsgroup piglets_nomadpiglets_split_record_id_25fba887_fk_piglets_e; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup
    ADD CONSTRAINT piglets_nomadpiglets_split_record_id_25fba887_fk_piglets_e FOREIGN KEY (split_record_id) REFERENCES piglets_events_splitnomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: piglets_nomadpigletsgroup piglets_nomadpiglets_status_id_6190ec1c_fk_piglets_p; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY piglets_nomadpigletsgroup
    ADD CONSTRAINT piglets_nomadpiglets_status_id_6190ec1c_fk_piglets_p FOREIGN KEY (status_id) REFERENCES piglets_pigletsstatus(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: sows_events_sowfarrow sows_events_sowfarro_new_born_piglets_gro_3ce96d73_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_sowfarrow
    ADD CONSTRAINT sows_events_sowfarro_new_born_piglets_gro_3ce96d73_fk_piglets_n FOREIGN KEY (new_born_piglets_group_id) REFERENCES piglets_newbornpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: sows_events_weaningsow sows_events_weanings_transaction_id_969218f5_fk_transacti; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_events_weaningsow
    ADD CONSTRAINT sows_events_weanings_transaction_id_969218f5_fk_transacti FOREIGN KEY (transaction_id) REFERENCES transactions_sowtransaction(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: sows_gilt sows_gilt_casting_list_to_seve_c604ae8f_fk_gilts_eve; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_casting_list_to_seve_c604ae8f_fk_gilts_eve FOREIGN KEY (casting_list_to_seven_five_id) REFERENCES gilts_events_castinglisttosevenfiveevent(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_location_id_6e9d5445_fk_locations_location_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_location_id_6e9d5445_fk_locations_location_id FOREIGN KEY (location_id) REFERENCES locations_location(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_merger_id_874a8dc3_fk_gilts_events_giltmerger_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_merger_id_874a8dc3_fk_gilts_events_giltmerger_id FOREIGN KEY (merger_id) REFERENCES gilts_events_giltmerger(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_mother_sow_id_c2fedd8a_fk_sows_sow_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_mother_sow_id_c2fedd8a_fk_sows_sow_id FOREIGN KEY (mother_sow_id) REFERENCES sows_sow(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_new_born_group_id_a94b121e_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_new_born_group_id_a94b121e_fk_piglets_n FOREIGN KEY (new_born_group_id) REFERENCES piglets_newbornpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: sows_gilt sows_gilt_status_id_9bf9b3a4_fk_sows_giltstatus_id; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY sows_gilt
    ADD CONSTRAINT sows_gilt_status_id_9bf9b3a4_fk_sows_giltstatus_id FOREIGN KEY (status_id) REFERENCES sows_giltstatus(id) DEFERRABLE INITIALLY DEFERRED;


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
-- Name: transactions_pigletstransaction transactions_piglets_piglets_group_id_dd2560ba_fk_piglets_n; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY transactions_pigletstransaction
    ADD CONSTRAINT transactions_piglets_piglets_group_id_dd2560ba_fk_piglets_n FOREIGN KEY (piglets_group_id) REFERENCES piglets_nomadpigletsgroup(id) DEFERRABLE INITIALLY DEFERRED;


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

