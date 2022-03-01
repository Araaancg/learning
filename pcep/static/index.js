window.onload = async function() {
    console.log("js file linked")

    const res = await fetch(`http://localhost:5000/test`, {
        method:"POST"
    });
    const data = await res.json()
    console.log(data);

    const main = document.querySelector("#main");
    const form = document.createElement("form");
    let count_q = 1
    let count_o = 1
    for (question of data["data"]) {
        const div_t = document.createElement("div");
        div_t.className = "question"
        div_t.setAttribute("id", question.id);
        const p = document.createElement("p");
        p.innerText = question.question;
        div_t.append(p);

        const div_o = document.createElement("div");
        div_o.className = "options"

        for (option of question.options) {
            const o_input = document.createElement("input");
            o_input.setAttribute("type","radio");
            o_input.setAttribute("name",`q_${count_q}`);
            o_input.setAttribute("value",`${question.id},${option.id}`);
            o_input.setAttribute("id",`o_${count_o}`);

            const option_div = document.createElement("div");
            
            const label = document.createElement("label");
            label.setAttribute("for",`o_${count_o}`);
            label.innerText = option.option
            count_o += 1;
            // label.append(o_input)
            option_div.append(o_input,label);
            div_o.append(option_div);
        };
        
        count_q += 1;
        div_t.append(div_o);
        form.append(div_t);

    };

    const btn_submit = document.createElement("button");
    btn_submit.setAttribute("type","button");
    btn_submit.innerText = "Submit";
    form.append(btn_submit);

    const div_score = document.createElement("div");
    div_score.className = "score"
    const score_span = document.createElement("span")
    div_score.append(score_span)
    div_score.style.display = "none"

    btn_submit.onclick = async function() {
        const submit_form = new FormData(form);
        const res = await fetch(`http://localhost:5000/score`, {
            method: "POST",
            body: submit_form
        });
        const score = await res.json();

        for (question of score.data) {
            for (div of document.querySelectorAll(".question")) {
                if (div.id == question.question && question.grade == "correct") {
                    div.style.background = "#95d5b2" //green
                }
                else if (div.id == question.question && question.grade == "incorrect") {
                    div.style.background = "#ee6055"; //red
                    // const q = document.querySelector(`#${}`)
                };
            };
        };

        score_span.innerText = `score: ${score.final_score}`;
        div_score.style.display = "block";
    };

    // show grades aside

    main.append(div_score);
    main.append(form);

};