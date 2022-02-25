
const form = document.createElement("form");

const input_name = document.createElement("input");
input_name.type = "text";
input_name.required;
input_name.id = "name";
input_name.name = "name";

const label_name = document.createElement("label");
label_name.for = "name";
label_name.innerText = "Nombre";

const main = document.querySelector("main");

form.append(label_name);
form.append(input_name);
main.append(form);


// new_package_form()