frappe.ui.form.on('MapWise Plot Details', {
    refresh: function(frm) {
        // Create a div for the map if it doesn't exist
        if (!frm.fields_dict.map_html.$wrapper.find('#map').length) {
            frm.fields_dict.map_html.$wrapper.html(`
                <div id="map" style="height: 400px; width: 100%;"></div>
                <button id="fetch-locations" class="btn btn-primary" style="margin-top: 10px;">Show Plots</button>
                <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
                <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>
            `);
        }

        // Initialize Map only once
        if (!window.myMap) {
            setTimeout(() => {
                window.myMap = L.map('map').setView([16.5377785, 74.6595871], 12);
                L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                    attribution: '&copy; OpenStreetMap contributors'
                }).addTo(window.myMap);

                window.markersLayer = L.layerGroup().addTo(window.myMap); // Layer group for markers
            }, 500);
        }

        // Flag to check if circle_office value has changed
        let circleOfficeChanged = false;

        // Set flag when circle_office is changed
        frm.fields_dict.circle_office.$input.off('change').on('change', function () {
            circleOfficeChanged = true;
        });

        // Add click event to fetch locations only if circle_office value has changed
        frm.fields_dict.map_html.$wrapper.find('#fetch-locations').off('click').on('click', async function () {
            if (frm.fields_dict.circle_office.$input.val()) {
                if (circleOfficeChanged) {
                    await fetchLocations(frm);
                    circleOfficeChanged = false; // Reset flag after fetching locations
                } else {
                    frappe.msgprint(__('Circle Office value has not changed.'));
                }
            } else {
                frappe.msgprint(__('Please select a Circle Office first.'));
            }
        });
    }
});

// Function to fetch and plot markers on the map
async function fetchLocations(frm) {
    frappe.msgprint(__('Fetching plot locations...'));

    try {
        const r = await frm.call({
            method: 'plot_data',  // Frappe backend method
            doc: frm.doc
        });

        if (r.message && r.message.length > 0) {
            updateMapWithNewLocations(r.message);
            frappe.msgprint(__('Plot locations updated on the map!'));
        } else {
            frappe.msgprint(__('No locations found.'));
        }
    } catch (error) {
        frappe.msgprint(__('Error fetching plot locations.'));
        console.error(error);
    }
}

// Function to get marker icon based on plantation_status
function getMarkerIcon(status) {
    let color;
    switch (status) {
        case "New":
            color = "green";
            break;
        case "To Harvesting":
        case "To Sampling":
        case "Added To Harvesting":
        case "Added To Sampling":
            color = "yellow";
            break;
        case "Harvested":
            color = "red";
            break;
        default:
            color = "blue"; // Default color if status is unknown
    }

    return L.icon({
        iconUrl: `https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-${color}.png`,
        shadowUrl: "https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png",
        iconSize: [25, 41],
        iconAnchor: [12, 41],
        popupAnchor: [1, -34],
        shadowSize: [41, 41]
    });
}

// Function to update the map with new locations
function updateMapWithNewLocations(locations) {
    // Clear all existing markers
    window.markersLayer.clearLayers();

    locations.forEach(location => {
        var marker = L.marker(
            [parseFloat(location.latitude), parseFloat(location.longitude)],
            { icon: getMarkerIcon(location.plantation_status) }
        ).addTo(window.markersLayer);

        marker.bindPopup(`
            <b>Plot No:</b> ${location.plot_no ?? "N/A"}<br>
            <b>Status:</b> ${location.plantation_status ?? "N/A"}<br>
            <b>Grower Code:</b> ${location.grower_code ?? "N/A"}<br>
            <b>Grower Name:</b> ${location.grower_name ?? "N/A"}<br>
            <b>Route Name:</b> ${location.route_name ?? "N/A"}
        `);
    });
}
