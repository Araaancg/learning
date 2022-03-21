window.onload = async function() {
    res = await fetch(`http://localhost:5000/flash_cards`, {
        method:"POST"
    });
    const data = await res.json();

    console.log(data);

    const main = document.querySelector("#main");
    const main_div = document.createElement("div");
    main_div.className = "packages";

    for (pack of data.packages) {
        const sub_div = document.createElement("div");
        sub_div.className = "single-package"
        sub_div.setAttribute("id",pack.id);
        const a = document.createElement("a");
        a.href = `http://localhost:5000/flash_cards/${pack.name}`
        const h2 = document.createElement("h2");
        h2.innerText = pack.name

        a.append(h2)

        const span_cat = document.createElement("span");
        span_cat.innerText = `Categoria: ${pack.category.name}`

        const btn_cards = document.createElement("button");
        btn_cards.innerText = "tarjetas";
        sub_div.append(a);

        const table = document.createElement("table");
        const thead = document.createElement("thead");
        const tbody = document.createElement("tbody");

        const th_a = document.createElement("th");
        const th_b = document.createElement("th");
        th_a.innerText = "Cara A";
        th_b.innerText = "Cara B";
        thead.append(th_a,th_b)
        
        let number_cards = 0;

        for (card of pack.cards) {
            const tr = document.createElement("tr");
            const td_a = document.createElement("td");
            td_a.innerText = card.side_a;
            const td_b = document.createElement("td");
            td_b.innerText = card.side_b;
            tr.append(td_a,td_b);
            tbody.append(tr);
            number_cards += 1
        };
        const number_span = document.createElement("span");
        number_span.innerText = `Nº tarjetas: ${number_cards}`;
        const info_pack = document.createElement("div");
        info_pack.className = "info-pack";
        info_pack.append(number_span,span_cat);
        sub_div.append(info_pack,btn_cards);
        table.append(thead,tbody);
        sub_div.append(table);
        table.style.display = "none";

        btn_cards.onclick = function() {
            if (table.style.display !== "none") {
                table.style.display = "none";
            }
            else {
                table.style.display = "block";
            };
        };
            main_div.append(sub_div);
            main.append(main_div);
    };
};