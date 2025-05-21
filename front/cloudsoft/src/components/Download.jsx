import { useLocation } from "react-router-dom";

const Download = () => {
    const location = useLocation();
    const preview =  location.state?.preview

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
                    <button className="text-white border border-white rounded-md p-2">
                        Téléchargé
                    </button>
                </div>
             </div>
        </div>
    )
}

export default Download;