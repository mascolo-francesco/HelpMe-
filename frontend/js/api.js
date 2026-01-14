/**
 * HelpMe! API Client
 * Handles all communication with the Flask backend
 */

const API_BASE = '/api/v1';

class HelpMeAPI {
    constructor() {
        this.baseUrl = API_BASE;
    }

    async request(endpoint, options = {}) {
        const url = `${this.baseUrl}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include',  // Include cookies for session
            ...options
        };

        if (options.body && typeof options.body === 'object') {
            config.body = JSON.stringify(options.body);
        }

        try {
            const response = await fetch(url, config);
            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.error || 'Si è verificato un errore');
            }

            return data;
        } catch (error) {
            if (error.message === 'Failed to fetch') {
                throw new Error('Impossibile connettersi al server');
            }
            throw error;
        }
    }

    // ========================
    // Auth
    // ========================

    async login(email, password) {
        return this.request('/auth/login', {
            method: 'POST',
            body: { email, password }
        });
    }

    async register(data) {
        return this.request('/auth/register', {
            method: 'POST',
            body: data
        });
    }

    async logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    }

    async getSession() {
        return this.request('/auth/session');
    }

    // ========================
    // Users
    // ========================

    async getProfile() {
        return this.request('/users/me');
    }

    async updateProfile(data) {
        return this.request('/users/me', {
            method: 'PUT',
            body: data
        });
    }

    async getUser(userId) {
        return this.request(`/users/${userId}`);
    }

    async getExperts(categoryId = null) {
        const query = categoryId ? `?category=${categoryId}` : '';
        return this.request(`/users/experts${query}`);
    }

    // ========================
    // Posts
    // ========================

    async getPosts(params = {}) {
        const query = new URLSearchParams(params).toString();
        return this.request(`/posts${query ? '?' + query : ''}`);
    }

    async getPost(postId) {
        return this.request(`/posts/${postId}`);
    }

    async createPost(data) {
        return this.request('/posts', {
            method: 'POST',
            body: data
        });
    }

    async updatePost(postId, data) {
        return this.request(`/posts/${postId}`, {
            method: 'PUT',
            body: data
        });
    }

    async deletePost(postId) {
        return this.request(`/posts/${postId}`, {
            method: 'DELETE'
        });
    }

    async closePost(postId, data) {
        return this.request(`/posts/${postId}/close`, {
            method: 'POST',
            body: data
        });
    }

    async getMyPosts() {
        return this.request('/posts/my');
    }

    // ========================
    // Comments
    // ========================

    async getComments(postId) {
        return this.request(`/comments/post/${postId}`);
    }

    async createComment(postId, data) {
        return this.request(`/comments/post/${postId}`, {
            method: 'POST',
            body: data
        });
    }

    async deleteComment(commentId) {
        return this.request(`/comments/${commentId}`, {
            method: 'DELETE'
        });
    }

    // ========================
    // Votes
    // ========================

    async voteComment(commentId, value) {
        return this.request(`/votes/comment/${commentId}`, {
            method: 'POST',
            body: { value }
        });
    }

    // ========================
    // Categories
    // ========================

    async getCategories() {
        return this.request('/categories');
    }

    async getCategory(categoryId) {
        return this.request(`/categories/${categoryId}`);
    }

    async createCategory(data) {
        return this.request('/categories', {
            method: 'POST',
            body: data
        });
    }

    async updateCategory(categoryId, data) {
        return this.request(`/categories/${categoryId}`, {
            method: 'PUT',
            body: data
        });
    }

    async deleteCategory(categoryId) {
        return this.request(`/categories/${categoryId}`, {
            method: 'DELETE'
        });
    }

    async subscribeCategory(categoryId) {
        return this.request(`/categories/${categoryId}/subscribe`, {
            method: 'POST'
        });
    }

    async unsubscribeCategory(categoryId) {
        return this.request(`/categories/${categoryId}/unsubscribe`, {
            method: 'POST'
        });
    }

    async getMySubscriptions() {
        return this.request('/categories/my-subscriptions');
    }

    // ========================
    // Notifications
    // ========================

    async getNotifications() {
        return this.request('/notifications');
    }

    async markNotificationRead(notificationId) {
        return this.request(`/notifications/${notificationId}/read`, {
            method: 'POST'
        });
    }

    async markAllNotificationsRead() {
        return this.request('/notifications/read-all', {
            method: 'POST'
        });
    }

    // ========================
    // Admin
    // ========================

    async getAdminUsers() {
        return this.request('/admin/users');
    }

    async banUser(userId, reason = '') {
        return this.request(`/admin/users/${userId}/ban`, {
            method: 'POST',
            body: { reason }
        });
    }

    async unbanUser(userId) {
        return this.request(`/admin/users/${userId}/unban`, {
            method: 'POST'
        });
    }

    async moderatePost(postId) {
        return this.request(`/admin/posts/${postId}/moderate`, {
            method: 'POST'
        });
    }

    async moderateComment(commentId) {
        return this.request(`/admin/comments/${commentId}/moderate`, {
            method: 'POST'
        });
    }

    async getAdminStats() {
        return this.request('/admin/stats');
    }
}

// Create global API instance
const api = new HelpMeAPI();
