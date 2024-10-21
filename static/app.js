async function fetchSectorData() {
    try {
        const response = await fetch('http://localhost:5000/api/sector_data');
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        const data = await response.json();
        displayData(data);
    } catch (error) {
        console.error('There has been a problem with your fetch operation:', error);
    }
}

function getRandomColor() {
    const letters = '0123456789ABCDEF';
    let color = '#';
    for (let i = 0; i < 6; i++) {
        color += letters[Math.floor(Math.random() * 16)];
    }
    return color;
}

function displayData(data) {
    const sectorDataDiv = document.getElementById('sector-data');
    sectorDataDiv.innerHTML = ''; // Clear previous data

    const containerWidth = window.innerWidth * 0.8; // Use 80% of the window width
    const containerHeight = window.innerHeight * 0.8; // Use 80% of the window height

    // Array to store bubble positions to prevent overlap
    const bubbles = [];

    for (const [etf, metrics] of Object.entries(data)) {
        const bubble = document.createElement('div');

        // Set the size based on total assets
        const size = Math.max(metrics.total_assets / 4e8, 80); // Increased divisor for larger circles
        const radius = size / 2; // Calculate the radius
        bubble.style.width = `${size}px`;
        bubble.style.height = `${size}px`;
        bubble.style.borderRadius = '50%';
        bubble.style.backgroundColor = getRandomColor(); // Different color for each bubble
        bubble.style.position = 'absolute'; // Use absolute positioning
        bubble.style.textAlign = 'center';
        bubble.style.lineHeight = `${size}px`; // Center the text vertically
        bubble.style.color = 'white'; // Text color

        // Clean the name to ensure only the industry name is shown
        const cleanName = metrics.name.toLowerCase(); // Convert name to lowercase
        bubble.innerText = cleanName; // Display the name

        // Positioning variables
        let positionFound = false;
        let positionX, positionY;

        while (!positionFound) {
            // Calculate a potential position
            positionX = Math.random() * (containerWidth - size);
            positionY = Math.random() * (containerHeight - size);

            // Check if the position is valid (no overlap)
            if (bubbles.every(bubble => {
                const bubbleRect = bubble.getBoundingClientRect();
                const dx = positionX - (bubbleRect.left + radius);
                const dy = positionY - (bubbleRect.top + radius);
                const distance = Math.sqrt(dx * dx + dy * dy);
                return distance >= (radius + bubble.style.width.replace('px', '') / 2); // Ensure circles touch but do not overlap
            })) {
                positionFound = true;
                bubble.style.left = `${positionX}px`;
                bubble.style.top = `${positionY}px`;
                bubbles.push(bubble); // Store the bubble for future overlap checks
            }
        }

        // Create a tooltip
        const tooltip = document.createElement('div');
        tooltip.innerText = `${cleanName.charAt(0).toUpperCase() + cleanName.slice(1)} - Total Assets: $${metrics.total_assets.toLocaleString()}`;
        tooltip.style.position = 'absolute';
        tooltip.style.backgroundColor = 'rgba(0, 0, 0, 0.75)';
        tooltip.style.color = 'white';
        tooltip.style.padding = '5px';
        tooltip.style.borderRadius = '5px';
        tooltip.style.visibility = 'hidden'; // Hidden by default

        // Show tooltip on hover
        bubble.addEventListener('mouseover', (event) => {
            tooltip.style.visibility = 'visible';
            tooltip.style.left = `${event.clientX + 10}px`; // Position slightly right from the cursor
            tooltip.style.top = `${event.clientY + 10}px`; // Position slightly below the cursor
            sectorDataDiv.appendChild(tooltip); // Append tooltip to the main div, not bubble
        });

        bubble.addEventListener('mouseout', () => {
            tooltip.style.visibility = 'hidden';
            sectorDataDiv.removeChild(tooltip); // Remove tooltip from DOM
        });

        sectorDataDiv.appendChild(bubble);
    }
}

// Fetch data when the page loads
document.addEventListener('DOMContentLoaded', fetchSectorData);
