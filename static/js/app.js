function back(){
    var path = document.getElementById("json");
    path.innerHTML = '';
    var path2 = document.getElementById("requests");
    path2.innerHTML = `<input class="content-requests-buttom" type = "submit" value = "/login" onclick="login();"/>
    <input class="content-requests-buttom" type = "submit" value = "/registration" onclick="registration();"/>
    <input class="content-requests-buttom" type = "submit" value = "/getForms" onclick="getForms();"/>`;
}

function login() {
    var path = document.getElementById("json");
    var path2 = document.getElementById("requests")
    path.innerHTML = `
        <pre class="content-requests">{<br>    status : Succeed,<br>    hash : 094bcef537f87550e151acae1b9cebaa,<br>    class : Admin<br>}<br></pre>`;

    path2.innerHTML = `<input class="content-requests-buttom" type = "submit" value = "Back" onclick="back();"/>`;
}

function registration() {
    var path = document.getElementById("json");
    var path2 = document.getElementById("requests")
    path.innerHTML = `
        <pre class="content-requests">{<br>    status : Succeed,<br>    hash : 094bcef537f87550e151acae1b9cebaa,<br>    message : User created with success...<br>}<br></pre>`;

    path2.innerHTML = `<input class="content-requests-buttom" type = "submit" value = "Back" onclick="back();"/>`;
}

function getForms() {
    var path = document.getElementById("json");
    var path2 = document.getElementById("requests")
    path.innerHTML = `
        <pre class="content-requests">[<br>    {<br>        'FormName': 'Form Test', <br>        'Creator': 'joel2', <br>        'Content': 'Content Form 1', <br>        'FormID': '1'<br>    },<br>{<br>        'FormName': 'Test', <br>        'Creator': 'joel2', <br>        'Content': 'Content Form 2', <br>        'FormID': '2'<br>    }<br>]<br></pre>`;

    path2.innerHTML = `<input class="content-requests-buttom" type = "submit" value = "Back" onclick="back();"/>`;
}