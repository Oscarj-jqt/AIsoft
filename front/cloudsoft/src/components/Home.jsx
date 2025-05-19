import { useState } from "react";
// import { axios } from "axios"


const Home = () => {
    const [file, setFile] = useState(null);
    const [preview, setPreview] = useState(null);
    const [items, setItems] = useState([]);
    const [prices, setPrices] = useState([]);

    const handleFile = e => {
        const img = e.target.fil[0]
        setFile(img)
        setPreview(URL.createObjectURL(img))
    }

    const handleDrop = (e) => {
        e.preventDefault()
        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            handleFile(e.dataTransfer.files[0])
        }
    }

    const handleDragOver = (e) => {
        e.preventDefault()
    }

    const analyzeImage = async() => {
          if (!file) return
        const form = new FormData()
        form.append('image', file)
        const res = await axios.post('/api/analyze', form, {
            headers: { 'Content-Type': 'multipart/form-data' }
        })
        setItems(res.data.items)
    }

    // const fetchPrices = async () => {
    //     const allPrices = {}
    //     for (const item of items) {
    //         const r = await axios.get('/api/prices', { params: { item: item.name } })
    //         allPrices[item.name] = r.data.offers
    //     }
    //     setPrices(allPrices)
    // }

    return (
        <div className="">
            <h1 className="font-krona text-3xl text-white ">ARMATUS</h1>
            <div className="p-6 bg-gray-800 rounded-xl flex flex-col gap-4 max-w-lg mx-auto">
                <div
                    onDrop={handleDrop}
                    onDragOver={handleDragOver}
                    className="w-full h-40 border-2 border-dashed border-gray-400 rounded flex items-center justify-center text-white cursor-pointer hover:bg-gray-700"
                >
                {preview ? (
                    <img src={preview} alt="preview" className="w-full h-full object-contain rounded" />
                ) : (
                    <span>Glissez une image ici ou cliquez pour choisir</span>
                )}
                <input
                    type="file"
                    accept="image/*"
                    onChange={(e) => handleFile(e.target.files[0])}
                    className="hidden"
                    id="upload"
                />
                </div>

                <label 
                htmlFor="upload"
                className="bg-gray-600 hover:bg-gray-700 text-white text-center py-2 rounded cursor-pointer"
                >
                    Ou choisir une image
                </label>

                <button
                    onClick={analyzeImage}
                    className="bg-black text-white px-4 py-2 rounded-lg border-solid border-white"
                >
                    Analyser l'image
                </button>
            </div>
        </div>
    )   
}

export default Home;