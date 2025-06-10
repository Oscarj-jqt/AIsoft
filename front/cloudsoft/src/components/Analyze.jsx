import { useLocation, useNavigate } from "react-router-dom";
import { useState } from "react";

const Analyze = () => {
    const location = useLocation();
    const preview = location.state?.preview;
    const file = location.state?.file;
    const navigate = useNavigate();

    const [loading, setLoading] = useState(false);
    const [result, setResult] = useState(null);
    const [error, setError] = useState(null);

    const handleAnalyze = async () => {
        if (!file) {
            setError("Aucune image sélectionnée.");
            return;
        }

        setLoading(true);
        setError(null);
        setResult(null);

        const formData = new FormData();
        formData.append("image", file);

        try {
            const res = await fetch("http://127.0.0.1:5000/analyze", {
                method: "POST",
                credentials: "include",
                body: formData,
            });

            const data = await res.json();
            console.log("Résultat analyse reçu :", data);

            if (res.ok) {
                setResult(data);
            } else {
                setError(data.error || "Erreur lors de l'analyse.");
            }
        } catch (err) {
            setError("Erreur de connexion au serveur.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="items-center justify-center min-h-screen p-6 bg-[url('/fond.jpg')] bg-cover bg-center">
            <div className="flex flex-col items-center">
                <h1 className="font-krona text-5xl text-white flex justify-center mt-5 text-outline">AIsoft</h1>
                <div className="w-full">
                    <div className="p-6 bg-black rounded-xl flex flex-col gap-4 max-w-lg mx-auto my-auto mt-28">
                        <div className="w-full min-h-[240px] border border-white rounded-2xl flex items-center justify-center text-white cursor-pointer bg-white/30">
                            {preview ? (
                                <img
                                    src={preview}
                                    alt="preview"
                                    className="max-w-full max-h-[220px] object-contain rounded"
                                />
                            ) : (
                                <p className="text-white">Aucune image sélectionnée.</p>
                            )}
                        </div>

                        {!result && (
                            <button
                                className="text-white border border-white rounded-md p-2"
                                onClick={handleAnalyze}
                                disabled={loading}
                            >
                                {loading ? "Analyse en cours..." : "Analyser"}
                            </button>
                        )}

                        {error && <p className="text-red-500 text-sm">{error}</p>}

                        {result && (
                            <div className="flex gap-5">
                                <div className="text-white text-sm mt-2">
                                    <h2 className="text-white font-semibold text-base mb-1">Résultat de l'analyse</h2>
                                    <p><strong>Nom :</strong> {result.weapon?.name || "Inconnu"}</p>
                                    <p><strong>Score de confiance :</strong> {result.confidence_score ?? "Non disponible"}%</p>

                                    {result.store_address && (
                                        <p><strong>Magasin :</strong> {result.store_address.name} ({result.store_address.address})</p>
                                    )}

                                    {result.online_site && (
                                        <p>
                                            <strong>Site Web :</strong>{" "}
                                            <a
                                                href={result.online_site.website}
                                                target="_blank"
                                                rel="noopener noreferrer"
                                                className="text-blue-400 underline"
                                            >
                                                {result.online_site.website}
                                            </a>
                                        </p>
                                    )}
                                </div>
                            </div>
                        )}


                            {result && !result.match_found && (
                                <p className="text-yellow-400 text-sm mt-2">{result.message}</p>
                            )}
                        <button
                            className="text-white text-sm flex items-center gap-1 hover:underline"
                            onClick={() => navigate("/home")}
                        >
                            <span className="text-xl">↩</span> Retour à l'upload
                        </button>
                    </div>

                    <div className="absolute bottom-4 left-4">
                    </div>
                </div>
                <div className="flex items-center gap-3 mt-10 w-[35%]">
                    <img src="/attention.svg" alt="attention" className="h-10 w-10 bg-white" />
                    <p className="font-krona text-[#C00F0C] text-sm">
                        Notre application est conçue exclusivement pour identifier des répliques d’armes de type airsoft.
                    </p>
                </div>
            </div>
            
        </div>
    );
};

export default Analyze;
