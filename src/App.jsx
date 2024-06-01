import { useState, useEffect } from "react";
import Inventory from "./components/Inventory";
import Login from "./components/Login";
import Modal from "./components/Modal";
import RegionSelection from "./components/RegionSelection";
import {
  fetchRandomEncounter,
  fetchPokeballs,
  increasePokeballs,
  catchPokemon,
  fetchUsers,
  initiateBattle,
} from "./services/api";

const regions = [
  { name: "Kanto", url: "https://pokeapi.co/api/v2/region/1/" },
  { name: "Johto", url: "https://pokeapi.co/api/v2/region/2/" },
  { name: "Hoenn", url: "https://pokeapi.co/api/v2/region/3/" },
  { name: "Sinnoh", url: "https://pokeapi.co/api/v2/region/4/" },
  { name: "Unova", url: "https://pokeapi.co/api/v2/region/5/" },
  { name: "Kalos", url: "https://pokeapi.co/api/v2/region/6/" },
];

const App = () => {
  const [isModalVisible, setModalVisible] = useState(false);
  const [isLoggedIn, setLoggedIn] = useState(false);
  const [isInventoryVisible, setInventoryVisible] = useState(false);
  const [isRegionModalVisible, setRegionModalVisible] = useState(false);
  const [userId, setUserId] = useState("");
  const [opponentId, setOpponentId] = useState("");
  const [users, setUsers] = useState([]);
  const [encounteredPokemon, setEncounteredPokemon] = useState(null);
  const [battleResult, setBattleResult] = useState(null);
  const [farmCount, setFarmCount] = useState(0);
  const [pokeballCount, setPokeballCount] = useState(0);

  useEffect(() => {
    const getPokeballCount = async () => {
      if (userId) {
        const count = await fetchPokeballs(userId);
        setPokeballCount(count);
      }
    };
    getPokeballCount();
  }, [userId]);

  useEffect(() => {
    const loadUsers = async () => {
      const userList = await fetchUsers();
      setUsers(userList);
    };
    loadUsers();
  }, []);

  const toggleModal = () => {
    setModalVisible(!isModalVisible);
  };

  const toggleInventory = () => {
    setInventoryVisible(!isInventoryVisible);
  };

  const toggleRegionModal = () => {
    setRegionModalVisible(!isRegionModalVisible);
  };

  const handleRegionSelect = async (region) => {
    toggleRegionModal();
    const data = await fetchRandomEncounter(region.url);
    setEncounteredPokemon(data);
  };

  const getPokeballs = async () => {
    setFarmCount(farmCount + 1);
    if (farmCount + 1 >= 50) {
      const newPokeballs = await increasePokeballs(userId);
      setPokeballCount(pokeballCount + newPokeballs);
      setFarmCount(0);
    }
  };

  const handleCatchPokemon = async () => {
    if (pokeballCount > 0) {
      const success = await catchPokemon(userId, encounteredPokemon.id);
      if (success) {
        setPokeballCount(pokeballCount - 1);
        alert(`You caught ${encounteredPokemon.name}!`);
        setEncounteredPokemon(null);
      } else {
        alert("Failed to catch the Pokemon. Try again!");
      }
    } else {
      alert("You do not have enough Pokeballs!");
    }
  };

  const handleBattle = async () => {
    const result = await initiateBattle(userId, opponentId);
    setBattleResult(result);
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
      {!isLoggedIn && (
        <>
          <h1 className="font-press2p text-3xl mb-6">
            <span className="font-bold">Poke</span><span className="text-red-600">Catch</span>
          </h1>
          <button
            onClick={toggleModal}
            className="font-press2p bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition duration-300"
          >
            Login
          </button>
          <Modal isVisible={isModalVisible} onClose={toggleModal}>
            <Login
              setLoggedIn={setLoggedIn}
              setUsername={setUserId}
              onClose={toggleModal}
            />
          </Modal>
        </>
      )}
      {isLoggedIn && (
        <div className="font-press2p w-full max-w-lg">
          <h1 className="text-3xl mb-6 text-center">Welcome, {userId}!</h1>
          <div className="flex flex-col gap-4 mb-6">
            <div className="flex items-center justify-between w-full">
              <select
                value={opponentId}
                onChange={(e) => setOpponentId(e.target.value)}
                className="bg-white border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 p-2.5"
              >
                <option value="">Select Opponent</option>
                {users.map((user) => (
                  <option key={user.userid} value={user.userid}>
                    {user.username}
                  </option>
                ))}
              </select>
              <button
                onClick={handleBattle}
                className="bg-red-600 text-white py-2 px-4 rounded-md hover:bg-red-700 transition duration-300"
              >
                Battle!
              </button>
            </div>
            <button
              onClick={toggleInventory}
              className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition duration-300"
            >
              View Inventory
            </button>
            <button
              onClick={toggleRegionModal}
              className="bg-indigo-600 text-white py-2 px-4 rounded-md hover:bg-indigo-700 transition duration-300"
            >
              Catch Pokemon
            </button>
            <div className="flex items-center">
              <button
                onClick={getPokeballs}
                className="bg-yellow-600 text-white py-2 px-4 rounded-md hover:bg-yellow-700 transition duration-300"
              >
                Get Pokeballs
              </button>
              <span className="ml-2">x {farmCount}/50</span>
              <span className="ml-2">Total: {pokeballCount}</span>
            </div>
          </div>
          <Modal isVisible={isInventoryVisible} onClose={toggleInventory}>
            <Inventory userId={userId} />
          </Modal>
          <Modal isVisible={isRegionModalVisible} onClose={toggleRegionModal}>
            <RegionSelection regions={regions} onSelect={handleRegionSelect} />
          </Modal>
          {encounteredPokemon && (
            <div className="mt-6 flex flex-col items-center">
              <h2 className="text-2xl font-bold">
                You encountered a {encounteredPokemon.name}!
              </h2>
              <img
                src={encounteredPokemon.sprites.front_default}
                alt={encounteredPokemon.name}
                className="w-36"
              />
              <button
                onClick={handleCatchPokemon}
                className="mt-4 bg-purple-600 text-white py-2 px-4 rounded-md hover:bg-purple-700 transition duration-300"
              >
                Catch!
              </button>
            </div>
          )}
          {battleResult && (
            <div className="mt-6 flex flex-col items-center">
              <h2 className="text-2xl font-bold">Battle Result</h2>
              <p>{battleResult.battleResult}</p>
              <div className="flex space-x-4">
                <div>
                  <h3 className="font-bold">Your Pokemon</h3>
                  <p>{battleResult.userPokemon.name}</p>
                  <img
                    src={battleResult.userPokemon.sprite}
                    alt={battleResult.userPokemon.name}
                    className="w-36"
                  />
                </div>
                <div>
                  <h3 className="font-bold">Opponent's Pokemon</h3>
                  <p>{battleResult.opponentPokemon.name}</p>
                  <img
                    src={battleResult.opponentPokemon.sprite}
                    alt={battleResult.opponentPokemon.name}
                    className="w-36"
                  />
                </div>
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default App;
