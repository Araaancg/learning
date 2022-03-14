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


    const main_body = document.createElement("div");
    main_body.setAttribute("id","main-body");
    const flash_card = document.createElement("div");
    let content_flashcard = document.createElement("p");
    flash_card.setAttribute("id","flash-card");
    // content_flashcard.innerText = "flash_card";
    content_flashcard.setAttribute("id","content-flashcard");
    flash_card.append(content_flashcard);

    // flash cards
    const btn_next = document.createElement("button");
    btn_next.setAttribute("id","btn-next");
    // btn_next.innerText = "next";
    btn_next.innerText = ">"

    const btn_prev = document.createElement("button");
    btn_prev.setAttribute("id","btn-prev");
    // btn_prev.innerText = "previous"
    btn_prev.innerText = "<"
    
    main_body.append(btn_prev,flash_card,btn_next)
    main.append(main_header,main_body);
    
    aside_1.innerText = "aside_1";
    // aside_2.innerText = "aside_2";

    //// ASIDE 2 ////
    const h3 = document.createElement("h3");
    h3.innerText = "Ajustes";
    // cambiar el lado que se muestra primero
    const switch_side = document.createElement("div");
    const p_1 = document.createElement("p");
    p_1.innerText = "Mostrar primero: ";
    const btn_caraa = document.createElement("button");
    btn_caraa.innerText = "cara A";
    btn_caraa.setAttribute("type","button");
    const btn_carab = document.createElement("button");
    btn_carab.innerText = "cara B";
    btn_carab.setAttribute("type","button");

    btn_caraa.className = "switch-side button-clicked"; // para hacer el css más simple el clicked-button
    btn_carab.className = "switch-side";
    let priority_side = "a";
    btn_caraa.onclick = function() {
        priority_side = "a";
        btn_caraa.classList.add("button-clicked");
        btn_carab.className = "switch-side";
        console.log(priority_side);
    };
    btn_carab.onclick = function() {
        priority_side = "b";
        btn_carab.classList.add("button-clicked");
        btn_caraa.className = "switch-side";
        console.log(priority_side);
    };
    // añadimos un div-start igual que el div-end pero con un botón de start, así puede ajustar los settings antes de empezar
    // por ejemplo el lado o si lo quiere mezclados no (botón de shuffle)
    const div_start = document.createElement("div");
    const btn_start = document.createElement("button");
    btn_start.setAttribute("type","button")
    btn_start.setAttribute("id","btn-start");
    btn_start.innerText = "empezar";
    content_flashcard.style.display = "none";
    div_start.append(btn_start);
    flash_card.append(div_start);

    //botón shuffle
    const btn_shuffle = document.createElement("button");
    btn_shuffle.innerText = "mezclar";
    const div_shuffle = document.createElement("div");
    btn_shuffle.setAttribute("type","button");
    btn_shuffle.setAttribute("id","btn-shuffle")
    div_shuffle.append(btn_shuffle);

    switch_side.append(p_1,btn_caraa,btn_carab);
    aside_2.append(h3,switch_side,div_shuffle);
    body_div.append(aside_1,main,aside_2);
    body.append(body_div);
    
    /////// FLASH CARDS ///////
    // btn_shuffle.onclick = function() {
        
        // };
        
    const end_div = document.createElement("div");
    end_div.setAttribute("id","end-div");
    end_div.style.display = "none";
    const btn_replay = document.createElement("button");
    const btn_chpack = document.createElement("button");
    end_div.append(btn_replay,btn_chpack);
    flash_card.append(end_div);
    
    cards = data.data.packages.cards
    let count = 0;

    $(document).ready(function() {
        $("#btn-start").click(function() {
            console.log("start");
            content_flashcard.style.display = "block"
            div_start.style.display = "none";
            // botón de repetir y de elegir otro paquete que apareceran al final
            btn_replay.setAttribute("id","btn-replay");
            btn_replay.setAttribute("type","button");
            // btn_replay.innerText = "&#8635;"
            btn_replay.innerText = "repetir"
            // btn_replay.style.display = "none";

            btn_chpack.setAttribute("id","btn-chpack");
            btn_chpack.setAttribute("type","button");
            btn_chpack.innerText = "cambiar paquete";
            // btn_chpack.style.display = "none";
            let replay_side = priority_side;
            btn_replay.onclick = function() {
                count = 0;
                content_flashcard.style.display = "block"
                // flash_card.style.opacity = 1;
                // replay_side = "b";
                replay_side = priority_side == "a"? "b":"a";
                content_flashcard.innerText = cards[0].side_a;
                end_div.style.display = "none"
                btn_prev.style.opacity = 0;
                btn_next.style.opacity = 1;
            };
            
            btn_chpack.onclick = function() {
                window.location.assign("http://localhost:5000/flash_cards") //prev url
            };

            // content_flashcard.innerText = cards[0].side_a;
            content_flashcard.innerText = priority_side === "a"? cards[0].side_a:cards[0].side_b;
            btn_prev.style.opacity = 0;

            let current_side = replay_side === "a" ? "a":"b";
            $("#flash-card").click(async function(){
                if (current_side == "a") {
                    content_flashcard.innerText = cards[count].side_b;
                    current_side = "b";
                }
                else {
                    content_flashcard.innerText = cards[count].side_a;
                    current_side = "a";
                };
            });
            $("#btn-next").click(function(){
                count += 1;
                btn_prev.style.opacity = count >= 0? 1:0;
                if (count < cards.length) {
                    content_flashcard.innerText = priority_side === "a"? cards[count].side_a:cards[count].side_b;
                }
                else {
                    content_flashcard.style.display = "none"
                    end_div.style.display = "block";
                    btn_next.style.opacity = 0;
                };
            });
            $("#btn-prev").click(function(){
                count -= 1;
                btn_next.style.opacity = count == cards.length? 0:1;
                if (count >= 0){
                    content_flashcard.innerText = priority_side === "a"? cards[count].side_a:cards[count].side_b;
                    btn_prev.style.opacity = count == 0? 0:1;
                    end_div.style.display = count < cards.length ? "none":"block";
                    content_flashcard.style.display = count < cards.length ? "block":"none"
                }
                else {
                    count += 1;
                };
            });
            $("#btn-shuffle").click(function(){
                cards = cards.sort((a, b) => 0.5 - Math.random());
                count = 0
                div_start.style.display = "block";
                content_flashcard.style.display = "none";
            });
        });
    });
};
