function back(){
    var path = document.getElementById("Login");
    path.innerHTML = `<input type = "submit" value = "Sign In" onclick="login();"/>
    <input type = "submit" value = "Sign Up" onclick="registration();"/>`;
}

function registration(){
    var path = document.getElementById("Login");
    path.innerHTML = `
        <form action = "/API/registration" method = "POST">
            <p> First Name : <input type = "text" name = "firstName" /></p>
            <p> Last Name : <input type = "text" name = "lastName" /></p>
            <p> Username : <input type = "text" name = "username" /></p>
            <p> Email : <input type = "text" name = "email" /></p>
            <p> Password : <input type = "password" name = "password" /></p>
            <p><input type = "submit" value = "Submit" /></p><input type = "submit" value = "Back" onclick="back();"/>
        </form> `;
}

function login(){
    var path = document.getElementById("Login");
    path.innerHTML = `
        <form action = "/API/login" method = "POST">
            <p> Login : <input type = "text" name = "Login" /></p>
            <p> Password : <input type = "password" name = "password" /></p>
            <p><input type = "submit" value = "Submit" /></p><input type = "submit" value = "Back" onclick="back();"/>
         </form> `;
}

function getForms(){
    var User = document.getElementById("nameUser");
    User = User.textContent;
    User = User.substring(8,);
    var URL = "API/getForms/" + User;

    $.ajax({
        type: "POST",
        url: URL,
        contentType: "application/json; charset=utf-8",
        dataType: 'json' ,
    }).done(function(data) {
        var path = document.getElementById("Forms");
        data = eval(data)
        var size = data['length'];
        var code = ''

        code += `
        <table border="1">
            <tr>
                <td> Formulary Name </td>
                <td> Creator </td>
                <td> Content </td>
                <td> Formulary ID </td>
            </tr>`;

        for(var i=0; i < size; i++){
            code += `
            <tr>
                <td> ${data[i]['FormName']} </td>
                <td> ${data[i]['Creator']} </td>
                <td> ${data[i]['Content']} </td>
                <td> ${data[i]['FormID']} </td>
            </tr>`;
        }
        
        code += `</table>`;

        code += `<br><input type = "submit" value = "Hide Forms" onclick="hideForms();"/>
        <input type = "submit" value = "Add Forms" onclick="addForms();"/>`
        path.innerHTML = code;
    });
}

function hideForms(){
    var path = document.getElementById("Forms");
    var code = `<input type = "submit" value = "Show Forms" onclick="getForms();"/>
    <input type = "submit" value = "Add Forms" onclick="addForms();"/>`;
    path.innerHTML = code;
}


function addForms(){
    var path = document.getElementById("Forms");
    var code = '';

    code += `
    <form onSubmit = "sendForm();">
        <p> Form Name : <input type = "text" name = "formName" /></p>
        <p> Content : <input type = "text" name = "content" /></p>
        <p><input type = "submit" value = "Submit" /></p>
    </form> `;

    path.innerHTML = code;
}

function sendForm(){

    var User = document.getElementById("nameUser");
    User = User.textContent;
    User = User.substring(8,);

    var formName = $('input[name=formName]').val();
    var content = $('input[name=content').val();

    $.ajax({
        type: "GET",
        url: 'API/addForm',
        contentType: "application/json; charset=utf-8",
        dataType: 'json' ,
        data: {
            'formName': formName,
            'creator': User,
            'content': content,
        },
    }).done(function(data) {
        data = eval(data);
        alert(data.status);
        
    });
}