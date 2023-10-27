window.onload = async function () {
    let uri = window.location.href;
    const date = uri.split("/")[uri.split("/").length - 1];
    console.log(`http://localhost:5000/test/${date}`)
    res = await fetch(`http://localhost:5000/test/${date}?get_test=true`);
    data = await res.json();
    console.log(data);

    const main = document.querySelector("#main");

    const div_score = document.createElement("div");
    div_score.className = "score"
    const score_span = document.createElement("span")
    div_score.append(score_span)

    score_span.innerText = `score: ${data.test.grade}/5`;

    main.append(div_score);

    // const form = document.createElement("form");
    let count_q = 1
    let count_o = 1
    for (question of data.test.test) {
        const div_t = document.createElement("div");
        div_t.className = "question"
        div_t.setAttribute("id", question.question_id);
        const p = document.createElement("p");
        p.innerText = question.question;
        div_t.append(p);

        const div_o = document.createElement("div");
        div_o.className = "options"

        for (option of question.options) {
            const o_input = document.createElement("input");
            o_input.setAttribute("type","radio");
            o_input.setAttribute("name",`q_${count_q}`);
            o_input.setAttribute("value",`${option.id}`);
            o_input.setAttribute("id",`o_${count_o}`);

            if (question.user_choice == option.id) {
                o_input.setAttribute("checked",true)
            };
            const option_div = document.createElement("div");
            
            const label = document.createElement("label");
            label.setAttribute("for",`o_${count_o}`);
            label.innerText = option.option
            count_o += 1;
            option_div.append(o_input,label);
            div_o.append(option_div);
            div_t.style.background = question.veredict == "correct"? "#95d5b2":"#ee6055";
            option_div.style.background = option.id == question.a ? "#e9c46a":null;
        };
        
        count_q += 1;
        div_t.append(div_o);
        main.append(div_t);

    };

    
};