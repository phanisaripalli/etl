CREATE SCHEMA stripe;

-- --ideally should be int but the JSON has the format evt_nr. I will leave as it is at this point
CREATE TABLE stripe.event ( 
     id       text NOT NULL, 
     livemode boolean, 
     type     text, 
     created  timestamp 
); 

CREATE TABLE stripe.charge ( 
     id                  text NOT NULL, 
     event_id		  	 text NOT NULL,
     customer_id         text, 
     invoice_id          text,
     created             timestamp, 
     livemode            boolean, 
     paid                boolean, 
     amount              numeric, 
     currency            text, 
     refunded            boolean, 
     captured            boolean, 
     balance_transaction text, 
     failure_message     text, 
     failure_code        text, 
     amount_refunded     numeric, 
     description         text, 
     dispute             text 
); 

  CREATE TABLE stripe.billing ( 
  	id  text NOT NULL, 
  	customer_id text,
  	object text,
	last4 integer,
  	"type" text,
  	brand text,
  	exp_month integer,
  	exp_year integer,
  	fingerprint text,        
  	country text,
  	"name" text,
  	address_line1 text,
  	address_line2 text,
  	address_city text,
  	address_state text,
  	address_zip text,
  	address_country text,
  	cvc_check text,
  	address_line1_check text,
  	address_zip_check text    
); 

  CREATE TABLE stripe.charge_billing ( 
  	charge_id  text NOT NULL, 
  	billing_id text NOT NULL
	 
); 


