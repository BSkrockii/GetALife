$(document).ready(function () { 

    var today = new Date();
    var todayYear = today.getFullYear();
    const month = today.toLocaleString('default', { month: 'long' });

    let temp = $( "#"+ month.toLowerCase() +"-"+todayYear+"-content");

    let temp2 = $( "#budget-year-" + todayYear);


    if(temp.attr('class') == "content-inactive"){
        temp.addClass('content-active').removeClass('content-inactive');
    }else{
        temp.addClass('content-inactive').removeClass('content-active');
    }

    if(temp2.attr('class') == "content-inactive"){
        temp2.addClass('content-active').removeClass('content-inactive');
    }else{
        temp2.addClass('content-inactive').removeClass('content-active');
    }


})


let selectedRow = null;
let inEditMode = 0;
let budgetName = null;
let planned = null;
let actual = null;

function showContentYear(callerYear) {

    let el = $( "#budget-year-" + callerYear);

    if(el.attr('class') == "content-inactive"){
        el.addClass('content-active').removeClass('content-inactive');
    }else{
        el.addClass('content-inactive').removeClass('content-active');
    }
}
function showContentMonth(callerMonthel) {

    let el = $("#" + callerMonthel.id + "-content");

    if(el.attr('class') == "content-inactive"){
        el.addClass('content-active').removeClass('content-inactive');
    }else{
        el.addClass('content-inactive').removeClass('content-active');
    }
    
}

function newExpense(month, year, button) {
    let el = $("#" + month + "-" + year + "-table");
    el.append("<tr><td><input type='text' id='newExpenseName" + month + year + "'\></td><td><input type='text' id='newPlanned" + month + year + "' \></td><td>0</td></tr>")

    let but = $("#" + button.id);
    but.text('ADD');
    but.attr("onClick", "addNewExpense('" + month + "', '" + year +"', this)");
    but.removeClass('btn btn-dark').addClass('btn btn-success');

}

function addNewExpense(month, year, button){
    let table = $("#" + month + "-" + year + "-table");
    let el = $("#" + month + "-" + year + "-table tr:last");
    let but = $("#" + button.id);
    let newExpense = $("#newExpenseName" + month + year);
    let newPlanned = $("#newPlanned" + month + year);

    $.ajax({
        crossOrigin: false,
        type: "POST",
        url: "http://127.0.0.1:8000/addExpense/",
        dataType: "json",
        async: true,
        data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                newExpense: newExpense.val(),
                newPlanned: newPlanned.val(),
                month: month,
                year: year},
        success: function (json, response){
            el.remove();
            table.append("<tr><td>"+ newExpense.val() +"</td><td>"+ newPlanned.val() +"</td><td>0</td></tr>");
            but.removeClass('btn btn-success').addClass('btn btn-dark');
            but.attr("onClick", "newExpense('" + month + "', '" + year +"', this)");
            but.text('Add Expense Type');
        },
        error: function (request, status, error){
            console.log("An Error Has Occured");
        }
    })

};


$("[id*=-table] tr").click(function(){   
    if(!inEditMode){
        let but = $("#" + $(this).parent().parent().parent().parent().attr('id') + "-but");
    
        if($(this).hasClass("table-dark")){
            $(this).removeClass('table-dark');
            but.prop("disabled",true);
            but.removeClass('btn btn-info').addClass('btn btn-secondary');
            selectedRow = null;
        }else{
            $(this).addClass('table-dark').siblings().removeClass('table-dark');
            but.prop("disabled",false);
            but.removeClass('btn btn-secondary').addClass('btn btn-info');
            selectedRow = $(this);
        }
    }
 });

$("[id*=-edit-but] ").click(function(){   
    if(!inEditMode){
        budgetName = selectedRow.children()[0].textContent;
        planned = selectedRow.children()[1].textContent;
        actual = selectedRow.children()[2].textContent;

        selectedRow.removeClass('table-dark');

        selectedRow.html("<td><input type='text' id='updatedBudgeName' value='" + budgetName + "'></td>" +
                "<td><input type='text' id='updatedPlanned' value='" + planned + "'></td>" +
                "<td>" + actual + "</td>");
        inEditMode = 1

        $(this).after("<button type='button' id='saveChanges' onclick='saveChanges()' class='ml-1 btn btn-success'>Save</button>" +
                        "<button type='button' id='undoChanges' onclick='undoChanges()' class='ml-1 btn btn-warning'>Undo</button>");
    }

});

function saveChanges(){
    let updatedBudgeName = $("#updatedBudgeName").val();
    let updatedPlanned = $("#updatedPlanned").val();

    let temp = $(selectedRow.attr('id').split("-"));


    if(updatedBudgeName == budgetName && updatedPlanned == planned){
        undoChanges();
    }else{
        
        $.ajax({
            crossOrigin: false,
            type: "POST",
            url: "http://127.0.0.1:8000/updateExpense/",
            dataType: "json",
            async: true,
            data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                    budgetName: updatedBudgeName,
                    planned: updatedPlanned,
                    month: temp[1],
                    year: temp[0],
                    oldValue: budgetName},
            success: function (json, response){
                $('#saveChanges').remove();
                $('#undoChanges').remove();
                let el = selectedRow;
                el.html("<td>" + updatedBudgeName + "</td>" +
                        "<td>" + updatedPlanned + "</td>" +
                        "<td>" + actual + "</td>");
                budgetName = null;
                planned = null;
                actual = null;
                selectedRow = null;
                inEditMode = 0;
            },
            error: function (request, status, error){
                console.log("An Error Has Occured");
            }
        })
    }
}

function undoChanges(){
   $('#saveChanges').remove();
   $('#undoChanges').remove();
   let el = selectedRow;
   el.html("<td>" + budgetName + "</td>" +
           "<td>" + planned + "</td>" +
           "<td>" + actual + "</td>");
    
    budgetName = null;
    planned = null;
    actual = null;
    selectedRow = null;
    inEditMode = 0;
}

    
