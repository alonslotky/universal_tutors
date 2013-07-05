--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'SQL_ASCII';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: auth_group; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


--
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- Name: auth_group_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_group_id_seq', 1, false);


--
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_group_permissions_id_seq', 1, false);


--
-- Name: auth_message; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_message (
    id integer NOT NULL,
    user_id integer NOT NULL,
    message text NOT NULL
);


--
-- Name: auth_message_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_message_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_message_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_message_id_seq OWNED BY auth_message.id;


--
-- Name: auth_message_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_message_id_seq', 1, false);


--
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


--
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- Name: auth_permission_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_permission_id_seq', 94, true);


--
-- Name: auth_user; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user (
    id integer NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    password character varying(128) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    is_superuser boolean NOT NULL,
    last_login timestamp with time zone NOT NULL,
    date_joined timestamp with time zone NOT NULL
);


--
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_id_seq', 2, true);


--
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('auth_user_user_permissions_id_seq', 1, false);


--
-- Name: classes_class; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE classes_class (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    tutor_id integer NOT NULL,
    student_id integer NOT NULL,
    date date NOT NULL,
    start time without time zone NOT NULL,
    "end" time without time zone NOT NULL,
    credit_fee double precision NOT NULL,
    scribblar_id character varying(100),
    name character varying(100) NOT NULL
);


--
-- Name: classes_class_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE classes_class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: classes_class_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE classes_class_id_seq OWNED BY classes_class.id;


--
-- Name: classes_class_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('classes_class_id_seq', 2, true);


--
-- Name: classes_class_subject; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE classes_class_subject (
    id integer NOT NULL,
    class_id integer NOT NULL,
    classsubject_id integer NOT NULL
);


--
-- Name: classes_class_subject_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE classes_class_subject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: classes_class_subject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE classes_class_subject_id_seq OWNED BY classes_class_subject.id;


--
-- Name: classes_class_subject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('classes_class_subject_id_seq', 2, true);


--
-- Name: classes_classsubject; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE classes_classsubject (
    id integer NOT NULL,
    subject character varying(30) NOT NULL
);


--
-- Name: classes_classsubject_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE classes_classsubject_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: classes_classsubject_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE classes_classsubject_id_seq OWNED BY classes_classsubject.id;


--
-- Name: classes_classsubject_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('classes_classsubject_id_seq', 1, true);


--
-- Name: classes_classuserhistory; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE classes_classuserhistory (
    id integer NOT NULL,
    _class_id integer NOT NULL,
    user_id integer NOT NULL,
    enter timestamp with time zone NOT NULL,
    leave timestamp with time zone NOT NULL
);


--
-- Name: classes_classuserhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE classes_classuserhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: classes_classuserhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE classes_classuserhistory_id_seq OWNED BY classes_classuserhistory.id;


--
-- Name: classes_classuserhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('classes_classuserhistory_id_seq', 1, false);


--
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL,
    CONSTRAINT django_admin_log_action_flag_check CHECK ((action_flag >= 0))
);


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_admin_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_admin_log_id_seq OWNED BY django_admin_log.id;


--
-- Name: django_admin_log_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_admin_log_id_seq', 9, true);


--
-- Name: django_comment_flags; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_comment_flags (
    id integer NOT NULL,
    user_id integer NOT NULL,
    comment_id integer NOT NULL,
    flag character varying(30) NOT NULL,
    flag_date timestamp with time zone NOT NULL
);


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_comment_flags_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_comment_flags_id_seq OWNED BY django_comment_flags.id;


--
-- Name: django_comment_flags_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_comment_flags_id_seq', 1, false);


--
-- Name: django_comments; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_comments (
    id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_pk text NOT NULL,
    site_id integer NOT NULL,
    user_id integer,
    user_name character varying(50) NOT NULL,
    user_email character varying(75) NOT NULL,
    user_url character varying(200) NOT NULL,
    comment text NOT NULL,
    submit_date timestamp with time zone NOT NULL,
    ip_address inet,
    is_public boolean NOT NULL,
    is_removed boolean NOT NULL
);


--
-- Name: django_comments_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_comments_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_comments_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_comments_id_seq OWNED BY django_comments.id;


--
-- Name: django_comments_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_comments_id_seq', 1, false);


--
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


--
-- Name: django_content_type_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_content_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_content_type_id_seq OWNED BY django_content_type.id;


--
-- Name: django_content_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_content_type_id_seq', 31, true);


--
-- Name: django_flatpage; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_flatpage (
    id integer NOT NULL,
    url character varying(100) NOT NULL,
    title character varying(200) NOT NULL,
    content text NOT NULL,
    enable_comments boolean NOT NULL,
    template_name character varying(70) NOT NULL,
    registration_required boolean NOT NULL
);


--
-- Name: django_flatpage_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_flatpage_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_flatpage_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_flatpage_id_seq OWNED BY django_flatpage.id;


--
-- Name: django_flatpage_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_flatpage_id_seq', 1, false);


--
-- Name: django_flatpage_sites; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_flatpage_sites (
    id integer NOT NULL,
    flatpage_id integer NOT NULL,
    site_id integer NOT NULL
);


--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_flatpage_sites_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_flatpage_sites_id_seq OWNED BY django_flatpage_sites.id;


--
-- Name: django_flatpage_sites_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_flatpage_sites_id_seq', 1, false);


--
-- Name: django_session; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


--
-- Name: django_site; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: django_site_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE django_site_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: django_site_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE django_site_id_seq OWNED BY django_site.id;


--
-- Name: django_site_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('django_site_id_seq', 1, true);


--
-- Name: emailconfirmation_emailaddress; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE emailconfirmation_emailaddress (
    id integer NOT NULL,
    user_id integer NOT NULL,
    email character varying(75) NOT NULL,
    verified boolean NOT NULL,
    "primary" boolean NOT NULL
);


--
-- Name: emailconfirmation_emailaddress_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE emailconfirmation_emailaddress_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: emailconfirmation_emailaddress_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE emailconfirmation_emailaddress_id_seq OWNED BY emailconfirmation_emailaddress.id;


--
-- Name: emailconfirmation_emailaddress_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('emailconfirmation_emailaddress_id_seq', 1, false);


--
-- Name: emailconfirmation_emailconfirmation; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE emailconfirmation_emailconfirmation (
    id integer NOT NULL,
    email_address_id integer NOT NULL,
    sent timestamp with time zone NOT NULL,
    confirmation_key character varying(40) NOT NULL
);


--
-- Name: emailconfirmation_emailconfirmation_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE emailconfirmation_emailconfirmation_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: emailconfirmation_emailconfirmation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE emailconfirmation_emailconfirmation_id_seq OWNED BY emailconfirmation_emailconfirmation.id;


--
-- Name: emailconfirmation_emailconfirmation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('emailconfirmation_emailconfirmation_id_seq', 1, false);


--
-- Name: facebook_facebookaccesstoken; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE facebook_facebookaccesstoken (
    id integer NOT NULL,
    app_id integer NOT NULL,
    account_id integer NOT NULL,
    access_token character varying(200) NOT NULL
);


--
-- Name: facebook_facebookaccesstoken_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE facebook_facebookaccesstoken_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: facebook_facebookaccesstoken_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE facebook_facebookaccesstoken_id_seq OWNED BY facebook_facebookaccesstoken.id;


--
-- Name: facebook_facebookaccesstoken_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('facebook_facebookaccesstoken_id_seq', 1, false);


--
-- Name: facebook_facebookaccount; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE facebook_facebookaccount (
    socialaccount_ptr_id integer NOT NULL,
    social_id character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    link character varying(200) NOT NULL
);


--
-- Name: facebook_facebookapp; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE facebook_facebookapp (
    id integer NOT NULL,
    site_id integer NOT NULL,
    name character varying(40) NOT NULL,
    application_id character varying(80) NOT NULL,
    api_key character varying(80) NOT NULL,
    application_secret character varying(80) NOT NULL
);


--
-- Name: facebook_facebookapp_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE facebook_facebookapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: facebook_facebookapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE facebook_facebookapp_id_seq OWNED BY facebook_facebookapp.id;


--
-- Name: facebook_facebookapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('facebook_facebookapp_id_seq', 1, true);


--
-- Name: openid_openidaccount; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE openid_openidaccount (
    socialaccount_ptr_id integer NOT NULL,
    identity character varying(255) NOT NULL
);


--
-- Name: openid_openidnonce; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE openid_openidnonce (
    id integer NOT NULL,
    server_url character varying(255) NOT NULL,
    "timestamp" integer NOT NULL,
    salt character varying(255) NOT NULL,
    date_created timestamp with time zone NOT NULL
);


--
-- Name: openid_openidnonce_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE openid_openidnonce_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: openid_openidnonce_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE openid_openidnonce_id_seq OWNED BY openid_openidnonce.id;


--
-- Name: openid_openidnonce_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('openid_openidnonce_id_seq', 1, false);


--
-- Name: openid_openidstore; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE openid_openidstore (
    id integer NOT NULL,
    server_url character varying(255) NOT NULL,
    handle character varying(255) NOT NULL,
    secret text NOT NULL,
    issued integer NOT NULL,
    lifetime integer NOT NULL,
    assoc_type text NOT NULL
);


--
-- Name: openid_openidstore_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE openid_openidstore_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: openid_openidstore_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE openid_openidstore_id_seq OWNED BY openid_openidstore.id;


--
-- Name: openid_openidstore_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('openid_openidstore_id_seq', 1, false);


--
-- Name: profile_child; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE profile_child (
    id integer NOT NULL,
    parent_id integer NOT NULL,
    child_id integer NOT NULL,
    active boolean NOT NULL,
    key character varying(30)
);


--
-- Name: profile_child_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE profile_child_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: profile_child_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE profile_child_id_seq OWNED BY profile_child.id;


--
-- Name: profile_child_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('profile_child_id_seq', 1, false);


--
-- Name: profile_newslettersubscription; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE profile_newslettersubscription (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    email character varying(255) NOT NULL,
    email_verified boolean DEFAULT false NOT NULL,
    hash_key character varying(20) NOT NULL
);


--
-- Name: profile_newslettersubscription_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE profile_newslettersubscription_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: profile_newslettersubscription_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE profile_newslettersubscription_id_seq OWNED BY profile_newslettersubscription.id;


--
-- Name: profile_newslettersubscription_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('profile_newslettersubscription_id_seq', 1, false);


--
-- Name: profile_userprofile; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE profile_userprofile (
    id integer NOT NULL,
    created timestamp with time zone NOT NULL,
    updated timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    about character varying(500),
    title character varying(100),
    profile_image character varying(100) NOT NULL,
    address character varying(150),
    location character varying(50),
    postcode character varying(10),
    country character varying(2),
    phone character varying(20),
    newsletters boolean DEFAULT true NOT NULL,
    type smallint NOT NULL,
    credit double precision NOT NULL,
    income double precision NOT NULL,
    referral smallint NOT NULL,
    date_of_birth date,
    scribblar_id character varying(100),
    subjects_id integer,
    CONSTRAINT ck_referral_pstv_5aeaec95 CHECK ((referral >= 0)),
    CONSTRAINT ck_type_pstv_410696c8 CHECK ((type >= 0)),
    CONSTRAINT profile_userprofile_referral_check CHECK ((referral >= 0)),
    CONSTRAINT profile_userprofile_type_check CHECK ((type >= 0))
);


--
-- Name: profile_userprofile_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE profile_userprofile_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: profile_userprofile_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE profile_userprofile_id_seq OWNED BY profile_userprofile.id;


--
-- Name: profile_userprofile_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('profile_userprofile_id_seq', 2, true);


--
-- Name: socialaccount_socialaccount; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE socialaccount_socialaccount (
    id integer NOT NULL,
    user_id integer NOT NULL,
    last_login timestamp with time zone DEFAULT '2012-04-23 10:36:11.630459+00'::timestamp with time zone NOT NULL,
    date_joined timestamp with time zone DEFAULT '2012-04-23 10:36:11.630678+00'::timestamp with time zone NOT NULL
);


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE socialaccount_socialaccount_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE socialaccount_socialaccount_id_seq OWNED BY socialaccount_socialaccount.id;


--
-- Name: socialaccount_socialaccount_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('socialaccount_socialaccount_id_seq', 1, false);


--
-- Name: south_migrationhistory; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE south_migrationhistory (
    id integer NOT NULL,
    app_name character varying(255) NOT NULL,
    migration character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE south_migrationhistory_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE south_migrationhistory_id_seq OWNED BY south_migrationhistory.id;


--
-- Name: south_migrationhistory_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('south_migrationhistory_id_seq', 16, true);


--
-- Name: tagging_tag; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE tagging_tag (
    id integer NOT NULL,
    name character varying(50) NOT NULL
);


--
-- Name: tagging_tag_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE tagging_tag_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: tagging_tag_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE tagging_tag_id_seq OWNED BY tagging_tag.id;


--
-- Name: tagging_tag_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('tagging_tag_id_seq', 1, false);


--
-- Name: tagging_taggeditem; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE tagging_taggeditem (
    id integer NOT NULL,
    tag_id integer NOT NULL,
    content_type_id integer NOT NULL,
    object_id integer NOT NULL,
    CONSTRAINT tagging_taggeditem_object_id_check CHECK ((object_id >= 0))
);


--
-- Name: tagging_taggeditem_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE tagging_taggeditem_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: tagging_taggeditem_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE tagging_taggeditem_id_seq OWNED BY tagging_taggeditem.id;


--
-- Name: tagging_taggeditem_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('tagging_taggeditem_id_seq', 1, false);


--
-- Name: twitter_twitteraccount; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE twitter_twitteraccount (
    socialaccount_ptr_id integer NOT NULL,
    social_id bigint NOT NULL,
    username character varying(15) NOT NULL,
    profile_image_url character varying(200) NOT NULL
);


--
-- Name: twitter_twitterapp; Type: TABLE; Schema: public; Owner: -; Tablespace: 
--

CREATE TABLE twitter_twitterapp (
    id integer NOT NULL,
    site_id integer NOT NULL,
    name character varying(40) NOT NULL,
    consumer_key character varying(80) NOT NULL,
    consumer_secret character varying(80) NOT NULL,
    request_token_url character varying(200) NOT NULL,
    access_token_url character varying(200) NOT NULL,
    authorize_url character varying(200) NOT NULL
);


--
-- Name: twitter_twitterapp_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE twitter_twitterapp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


--
-- Name: twitter_twitterapp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE twitter_twitterapp_id_seq OWNED BY twitter_twitterapp.id;


--
-- Name: twitter_twitterapp_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('twitter_twitterapp_id_seq', 1, false);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_message ALTER COLUMN id SET DEFAULT nextval('auth_message_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE classes_class ALTER COLUMN id SET DEFAULT nextval('classes_class_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE classes_class_subject ALTER COLUMN id SET DEFAULT nextval('classes_class_subject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE classes_classsubject ALTER COLUMN id SET DEFAULT nextval('classes_classsubject_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE classes_classuserhistory ALTER COLUMN id SET DEFAULT nextval('classes_classuserhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_admin_log ALTER COLUMN id SET DEFAULT nextval('django_admin_log_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_comment_flags ALTER COLUMN id SET DEFAULT nextval('django_comment_flags_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_comments ALTER COLUMN id SET DEFAULT nextval('django_comments_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_content_type ALTER COLUMN id SET DEFAULT nextval('django_content_type_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_flatpage ALTER COLUMN id SET DEFAULT nextval('django_flatpage_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_flatpage_sites ALTER COLUMN id SET DEFAULT nextval('django_flatpage_sites_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE django_site ALTER COLUMN id SET DEFAULT nextval('django_site_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE emailconfirmation_emailaddress ALTER COLUMN id SET DEFAULT nextval('emailconfirmation_emailaddress_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE emailconfirmation_emailconfirmation ALTER COLUMN id SET DEFAULT nextval('emailconfirmation_emailconfirmation_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE facebook_facebookaccesstoken ALTER COLUMN id SET DEFAULT nextval('facebook_facebookaccesstoken_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE facebook_facebookapp ALTER COLUMN id SET DEFAULT nextval('facebook_facebookapp_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE openid_openidnonce ALTER COLUMN id SET DEFAULT nextval('openid_openidnonce_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE openid_openidstore ALTER COLUMN id SET DEFAULT nextval('openid_openidstore_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE profile_child ALTER COLUMN id SET DEFAULT nextval('profile_child_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE profile_newslettersubscription ALTER COLUMN id SET DEFAULT nextval('profile_newslettersubscription_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE profile_userprofile ALTER COLUMN id SET DEFAULT nextval('profile_userprofile_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE socialaccount_socialaccount ALTER COLUMN id SET DEFAULT nextval('socialaccount_socialaccount_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE south_migrationhistory ALTER COLUMN id SET DEFAULT nextval('south_migrationhistory_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE tagging_tag ALTER COLUMN id SET DEFAULT nextval('tagging_tag_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE tagging_taggeditem ALTER COLUMN id SET DEFAULT nextval('tagging_taggeditem_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE twitter_twitterapp ALTER COLUMN id SET DEFAULT nextval('twitter_twitterapp_id_seq'::regclass);


--
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- Data for Name: auth_message; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_message (id, user_id, message) FROM stdin;
\.


--
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
1	Can add permission	1	add_permission
2	Can change permission	1	change_permission
3	Can delete permission	1	delete_permission
4	Can add group	2	add_group
5	Can change group	2	change_group
6	Can delete group	2	delete_group
7	Can add user	3	add_user
8	Can change user	3	change_user
9	Can delete user	3	delete_user
10	Can add message	4	add_message
11	Can change message	4	change_message
12	Can delete message	4	delete_message
13	Can add content type	5	add_contenttype
14	Can change content type	5	change_contenttype
15	Can delete content type	5	delete_contenttype
16	Can add session	6	add_session
17	Can change session	6	change_session
18	Can delete session	6	delete_session
19	Can add site	7	add_site
20	Can change site	7	change_site
21	Can delete site	7	delete_site
22	Can add log entry	8	add_logentry
23	Can change log entry	8	change_logentry
24	Can delete log entry	8	delete_logentry
25	Can add comment	9	add_comment
26	Can change comment	9	change_comment
27	Can delete comment	9	delete_comment
28	Can moderate comments	9	can_moderate
29	Can add comment flag	10	add_commentflag
30	Can change comment flag	10	change_commentflag
31	Can delete comment flag	10	delete_commentflag
32	Can add flat page	11	add_flatpage
33	Can change flat page	11	change_flatpage
34	Can delete flat page	11	delete_flatpage
35	Can add migration history	12	add_migrationhistory
36	Can change migration history	12	change_migrationhistory
37	Can delete migration history	12	delete_migrationhistory
38	Can add tag	13	add_tag
39	Can change tag	13	change_tag
40	Can delete tag	13	delete_tag
41	Can add tagged item	14	add_taggeditem
42	Can change tagged item	14	change_taggeditem
43	Can delete tagged item	14	delete_taggeditem
44	Can add email address	15	add_emailaddress
45	Can change email address	15	change_emailaddress
46	Can delete email address	15	delete_emailaddress
47	Can add email confirmation	16	add_emailconfirmation
48	Can change email confirmation	16	change_emailconfirmation
49	Can delete email confirmation	16	delete_emailconfirmation
50	Can add social account	17	add_socialaccount
51	Can change social account	17	change_socialaccount
52	Can delete social account	17	delete_socialaccount
53	Can add twitter app	18	add_twitterapp
54	Can change twitter app	18	change_twitterapp
55	Can delete twitter app	18	delete_twitterapp
56	Can add twitter account	19	add_twitteraccount
57	Can change twitter account	19	change_twitteraccount
58	Can delete twitter account	19	delete_twitteraccount
59	Can add open id account	20	add_openidaccount
60	Can change open id account	20	change_openidaccount
61	Can delete open id account	20	delete_openidaccount
62	Can add open id store	21	add_openidstore
63	Can change open id store	21	change_openidstore
64	Can delete open id store	21	delete_openidstore
65	Can add open id nonce	22	add_openidnonce
66	Can change open id nonce	22	change_openidnonce
67	Can delete open id nonce	22	delete_openidnonce
68	Can add facebook app	23	add_facebookapp
69	Can change facebook app	23	change_facebookapp
70	Can delete facebook app	23	delete_facebookapp
71	Can add facebook account	24	add_facebookaccount
72	Can change facebook account	24	change_facebookaccount
73	Can delete facebook account	24	delete_facebookaccount
74	Can add facebook access token	25	add_facebookaccesstoken
75	Can change facebook access token	25	change_facebookaccesstoken
76	Can delete facebook access token	25	delete_facebookaccesstoken
77	Can add user profile	26	add_userprofile
78	Can change user profile	26	change_userprofile
79	Can delete user profile	26	delete_userprofile
80	Can add child	27	add_child
81	Can change child	27	change_child
82	Can delete child	27	delete_child
83	Can add newsletter subscription	28	add_newslettersubscription
84	Can change newsletter subscription	28	change_newslettersubscription
85	Can delete newsletter subscription	28	delete_newslettersubscription
86	Can add class subject	29	add_classsubject
87	Can change class subject	29	change_classsubject
88	Can delete class subject	29	delete_classsubject
89	Can add class	30	add_class
90	Can change class	30	change_class
91	Can delete class	30	delete_class
92	Can add class user history	31	add_classuserhistory
93	Can change class user history	31	change_classuserhistory
94	Can delete class user history	31	delete_classuserhistory
\.


--
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user (id, username, first_name, last_name, email, password, is_staff, is_active, is_superuser, last_login, date_joined) FROM stdin;
2	student	First	Student	student@rawjam.co.uk	sha1$647a6$abf4b51c1625f3340e7042c714ba0840730e7727	f	t	f	2012-04-25 14:22:16.859263+00	2012-04-23 11:31:12+00
1	admin	Tutor	and Admin	support@rawjam.co.uk	sha1$7eb81$c00ad9bad80c33652c55cb0457fbb89c9f02f52d	t	t	t	2012-04-26 12:20:14.956391+00	2012-04-23 10:36:01+00
\.


--
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: -
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- Data for Name: classes_class; Type: TABLE DATA; Schema: public; Owner: -
--

COPY classes_class (id, created, updated, tutor_id, student_id, date, start, "end", credit_fee, scribblar_id, name) FROM stdin;
1	2012-04-23 11:32:39.557086+00	2012-04-23 11:32:40.089088+00	1	2	2012-04-26	13:00:00	15:00:00	10	b5j6k766	My first class
2	2012-04-23 11:37:19.081005+00	2012-04-23 11:37:19.614736+00	1	2	2012-04-20	04:00:00	06:00:00	20	tfqjs4m	Test class
\.


--
-- Data for Name: classes_class_subject; Type: TABLE DATA; Schema: public; Owner: -
--

COPY classes_class_subject (id, class_id, classsubject_id) FROM stdin;
1	1	1
2	2	1
\.


--
-- Data for Name: classes_classsubject; Type: TABLE DATA; Schema: public; Owner: -
--

COPY classes_classsubject (id, subject) FROM stdin;
1	Math
\.


--
-- Data for Name: classes_classuserhistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY classes_classuserhistory (id, _class_id, user_id, enter, leave) FROM stdin;
\.


--
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
1	2012-04-23 10:57:20.73621+00	1	23	1	Rawjam Staging (@example.com)	1	
2	2012-04-23 11:08:23.413361+00	1	29	1	Math	1	
3	2012-04-23 11:12:03.465719+00	1	3	1	admin	2	Changed scribblar_id and type for user profile "admin".
4	2012-04-23 11:23:47.019424+00	1	3	1	admin	2	Changed date_of_birth and type for user profile "admin".
5	2012-04-23 11:31:12.972978+00	1	3	2	student	1	
6	2012-04-23 11:31:46.079936+00	1	3	2	student	2	Changed first_name, last_name and email.
7	2012-04-23 11:32:40.101861+00	1	30	1	My first class	1	
8	2012-04-23 11:37:19.623739+00	1	30	2	Test class	1	
9	2012-04-23 13:30:14.750246+00	1	3	1	admin	2	Changed first_name and last_name.
\.


--
-- Data for Name: django_comment_flags; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_comment_flags (id, user_id, comment_id, flag, flag_date) FROM stdin;
\.


--
-- Data for Name: django_comments; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_comments (id, content_type_id, object_pk, site_id, user_id, user_name, user_email, user_url, comment, submit_date, ip_address, is_public, is_removed) FROM stdin;
\.


--
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
1	permission	auth	permission
2	group	auth	group
3	user	auth	user
4	message	auth	message
5	content type	contenttypes	contenttype
6	session	sessions	session
7	site	sites	site
8	log entry	admin	logentry
9	comment	comments	comment
10	comment flag	comments	commentflag
11	flat page	flatpages	flatpage
12	migration history	south	migrationhistory
13	tag	tagging	tag
14	tagged item	tagging	taggeditem
15	email address	emailconfirmation	emailaddress
16	email confirmation	emailconfirmation	emailconfirmation
17	social account	socialaccount	socialaccount
18	twitter app	twitter	twitterapp
19	twitter account	twitter	twitteraccount
20	open id account	openid	openidaccount
21	open id store	openid	openidstore
22	open id nonce	openid	openidnonce
23	facebook app	facebook	facebookapp
24	facebook account	facebook	facebookaccount
25	facebook access token	facebook	facebookaccesstoken
26	user profile	profile	userprofile
27	child	profile	child
28	newsletter subscription	profile	newslettersubscription
29	class subject	classes	classsubject
30	class	classes	class
31	class user history	classes	classuserhistory
\.


--
-- Data for Name: django_flatpage; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_flatpage (id, url, title, content, enable_comments, template_name, registration_required) FROM stdin;
\.


--
-- Data for Name: django_flatpage_sites; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_flatpage_sites (id, flatpage_id, site_id) FROM stdin;
\.


--
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
5a24a85e4abe7449255fe4d5ebc521e1	NjYzYWM2YmM0Yjk2OTkxZDUxZjU1ZDdkYmIwZTVlMmZkNDkzMzllNDqAAn1xAShVEl9hdXRoX3Vz\nZXJfYmFja2VuZHECVSlkamFuZ28uY29udHJpYi5hdXRoLmJhY2tlbmRzLk1vZGVsQmFja2VuZHED\nVQ1fYXV0aF91c2VyX2lkcQRLAXUu\n	2012-05-07 10:49:45.756064+00
624da681b6c504bab395d5e3d1e7b45e	YzM5ZGVjYjRjNjZmODJmMzhmNTllMWFjNDMxNTdiZDkyM2QzYjlmMDqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAnUu\n	2012-05-09 14:22:16.931249+00
b645e39621e190e87c4edb06ee4a39db	MWRhNjM1OTY1OTU4MTkwOGIzZGM3M2I4MmRkN2QyYWFjMGI1NmFkNjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAXUu\n	2012-05-09 14:22:57.70587+00
080b24cba95c7e898e0091f305b0b265	MWRhNjM1OTY1OTU4MTkwOGIzZGM3M2I4MmRkN2QyYWFjMGI1NmFkNjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAXUu\n	2012-05-10 12:20:15.01765+00
4d057c56a33c47977c539503ad546e35	MWRhNjM1OTY1OTU4MTkwOGIzZGM3M2I4MmRkN2QyYWFjMGI1NmFkNjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAXUu\n	2012-05-07 12:03:57.60696+00
45c93a065cf4d320ca980bcb1b6b589e	MWRhNjM1OTY1OTU4MTkwOGIzZGM3M2I4MmRkN2QyYWFjMGI1NmFkNjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAXUu\n	2012-05-07 12:13:01.806463+00
2adee0639804c0b1c4671c48aaf4293f	YzM5ZGVjYjRjNjZmODJmMzhmNTllMWFjNDMxNTdiZDkyM2QzYjlmMDqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAnUu\n	2012-05-07 12:13:21.575749+00
674653af6fdb9d54285c94d79e9ce791	MWRhNjM1OTY1OTU4MTkwOGIzZGM3M2I4MmRkN2QyYWFjMGI1NmFkNjqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAXUu\n	2012-05-07 14:47:38.549198+00
5786809dc94ce99c73bdb289d1b2176e	YzM5ZGVjYjRjNjZmODJmMzhmNTllMWFjNDMxNTdiZDkyM2QzYjlmMDqAAn1xAShVD19zZXNzaW9u\nX2V4cGlyeXECSwBVEl9hdXRoX3VzZXJfYmFja2VuZHEDVSlkamFuZ28uY29udHJpYi5hdXRoLmJh\nY2tlbmRzLk1vZGVsQmFja2VuZHEEVQ1fYXV0aF91c2VyX2lkcQVLAnUu\n	2012-05-07 15:09:45.18712+00
\.


--
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: -
--

COPY django_site (id, domain, name) FROM stdin;
1	example.com	example.com
\.


--
-- Data for Name: emailconfirmation_emailaddress; Type: TABLE DATA; Schema: public; Owner: -
--

COPY emailconfirmation_emailaddress (id, user_id, email, verified, "primary") FROM stdin;
\.


--
-- Data for Name: emailconfirmation_emailconfirmation; Type: TABLE DATA; Schema: public; Owner: -
--

COPY emailconfirmation_emailconfirmation (id, email_address_id, sent, confirmation_key) FROM stdin;
\.


--
-- Data for Name: facebook_facebookaccesstoken; Type: TABLE DATA; Schema: public; Owner: -
--

COPY facebook_facebookaccesstoken (id, app_id, account_id, access_token) FROM stdin;
\.


--
-- Data for Name: facebook_facebookaccount; Type: TABLE DATA; Schema: public; Owner: -
--

COPY facebook_facebookaccount (socialaccount_ptr_id, social_id, name, link) FROM stdin;
\.


--
-- Data for Name: facebook_facebookapp; Type: TABLE DATA; Schema: public; Owner: -
--

COPY facebook_facebookapp (id, site_id, name, application_id, api_key, application_secret) FROM stdin;
1	1	Rawjam Staging	361857900525216	361857900525216	0851c338b395e6c6beb7c26cf37987a0
\.


--
-- Data for Name: openid_openidaccount; Type: TABLE DATA; Schema: public; Owner: -
--

COPY openid_openidaccount (socialaccount_ptr_id, identity) FROM stdin;
\.


--
-- Data for Name: openid_openidnonce; Type: TABLE DATA; Schema: public; Owner: -
--

COPY openid_openidnonce (id, server_url, "timestamp", salt, date_created) FROM stdin;
\.


--
-- Data for Name: openid_openidstore; Type: TABLE DATA; Schema: public; Owner: -
--

COPY openid_openidstore (id, server_url, handle, secret, issued, lifetime, assoc_type) FROM stdin;
\.


--
-- Data for Name: profile_child; Type: TABLE DATA; Schema: public; Owner: -
--

COPY profile_child (id, parent_id, child_id, active, key) FROM stdin;
\.


--
-- Data for Name: profile_newslettersubscription; Type: TABLE DATA; Schema: public; Owner: -
--

COPY profile_newslettersubscription (id, created, updated, email, email_verified, hash_key) FROM stdin;
\.


--
-- Data for Name: profile_userprofile; Type: TABLE DATA; Schema: public; Owner: -
--

COPY profile_userprofile (id, created, updated, user_id, about, title, profile_image, address, location, postcode, country, phone, newsletters, type, credit, income, referral, date_of_birth, scribblar_id, subjects_id) FROM stdin;
1	2012-04-23 10:57:35.36801+00	2012-04-23 11:23:47.015831+00	1			images/defaults/profile.png				\N		f	1	0	0	0	1983-08-15	24C15193-DF8B-5A51-3D72859F709F5727	\N
2	2012-04-23 11:31:12.263964+00	2012-04-23 11:31:12.970589+00	2			images/defaults/profile.png				\N		f	2	0	0	0	1987-04-23	B67364B7-F925-D4A8-A33F537E581BAD3D	\N
\.


--
-- Data for Name: socialaccount_socialaccount; Type: TABLE DATA; Schema: public; Owner: -
--

COPY socialaccount_socialaccount (id, user_id, last_login, date_joined) FROM stdin;
\.


--
-- Data for Name: south_migrationhistory; Type: TABLE DATA; Schema: public; Owner: -
--

COPY south_migrationhistory (id, app_name, migration, applied) FROM stdin;
1	socialaccount	0001_initial	2012-04-23 09:36:11.643107+00
2	twitter	0001_initial	2012-04-23 09:36:11.81444+00
3	twitter	0002_snowflake	2012-04-23 09:36:11.984009+00
4	openid	0001_initial	2012-04-23 09:36:12.079233+00
5	facebook	0001_initial	2012-04-23 09:36:12.155761+00
6	facebook	0002_auto__add_facebookaccesstoken__add_unique_facebookaccesstoken_app_acco	2012-04-23 09:36:12.187413+00
7	profile	0001_initial	2012-04-23 09:36:12.276697+00
8	profile	0002_auto__add_field_userprofile_parent__add_field_userprofile_type__add_fi	2012-04-23 09:36:12.377719+00
9	profile	0003_auto__add_child__del_field_userprofile_parent	2012-04-23 09:36:12.409595+00
10	profile	0004_auto__add_field_userprofile_date_of_birth	2012-04-23 09:36:12.440675+00
11	profile	0005_auto__chg_field_userprofile_date_of_birth	2012-04-23 09:36:12.488237+00
12	profile	0006_auto__add_field_userprofile_scribblar_id__add_field_child_active__add_	2012-04-23 09:36:12.543438+00
13	classes	0001_initial	2012-04-23 09:36:24.375996+00
14	profile	0007_auto__add_field_userprofile_subjects	2012-04-23 09:36:27.438762+00
15	profile	0008_auto__chg_field_userprofile_scribblar_id	2012-04-23 09:36:27.493644+00
16	profile	0009_auto__chg_field_userprofile_profile_image	2012-04-23 09:36:27.544243+00
\.


--
-- Data for Name: tagging_tag; Type: TABLE DATA; Schema: public; Owner: -
--

COPY tagging_tag (id, name) FROM stdin;
\.


--
-- Data for Name: tagging_taggeditem; Type: TABLE DATA; Schema: public; Owner: -
--

COPY tagging_taggeditem (id, tag_id, content_type_id, object_id) FROM stdin;
\.


--
-- Data for Name: twitter_twitteraccount; Type: TABLE DATA; Schema: public; Owner: -
--

COPY twitter_twitteraccount (socialaccount_ptr_id, social_id, username, profile_image_url) FROM stdin;
\.


--
-- Data for Name: twitter_twitterapp; Type: TABLE DATA; Schema: public; Owner: -
--

COPY twitter_twitterapp (id, site_id, name, consumer_key, consumer_secret, request_token_url, access_token_url, authorize_url) FROM stdin;
\.


--
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- Name: auth_group_permissions_group_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_key UNIQUE (group_id, permission_id);


--
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- Name: auth_message_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_pkey PRIMARY KEY (id);


--
-- Name: auth_permission_content_type_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_content_type_id_key UNIQUE (content_type_id, codename);


--
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- Name: auth_user_groups_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_key UNIQUE (user_id, group_id);


--
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- Name: auth_user_user_permissions_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_key UNIQUE (user_id, permission_id);


--
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- Name: classes_class_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classes_class
    ADD CONSTRAINT classes_class_pkey PRIMARY KEY (id);


--
-- Name: classes_class_subject_class_id_c776ee_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classes_class_subject
    ADD CONSTRAINT classes_class_subject_class_id_c776ee_uniq UNIQUE (class_id, classsubject_id);


--
-- Name: classes_class_subject_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classes_class_subject
    ADD CONSTRAINT classes_class_subject_pkey PRIMARY KEY (id);


--
-- Name: classes_classsubject_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classes_classsubject
    ADD CONSTRAINT classes_classsubject_pkey PRIMARY KEY (id);


--
-- Name: classes_classuserhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY classes_classuserhistory
    ADD CONSTRAINT classes_classuserhistory_pkey PRIMARY KEY (id);


--
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- Name: django_comment_flags_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_pkey PRIMARY KEY (id);


--
-- Name: django_comment_flags_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_key UNIQUE (user_id, comment_id, flag);


--
-- Name: django_comments_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_pkey PRIMARY KEY (id);


--
-- Name: django_content_type_app_label_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_app_label_key UNIQUE (app_label, model);


--
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- Name: django_flatpage_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_flatpage
    ADD CONSTRAINT django_flatpage_pkey PRIMARY KEY (id);


--
-- Name: django_flatpage_sites_flatpage_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_flatpage_sites
    ADD CONSTRAINT django_flatpage_sites_flatpage_id_key UNIQUE (flatpage_id, site_id);


--
-- Name: django_flatpage_sites_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_flatpage_sites
    ADD CONSTRAINT django_flatpage_sites_pkey PRIMARY KEY (id);


--
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- Name: emailconfirmation_emailaddress_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY emailconfirmation_emailaddress
    ADD CONSTRAINT emailconfirmation_emailaddress_pkey PRIMARY KEY (id);


--
-- Name: emailconfirmation_emailaddress_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY emailconfirmation_emailaddress
    ADD CONSTRAINT emailconfirmation_emailaddress_user_id_key UNIQUE (user_id, email);


--
-- Name: emailconfirmation_emailconfirmation_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY emailconfirmation_emailconfirmation
    ADD CONSTRAINT emailconfirmation_emailconfirmation_pkey PRIMARY KEY (id);


--
-- Name: facebook_facebookaccesstoken_app_id_2dd6dfc2_uniq; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY facebook_facebookaccesstoken
    ADD CONSTRAINT facebook_facebookaccesstoken_app_id_2dd6dfc2_uniq UNIQUE (app_id, account_id);


--
-- Name: facebook_facebookaccesstoken_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY facebook_facebookaccesstoken
    ADD CONSTRAINT facebook_facebookaccesstoken_pkey PRIMARY KEY (id);


--
-- Name: facebook_facebookaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY facebook_facebookaccount
    ADD CONSTRAINT facebook_facebookaccount_pkey PRIMARY KEY (socialaccount_ptr_id);


--
-- Name: facebook_facebookaccount_social_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY facebook_facebookaccount
    ADD CONSTRAINT facebook_facebookaccount_social_id_key UNIQUE (social_id);


--
-- Name: facebook_facebookapp_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY facebook_facebookapp
    ADD CONSTRAINT facebook_facebookapp_pkey PRIMARY KEY (id);


--
-- Name: openid_openidaccount_identity_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY openid_openidaccount
    ADD CONSTRAINT openid_openidaccount_identity_key UNIQUE (identity);


--
-- Name: openid_openidaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY openid_openidaccount
    ADD CONSTRAINT openid_openidaccount_pkey PRIMARY KEY (socialaccount_ptr_id);


--
-- Name: openid_openidnonce_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY openid_openidnonce
    ADD CONSTRAINT openid_openidnonce_pkey PRIMARY KEY (id);


--
-- Name: openid_openidstore_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY openid_openidstore
    ADD CONSTRAINT openid_openidstore_pkey PRIMARY KEY (id);


--
-- Name: profile_child_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY profile_child
    ADD CONSTRAINT profile_child_pkey PRIMARY KEY (id);


--
-- Name: profile_newslettersubscription_email_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY profile_newslettersubscription
    ADD CONSTRAINT profile_newslettersubscription_email_key UNIQUE (email);


--
-- Name: profile_newslettersubscription_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY profile_newslettersubscription
    ADD CONSTRAINT profile_newslettersubscription_pkey PRIMARY KEY (id);


--
-- Name: profile_userprofile_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY profile_userprofile
    ADD CONSTRAINT profile_userprofile_pkey PRIMARY KEY (id);


--
-- Name: profile_userprofile_user_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY profile_userprofile
    ADD CONSTRAINT profile_userprofile_user_id_key UNIQUE (user_id);


--
-- Name: socialaccount_socialaccount_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT socialaccount_socialaccount_pkey PRIMARY KEY (id);


--
-- Name: south_migrationhistory_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY south_migrationhistory
    ADD CONSTRAINT south_migrationhistory_pkey PRIMARY KEY (id);


--
-- Name: tagging_tag_name_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tagging_tag
    ADD CONSTRAINT tagging_tag_name_key UNIQUE (name);


--
-- Name: tagging_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tagging_tag
    ADD CONSTRAINT tagging_tag_pkey PRIMARY KEY (id);


--
-- Name: tagging_taggeditem_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tagging_taggeditem
    ADD CONSTRAINT tagging_taggeditem_pkey PRIMARY KEY (id);


--
-- Name: tagging_taggeditem_tag_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY tagging_taggeditem
    ADD CONSTRAINT tagging_taggeditem_tag_id_key UNIQUE (tag_id, content_type_id, object_id);


--
-- Name: twitter_twitteraccount_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY twitter_twitteraccount
    ADD CONSTRAINT twitter_twitteraccount_pkey PRIMARY KEY (socialaccount_ptr_id);


--
-- Name: twitter_twitteraccount_social_id_key; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY twitter_twitteraccount
    ADD CONSTRAINT twitter_twitteraccount_social_id_key UNIQUE (social_id);


--
-- Name: twitter_twitterapp_pkey; Type: CONSTRAINT; Schema: public; Owner: -; Tablespace: 
--

ALTER TABLE ONLY twitter_twitterapp
    ADD CONSTRAINT twitter_twitterapp_pkey PRIMARY KEY (id);


--
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- Name: auth_message_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_message_user_id ON auth_message USING btree (user_id);


--
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- Name: classes_class_student_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_class_student_id ON classes_class USING btree (student_id);


--
-- Name: classes_class_subject_class_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_class_subject_class_id ON classes_class_subject USING btree (class_id);


--
-- Name: classes_class_subject_classsubject_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_class_subject_classsubject_id ON classes_class_subject USING btree (classsubject_id);


--
-- Name: classes_class_tutor_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_class_tutor_id ON classes_class USING btree (tutor_id);


--
-- Name: classes_classuserhistory__class_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_classuserhistory__class_id ON classes_classuserhistory USING btree (_class_id);


--
-- Name: classes_classuserhistory_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX classes_classuserhistory_user_id ON classes_classuserhistory USING btree (user_id);


--
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- Name: django_comment_flags_comment_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comment_flags_comment_id ON django_comment_flags USING btree (comment_id);


--
-- Name: django_comment_flags_flag; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comment_flags_flag ON django_comment_flags USING btree (flag);


--
-- Name: django_comment_flags_flag_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comment_flags_flag_like ON django_comment_flags USING btree (flag varchar_pattern_ops);


--
-- Name: django_comment_flags_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comment_flags_user_id ON django_comment_flags USING btree (user_id);


--
-- Name: django_comments_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comments_content_type_id ON django_comments USING btree (content_type_id);


--
-- Name: django_comments_site_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comments_site_id ON django_comments USING btree (site_id);


--
-- Name: django_comments_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_comments_user_id ON django_comments USING btree (user_id);


--
-- Name: django_flatpage_sites_flatpage_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_flatpage_sites_flatpage_id ON django_flatpage_sites USING btree (flatpage_id);


--
-- Name: django_flatpage_sites_site_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_flatpage_sites_site_id ON django_flatpage_sites USING btree (site_id);


--
-- Name: django_flatpage_url; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_flatpage_url ON django_flatpage USING btree (url);


--
-- Name: django_flatpage_url_like; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_flatpage_url_like ON django_flatpage USING btree (url varchar_pattern_ops);


--
-- Name: django_session_expire_date; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX django_session_expire_date ON django_session USING btree (expire_date);


--
-- Name: emailconfirmation_emailaddress_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX emailconfirmation_emailaddress_user_id ON emailconfirmation_emailaddress USING btree (user_id);


--
-- Name: emailconfirmation_emailconfirmation_email_address_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX emailconfirmation_emailconfirmation_email_address_id ON emailconfirmation_emailconfirmation USING btree (email_address_id);


--
-- Name: facebook_facebookaccesstoken_account_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX facebook_facebookaccesstoken_account_id ON facebook_facebookaccesstoken USING btree (account_id);


--
-- Name: facebook_facebookaccesstoken_app_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX facebook_facebookaccesstoken_app_id ON facebook_facebookaccesstoken USING btree (app_id);


--
-- Name: facebook_facebookapp_site_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX facebook_facebookapp_site_id ON facebook_facebookapp USING btree (site_id);


--
-- Name: profile_child_parent_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX profile_child_parent_id ON profile_child USING btree (parent_id);


--
-- Name: profile_userprofile_subjects_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX profile_userprofile_subjects_id ON profile_userprofile USING btree (subjects_id);


--
-- Name: socialaccount_socialaccount_user_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX socialaccount_socialaccount_user_id ON socialaccount_socialaccount USING btree (user_id);


--
-- Name: tagging_taggeditem_content_type_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX tagging_taggeditem_content_type_id ON tagging_taggeditem USING btree (content_type_id);


--
-- Name: tagging_taggeditem_object_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX tagging_taggeditem_object_id ON tagging_taggeditem USING btree (object_id);


--
-- Name: tagging_taggeditem_tag_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX tagging_taggeditem_tag_id ON tagging_taggeditem USING btree (tag_id);


--
-- Name: twitter_twitterapp_site_id; Type: INDEX; Schema: public; Owner: -; Tablespace: 
--

CREATE INDEX twitter_twitterapp_site_id ON twitter_twitterapp USING btree (site_id);


--
-- Name: _class_id_refs_id_637007a1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_classuserhistory
    ADD CONSTRAINT _class_id_refs_id_637007a1 FOREIGN KEY (_class_id) REFERENCES classes_class(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: account_id_refs_socialaccount_ptr_id_45e95643; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY facebook_facebookaccesstoken
    ADD CONSTRAINT account_id_refs_socialaccount_ptr_id_45e95643 FOREIGN KEY (account_id) REFERENCES facebook_facebookaccount(socialaccount_ptr_id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: app_id_refs_id_6d24d761; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY facebook_facebookaccesstoken
    ADD CONSTRAINT app_id_refs_id_6d24d761 FOREIGN KEY (app_id) REFERENCES facebook_facebookapp(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_group_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_message_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_message
    ADD CONSTRAINT auth_message_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: child_id_refs_id_7b96ff3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY profile_child
    ADD CONSTRAINT child_id_refs_id_7b96ff3 FOREIGN KEY (child_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: class_id_refs_id_7cd35846; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_class_subject
    ADD CONSTRAINT class_id_refs_id_7cd35846 FOREIGN KEY (class_id) REFERENCES classes_class(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: classsubject_id_refs_id_570b2b1; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_class_subject
    ADD CONSTRAINT classsubject_id_refs_id_570b2b1 FOREIGN KEY (classsubject_id) REFERENCES classes_classsubject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: content_type_id_refs_id_728de91f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_728de91f FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags_comment_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_comment_id_fkey FOREIGN KEY (comment_id) REFERENCES django_comments(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comment_flags_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_comment_flags
    ADD CONSTRAINT django_comment_flags_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_site_id_fkey FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_comments_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_comments
    ADD CONSTRAINT django_comments_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: django_flatpage_sites_site_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_flatpage_sites
    ADD CONSTRAINT django_flatpage_sites_site_id_fkey FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: emailconfirmation_emailaddress_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY emailconfirmation_emailaddress
    ADD CONSTRAINT emailconfirmation_emailaddress_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: emailconfirmation_emailconfirmation_email_address_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY emailconfirmation_emailconfirmation
    ADD CONSTRAINT emailconfirmation_emailconfirmation_email_address_id_fkey FOREIGN KEY (email_address_id) REFERENCES emailconfirmation_emailaddress(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: flatpage_id_refs_id_3f17b0a6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY django_flatpage_sites
    ADD CONSTRAINT flatpage_id_refs_id_3f17b0a6 FOREIGN KEY (flatpage_id) REFERENCES django_flatpage(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: group_id_refs_id_3cea63fe; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT group_id_refs_id_3cea63fe FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: parent_id_refs_id_7b96ff3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY profile_child
    ADD CONSTRAINT parent_id_refs_id_7b96ff3 FOREIGN KEY (parent_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: site_id_refs_id_2ab952e9; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY facebook_facebookapp
    ADD CONSTRAINT site_id_refs_id_2ab952e9 FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: site_id_refs_id_55bf92c3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY twitter_twitterapp
    ADD CONSTRAINT site_id_refs_id_55bf92c3 FOREIGN KEY (site_id) REFERENCES django_site(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_ptr_id_refs_id_14575d37; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY facebook_facebookaccount
    ADD CONSTRAINT socialaccount_ptr_id_refs_id_14575d37 FOREIGN KEY (socialaccount_ptr_id) REFERENCES socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_ptr_id_refs_id_68c0e1e3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY openid_openidaccount
    ADD CONSTRAINT socialaccount_ptr_id_refs_id_68c0e1e3 FOREIGN KEY (socialaccount_ptr_id) REFERENCES socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: socialaccount_ptr_id_refs_id_bc919e5; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY twitter_twitteraccount
    ADD CONSTRAINT socialaccount_ptr_id_refs_id_bc919e5 FOREIGN KEY (socialaccount_ptr_id) REFERENCES socialaccount_socialaccount(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: student_id_refs_id_4acadba4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_class
    ADD CONSTRAINT student_id_refs_id_4acadba4 FOREIGN KEY (student_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: subjects_id_refs_id_5d247d13; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY profile_userprofile
    ADD CONSTRAINT subjects_id_refs_id_5d247d13 FOREIGN KEY (subjects_id) REFERENCES classes_classsubject(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tagging_taggeditem_content_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY tagging_taggeditem
    ADD CONSTRAINT tagging_taggeditem_content_type_id_fkey FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tagging_taggeditem_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY tagging_taggeditem
    ADD CONSTRAINT tagging_taggeditem_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES tagging_tag(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: tutor_id_refs_id_4acadba4; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_class
    ADD CONSTRAINT tutor_id_refs_id_4acadba4 FOREIGN KEY (tutor_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_651975b6; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY socialaccount_socialaccount
    ADD CONSTRAINT user_id_refs_id_651975b6 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_7622d5ff; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY profile_userprofile
    ADD CONSTRAINT user_id_refs_id_7622d5ff FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_7ceef80f; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT user_id_refs_id_7ceef80f FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_ab95d68; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY classes_classuserhistory
    ADD CONSTRAINT user_id_refs_id_ab95d68 FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- Name: user_id_refs_id_dfbab7d; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT user_id_refs_id_dfbab7d FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- PostgreSQL database dump complete
--

