import json
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: catch**")
        
        # setup AWS based on config file:
        config_file = 'pokeapp-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        # configure for RDS access
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        # the user has sent us two parameters: userid and pokemonid
        print("**Accessing request body**")
        
        if "body" not in event:
            raise Exception("event has no body")
          
        body = json.loads(event["body"]) # parse the json
        
        if "userid" not in body:
            raise Exception("event has a body but no userid")
        if "pokemonid" not in body:
            raise Exception("event has a body but no pokemonid")
    
        userid = body["userid"]
        pokemonid = body["pokemonid"]
        
        print("userid:", userid)
        print("pokemonid:", pokemonid)

        # open connection to the database:
        print("**Opening connection**")
        
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        
        # Check if user has pokeballs
        sql = "SELECT ballcount FROM pokeballs WHERE userid = %s"
        row = datatier.retrieve_one_row(dbConn, sql, [userid])
        
        if row == ():
            raise Exception("invalid user")
        elif row[0] == 0:
            raise Exception("insufficient Pokeballs")
        else:
            # update pokeball count from user inventory
            print("**Using Pokeball**")
            sql = """
            UPDATE pokeballs
            SET ballcount = ballcount - 1
            WHERE userid = %s;
            """
            datatier.perform_action(dbConn, sql, [userid])
            
            # retrieve updated ballcount
            sql = "SELECT ballcount FROM pokeballs WHERE userid = %s"
            row = datatier.retrieve_one_row(dbConn, sql, [userid])
            updated_ballcount = row[0]
            
            # add caught pokemon to user inventory 
            print("**Adding Pokemon to Inventory**")
            sql = """
            INSERT INTO inventory(userid, pokemonid)
                  VALUES(%s, %s);
            """
            datatier.perform_action(dbConn, sql, [userid, pokemonid])
        
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
              'body': json.dumps({'message': 'success', 'ballcount': updated_ballcount})
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
          'body': json.dumps({'message': str(err)})
        }
