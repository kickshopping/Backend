"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState } from "react";
import style from "./login.module.css"; // Importa los estilos específicos de esta página

export default function Home() {
    const [menuOpen, setMenuOpen] = useState(false);
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [loading, setLoading] = useState(false);

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
            const res = await fetch("http://localhost:8000/auth/login", {
                method: "POST",
                headers: { "Content-Type": "application/x-www-form-urlencoded" },
                body: new URLSearchParams({
                    username: email,
                    password: password
                })
            });
            const data = await res.json();
            if (res.ok && data.access_token) {
                localStorage.setItem("token", data.access_token);
                window.location.href = "/usuario";
            } else {
                setError(data.detail || "Error de autenticación");
            }
        } catch (err) {
            setError("Error de red");
        }
        setLoading(false);
    };

    return (
        <div>
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

                <main>
                    <div className={style["login-container"]}>
                        <h2 className={style["login-title"]}>Login</h2>
                        <form onSubmit={handleSubmit}>
                            <div className={style["input-box"]}>
                                <input
                                    type="email"
                                    placeholder="Email de Gmail"
                                    required
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                />
                                <i className="bx bx-envelope"></i>
                            </div>
                            <div className={style["input-box"]}>
                                <input
                                    type="password"
                                    placeholder="Password"
                                    required
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                />
                                <i className="bx bx-lock-alt"></i>
                            </div>
                            <div className={style.options}>
                                <label>
                                    <input type="checkbox" /> Remember Me
                                </label>
                                <a href="#">Forgot Password?</a>
                            </div>
                            {error && <div style={{ color: "#ff5555", marginBottom: 8 }}>{error}</div>}
                            <button type="submit" className={style["btn"]} disabled={loading}>
                                {loading ? "Cargando..." : "Login"}
                            </button>
                            <p className="register-text">Don't have an account? <a href="/register">Register</a></p>
                        </form>
                    </div>
                </main>
            </div>
        </div>
    );
}