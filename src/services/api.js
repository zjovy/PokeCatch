
export const fetchUserInventory = async (userId) => {
    try {
    //  const response = await fetch(`https://your-api-gateway-url.com/inventory?userId=${userId}`);
    //  const data = await response.json();
    const mockInventory = [
        {
          pokemonid: 1,
          name: 'Bulbasaur',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/1.png',
          type: 'Grass/Poison',
          region: 'Kanto'
        },
        {
          pokemonid: 4,
          name: 'Charmander',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/4.png',
          type: 'Fire',
          region: 'Kanto'
        },
        {
          pokemonid: 7,
          name: 'Squirtle',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/7.png',
          type: 'Water',
          region: 'Kanto'
        },
        {
          pokemonid: 25,
          name: 'Pikachu',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/25.png',
          type: 'Electric',
          region: 'Kanto'
        },
        {
          pokemonid: 152,
          name: 'Chikorita',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/152.png',
          type: 'Grass',
          region: 'Johto'
        },
        {
          pokemonid: 155,
          name: 'Cyndaquil',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/155.png',
          type: 'Fire',
          region: 'Johto'
        },
        {
          pokemonid: 158,
          name: 'Totodile',
          sprite: 'https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/158.png',
          type: 'Water',
          region: 'Johto'
        }
      ];
  
      const data = mockInventory;
      return data;
    } catch (error) {
      console.error('Error fetching user inventory:', error);
      return [];
    }  
};
  
export const fetchRandomEncounter = async (region) => {
    try {
    //   const response = await fetch(`https://your-api-gateway-url.com/random-encounter?region=${region}`);
      const response = await fetch("https://pokeapi.co/api/v2/pokemon/charmander");
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching random encounter:', error);
      return null;
    }
};
  

export const fetchPokeballs = async (userId) => {
    try {
      const response = await fetch(`https://your-api-gateway-url.com/get-pokeballs?userId=${userId}`, {
        method: 'GET',
      });
      const data = await response.json();
      return data.ballCount; // assuming the response contains the number of pokeballs
    } catch (error) {
      console.error('Error fetching pokeballs:', error);
      return 0;
    }
};
  
export const increasePokeballs = async (userId) => {
    try {
      const response = await fetch(`https://your-api-gateway-url.com/post-pokeballs?userId=${userId}`, {
        method: 'POST',
      });
      const data = await response.json();
      return data.ballCount; // assuming the response contains the number of pokeballs
    } catch (error) {
      console.error('Error increasing pokeballs:', error);
      return 0;
    }
};

export const catchPokemon = async (userId, pokemonId) => {
    try {
      const response = await fetch(`https://your-api-gateway-url.com/catch-pokemon?userId=${userId}?pokemonId=${pokemonId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId, pokemonId }),
      });
      const data = await response.json();
      return data
    } catch (error) {
      console.error('Error catching pokemon:', error);
      return false;
    }
};

export const fetchUsers = async () => {
    try {
      const response = await fetch(`https://your-api-gateway-url.com/fetch-users`, {
        method: 'GET',
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error fetching users:', error);
      return [];
    }
};
  
  export const initiateBattle = async (userId, opponentId) => {
    try {
      const response = await fetch(`https://your-api-gateway-url.com/battle`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ userId, opponentId }),
      });
      const data = await response.json();
      return data;
    } catch (error) {
      console.error('Error initiating battle:', error);
      return null;
    }
};