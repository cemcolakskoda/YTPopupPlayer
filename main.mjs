// main.mjs
import config from './config.js';

let player; // Variable to store the YouTube player instance

function onYouTubeIframeAPIReady() {
    player = new YT.Player('YTPlayerPopup', {
        events: {
            'onReady': onPlayerReady
        }
    });
}

function onPlayerReady(event) {
    // Video is ready to play, but we won't autoplay it
}

const YTLinks = document.querySelectorAll(".youtube-link");
const YTPlayerPopup = document.querySelector(".youtube-player-popup iframe");

YTLinks.forEach(link => {
    link.addEventListener("click", () => {
        const videoId = config.videoSource === 'youtube' ? config.youtubeLinks[link.dataset.link] : config.onedriveLinks[link.dataset.link];
        const videoLink = config.videoSource === 'youtube' ? `https://www.youtube.com/embed/${videoId}?enablejsapi=1` : videoId;

        document.querySelector(".youtube-player-popup iframe").src = videoLink;
        YTPlayerPopup.classList.add("active");
    });
});

YTPlayerPopup.addEventListener("click", () => {
    YTPlayerPopup.classList.remove("active");
    closePopup(); // Optionally close the popup when the video is clicked
});

function closePopup() {
    // Pause the video using the YouTube API when closing the overlay
    if (player && typeof player.pauseVideo === 'function') {
        player.pauseVideo();
    }

    // Reset the video source to stop playback
    YTPlayerPopup.src = '';

    // Remove the "active" class from the overlay
    YTPlayerPopup.classList.remove("active");
}

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
