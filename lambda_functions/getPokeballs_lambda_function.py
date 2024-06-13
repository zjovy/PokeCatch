import json
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: getsomeballs**")
        
        # Setup AWS based on config file:
        config_file = 'pokecatch-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        # Configure for RDS access
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        #
        # userid from event: could be a parameter
        # or could be part of URL path ("pathParameters"):
        #
        if "userid" in event:
          userid = event["userid"]
        elif "pathParameters" in event:
          if "userid" in event["pathParameters"]:
            userid = event["pathParameters"]["userid"]
          else:
            raise Exception("requires userid parameter in pathParameters")
        else:
            raise Exception("requires userid parameter in event")
        
        # Open connection to the MySQL database:
        print("**Opening connection**")
        
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)

        # Fetch the number of pokeballs for the user:
        print("**Fetching number of pokeballs for user**")
        
        sql = """
        SELECT ballcount
        FROM pokeballs
        WHERE userid = %s
        """
        row = datatier.retrieve_one_row(dbConn, sql, [userid])
        
        if not row:
            print("**No pokeballs found for user**")
            return {
                'statusCode': 404,
                'body': json.dumps(f"No pokeballs found for user {userid}")
            }
        
        ballcount = row[0]
        
        print("**DONE, returning ballcount**")
        return {
            'statusCode': 200,
            'headers': {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Api-Key, X-Amz-Date, X-Amz-Security-Token',
              'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps({'userid': userid, 'ballcount': ballcount})
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
