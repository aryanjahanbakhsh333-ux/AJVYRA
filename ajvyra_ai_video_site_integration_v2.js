(() => {
  "use strict";

  const FEED_URL =
    window.AJVYRA_AI_COMMUNITY_FEED_URL ||
    "assets/ai-video-library/ajvyra-ai-community-feed-v2.json";

  const state = {
    videos: [],
    loaded: false,
  };

  function escapeHTML(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function validVideo(item) {
    return (
      item &&
      item.ready === true &&
      item.published === true &&
      typeof item.video_url === "string" &&
      item.video_url.length > 0
    );
  }

  async function loadFeed() {
    try {
      const response = await fetch(
        FEED_URL,
        {
          cache: "no-store",
        }
      );

      if (!response.ok) {
        throw new Error(
          `Feed request failed: ${response.status}`
        );
      }

      const data = await response.json();

      state.videos = Array.isArray(data.videos)
        ? data.videos.filter(validVideo)
        : [];

      state.loaded = true;

      render();
      dispatchReady();

      return state.videos;
    } catch (error) {
      console.warn(
        "[AJVYRA AI] Feed unavailable:",
        error
      );

      state.videos = [];
      state.loaded = false;

      render();

      return [];
    }
  }

  function dispatchReady() {
    window.dispatchEvent(
      new CustomEvent(
        "ajvyra:ai-community-ready",
        {
          detail: {
            videos: state.videos,
            count: state.videos.length,
          },
        }
      )
    );
  }

  function openVideo(video) {
    window.dispatchEvent(
      new CustomEvent(
        "ajvyra:open-release",
        {
          detail: {
            release: {
              id: video.id,
              title: video.title,
              video_url: video.video_url,
              poster_url: video.poster_url,
              subtitle_url: video.subtitle_url,
            },
          },
        }
      )
    );
  }

  function ensureSection() {
    let section =
      document.querySelector(
        "#ajvyra-ai-community"
      );

    if (section) {
      return section;
    }

    section = document.createElement(
      "section"
    );

    section.id =
      "ajvyra-ai-community";

    section.style.cssText = `
      padding: 56px 20px;
      background: #050505;
      color: #fff;
    `;

    const anchor =
      document.querySelector(
        "#anime"
      ) ||
      document.querySelector(
        "#games"
      ) ||
      document.body;

    anchor.parentNode.insertBefore(
      section,
      anchor
    );

    return section;
  }

  function render() {
    const section =
      ensureSection();

    const cards = state.videos
      .map((video) => {
        const title = escapeHTML(
          video.title ||
            "AJVYRA AI Creation"
        );

        const prompt = escapeHTML(
          video.prompt || ""
        );

        return `
          <article
            class="ajvyra-ai-video-card"
            data-ai-video-id="${escapeHTML(
              video.id
            )}"
            style="
              background:#0b0b0b;
              border:1px solid #202020;
              border-radius:18px;
              overflow:hidden;
            "
          >
            <div
              style="
                aspect-ratio:16/9;
                background:#111;
                display:flex;
                align-items:center;
                justify-content:center;
              "
            >
              <video
                src="${escapeHTML(
                  video.video_url
                )}"
                preload="metadata"
                muted
                playsinline
                controls
                style="
                  width:100%;
                  height:100%;
                  object-fit:cover;
                "
              ></video>
            </div>

            <div style="padding:18px;">
              <div
                style="
                  font-size:17px;
                  font-weight:700;
                  margin-bottom:7px;
                "
              >
                ${title}
              </div>

              <div
                style="
                  color:#858585;
                  font-size:13px;
                  line-height:1.5;
                  min-height:40px;
                "
              >
                ${prompt}
              </div>

              <button
                type="button"
                class="ajvyra-ai-watch"
                data-ai-watch="${escapeHTML(
                  video.id
                )}"
                style="
                  margin-top:14px;
                  width:100%;
                  min-height:44px;
                  border:0;
                  border-radius:12px;
                  background:#fff;
                  color:#000;
                  font-weight:700;
                  cursor:pointer;
                "
              >
                Watch
              </button>
            </div>
          </article>
        `;
      })
      .join("");

    section.innerHTML = `
      <div
        style="
          max-width:1100px;
          margin:0 auto;
        "
      >
        <div style="margin-bottom:24px;">
          <div
            style="
              font-size:12px;
              letter-spacing:.18em;
              color:#777;
              text-transform:uppercase;
            "
          >
            AJVYRA AI
          </div>

          <h2
            style="
              margin:7px 0;
              font-size:32px;
            "
          >
            AI Community
          </h2>

          <p
            style="
              margin:0;
              color:#777;
            "
          >
            Anime videos created by AJVYRA visitors.
          </p>
        </div>

        ${
          state.videos.length
            ? `
              <div
                style="
                  display:grid;
                  grid-template-columns:
                    repeat(
                      auto-fit,
                      minmax(260px, 1fr)
                    );
                  gap:18px;
                "
              >
                ${cards}
              </div>
            `
            : `
              <div
                style="
                  padding:40px 20px;
                  border:1px solid #181818;
                  border-radius:18px;
                  color:#666;
                  text-align:center;
                "
              >
                No public AI creations yet.
              </div>
            `
        }
      </div>
    `;

    section
      .querySelectorAll(
        ".ajvyra-ai-watch"
      )
      .forEach((button) => {
        button.addEventListener(
          "click",
          () => {
            const id =
              button.dataset.aiWatch;

            const video =
              state.videos.find(
                (item) =>
                  item.id === id
              );

            if (video) {
              openVideo(video);
            }
          }
        );
      });
  }

  window.AJVYRAAICommunity = {
    load: loadFeed,

    getVideos() {
      return [...state.videos];
    },

    refresh() {
      return loadFeed();
    },
  };

  if (
    document.readyState ===
    "loading"
  ) {
    document.addEventListener(
      "DOMContentLoaded",
      loadFeed,
      { once: true }
    );
  } else {
    loadFeed();
  }
})();
