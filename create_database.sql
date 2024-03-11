-- Database: gestor_vida

-- DROP DATABASE IF EXISTS gestor_vida;

CREATE DATABASE gestor_vida
    WITH
    OWNER = vitor
    ENCODING = 'UTF8'
    LC_COLLATE = 'pt_BR.utf8'
    LC_CTYPE = 'pt_BR.utf8'
    LOCALE_PROVIDER = 'libc'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1
    IS_TEMPLATE = False;
	
-- Table: public.produtos

-- DROP TABLE IF EXISTS public.produtos;

CREATE TABLE IF NOT EXISTS public.produtos
(
    id_interno smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 32767 CACHE 1 ),
    nome character varying(256) COLLATE pg_catalog."default" NOT NULL,
    barras bigint NOT NULL DEFAULT nextval('produtos_barras_seq'::regclass),
    CONSTRAINT produtos_pkey PRIMARY KEY (id_interno)
)

TABLESPACE pg_default;

-- Table: public.notas

-- DROP TABLE IF EXISTS public.notas;

CREATE TABLE IF NOT EXISTS public.notas
(
    id_nota smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 32767 CACHE 1 ),
    link_nota character varying(256) COLLATE pg_catalog."default" NOT NULL,
    consultada boolean NOT NULL DEFAULT false,
    numero_nf character varying(40) COLLATE pg_catalog."default",
    data_nota date,
    empresa smallint,
    CONSTRAINT notas_pkey PRIMARY KEY (id_nota),
    CONSTRAINT id_empresa FOREIGN KEY (empresa)
        REFERENCES public.empresas (id_empresa) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

-- Table: public.empresas

-- DROP TABLE IF EXISTS public.empresas;

CREATE TABLE IF NOT EXISTS public.empresas
(
    id_empresa smallint NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 32767 CACHE 1 ),
    cnpj character varying(18) COLLATE pg_catalog."default" NOT NULL,
    nome_empresa character varying(256) COLLATE pg_catalog."default",
    CONSTRAINT empresas_pkey PRIMARY KEY (id_empresa)
)

TABLESPACE pg_default;


-- Table: public.dicionario_produtos

-- DROP TABLE IF EXISTS public.dicionario_produtos;

CREATE TABLE IF NOT EXISTS public.dicionario_produtos
(
    id_dicionario integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    nome_externo character varying(256) COLLATE pg_catalog."default",
    empresa smallint NOT NULL,
    id_produto_interno smallint,
    id_externo bigint NOT NULL DEFAULT nextval('dicionario_produtos_id_externo_seq'::regclass),
    CONSTRAINT dicionario_produtos_pkey PRIMARY KEY (id_dicionario),
    CONSTRAINT empresa_id FOREIGN KEY (empresa)
        REFERENCES public.empresas (id_empresa) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT id_interno FOREIGN KEY (id_produto_interno)
        REFERENCES public.produtos (id_interno) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

	
-- Table: public.conteudo_nota

-- DROP TABLE IF EXISTS public.conteudo_nota;

CREATE TABLE IF NOT EXISTS public.conteudo_nota
(
    id_registro integer NOT NULL GENERATED ALWAYS AS IDENTITY ( INCREMENT 1 START 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1 ),
    produto_registro smallint NOT NULL,
    valor_produto real NOT NULL DEFAULT 0.00,
    data_registro date NOT NULL,
    nf_registro smallint NOT NULL,
    "UN" character varying(10) COLLATE pg_catalog."default",
    quantidade real NOT NULL,
    valor_total real,
    CONSTRAINT conteudo_nota_pkey PRIMARY KEY (id_registro),
    CONSTRAINT nf FOREIGN KEY (nf_registro)
        REFERENCES public.notas (id_nota) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    CONSTRAINT produto FOREIGN KEY (produto_registro)
        REFERENCES public.dicionario_produtos (id_dicionario) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;
