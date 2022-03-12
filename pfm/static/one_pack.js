window.onload = async function() {
    const uri = window.location.href;
    const pack_name = uri.split("/")[uri.split("/").length - 1];
    console.log(pack_name);
    const res = await fetch(`http://localhost:5000/my_packages/${pack_name}`, {
        method:"POST"
    });
    const data = await res.json();
    console.log(data)

    const main = document.querySelector("#main");

    //header
    const div_header = document.createElement("section");
    div_header.setAttribute("id","pack_header");
    div_header.className = "main-parts";
    const h1 = document.createElement("h1");
    h1.innerText = data["data"]["packages"].name;
    const cat_span = document.createElement("span");
    cat_span.innerText = `Categoría: ${data.data.packages.category.name}`;

    //body
    const div_body = document.createElement("section");
    div_body.setAttribute("id","pack_body");
    div_body.className = "main-parts"
    const h2 = document.createElement("h2");
    h2.innerText = "Tarjetas";
    const h3_a = document.createElement("h3");
    h3_a.innerText = "Cara A";
    const h3_b = document.createElement("h3");
    h3_b.innerText = "Cara B";

    let number_cards = 0;

    div_body.append(h2,h3_a,h3_b);
    // tarjetas
    for (let card of data.data.packages.cards) {
        const section_card = document.createElement("section");
        section_card.setAttribute("id",card.id);
        section_card.className = "cards";
        // const span_a = document.createElement("span");
        // span_a.innerText = card.side_a;
        // const span_b = document.createElement("span");
        // span_b.innerText = card.side_b;
        // section_card.append(span_a,span_b);
        const s_cards_left = document.createElement("div");
        const card_a = document.createElement("div");
        const card_b = document.createElement("div");
        card_a.className = "left card_a";
        card_b.className = "left card_b";
        s_cards_left.className = "cards left";
        const content_a = document.createElement("p");
        content_a.innerText = card.side_a;
        const content_b = document.createElement("p");
        content_b.innerText = card.side_b;
        card_a.append(content_a);
        card_b.append(content_b);
        s_cards_left.append(card_a,card_b);

        //hid div to edit
        const edit_div = document.createElement("div");
        edit_div.className = "edit-div";

        const editing_form = document.createElement("form");
        const einput_a = document.createElement("input");
        const einput_b = document.createElement("input");
        //input side_a
        einput_a.setAttribute("id","side_a");
        einput_a.setAttribute("type","text");
        einput_a.setAttribute("name","side_a");
        einput_a.setAttribute("placeholder","cara a");
        //input side_b
        einput_b.setAttribute("id","side_b");
        einput_b.setAttribute("type","text");
        einput_b.setAttribute("name","side_b");
        einput_b.setAttribute("placeholder","cara b");        
        
        //button for deleting card
        const btn_delete = document.createElement("button");
        btn_delete.innerText = "x";
        btn_delete.className = "btn-delete-card";
        btn_delete.setAttribute("type","button");
        const delete_form = new FormData();
        delete_form.append("card_id",card.id);
        btn_delete.onclick = async function() {
            await fetch(`http://localhost:5000/my_packages/${data.data.packages.name}?delete_card=${card.id}`);
            window.location.reload();
        };
        
        //button for editing
        const btn_edit = document.createElement("button");
        btn_edit.setAttribute("type","button");
        btn_edit.className = "btn-edit-card";
        btn_edit.innerText = "editar";
        btn_edit.onclick = function() {
            if (edit_div.style.display !== "none") {
                edit_div.style.display = "none";
            }
            else {
                edit_div.style.display = "block";
            };
        };
        //button saving what's edited
        const btn_save = document.createElement("button");
        btn_save.setAttribute("type","button");
        btn_save.innerText = "guardar";
        editing_form.append(einput_a,einput_b,btn_save);
        edit_div.append(editing_form);
        edit_div.style.display = "none";
        btn_save.onclick = async function() {
            const form = new FormData(editing_form);
            await fetch(`http://localhost:5000/my_packages/${data.data.packages.name}?edit_card=${card.id}`, {
                method:"PUT",
                body:form
            });
            window.location.reload();
        };
        const s_cards_right = document.createElement("div");
        s_cards_right.className = "cards right";
        s_cards_right.append(btn_edit,btn_delete);
        s_cards_left.append(edit_div);
        section_card.append(s_cards_left,s_cards_right);
        div_body.append(section_card);
        number_cards += 1;
    };

    const div_new_cards = document.createElement("div");
    div_new_cards.className = "new-card";
    const form_new_cards = document.createElement("form");
    div_new_cards.append(form_new_cards);
    const btn_save_new_cards = document.createElement("button");
    btn_save_new_cards.setAttribute("type","button");
    btn_save_new_cards.innerText = "guardar";
    btn_save_new_cards.style.display = "none";

    //footer
    const div_footer = document.createElement("section");
    div_footer.setAttribute("id","pack_footer");
    // delete pack
    const btn_delete_pack = document.createElement("button");
    btn_delete_pack.setAttribute("type","button");
    btn_delete_pack.setAttribute("id","btn-delete-pack")
    btn_delete_pack.innerText = "eliminar paquete";
    btn_delete_pack.onclick = async function() {
        confirmation = confirm("el paquete se eliminará de la base de datos");
        if (confirmation) {
            await fetch(`http://localhost:5000/my_packages/${data.data.packages.name}?delete_pack=${data.data.packages.id}`);
            window.location.assign("http://localhost:5000/my_packages");
            console.log("paquete eliminardo");
        }
        else {
            console.log("acción cancelada");
        };
    };
    // add new cards
    const btn_add_cards = document.createElement("button");
    btn_add_cards.setAttribute("type","button");
    btn_add_cards.setAttribute("id","btn-add-cards");
    btn_add_cards.innerText = "+";
    let count_new_cards = 1;
    btn_add_cards.onclick = function() {
        console.log("button used");
        btn_save_new_cards.style.display = "block";
        const new_side_a = document.createElement("input");
        new_side_a.setAttribute("placeholder","cara a");
        new_side_a.setAttribute("name",`side_a_${count_new_cards}`)
        new_side_a.className = "new-card";
        const new_side_b = document.createElement("input");
        new_side_b.setAttribute("placeholder","cara b");
        new_side_b.setAttribute("name",`side_b_${count_new_cards}`)
        new_side_b.className = "new-card";
        const single_newcard_div = document.createElement("div");
        single_newcard_div.append(new_side_a,new_side_b);
        form_new_cards.append(single_newcard_div);
        div_body.append(div_new_cards);
        count_new_cards += 1;
    };

    //add function btn save new cards
    btn_save_new_cards.onclick = async function() {
        const form = new FormData(form_new_cards);
        await fetch(`http://localhost:5000/my_packages/${data.data.packages.name}?new_card=${data.data.packages.id}`, {
            method:"PUT",
            body:form
        });
        window.location.reload()
        console.log("cards added");
    };

    div_new_cards.append(btn_save_new_cards)
    div_footer.append(btn_add_cards,btn_delete_pack);

    const hr = document.createElement("hr");

    const nc_span = document.createElement("span");
    nc_span.innerText = `Nº tarjetas: ${number_cards}`;
    div_header.append(h1,cat_span,nc_span);
    main.append(div_header,hr,div_body,div_footer);
};