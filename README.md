Make sure you have Basic Music data set in tour folder for data set from it can read 
For me i made it run Netwok rather than LocalHost 
Used (ytmusicapi)-- pip install ytmusicapi
First get the logic of the Recomendation
Then run app.py
Follow the PreRequistes file and make sure the files are in place.It can make issue in html and Java scipt file


📝 Steps in the Flowchart:
1️⃣ User opens the webpage (index.html).
2️⃣ User types a song name → Autocomplete suggests songs.
3️⃣ User clicks "Search" → Sends request to Flask API (/api/get_songs).
4️⃣ Flask calls YouTube Music API (ytmusic.search()) to fetch song details.
5️⃣ Flask returns song recommendations as JSON.
6️⃣ JavaScript updates the UI → Shows song details with YouTube Music links.
