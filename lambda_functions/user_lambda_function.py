import json
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: user**")
        
        #
        # setup AWS based on config file:
        #
        config_file = 'pokeapp-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        #
        # configure for RDS access
        #
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        #
        # the user has sent us two parameters:
        #  1. userid 
        #  2. password
        #
        # The parameters are coming through web server 
        # (or API Gateway) in the body of the request
        # in JSON format.
        #
        print("**Accessing request body**")
        
        if "body" not in event:
          raise Exception("event has no body")
          
        body = json.loads(event["body"]) # parse the json
        
        if "userid" not in body:
          raise Exception("event has a body but no userid")
        if "password" not in body:
          raise Exception("event has a body but no password")
    
        userid = body["userid"]
        password = body["password"]
        
        print("userid:", userid)
        print("password:", password)
            
        #
        # open connection to the database:
        #
        print("**Opening connection**")
        
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

        #
        # add user into db if new, do nothing if exists already
        #
        print("**Checking if user exists**")
        
        checksql = """
        SELECT * 
        FROM users
        WHERE userid = %s
        """
        row = datatier.retrieve_one_row(dbConn, checksql, [userid])
        
        if row == ():  # no such user
            print("**No such user, adding into table...**")
            sql = """
                INSERT INTO users(userid, password)
                      VALUES(%s, %s);
                """
            datatier.perform_action(dbConn, sql, [userid, password])
            
            # add to pokeballs table
            sql = """
                INSERT INTO pokeballs(userid, ballcount)
                    VALUES(%s, %s)
                """
            datatier.perform_action(dbConn, sql, [userid, 0])
            
        print("**DONE, returning**")
        return {
            'statusCode': 200,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : "true",
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*"
            },
            'body': json.dumps("success")
        }   
        
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
          'statusCode': 400,
            'headers': {
                "Content-Type" : "application/json",
                "Access-Control-Allow-Headers" : "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
                "Access-Control-Allow-Methods" : "OPTIONS,POST",
                "Access-Control-Allow-Credentials" : "true",
                "Access-Control-Allow-Origin" : "*",
                "X-Requested-With" : "*"
            },
          'body': json.dumps(str(err))
        }