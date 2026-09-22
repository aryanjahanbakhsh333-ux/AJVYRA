(function (window) {
    "use strict";

    class AJVYRACinematicWebPlayer {
        constructor(videoElement, options) {
            if (!videoElement) {
                throw new Error(
                    "A video element is required."
                );
            }

            this.video = videoElement;
            this.options = options || {};
            this.currentMovie = null;
        }

        playMovie(movie) {
            if (!movie || !movie.movie_url) {
                throw new Error(
                    "Movie does not contain a playable URL."
                );
            }

            this.currentMovie = movie;

            this.video.pause();
            this.video.removeAttribute("src");

            while (this.video.firstChild) {
                this.video.removeChild(
                    this.video.firstChild
                );
            }

            const source = document.createElement("source");

            source.src = movie.movie_url;
            source.type = "video/mp4";

            this.video.appendChild(source);
            this.video.load();

            return this.video.play();
        }

        stop() {
            this.video.pause();
            this.video.currentTime = 0;
        }

        pause() {
            this.video.pause();
        }

        resume() {
            return this.video.play();
        }

        toggle() {
            if (this.video.paused) {
                return this.resume();
            }

            this.pause();
            return Promise.resolve();
        }

        setSubtitleTrack(language) {
            const tracks =
                this.video.textTracks;

            for (let i = 0; i < tracks.length; i += 1) {
                tracks[i].mode =
                    language &&
                    tracks[i].language === language
                        ? "showing"
                        : "hidden";
            }
        }

        disableSubtitles() {
            const tracks =
                this.video.textTracks;

            for (let i = 0; i < tracks.length; i += 1) {
                tracks[i].mode = "disabled";
            }
        }

        isPlaying() {
            return (
                !this.video.paused &&
                !this.video.ended
            );
        }
    }

    window.AJVYRACinematicWebPlayer =
        AJVYRACinematicWebPlayer;
})(window);
