const registerForm = document.getElementById("registerForm");
const alertBox = document.getElementById("alert");
const alertMessage = document.getElementById("alertMessage");
const submitBtn = document.getElementById("submitBtn");
const btnText = document.getElementById("btnText");
const btnSpinner = document.getElementById("btnSpinner");

registerForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const first_name = document.getElementById("first_name").value;
    const last_name = document.getElementById("last_name").value;
    const phone = document.getElementById("phone").value;
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    alertBox.classList.add("d-none");
    submitBtn.disabled = true;
    btnText.classList.add("d-none");
    btnSpinner.classList.remove("d-none");

    try {
        const response = await fetch("http://127.0.0.1:8000/usuarios", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                user_in: { email, password, id_role: 2 }, // 2 = cliente
                profile_in: { first_name, last_name, phone }
            })
        });

        const data = await response.json();

        if (!response.ok) throw new Error(data.detail || "Error al registrar");

        // Guardamos la info mínima del usuario en localStorage para simular login
        localStorage.setItem("user", JSON.stringify({
            id_user: data.id_user,
            email: data.email,
            first_name,
            last_name
        }));

        alertBox.classList.remove("alert-danger");
        alertBox.classList.add("alert-success");
        alertMessage.innerHTML = '<i class="fas fa-check-circle me-2"></i>¡Registro exitoso! Redirigiendo...';
        alertBox.classList.remove("d-none");

        setTimeout(() => {
            // Redirige al perfil del cliente
            window.location.href = "../pages/client/profile.html";
        }, 1000);

    } catch (error) {
        submitBtn.disabled = false;
        btnText.classList.remove("d-none");
        btnSpinner.classList.add("d-none");

        alertBox.classList.remove("alert-success");
        alertBox.classList.add("alert-danger");
        alertMessage.innerHTML = `<i class="fas fa-exclamation-circle me-2"></i>${error.message}`;
        alertBox.classList.remove("d-none");
    }
});