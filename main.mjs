import config from './config.js';
import config from './config.json';

const YTPlayerOverlay = document.querySelector(".youtube-player-overlay");
const YTLinks = document.querySelectorAll(".youtube-link");
const YTPlayerPopup = document.querySelector(".youtube-player-popup iframe");
const divTitles = config.divTitles;

let player; // Variable to store the YouTube player instance

function onYouTubeIframeAPIReady() {
    player = new YT.Player(YTPlayerPopup, {
        events: {
            'onReady': onPlayerReady
        }
    });
}

function onPlayerReady(event) {
    // Video is ready to play, but we won't autoplay it
}

YTLinks.forEach(link => {
    link.addEventListener("click", () => {
        YTPlayerOverlay.classList.add("active");

        // Determine the video source (YouTube or OneDrive)
        const videoId = config.videoSource === 'youtube' ? config.youtubeLinks[link.dataset.link] : config.onedriveLinks[link.dataset.link];
        const videoLink = config.videoSource === 'youtube' ? `https://www.youtube.com/embed/${videoId}?enablejsapi=1` : videoId;

        // Set the video link to the iframe
        YTPlayerPopup.src = videoLink;

        // Ensure the YouTube API is loaded before creating the player
        if (config.videoSource === 'youtube' && typeof YT !== 'undefined' && YT.loaded) {
            onYouTubeIframeAPIReady();
        }
    });
});

function closePopup() {
    // Pause the video using the YouTube API when closing the overlay
    if (player && typeof player.pauseVideo === 'function') {
        player.pauseVideo();
    }

    // Reset the video source to stop playback
    YTPlayerPopup.src = '';

    // Remove the "active" class from the overlay
    YTPlayerOverlay.classList.remove("active");
}

YTPlayerOverlay.addEventListener("click", (event) => {
    // Check if the click was outside the popup area
    if (event.target === YTPlayerOverlay) {
        closePopup();
    }
});

document.addEventListener("keydown", (event) => {
    // Check if the "Esc" key was pressed
    if (event.key === "Escape") {
        closePopup();
    }
});

// Handle page reload (F5)
window.addEventListener('beforeunload', () => {
    closePopup();
});

// Dynamically generate div elements with titles
divTitles.forEach(title => {
const divElement = document.createElement('div');
    divElement.className = 'youtube-link';
    divElement.dataset.link = title; // Assuming you want to use the title as the link
    divElement.innerHTML = `
        <div class="icon">
            <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="1.5" stroke="currentColor" class="w-6 h-6">
                <!-- Your SVG path here -->
            </svg>
        </div>
        ${title}
    `;

    // Add the div element to the container
    divContainer.appendChild(divElement);
});