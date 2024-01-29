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

        // Determine the video source (YouTube or OneDrive)
        const videoSource = link.dataset.source || 'youtube';
        const videoId = videoSource === 'youtube' ? link.dataset.youtube : link.dataset.onedrive;

        // Build the video link based on the source
        let videoLink = '';
        if (videoSource === 'youtube') {
            videoLink = `https://www.youtube.com/embed/${videoId}?enablejsapi=1`;
            // Ensure the YouTube API is loaded before creating the player
            if (typeof YT !== 'undefined' && YT.loaded) {
                onYouTubeIframeAPIReady();
            }
        } else if (videoSource === 'onedrive') {
            videoLink = videoId;
        }

        // Set the video link to the iframe
        YTPlayerPopup.src = videoLink;
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
