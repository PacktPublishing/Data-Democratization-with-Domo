-- Table: public.Opportunity
-- DROP TABLE public."Opportunity";

CREATE TABLE public."Opportunity"
(
    "AccountId" character varying COLLATE pg_catalog."default",
    "Amount" money,
    "CampaignId" character varying COLLATE pg_catalog."default",
    "CloseDate" date,
    "ConnectionReceivedId" character varying COLLATE pg_catalog."default",
    "ConnectionSentId" character varying COLLATE pg_catalog."default",
    "CreatedDate" timestamp without time zone,
    "CurrencyIsoCode" character varying COLLATE pg_catalog."default",
    "Description" character varying COLLATE pg_catalog."default",
    "Fiscal" character varying COLLATE pg_catalog."default",
    "FiscalQuarter" bigint,
    "FiscalYear" bigint,
    "ForecastCategory" character varying COLLATE pg_catalog."default",
    "ForecastCategoryName" character varying COLLATE pg_catalog."default",
    "HasOpenActivity" boolean,
    "HasOpportunityLineItem" boolean,
    "HasOverdueTask" boolean,
    id character varying COLLATE pg_catalog."default" NOT NULL,
    "IsClosed" boolean,
	"Is Deleted" boolean,
	"IsWon" boolean,
    "LastActivityDate" date,
    "LastModifiedDate" timestamp without time zone,
    "LastReferencedDate" timestamp without time zone,
    "LastViewedDate" timestamp without time zone,
    "LeadSource" character varying COLLATE pg_catalog."default",
    "Name" character varying COLLATE pg_catalog."default",
    "NextStep" character varying COLLATE pg_catalog."default",
    "OwnerId" character varying COLLATE pg_catalog."default",
    "Pricebook2Id" character varying COLLATE pg_catalog."default",
    "Probability" bigint,
    "RecordTypeId" character varying COLLATE pg_catalog."default",
    "StageName" character varying COLLATE pg_catalog."default",
    "TotalOpportunityQuantity" bigint,
    "Type" character varying COLLATE pg_catalog."default",
    "_BATCH_ID_" bigint,
    "_BATCH_LAST_RUN_" timestamp without time zone,

    CONSTRAINT "Opportunity_pkey" PRIMARY KEY (id)
)

TABLESPACE pg_default;

ALTER TABLE public."Opportunity"
    OWNER to postgres;