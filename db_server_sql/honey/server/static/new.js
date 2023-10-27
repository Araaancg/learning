async function new_register_on_table() {
    let uri = window.location.href;
    const table_name = uri.split("/")[uri.split("/").length - 1];
    console.log(table_name)
    const name = document.querySelector("#name");
    console.log(name.value);
    const email = document.querySelector("#email");
    console.log(email.value);

    const form = new FormData();
    form.append("name", name.value);
    form.append("email", email.value);
    if (email.value && email.value) {
        await fetch(`http://localhost:3000/honey/api/${table_name}s`, {
            method: "POST",
            body: form
        });
        // console.log(`http://localhost:3000/honey/api/${table_name}s`)
        window.location.replace(`http://localhost:5000/honey/${table_name}s`);
    };
    else {
        alert("Fill in all of the blanks")
    };
};
