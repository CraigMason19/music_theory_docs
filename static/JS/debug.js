// DEBUG
// Allows you to see each elements borders
document.addEventListener('keydown', function(event) {
    if (event.key === 'd' || event.key === 'D') {
        document.querySelectorAll('*').forEach(e => {
            e.classList.toggle('show-borders');
        });
    }
});