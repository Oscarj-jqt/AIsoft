import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";

const apiUrl = import.meta.env.VITE_API_URL;


const Home = () => {
    const [name, setName] = useState("");
    const [brand, setBrand] = useState("");
    const [model, setModel] = useState("");
    const [type, setType] = useState("");
    const [price, setPrice] = useState("");
    const [description, setDescription] = useState("");
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);

    const [backendMessage, setBackendMessage] = useState("Connexion au back…");

    const navigate = useNavigate();

    const handleDrop = (e) => {
        e.preventDefault();
        const droppedFile = e.dataTransfer.files[0];
        if (droppedFile) {
            handleFile(droppedFile);
        }
    };

    const handleDragOver = (e) => {
        e.preventDefault();
    };

    const handleFile = (file) => {
        if (!file) return;
        setFile(file);
        setPreview(URL.createObjectURL(file));
    };

    const goToUpload = async () => {
    if (!file || !preview) return;

    const formData = new FormData();
    formData.append("image", file);
    formData.append("name", name);
    formData.append("brand", brand);
    formData.append("model", model);
    formData.append("type", type);
    formData.append("price", price);
    formData.append("description", description);

    try {
        const res = await fetch(`${apiUrl}/upload`, {
            method: "POST",
            credentials: "include", 
            body: formData,
        });

        if (res.ok) {
            alert("Upload réussi !");
            navigate("/analyze", { state: { file, preview } });
        } else {
            const errorText = await res.text();
            alert("Erreur à l'upload : " + errorText);
        }
    } catch (err) {
        console.error(err);
        alert("Erreur réseau");
    }
};

    useEffect(() => {
        fetch(`${apiUrl}/`)
            .then((res) => res.text())
            .then((data) => setBackendMessage(data))
            .catch((err) => setBackendMessage("Erreur : back injoignable"));
    }, []);

    return (
        <div className="items-center justify-center min-h-screen p-6">
            <h1 className="font-krona text-3xl text-white flex justify-center">AIsoft</h1>
            <p className="text-white text-sm mt-4 text-center">{backendMessage}</p>

            <div className="p-6 bg-black rounded-xl flex flex-col gap-4 max-w-lg mx-auto my-auto mt-28">
                <div
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    className="w-full min-h-[240px] border border-white rounded-2xl flex items-center justify-center text-white cursor-pointer bg-white/30"
                >
                    {preview ? (
                        <img src={preview} alt="preview" className="max-w-full max-h-[220px] object-contain rounded" />
                    ) : (
                        <label
                            htmlFor="upload"
                            className="bg-[#d3d3d3] text-black text-center p-3 rounded-full cursor-pointer font-bold w-24 h-24 flex flex-col items-center"
                        >
                            <svg
                                xmlns="http://www.w3.org/2000/svg"
                                className="w-8 h-8 text-black"
                                fill="none"
                                viewBox="0 0 24 24"
                                stroke="currentColor"
                                strokeWidth={2}
                            >
                                <path strokeLinecap="round" strokeLinejoin="round" d="M5 12l7-7 7 7M12 5v14" />
                            </svg>
                            UPLOAD
                        </label>
                    )}
                    <input
                        type="file"
                        accept="image/*"
                        onChange={(e) => handleFile(e.target.files[0])}
                        className="hidden"
                        id="upload"
                    />
                </div>
                {!preview && (
                    <p className="text-red-500 text-sm font-krona">
                        Vous devez mettre une image
                    </p>
                )}

                <input type="text" placeholder="Nom" onChange={(e) => setName(e.target.value)} className="input-style" />
                <input type="text" placeholder="Marque" onChange={(e) => setBrand(e.target.value)} className="input-style" />
                <input type="text" placeholder="Modèle" onChange={(e) => setModel(e.target.value)} className="input-style" />
                <input type="text" placeholder="Type" onChange={(e) => setType(e.target.value)} className="input-style" />
                <input type="number" placeholder="Prix" onChange={(e) => setPrice(e.target.value)} className="input-style" />
                <textarea placeholder="Description" onChange={(e) => setDescription(e.target.value)} className="input-style" />
                <div>
                    <button
                        onClick={goToUpload}
                        disabled={!preview}
                        className={`px-4 py-2 rounded-lg font-krona border ${
                            preview
                                ? "bg-black text-white border-white cursor-pointer"
                                : " text-white border-gray-300 cursor-not-allowed"
                        }`}
                    >
                        Upload
                    </button>
                </div>
            </div>

            <div className="flex items-center gap-3 mt-5">
                <img src="/attention.svg" alt="attention" className="h-10 w-10 bg-white" />
                <p className="font-krona text-[#C00F0C] text-sm">
                    Notre application est conçue exclusivement pour identifier des répliques d’armes de type airsoft.
                </p>
            </div>
        </div>
    );
};

export default Home;
