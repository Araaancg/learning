window.onload = function() {

    // NAME OF PACKAGE
    const form = document.createElement('form');
    const input_name = document.createElement("input");
    input_name.type = "text";
    input_name.required;
    input_name.id = "name";
    input_name.name = "name";
    const label_name = document.createElement("label");
    label_name.for = "name";
    label_name.innerText = "Nombre";
    form.append(label_name);
    form.append(input_name);
    
    // CARDS
    let count = 10;
    
    while (count > 0) {
        const input_card = document.createElement("input");
        input_card.type = "text";
        // input_name.id = "name";
        input_name.name = `card_${count}`;
        form.append(input_card)
        count -= 1;
    };
    

    document.querySelector('main').append(form);
};
