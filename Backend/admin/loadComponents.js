function loadHTML(id, url) {
    fetch(url)
        .then(response => response.text())
        .then(data => {
            document.getElementById(id).innerHTML = data;
        })
        .catch(error => console.error('Error cargando el archivo:', error));
}

window.addEventListener('DOMContentLoaded', () => {
    loadHTML('header-container', 'header.html');
    loadHTML('sidebar-container', 'sidebar.html');
});
