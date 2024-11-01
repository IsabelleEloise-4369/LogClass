document.getElementById('status-filter').addEventListener('change', function() {
    const filterValue = this.value;
    const users = document.querySelectorAll('.user-item');

    users.forEach(user => {
        if (filterValue === 'all') {
            user.style.display = 'flex';
        } else {
            if (user.getAttribute('data-status') === filterValue) {
                user.style.display = 'flex';
            } else {
                user.style.display = 'none';
            }
        }
    });
});