"use client"; // Necesario porque usamos onClick (JS en el cliente)
import { useState } from "react";
import styles from "./register.module.css";


export default function Home() {
    const [menuOpen, setMenuOpen] = useState(false);
    const [username, setUsername] = useState("");
    const [firstName, setFirstName] = useState("");
    const [lastName, setLastName] = useState("");
    const [phone, setPhone] = useState("");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [showPassword, setShowPassword] = useState(false);
    const [birthDay, setBirthDay] = useState("");
    const [birthMonth, setBirthMonth] = useState("");
    const [birthYear, setBirthYear] = useState("");
    const [error, setError] = useState("");
    const [success, setSuccess] = useState("");
    const [loading, setLoading] = useState(false);
    const [userType, setUserType] = useState<string>("");

    // Alterna abrir/cerrar menú
    const toggleMenu = () => setMenuOpen(!menuOpen);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setError("");
        setSuccess("");
        setLoading(true);
        if (!userType) {
            setError("Selecciona si eres vendedor o comprador");
            setLoading(false);
            return;
        }
        // Solo permitir emails de Gmail
        if (!email.endsWith("@gmail.com")) {
            setError("Solo se permiten cuentas de Gmail");
            setLoading(false);
            return;
        }
        try {
            // Construir fecha en formato YYYY-MM-DD
            const birthdate = birthYear && birthMonth && birthDay ? `${birthYear}-${birthMonth.padStart(2, '0')}-${birthDay.padStart(2, '0')}` : "";
            const res = await fetch("http://localhost:8000/usuarios", {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    username: email, // username igual al email
                    email,
                    password,
                    birthdate,
                    first_name: firstName,
                    last_name: lastName,
                    phone: phone,
                    user_type: userType // Enviar el tipo al backend si lo soporta
                })
            });
            const data = await res.json();
            if (res.ok && data.access_token && data.user_id) {
                localStorage.setItem("token", data.access_token);
                localStorage.setItem("user_id", data.user_id);
                localStorage.setItem("user_type", userType);
                window.location.href = "/";
            } else if (res.ok && data.id) {
                setSuccess("¡Registro exitoso! Ahora puedes iniciar sesión.");
                setUsername(""); setEmail(""); setPassword(""); setBirthDay(""); setBirthMonth(""); setBirthYear("");
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
                            {/* ...existing code... */}
                            <div className={styles["input-box"]}>
                                <input
                                    type="text"
                                    placeholder="Nombre"
                                    required
                                    value={firstName}
                                    onChange={e => setFirstName(e.target.value)}
                                />
                            </div>
                            <div className={styles["input-box"]}>
                                <input
                                    type="text"
                                    placeholder="Apellido"
                                    required
                                    value={lastName}
                                    onChange={e => setLastName(e.target.value)}
                                />
                            </div>
                            <div className={styles["input-box"]}>
                                <input
                                    type="email"
                                    placeholder="Correo electrónico"
                                    required
                                    value={email}
                                    onChange={e => setEmail(e.target.value)}
                                />
                            </div>
                            <div className={styles["input-box"]} style={{position:'relative'}}>
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
                            <div style={{ display: 'flex', justifyContent: 'center', gap: '16px', marginBottom: '18px' }}>
                                <button
                                    type="button"
                                    className={userType === "comprador" ? styles.btnSelected : styles.btn}
                                    style={{ padding: '8px 18px', background: userType === "comprador" ? '#2196f3' : '#eee', color: userType === "comprador" ? '#fff' : '#444', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
                                    onClick={() => setUserType("comprador")}
                                >
                                    Registrarse como Comprador
                                </button>
                                <button
                                    type="button"
                                    className={userType === "vendedor" ? styles.btnSelected : styles.btn}
                                    style={{ padding: '8px 18px', background: userType === "vendedor" ? '#2196f3' : '#eee', color: userType === "vendedor" ? '#fff' : '#444', borderRadius: '6px', border: 'none', cursor: 'pointer' }}
                                    onClick={() => setUserType("vendedor")}
                                >
                                    Registrarse como Vendedor
                                </button>
                            </div>
                            <div className={styles["input-box"]}>
                                <label style={{display:'block',marginBottom:4}}>Fecha de nacimiento</label>
                                <div style={{display:'flex',gap:8}}>
                                    <select required value={birthDay} onChange={e => setBirthDay(e.target.value)}>
                                        <option value="">Día</option>
                                        {[...Array(31)].map((_,i)=>(<option key={i+1} value={String(i+1)}>{i+1}</option>))}
                                    </select>
                                    <select required value={birthMonth} onChange={e => setBirthMonth(e.target.value)}>
                                        <option value="">Mes</option>
                                        {[...Array(12)].map((_,i)=>(<option key={i+1} value={String(i+1).padStart(2,'0')}>{String(i+1).padStart(2,'0')}</option>))}
                                    </select>
                                    <select required value={birthYear} onChange={e => setBirthYear(e.target.value)}>
                                        <option value="">Año</option>
                                        {Array.from({length: 100},(_,i)=>2025-i).map(y=>(<option key={y} value={String(y)}>{y}</option>))}
                                    </select>
                                </div>
                                <i className='bx bx-calendar'></i>
                            </div>
                            {error && <div style={{ color: "#ff5555", marginBottom: 8 }}>{error}</div>}
                            {success && <div style={{ color: "#4caf50", marginBottom: 8 }}>{success}</div>}
                            <button type="submit" className={styles.btn} disabled={loading}>
                                {loading ? "Cargando..." : "Registrarse"}
                            </button>
                            <p className={styles["register-text"]} style={{color:'#fff'}}>¿Ya tienes cuenta? <a href="/login" style={{color:'#2196f3',textDecoration:'underline'}}>Inicia sesión</a></p>
                        </form>
                    </div>
                      {/* Usa CSS Modules o globales para los estilos. */}
                </main>
            </div>
        </div>
    );
}
