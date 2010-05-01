$(document).ready(function(){

$("#name").val('Expense name');
$("#date").datepicker({dateFormat: 'DD, d M yy', altField: '#expDate', altFormat: 'dd-mm-yy'});

$("#expSubmit").click(function() {
$.post("/addexpense", { expName: $("#expName").val(), expType: $("#expType").val(), expDate: $("#expDate").val() });
});
});
