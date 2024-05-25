document.addEventListener('DOMContentLoaded', function () {
    const notificationButton = document.getElementById('notification-button');
    const notificationPanel = document.getElementById('notification-panel');
    const unreadCount = document.getElementById('unread-count');

    notificationButton.addEventListener('click', function () {
        notificationPanel.classList.toggle('hidden');
        fetch('/users/mark_notifications_as_read/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify({})
        }).then(response => {
            if (response.status === 200) {
                unreadCount.textContent = '';
            }
        });
    });

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
});