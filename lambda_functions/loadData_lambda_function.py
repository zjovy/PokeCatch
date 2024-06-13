import json
import datatier
import os
import requests

from configparser import ConfigParser

def lambda_handler(event, context):
    try:
        print("**STARTING**")
        print("**lambda: loadData**")
        
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

        # Open database connection
        print("**Opening connection**")
        dbConn = datatier.get_dbConn(rds_endpoint, rds_portnum, rds_username, rds_pwd, rds_dbname)
        
        # Hard coded region data
        regions = [
            { "name": "kanto", "url": "https://pokeapi.co/api/v2/pokedex/2/" },
            { "name": "johto", "url": "https://pokeapi.co/api/v2/pokedex/3/" },
            { "name": "hoenn", "url": "https://pokeapi.co/api/v2/pokedex/4/" },
            { "name": "sinnoh", "url": "https://pokeapi.co/api/v2/pokedex/5/" },
            { "name": "unova", "url": "https://pokeapi.co/api/v2/pokedex/8/" },
            { "name": "kalos", "url": "https://pokeapi.co/api/v2/pokedex/12/" },
            { "name": "alola", "url": "https://pokeapi.co/api/v2/pokedex/16/" },
            { "name": "galar", "url": "https://pokeapi.co/api/v2/pokedex/27/" },
            { "name": "hisui", "url": "https://pokeapi.co/api/v2/pokedex/30/" },
            { "name": "paldea", "url": "https://pokeapi.co/api/v2/pokedex/31/" },
        ]
        
        # Fetch and insert Pokémon data
        for r in regions:
            pokedex_response = requests.get(r["url"])
            pokedex_response.raise_for_status()
            pokedex = pokedex_response.json()
            pokemon_entries = pokedex["pokemon_entries"]
            
            for entry in pokemon_entries:
                pokemon_species_url = entry["pokemon_species"]["url"]
                species_response = requests.get(pokemon_species_url)
                species_response.raise_for_status()
                species = species_response.json()
                
                pokemonid = species["id"]
                
                sql = """
                SELECT COUNT(*) FROM pokemons WHERE pokemonid = %s
                """
                
                result = datatier.retrieve_one_row(dbConn, sql, [pokemonid])
                
                if result[0] > 0:
                    print(f"Pokemon with ID {pokemonid} already exists. Skipping.")
                    continue
                
                name = species["name"]
                
                pokemon_response = requests.get(f"https://pokeapi.co/api/v2/pokemon/{pokemonid}")
                pokemon_response.raise_for_status()
                pokemon = pokemon_response.json()
                
                sprite = pokemon["sprites"]["front_default"]
                
                # Concatenate types
                types = "/".join(t["type"]["name"] for t in pokemon["types"])
                
                region = r["name"]
                
                # Calculate encounter rate
                if species["is_legendary"] or species["is_mythical"]:
                    encounter_rate = 5
                else:
                    encounter_rate = 60 if species["evolves_from_species"] is not None else 90
                    
                    average_base_stat = sum(stat["base_stat"] for stat in pokemon["stats"]) / len(pokemon["stats"])
                    base_stat_factor = average_base_stat / 10
                    encounter_rate -= base_stat_factor
                    
                    base_experience = pokemon["base_experience"]
                    if base_experience < 100:
                        encounter_rate -= 2
                    elif base_experience < 200:
                        encounter_rate -= 25
                    else:
                        encounter_rate -= 40
                    
                    encounter_rate = max(min(encounter_rate, 100), 5)
                
                sql = """
                INSERT INTO pokemons(pokemonid, name, sprite, type, region, encounter_rate)
                VALUES(%s, %s, %s, %s, %s, %s)
                """
                
                datatier.perform_action(dbConn, sql, [pokemonid, name, sprite, types, region, encounter_rate])
        
        print("**DONE, returning**")
        return {
          'statusCode': 200,
          'body': "success"
        }
   
    except Exception as err:
        print("**ERROR**")
        print(str(err))
        
        return {
          'statusCode': 400,
          'body': json.dumps(str(err))
        }
