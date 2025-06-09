document.addEventListener('DOMContentLoaded', () => {

    const API_BACKEND_URL = 'http://127.0.0.1:8000/posts/'; 

    const navButtons = document.querySelectorAll('.nav-btn');
    const formContainers = document.querySelectorAll('.form-container');
    const notificationArea = document.getElementById('notification-area');

    const createForm = document.getElementById('create-post-form');
    const editForm = document.getElementById('edit-post-form');
    const deleteForm = document.getElementById('delete-post-form');

    let notificationTimeout;


    function showNotification(message, isError = false) {
        if (notificationTimeout) {
            clearTimeout(notificationTimeout);
        }

        notificationArea.innerHTML = '';

        const notification = document.createElement('div');
        notification.className = 'notification';
        if (isError) {
            notification.classList.add('error');
        }
        notification.textContent = message;
        notificationArea.appendChild(notification);

        setTimeout(() => {
            notification.classList.add('show');
        }, 10);

        notificationTimeout = setTimeout(() => {
            notification.classList.remove('show');
            notification.addEventListener('transitionend', () => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, { once: true });
        }, 3000);
    }


    const apiService = {
        async request(endpoint, options = {}) {
            try {
                const response = await fetch(endpoint, {
                    headers: { 'Content-Type': 'application/json' },
                    ...options,
                });

                if (!response.ok) {
                    const errorData = await response.json().catch(() => null);
                    throw new Error(errorData?.message || response.statusText);
                }
                
                if (response.status === 204 || !response.headers.get('content-length')) {
                    return {};
                }
                
                return await response.json();
            } catch (error) {
                console.error('API Request Failed:', error);
                throw error;
            }
        },

        createPost(data) {
            return this.request(API_BACKEND_URL, {
                method: 'POST',
                body: JSON.stringify(data),
            });
        },

        updatePost(id, data) {
            return this.request(`${API_BACKEND_URL}${id}`, {
                method: 'PUT',
                body: JSON.stringify(data),
            });
        },

        deletePost(id) {
            return this.request(`${API_BACKEND_URL}${id}`, {
                method: 'DELETE',
            });
        },
    };


    navButtons.forEach(button => {
        button.addEventListener('click', () => {
            const targetFormId = button.getAttribute('data-form');
            
            navButtons.forEach(btn => btn.classList.remove('active'));
            button.classList.add('active');

            formContainers.forEach(container => {
                if (container.id === targetFormId) {
                    container.classList.add('active');
                } else {
                    container.classList.remove('active');
                }
            });
        });
    });


    if (createForm) {
        createForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const title = document.getElementById('post-title').value;
            const content = document.getElementById('post-content').value;

            if (title.trim() === '' || content.trim() === '') {
                showNotification('Пожалуйста, заполните заголовок и содержание', true);
                return;
            }

            try {
                const createdPost = await apiService.createPost({ title, content });
                showNotification(createdPost.message);
                createForm.reset();
            } catch (error) {
                showNotification(`Ошибка: ${error.message}`, true);
            }
        });
    }

    if (editForm) {
        editForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const id = document.getElementById('edit-post-id').value;
            const title = document.getElementById('edit-post-title').value;
            const content = document.getElementById('edit-post-content').value;

            if (!id) {
                showNotification('Пожалуйста, укажите ID поста', true);
                return;
            }

            if (!title && !content) {
                showNotification('Введите новый заголовок или новое содержание', true);
                return;
            }

            try {
                const updatedPost = await apiService.updatePost(id, { title, content });
                showNotification(updatedPost.message);
                editForm.reset();
            } catch(error) {
                showNotification(`Ошибка: ${error.message}`, true);
            }
        });
    }

    if(deleteForm) {
        deleteForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const id = document.getElementById('delete-post-id').value;
            
            if(id.trim() === '') {
                showNotification('Пожалуйста, введите ID поста', true);
                return;
            }
            
            try {
                const deletePost = await apiService.deletePost(id);
                showNotification(deletePost.message);
                deleteForm.reset();
            } catch(error) {
                showNotification(`Ошибка: ${error.message}`, true);
            }
        });
    }
});
