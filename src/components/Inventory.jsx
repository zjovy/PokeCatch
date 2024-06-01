import { useEffect, useState } from 'react';
import { fetchUserInventory } from '../services/api';

const Inventory = ({ userId }) => {
  const [inventory, setInventory] = useState([]);

  useEffect(() => {
    const loadInventory = async () => {
      const data = await fetchUserInventory(userId);
      setInventory(data);
    };

    loadInventory();
  }, [userId]);

  return (
    <div className="p-4 bg-white rounded-lg max-h-screen">
      <h2 className="text-2xl font-bold mb-4">Your Pokemon Inventory</h2>
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
        {inventory.map((pokemon) => (
          <div key={pokemon.pokemonid} className="bg-gray-100 p-4 rounded-lg shadow-md">
            <img src={pokemon.sprite} alt={pokemon.name} className="w-32" />
            <h3 className="mt-2 font-bold">{pokemon.name}</h3>
            <p>Type: {pokemon.type}</p>
            <p>Region: {pokemon.region}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Inventory;
