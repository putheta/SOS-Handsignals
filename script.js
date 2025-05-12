let map;
let marker;

function sendSOS() {
  const spinner = document.getElementById("spinner");
  spinner.style.display = "block";

  if (navigator.geolocation) {
    navigator.geolocation.getCurrentPosition(async position => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      let location = "Unknown";
      try {
        const res = await fetch(`https://nominatim.openstreetmap.org/reverse?format=jsonv2&lat=${lat}&lon=${lng}`);
        const data = await res.json();
        location = data.display_name || "Unknown";
      } catch (err) {
        console.error("❌ ไม่สามารถดึงชื่อสถานที่ได้:", err);
      }

      const payload = {
        prediction: "sos",
        confidence: 0.97,
        timestamp: new Date().toISOString(),
        location: location,
        latitude: lat,
        longitude: lng,
        image_url: "https://example.com/sample.jpg"
      };

      fetch("/api/sos", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
      })
      .then(async res => {
        if (!res.ok) {
          const errorText = await res.text();
          throw new Error(`Server Error: ${res.status} - ${errorText}`);
        }
      
        const data = await res.json();
        alert("✅ SOS sent!");
        showLatest(payload);
      })
      .catch(err => {
        alert("❌ เกิดข้อผิดพลาดขณะส่ง SOS");
        console.error("Error:", err.message || err);
      })
      .finally(() => {
        spinner.style.display = "none";
      });
      
    }, () => {
      alert("❌ ไม่สามารถดึงตำแหน่งของคุณได้");
      spinner.style.display = "none";
    });
  } else {
    alert("❌ เบราว์เซอร์ของคุณไม่รองรับการระบุตำแหน่ง");
    spinner.style.display = "none";
  }
}

function showLatest(data) {
  const container = document.getElementById("latest-sos");

  const lat = data.latitude ? data.latitude.toFixed(5) : "N/A";
  const lng = data.longitude ? data.longitude.toFixed(5) : "N/A";

  container.innerHTML = `
    <p><strong>Time:</strong> ${new Date(data.timestamp).toLocaleString()}</p>
    <p><strong>Location:</strong> ${data.location}</p>
    <p><strong>Coordinates:</strong> Lat: ${lat}, Lng: ${lng}</p>
    <p><strong>Confidence:</strong> ${data.confidence}</p>
    <p><a href="${data.image_url}" target="_blank">View Image</a></p>
  `;

  if (!map) {
    map = L.map('map').setView([data.latitude, data.longitude], 15);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      attribution: '© OpenStreetMap contributors'
    }).addTo(map);

    marker = L.marker([data.latitude, data.longitude]).addTo(map);
  } else {
    map.setView([data.latitude, data.longitude], 15);
    marker.setLatLng([data.latitude, data.longitude]);
  }
}
