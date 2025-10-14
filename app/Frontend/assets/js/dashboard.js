// app/Frontend/assets/js/dashboard.js

// la logica de este doc falta por ser revisada.
// Verificar autenticación al cargar
document.addEventListener('DOMContentLoaded', () => {
    if (!checkAuth()) {
        return;
    }

    loadUserData();
    loadStats();
    loadRecentActivity();
});

/**
 * Cargar datos del usuario
 */
function loadUserData() {
    const userData = getUserData();
    document.getElementById('userName').textContent = userData.nombre;
    document.getElementById('userNameWelcome').textContent = userData.nombre;
}

/**
 * Cargar estadísticas del dashboard
 */
async function loadStats() {
    try {
        // Obtener reservas
        const reservas = await ReservasAPI.getAll();
        const today = new Date().toISOString().split('T')[0];
        
        const todayReservations = reservas.filter(r => 
            r.fecha_hora.startsWith(today)
        ).length;
        
        const pendingReservations = reservas.filter(r => 
            r.estado === 'pendiente'
        ).length;

        // Obtener clientes
        const usuarios = await UsuariosAPI.getAll();
        const clientes = usuarios.filter(u => u.rol === 'cliente').length;

        // Obtener servicios
        const servicios = await ServiciosAPI.getAll();

        // Actualizar UI
        document.getElementById('todayReservations').textContent = todayReservations;
        document.getElementById('pendingReservations').textContent = pendingReservations;
        document.getElementById('totalClients').textContent = clientes;
        document.getElementById('totalServices').textContent = servicios.length;

    } catch (error) {
        console.error('Error al cargar estadísticas:', error);
        // Mostrar valores por defecto en caso de error
        document.getElementById('todayReservations').textContent = '-';
        document.getElementById('pendingReservations').textContent = '-';
        document.getElementById('totalClients').textContent = '-';
        document.getElementById('totalServices').textContent = '-';
    }
}

/**
 * Cargar actividad reciente
 */
async function loadRecentActivity() {
    const activityList = document.getElementById('activityList');
    
    try {
        const reservas = await ReservasAPI.getAll();
        
        // Tomar las últimas 5 reservas
        const recentReservas = reservas
            .sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
            .slice(0, 5);

        if (recentReservas.length === 0) {
            activityList.innerHTML = `
                <div class="alert alert-info">
                    <i class="fas fa-info-circle me-2"></i>
                    No hay actividad reciente
                </div>
            `;
            return;
        }

        activityList.innerHTML = recentReservas.map(reserva => {
            const icon = getActivityIcon(reserva.estado);
            const color = getActivityColor(reserva.estado);
            const timeAgo = getTimeAgo(reserva.created_at);

            return `
                <div class="d-flex align-items-center mb-3 pb-3 border-bottom">
                    <div class="me-3">
                        <i class="fas fa-${icon} text-${color}" style="font-size: 1.5rem;"></i>
                    </div>
                    <div class="flex-grow-1">
                        <div class="fw-semibold">Reserva ${reserva.estado}</div>
                        <small class="text-muted">${timeAgo}</small>
                    </div>
                </div>
            `;
        }).join('');

    } catch (error) {
        console.error('Error al cargar actividad:', error);
        activityList.innerHTML = `
            <div class="alert alert-warning">
                <i class="fas fa-exclamation-triangle me-2"></i>
                No se pudo cargar la actividad reciente
            </div>
        `;
    }
}

/**
 * Obtener icono según estado
 */
function getActivityIcon(estado) {
    const icons = {
        'confirmada': 'check-circle',
        'pendiente': 'clock',
        'cancelada': 'times-circle',
        'completada': 'check-double'
    };
    return icons[estado] || 'calendar';
}

/**
 * Obtener color según estado
 */
function getActivityColor(estado) {
    const colors = {
        'confirmada': 'success',
        'pendiente': 'warning',
        'cancelada': 'danger',
        'completada': 'primary'
    };
    return colors[estado] || 'secondary';
}

/**
 * Calcular tiempo transcurrido
 */
function getTimeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    if (seconds < 60) return 'Hace un momento';
    if (seconds < 3600) return `Hace ${Math.floor(seconds / 60)} min`;
    if (seconds < 86400) return `Hace ${Math.floor(seconds / 3600)} horas`;
    return `Hace ${Math.floor(seconds / 86400)} días`;
}

/**
 * Cerrar sesión
 */
function logout() {
    if (confirm('¿Estás seguro de que quieres cerrar sesión?')) {
        AuthAPI.logout();
    }
}