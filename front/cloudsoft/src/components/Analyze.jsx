import { useLocation, useNavigate } from "react-router-dom";

const Analyze = () => {
    const location = useLocation();
    const preview =  location.state?.preview
    const navigate = useNavigate();

    return (
        <div className="items-center justify-center min-h-screen p-6">
            <h1 className="font-krona text-3xl text-white flex justify-center">AISOFT</h1>
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
                <div className="">
                    <button 
                    className="text-white border border-white rounded-md p-2"
                    onClick={() => navigate('/arme')}
                    >
                        Analyze
                    </button>
                </div>
             </div>
            <div className="flex items-center gap-3">
                <img src="/attention.svg" alt="attention" className="h-10 w-10 bg-white" />
                <p className="font-krona text-[#C00F0C] text-sm">
                    Notre application est conçue exclusivement pour identifier des répliques d’armes de type airsoft.
                </p>
            </div>
        </div>
    )
}

export default Analyze;