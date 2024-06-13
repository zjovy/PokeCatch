import json
import datatier
import os
import requests

from configparser import ConfigParser

# type effectiveness chart
type_effectiveness = {
    "normal": {"rock": 0.8, "ghost": 0.0, "steel": 0.8},
    "fire": {"fire": 0.8, "water": 0.8, "grass": 1.2, "ice": 1.2, "bug": 1.2, "rock": 0.8, "dragon": 0.8, "steel": 1.2},
    "water": {"fire": 1.2, "water": 0.8, "grass": 0.8, "ground": 1.2, "rock": 1.2, "dragon": 0.8},
    "electric": {"water": 1.2, "electric": 0.8, "grass": 0.8, "ground": 0.0, "flying": 1.2, "dragon": 0.8},
    "grass": {"fire": 0.8, "water": 1.2, "grass": 0.8, "poison": 0.8, "ground": 1.2, "flying": 0.8, "bug": 0.8, "rock": 1.2, "dragon": 0.8, "steel": 0.8},
    "ice": {"fire": 0.8, "water": 0.8, "grass": 1.2, "ice": 0.8, "ground": 1.2, "flying": 1.2, "dragon": 1.2, "steel": 0.8},
    "fighting": {"normal": 1.2, "ice": 1.2, "poison": 0.8, "flying": 0.8, "psychic": 0.8, "bug": 0.8, "rock": 1.2, "ghost": 0.0, "dark": 1.2, "steel": 1.2, "fairy": 0.8},
    "poison": {"grass": 1.2, "poison": 0.8, "ground": 0.8, "rock": 0.8, "ghost": 0.8, "steel": 0.0, "fairy": 1.2},
    "ground": {"fire": 1.2, "electric": 1.2, "grass": 0.8, "poison": 1.2, "flying": 0.0, "bug": 0.8, "rock": 1.2, "steel": 1.2},
    "flying": {"electric": 0.8, "grass": 1.2, "fighting": 1.2, "bug": 1.2, "rock": 0.8, "steel": 0.8},
    "psychic": {"fighting": 1.2, "poison": 1.2, "psychic": 0.8, "dark": 0.0, "steel": 0.8},
    "bug": {"fire": 0.8, "grass": 1.2, "fighting": 0.8, "poison": 0.8, "flying": 0.8, "psychic": 1.2, "ghost": 0.8, "dark": 1.2, "steel": 0.8, "fairy": 0.8},
    "rock": {"fire": 1.2, "ice": 1.2, "fighting": 0.8, "ground": 0.8, "flying": 1.2, "bug": 1.2, "steel": 0.8},
    "ghost": {"normal": 0.0, "psychic": 1.2, "ghost": 1.2, "dark": 0.8},
    "dragon": {"dragon": 1.2, "steel": 0.8, "fairy": 0.0},
    "dark": {"fighting": 0.8, "psychic": 1.2, "ghost": 1.2, "dark": 0.8, "fairy": 0.8},
    "steel": {"fire": 0.8, "water": 0.8, "electric": 0.8, "ice": 1.2, "rock": 1.2, "steel": 0.8, "fairy": 1.2},
    "fairy": {"fire": 0.8, "fighting": 1.2, "poison": 0.8, "dragon": 1.2, "dark": 1.2, "steel": 0.8}
}

def get_type_effectiveness(attacker_types, defender_types):
    effectiveness = 1.0
    for atk_type in attacker_types:
        for def_type in defender_types:
            if atk_type in type_effectiveness and def_type in type_effectiveness[atk_type]:
                effectiveness *= type_effectiveness[atk_type][def_type]
    return effectiveness

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: battle**")
        
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
        
        # userid and opponentid from event
        print("**Accessing event**")
        
        if "body" not in event:
          raise Exception("event has no body")
          
        body = json.loads(event["body"]) # parse the json
        
        if "userid" not in body:
          raise Exception("event has a body but no userid")
        if "opponentid" not in body:
          raise Exception("event has a body but no opponentid")
    
        userid = body["userid"]
        opponentid = body["opponentid"]

        # Open database connection
        print("**Opening connection**")
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        
        # randomly pick one Pokemon from user and one from opponent
        sql = """
        SELECT pokemonid
        FROM inventory
        WHERE userid = %s
        ORDER BY RAND()
        LIMIT 1;
        """
        
        me = datatier.retrieve_one_row(dbConn, sql, [userid])
        if not me:
            raise Exception("user inventory empty")
        myPokemonId = me[0]
        
        enemy = datatier.retrieve_one_row(dbConn, sql, [opponentid])
        if not enemy:
            raise Exception("opponent inventory empty")
        opponentPokemonId = enemy[0]
        
        # get Pokemon data from PokeAPI
        baseurl = "https://pokeapi.co/api/v2/pokemon/"
        
        myPokemon = requests.get(baseurl + str(myPokemonId)).json()
        opponentPokemon = requests.get(baseurl + str(opponentPokemonId)).json()
        
        # get base stats
        myStats = myPokemon["stats"]
        opponentStats = opponentPokemon["stats"]
        
        # base power is sum of base stats
        myPower = sum(stat["base_stat"] for stat in myStats)
        opponentPower = sum(stat["base_stat"] for stat in opponentStats)
        
        # get types
        myTypes = [t['type']['name'] for t in myPokemon['types']]
        opponentTypes = [t['type']['name'] for t in opponentPokemon['types']]
        
        # calculate type effectiveness
        myTypeEffectiveness = get_type_effectiveness(myTypes, opponentTypes)
        opponentTypeEffectiveness = get_type_effectiveness(opponentTypes, myTypes)
        
        # adjust power based on type effectiveness
        myAdjustedPower = round(myPower * myTypeEffectiveness, 2)
        opponentAdjustedPower = round(opponentPower * opponentTypeEffectiveness, 2)
        
        # get winner
        if myAdjustedPower > opponentAdjustedPower:
            winner = userid
        elif opponentAdjustedPower > myAdjustedPower:
            winner = opponentid
        else:
            winner = "draw"
        
        result = {
            'user_pokemon': {
                'id': myPokemon['id'],
                'name': myPokemon['name'],
                'types': myTypes,
                'power': myAdjustedPower,
                'sprite': myPokemon['sprites']['front_default']
            },
            'opponent_pokemon': {
                'id': opponentPokemon['id'],
                'name': opponentPokemon['name'],
                'types': opponentTypes,
                'power': opponentAdjustedPower,
                'sprite': opponentPokemon['sprites']['front_default']
            },
            'winner': winner
        }
        
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
            'body': json.dumps(result)
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
