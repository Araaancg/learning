const uri_collectors = "http://localhost:3000/honey/api/collectors";

async function get_data(uri) {
    const res = await fetch(uri);
    const pre_data = await res.json();
    const data = await pre_data["data"];

    const fields = Object.keys(data[0]);
    const h_tr = document.createElement("tr");
    for (let field of fields) {
        const th = document.createElement("th");
        th.innerText = field;
        h_tr.append(th);
    };
    const thead = document.querySelector("#thead");
    thead.append(h_tr);

    for (let person of data) {
        const d_tr = document.createElement("tr");
        // console.log(Object.values(person));
        // console.log(person);
        // const val = Object.values(person);
        // console.log(val);
        for (let v of Object.values(person)) {
            // console.log(v);
            const td = document.createElement("td");
            td.innerText = v;
            d_tr.append(td);
        };
        const tbody = document.querySelector("#tbody");
        tbody.append(d_tr);
    };
    
};

get_data(uri_collectors)


