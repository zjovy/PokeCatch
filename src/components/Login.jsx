import { useState } from "react";
import { logIn } from "../services/api";

const Login = ({ setLoggedIn, setUsername, onClose }) => {
  const [localUsername, setLocalUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (localUsername.trim() === "" || password.trim() === "") {
      alert("Please fill in both fields");
      return;
    }

    // Mock log in logic
    await logIn(localUsername, password);

    setUsername(localUsername);
    setLoggedIn(true);
    onClose();
  };

  return (
    <div className="font-press2p relative bg-white p-8 rounded-lg w-80">
      <form onSubmit={handleSubmit} className="flex flex-col items-center">
        <h2 className="text-2xl font-bold mb-6 text-center">Login</h2>
        <div className="mb-4 w-full">
          <input
            type="text"
            placeholder="Username"
            value={localUsername}
            onChange={(e) => setLocalUsername(e.target.value)}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-600"
          />
        </div>
        <div className="mb-6 w-full">
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full px-4 py-2 border rounded-md focus:outline-none focus:ring-2 focus:ring-green-600"
          />
        </div>
        <button
          type="submit"
          className="w-full bg-green-600 text-white py-2 rounded-md hover:bg-green-700 transition duration-300"
        >
          Login
        </button>
      </form>
    </div>
  );
};

export default Login;
