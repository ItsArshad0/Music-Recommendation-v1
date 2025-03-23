document.addEventListener("DOMContentLoaded", function () {
    function getRecommendations() {
        let songName = document.getElementById("songName").value;
        let recommendationsDiv = document.getElementById("recommendations");
        recommendationsDiv.innerHTML = "<p>Loading...</p>";

        fetch(`/api/get_songs?query=${encodeURIComponent(songName)}`)
            .then(response => response.json())
            .then(data => {
                recommendationsDiv.innerHTML = "";
                
                if (data.error) {
                    recommendationsDiv.innerHTML = `<p>${data.error}</p>`;
                    return;
                }

                data.forEach(song => {
                    let songItem = document.createElement("div");
                    songItem.classList.add("card", "p-3", "mb-2");
                    songItem.innerHTML = `
                        <strong>${song.title}</strong> - ${song.artist} <br>
                        Album: ${song.album} <br>
                        <a href="${song.url}" target="_blank" class="btn btn-sm btn-danger mt-1">🎵 Listen on YouTube Music</a>
                    `;
                    recommendationsDiv.appendChild(songItem);
                });
            })
            .catch(error => console.error("Error fetching songs:", error));
    }

    function showSuggestions(value) {
        let autocompleteBox = document.getElementById("autocomplete-list");
        autocompleteBox.innerHTML = "";

        if (!value) return;

        fetch(`/api/get_songs?query=${encodeURIComponent(value)}`)
            .then(response => response.json())
            .then(data => {
                data.forEach(song => {
                    let suggestionItem = document.createElement("div");
                    suggestionItem.classList.add("p-2", "border-bottom");
                    suggestionItem.innerText = song.title;
                    suggestionItem.onclick = () => {
                        document.getElementById("songName").value = song.title;
                        autocompleteBox.innerHTML = "";
                    };
                    autocompleteBox.appendChild(suggestionItem);
                });
            });
    }

    document.getElementById("songName").addEventListener("input", function () {
        showSuggestions(this.value);
    });

    window.getRecommendations = getRecommendations;
});