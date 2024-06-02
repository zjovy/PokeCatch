const baseurl = "https://m8rdzn4157.execute-api.us-east-2.amazonaws.com/prod";

export const logIn = async (userid, password) => {
  try {
    const response = await fetch(`${baseurl}/user`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userid, password }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error logging in:', error);
    return null;
  }
};

export const fetchUserInventory = async (userid) => {
  try {
    const response = await fetch(`${baseurl}/inventory/${userid}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching user inventory:', error);
    return [];
  }  
};
  
export const fetchRandomEncounter = async (region) => {
  try {
    const response = await fetch(`${baseurl}/random-encounter/${region}`);
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching random encounter:', error);
    return null;
  }
};

export const fetchPokeballs = async (userid) => {
  try {
    const response = await fetch(`${baseurl}/get-pokeballs/${userid}`, {
      method: 'GET',
    });
    const data = await response.json();
    return data.ballcount;
  } catch (error) {
    console.error('Error fetching pokeballs:', error);
    return 0;
  }
};
  
export const increasePokeballs = async (userid) => {
  try {
    const response = await fetch(`${baseurl}/add-pokeball`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userid }),
    });
    const data = await response.json();
    return data.ballcount; // assuming the response contains the number of pokeballs
  } catch (error) {
    console.error('Error increasing pokeballs:', error);
    return 0;
  }
};

export const catchPokemon = async (userid, pokemonid) => {
  try {
      const response = await fetch(`${baseurl}/catch`, {
          method: 'POST',
          headers: {
              'Content-Type': 'application/json',
          },
          body: JSON.stringify({ userid, pokemonid }),
      });
      const data = await response.json();
      if (response.ok) {
          return data;
      } else {
          throw new Error(data.message);
      }
  } catch (error) {
      console.error('Error catching pokemon:', error);
      return null;
  }
};

export const fetchUsers = async () => {
  try {
    const response = await fetch(`${baseurl}/users`, {
      method: 'GET',
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error fetching users:', error);
    return [];
  }
};
  
export const initiateBattle = async (userid, opponentid) => {
  try {
    const response = await fetch(`${baseurl}/battle`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ userid, opponentid }),
    });
    const data = await response.json();
    return data;
  } catch (error) {
    console.error('Error initiating battle:', error);
    return null;
  }
};