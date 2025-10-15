// app/Frontend/js/login.js
document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("alert");
    
    // Ocultar alerta previa
    alertBox.classList.add("d-none");
    
    try {
        const response = await fetch("http://127.0.0.1:8000/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                email: email,
                password: password
            }),
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Credenciales inválidas");
        }

        // Guardar en memoria (temporal para esta sesión)
        localStorage.setItem("usuario", JSON.stringify(data.usuario));
        localStorage.setItem("token", data.access_token);
        // Redirigir según tipo
        const usuario = data.usuario;
        if (usuario.tipo === "cliente") {
            window.location.href = "/pages/cliente/profile.html";
        } else if (usuario.tipo === "empleado" || usuario.tipo === "admin") {
            window.location.href = "/pages/empleado/dashboard.html";
        }
        
    } catch (error) {
        alertBox.textContent = error.message;
        alertBox.classList.remove("d-none");
        console.error("Error de login:", error);
    }
});