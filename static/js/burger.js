document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    const overlay = document.createElement('div');

    overlay.classList.add('overlay');
    document.body.appendChild(overlay);

    function toggleMenu() {
        nav.classList.toggle('active');
        overlay.classList.toggle('show');
    }

    burger?.addEventListener('click', toggleMenu);

    overlay.addEventListener('click', () => {
        nav.classList.remove('active');
        overlay.classList.remove('show');
    });
});
