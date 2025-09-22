"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState, useEffect } from "react";
import style from "./product.module.css"; // Importa los estilos específicos de esta página

export default function ProductPage() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  // Alterna abrir/cerrar menú
  const toggleMenu = () => setMenuOpen(!menuOpen);

  // Para demo: obtener el primer producto del backend
  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const res = await fetch("http://localhost:8000/products/");
        const data = await res.json();
        setProduct(data[0] || null);
      } catch (err) {
        setError("No se pudo cargar el producto");
      }
      setLoading(false);
    };
    fetchProduct();
  }, []);

  return (
    <div>
      {/* Barra de navegación */}
      <div className="navbar">
        <i id="menu-icon" className="bx bx-menu" onClick={toggleMenu}></i>
        <div className="navbar-title">KICKSHOPPING</div>
        <div className="right-icons">
          <a href="/carrito">
            <i className="bx bx-cart"></i>
          </a>
          <a href="/usuario">
            <i className="bx bx-user"></i>
          </a>
          <a href="/">
            <i className="bx bx-home"></i>
          </a>
        </div>
      </div>

      {/* Menú desplegable */}
      <ul className={`dropdown ${menuOpen ? "show" : ""}`} id="menu">
        <li><a href="#">Ofertas</a></li>
        <li><a href="#">Todo</a></li>
        <details>
          <summary>Hombre ‣</summary>
          <ol>
            <li><a href="#">Calzones</a></li>
            <li><a href="#">Gorras</a></li>
            <li><a href="#">Camperas</a></li>
            <li><a href="#">Buzos</a></li>
            <li><a href="#">Pantalones</a></li>
            <li><a href="#">Remeras</a></li>
            <li><a href="#">Camisas</a></li>
            <li><a href="#">Zapatillas</a></li>
          </ol>
        </details>
        <details>
          <summary>Mujer ‣</summary>
          <ol>
            <li><a href="#">Vestidos</a></li>
            <li><a href="#">Blusas</a></li>
            <li><a href="#">Faldas</a></li>
            <li><a href="#">Pantalones</a></li>
            <li><a href="#">Remeras</a></li>
            <li><a href="#">Zapatillas</a></li>
            <li><a href="#">Bolsos</a></li>
            <li><a href="#">Accesorios</a></li>
          </ol>
        </details>
      </ul>

      {/* Vista de Producto */}
      <main className={style["vista-producto"]}>
        {loading && <div>Cargando producto...</div>}
        {error && <div style={{color: '#ff5555'}}>{error}</div>}
        {!loading && !error && product && (
          <div className={style["producto-detalle"]}>
            {/* Imagen del producto */}
            <div className={style["producto-imagen"]}>
              <img src={product.image_url || "/buzo.jpeg"} alt={product.name} />
              {product.discount > 0 && (
                <span className={style.descuento}>{product.discount}% OFF</span>
              )}
            </div>
            {/* Información del producto */}
            <div className={style["producto-info"]}>
              <h1>{product.name}</h1>
              <p className={style["precio-anterior"]}>{product.price && product.discount ? `$${(product.price / (1 - product.discount / 100)).toFixed(2)}` : ''}</p>
              <p className={style.precio}>${product.price}</p>
              <p className={style.transferencia}>{product.description}</p>
              <div className={style.acciones}>
                <button className={style["btn-comprar"]}>COMPRAR</button>
                <button className={style["btn-carrito"]}><i className="bx bx-cart"></i> Agregar al carrito</button>
              </div>
            </div>
          </div>
        )}
        {!loading && !error && !product && <div>No se encontró el producto.</div>}
      </main>
    </div>
  );
}