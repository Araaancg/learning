function delete_from_table() {
    let uri = window.location.href;
    const table_name = uri.split("/")[uri.split("/").length - 2];
    console.log(table_name);
    const id = uri.split("/")[uri.split("/").length - 1];
    console.log(id);

    fetch(`http://localhost:3000/api/${table_name}/${id}`, {
        method: "DELETE"
        // body: form
    });
    window.location.replace(`http://localhost:3000/honey/api/${table_name}`);

};

