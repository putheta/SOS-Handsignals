// static/js/myarea.js
let areaMap = null;

function initAreaMap() {
  const mapContainer = document.getElementById("area-map");
  if (!mapContainer || mapContainer._leaflet_id) return;

  setTimeout(() => {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const lat = position.coords.latitude;
      const lng = position.coords.longitude;

      areaMap = L.map("area-map").setView([lat, lng], 14);
      L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
        attribution: '&copy; OpenStreetMap contributors',
      }).addTo(areaMap);

      // 🔵 My Location
      L.circleMarker([lat, lng], {
        radius: 8,
        color: "blue",
        fillColor: "blue",
        fillOpacity: 0.9,
      }).addTo(areaMap).bindPopup("🧍‍♀️ You are here");

      // ✅ SOS จุดต่าง ๆ จาก API
      const sosRes = await fetch("/api/sos");
      const sosData = await sosRes.json();
      sosData.forEach(item => {
        if (item.latitude && item.longitude) {
          let color = "gray";
          if (item.source === "camera") color = "red";
          else if (item.source === "user") color = "orange";
          else if (item.source === "observer") color = "blue";

          L.circleMarker([item.latitude, item.longitude], {
            radius: 8,
            color,
            fillColor: color,
            fillOpacity: 0.9,
          }).addTo(areaMap).bindPopup(`📍 ${item.source?.toUpperCase() || "UNKNOWN"}<br/>${item.location || "-"}<br/>${item.timestamp || ""}`);
        }
      });

      // 🟢 Overpass API: Police Stations (within ~3km)
      const delta = 0.03;
      const latMin = lat - delta, latMax = lat + delta;
      const lngMin = lng - delta, lngMax = lng + delta;
      const query = `[out:json];node["amenity"="police"](${latMin},${lngMin},${latMax},${lngMax});out body;`;
      const url = `https://overpass-api.de/api/interpreter?data=${encodeURIComponent(query)}`;

      const policeRes = await fetch(url);
      const policeData = await policeRes.json();
      policeData.elements.forEach(p => {
        L.circleMarker([p.lat, p.lon], {
          radius: 8,
          color: "green",
          fillColor: "green",
          fillOpacity: 0.9,
        }).addTo(areaMap).bindPopup("👮 Police Station");
      });

      // ✅ Add legend to map
      const legend = L.control({ position: "bottomright" });
      legend.onAdd = function () {
        const div = L.DomUtil.create("div", "info legend");
        div.innerHTML += `
          <div style="background: white; padding: 10px; border-radius: 8px;">
            <strong>🗺️ Legend</strong><br/>
            <span style="color: red;">●</span> AI Camera SOS<br/>
            <span style="color: orange;">●</span> User Triggered SOS<br/>
            <span style="color: blue;">●</span> Observer Report<br/>
            <span style="color: green;">●</span> Police Station<br/>
            <span style="color: gray;">●</span> Unknown
          </div>
        `;
        return div;
      };
      legend.addTo(areaMap);
    });
  }, 100);
}
