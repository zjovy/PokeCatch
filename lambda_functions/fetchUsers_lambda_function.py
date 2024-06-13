import json
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: fetchusers**")
        
        config_file = 'pokeapp-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
   
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        # Open connection to the database:
        print("**Opening connection**")
        
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

        # Fetch all users
        print("**Fetching all users**")
        
        sql = """
        SELECT userid
        FROM users
        """
        rows = datatier.retrieve_all_rows(dbConn, sql)
        
        if not rows:
            print("**No users found**")
            raise Exception("No users found")
        
        users = [row[0] for row in rows]

        print("**DONE, returning users**")
        return {
            'statusCode': 200,
            'headers': {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Api-Key, X-Amz-Date, X-Amz-Security-Token',
              'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(users)
        }
        
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
            'statusCode': 400,
            'headers': {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Api-Key, X-Amz-Date, X-Amz-Security-Token',
              'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps(str(err))
        }
