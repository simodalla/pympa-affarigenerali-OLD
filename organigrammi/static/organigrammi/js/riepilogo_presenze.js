$(document).ready(function() {
    $(".range_date_field").datepicker({
        showOtherMonths: true,
        selectOtherMonths: true,
        changeMonth: true,
        changeYear: true,
        minDate: "-10Y",
        maxDate: "+2Y",
        dateFormat: "dd/mm/yy"
    });
    $("input[type=submit]").button();
    $("th.persona").parent().css("background-color", "lightpink");
    $("th.assessore").parent().css("background-color", "lightblue");
    $("#result_list tr:last").prepend(
        "<th colspan='" + ($("#result_list tr:first").children().length -
            $("#result_list tr:last").children().length)  +"'>Totali:</th>");
    $("#result_list tr:last").children().css("padding-top", "20px");
});