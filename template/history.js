// static/js/history.js
let allData = [];

function formatTimestamp(iso) {
  const date = new Date(iso);
  return date.toLocaleString('en-GB', {
    year: 'numeric', month: 'short', day: 'numeric',
    hour: '2-digit', minute: '2-digit',
    hour12: false
  });
}

function fetchData() {
  console.log("✅ fetchData() started");

  fetch('/api/sos')
    .then(res => {
      if (!res.ok) throw new Error("Failed to fetch SOS data");
      return res.json();
    })
    .then(data => {
      if (!data || data.length === 0) return;

      allData = data;

      const latest = data[0];
      document.getElementById("latest-time").textContent = latest.timestamp || '-';
      document.getElementById("latest-location").textContent = latest.location || '-';
      document.getElementById("latest-coord").textContent = `${latest.latitude}, ${latest.longitude}`;
      document.getElementById("latest-confidence").textContent = latest.confidence;
      document.getElementById("latest-image").src = latest.image_url || '';

      initHistoryMap(data);
      updateTable(data);
    })
    .catch(err => {
      alert("❌ Error: " + err.message);
    });
}

function initHistoryMap(data) {
  const mapEl = document.getElementById("history-map");
  if (!mapEl || mapEl._leaflet_id) return;

  const latest = data[0];
  const map = L.map("history-map").setView([latest.latitude, latest.longitude], 13);
  L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: '&copy; OpenStreetMap contributors'
  }).addTo(map);

  data.forEach(item => {
    if (item.latitude && item.longitude) {
      L.marker([item.latitude, item.longitude]).addTo(map)
        .bindPopup(`
          <b>📍 SOS Event</b><br/>
          <b>Time:</b> ${item.timestamp || '-'}<br/>
          <b>Location:</b> ${item.location || '-'}<br/>
          <b>Confidence:</b> ${item.confidence || '?'}
        `);
    }
  });
}

function updateTable(data) {
  const tbody = document.querySelector("#history-table tbody");
  tbody.innerHTML = "";

  data.forEach(item => {
    const tr = document.createElement("tr");
    tr.innerHTML = `
      <td>${formatTimestamp(item.timestamp)}</td>
      <td>${item.location || '-'}</td>
      <td>${item.latitude}, ${item.longitude}</td>
      <td>${item.confidence}</td>
      <td><img src="${item.image_url || ''}" width="80"/></td>
      <td><button class="delete-btn" onclick="deleteSOS('${item._id}')">🗑️</button></td>
    `;
    tbody.appendChild(tr);
  });
}

function deleteSOS(id) {
  if (!confirm("Are you sure you want to delete this record?")) return;

  fetch(`/api/sos/${id}`, {
    method: 'DELETE'
  })
    .then(res => {
      if (!res.ok) throw new Error("Failed to delete");
      fetchData();
    })
    .catch(err => alert("❌ Delete Error: " + err.message));
}
