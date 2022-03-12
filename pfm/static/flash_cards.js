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
    aside_2.append(h3)
    
    body_div.append(aside_1,main,aside_2);
    body.append(body_div);
    
    /////// FLASH CARDS ///////
    not_shuffled = data.data.packages.cards
    cards = not_shuffled.sort((a, b) => 0.5 - Math.random());
    
    const end_div = document.createElement("div");
    end_div.setAttribute("id","end-div");
    end_div.style.display = "none"
    $(document).ready(function() {
        // botón de repetir y de elegir otro paquete que apareceran al final
        const btn_replay = document.createElement("button");
        btn_replay.setAttribute("id","btn-replay");
        btn_replay.setAttribute("type","button");
        // btn_replay.innerText = "&#8635;"
        btn_replay.innerText = "repetir"
        // btn_replay.style.display = "none";

        const btn_chpack = document.createElement("button");
        btn_chpack.setAttribute("id","btn-chpack");
        btn_chpack.setAttribute("type","button");
        btn_chpack.innerText = "cambiar paquete";
        // btn_chpack.style.display = "none";
        let replay_side = null
        btn_replay.onclick = function() {
            count = 0;
            content_flashcard.style.display = "block"
            // flash_card.style.opacity = 1;
            replay_side = "b";
            content_flashcard.innerText = cards[0].side_a;
            end_div.style.display = "none"
            btn_prev.style.opacity = 0;
            btn_next.style.opacity = 1;
        };
        
        btn_chpack.onclick = function() {
            window.location.assign("http://localhost:5000/flash_cards") //prev url
        };
        end_div.append(btn_replay,btn_chpack);
        flash_card.append(end_div);

        

        
        content_flashcard.innerText = cards[0].side_a;
        let count = 0;
        btn_prev.style.opacity = 0;

        let current_side = replay_side == "a" ? "a":"b";
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
                content_flashcard.innerText = cards[count].side_a;
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
                content_flashcard.innerText = cards[count].side_a;
                btn_prev.style.opacity = count == 0? 0:1;
                end_div.style.display = count < cards.length ? "none":"block";
                content_flashcard.style.display = count < cards.length ? "block":"none"
            }
            else {
                count += 1;
            };
        });
    });
};
