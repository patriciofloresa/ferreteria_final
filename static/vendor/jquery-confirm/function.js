
function alert_jqueryconfirm(){
    $.confirm({
        theme: 'materia',
        title: 'Confirmacion',
        icon: 'fa fa-info',
        content: '',
        columnClass: 'medium',
        typeAnimated: true,
        cancelButtonClass: 'btn-primary',
        draggable: true,
        dragWindowBorder: false,
        buttons: {
            info: {
                text: "Si",
                btnClass: 'btn-primary',
                action: function () {

                }
            },
            danger: {
                text: 'No',
                btnClass: 'btn-red',
                action: function(){

                }
            },
        }

    })
}