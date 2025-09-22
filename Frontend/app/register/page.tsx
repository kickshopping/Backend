
"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState } from "react";
import styles from "./register.module.css";


export default function Home() {
    const [menuOpen, setMenuOpen] = useState(false);
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [birthdate, setBirthdate] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);

    // Alterna abrir/cerrar menú
    const toggleMenu = () => setMenuOpen(!menuOpen);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        setLoading(true);
        // Solo permitir emails de Gmail
        if (!email.endsWith("@gmail.com")) {
            setError("Solo se permiten cuentas de Gmail");
            setLoading(false);
            return;
        }
        try {
            const res = await fetch("http://localhost:8000/auth/register", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: email, // username igual al email
                    email,
                    password,
                    birthdate
                })
            });
            const data = await res.json();
            if (res.ok && data.id) {
                setSuccess("¡Registro exitoso! Ahora puedes iniciar sesión.");
                setUsername(""); setEmail(""); setPassword(""); setBirthdate("");
            } else {
                setError(data.detail || "Error en el registro");
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
                    <div className="navbar-title">KICKSHOPPING</div>
                    <div className="right-icons">
                        <a href="/">
                            <i className="bx bx-home"></i>
                        </a>
                    </div>
                </div>

                <main>
                    <div className={styles["login-container"]}>
                        <h2 className={styles["login-title"]}>Registro</h2>
                        <form onSubmit={handleSubmit}>
                            {/* Username oculto, se usará el email como username */}
                            <div className={styles["input-box"]}>
                                <input
                                    type="email"
                                    placeholder="Email"
                                    required
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                />
                                <i className="bx bx-envelope"></i>
                            </div>
                            <div className={styles["input-box"]}>
                                <input
                                    type="password"
                                    placeholder="Password"
                                    required
                                    value={password}
                                    onChange={e => setPassword(e.target.value)}
                                />
                                <i className="bx bx-lock-alt"></i>
                            </div>
                            <div className={styles["input-box"]}>
                                <input
                                    type="date"
                                    id="fecha_nacimiento"
                                    placeholder="Date"
                                    required
                                    value={birthdate}
                                    onChange={e => setBirthdate(e.target.value)}
                                />
                                <i className='bx bx-calendar'></i>
                            </div>
                            {error && <div style={{ color: "#ff5555", marginBottom: 8 }}>{error}</div>}
                            {success && <div style={{ color: "#4caf50", marginBottom: 8 }}>{success}</div>}
                            <button type="submit" className={styles.btn} disabled={loading}>
                                {loading ? "Cargando..." : "Registrarse"}
                            </button>
                            <p className={styles["register-text"]}>¿Ya tienes cuenta? <a href="/login">Inicia sesión</a></p>
                        </form>
                    </div>
                      {/* Usa CSS Modules o globales para los estilos. */}
                </main>
            </div>
        </div>
    );
}
