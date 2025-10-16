const apiUrl = "http://127.0.0.1:8000/services";
const bulkUploadUrl = "http://127.0.0.1:8000/services/bulk-upload";

const serviceForm = document.getElementById("serviceForm");
const servicesTable = document.getElementById("servicesTable");
const alertBox = document.getElementById("alertBox");
const formTitle = document.getElementById("formTitle");
const submitBtn = document.getElementById("submitBtn");
const cancelBtn = document.getElementById("cancelBtn");
const serviceIdInput = document.getElementById("serviceId");

const excelFile = document.getElementById("excelFile");
const uploadBtn = document.getElementById("uploadBtn");
const fileName = document.getElementById("fileName");
const downloadTemplate = document.getElementById("downloadTemplate");

// Mostrar alerta
function showAlert(message, type = "success") {
    alertBox.className = `alert alert-modern alert-${type}`;
    alertBox.innerHTML = `<i class="fas fa-${type === 'success' ? 'check-circle' : type === 'danger' ? 'exclamation-circle' : 'info-circle'} me-2"></i>${message}`;
    alertBox.classList.remove("d-none");
    setTimeout(() => alertBox.classList.add("d-none"), 5000);
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Manejar selección de archivo
excelFile.addEventListener("change", (e) => {
    if (e.target.files.length > 0) {
        const file = e.target.files[0];
        fileName.innerHTML = `<i class="fas fa-file-excel me-2"></i>Archivo seleccionado: <strong>${file.name}</strong>`;
        uploadBtn.disabled = false;
    } else {
        fileName.textContent = "";
        uploadBtn.disabled = true;
    }
});


// ==========================
// Carga Masiva de Servicios
// ==========================

// Esta sección permite subir un archivo Excel (.xls o .xlsx) con múltiples servicios de manera simultánea.
// La lógica de funcionamiento es la siguiente:

// 1. El usuario selecciona un archivo Excel que contenga las columnas obligatorias: 
//    name, description, duration_minutes, price.
// 2. Se habilita el botón "Cargar Servicios" una vez seleccionado el archivo.
// 3. Al hacer clic en el botón, se envía el archivo al endpoint FastAPI /services/bulk-upload mediante un POST.
// 4. La barra de progreso muestra el avance de la subida del archivo al servidor.
// 5. El backend valida el contenido, crea los servicios válidos y devuelve un resumen:
//    - Número de servicios creados
//    - Lista de servicios
//    - Errores en filas que no cumplieron los requisitos
// 6. Se muestra una alerta con el resultado de la carga y se actualiza la tabla de servicios en la interfaz.


uploadBtn.addEventListener("click", () => {
    // Obtener el primer archivo seleccionado del input (si hay)
    const file = excelFile.files[0];
    if (!file) return;

    // Crear un objeto FormData para enviar el archivo como multipart/form-data
    const formData = new FormData();
    // Añadir el archivo al FormData con la clave "file" (mismo nombre que espera el backend)
    formData.append("file", file);


    uploadBtn.disabled = true;
    // spiner subida
    uploadBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i> Subiendo...';
    
    
    // Obtener el contenedor de la barra de progreso del DOM
    const progressContainer = document.getElementById("progressContainer");
    const progressBar = document.getElementById("uploadProgress");
    progressContainer.style.display = "block";
    progressBar.style.width = "0%";
    progressBar.innerText = "0%";

    // Crear una instancia de XMLHttpRequest para enviar el FormData
    const xhr = new XMLHttpRequest();
    xhr.open("POST", bulkUploadUrl, true);

    // ---------- Progreso de subida: evento que se dispara mientras se suben bytes ----------
    xhr.upload.onprogress = (event) => {
        if (event.lengthComputable) {
            //(bytes enviados / total bytes) * 100
            const percent = Math.round((event.loaded / event.total) * 100);
            progressBar.style.width = percent + "%";
            progressBar.innerText = percent + "%";
        }
    };

    // ---------- Cuando la petición HTTP finaliza (llega respuesta del servidor) ----------
    xhr.onload = async () => {
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Cargar Servicios';
        
        progressBar.classList.remove("progress-bar-animated");
      
        progressBar.style.width = "100%";
      
        progressBar.innerText = "100%";

      
        if (xhr.status >= 200 && xhr.status < 300) {
            const data = JSON.parse(xhr.responseText);
            let message = `✅ ${data.data.servicios_creados} servicio(s) cargado(s) exitosamente`;
            if (data.data.errores && data.data.errores.length > 0) {
                message += `<br><small class="text-warning">⚠️ ${data.data.errores.length} fila(s) con errores</small>`;
            }
            showAlert(message, "success");
            excelFile.value = "";
            fileName.textContent = "";
            loadServices();
        } else {
            try {
                const errData = JSON.parse(xhr.responseText);
                showAlert(`❌ Error: ${errData.detail || "No se pudo cargar el archivo"}`, "danger");
            } catch { 
                showAlert("❌ Error desconocido al cargar el archivo", "danger");
            }
        }

    
        setTimeout(() => {
            progressContainer.style.display = "none";
            progressBar.classList.add("progress-bar-animated");
        }, 2000);
    };

    // ---------- Error de red / conexión (no recibe respuesta del servidor) ----------
    xhr.onerror = () => {
        
        showAlert("❌ Error de conexión al servidor", "danger");
        uploadBtn.disabled = false;
        uploadBtn.innerHTML = '<i class="fas fa-upload me-2"></i>Cargar Servicios';
        progressContainer.style.display = "none";
    };

    // Enviar realmente el FormData (comienza la subida y disparará onprogress)
    xhr.send(formData);
});

// Descargar plantilla
downloadTemplate.addEventListener("click", (e) => {
    e.preventDefault();
    const csvContent = "name,description,duration_minutes,price\nCorte de Cabello,Corte de cabello profesional,30,25000\nMaquillaje,Maquillaje completo para eventos,60,80000\nManicure,Cuidado completo de uñas,45,35000";
    const blob = new Blob([csvContent], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'plantilla_servicios.csv';
    a.click();
    window.URL.revokeObjectURL(url);
});

// Cargar servicios
async function loadServices() {
    try {
        const response = await fetch(apiUrl);
        const result = await response.json();
        const services = result.data || [];  // ← Aquí está el cambio
        servicesTable.innerHTML = "";

        services.forEach(svc => {
            const row = `
                <tr>
                    <td><strong>#${svc.id_service}</strong></td>
                    <td><strong>${svc.name}</strong></td>
                    <td>${svc.description || ''}</td>
                    <td><span class="badge-duration"><i class="fas fa-clock me-1"></i>${svc.duration_minutes} min</span></td>
                    <td><span class="badge-price">$${Number(svc.price).toLocaleString()}</span></td>
                    <td class="text-center">
                        <button class="btn btn-warning btn-action me-2" onclick="editService(${svc.id_service})">
                            <i class="fas fa-edit"></i> Editar
                        </button>
                        <button class="btn btn-danger btn-action" onclick="deleteService(${svc.id_service})">
                            <i class="fas fa-trash"></i> Eliminar
                        </button>
                    </td>
                </tr>
            `;
            servicesTable.insertAdjacentHTML("beforeend", row);
        });
    } catch (error) {
        showAlert("Error al cargar servicios", "danger");
    }
}

// Crear o actualizar servicio
serviceForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const serviceData = {
        name: document.getElementById("name").value,
        description: document.getElementById("description").value,
        duration_minutes: parseInt(document.getElementById("duration").value),
        price: parseFloat(document.getElementById("price").value)
    };

    const id = serviceIdInput.value;
    const method = id ? "PUT" : "POST";
    const url = id ? `${apiUrl}/${id}` : apiUrl;

    try {
        const response = await fetch(url, {
            method,
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(serviceData)
        });

        if (response.ok) {
            showAlert(id ? "✅ Servicio actualizado correctamente" : "✅ Servicio creado correctamente");
            serviceForm.reset();
            serviceIdInput.value = "";
            formTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Agregar Nuevo Servicio';
            submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Guardar';
            loadServices();
        } else {
            const data = await response.json();
            showAlert(data.detail || "Error en la operación", "danger");
        }
    } catch (error) {
        showAlert("Error de conexión", "danger");
    }
});

// Editar servicio
async function editService(id) {
    try {
        const response = await fetch(`${apiUrl}/${id}`);
        //const svc = await response.json();
        const svc = (await response.json()).data;
        
        serviceIdInput.value = svc.id_service;
        document.getElementById("name").value = svc.name;
        document.getElementById("description").value = svc.description;
        document.getElementById("duration").value = svc.duration_minutes;
        document.getElementById("price").value = svc.price;
        
        formTitle.innerHTML = '<i class="fas fa-edit"></i> Editar Servicio';
        submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Actualizar';
        
        window.scrollTo({ top: 0, behavior: 'smooth' });
    } catch (error) {
        showAlert("Error al cargar servicio", "danger");
    }
}

// Eliminar servicio
async function deleteService(id) {
    if (!confirm("¿Estás seguro de eliminar este servicio?")) return;

    try {
        const response = await fetch(`${apiUrl}/${id}`, { method: "DELETE" });
        if (response.ok) {
            showAlert("🗑️ Servicio eliminado correctamente");
            loadServices();
        } else {
            const data = await response.json();
            showAlert(data.detail || "Error al eliminar", "danger");
        }
    } catch (error) {
        showAlert("Error de conexión", "danger");
    }
}

// Cancelar edición
cancelBtn.addEventListener("click", () => {
    serviceForm.reset();
    serviceIdInput.value = "";
    formTitle.innerHTML = '<i class="fas fa-plus-circle"></i> Agregar Nuevo Servicio';
    submitBtn.innerHTML = '<i class="fas fa-save me-2"></i>Guardar';
});

// Inicializar
loadServices();

document.getElementById("backBtn").addEventListener("click", () => {
    window.location.href = "../dashboard.html"; // Ajusta la ruta según tu estructura
});