const YTPlayerOverlay = document.querySelector(".youtube-player-overlay");
const YTLinks = document.querySelectorAll(".youtube-link");
const YTPlayerPopup = document.querySelector(".youtube-player-popup iframe");

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
        let videoLink = `https://www.youtube.com/embed/${link.dataset.link}?enablejsapi=1`;
        YTPlayerPopup.src = videoLink;

        // Ensure the YouTube API is loaded before creating the player
        if (typeof YT !== 'undefined' && YT.loaded) {
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
