window.onload = async function() {
    const main = document.querySelector("#main");
    const left_div = document.createElement("container");
    const right_div = document.createElement("container");

    left_div.setAttribute("id","left-div");
    right_div.setAttribute("id","right-div");
    left_div.className = "main-divs"
    right_div.className = "main-divs";
    // left_div.innerText = "left div"
    // right_div.innerText = "right_div"

    // LEFT DIV: divided into two parts, a button to take a test and 
    // a graphic of users's grades
    const btn_ttest =  document.createElement("button");
    btn_ttest.setAttribute("type","button");
    btn_ttest.innerText = "take a test";
    btn_ttest.setAttribute("id","btn_ttest");
    btn_ttest.onclick = function() {
        window.location.assign("http://localhost:5000/test");
    };

    const graph_div = document.createElement("section");
    graph_div.setAttribute("id","graph-div");
    graph_div.innerText = "future graphic";

    left_div.append(btn_ttest, graph_div);

    // RIGHT DIV: table with all the tests done, grades and time
    const h2 = document.createElement("h2");
    h2.innerText = "Tests";

    //table
    const table = document.createElement("table");
    const thead = document.createElement("thead");
    const th_date = document.createElement("th");
    const th_grade = document.createElement("th");
    th_date.innerText = "date";
    th_grade.innerText = "grade";
    thead.append(th_date,th_grade);
    table.append(thead);

    // data for the table
    res = await fetch(`http://localhost:5000/test?get_all=True`);
    data = await res.json();
    console.log(data);
    const tbody = document.createElement("tbody");
    for (let test of data.tests) {
        const tr = document.createElement("tr");
        const td_date = document.createElement("td");
        td_date.className = "dates"
        const td_grade = document.createElement("td");
        td_date.innerText = test.date.replace("T", " | ");
        const a = document.createElement("a");
        a.href = `http://localhost:5000/test/${test.date}`
        a.append(td_date);
        td_grade.innerText = `${test.grade}/5`;
        tr.append(a,td_grade);
        tbody.append(tr);
    };
    table.append(tbody)

    right_div.append(h2,table);

    main.append(left_div,right_div);
};