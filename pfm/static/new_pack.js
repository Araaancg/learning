window.onload = async function() {

    const res = await fetch(`http://localhost:5000/my_packages/create_new?get=categories`);
    const cat_list = await res.json();
    console.log(cat_list);

    const main = document.querySelector("#main");
    const form = document.createElement("form");

    const div_name = document.createElement("div_name");
    const input_name = document.createElement("input");
    const label_name = document.createElement("label");
    label_name.innerText = "name";

    label_name.setAttribute("for", "name");

    input_name.setAttribute("id", "name");
    input_name.setAttribute("required", true);
    input_name.setAttribute("name","pack_name")
    input_name.setAttribute("type","text")

    div_name.append(label_name);
    div_name.append(input_name);
    div_name.className = "name-input";

    const div_category = document.createElement("div");
    div_category.className = "categories";

    const label_cat = document.createElement("label");
    const input_cat = document.createElement("input");

    label_cat.setAttribute("for","category");
    label_cat.innerText = "Category"
    input_cat.setAttribute("id","category");
    input_cat.setAttribute("name","category")
    div_category.append(label_cat)
    div_category.append(input_cat)

    const div_existing_categories = document.createElement("div");
    div_existing_categories.className = "existing-categories";

    for (let category of cat_list["categories"]) {
        const btn_category = document.createElement("span");
        btn_category.setAttribute("type","button");
        btn_category.innerText = category["name"];
        btn_category.className = "cat-name";
        div_existing_categories.append(btn_category);

        btn_category.style.width = "fit-content";
        btn_category.style.height = "fit-content";
        btn_category.style.padding = "3px";
        btn_category.style.border = "1px solid #000";

        btn_category.onclick = function() {
            console.log(category);
            input_cat.setAttribute("value",category["name"])
        };
    };

    div_category.append(div_existing_categories);

    const div_cards = document.createElement("div");
    div_cards.className = "cards";
    let count = 1
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

    const btn_submit = document.createElement("button");
    btn_submit.setAttribute("type","button");
    btn_submit.innerText = "Submit"
    btn_submit.onclick = async function() {
        const submit_form = new FormData();
        for (let elem of form) {
            if (elem.value) {
                submit_form.append(elem.name, elem.value);
            };
        };
        console.log(submit_form)
        await fetch(`http://localhost:5000/my_packages/create_new`, {
            method: "POST",
            body: submit_form
        });
        console.log("Works");
        window.location.assign("http://localhost:5000/my_packages");
    };
    
    
    form.append(div_name);
    form.append(div_category);
    form.append(div_cards);
    form.append(btn_card);
    form.append(btn_submit);
    main.append(form);

    
};

