import json
import pg8000
import logging
import sys
import datetime


#rds settings
rds_host  = "##############################"
rds_username = 'postgres'
rds_password = '<FROM CLOUDINFO>'
rds_db_name = '<DBNAME>'

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    connection = pg8000.connect(host=rds_host, port=5432, user=rds_username, password=rds_password, database=rds_db_name, connect_timeout=5)
    connection = pg8000.connect(host=rds_host, port=5432, user=rds_username, password=rds_password, database=rds_db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to Postgres RDS instance.")
    sys.exit()

def handle(event, context):
    source = event['data']['object']['source']
    cur = connection.cursor()
    # ---------------- DELETE EVENT AND INSERT ------------------------
    created = datetime.datetime.fromtimestamp(
                int(event['created'])
              ).strftime('%Y-%m-%d %H:%M:%S')
    
    data = (event['id'], event['livemode'], event['type'], created)
    try:
        cur.execute("DELETE FROM stripe.event WHERE id = '" + event['id'] + "'")
        #
        cur.execute("INSERT INTO stripe.event (id, livemode, type, created) VALUES (%s, %s, %s, %s)", data)
    except pg8000.Error as e:
        response = {
            "status": "Fail",
            "message": "Database error while handling charges"
        }        
        return response  
    
    #this is a charge event, so we insert charges and respective billing data
    # ---------------- DELETE EVENT AND INSERT ------------------------    
    charge_event = event['data']['object']
    created = datetime.datetime.fromtimestamp(int(charge_event['created'])).strftime('%Y-%m-%d %H:%M:%S')
    data = (
            charge_event['id'],
            charge_event["customer"],
            event['id'],                
            charge_event["invoice"],                
            charge_event["livemode"],
            charge_event["paid"],
            charge_event["amount"],
            charge_event["currency"],
            charge_event["refunded"],
            charge_event["captured"],
            charge_event["balance_transaction"],
            charge_event["failure_message"],
            charge_event["failure_code"],
            charge_event["amount_refunded"],                                
            charge_event["description"],
            charge_event["dispute"],
            created
    )
    try:
        cur.execute("DELETE FROM stripe.charge WHERE id = '" + event['data']['object']['id'] + "'")
        cur.execute("""INSERT INTO stripe.charge (id, event_id, customer_id, invoice_id, livemode,
                                             paid, amount, currency, refunded, captured,
                                             balance_transaction, failure_message, failure_code,
                                            amount_refunded, description, dispute, created)                                       
                   VALUES (%s, %s, %s, %s, %s,
                            %s, %s, %s, %s, %s, 
                            %s, %s, %s,
                            %s, %s, %s, %s
                            )""",
                            data
        )
    except pg8000.Error as e:
        response = {
            "status": "Fail",
            "message": "Database error while handling charges"
        }       
        return response            
                
    #connection.commit()
    # ---------------- HANDLE BILLING DETAILS ------------------------

    billing_details = event['data']['object']['source']                
    data = (billing_details['id'],
            billing_details["name"],
            billing_details["customer"],
            billing_details["object"],
            billing_details['last4'],                
            billing_details["type"],                
            billing_details["brand"],
            billing_details["exp_month"],
            billing_details["exp_year"],
            billing_details["fingerprint"],      
            billing_details["country"],                  
            billing_details["address_line1"],                                    
            billing_details["address_line2"],                  
            billing_details["address_state"],                  
            billing_details["address_zip"],                  
            billing_details["address_country"],                  
            billing_details["cvc_check"],                  
            billing_details["address_line1_check"],                  
            billing_details["address_zip_check"],                  
            )        
    try:
        cur.execute("DELETE FROM stripe.billing WHERE id = '" + billing_details['id'] + "'")
        cur.execute("""INSERT INTO stripe.billing ("id", "name", "customer_id", "object",
                                                "last4","type","brand",
                                                "exp_month","exp_year",
                                                "fingerprint",
                                                "country", 
                                                "address_line1", "address_line2", 
                                                "address_state", "address_zip", "address_country",
                                                "cvc_check", "address_line1_check", "address_zip_check") 
                     VALUES (%s, %s, %s, %s,
                              %s, %s, %s,
                              %s, %s,
                              %s,
                              %s,
                              %s, %s,
                              %s, %s, %s,
                              %s, %s, %s)""", 
                    data
                  )              
    except pg8000.Error as e:
        response = {
            "status": "Fail",
            "message": "Database error while handling billing"
        }        
        return response  
    # ---------------- HANDLE BILLING DETAILS JOIN TABLE ------------------------    
    data = (charge_event['id'],                  
            billing_details["id"],                  
            )        
    
    try:
        cur.execute("DELETE FROM stripe.charge_billing WHERE billing_id = '" + billing_details['id'] + "' AND charge_id = '" + charge_event['id'] + "'")
        cur.execute("""INSERT INTO stripe.charge_billing("charge_id", "billing_id") 
                   VALUES (%s, %s)""", 
                    data
                )
    except pg8000.Error as e:        
        response = {
            "status": "Fail",
            "message": "Database error while handling charges and billing"
        }
        
        return response
        
    connection.commit()
    logger.error("SUCCESS: copied to Postgres RDS instance.")
    return source
