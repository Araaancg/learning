
async function dea_finder() {
    window.navigator.geolocation.getCurrentPosition((coords) => {
        const lat = coords.coords.latitude
        const lon = coords.coords.longitude
        fetch(`http://localhost:5000/dea/finder?lat=${lat}&lon=${lon}`, {
            method:"POST"
        });
        console.log(lat,lon);
});
};

