window.onload = async function() {

    const res = await fetch(`http://localhost:5000/my_packages/create_new?get=categories`);
    const cat_list = await res.json();
    console.log(cat_list);

    const main = document.querySelector("#main");
    const form = document.createElement("form");

    const div_name = document.createElement("div");
    const input_name = document.createElement("input");
    const label_name = document.createElement("label");
    label_name.innerText = "Nombre";

    label_name.setAttribute("for", "name");

    input_name.setAttribute("id", "name");
    input_name.setAttribute("required", true);
    input_name.setAttribute("name","pack_name");
    input_name.setAttribute("type","text");
    input_name.style.overflow = "auto"

    div_name.append(label_name);
    div_name.append(input_name);
    div_name.className = "left-div";
    div_name.setAttribute("id","name-input")

    const div_category = document.createElement("div");
    div_category.className = "left-div";
    div_category.setAttribute("id","category-input");

    const label_cat = document.createElement("label");
    const input_cat = document.createElement("input");

    label_cat.setAttribute("for","category");
    label_cat.innerText = "Categoría"
    input_cat.setAttribute("id","category");
    input_cat.setAttribute("name","category")
    div_category.append(label_cat)
    div_category.append(input_cat)

    const div_existing_categories = document.createElement("div");
    div_existing_categories.className = "existing-categories";

    if (cat_list.categories[1].private.length > 0) {
        const div_private_categories = document.createElement("div");
        div_private_categories.className = "existing-categories";
        div_private_categories.setAttribute("id","private-categories")
        for (let category of cat_list.categories[1].private) {
            const btn_category = document.createElement("button");
            btn_category.setAttribute("type","button");
            btn_category.innerText = category["name"];
            btn_category.className = "cat-name";
            div_private_categories.append(btn_category);
    
            btn_category.onclick = function() {
                console.log(category);
                input_cat.setAttribute("value",category["name"])
            };
        };
        const hr = document.createElement("hr");
        div_existing_categories.append(div_private_categories,hr);
    };


    for (let category of cat_list.categories[0].public) {
        const btn_category = document.createElement("button");
        btn_category.setAttribute("type","button");
        btn_category.innerText = category["name"];
        btn_category.className = "cat-name";
        div_existing_categories.append(btn_category);

        btn_category.onclick = function() {
            console.log(category);
            btn_category.style.border_color = "#dd7596";
            input_cat.setAttribute("value",category["name"])
        };
    };

    div_category.append(div_existing_categories);

    const h2 = document.createElement("h2");
    h2.innerText = "Tarjetas"
    const div_cards = document.createElement("div");
    div_cards.className = "cards";
    let count = 1
    while (count < 6) {
        const single_card_div = document.createElement("div");
        single_card_div.setAttribute("id",`card_${count}`);
        const input_a = document.createElement("input");
        input_a.setAttribute("placeholder","cara a");
        input_a.setAttribute("name",`side_a_${count}`);
        const input_b = document.createElement("input");
        input_b.setAttribute("placeholder","cara b");
        input_b.setAttribute("name",`side_b_${count}`);
        single_card_div.append(input_a,input_b);
        div_cards.append(single_card_div);
        count += 1;
    };
    const btn_card = document.createElement("button");
    btn_card.setAttribute("type","button");
    btn_card.setAttribute("id","btn-more-cards");
    btn_card.innerText = "añadir tarjeta";
    console.log(count);
    btn_card.onclick = function() {
        const single_card_div = document.createElement("div");
        single_card_div.setAttribute("id",`card_${count}`);
        const input_a = document.createElement("input");
        input_a.setAttribute("placeholder","side_a");
        input_a.setAttribute("name",`side_a_${count}`);
        const input_b = document.createElement("input");
        input_b.setAttribute("placeholder","side_b");
        input_b.setAttribute("name",`side_b_${count}`);
        single_card_div.append(input_a,input_b);
        div_cards.append(single_card_div);
        count += 1;
    };

    const div_status = document.createElement("div");
    div_status.className = "left-div";
    div_status.setAttribute("id","status-input");
    const div_status_btn = document.createElement("div");
    div_status_btn.setAttribute("id","status-input-btn");
    const btn_public = document.createElement("button");
    btn_public.className = "btn-status"
    btn_public.setAttribute("id","btn-public");
    btn_public.setAttribute("type","button");
    btn_public.innerText = "público";
    let status_value = null;
    btn_public.onclick = function() {
        status_value = "public";
        console.log(status_value);
        btn_private.className = "btn-status";
        btn_public.classList.add("btn-clicked");
    };
    const btn_private = document.createElement("button");
    btn_private.className = "btn-status"
    btn_private.setAttribute("id","btn-private");
    btn_private.setAttribute("type","button");
    btn_private.innerText = "privado";
    btn_private.onclick = function() {
        status_value = "private";
        console.log(status_value);
        btn_public.className = "btn-status";
        btn_private.classList.add("btn-clicked");
    };
    const status_span = document.createElement("span")
    status_span.innerText = "Status";
    div_status_btn.append(btn_public,btn_private);
    div_status.append(status_span,div_status_btn);

    const btn_submit = document.createElement("button");
    btn_submit.setAttribute("id","btn-submit")
    btn_submit.setAttribute("type","button");
    btn_submit.innerText = "Crear"
    btn_submit.onclick = async function() {
        const submit_form = new FormData();
        for (let elem of form) {
            if (elem.value) {
                submit_form.append(elem.name, elem.value);
            };
        };
        submit_form.append("status",status_value);
        console.log(submit_form)
        await fetch(`http://localhost:5000/my_packages/create_new`, {
            method: "POST",
            body: submit_form
        });
        console.log("Works");
        window.location.assign("http://localhost:5000/my_packages");
    };
    
    const left_div = document.createElement("section");
    left_div.setAttribute("id","left-section")
    const right_div = document.createElement("section");
    right_div.setAttribute("id","right-section")
    const btn_div = document.createElement("section");
    btn_div.setAttribute("id","down-section")
    
    left_div.append(div_name, div_category,div_status);
    right_div.append(h2,div_cards,btn_card);
    btn_div.append(btn_submit);
    form.append(left_div,right_div)
    main.append(form,btn_div);

    
};

