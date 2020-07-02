$(document).ready(function() {
    $(".solo_numeros").change(function() {
        var campo = $(this);
        validarSoloNumeros(campo);
    });
    $("form").on("submit", function () {
        $(this).find("select, input").prop("disabled", false);
        return true;
    });
});