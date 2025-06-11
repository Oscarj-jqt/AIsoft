import { useState } from "react";
import { useNavigate } from "react-router-dom";

const Login = () => {
  const [pseudo, setPseudo] = useState("");
  const [password, setPassword] = useState("");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
  e.preventDefault();

  try {
    const response = await fetch("http://localhost:5000/login", {
      method: "POST",
      credentials: "include",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ pseudo, password }),
    });

    if (response.ok) {
      console.log("Connexion réussie !");
      navigate("/home");
    } else {
      const errorData = await response.json();
      alert(errorData.error || "Erreur lors de la connexion.");
    }
  } catch (error) {
    console.error("Erreur réseau:", error);
    alert("Erreur réseau. Veuillez réessayer.");
  }
};

  return (
    <main className="flex justify-center items-center flex-1 px-4 relative min-h-screen bg-[url('/fond.jpg')] bg-cover bg-center">
      <div className="absolute inset-0 bg-black bg-opacity-50 backdrop-blur-lg z-0"></div>

      <div className="bg-white bg-opacity-90 backdrop-blur-lg rounded-2xl shadow-lg p-8 w-full sm:w-96 z-10">
        <h1 className="text-3xl font-semibold text-gray-800 mb-8">Connexion</h1>

        <form onSubmit={handleSubmit}>
          <div className="mb-6">
            <label htmlFor="pseudo" className="block text-gray-700 text-lg font-medium">
              Pseudo:
            </label>
            <input
              type="text"
              id="pseudo"
              name="pseudo"
              value={pseudo}
              onChange={(e) => setPseudo(e.target.value)}
              required
              className="w-full mt-2 px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ease-in-out"
            />
          </div>

          <div className="mb-6">
            <label htmlFor="password" className="block text-gray-700 text-lg font-medium">
              Mot de passe:
            </label>
            <input
              type="password"
              id="password"
              name="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              className="w-full mt-2 px-6 py-4 text-lg border-2 border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 ease-in-out"
            />
          </div>

          <button
          onClick={handleSubmit}
            type="submit"
            className="w-full bg-blue-500 text-white py-4 text-lg rounded-xl hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-300 transition ease-in-out duration-200"
          >
            Se connecter
          </button>
        </form>

        <p className="text-sm text-gray-600 text-center mt-6">
          Pas encore de compte ?{" "}
          <a href="/register" className="text-blue-500 hover:underline">
            Inscrivez-vous ici
          </a>
        </p>
      </div>
    </main>
  );
};

export default Login;
