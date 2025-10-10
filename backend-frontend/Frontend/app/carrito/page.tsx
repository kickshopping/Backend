"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState, useEffect } from "react";
import style from "./cart.module.css"; // Importa los estilos específicos de esta página


export default function Home() {
  const [menuOpen, setMenuOpen] = useState(false);
  const [cart, setCart] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  // Obtener userId real del token
  let userId = 1;
  if (typeof window !== "undefined") {
    const token = localStorage.getItem("token");
    if (token) {
      try {
        const payload = JSON.parse(atob(token.split('.')[1]));
        if (payload && payload.user_id) userId = payload.user_id;
      } catch {}
    }
  }

  // Alterna abrir/cerrar menú
  const toggleMenu = () => setMenuOpen(!menuOpen);

  // Refetch carrito cada vez que la página gana foco (por ejemplo, tras redirección)
  useEffect(() => {
    const fetchCart = async () => {
      try {
        const res = await fetch(`http://localhost:8000/cart_items/user/${userId}`);
        const data = await res.json();
        console.log('Respuesta del backend (carrito):', data);
        setCart(Array.isArray(data) ? data : []);
      } catch (err) {
        setError("No se pudo cargar el carrito");
      }
      setLoading(false);
    };
    fetchCart();
    // Refetch cuando la página gana foco
    const handleVisibility = () => {
      if (document.visibilityState === "visible") {
        setLoading(true);
        fetchCart();
      }
    };
    document.addEventListener("visibilitychange", handleVisibility);
    return () => {
      document.removeEventListener("visibilitychange", handleVisibility);
    };
  }, []);

  const total = Array.isArray(cart) ? cart.reduce((acc, item) => acc + (item.product?.price || 0) * item.quantity, 0) : 0;

  return (
    <div>
      {/* Barra de navegación */}
      <div className="navbar">
        <i id="menu-icon" className="bx bx-menu" onClick={toggleMenu}></i>
        <div className="navbar-title">KICKSHOPPING</div>
        <div className="right-icons">
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

      {/* Productos */}
      <main>
        <div className={style.container}>
          <h2>Carrito de Compras</h2>
          {loading && <div>Cargando carrito...</div>}
          {error && <div style={{color: '#ff5555'}}>{error}</div>}
          {!loading && !error && cart.length === 0 && <div>No hay productos en el carrito.</div>}
          {!loading && !error && cart.length > 0 && (
            <>
              {cart.map(item => (
                <div key={item.id} className={style["carrito-item"]}>
                  <img src={item.product?.image_url || "/buzo.jpeg"} alt={item.product?.name || "Producto"} />
                  <div className={style.info}>
                    <div>{item.product?.name || "Producto"}</div>
                    <div>Cantidad: {item.quantity}</div>
                    <div>Precio: ${item.product?.price ?? "-"}</div>
                  </div>
                  <button
                    style={{marginLeft: 16, background: '#ff5555', color: 'white', border: 'none', borderRadius: 4, padding: '6px 12px', cursor: 'pointer'}}
                    onClick={async () => {
                      // Eliminar del backend (debería ser /cart_items/{id})
                      try {
                        const res = await fetch(`http://localhost:8000/cart_items/${item.id}`, { method: "DELETE" });
                        if (res.ok) {
                          setCart(cart.filter(ci => ci.id !== item.id));
                        } else {
                          alert("No se pudo eliminar el producto del carrito");
                        }
                      } catch (e) {
                        alert("Error de red al eliminar del carrito");
                      }
                    }}
                  >Eliminar</button>
                </div>
              ))}
            </>
          )}
          <div className={style.total} id="carrito-total">Total: ${total.toFixed(2)}</div>
          <button className={style["btn-comprar"]}>Realizar compra</button>
        </div>
      </main>
    </div>
  );
}
