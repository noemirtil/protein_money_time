const mobileMenuButton = document.getElementById('mobile-menu-button');
const mobileMenu = document.getElementById('mobile-menu');
const menuIcon = document.getElementById('menu-icon');
const closeIcon = document.getElementById('close-icon');
const scrollUpButton = document.getElementById('scroll-up-button');
const modal = document.getElementById('about-modal');
const openButtons = document.querySelectorAll('[id^="open-about-modal"]');
const closeButtons = document.querySelectorAll('#close-modal-button, #modal-close-footer');

function openModal() {
    if (modal) {
        modal.classList.remove('hidden');
    }
}

function closeModal() {
    if (modal) {
        modal.classList.add('hidden');
    }
}

openButtons.forEach(button => {
    button.addEventListener('click', openModal);
});

closeButtons.forEach(button => {
    button.addEventListener('click', closeModal);
});

window.addEventListener('click', (event) => {
    if (event.target === modal) {
        closeModal();
    }
});

document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape' && !modal.classList.contains('hidden')) {
        closeModal();
    }
});

mobileMenuButton.addEventListener('click', () => {
    mobileMenu.classList.toggle('hidden');
    menuIcon.classList.toggle('hidden');
    closeIcon.classList.toggle('hidden');
});
window.addEventListener('scroll', () => {
    let scrollPosition = window.scrollY;

    if (scrollPosition > 300) {
        scrollUpButton.classList.add('opacity-100');
        scrollUpButton.classList.remove('pointer-events-none');
    } else {
        scrollUpButton.classList.remove('opacity-100');
        scrollUpButton.classList.add('pointer-events-none');
    }
});
scrollUpButton.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
});