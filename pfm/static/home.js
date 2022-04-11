window.onload = function() {
    const btn_new = document.querySelector("#new_pack");
    btn_new.onclick = function() {
        window.location.assign("http://localhost:5000/my_packages")
    };
    

};