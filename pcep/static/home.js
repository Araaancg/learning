window.onload = async function() {
    const main = document.querySelector("#main");
    const div_grades = document.createElement("div");

    //button to show table of grades
    const btn_grades = document.createElement("button");
    btn_grades.innerText = "show your grades";

    //table of grades
    const res = await fetch("http://localhost:5000/home", {
        method:"POST"   
    });
    const data = await res.json();
    console.log(data);
    if (data.grades) {
        const span_grades = document.createElement("span");
        span_grades.innerText = "Grades";
        const grade_list = document.createElement("ul");
        for (grade of data.grades) {
            const li = document.createElement("li");
            li.innerText = grade
            grade_list.append(li);
        };
        
        const span_plus_list = document.createElement("div");
        span_plus_list.className = "grades-list"
        span_plus_list.append(span_grades,grade_list);
        span_plus_list.style.display = "none";
    
        btn_grades.onclick = function() {
            if (span_plus_list.style.display !== "none") {
                span_plus_list.style.display = "none";
            }
            else {
                span_plus_list.style.display = "block";
            };
        };
        div_grades.append(btn_grades, span_plus_list);
    };


    const btn_test = document.querySelector("#href-btn");
    btn_test.onclick = function() {
        window.location.assign("http://localhost:5000/test");
    };

    div_grades.className = "action";


    main.append(div_grades)
};