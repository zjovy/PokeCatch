import json
import random
import datatier
import os

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: randomEncounter**")
        
        # Setup AWS based on config file
        config_file = 'pokeapp-config.ini'
        os.environ['AWS_SHARED_CREDENTIALS_FILE'] = config_file
        
        configur = ConfigParser()
        configur.read(config_file)
        
        # Configure for RDS access
        rds_endpoint = configur.get('rds', 'endpoint')
        rds_portnum = int(configur.get('rds', 'port_number'))
        rds_username = configur.get('rds', 'user_name')
        rds_pwd = configur.get('rds', 'user_pwd')
        rds_dbname = configur.get('rds', 'db_name')
        
        # get user's region
        print("**Accessing event/pathParameters**")
        
        if "region" in event:
          user_region = event["region"]
        elif "pathParameters" in event:
          if "region" in event["pathParameters"]:
            user_region = event["pathParameters"]["region"]
          else:
            raise Exception("requires region parameter in pathParameters")
        else:
            raise Exception("requires region parameter in event")

        # Open database connection
        print("**Opening connection**")
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        
        # determine the rarity of the pokemon user will encounter
        roll = random.randint(1, 100)
        if roll <= 5:
            min_encounter_rate = 1
            max_encounter_rate = 5
            rarity = "legendary"
        elif roll <= 15:
            min_encounter_rate = 6
            max_encounter_rate = 15
            rarity = "epic"
        elif roll <= 30:
            min_encounter_rate = 16
            max_encounter_rate = 30
            rarity = "rare"
        else:
            min_encounter_rate = 31
            max_encounter_rate = 100
            rarity = "common"
            
        print(f"Roll: {roll}, Min Encounter Rate: {min_encounter_rate}, Max Encounter Rate: {max_encounter_rate}")
        
        # get a random Pokémon from the pokemons table based on region and encounter rate
        sql = """
        SELECT * FROM pokemons
        WHERE region = %s AND encounter_rate BETWEEN %s AND %s
        ORDER BY RAND()
        LIMIT 1;
        """
        
        result = datatier.retrieve_one_row(dbConn, sql, [user_region, min_encounter_rate, max_encounter_rate])
        
        if not result:
            raise Exception("No Pokemon found for the specified region")
        
        columns = ["pokemonid", "name", "sprite", "type", "region", "encounter_rate"]
        pokemon = dict(zip(columns, result))
        pokemon["rarity"] = rarity
        print(pokemon)
        
        print("DONE. returning")
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
            'body': json.dumps(pokemon)
        }
    
    except Exception as e:
        print("**ERROR**")
        print(str(e))
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
            'body': json.dumps(str(e))
        }