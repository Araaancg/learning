function decodeHtmlCharCodes(str) { 
    return str.replace(/(&#(\d+);)/g, function(match, capture, charCode) {
      return String.fromCharCode(charCode);
    });
}

window.onload = async function() {
  if (window.localStorage.getItem("theme") === "light") {
    const body = document.querySelector("body");
    body.className = "light";
  };

  const main = document.querySelector("#main");
  const uri = window.location.href;
  const pack_name = uri.split("/")[uri.split("/").length - 1];
  // console.log(pack_name);
  const res = await fetch(`http://localhost:5000/mis_paquetes/${pack_name}`, {
      method:"POST"
  });
  const data = await res.json();
  console.log(data);

  // ponemos título
  const head_html = document.querySelector("head");
  const title = document.createElement("title");
  title.innerText = `PFM | Mis paquetes: ${data.data.packages.name}`;
  head_html.append(title);

  // habrá tres partes:
  // top: tendrá el título, categoría y número de tarjetas
  // center: tendrá las tarjetas
  // bottom: botones para eliminar paquete, crear tarjetas...


  // TOP
  const top = document.createElement("section");
  top.className = "main-parts top";

  const h1 = document.createElement("h1");
  h1.innerText = data.data.packages.name;

  const pack_info = document.createElement("div"); //category and number of cards
  pack_info.className = "pack-info";
  const cat_span = document.createElement("span");
  let number_span = document.createElement("span");
  cat_span.innerText = `Categoría: ${data.data.packages.category.name}`;
  number_span.innerText = `Nº de tarjetas: `
  let number_cards = 0;
  
  pack_info.append(cat_span, number_span);
  top.append(h1,pack_info);

  // CENTER
  const edit_overlay = document.createElement("div"); 
  edit_overlay.style.display = "none";
  edit_overlay.className = "edit-overlay";
  const center = document.createElement("section");
  center.className = "main-parts center";
  for (let card of data.data.packages.cards) {
    const single_card = document.createElement("div");
    single_card.className = "single-card";

    // main part
    const center_card = document.createElement("div");
    center_card.className = "center-card";
    const hr = document.createElement("hr");
    const p_sidea = document.createElement("p");
    const p_sideb = document.createElement("p");
    p_sidea.innerText = card.side_a;
    p_sideb.innerText = card.side_b;
    center_card.append(p_sidea,hr,p_sideb);

    // top part with btn-delete
    const top_card = document.createElement("div");
    top_card.className = "top-card";
    const btn_delete = document.createElement("button");
    btn_delete.className = "btn-delete";
    btn_delete.type = "button";
    btn_delete.title = "eliminar del paquete"
    btn_delete.innerText = "x";
    btn_delete.onclick = async function() {
      await fetch(`http://localhost:5000/mis_paquetes/${data.data.packages.id}?delete_card=${card.id}`);
      window.location.reload();
    };
    top_card.append(btn_delete);

    // bottom part with btn-edit
    const bottom_card = document.createElement("div");
    bottom_card.className = "bottom-card";
    const btn_edit = document.createElement("button");
    btn_edit.className = "btn-edit";
    btn_edit.innerText = "editar";
    btn_edit.onclick = function(){
      // for editing will create an overlay
      edit_overlay.style.display = "flex";
      const edit_popup =  document.createElement("div");
      edit_popup.className = "edit-popup";

      const edit_cards = document.createElement("div");
      edit_cards.className = "edit-cards";

      const right_card = document.createElement("div");
      right_card.className = "popup-card right-card";
      const left_card = document.createElement("div");
      left_card.className = "popup-card left-card";

      // left card: current card
      const p_sidea_edit = document.createElement("p");
      const p_sideb_edit = document.createElement("p");
      const edit_hr1 = document.createElement("hr");
      p_sidea_edit.innerText = card.side_a;
      p_sideb_edit.innerText = card.side_b;
      left_card.append(p_sidea_edit,edit_hr1,p_sideb_edit);

      // right card: card with inputs to edit
      const textareaa = document.createElement("textarea");
      const textareab =  document.createElement("textarea");
      const edit_hr2 = document.createElement("hr");
      textareaa.placeholder = "cara a";
      textareab.placeholder = "cara b";
      right_card.append(textareaa,edit_hr2,textareab);

      // bottom part: buttons
      const edit_buttons_div = document.createElement("div");
      edit_buttons_div.className = "edit-buttons-div";
      const btn_cancel_edit = document.createElement("button");
      btn_cancel_edit.type = "button";
      btn_cancel_edit.innerText = "cancelar";
      btn_cancel_edit.className = "edit-buttons btn-cancel";
      btn_cancel_edit.onclick = function() {
        edit_overlay.style.display = "none";
        edit_overlay.innerText = "";
      };
      const btn_save_edit = document.createElement("button");
      btn_save_edit.type = "button";
      btn_save_edit.innerText = "guardar";
      btn_save_edit.className = "edit-buttons btn-save";
      btn_save_edit.onclick = async function() {
        const form = new FormData();
        form.append("side_a",textareaa.value);
        form.append("side_b",textareab.value);
        await fetch(`http://localhost:5000/mis_paquetes/${data.data.packages.name}?edit_card=${card.id}`, {
            method:"PUT",
            body:form
        });
        window.location.reload();
      };
      edit_buttons_div.append(btn_cancel_edit,btn_save_edit);
      
      edit_cards.append(left_card,right_card);
      edit_popup.append(edit_cards,edit_buttons_div);
      edit_overlay.append(edit_popup);
    };
    
    bottom_card.append(btn_edit);

    
    single_card.append(top_card,center_card,bottom_card);
    center.append(single_card);
    number_cards += 1;
  };
  number_span.innerText += number_cards;

  // BOTTOM: eliminar paquete y añadir tarjetas
  const bottom = document.createElement("section");
  bottom.className = "bottom";
  const btn_delete_pack = document.createElement("button");
  btn_delete_pack.id = "btn-delete-pack";
  btn_delete_pack.type = "button";
  btn_delete_pack.innerText = "eliminar paquete";
  btn_delete_pack.onclick = async function(){
    confirmation = confirm("El paquete se eliminará de la base de datos pero las tarjetas se te quedarán en el perfil. Para eliminarlas vete a tu perfil.");
      if (confirmation) {
          await fetch(`http://localhost:5000/mis_paquetes/${data.data.packages.name}?delete_pack=${data.data.packages.id}`);
          window.location.assign("http://localhost:5000/mis_paquetes");
          console.log("paquete eliminardo");
      }
      else {
          console.log("acción cancelada");
      }
  };

  const btn_create_card  = document.createElement("button");
  btn_create_card.className = "btn-create-cards";
  btn_create_card.innerText = "crear tarjeta";
  btn_create_card.type = "button";
  btn_create_card.onclick = function() {
    edit_overlay.style.display = "flex";

    const card_to_create = document.createElement("div");
    card_to_create.className = "card-to-create";

    const create_sidea = document.createElement("textarea");
    const create_sideb = document.createElement("textarea");
    const create_hr = document.createElement("hr");
    create_sidea.placeholder = "cara a";
    create_sideb.placeholder = "cara b";
    card_to_create.append(create_sidea,create_hr,create_sideb);

    //buttons
    const div_buttons_create = document.createElement("div");
    div_buttons_create.className = "div-buttons-create";

    const btn_cancel_create = document.createElement("button");
    btn_cancel_create.type = "button";
    btn_cancel_create.innerText = "cancel";
    btn_cancel_create.className = "btn-cancel-create"
    btn_cancel_create.onclick = function() {
      edit_overlay.style.display = "none";
      edit_overlay.innerText = "";
    }

    const btn_save_create = document.createElement("button");
    btn_save_create.type = "button";
    btn_save_create.innerText = "guardar";
    btn_save_create.className = "btn-save-create";
    btn_save_create.onclick = async function() {
      const form = new FormData();
      form.append("side_a",create_sidea.value);
      form.append("side_b",create_sideb.value);
      await fetch(`http://localhost:5000/mis_paquetes/${data.data.packages.name}?new_card=${data.data.packages.id}`, {
          method:"PUT",
          body:form
      });
      window.location.reload()
    };

      div_buttons_create.append(btn_cancel_create,btn_save_create)
      edit_overlay.append(card_to_create,div_buttons_create);
    };

    const btn_add_currentcard = document.createElement("button");
    btn_add_currentcard.className = "btn-add-currentcard";
    btn_add_currentcard.innerText = "añadir tarjetas de mi biblioteca";
    btn_add_currentcard.type = "button";

    btn_add_currentcard.onclick = async function() {
      const popres = await fetch(`http://localhost:5000/ajustes?get=mycards`);
      const result = await popres.json();

      edit_overlay.style.display = "flex";
      
      const existing_cards = document.createElement("div");
      existing_cards.className = "existing-cards";
      
      for (let card of result.cards) {
        let card_isin_pack = "no";
        for (let pack of card.packages) {
            if (pack.id === data.data.packages.id && card_isin_pack === "no") {
                card_isin_pack = "yes";
            };
        };
        if (card_isin_pack === "no"){
            const single_card = document.createElement("div");
            const p_sidea = document.createElement("p");
            const p_sideb = document.createElement("p");
            const pophr = document.createElement("hr");
            single_card.id = card.id

            single_card.className = "single-existing-card";
            p_sidea.innerText = card.side_a;
            p_sideb.innerText = card.side_b;

            single_card.append(p_sidea,pophr,p_sideb);
            existing_cards.append(single_card);
        };
      };

      // bottom with two buttons
      const div_existing_buttons = document.createElement("div");
      div_existing_buttons.className = "existing-cards-btns"
      // botón de confirmación y cerrar ventana
      const btn_confirmation = document.createElement("button");
      btn_confirmation.type = "button";
      btn_confirmation.innerText = "añadir";
      btn_confirmation.className = "btn-confirm";

      const btn_close_ex = document.createElement("button");
      btn_close_ex.type = "button";
      btn_close_ex.innerText = "cerrar";
      btn_close_ex.className = "btn-close-ex";
      btn_close_ex.onclick = function() {
        edit_overlay.innerText = "";
        edit_overlay.style.display = "none";
      };

      let cards_to_add = [];

      $(document).ready(function() {
          $(".single-existing-card").click(function(){
              if ($(this).hasClass("card-selected")) {
                  $(this).removeClass("card-selected");
                  cards_to_add = cards_to_add.filter(card => card !== $(this).attr('id'));
                  console.log(cards_to_add);
              }
              else {
                  $(this).addClass("card-selected");
                  cards_to_add.push($(this).attr('id'));
                  console.log(cards_to_add);
              };
          });
      });

      btn_confirmation.onclick = async function() {
        const form = new FormData();
        let count = 0
        for (let item of cards_to_add){
            form.append(`exist_${count}`,item);
            count += 1
        };
        await fetch(`http://localhost:5000/mis_paquetes/${data.data.packages.name}?existing_cards=${data.data.packages.id}`, {
            method:"PUT",
            body:form
        });
        window.location.reload();
      };

      div_existing_buttons.append(btn_close_ex,btn_confirmation)
      edit_overlay.append(existing_cards,div_existing_buttons);
    };

    bottom.append(btn_create_card,btn_add_currentcard,btn_delete_pack);


    main.append(top,center,bottom,edit_overlay);
};