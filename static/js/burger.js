document.addEventListener('DOMContentLoaded', () => {
    const burger = document.querySelector('.burger');
    const nav = document.querySelector('.nav-links');
    if (burger && nav) {
        burger.addEventListener('click', () => {
            nav.classList.toggle('active');
        });
    }
});
