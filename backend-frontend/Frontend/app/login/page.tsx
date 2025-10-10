"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState } from "react";
import style from "./login.module.css"; // Importa los estilos específicos de esta página

export default function Home() {
    const [menuOpen, setMenuOpen] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);
    const [rememberMe, setRememberMe] = useState(false);

    // Alterna abrir/cerrar menú
    const toggleMenu = () => setMenuOpen(!menuOpen);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        setError("");
        // Solo permitir emails de Gmail
        if (!email.endsWith("@gmail.com")) {
            setError("Solo se permiten cuentas de Gmail");
            setLoading(false);
            return;
        }
        try {
            const res = await fetch("http://localhost:8000/usuarios/login", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: email,
                    password: password
                })
            });
            const data = await res.json();
            if (res.ok && data.access_token && data.user_id) {
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("user_id", data.user_id);
                // Guardar el tipo de usuario si viene en la respuesta
                if (data.user_type) {
                    localStorage.setItem("user_type", data.user_type);
                }
                window.location.href = "/";
            } else {
                setError(data.detail || "Usuario o contraseña incorrectos");
            }
        } catch (err) {
            setError("Error de conexión");
        }
        setLoading(false);
    };

    return (
        <div>
            <div>
                {/* Barra de navegación */}
                <div className="navbar">
                    <i id="menu-icon" className="bx bx-menu" onClick={toggleMenu}></i>
                    <div className="navbar-title" style={{cursor:'pointer'}} onClick={()=>window.location.href='/'}>KICKSHOPPING</div>
                    <div className="right-icons">
                        <a href="/usuario">
                            <i className="bx bx-user"></i>
                        </a>
                        <a href="/">
                            <i className="bx bx-home"></i>
                        </a>
                    </div>
                </div>

                <main>
                    <div className={style["login-container"]}>
                        <h2 className={style["login-title"]}>Login</h2>
                        <form onSubmit={handleSubmit}>
                            {/* ...existing code... */}
                            <div className={style["input-box"]} style={{position:'relative'}}>
                                <input
                                    type="email"
                                    placeholder="Correo electrónico"
                                    required
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                />
                                <span style={{position:'absolute',right:10,top:'50%',transform:'translateY(-50%)',color:'#aaa'}}>
                                    <i className="bx bx-envelope"></i>
                                </span>
                            </div>
                            <div className={style["input-box"]} style={{position:'relative'}}>
                                <input
                                    type={showPassword ? "text" : "password"}
                                    placeholder="Contraseña"
                                    required
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                />
                                <span
                                    style={{position:'absolute',right:10,top:'50%',transform:'translateY(-50%)',cursor:'pointer',color:'#aaa'}}
                                    onClick={()=>setShowPassword(v=>!v)}
                                    title={showPassword?"Ocultar contraseña":"Mostrar contraseña"}
                                >
                                    <i className={showPassword?"bx bx-show":"bx bx-hide"}></i>
                                </span>
                            </div>
                            <div style={{ width: '100%' }}>
                                <button type="button" className={style.btn} style={{width:'100%',marginTop:12,padding:'6px 18px',background:'#444',color:'#fff'}}>
                                    ¿Olvidaste tu contraseña?
                                </button>
                                <div style={{ display: 'flex', alignItems: 'center', marginTop: 12 }}>
                                    <input type="checkbox" id="remember" checked={rememberMe} onChange={() => setRememberMe(!rememberMe)} />
                                    <label htmlFor="remember" style={{ marginLeft: 8 }}>Guardar contraseña</label>
                                </div>
                            </div>
                            {error && <div style={{ color: "#ff5555", marginBottom: 8 }}>{error}</div>}
                            <button type="submit" className={style["btn"]} disabled={loading}>
                          {loading ? "Cargando..." : "Iniciar sesión"}
                            </button>
                            <p className="register-text" style={{marginTop: '18px'}}>¿No tienes una cuenta? <a href="/register" style={{color:'#2196f3',textDecoration:'underline'}}>Regístrate</a></p>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}