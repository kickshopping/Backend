"use client";
import { useState } from "react";
import style from "../product/product.module.css";

export default function PublicarProductoPage() {
  const [name, setName] = useState("");
  const [price, setPrice] = useState("");
  const [image, setImage] = useState<string | null>(null);
  const [preview, setPreview] = useState<string>("");
  const [success, setSuccess] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleImageChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setImage(file as any);
      setPreview(URL.createObjectURL(file));
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);
    if (!name || !price || !image) {
      setError("Completa todos los campos e incluye una imagen");
      setLoading(false);
      return;
    }
    // Simulación de publicación (aquí iría el fetch real)
    setTimeout(() => {
      setSuccess("¡Producto publicado exitosamente!");
      setLoading(false);
      setName("");
      setPrice("");
      setImage(null);
      setPreview("");
    }, 1200);
  };

  return (
    <div>
      <div className="navbar">
        <div className="navbar-title">KICKSHOPPING</div>
        <div className="right-icons">
          <a href="/">
            <i className="bx bx-home"></i>
          </a>
        </div>
      </div>
      <main className={style["vista-producto"]}>
        <h2 style={{marginBottom:24}}>Publicar nuevo producto</h2>
        <form onSubmit={handleSubmit} style={{maxWidth:400,margin:'0 auto',background:'#fff',padding:24,borderRadius:12,boxShadow:'0 2px 8px #eee'}}>
          <div className={style["producto-imagen"]} style={{marginBottom:16}}>
            {preview ? (
              <img src={preview} alt="preview" style={{width:'100%',borderRadius:'8px'}} />
            ) : (
              <div style={{width:'100%',height:180,background:'#eee',borderRadius:'8px',display:'flex',alignItems:'center',justifyContent:'center',color:'#aaa'}}>Sin imagen</div>
            )}
            <input type="file" accept="image/*" onChange={handleImageChange} style={{marginTop:8}} />
          </div>
          <div className={style["input-box"]}>
            <input
              type="text"
              placeholder="Nombre del producto"
              value={name}
              onChange={e => setName(e.target.value)}
              required
            />
          </div>
          <div className={style["input-box"]}>
            <input
              type="number"
              placeholder="Precio"
              value={price}
              onChange={e => setPrice(e.target.value)}
              required
              min={0}
            />
          </div>
          {error && <div style={{color:'#ff5555',marginBottom:8}}>{error}</div>}
          {success && <div style={{color:'#4caf50',marginBottom:8}}>{success}</div>}
          <button type="submit" className={style["btn-comprar"]} disabled={loading} style={{width:'100%',marginTop:12}}>
            {loading ? "Publicando..." : "Publicar producto"}
          </button>
        </form>
      </main>
    </div>
  );
}
