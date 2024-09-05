// scripts/carousel.js

const carouselTrack = document.querySelector('.carousel-track');
const images = document.querySelectorAll('.carousel-track img');
const imageWidth = images[0].clientWidth;
const totalImages = images.length;

// Variables to manage the current position
let currentIndex = 0;

// Function to handle smooth scrolling
const scrollCarousel = (index) => {
    carouselTrack.style.transition = 'transform 0.5s ease';
    const offset = -index * imageWidth;
    carouselTrack.style.transform = `translateX(${offset}px)`;
};

// Function to handle automatic scrolling
const autoScrollCarousel = () => {
    setInterval(() => {
        currentIndex = (currentIndex + 1) % (totalImages / 2);
        scrollCarousel(currentIndex);
    }, 3000); // Change image every 3 seconds
};

// Handle mouse wheel event
const handleMouseWheel = (event) => {
    event.preventDefault();
    const delta = event.deltaY > 0 ? 1 : -1;
    currentIndex = (currentIndex + delta + (totalImages / 2)) % (totalImages / 2);
    scrollCarousel(currentIndex);
};

// Add mouse wheel event listener
window.addEventListener('wheel', handleMouseWheel, { passive: false });

// Start automatic scrolling
autoScrollCarousel();
