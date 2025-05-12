let fullData = [];

async function fetchHistory() {
  try {
    const res = await fetch("/api/sos/history");
    const data = await res.json();
    fullData = data;
    renderSummary(data);
    renderTable(data);
  } catch (error) {
    console.error("❌ Failed to fetch history:", error);
  }
}

function renderSummary(data) {
  const summary = document.getElementById("summary");
  summary.textContent = `📊 Total SOS Events: ${data.length}`;
}

function renderTable(data) {
  const tbody = document.querySelector("#sos-table tbody");
  tbody.innerHTML = "";

  if (data.length === 0) {
    tbody.innerHTML = "<tr><td colspan='6'>No data found.</td></tr>";
    return;
  }

  data.forEach(event => {
    const row = document.createElement("tr");
    const dateOnly = event.timestamp?.split("T")[0] || "";
    row.setAttribute("data-date", dateOnly);

    row.innerHTML = `
      <td>${new Date(event.timestamp).toLocaleString()}</td>
      <td>${event.location || "Unknown"}</td>
      <td>${event.latitude?.toFixed(5) || "N/A"}, ${event.longitude?.toFixed(5) || "N/A"}</td>
      <td>${event.confidence}</td>
      <td><a href="${event.image_url}" target="_blank">View</a></td>
      <td><button onclick="deleteRow('${event._id}')">🗑️ Delete</button></td>
    `;
    tbody.appendChild(row);
  });
}

document.getElementById("search").addEventListener("input", function () {
  const keyword = this.value.trim().toLowerCase();
  const rows = document.querySelectorAll("#sos-table tbody tr");

  rows.forEach(row => {
    const text = row.innerText.toLowerCase();
    const date = row.getAttribute("data-date") || "";
    if (text.includes(keyword) || date.includes(keyword)) {
      row.style.display = "";
    } else {
      row.style.display = "none";
    }
  });
});

function exportCSV() {
  const rows = fullData.map(e => [
    e.timestamp,
    e.location,
    e.latitude,
    e.longitude,
    e.confidence,
    e.image_url
  ]);

  let csv = "timestamp,location,latitude,longitude,confidence,image_url\n";
  rows.forEach(row => {
    csv += row.join(",") + "\n";
  });

  const blob = new Blob([csv], { type: "text/csv" });
  const url = URL.createObjectURL(blob);

  const link = document.createElement("a");
  link.href = url;
  link.download = "sos_history.csv";
  link.click();
  URL.revokeObjectURL(url);
}

async function deleteRow(id) {
  if (!confirm("Are you sure you want to delete this item?")) return;

  try {
    const res = await fetch(`/api/sos/${id}`, { method: "DELETE" });
    if (res.ok) {
      alert("✅ Deleted successfully");
      fetchHistory(); // reload
    } else {
      alert("❌ Failed to delete");
    }
  } catch (err) {
    console.error("❌ Delete error:", err);
  }
}

function enableSort() {
  const headers = document.querySelectorAll("#sos-table th.sortable");
  headers.forEach((th, index) => {
    th.addEventListener("click", () => {
      const sorted = [...fullData].sort((a, b) => {
        const va = Object.values(a)[index];
        const vb = Object.values(b)[index];
        return va > vb ? 1 : -1;
      });
      renderTable(sorted);
    });
  });
}

window.onload = () => {
  fetchHistory();
  enableSort();
};
