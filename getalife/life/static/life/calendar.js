var globalCalendar;

document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var currentDateEL;

    getEvents();
    

    var calendar = new FullCalendar.Calendar(calendarEl, {

        

        plugins: [ 'dayGrid', 'interaction' ],
        dateClick: function(info) {

            if(currentDateEL){
                currentDateEL.style.backgroundColor = 'transparent';
            }
            
            if(info.date.toLocaleDateString() != (new Date().toLocaleDateString())){
                currentDateEL = info.dayEl;
                info.dayEl.style.backgroundColor = '#CECEF6';
            }

            calendar.state.currentDate = info.date;

            str = calendar.formatDate(info.date,{
                month: 'long',
                year: 'numeric',
                day: 'numeric'
              });
            updateScreen(str);
          },
        displayEventTime: false,
        updateEvent: function() {
            calendar.addEvent({title: 'New Event On 29' ,start: '2020-03-29'});
        }


    });

    globalCalendar = calendar;
    
    calendar.render();

    calendar.updateEvent;

    var str = calendar.formatDate(calendar.state.currentDate,{
        month: 'long',
        year: 'numeric',
        day: 'numeric'
      });
      updateScreen(str);

  function updateScreen(str){
    document.getElementById("currentDate").innerHTML = str;

    $("#events").find("tr:not(:first)").remove();

    var tableString = '';
    var temp = calendar.getEvents();
    for (let i = 0; i < temp.length; i++) {
        if(temp[i].start.toLocaleDateString() == calendar.state.currentDate.toLocaleDateString()){
            tableString += '<tr id="' + temp[i].id + '">';
            tableString += '<td>' + temp[i].title +'</td>';
            tableString += '<td>' + temp[i].start.toLocaleDateString() +'</td>';
            tableString += '<td>' + temp[i].extendedProps.amount +'</td>';
            tableString += '<td>' + temp[i].extendedProps.event_type +'</td>';
            tableString += '<td><button class="deleteEvent" onclick="deleteEvent(this)">X</button></td>';
            tableString += '</tr>';
        }
    }
    document.getElementById("events").innerHTML += tableString;
  };



  function getEvents(){
    $.ajax({
        crossOrigin: false,
        type: "GET",
        url: "http://127.0.0.1:8000/event",
        dataType: "json",
        async: true,
        data: { csrfmiddlewaretoken: '{{ csrf_token }}'},
        success: function (json){
            parsed = JSON.parse(json);
            for (let i = 0; i < parsed.length; i++) {
                calendar.addEvent({id: parsed[i].pk,
                                   title: parsed[i].fields.event_name,
                                   start: parsed[i].fields.start_date,
                                   extendedProps:{ amount: parsed[i].fields.amount,
                                                   event_type: parsed[i].fields.event_type,
                                    }});
              }
        }
    })
}


});

function openForm(){
    $.ajax({
        crossOrigin: false,
        type: "GET",
        url: "http://127.0.0.1:8000/getExpenseTypes",
        dataType: "json",
        async: true,
        data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                date: globalCalendar.state.currentDate.toLocaleDateString()},
        success: function (json){
            parsed = JSON.parse(json);
                var form = "<tr><td><input type='text' placeholder='Event' id='newEvent' required></td></tr>";
                form += "<tr><td>" + globalCalendar.state.currentDate.toLocaleDateString() + "</td></tr>";
                form += "<tr><td>" + "<input type='text' placeholder='Amount' id='newAmount' required>" + "</td></tr>";
                form += "<tr><td>" + "<select name='expenseType' id='newExpense'>";
                for (i = 0; i < parsed.length; i++) {
                    form += "<option value=" + parsed[i].name +">" + parsed[i].name + "</option>";
                  }
                form += "</select>" + "</td></tr>"              
                form += "<tr><td><button onclick='saveEvent()'>ADD</button><button class='deleteEvent' onclick='closeForm()'>X</button></td></tr>";
                document.getElementById("events").innerHTML += form;
                document.getElementById("newEvent").focus();
        }
    })

}

//Not very pretty, but it works
function closeForm(){
    var table = document.getElementById("events");
    var rowCount = table.rows.length;
    table.deleteRow(rowCount -1);
    table.deleteRow(rowCount -2);
    table.deleteRow(rowCount -3);
    table.deleteRow(rowCount -4);
    table.deleteRow(rowCount -5);

}

function saveEvent() {
    var event = document.getElementById("newEvent");
    var date = globalCalendar.state.currentDate.toLocaleDateString();
    var amount = document.getElementById("newAmount");
    var expenseType = document.getElementById("newExpense");

    $.ajax({
        crossOrigin: true,
        type: "POST",
        url: "http://127.0.0.1:8000/saveEvent/",
        dataType: "json",
        async: true,
        headers: { "X-CSRFToken": '{{ csrf_token }}'},
        data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                "event": event.value,
                "date": date,
                "amount": amount.value,
                "expenseType": expenseType.value},
        success: function (json){
            closeForm();
            globalCalendar.addEvent({id: json.id,
                                    title: event.value, 
                                    start: globalCalendar.state.currentDate,
                                    extendedProps:{ amount: amount.value, event_type: expenseType.value,
                                    }
            });
            updateScreen();
        }
    })
}
function deleteEvent(node) {
    parent = node.parentNode.parentNode;
    $.ajax({
        crossOrigin: true,
        type: "POST",
        url: "http://127.0.0.1:8000/deleteEvent/",
        dataType: "json",
        async: true,
        headers: { "X-CSRFToken": '{{ csrf_token }}'},
        data: { csrfmiddlewaretoken: '{{ csrf_token }}',
                "id": parent.id},
        success: function (json){
            globalCalendar.getEventById(parent.id).remove();
            updateScreen();
        }
    })
    
    
}
function updateScreen(){

    $("#events").find("tr:not(:first)").remove();

    var tableString = '';
    var temp = globalCalendar.getEvents();
    for (let i = 0; i < temp.length; i++) {
        if(temp[i].start.toLocaleDateString() == globalCalendar.state.currentDate.toLocaleDateString()){
            tableString += '<tr id="' + temp[i].id + '">';
            tableString += '<td>' + temp[i].title +'</td>';
            tableString += '<td>' + temp[i].start.toLocaleDateString() +'</td>';
            tableString += '<td>' + temp[i].extendedProps.amount +'</td>';
            tableString += '<td>' + temp[i].extendedProps.event_type +'</td>';
            tableString += '<td><button class="deleteEvent" onclick="deleteEvent(this)">X</button></td>';
            tableString += '</tr>';
        }
    }
    document.getElementById("events").innerHTML += tableString;
  };