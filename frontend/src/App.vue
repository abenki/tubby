<template>
    <div class="navbar bg-base-100 shadow-sm">
        <div class="navbar-start"></div>
        <div class="navbar-center">
            <a class="btn btn-ghost text-xl">Tubby</a>
        </div>
        <div class="navbar-end"></div>
    </div>
    <main class="flex justify-center items-center mt-10">
        <!-- URL Input Field and button -->
        <div class="flex flex-col items-center space-y-4">
            <input
                v-model="url"
                type="url"
                placeholder="Enter URL"
                class="input input-bordered w-100"
                @input="fetchVideoDetails"
            />
            <div
                v-if="videoDetails"
                class="card w-100 shadow-sm border-2 border-base-300"
            >
                <figure>
                    <img
                        :src="videoDetails.thumbnail"
                        :alt="videoDetails.title"
                    />
                </figure>
                <div class="card-body">
                    <h2 class="card-title">{{ videoDetails.title }}</h2>
                    <p>{{ videoDetails.channel }}</p>
                    <p>{{ formatDuration(videoDetails.duration) }}</p>
                </div>
            </div>
            <!-- Progress Bar -->
            <div v-if="isDownloading" class="w-full mt-4 flex justify-center">
                <progress
                    class="progress progress-accent w-56"
                    :value="progress"
                    max="100"
                ></progress>
            </div>
            <div
                v-if="isDownloading"
                role="alert"
                class="alert alert-info alert-soft"
            >
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 24 24"
                    class="h-6 w-6 shrink-0 stroke-current"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
                    ></path>
                </svg>
                <span>{{ progressMessage }}</span>
            </div>
            <!-- Error display -->
            <div v-if="downloadError" class="alert alert-error mt-4">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    class="stroke-current shrink-0 h-6 w-6"
                    fill="none"
                    viewBox="0 0 24 24"
                >
                    <path
                        stroke-linecap="round"
                        stroke-linejoin="round"
                        stroke-width="2"
                        d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z"
                    />
                </svg>
                <span>{{ downloadError }}</span>
            </div>
            <!-- Download button -->
            <button
                class="btn btn-primary"
                @click="startDownload"
                :disabled="isDownloading"
            >
                Download
            </button>
        </div>
    </main>
</template>

<script setup>
import { ref } from "vue";

const url = ref(""); // Store the URL entered by the user
const videoDetails = ref(null); // Store the fetched video details
const progress = ref(0); // Store progress value
const isDownloading = ref(false); // Whether the download is in progress
const progressMessage = ref(""); // Message to display during download
const downloadError = ref("");

// Fetch video details from YouTube API
const fetchVideoDetails = async () => {
    if (!url.value) {
        videoDetails.value = null;
        return;
    }

    try {
        const response = await fetch(
            `/api/video_details?url=${encodeURIComponent(url.value)}`,
        );
        const result = await response.json();

        if (result.success) {
            videoDetails.value = result.data;
        } else {
            videoDetails.value = null;
            console.error("Error fetching video details:", result.error);
        }
    } catch (error) {
        console.error("Error fetching video details:", error);
        videoDetails.value = null;
    }
};

// Format video duration (ISO 8601 duration to HH:MM:SS format)
const formatDuration = (duration) => {
    const regex = /PT(\d+H)?(\d+M)?(\d+S)?/;
    const match = duration.match(regex);

    // Extract hours, minutes, and seconds (or use default 0 if missing)
    const hours = match[1] ? match[1].replace("H", "") : "00";
    const minutes = match[2] ? match[2].replace("M", "") : "00";
    const seconds = match[3] ? match[3].replace("S", "") : "00";

    // Ensure two-digit formatting for minutes and seconds
    const formattedMinutes = minutes.padStart(2, "0");
    const formattedSeconds = seconds.padStart(2, "0");

    return `${hours}:${formattedMinutes}:${formattedSeconds}`;
};

// Start downloading
const startDownload = async () => {
    if (!url.value) {
        alert("Please enter a valid YouTube URL");
        return;
    }

    downloadError.value = "";
    isDownloading.value = true;
    progress.value = 0;
    progressMessage.value = "Starting download...";

    try {
        // Call the backend API
        const response = await fetch("/api/download", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({
                url: url.value,
                format: "best", // TODO: add a format selector in the UI
            }),
        });

        const result = await response.json();

        if (result.success) {
            progress.value = 100;
            progressMessage.value = `Download complete! Saved to: ${result.path}`;
        } else {
            progress.value = 0;
            downloadError.value = result.error || result.message;
            progressMessage.value = "Download failed";
        }
    } catch (error) {
        console.error("Download failed:", error);
        progress.value = 0;
        downloadError.value = `Error: ${error.message}`;
        progressMessage.value = "Download failed";
    } finally {
        setTimeout(() => {
            isDownloading.value = false;
        }, 3000);
    }
};
</script>
