import json
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
  try:
    print("**STARTING**")
    print("**lambda: addPokeball**")
    
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
    # userid from event: could be a parameter
    # or could be part of URL path ("pathParameters"):
    #
    print("**Accessing event/pathParameters**")
    
    if "body" not in event:
        raise Exception("event has no body")
          
    body = json.loads(event["body"]) # parse the json
    
    if "userid" not in body:
      raise Exception("event has a body but no userid")
      
    userid = body["userid"]

    #
    # open connection to the database:
    #
    print("**Opening connection**")
    
    dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
    
    #
    # update user ballcount
    #
    print("**Adding Pokeball**")
    sql = """
    UPDATE pokeballs
    SET ballcount = ballcount + 1
    WHERE userid = %s;
    """
    datatier.perform_action(dbConn, sql, [userid])
    
    #
    # retrieve updated ballcount
    #
    print("**Retrieving updated ballcount**")
    select_sql = """
    SELECT ballcount
    FROM pokeballs
    WHERE userid = %s;
    """
    result = datatier.retrieve_one_row(dbConn, select_sql, [userid])
    
    if not result:
        raise Exception("Failed to retrieve updated ballcount")
    
    updated_ballcount = result[0]
    
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
      'body': json.dumps({'ballcount': updated_ballcount})
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