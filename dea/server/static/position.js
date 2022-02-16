
// async function dea_finder() {
//     window.navigator.geolocation.getCurrentPosition((coords) => {
//         const lat = coords.coords.latitude
//         const lon = coords.coords.longitude
//         fetch(`http://localhost:5000/dea/finder?lat=${lat}&lon=${lon}`, {
//             method:"POST"
//         });
//         // console.log(lat,lon);

//         //CARDS
        
//     });
// };


window.navigator.geolocation.getCurrentPosition((coords) => {
    const lat = coords.coords.latitude
    const lon = coords.coords.longitude
    fetch(`http://localhost:5000/dea/finder?lat=${lat}&lon=${lon}`, {
        method:"POST"
    });
    // console.log(lat,lon);

    //CARDS
    const card = document.createElement("div");
    const img = document.createElement("img");
    const card_body = document.createElement("div");
    const card_title = document.createElement("h5");
    const card_text = document.createElement("p");
    const btn = document.createElement("a");
    const main = document.querySelector("#main");

    card_title.innerText = "hola";

    card_body.append(card_title);
    card_body.append(card_text);
    card_body.append(btn);
    card.append(img);
    card.append(card_body);
    main.append(card);
});

