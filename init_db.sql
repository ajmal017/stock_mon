create table if not exists stocks_info (
       code varchar(32),
       name varchar(32),
       industry varchar(32),
       area  varchar(32),
       pe   numeric(16,2),
       outstanding  numeric(16,2),
       totals  numeric(16,2),
       totalAssets  numeric(16,2),
       liquidAssets  numeric(16,2),
       fixedAssets  numeric(16,2),
       reserved  numeric(16,2),
       reservedPerShare  numeric(16,2),
       esp  numeric(16,2),
       bvps  numeric(16,2),
       pb  numeric(16,2),
       timeToMarket bigint,
       undp  numeric(16,2),
       perundp  numeric(16,2),
       rev  numeric(16,2),
       profit  numeric(16,2),
       gpr  numeric(16,2),
       npr  numeric(16,2),
       holders bigint,
       constraint pk_si primary key(code)       
);

--create index for stocks_info on industry
create index idx_si_industry on stocks_info (industry);

create table if not exists stocks_m_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_smhd primary key(code,date) 
);

create index idx_smhd_date on stocks_m_hst_data (date);

create table if not exists stocks_w_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_swhd primary key(code,date) 
);

create index idx_swhd_date on stocks_w_hst_data (date);

create table if not exists stocks_d_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_sdhd primary key(code,date) 
);

create index idx_sdhd_date on stocks_d_hst_data (date);

create table if not exists stocks_60m_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_s60mhd primary key(code,date) 
);
create index idx_s60mhd_date on stocks_60m_hst_data (date);

create table if not exists stocks_30m_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_s30mhd primary key(code,date) 
);
create index idx_s30mhd_date on stocks_30m_hst_data (date);

create table if not exists stocks_15m_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_s15mhd primary key(code,date) 
);
create index idx_s15mhd_date on stocks_15m_hst_data (date);

create table if not exists stocks_5m_hst_data (
       code  varchar(32),
       date  numeric(16,2),
       open  numeric(16,2),
       close numeric(16,2),
       high  numeric(16,2),
       low   numeric(16,2),
       volume  numeric(16,2),
       constraint pk_s5mhd primary key(code,date) 
);
create index idx_s5mhd_date on stocks_5m_hst_data (date);
