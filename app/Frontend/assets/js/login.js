// app/Frontend/js/login.js
document.getElementById("loginForm").addEventListener("submit", async (event) => {
    event.preventDefault();
    
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;
    const alertBox = document.getElementById("alert");
    
    // Ocultar alerta previa
    alertBox.classList.add("d-none");
    
    try {
        const response = await fetch("http://127.0.0.1:8000/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
            body: new URLSearchParams({
                username: email,
                password: password
            }),
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.detail || "Credenciales inválidas");
        }

        const data = await response.json();
        
        // Guardar en memoria (temporal para esta sesión)
        sessionStorage.setItem("token", data.access_token);
        sessionStorage.setItem("usuario", data.usuario);
        
        // Redirigir al dashboard
        window.location.href = "dashboard.html";
        
    } catch (error) {
        alertBox.textContent = error.message;
        alertBox.classList.remove("d-none");
        console.error("Error de login:", error);
    }
});