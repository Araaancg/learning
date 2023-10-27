    window.navigator.geolocation.getCurrentPosition(async (coords) => {
        const lat = coords.coords.latitude;
        const lon = coords.coords.longitude;
        const res = await fetch(`http://localhost:5000/dea/finder?lat=${lat}&lon=${lon}`, {
            method : "POST"
        });
        const data = await res.json();
        console.log(data);

        // CARDS

        for (let dea of data["data"]) {
            // create elements
            const card = document.createElement("div");
            // const img = document.createElement("img");
            const card_body = document.createElement("div");
            const card_title = document.createElement("h5");
            const card_text = document.createElement("p");
            const btn = document.createElement("a");
            const total_dea = document.createElement("div");
            const main = document.querySelector("#main");

            const iframe = document.createElement("iframe");

            card_title.innerText = `${dea.address}. `;
            card_text.innerText = `A ${Math.round(dea.distance)} metros`
            card_text.innerText += `\n${dea.name}`;
            btn.innerText = "MAPS";
            btn.href = `https://www.google.com/maps/dir/${lat},${lon}/${dea.latlon[0]},${dea.latlon[1]}`;
            btn.target = "_blank";
            
            iframe.id = "iframe";
            iframe.width = 300;
            iframe.height = 225;
            const dif_lat = 0.002425;
            const dif_lon = 0.000334;
            iframe.src = `https://www.openstreetmap.org/export/embed.html?bbox=${dea.latlon[1]-dif_lon}%2C${dea.latlon[0]-dif_lat}%2C${dea.latlon[1]+dif_lon}%2C${dea.latlon[0]+dif_lat}&amp;layer=mapnik&amp;marker=${dea.latlon[0]}%2C${dea.latlon[1]}`;
            // ;marker=${dea.latlon[0]}%2C${dea.latlon[1]

            
            // bootstrap classes
            card.className = "card custome-container container";
            iframe.className = "card-img-top";
            card_body.className = "card-body text-center";
            card_title.className = "card-title text-center";
            card_text.className = "card-text text-center";
            btn.className = "btn btn-success";
        
            // finish the structure
            card_body.append(card_title);
            card_body.append(card_text);
            card_body.append(btn);
            card.append(iframe);
            card.append(card_body);
            // total_dea.append(card);
            // total_dea.append(iframe);
            // main.append(total_dea);
            main.append(card)
        };

    });


