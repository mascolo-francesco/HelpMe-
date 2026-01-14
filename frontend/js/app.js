/**
 * HelpMe! Single Page Application
 * Main application logic and routing
 */

class HelpMeApp {
    constructor() {
        this.user = null;
        this.categories = [];
        this.init();
    }

    async init() {
        // Check session
        await this.checkSession();
        
        // Load categories
        await this.loadCategories();
        
        // Setup event listeners
        this.setupEventListeners();
        
        // Setup routing
        this.setupRouting();
        
        // Handle initial route
        this.handleRoute();
    }

    async checkSession() {
        try {
            const data = await api.getSession();
            if (data.authenticated) {
                this.setUser(data.user);
            }
        } catch (error) {
            console.log('Not authenticated');
        }
    }

    setUser(user) {
        this.user = user;
        document.body.classList.add('authenticated');
        
        if (user.role === 'ADMIN') {
            document.body.classList.add('is-admin');
        }
        
        // Update UI with user information
        const initials = this.getInitials(user.nome);
        document.getElementById('user-initials').textContent = initials;
        document.getElementById('dropdown-user-initials').textContent = initials;
        document.getElementById('user-dropdown-name').textContent = user.nome;
        document.getElementById('user-dropdown-email').textContent = user.email;
        
        // Update role badge
        const roleBadge = document.getElementById('user-dropdown-role');
        const roleText = {
            'ADMIN': 'Amministratore',
            'EXPERT': 'Esperto',
            'USER': 'Utente'
        };
        
        roleBadge.textContent = roleText[user.role] || 'Utente';
        roleBadge.className = 'dropdown-user-badge';
        
        if (user.role === 'ADMIN') {
            roleBadge.classList.add('admin');
        } else if (user.role === 'EXPERT') {
            roleBadge.classList.add('expert');
        }
        
        // Load notifications
        this.loadNotifications();
    }

    clearUser() {
        this.user = null;
        document.body.classList.remove('authenticated', 'is-admin');
    }

    getInitials(name) {
        return name.split(' ').map(n => n[0]).slice(0, 2).join('').toUpperCase();
    }

    async loadCategories() {
        try {
            const data = await api.getCategories();
            this.categories = data.categories || [];
        } catch (error) {
            console.error('Failed to load categories:', error);
        }
    }

    async loadNotifications() {
        if (!this.user) return;
        
        try {
            const data = await api.getNotifications();
            const countEl = document.getElementById('notification-count');
            
            if (data.unread_count > 0) {
                countEl.textContent = data.unread_count;
                countEl.style.display = 'flex';
            } else {
                countEl.style.display = 'none';
            }
            
            this.renderNotifications(data.notifications);
        } catch (error) {
            console.error('Failed to load notifications:', error);
        }
    }

    renderNotifications(notifications) {
        const list = document.getElementById('notifications-list');
        
        if (!notifications || notifications.length === 0) {
            list.innerHTML = '<p class="no-notifications">Nessuna notifica</p>';
            return;
        }
        
        list.innerHTML = notifications.map(n => `
            <div class="notification-item ${n.read_at ? '' : 'unread'}" data-id="${n.id}" data-post="${n.post_id || ''}">
                <div class="notification-text">${n.messaggio}</div>
                <div class="notification-time">${this.formatDate(n.created_at)}</div>
            </div>
        `).join('');
        
        // Add click handlers
        list.querySelectorAll('.notification-item').forEach(item => {
            item.addEventListener('click', async () => {
                const id = item.dataset.id;
                const postId = item.dataset.post;
                
                await api.markNotificationRead(id);
                item.classList.remove('unread');
                
                if (postId) {
                    window.location.hash = `#/post/${postId}`;
                }
                
                document.getElementById('notifications-panel').style.display = 'none';
                this.loadNotifications();
            });
        });
    }

    setupEventListeners() {
        // Login button
        document.getElementById('btn-login').addEventListener('click', () => {
            this.showModal('login-modal');
        });

        // Register button
        document.getElementById('btn-register').addEventListener('click', () => {
            this.showModal('register-modal');
        });

        // Close modals
        document.querySelectorAll('.modal-close, .modal-backdrop').forEach(el => {
            el.addEventListener('click', (e) => {
                if (e.target === el) {
                    this.closeAllModals();
                }
            });
        });

        // Switch between login/register
        document.getElementById('switch-to-register').addEventListener('click', (e) => {
            e.preventDefault();
            this.closeAllModals();
            this.showModal('register-modal');
        });

        document.getElementById('switch-to-login').addEventListener('click', (e) => {
            e.preventDefault();
            this.closeAllModals();
            this.showModal('login-modal');
        });

        // Login form
        document.getElementById('login-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleLogin();
        });

        // Register form
        document.getElementById('register-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleRegister();
        });

        // Logout
        document.getElementById('btn-logout').addEventListener('click', async () => {
            await this.handleLogout();
        });

        // New post button
        document.getElementById('btn-new-post').addEventListener('click', () => {
            this.showNewPostModal();
        });

        // New post form
        document.getElementById('new-post-form').addEventListener('submit', async (e) => {
            e.preventDefault();
            await this.handleCreatePost();
        });

        // User dropdown
        document.getElementById('user-avatar-btn').addEventListener('click', (e) => {
            e.stopPropagation();
            document.getElementById('user-dropdown-menu').classList.toggle('show');
        });
        
        // Close dropdown when clicking on links inside
        document.querySelectorAll('#user-dropdown-menu .dropdown-item').forEach(item => {
            item.addEventListener('click', () => {
                document.getElementById('user-dropdown-menu').classList.remove('show');
            });
        });

        // Notifications button
        document.getElementById('btn-notifications').addEventListener('click', (e) => {
            e.stopPropagation();
            const panel = document.getElementById('notifications-panel');
            panel.style.display = panel.style.display === 'none' ? 'block' : 'none';
        });

        // Mark all notifications read
        document.getElementById('mark-all-read').addEventListener('click', async () => {
            await api.markAllNotificationsRead();
            this.loadNotifications();
        });

        // Close dropdowns on outside click
        document.addEventListener('click', () => {
            document.getElementById('user-dropdown-menu').classList.remove('show');
            document.getElementById('notifications-panel').style.display = 'none';
        });

        // Nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            });
        });
    }

    setupRouting() {
        window.addEventListener('hashchange', () => this.handleRoute());
    }

    handleRoute() {
        const hash = window.location.hash || '#/';
        const [path, ...params] = hash.slice(2).split('/');

        // Update active nav
        document.querySelectorAll('.nav-link').forEach(link => {
            const page = link.dataset.page;
            if ((path === '' && page === 'home') || path === page) {
                link.classList.add('active');
            } else {
                link.classList.remove('active');
            }
        });

        // Route handling
        switch (path) {
            case '':
            case 'home':
                this.renderHomePage();
                break;
            case 'categories':
                this.renderCategoriesPage();
                break;
            case 'category':
                this.renderCategoryPage(params[0]);
                break;
            case 'experts':
                this.renderExpertsPage();
                break;
            case 'post':
                this.renderPostPage(params[0]);
                break;
            case 'my-activity':
                this.renderMyActivityPage();
                break;
            case 'profile':
                this.renderProfilePage();
                break;
            case 'admin':
                this.renderAdminPage();
                break;
            default:
                this.renderHomePage();
        }
    }

    // ========================
    // Page Renderers
    // ========================

    async renderHomePage() {
        const main = document.getElementById('main-content');
        main.innerHTML = `
            <div class="container">
                <section class="hero">
                    <div class="hero-content">
                        <h1>Trova aiuto. Offri soluzioni. Cresci insieme.</h1>
                        <p>HelpMe! è la community dove condividere problemi e ricevere consigli da persone esperte. Ogni domanda trova risposta, ogni risposta crea valore.</p>
                        <div class="hero-actions">
                            ${this.user ? `
                                <button class="btn btn-primary" onclick="app.showNewPostModal()">Pubblica un problema</button>
                            ` : `
                                <button class="btn btn-primary" onclick="app.showModal('register-modal')">Inizia ora</button>
                            `}
                            <a href="#/categories" class="btn btn-outline">Scopri le categorie</a>
                        </div>
                    </div>
                    <div class="hero-visual">
                        <div class="feature-card">
                            <h3>Poni domande</h3>
                            <p>Descrivi il tuo problema nelle categorie tematiche e ricevi risposte da chi sa aiutarti davvero.</p>
                        </div>
                        <div class="feature-card">
                            <h3>Condividi competenze</h3>
                            <p>Metti a disposizione le tue conoscenze, aiuta gli altri e diventa esperto riconosciuto.</p>
                        </div>
                    </div>
                </section>
            </div>
            
            <section class="categories-section">
                <div class="container">
                    <div class="section-header">
                        <h2>Esplora per categoria</h2>
                        <p>Trova aiuto nell'ambito che ti interessa</p>
                    </div>
                    <div class="categories-grid" id="home-categories"></div>
                </div>
            </section>
            
            <div class="container page-section">
                <div class="two-column-layout">
                    <div class="posts-main">
                        <div class="section-header">
                            <h2>Problemi recenti</h2>
                        </div>
                        <div class="posts-list" id="posts-list">
                            <div class="loading"><div class="spinner"></div></div>
                        </div>
                    </div>
                    <aside class="sidebar">
                        <div class="sidebar-card">
                            <h3>Esperti della settimana</h3>
                            <div class="expert-list" id="sidebar-experts">
                                <div class="loading"><div class="spinner"></div></div>
                            </div>
                        </div>
                        <div class="sidebar-card">
                            <h3>Statistiche community</h3>
                            <div class="stats-list" id="sidebar-stats">
                                <div class="loading"><div class="spinner"></div></div>
                            </div>
                        </div>
                    </aside>
                </div>
            </div>
            
            <section class="cta-section">
                <div class="cta-content">
                    <h2>Unisciti alla community HelpMe!</h2>
                    <p>Migliaia di persone si aiutano ogni giorno. Inizia anche tu a dare e ricevere supporto.</p>
                    ${this.user ? '' : `
                        <button class="btn btn-white" onclick="app.showModal('register-modal')">Registrati gratuitamente</button>
                    `}
                </div>
            </section>
        `;

        // Load categories
        this.renderCategoriesGrid('home-categories');
        
        // Load posts
        this.loadPosts();
        
        // Load experts
        this.loadExperts('sidebar-experts');
        
        // Load stats
        this.loadStats();
    }

    renderCategoriesGrid(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        const icons = {
            'Cucina': '👨‍🍳',
            'Informatica': '💻',
            'Giardinaggio': '🌱',
            'Meccanica': '🔧',
            'Scuola': '📚',
            'Elettronica': '⚡',
            'Casa': '🏠',
            'Salute': '💊',
            'Sport': '⚽',
            'Finanza': '💰'
        };
        
        container.innerHTML = this.categories.map(cat => `
            <a href="#/category/${cat.id}" class="category-tag">
                <span class="category-icon">${icons[cat.nome] || '📁'}</span>
                <div class="category-name">${cat.nome}</div>
                <div class="category-count">${cat.post_count || 0} problemi</div>
            </a>
        `).join('');
    }

    async loadPosts(categoryId = null, status = null) {
        const container = document.getElementById('posts-list');
        if (!container) return;
        
        try {
            const params = {};
            if (categoryId) params.category = categoryId;
            if (status) params.status = status;
            
            const data = await api.getPosts(params);
            
            if (!data.posts || data.posts.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>Nessun problema trovato</h3>
                        <p>Sii il primo a pubblicare un problema!</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = data.posts.map(post => this.renderPostCard(post)).join('');
        } catch (error) {
            container.innerHTML = `<p class="error">Errore nel caricamento dei post</p>`;
        }
    }

    renderPostCard(post) {
        const initials = this.getInitials(post.autore_nome);
        const categories = post.categorie ? post.categorie.split(', ') : [];
        const icons = {
            'Cucina': '👨‍🍳', 'Informatica': '💻', 'Giardinaggio': '🌱',
            'Meccanica': '🔧', 'Scuola': '📚', 'Elettronica': '⚡',
            'Casa': '🏠', 'Salute': '💊', 'Sport': '⚽', 'Finanza': '💰'
        };
        
        return `
            <article class="post-card" onclick="window.location.hash='#/post/${post.id}'">
                <div class="post-header">
                    <div class="avatar">${initials}</div>
                    <div class="post-meta">
                        <div class="post-author">
                            ${post.autore_nome}
                        </div>
                        <div class="post-timestamp">${this.formatDate(post.data_inserimento)}</div>
                    </div>
                </div>
                <h3 class="post-title">${this.escapeHtml(post.titolo)}</h3>
                <p class="post-description">${this.escapeHtml(this.truncate(post.descrizione, 200))}</p>
                <div class="post-categories">
                    ${categories.map(c => `<span class="post-category">${icons[c] || '📁'} ${c}</span>`).join('')}
                </div>
                <div class="post-footer">
                    <div class="post-stat">
                        <svg viewBox="0 0 24 24"><path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path></svg>
                        <span>${post.commenti_count || 0} risposte</span>
                    </div>
                    <span class="post-status ${post.status === 'OPEN' ? 'status-open' : 'status-closed'}">
                        ${post.status === 'OPEN' ? 'Aperto' : 'Risolto'}
                    </span>
                </div>
            </article>
        `;
    }

    async loadExperts(containerId) {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        try {
            const data = await api.getExperts();
            
            if (!data.experts || data.experts.length === 0) {
                container.innerHTML = '<p class="no-data">Nessun esperto ancora</p>';
                return;
            }
            
            container.innerHTML = data.experts.slice(0, 5).map(expert => `
                <div class="expert-item">
                    <div class="expert-avatar">${this.getInitials(expert.nome)}</div>
                    <div class="expert-info">
                        <div class="expert-name">${expert.nome}</div>
                        <div class="expert-category">${expert.categoria} · ${expert.score} punti</div>
                    </div>
                </div>
            `).join('');
        } catch (error) {
            container.innerHTML = '<p class="error">Errore</p>';
        }
    }

    async loadStats() {
        const container = document.getElementById('sidebar-stats');
        if (!container) return;
        
        try {
            // Use admin stats if admin, otherwise show category counts
            const postsData = await api.getPosts({ status: 'CLOSED' });
            const expertsData = await api.getExperts();
            
            container.innerHTML = `
                <div class="stat-item">
                    <div class="stat-value">${postsData.total || 0}</div>
                    <div class="stat-label">Problemi risolti</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value secondary">${this.categories.length}</div>
                    <div class="stat-label">Categorie attive</div>
                </div>
                <div class="stat-item">
                    <div class="stat-value accent">${expertsData.experts?.length || 0}</div>
                    <div class="stat-label">Esperti certificati</div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = '<p class="error">Errore</p>';
        }
    }

    async renderCategoriesPage() {
        const main = document.getElementById('main-content');
        main.innerHTML = `
            <div class="container page-section">
                <div class="section-header">
                    <h2>Tutte le categorie</h2>
                    <p>Sfoglia i problemi per categoria</p>
                </div>
                <div class="categories-grid" id="all-categories"></div>
            </div>
        `;
        
        this.renderCategoriesGrid('all-categories');
    }

    async renderCategoryPage(categoryId) {
        const main = document.getElementById('main-content');
        const category = this.categories.find(c => c.id == categoryId);
        
        if (!category) {
            main.innerHTML = '<div class="container page-section"><p>Categoria non trovata</p></div>';
            return;
        }
        
        main.innerHTML = `
            <div class="container page-section">
                <div class="section-header">
                    <h2>${category.nome}</h2>
                    <p>${category.descrizione || 'Problemi relativi a ' + category.nome.toLowerCase()}</p>
                </div>
                <div class="posts-list" id="posts-list">
                    <div class="loading"><div class="spinner"></div></div>
                </div>
            </div>
        `;
        
        await this.loadPosts(categoryId);
    }

    async renderExpertsPage() {
        const main = document.getElementById('main-content');
        main.innerHTML = `
            <div class="container page-section">
                <div class="section-header">
                    <h2>Esperti della community</h2>
                    <p>Utenti che hanno raggiunto la soglia di punteggio per categoria</p>
                </div>
                <div class="expert-list" id="experts-list" style="max-width: 600px;">
                    <div class="loading"><div class="spinner"></div></div>
                </div>
            </div>
        `;
        
        try {
            const data = await api.getExperts();
            const container = document.getElementById('experts-list');
            
            if (!data.experts || data.experts.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>Nessun esperto ancora</h3>
                        <p>Aiuta la community e diventa il primo esperto!</p>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = data.experts.map(expert => `
                <div class="expert-item" style="padding: 1rem 0; border-bottom: 1px solid var(--color-border);">
                    <div class="expert-avatar">${this.getInitials(expert.nome)}</div>
                    <div class="expert-info">
                        <div class="expert-name">${expert.nome} (@${expert.nickname})</div>
                        <div class="expert-category">${expert.categoria} · ${expert.score} punti</div>
                    </div>
                    <span class="expert-badge">Esperto</span>
                </div>
            `).join('');
        } catch (error) {
            document.getElementById('experts-list').innerHTML = '<p class="error">Errore nel caricamento</p>';
        }
    }

    async renderPostPage(postId) {
        const main = document.getElementById('main-content');
        main.innerHTML = '<div class="container page-section"><div class="loading"><div class="spinner"></div></div></div>';
        
        try {
            const postData = await api.getPost(postId);
            const post = postData.post;
            const commentsData = await api.getComments(postId);
            const comments = commentsData.comments || [];
            
            const isOwner = this.user && this.user.id === post.autore_id;
            const isAdmin = this.user && this.user.role === 'ADMIN';
            const icons = {
                'Cucina': '👨‍🍳', 'Informatica': '💻', 'Giardinaggio': '🌱',
                'Meccanica': '🔧', 'Scuola': '📚', 'Elettronica': '⚡',
                'Casa': '🏠', 'Salute': '💊', 'Sport': '⚽', 'Finanza': '💰'
            };
            
            main.innerHTML = `
                <div class="container page-section">
                    <article class="post-detail">
                        <div class="post-header">
                            <div class="avatar ${post.autore_is_expert ? 'expert' : ''}">${this.getInitials(post.autore_nome)}</div>
                            <div class="post-meta">
                                <div class="post-author">
                                    ${post.autore_nome}
                                    ${post.autore_is_expert ? '<span class="expert-badge">Esperto</span>' : ''}
                                </div>
                                <div class="post-timestamp">${this.formatDate(post.data_inserimento)}</div>
                            </div>
                            <span class="post-status ${post.status === 'OPEN' ? 'status-open' : 'status-closed'}">
                                ${post.status === 'OPEN' ? 'Aperto' : 'Risolto'}
                            </span>
                        </div>
                        <h1 class="post-title">${this.escapeHtml(post.titolo)}</h1>
                        <p class="post-description">${this.escapeHtml(post.descrizione)}</p>
                        <div class="post-categories">
                            ${post.categorie.map(c => `<span class="post-category">${icons[c.nome] || '📁'} ${c.nome}</span>`).join('')}
                        </div>
                        
                        ${post.status === 'CLOSED' && post.final_solution_text ? `
                            <div class="solution-box">
                                <h4>Soluzione</h4>
                                <p>${this.escapeHtml(post.final_solution_text)}</p>
                            </div>
                        ` : ''}
                        
                        ${isOwner && post.status === 'OPEN' ? `
                            <div class="close-post-box">
                                <h4>Chiudi il problema</h4>
                                <p>Se hai trovato una soluzione, chiudi il problema indicando come l'hai risolto.</p>
                                <div class="form-group mt-2">
                                    <textarea id="final-solution" placeholder="Descrivi come hai risolto il problema..." rows="3"></textarea>
                                </div>
                                <button class="btn btn-secondary" onclick="app.handleClosePost(${post.id})">Chiudi problema</button>
                            </div>
                        ` : ''}
                        
                        ${(isOwner || isAdmin) ? `
                            <div class="mt-3">
                                <button class="btn btn-outline" onclick="app.handleDeletePost(${post.id})" style="color: var(--color-error);">
                                    Elimina post
                                </button>
                            </div>
                        ` : ''}
                    </article>
                    
                    <section class="comments-section">
                        <h3>${comments.length} Rispost${comments.length === 1 ? 'a' : 'e'}</h3>
                        
                        ${this.user && post.status === 'OPEN' ? `
                            <div class="comment-form">
                                <textarea id="new-comment" placeholder="Scrivi una risposta..."></textarea>
                                <button class="btn btn-primary" onclick="app.handleAddComment(${post.id})">Rispondi</button>
                            </div>
                        ` : ''}
                        
                        ${post.status === 'CLOSED' ? `
                            <p class="text-center" style="color: var(--color-text-muted); margin-bottom: 1rem;">
                                Questo problema è stato chiuso. Non è possibile aggiungere nuove risposte.
                            </p>
                        ` : ''}
                        
                        <div class="comments-list" id="comments-list">
                            ${this.renderComments(comments, post.solution_comment_id)}
                        </div>
                    </section>
                </div>
            `;
        } catch (error) {
            main.innerHTML = `<div class="container page-section"><p class="error">Errore nel caricamento del post: ${error.message}</p></div>`;
        }
    }

    renderComments(comments, solutionId) {
        if (!comments || comments.length === 0) {
            return '<p class="empty-state">Nessuna risposta ancora. Sii il primo a rispondere!</p>';
        }
        
        return comments.map(comment => `
            <div class="comment-card ${comment.id === solutionId ? 'solution' : ''}">
                <div class="comment-header">
                    <div class="avatar ${comment.autore_is_expert ? 'expert' : ''}">${this.getInitials(comment.autore_nome)}</div>
                    <div class="post-meta">
                        <div class="post-author">
                            ${comment.autore_nome}
                            ${comment.autore_is_expert ? '<span class="expert-badge">Esperto</span>' : ''}
                        </div>
                        <div class="post-timestamp">${this.formatDate(comment.data_inserimento)}</div>
                    </div>
                </div>
                <div class="comment-content">${this.escapeHtml(comment.testo)}</div>
                <div class="comment-actions">
                    <div class="vote-buttons">
                        <button class="btn-vote ${comment.my_vote === 1 ? 'active-up' : ''}" 
                                onclick="app.handleVote(${comment.id}, ${comment.my_vote === 1 ? 0 : 1})" 
                                ${!this.user ? 'disabled' : ''}>
                            ▲
                        </button>
                        <span class="vote-count">${comment.voto_totale}</span>
                        <button class="btn-vote ${comment.my_vote === -1 ? 'active-down' : ''}" 
                                onclick="app.handleVote(${comment.id}, ${comment.my_vote === -1 ? 0 : -1})"
                                ${!this.user ? 'disabled' : ''}>
                            ▼
                        </button>
                    </div>
                </div>
            </div>
        `).join('');
    }

    async renderMyActivityPage() {
        if (!this.user) {
            window.location.hash = '#/';
            return;
        }
        
        const main = document.getElementById('main-content');
        main.innerHTML = `
            <div class="container page-section">
                <div class="section-header">
                    <h2>La mia attività</h2>
                    <p>I tuoi problemi e le tue risposte</p>
                </div>
                <div class="posts-list" id="my-posts-list">
                    <div class="loading"><div class="spinner"></div></div>
                </div>
            </div>
        `;
        
        try {
            const data = await api.getMyPosts();
            const container = document.getElementById('my-posts-list');
            
            if (!data.posts || data.posts.length === 0) {
                container.innerHTML = `
                    <div class="empty-state">
                        <h3>Nessun problema pubblicato</h3>
                        <p>Inizia a pubblicare i tuoi problemi per ricevere aiuto dalla community!</p>
                        <button class="btn btn-primary mt-2" onclick="app.showNewPostModal()">Pubblica un problema</button>
                    </div>
                `;
                return;
            }
            
            container.innerHTML = data.posts.map(post => this.renderPostCard(post)).join('');
        } catch (error) {
            document.getElementById('my-posts-list').innerHTML = `<p class="error">Errore: ${error.message}</p>`;
        }
    }

    async renderProfilePage() {
        if (!this.user) {
            window.location.hash = '#/';
            return;
        }
        
        const main = document.getElementById('main-content');
        main.innerHTML = '<div class="container page-section"><div class="loading"><div class="spinner"></div></div></div>';
        
        try {
            const data = await api.getProfile();
            
            main.innerHTML = `
                <div class="container page-section" style="max-width: 600px;">
                    <div class="section-header">
                        <h2>Il mio profilo</h2>
                    </div>
                    
                    <div class="sidebar-card">
                        <div class="expert-item" style="margin-bottom: 1.5rem;">
                            <div class="avatar" style="width: 60px; height: 60px; font-size: 1.2rem;">${this.getInitials(data.user.nome)}</div>
                            <div class="expert-info">
                                <div class="expert-name" style="font-size: 1.2rem;">${data.user.nome}</div>
                                <div class="expert-category">@${data.user.nickname}</div>
                            </div>
                        </div>
                        
                        <div style="display: flex; gap: 2rem; margin-bottom: 1.5rem;">
                            <div>
                                <strong>${data.post_count}</strong> problemi
                            </div>
                            <div>
                                <strong>${data.comment_count}</strong> risposte
                            </div>
                        </div>
                        
                        ${data.stats && data.stats.length > 0 ? `
                            <h4 style="margin-bottom: 0.5rem;">Punteggi per categoria</h4>
                            <div style="margin-bottom: 1rem;">
                                ${data.stats.map(s => `
                                    <div style="display: flex; justify-content: space-between; padding: 0.5rem 0; border-bottom: 1px solid var(--color-border);">
                                        <span>${s.categoria}</span>
                                        <span>
                                            ${s.score} punti
                                            ${s.is_expert ? '<span class="expert-badge">Esperto</span>' : ''}
                                        </span>
                                    </div>
                                `).join('')}
                            </div>
                        ` : ''}
                        
                        <h4 style="margin-bottom: 0.5rem;">Categorie seguite</h4>
                        ${data.subscriptions && data.subscriptions.length > 0 ? `
                            <div style="display: flex; flex-wrap: wrap; gap: 0.5rem;">
                                ${data.subscriptions.map(s => `<span class="post-category">${s.nome}</span>`).join('')}
                            </div>
                        ` : '<p style="color: var(--color-text-muted);">Nessuna categoria seguita</p>'}
                    </div>
                </div>
            `;
        } catch (error) {
            main.innerHTML = `<div class="container page-section"><p class="error">Errore: ${error.message}</p></div>`;
        }
    }

    async renderAdminPage() {
        if (!this.user || this.user.role !== 'ADMIN') {
            window.location.hash = '#/';
            return;
        }
        
        const main = document.getElementById('main-content');
        main.innerHTML = `
            <div class="container page-section">
                <div class="section-header">
                    <h2>Pannello Amministrazione</h2>
                </div>
                
                <div class="admin-tabs">
                    <button class="admin-tab active" data-tab="users" onclick="app.switchAdminTab('users')">Utenti</button>
                    <button class="admin-tab" data-tab="categories" onclick="app.switchAdminTab('categories')">Categorie</button>
                    <button class="admin-tab" data-tab="stats" onclick="app.switchAdminTab('stats')">Statistiche</button>
                </div>
                
                <div id="admin-content">
                    <div class="loading"><div class="spinner"></div></div>
                </div>
            </div>
        `;
        
        await this.loadAdminUsers();
    }

    async switchAdminTab(tab) {
        document.querySelectorAll('.admin-tab').forEach(t => t.classList.remove('active'));
        document.querySelector(`.admin-tab[data-tab="${tab}"]`).classList.add('active');
        
        switch (tab) {
            case 'users':
                await this.loadAdminUsers();
                break;
            case 'categories':
                await this.loadAdminCategories();
                break;
            case 'stats':
                await this.loadAdminStats();
                break;
        }
    }

    async loadAdminUsers() {
        const container = document.getElementById('admin-content');
        
        try {
            const data = await api.getAdminUsers();
            
            container.innerHTML = `
                <table class="admin-table">
                    <thead>
                        <tr>
                            <th>ID</th>
                            <th>Nome</th>
                            <th>Nickname</th>
                            <th>Email</th>
                            <th>Ruolo</th>
                            <th>Stato</th>
                            <th>Azioni</th>
                        </tr>
                    </thead>
                    <tbody>
                        ${data.users.map(user => `
                            <tr>
                                <td>${user.id}</td>
                                <td>${user.nome}</td>
                                <td>@${user.nickname}</td>
                                <td>${user.email}</td>
                                <td>${user.role}</td>
                                <td>
                                    <span class="status-badge ${user.status === 'ACTIVE' ? 'active' : 'banned'}">
                                        ${user.status === 'ACTIVE' ? 'Attivo' : 'Bannato'}
                                    </span>
                                </td>
                                <td>
                                    ${user.role !== 'ADMIN' ? `
                                        ${user.status === 'ACTIVE' ? `
                                            <button class="btn btn-outline" onclick="app.handleBanUser(${user.id})" style="padding: 0.25rem 0.75rem; font-size: 0.85rem;">Ban</button>
                                        ` : `
                                            <button class="btn btn-secondary" onclick="app.handleUnbanUser(${user.id})" style="padding: 0.25rem 0.75rem; font-size: 0.85rem;">Unban</button>
                                        `}
                                    ` : ''}
                                </td>
                            </tr>
                        `).join('')}
                    </tbody>
                </table>
            `;
        } catch (error) {
            container.innerHTML = `<p class="error">Errore: ${error.message}</p>`;
        }
    }

    async loadAdminCategories() {
        const container = document.getElementById('admin-content');
        
        container.innerHTML = `
            <div class="mb-3">
                <h4>Aggiungi categoria</h4>
                <div style="display: flex; gap: 1rem; margin-top: 1rem;">
                    <input type="text" id="new-cat-name" placeholder="Nome categoria" style="flex: 1; padding: 0.5rem 1rem; border: 2px solid var(--color-border); border-radius: 8px;">
                    <input type="text" id="new-cat-desc" placeholder="Descrizione (opzionale)" style="flex: 2; padding: 0.5rem 1rem; border: 2px solid var(--color-border); border-radius: 8px;">
                    <button class="btn btn-primary" onclick="app.handleCreateCategory()">Aggiungi</button>
                </div>
            </div>
            
            <table class="admin-table">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Nome</th>
                        <th>Descrizione</th>
                        <th>Post</th>
                        <th>Azioni</th>
                    </tr>
                </thead>
                <tbody>
                    ${this.categories.map(cat => `
                        <tr>
                            <td>${cat.id}</td>
                            <td>${cat.nome}</td>
                            <td>${cat.descrizione || '-'}</td>
                            <td>${cat.post_count || 0}</td>
                            <td>
                                <button class="btn btn-outline" onclick="app.handleDeleteCategory(${cat.id})" style="padding: 0.25rem 0.75rem; font-size: 0.85rem; color: var(--color-error);">Elimina</button>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
    }

    async loadAdminStats() {
        const container = document.getElementById('admin-content');
        
        try {
            const data = await api.getAdminStats();
            
            container.innerHTML = `
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem;">
                    <div class="sidebar-card">
                        <div class="stat-value">${data.total_users}</div>
                        <div class="stat-label">Utenti totali</div>
                    </div>
                    <div class="sidebar-card">
                        <div class="stat-value secondary">${data.total_posts}</div>
                        <div class="stat-label">Problemi totali</div>
                    </div>
                    <div class="sidebar-card">
                        <div class="stat-value accent">${data.closed_posts}</div>
                        <div class="stat-label">Problemi risolti</div>
                    </div>
                    <div class="sidebar-card">
                        <div class="stat-value">${data.total_comments}</div>
                        <div class="stat-label">Commenti totali</div>
                    </div>
                    <div class="sidebar-card">
                        <div class="stat-value secondary">${data.total_experts}</div>
                        <div class="stat-label">Esperti certificati</div>
                    </div>
                </div>
            `;
        } catch (error) {
            container.innerHTML = `<p class="error">Errore: ${error.message}</p>`;
        }
    }

    // ========================
    // Event Handlers
    // ========================

    async handleLogin() {
        const email = document.getElementById('login-email').value;
        const password = document.getElementById('login-password').value;
        const errorEl = document.getElementById('login-error');
        
        try {
            const data = await api.login(email, password);
            this.setUser(data.user);
            this.closeAllModals();
            this.showToast('Login effettuato con successo!', 'success');
            this.handleRoute();
        } catch (error) {
            errorEl.textContent = error.message;
        }
    }

    async handleRegister() {
        const nome = document.getElementById('register-nome').value;
        const nickname = document.getElementById('register-nickname').value;
        const email = document.getElementById('register-email').value;
        const password = document.getElementById('register-password').value;
        const errorEl = document.getElementById('register-error');
        
        try {
            const data = await api.register({ nome, nickname, email, password });
            this.setUser(data.user);
            this.closeAllModals();
            this.showToast('Registrazione completata!', 'success');
            this.handleRoute();
        } catch (error) {
            errorEl.textContent = error.message;
        }
    }

    async handleLogout() {
        try {
            await api.logout();
            this.clearUser();
            this.showToast('Logout effettuato', 'success');
            window.location.hash = '#/';
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    showNewPostModal() {
        if (!this.user) {
            this.showModal('login-modal');
            return;
        }
        
        // Populate categories
        const container = document.getElementById('post-categories');
        container.innerHTML = this.categories.map(cat => `
            <input type="checkbox" id="cat-${cat.id}" class="category-checkbox" value="${cat.id}">
            <label for="cat-${cat.id}" class="category-label">${cat.nome}</label>
        `).join('');
        
        this.showModal('new-post-modal');
    }

    async handleCreatePost() {
        const titolo = document.getElementById('post-title').value;
        const descrizione = document.getElementById('post-description').value;
        const mediaUrl = document.getElementById('post-media').value;
        const errorEl = document.getElementById('post-error');
        
        const selectedCategories = Array.from(document.querySelectorAll('.category-checkbox:checked'))
            .map(cb => parseInt(cb.value));
        
        if (selectedCategories.length === 0) {
            errorEl.textContent = 'Seleziona almeno una categoria';
            return;
        }
        
        const media = mediaUrl ? [{ tipo: 'IMAGE', url: mediaUrl }] : [];
        
        try {
            const data = await api.createPost({
                titolo,
                descrizione,
                categorie: selectedCategories,
                media
            });
            
            this.closeAllModals();
            this.showToast('Problema pubblicato!', 'success');
            
            // Reset form
            document.getElementById('new-post-form').reset();
            
            // Navigate to the new post
            window.location.hash = `#/post/${data.post_id}`;
        } catch (error) {
            errorEl.textContent = error.message;
        }
    }

    async handleAddComment(postId) {
        const textarea = document.getElementById('new-comment');
        const testo = textarea.value.trim();
        
        if (!testo) {
            this.showToast('Scrivi un commento', 'error');
            return;
        }
        
        try {
            await api.createComment(postId, { testo });
            this.showToast('Risposta aggiunta!', 'success');
            textarea.value = '';
            
            // Reload comments
            const commentsData = await api.getComments(postId);
            const postData = await api.getPost(postId);
            document.getElementById('comments-list').innerHTML = this.renderComments(
                commentsData.comments, 
                postData.post.solution_comment_id
            );
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleVote(commentId, value) {
        if (!this.user) {
            this.showModal('login-modal');
            return;
        }
        
        try {
            await api.voteComment(commentId, value);
            // Reload the current post page
            const postId = window.location.hash.split('/')[2];
            this.renderPostPage(postId);
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleClosePost(postId) {
        const solution = document.getElementById('final-solution').value.trim();
        
        if (!solution) {
            this.showToast('Descrivi la soluzione', 'error');
            return;
        }
        
        try {
            await api.closePost(postId, { final_solution_text: solution });
            this.showToast('Problema chiuso con successo!', 'success');
            this.renderPostPage(postId);
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleDeletePost(postId) {
        if (!confirm('Sei sicuro di voler eliminare questo post?')) return;
        
        try {
            await api.deletePost(postId);
            this.showToast('Post eliminato', 'success');
            window.location.hash = '#/';
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleBanUser(userId) {
        const reason = prompt('Motivo del ban (opzionale):');
        
        try {
            await api.banUser(userId, reason || '');
            this.showToast('Utente bannato', 'success');
            this.loadAdminUsers();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleUnbanUser(userId) {
        try {
            await api.unbanUser(userId);
            this.showToast('Utente riabilitato', 'success');
            this.loadAdminUsers();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleCreateCategory() {
        const nome = document.getElementById('new-cat-name').value.trim();
        const descrizione = document.getElementById('new-cat-desc').value.trim();
        
        if (!nome) {
            this.showToast('Inserisci un nome per la categoria', 'error');
            return;
        }
        
        try {
            await api.createCategory({ nome, descrizione });
            this.showToast('Categoria creata', 'success');
            await this.loadCategories();
            this.loadAdminCategories();
            document.getElementById('new-cat-name').value = '';
            document.getElementById('new-cat-desc').value = '';
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    async handleDeleteCategory(categoryId) {
        if (!confirm('Sei sicuro di voler eliminare questa categoria?')) return;
        
        try {
            await api.deleteCategory(categoryId);
            this.showToast('Categoria eliminata', 'success');
            await this.loadCategories();
            this.loadAdminCategories();
        } catch (error) {
            this.showToast(error.message, 'error');
        }
    }

    // ========================
    // Utility Methods
    // ========================

    showModal(modalId) {
        document.getElementById(modalId).classList.add('show');
    }

    closeAllModals() {
        document.querySelectorAll('.modal').forEach(m => m.classList.remove('show'));
        // Clear error messages
        document.querySelectorAll('.form-error').forEach(el => el.textContent = '');
    }

    showToast(message, type = 'success') {
        const container = document.getElementById('toast-container');
        const toast = document.createElement('div');
        toast.className = `toast ${type}`;
        toast.innerHTML = `
            <span>${type === 'success' ? '✓' : '✗'}</span>
            <span>${message}</span>
        `;
        container.appendChild(toast);
        
        setTimeout(() => {
            toast.remove();
        }, 3000);
    }

    formatDate(dateStr) {
        if (!dateStr) return '';
        const date = new Date(dateStr);
        const now = new Date();
        const diff = now - date;
        
        // Less than 1 minute
        if (diff < 60000) return 'Adesso';
        // Less than 1 hour
        if (diff < 3600000) return `${Math.floor(diff / 60000)} min fa`;
        // Less than 1 day
        if (diff < 86400000) return `${Math.floor(diff / 3600000)} ore fa`;
        // Less than 1 week
        if (diff < 604800000) return `${Math.floor(diff / 86400000)} giorni fa`;
        
        return date.toLocaleDateString('it-IT', { day: 'numeric', month: 'short', year: 'numeric' });
    }

    escapeHtml(text) {
        if (!text) return '';
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }

    truncate(text, length) {
        if (!text) return '';
        if (text.length <= length) return text;
        return text.slice(0, length) + '...';
    }
}

// Initialize app
const app = new HelpMeApp();
