// app/Frontend/assets/js/api.js

const API_BASE_URL = 'http://127.0.0.1:8000';

/**
 * Configuración base para fetch
 */
const fetchConfig = {
    headers: {
        'Content-Type': 'application/json',
    }
};

/**
 * Obtiene el token de autenticación
 */
function getAuthToken() {
    return sessionStorage.getItem('token');
}

/**
 * Añade el token de autenticación a las cabeceras
 */
function getAuthHeaders() {
    const token = getAuthToken();
    return {
        ...fetchConfig.headers,
        'Authorization': `Bearer ${token}`
    };
}

/**
 * API de Autenticación
 */
const AuthAPI = {
    /**
     * Login de usuario
     */
    async login(email, password) {
        const response = await fetch(`${API_BASE_URL}/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ email, password }),
        });

        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || 'Error en el login');
        }

        return await response.json(); // Devuelve { access_token }
    },

    /**
     * Logout de usuario
     */
    logout() {
        sessionStorage.removeItem('token');
        sessionStorage.removeItem('usuario');
        window.location.href = 'index.html';
    }
};

/**
 * API de Usuarios
 */
const UsuariosAPI = {
    /**
     * Obtener todos los usuarios
     */
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/usuarios`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error('Error al obtener usuarios');
        }

        return await response.json();
    },

    /**
     * Obtener usuario por ID
     */
    async getById(id) {
        const response = await fetch(`${API_BASE_URL}/usuarios/${id}`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error('Error al obtener usuario');
        }

        return await response.json();
    }
};

/**
 * API de Servicios
 */
const ServiciosAPI = {
    /**
     * Obtener todos los servicios
     */
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/servicios`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error('Error al obtener servicios');
        }

        return await response.json();
    },

    /**
     * Crear nuevo servicio
     */
    async create(servicio) {
        const response = await fetch(`${API_BASE_URL}/servicios`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(servicio)
        });

        if (!response.ok) {
            throw new Error('Error al crear servicio');
        }

        return await response.json();
    }
};

/**
 * API de Reservas
 */
const ReservasAPI = {
    /**
     * Obtener todas las reservas
     */
    async getAll() {
        const response = await fetch(`${API_BASE_URL}/reservas`, {
            headers: getAuthHeaders()
        });

        if (!response.ok) {
            throw new Error('Error al obtener reservas');
        }

        return await response.json();
    },

    /**
     * Crear nueva reserva
     */
    async create(reserva) {
        const response = await fetch(`${API_BASE_URL}/reservas`, {
            method: 'POST',
            headers: getAuthHeaders(),
            body: JSON.stringify(reserva)
        });

        if (!response.ok) {
            throw new Error('Error al crear reserva');
        }

        return await response.json();
    },

    /**
     * Actualizar estado de reserva
     */
    async updateStatus(id, estado) {
        const response = await fetch(`${API_BASE_URL}/reservas/${id}/estado`, {
            method: 'PATCH',
            headers: getAuthHeaders(),
            body: JSON.stringify({ estado })
        });

        if (!response.ok) {
            throw new Error('Error al actualizar reserva');
        }

        return await response.json();
    }
};

/**
 * Utilidad para verificar autenticación
 */
function checkAuth() {
    const token = getAuthToken();
    if (!token) {
        window.location.href = 'login.html';
        return false;
    }
    return true;
}

/**
 * Utilidad para obtener datos del usuario
 */
function getUserData() {
    return {
        nombre: sessionStorage.getItem('usuario') || 'Usuario',
        token: getAuthToken()
    };
}