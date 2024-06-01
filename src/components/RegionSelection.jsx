const RegionSelection = ({ regions, onSelect }) => {
  return (
    <div className="p-4 bg-white shadow-md rounded-lg">
      <h2 className="text-2xl font-bold mb-4">Select a Region</h2>
      <div className="grid grid-cols-1 gap-4">
        {regions.map((region) => (
          <button
            key={region.name}
            onClick={() => onSelect(region.name)}
            className="bg-green-600 text-white py-2 px-4 rounded-md hover:bg-green-700 transition duration-300"
          >
            {region.name}
          </button>
        ))}
      </div>
    </div>
  );
};

export default RegionSelection;
