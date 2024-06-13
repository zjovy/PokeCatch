import json
import datatier
import os
import pymysql

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: inventory**")
        
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
        
        if "userid" in event:
          userid = event["userid"]
        elif "pathParameters" in event:
          if "userid" in event["pathParameters"]:
            userid = event["pathParameters"]["userid"]
          else:
            raise Exception("requires userid parameter in pathParameters")
        else:
            raise Exception("requires userid parameter in event")
            
        print("**Opening connection**")
        dbConn = pymysql.connect(host=rds_endpoint,
                                 user=rds_username,
                                 password=rds_pwd,
                                 database=rds_dbname,
                                 port=rds_portnum,
                                 cursorclass=pymysql.cursors.DictCursor)

        cursor = dbConn.cursor()
        
        sql = """
        SELECT pokemonid
        FROM inventory
        WHERE userid = %s
        """
        
        cursor.execute(sql, (userid,))
        rows = cursor.fetchall()
        
        print(rows)
        
        if not rows:
            return {
          'statusCode': 200,
            'headers': {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Api-Key, X-Amz-Date, X-Amz-Security-Token',
              'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
            'body': json.dumps([])
            }
            
        pokemons = []
        
        for row in rows:
            pokemonid = row['pokemonid']
            
            pokesql = """
            SELECT * 
            FROM pokemons
            WHERE pokemonid = %s
            """
            cursor.execute(pokesql, (pokemonid,))
            pokeRow = cursor.fetchone()
            
            if not pokeRow:
                return {
                    'statusCode': 400,
                    'body': json.dumps('invalid pokemon')
                }
            
            print(pokeRow)
            
            pokemons.append(pokeRow)
        
        cursor.close()
        dbConn.close()
            
        print("**DONE, returning**")
        return {
          'statusCode': 200,
          'headers': {
              'Access-Control-Allow-Origin': '*',
              'Access-Control-Allow-Headers': 'Content-Type, Authorization, X-Api-Key, X-Amz-Date, X-Amz-Security-Token',
              'Access-Control-Allow-Methods': 'OPTIONS,POST,GET'
            },
          'body': json.dumps(pokemons)
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
    