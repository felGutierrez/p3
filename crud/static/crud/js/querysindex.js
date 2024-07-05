
$(document).ready(function () {

    console.log("Esperando...");
    $.getJSON('https://mindicador.cl/api', function () {

      /* console.log([data]);
       $("#dolar").text(data.dolar.valor);*/

    }).fail(function () {
        console.log('Error al consumir la API!');
        $("#dolar").text('Error al consumir la API!');
    }).done(function(data)
    {
       
        $(".spinner").hide();
        $("#dolar").text("CLP$" + data.dolar.valor);
        $("#euro").text("CLP$" + data.euro.valor);
        $("#utm").text("CLP$" + data.utm.valor);
    });
});

$(document).ready(function () {
    $("#texto").blur(function (e) { 
        console.log([e]);
        if ($("#texto").val()!="")
        {
            $("#botoncito").removeAttr("disabled");
        }

        
    });
});

$(document).ready(function () {
    $("#valtexto").dblclick(function (e) { 
        console.log([e]);
        alert("hola doble click");
        
    });

});