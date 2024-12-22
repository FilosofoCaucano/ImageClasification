import React, { useState } from 'react';
import axios from 'axios';
import '../styles.css';  // Importa el CSS

const ImageUploader = () => {
    const [image, setImage] = useState(null);
    const [result, setResult] = useState(null);
    const [loading, setLoading] = useState(false);

    const handleImageChange = (e) => {
        setImage(e.target.files[0]);
        setResult(null);
    };

    const handleUpload = async () => {
        if (!image) return alert('Selecciona una imagen.');

        const formData = new FormData();
        formData.append('file', image);

        try {
            setLoading(true);
            console.log('Enviando imagen al backend...');
            const response = await axios.post('http://localhost:5000/api/image-classification', formData);
            setResult(response.data);
        } catch (error) {
            console.error('Error al procesar la imagen:', error);
            alert('Error al procesar la imagen.');
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="container">
            <h1>Clasificador de Imágenes Climáticas</h1>
            <input type="file" onChange={handleImageChange} />
            <button onClick={handleUpload} disabled={loading}>
                {loading ? 'Cargando...' : 'Clasificar Imagen'}
            </button>
            {result && (
                <div className="result">
                    <p>Clase: <strong>{result.class}</strong></p>
                    <p>Confianza: <strong>{result.confidence}%</strong></p>
                </div>
            )}
        </div>
    );
};

export default ImageUploader;
