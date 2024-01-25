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

YTPlayerOverlay.addEventListener("click", () => {
    // Pause the video using the YouTube API when closing the overlay
    if (player) {
        player.pauseVideo();
    }

    // Remove the "active" class from the overlay
    YTPlayerOverlay.classList.remove("active");
});
