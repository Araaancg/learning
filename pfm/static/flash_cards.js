window.onload = async function() {
    const uri = window.location.href;
    const pack_name = uri.split("/")[uri.split("/").length - 1];

    const res = await fetch(`http://localhost:5000/my_packages/${pack_name}`, {method:"POST"});
    const data = await res.json();
    console.log(data);

    // elementos principales. Esquema
    // body > h1 + main. Main > left_aside, center_div, right_aside.
    // left and right aside for settings and tools. Center_div used for the flashcard + nav buttons 
    const body = document.querySelector("body");
    const main = document.createElement("main"); 
    const aside_left = document.createElement("aside");
    const center_div = document.createElement("div");
    const aside_right = document.createElement("aside");

    main.id = "main";
    aside_left.id = "aside-left";
    aside_right.id = "aside-right";
    center_div.id = "center-div";

    aside_left.className = "main-elements";
    aside_right.className = "main-elements";
    center_div.className = "main-elements";

    main.append(aside_left,center_div,aside_right);
    body.append(main);   

    // ASIDE RIGHT contains:
    // possibility to switch side a with side b so that it appears first
    // possibility to shuffle the cards
    // all of those inside buttons and have to be set BEFORE starting

    const h3 = document.createElement("h3");
    h3.innerText = "Ajustes";
    const hr =  document.createElement("hr");

    const switch_div = document.createElement("div");
    const switch_p = document.createElement("p");
    const switch_btns = document.createElement("div");
    const btn_switcha = document.createElement("button"); // change to side a
    const btn_switchb = document.createElement("button"); // change to side b
    
    switch_div.id = "switch-div";
    switch_div.className = "right";
    btn_switcha.innerText = "Cara A";
    btn_switchb.innerText = "Cara B";
    btn_switcha.className = "right-btn"
    btn_switchb.className = "right-btn"
    switch_p.innerText = "¡Aquí puedes cambiar el lado que aparecerá primero en la tarjeta!";
    switch_btns.append(btn_switcha,btn_switchb);
    switch_div.append(switch_p,switch_btns);

    let priority_side = "a"; // por defecto ponemos la cara a como prioridad
    btn_switcha.classList.add("btn-clicked")
    // los botones tendrán funcionalidad más abajo

    const shuffle_div = document.createElement("div");
    const shuffle_p = document.createElement("p");
    const btn_shuffle = document.createElement("button");
    
    btn_shuffle.id = "btn-shuffle";
    btn_shuffle.className = "right-btn"
    shuffle_div.id = "shuffle-div";
    shuffle_div.className = "right";
    shuffle_p.innerText = "¿Quieres mezclar las tarjetas?";
    btn_shuffle.innerText = "NO";
    let shuffle_cards = false // por defecto no las mezclamos
    shuffle_div.append(shuffle_p,btn_shuffle);

    aside_right.append(h3,hr,switch_div,shuffle_div);


    // CENTER DIV.
    // elementos: header, body, footer 
    // header: h2 con el nombre del paquete, un par de spans con el nº de tarjetas + categorías
    // body: div cuadrado que será la flashcard
    // footer: tres botones, "siguiente", "anterior", "dar la vuelta a la tarjeta"

    const cheader = document.createElement("section");
    const cbody = document.createElement("section");
    const cfooter = document.createElement("section");

    cheader.id = "cheader";
    cfooter.id = "cfooter";
    cbody.id = "cbody";
    cheader.className = "center-elements";
    cfooter.className = "center-elements";
    cbody.className = "center-elements";

    center_div.append(cheader,cbody,cfooter);

    // center header: h2 + spansx2
    const h2 = document.createElement("h2");
    h2.innerText = data.data.packages.name;

    const group_spans = document.createElement("div");
    group_spans.id = "main-spans"
    
    const cat_span = document.createElement("span");
    cat_span.innerText = `Categoría: ${data.data.packages.category.name}`;

    const number_span = document.createElement("span");
    number_span.innerText = `Nº tarjetas: ${data.data.packages.cards.length}`
    
    group_spans.append(cat_span,number_span);
    cheader.append(h2,group_spans);

    // center footer: 3 botones
    const btn_prev = document.createElement("button");
    const btn_next = document.createElement("button");
    const btn_flip = document.createElement("button");

    btn_prev.id = "btn-prev";
    btn_next.id = "btn-next";
    btn_flip.id = "btn-flip";
    btn_prev.className = "btn-footer";
    btn_next.className = "btn-footer";
    btn_flip.className = "btn-footer";

    btn_prev.innerText = "<";
    btn_next.innerText = ">";
    btn_flip.innerText = "o";

    cfooter.append(btn_prev,btn_flip,btn_next);

    // center body: flashcards. DIV cuadrado grande simulando una tarjeta
    const flashcard = document.createElement("div");
    flashcard.id = "flashcard";
    // flashcard.innerText = "flashcard";
    cbody.append(flashcard);

    // FLASH CARD ELEMENTS

    // dentro de la flashcard vamos a poner tres divs, que aparecerán según el estado
    // start-div: cuando se empiece
    // ongoing-div: cuando se esté estudiando, se divide en cara a y cara b
    // end-div: al terminar

    const start_div = document.createElement("div");
    const ongoing_div = document.createElement("div");
    const end_div = document.createElement("div");
    
    start_div.className = "fcelements start";
    ongoing_div.className = "fcelements ongoing";
    end_div.className = "fcelements end";
    
    // al principio: start > display:block, og,end > display:none
    // durante: og > display:block, start,end > display:none
    // al final: end > display:block, og,start > display:none

    start_div.style.display = "flex";
    ongoing_div.style.display = "none";
    end_div.style.display = "none";

    flashcard.append(start_div,ongoing_div,end_div)

    // start div: tendrá un botón de start e info de los settings puestos
    const btn_start = document.createElement("button");
    btn_start.innerText = "Empezar";
    btn_start.id = "btn-start";

    const p_side = document.createElement("p");
    p_side.innerText = `Front: A`; //por defecto estará en el a
    const p_shuffle = document.createElement("p");
    p_shuffle.innerText = "Mezclar cartas: NO";
    // los botones del aside right
    btn_switcha.onclick = function(){
        // count = 0;
        // btn_next.classList.remove("dissabled");
        // btn_prev.classList.add("dissabled");
        // end_div.style.display = "none";
        // ongoing_div.style.display = "none";
        // start_div.style.display = "flex";
        priority_side = "a";
        p_side.innerText = `Front: A`;
        btn_switcha.classList.add("btn-clicked");
        btn_switchb.classList.remove("btn-clicked");
    };
    btn_switchb.onclick = function(){
        // count = 0;
        // btn_next.classList.remove("dissabled");
        // btn_prev.classList.add("dissabled");
        // end_div.style.display = "none";
        // ongoing_div.style.display = "none";
        // start_div.style.display = "flex";
        priority_side = "b";
        p_side.innerText = `Front: B`;
        btn_switchb.classList.add("btn-clicked");
        btn_switcha.classList.remove("btn-clicked");
    };
    btn_shuffle.onclick = function() {
        // count = 0;
        // btn_next.classList.remove("dissabled");
        // btn_prev.classList.add("dissabled");
        // end_div.style.display = "none";
        // ongoing_div.style.display = "none";
        // start_div.style.display = "flex";
        if (shuffle_cards) {
            p_shuffle.innerText = "Mezclar cartas: NO";
            btn_shuffle.innerText = "NO";
            shuffle_cards = false;
        }
        else {
            p_shuffle.innerText = "Mezclar cartas: SÍ";
            btn_shuffle.innerText = "SÍ";
            shuffle_cards = true;
        };
    };
    
    start_div.append(p_side,p_shuffle,btn_start);
    
    // ongoing div, side a and side b. Lo dividimos en dos para poder hacer el efecto de flip
    const side_a  = document.createElement("div");
    const side_b = document.createElement("div");
    const p_side_a =  document.createElement("p");
    const p_side_b =  document.createElement("p");
    side_a.append(p_side_a);
    side_b.append(p_side_b);
    side_a.className = "card-sides";
    side_b.className = "card-sides";
    
    //en base a nuestro priority side ponemos esto de una manera u otra, estos IDs son los que hacen functionar el css
    // si se cambian se le da la vuelta a las cartas
    let not_shuffled = [];
    for (let card of data.data.packages.cards) {
        not_shuffled.push(card);
    };
    let beta_cards = []
    for (let card of data.data.packages.cards) {
        beta_cards.push(card);
    };
    let cards = null;

    $("#btn-start").click(function(){
        console.log(priority_side)
        console.log(shuffle_cards)
        start_div.style.display = "none";
        ongoing_div.style.display = "block";
        if (priority_side === "a") {
            side_a.classList.add("front");
            side_b.classList.add("back");
            ongoing_div.append(side_a,side_b)
            console.log("funciona")
        }
        else {
            side_b.classList.add("front");
            side_a.classList.add("back");
            ongoing_div.append(side_b,side_a)
            console.log("funciona")
        };
        if (shuffle_cards) {
            // cards = beta_cards.sort((a, b) => 0.5 - Math.random());
            cards = beta_cards.sort(() => (Math.random() > .5) ? 1 : -1);
            p_side_a.innerText = cards[count].side_a;
            p_side_b.innerText = cards[count].side_b;
            console.log("funciona")
        }
        else {
            cards = not_shuffled
            p_side_a.innerText = data.data.packages.cards[count].side_a;
            p_side_b.innerText = data.data.packages.cards[count].side_b;
            console.log("funciona")
        };
        // console.log(cards)
        // console.log(data.data.packages.cards)
        
    });
    
    
    let count = 0;

    //buttons
    // botones next y prev estarán disabilitados cuando lleguen a ambos extremos, añadimos la clase "dissabled"

    btn_prev.classList.add("dissabled");

    $("#btn-flip").click(function() {
        if (ongoing_div.style.display !== "none") {
            if (ongoing_div.classList.contains("flipper")) {
                ongoing_div.classList.remove("flipper");
            }
            else {
                ongoing_div.classList.add("flipper");
            };
        };
    });

    $("#btn-next").click(function(){
        if (ongoing_div.style.display !== "none") {
            if (ongoing_div.classList.contains("flipper")){
                ongoing_div.classList.remove("flipper");
            };
            count += 1;
            if (count < cards.length){
                btn_prev.classList.remove("dissabled"); // botón habilitado
                p_side_a.innerText = cards[count].side_a;
                p_side_b.innerText = cards[count].side_b;
            }
            else {
                btn_next.classList.add("dissabled");
                ongoing_div.style.display = "none";
                end_div.style.display = "flex";
            };
        };
    });

    $("#btn-prev").click(function(){
        if (start_div.style.display === "none") {
            if (ongoing_div.classList.contains("flipper")){
                ongoing_div.classList.remove("flipper");
            };
            count -= 1;
            if (count >= 0){ //comprobamos que no sea la primera tarjeta
                if (end_div.style.display == "flex"){
                    btn_next.classList.remove("dissabled");
                    end_div.style.display = "none";
                    ongoing_div.style.display = "block";
                };
                p_side_a.innerText = cards[count].side_a;
                p_side_b.innerText = cards[count].side_b;
            }
            else {
                count += 1; // se anula la resta
                btn_prev.classList.add("dissabled");
            };
        };
    });

    // end div. dos botones, uno para hacer replay y otro para volver a seleccionar otro pack
    // añadimos otro botón por si se quiere resetear los settings
    const btn_replay = document.createElement("button"); //replay
    btn_replay.id = "btn-replay";
    btn_replay.type = "button";
    btn_replay.innerText = "replay";
    
    const btn_chpack = document.createElement("button"); // choose another pack
    btn_chpack.id = "btn-chpack";
    btn_chpack.type = "button";
    btn_chpack.innerText = "cambiar paquete";

    const btn_reset = document.createElement("button");
    btn_reset.id = "btn-reset";
    btn_reset.type = "button";
    btn_reset.innerText = "resetear ajustes"

    $(document).ready(function() {
        $("#btn-replay").click(function(){
            count = 0;
            btn_next.classList.remove("dissabled");
            btn_prev.classList.add("dissabled");
            p_side_a.innerText = cards[count].side_a;
            p_side_b.innerText = cards[count].side_b;
            end_div.style.display = "none";
            ongoing_div.style.display = "block";
        });

        $("#btn-chpack").click(function(){
            window.location.assign("http://localhost:5000/flash_cards");
        });
        $("#btn-reset").click(function(){
            count = 0;
            btn_next.classList.remove("dissabled");
            btn_prev.classList.add("dissabled");
            end_div.style.display = "none";
            ongoing_div.style.display = "none";
            start_div.style.display = "flex";
        });
    });
    
    end_div.append(btn_replay,btn_chpack,btn_reset);



};
