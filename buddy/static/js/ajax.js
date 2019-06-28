$(document).ready(function(){
    console.log("js connected")
    $('#email').keyup(function(){
        console.log("button was pressed")
        var data = $("#regForm").serialize()   // capture all the data in the form in the variable data
        console.log("Data from form: ", data)
        $.ajax({
            url: "/email",
            method: "POST",   // we are using a post request here, but this could also be done with a get
            data: data
        })
        .done(function(res){
            console.log('done function test good')
             $('#emailMsg').html(res)  // manipulate the dom when the response comes back
             console.log(res)
        })
        console.log("After ajax call!")
    })
})