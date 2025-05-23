const Arme = () => {
    return (
        <div className="flex items-center justify-center min-h-screen p-6 bg-gray-900">
            <div className="p-6 bg-black rounded-xl flex flex-col gap-4 max-w-lg w-full text-white">
                <h1 className="font-krona text-3xl text-center text-white">AISOFT</h1>

                <div className="mt-6 space-y-4">
                    <h2 className="text-2xl font-bold">AK 47</h2>
                    <p className="text-sm text-gray-300">
                        L'AK-47 est un fusil d'assaut soviétique conçu par Mikhaïl Kalachnikov. Robuste, fiable et facile à entretenir,
                        il est largement utilisé dans le monde entier depuis les années 1940.
                    </p>
                    <ul className="text-sm text-gray-400 list-disc list-inside">
                        <li>Calibre : 7.62×39mm</li>
                        <li>Cadence de tir : 600 coups/min</li>
                        <li>Portée effective : 350 m</li>
                        <li>Chargeur : 30 cartouches</li>
                    </ul>
                    <p className="text-lg font-semibold text-green-400">Prix estimé : 500 $</p>
                </div>
            </div>
        </div>
    );
};

export default Arme;
