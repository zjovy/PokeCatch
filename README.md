# PokeCatch

## Overview

PokeCatch is a simple Pokemon-inspired Gatcha Game utilizing the public PokeAPI for all Pokemon data. This project was developed by Jovy Zhou, Sean Lee, and Richard Yang.

Video Demo: [https://www.youtube.com/watch?v=ysIAQj9P2qc](url)

## Features

- **Random Encounter Generator**
- **Load Pokemon Data**
- **Battle System**

## PokeAPI Endpoints

- Get Pokedexes of a region: `https://pokeapi.co/api/v2/region/{id or name}/`
- Get Pokemon entries from pokedex id: `https://pokeapi.co/api/v2/pokedex/{id or name}/`
- Use name to get info: `https://pokeapi.co/api/v2/pokemon/{id or name}/` and `https://pokeapi.co/api/v2/pokemon-species/{id or name}`

## Database Schema

### Tables

1. **Pokemons**
   - `pokemonid`
   - `name`
   - `sprite`
   - `type`
   - `region`
   - `encounter_rate`

2. **Users**
   - `userid`
   - `password`

3. **Inventory**
   - `id`
   - `userid`
   - `pokemonid`

4. **Pokeballs**
   - `userid`
   - `ballcount`

## Lambda Functions

### Load Pokemon Data

This function loads Pokemon data from PokeAPI. For each region, the function retrieves their Pokedex and for each Pokemon species, it checks the evolution status and assigns an encounter rate. The data is then loaded into the MySQL database.

### Random Encounter Generator

This function triggers a random Pokemon encounter based on the user’s current region. It assigns different encounter rates to Pokemons based on their rarity and displays the Pokemon on the website.

### Pokemon Battle

Users can battle each other by selecting a Pokemon from their inventory. The winner is determined based on the power value, which is calculated from the base stats and type effectiveness.

### User Functions

1. **Add User**: Adds a user to the database.
2. **Fetch Users**: Retrieves all user IDs from the database.
3. **Catch Pokemon**: Allows users to catch encountered Pokemon and updates the inventory and Pokeballs tables.
4. **Retrieve User Inventory**: Fetches and displays all the Pokemon a user owns.
5. **Update Pokeball Count**: Updates the user's Pokeball count.
6. **Get Pokeballs**: Retrieves the user's Pokeball count.

## How to Run

1. **Set Up MySQL Database with Amazon RDS**
   - Create the tables as described in the database schema.
   
2. **Configure AWS Lambda Functions**
   - Set up the lambda functions to interact with the PokeAPI and your MySQL database.
   - Modify the config files
   - Upload the lambda functions included to your AWS Lambda

3. **Front-End Integration**
   - Clone this repo for the front-end
   - Install React.js and Tailwind CSS
   - Run the project with vite

## Contributing

Please feel free to submit issues, fork the repository and send pull requests!

## License

This project is licensed under the MIT License.

---

# Contact

For any inquiries, please contact:
- Jovy Zhou
- Sean Lee
- Richard Yang
