window.onload = async function() {
    const uri = window.location.href;
    const pack_name = uri.split("/")[uri.split("/").length - 1];

    const res = await fetch(`http://localhost:5000/my_packages/${pack_name}`, {method:"POST"});
    const data = await res.json();
    console.log(data);

    const body = document.querySelector("body");
    const body_div = document.createElement("div");
    body_div.setAttribute("id","body-div")
    const aside_1 = document.createElement("aside");
    const aside_2 = document.createElement("aside");
    const main = document.createElement("main");

    // divs para distribuir los elementos en tres columnas
    aside_1.className = "box";
    aside_2.className = "box";
    main.className = "box"; 
    aside_2.setAttribute("id","aside_2");
    aside_1.setAttribute("id","aside_1");
    main.setAttribute("id","main");

    //MAIN. donde estarán las flash cards
    const main_header = document.createElement("div");
    main_header.setAttribute("id","main-header");
    const h2 = document.createElement("h2");
    const hr = document.createElement("hr");
    h2.innerText = pack_name;
    main_header.append(h2,hr); //will include category, number of cards...

    const flash_card = document.createElement("div");
    const content_flashcard = document.createElement("p");
    flash_card.setAttribute("id","flash_card");
    content_flashcard.innerText = "flash_card";
    content_flashcard.setAttribute("id","content-flashcard");
    flash_card.append(content_flashcard);

    // flash cards
    const btn_next = document.createElement("button");
    btn_next.setAttribute("next","button");
    btn_next.innerText = "next";

    let change_side = false
    let change_card = true
    
    function ClickToChange(variab) {
        variab = true
        console.log("side_changed")
    };

    for (let card of data.data.packages.cards) {
        content_flashcard.innerText = card.side_a
        flash_card.addEventListener("click",ClickToChange(change_side))
        if (change_side == true) {
            content_flashcard.innerText = card.side_b
        };
    };




    main.append(main_header,flash_card,btn_next);
    
    
    
    
    /////////////////////////////////////
    aside_1.innerText = "aside_1";
    aside_2.innerText = "aside_2";
    
    body_div.append(aside_1,main,aside_2);
    body.append(body_div);
    
};