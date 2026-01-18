--
-- PostgreSQL database dump
--

\restrict Il568coIjtnOJqB6dU3w8kwimQTVQCqtbHPQSH4ayth9vQICqHuJweU4kUWvfJb

-- Dumped from database version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.11 (Ubuntu 16.11-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: test_backup; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_backup (
    id integer NOT NULL
);


ALTER TABLE public.test_backup OWNER TO postgres;

--
-- Name: test_backup_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_backup_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_backup_id_seq OWNER TO postgres;

--
-- Name: test_backup_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_backup_id_seq OWNED BY public.test_backup.id;


--
-- Name: test_failover; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_failover (
    id integer NOT NULL
);


ALTER TABLE public.test_failover OWNER TO postgres;

--
-- Name: test_failover_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_failover_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_failover_id_seq OWNER TO postgres;

--
-- Name: test_failover_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_failover_id_seq OWNED BY public.test_failover.id;


--
-- Name: test_final; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.test_final (
    id integer NOT NULL
);


ALTER TABLE public.test_final OWNER TO postgres;

--
-- Name: test_final_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.test_final_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.test_final_id_seq OWNER TO postgres;

--
-- Name: test_final_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.test_final_id_seq OWNED BY public.test_final.id;


--
-- Name: test_backup id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_backup ALTER COLUMN id SET DEFAULT nextval('public.test_backup_id_seq'::regclass);


--
-- Name: test_failover id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_failover ALTER COLUMN id SET DEFAULT nextval('public.test_failover_id_seq'::regclass);


--
-- Name: test_final id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.test_final ALTER COLUMN id SET DEFAULT nextval('public.test_final_id_seq'::regclass);


--
-- Data for Name: test_backup; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_backup (id) FROM stdin;
\.


--
-- Data for Name: test_failover; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_failover (id) FROM stdin;
\.


--
-- Data for Name: test_final; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.test_final (id) FROM stdin;
\.


--
-- Name: test_backup_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_backup_id_seq', 1, false);


--
-- Name: test_failover_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_failover_id_seq', 1, false);


--
-- Name: test_final_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.test_final_id_seq', 1, false);


--
-- PostgreSQL database dump complete
--

\unrestrict Il568coIjtnOJqB6dU3w8kwimQTVQCqtbHPQSH4ayth9vQICqHuJweU4kUWvfJb

