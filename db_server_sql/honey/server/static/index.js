// const <html_element> = document()

// fetch(uri_collectors)
//     .then((res) => res.json())
//     .then((data) => {for (let collector of data["data"]) console.log(collector)});


// async function get_data(uri) {
    //     const res = await fetch(uri);
    //     const data = await res.json();
    //     for (let value of data["data"]){
        //         data_out.push(value)
        //     }
        // };
        
        
const uri_collectors = "http://localhost:3000/honey/api/collectors";

async function get_table(uri) {
    const res = await fetch(uri);
    const pre_data = await res.json();
    const data = await pre_data["data"];
    const fields = Object.keys(data[0]);
    const h_tr = document.createElement("tr")
    for (let field of fields) {
        const th = document.createElement("th");
        th.innerText = field;
        h_tr.append(th)
        // console.log(field)
    };
    const thead = document.querySelector("#thead");
    thead.append(h_tr);
    
};

get_table(uri_collectors)


