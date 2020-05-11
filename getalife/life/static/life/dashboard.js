//setup page
var today = new Date();
var year = today.getFullYear();
var month = today.getMonth();
var day = today.getDate();
var monthsInText = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"];
var selectedMonth = monthsInText[month];
document.getElementById("year").innerHTML = year;
document.getElementById("currentDate").innerHTML = selectedMonth + " " + day;

var accountID = 1;
accounts = getrecord("BudgetAccount",-1)
if (accounts.length > 0) accountID = accounts[0].id

var graphType = 1;

addType = 4;

income = [];
expense = [];
balances = [];

today = year + "-" + month + "-" + day
editmonth = accounts[0].month
edityear = accounts[0].name
editID = accounts[0].id

makeaccounts();

refresh();

addTypes();

//document.getElementById("monthpay").value = month + "/" + day + "/" + year
//document.getElementById("monthcost").value = month + "/" + day + "/" + year

document.getElementById("monthpay").value = day
document.getElementById("monthcost").value = day

//setup
function makeaccounts() {
	for(i=0; i<accounts.length; i++) {
		var val = accounts[i].id + "','" + accounts[i].month + "','" + accounts[i].name + "','" + accounts[i].id
		addButton("Budget: " + accounts[i].description, val,3)
	}
}

function addTypes() {
	
	var expenseT = getrecord("BudgetExpense", -1);
	
	var options = ""
	
	for(i=0; i<expenseT.length; i++) {
		if(accountID == expenseT[i].account) options = options + "<option value='" + expenseT[i].name + "'> " + expenseT[i].name + " </option>";
	}
	
	document.getElementById("newExpense").innerHTML = options;
}

function refresh() {
	getdata();
	makegraph();
	balancedisplay();
	createlistings();
}

function getdata() {
	income = getrecord("BudgetIncome",-1);
	expense = getEvents()
	
	income = validincome()
	expense = validexpense()

	balances = createbalances(balances);
}

function validincome() {
	var ret = []
	var a =0
	for(i=0; i<income.length; i++) {
		if(income[i].account == editID) {
			ret[a] = income[i]
			a += 1
		}
	}
	 
	return ret
}

function validexpense() {
	var ret = []
	var a =0
	for(i=0; i<expense.length; i++) {
		if(parseInt(expense[i].start_date.split("-")[1]) == parseInt(editmonth) && parseInt(expense[i].start_date.split("-")[0]) == parseInt(edityear)) {
			ret[a] = expense[i]
			a += 1
		}
	}
	 
	return ret
}

//switch accounts
function switchaccounts(id, newmonth, newyear, newID) {
	accountID = id;
	editmonth = newmonth
	edityear = newyear
	editID = newID
	
	addTypes();
	refresh();
}

//balance display
function balancedisplay() {
	
	var gain = 0;
	var loss = 0;
	
	for(i=0; i<expense.length; i++) {
	loss += parseFloat(expense[i].amount);
	}
	
	for(i=0; i<income.length; i++) {
	gain += parseFloat(income[i].income);
	}
	
	var c = document.getElementById("myBalance");
	var context = c.getContext("2d");
	context.clearRect(0, 0, c.width, c.height);
	context.beginPath();
	
	context.fillStyle="black";
	
	context.textAlign = "left";
	context.font = "20px Arial";
	context.fillText("Current Balance", 5, 20);
	
	context.textAlign = "center";
	var gaintext = "$" + gain;
	context.fillText(gaintext, 55, 110);
	
	var losstext = "$" + loss;
	context.fillText(losstext, 55, 150);
	
	var total = gain - loss;
	var totaltext = "$" + total;
	context.font = "25px Arial";
	context.fillText(totaltext, 55, 60);
	
	var max = gain;
	if (loss > gain) max = loss;
	
	context.fillStyle="green";
	context.fillRect(120,90,(gain/max*300),20);
	
	context.fillStyle="red";
	context.fillRect(120,130,(loss/max*300),20);
}

//listing display
function createlistings() {
	$( ".listingButton" ).remove();

	$( ".budgetReportButton" ).remove();

	for(i=0; i<income.length; i++) {
		var text = "Income: " + income[i].name + " , $" + income[i].income
		addButton(text,income[i].id,2)
	}
	
	for(i=0; i<expense.length; i++) {
		var text = "Expense: " + expense[i].event_name + " , $" + expense[i].amount + " " + expense[i].start_date
		addButton(text,expense[i].id,1)
	}
}

//create graphs based on data
function createbalances() {
	
	b = []
	
	var nextmonth= editmonth + 1
	var maxdays = daysBetween("2020-"+ nextmonth + "-1","2020-"+ editmonth + "-1");
	
	for(i=0; i<maxdays+1; i++) {
		b[i] = 0;
	}
	
	for(i=0; i<expense.length; i++) {
		var sday = expense[i].start_date.split("-")[2]
		if (sday <= maxdays && sday > 0) b[sday] -= parseFloat(expense[i].amount);
	}
	
	for(i=0; i<income.length; i++) {
		var sday = income[i].description.split("-")[0]
		if (sday <= maxdays && sday > 0) b[sday] += parseFloat(income[i].income);
	}
	
	for(i=0; i<b.length - 1; i++) {
	var v1 = b[i+1];
	var v2 = b[i];
	if (typeof b[i+1] == "string") v1  = parseFloat(b[i+1]);
	if (typeof b[i] == "string") v2  = parseFloat(b[i]);
	b[i] = v2;
	b[i+1] = v1 + v2;
	}
	
	return b;
}

//graph creation
function nextgraph() {
	graphType += 1;
	if (graphType > 4) graphType = 1;

	makegraph();
}

function makegraph() {
	var c = document.getElementById("myGraph");
	var context = c.getContext("2d");
	context.clearRect(0, 0, c.width, c.height);
	context.beginPath();
	
	if(graphType == 1) drawbalanceline("myGraph", balances);
	if(graphType == 2) drawincomeline("myGraph", income);
	if(graphType == 3) drawexpensepie("myGraph", expense);
	if(graphType == 4) drawexpenseline("myGraph", expense);
}

function drawbalanceline(canvasID,b) {

	var c = document.getElementById(canvasID);
	var context = c.getContext("2d");
	
	
	//if (b.length < 1) return 0;
	
	var max = b[0];
	var min = b[0];
	var scale = 1;
	
	for (i = 0; i < b.length; i++) {
		if (b[i] > max) max = b[i];
		if (b[i] < min) min = b[i];
	}
	
	var lines = Math.abs(Math.round((max - min) / 5 / 20) * 20)
	if (lines < 2) lines = 2;
	
	scale = c.height * 0.7 / (max - min)
	
	context.textAlign = "right";
	context.font = "15px Arial";
	
	for (i = min - lines; i < max; i += lines) {
		var h = c.height - (i - min) * scale - c.height/10
	
		drawline(canvasID, "#E8E8E8", 0, h, c.width, h);
		if(h < c.height - 15) context.fillText(i, c.width - 2, h - 2);
	}
	
	
	for (i = 1; i < b.length; i++) {
		drawline(canvasID, "#000000", (i-1) * (c.width*0.9/(b.length)), c.height - (b[i-1] - min) * scale - c.height/10, i * (c.width*0.9/(b.length)), c.height - (b[i] - min) * scale - c.height/10);
	}
	
	context.textAlign = "left";
	context.font = "20px Arial";
	context.fillText("Net Change Monthly", 5, 20);

}

function drawincomeline(canvasID, income) {
	
	var c = document.getElementById(canvasID);
	var context = c.getContext("2d");
	
	g = []
	
	var nextmonth= editmonth + 1
	var maxdays = daysBetween("2020-"+ nextmonth + "-1","2020-"+ editmonth + "-1");
	
	for(i=0; i<maxdays+1; i++) {
		g[i] = 0;
	}
	
	for(i=0; i<income.length; i++) {
		var sday = income[i].description.split("-")[0]
		if (sday <= maxdays && sday > 0) g[sday] += parseFloat(income[i].income);
	}
	
	var max = g[0];
	var min = g[0];
	var scale = 1;
	
	for(i=0; i<maxdays; i++) {
		if (g[i] > max) max = g[i];
		if (g[i] < min) min = g[i];
	}
	
	var lines = Math.abs(Math.round((max - min) / 5 / 20) * 20)
	
	if (lines < 2) lines = 2;
	
	scale = c.height * 0.7 / (max - min)
	
	context.textAlign = "right";
	context.font = "15px Arial";
	
	for (i = 0; i < max; i += lines) {
		var h = c.height - (i - min) * scale - c.height/10
	
		drawline(canvasID, "#E8E8E8", 0, h, c.width, h);
		if(h < c.height - 15) context.fillText(i, c.width - 2, h - 2);
	}
	
	
	for (i = 1; i < g.length; i++) {
		drawline(canvasID, "#000000", (i-1) * (c.width/(12)), c.height - (g[i-1] - min) * scale - c.height/10, i * (c.width/(12)), c.height - (g[i] - min) * scale - c.height/10);
	}
	
	context.textAlign = "left";
	context.font = "20px Arial";
	context.fillText("Income Monthly", 5, 20);
}

function drawexpenseline(canvasID, expense) {
	
	var c = document.getElementById(canvasID);
	var context = c.getContext("2d");
	
	g = []
	
	var nextmonth= editmonth + 1
	var maxdays = daysBetween("2020-"+ nextmonth + "-1","2020-"+ editmonth + "-1");
	
	for(i=0; i<maxdays+1; i++) {
		g[i] = 0;
	}
	
	for(i=0; i<expense.length; i++) {
		var sday = expense[i].start_date.split("-")[2]
		if (sday <= maxdays && sday > 0) g[sday] += parseFloat(expense[i].amount);
	}
	
	var max = g[0];
	var min = g[0];
	var scale = 1;
	
	for(i=0; i<maxdays; i++) {
		if (g[i] > max) max = g[i];
		if (g[i] < min) min = g[i];
	}
	
	var lines = Math.abs(Math.round((max - min) / 5 / 20) * 20)
	
	if (lines < 2) lines = 2;
	
	scale = c.height * 0.7 / (max - min)
	
	context.textAlign = "right";
	context.font = "15px Arial";
	
	for (i = 0; i < max; i += lines) {
		var h = c.height - (i - min) * scale - c.height/10
	
		drawline(canvasID, "#E8E8E8", 0, h, c.width, h);
		if(h < c.height - 15) context.fillText(i, c.width - 2, h - 2);
	}
	
	
	for (i = 1; i < g.length; i++) {
		drawline(canvasID, "#000000", (i-1) * (c.width/(12)), c.height - (g[i-1] - min) * scale - c.height/10, i * (c.width/(12)), c.height - (g[i] - min) * scale - c.height/10);
	}
	
	context.textAlign = "left";
	context.font = "20px Arial";
	context.fillText("Spending Monthly", 5, 20);
}

function drawexpensepie(canvasID, expense) {
	var c = document.getElementById(canvasID);
	var context = c.getContext("2d");
	context.font = "20px Arial";
	context.textAlign = "left";
	context.fillText("Spending Areas", 5, 20);

	context.arc(c.width - c.width/3, c.height/2, c.height/3, 0, 2 * Math.PI);
	context.stroke();
	
	var totalexpense = 0;
	var expensetype = [];
	var expensetotal = [];
	
	for(i=0; i<expense.length; i++) {
		var a = expensetype.length
		for (x=0; x< expensetype.length; x++) {
			if (expensetype[x] == expense[i].event_type) {
				a = x;
				x = 9999999;
			}
		}
		
		if (a == expensetype.length) expensetotal[a] = 0
		expensetype[a] = expense[i].event_type
		expensetotal[a] += parseFloat(expense[i].amount);
		totalexpense += parseFloat(expense[i].amount);
	}
	
	var total = 0;
	for(i=0; i<expensetype.length; i++) {
		if (expensetotal[i] > 0) {
			//drawline(canvasID, "#000000", c.width - c.width/3, c.height/2, c.width - c.width/3 + c.height/3 * Math.sin(total), c.height/3 * Math.cos(total) + c.height/2);
			total += (expensetotal[i]/totalexpense) * (2 * Math.PI);
			drawline(canvasID, "#000000", c.width - c.width/3, c.height/2, c.width - c.width/3 + c.height/3 * Math.sin(total), c.height/3 * Math.cos(total) + c.height/2);
		}
	}
	
	var a = 0;
	for(i=0; i<expensetype.length; i++) {
		context.textAlign = "left";
		var text = expensetype[i] + ": $" + expensetotal[i];
		context.fillText(text, 5, 80 + i * 40);
	}

}

function drawline(canvasID, style ,x1, y1, x2, y2) {
	var c = document.getElementById(canvasID);
	var context = c.getContext("2d");
	context.strokeStyle = style;
	context.moveTo(x1,y1);
	context.lineTo(x2,y2);
	context.stroke();
	context.closePath();
	context.beginPath();
}

//Button generation
function addButton(text,val,type) {
	var para = document.createElement("button");
	var node = document.createTextNode(text);
	
	var att = document.createAttribute("onclick");
	var clickadd = ""
	if (type==1) clickadd = "deleteEvent('"+val+"')";
	if (type==2) clickadd = "deletepay('"+val+"')";
	if (type==3) clickadd = "switchaccounts('"+val+"')";
	att.value = clickadd
	para.setAttributeNode(att);
	
	var att2 = document.createAttribute("class");
	att2.value = "listingButton";
	if (type==3) att2.value = "listingButton2";
	para.setAttributeNode(att2);
	
	para.appendChild(node);

	var element = document.getElementById("scrollarea");
	if (type==3) element = document.getElementById("accountsarea")
	element.appendChild(para);
	
	//var bar = document.createElement("div");
	//element.appendChild(bar);
}

//SQL fetching
function testjquery() {
if (window.jQuery) {
alert('jQuery is loaded');
} else {
alert('jQuery is not loaded');
}}


function getrecord(loc,id) 
{
var protocol = 'http://';
var domainName = '127.0.0.1';
var port = ':8000';
var path = '/api/';
var model = loc + '/';
var format = '?format=json';

let ret = undefined;

var surl = protocol + domainName + port + path + model + id + format
if (id == -1) surl = protocol + domainName + port + path + model + format

$.ajax({
	async: false,
	headers: {
		'Access-Control-Allow-Origin': protocol + domainName
	},

	type: "GET",
	data: { csrfmiddlewaretoken: '{{ csrf_token }}'},
	url: surl,

}).done(function(json) { ret = json; });

return ret;

}

function pushrecord(loc,datains) 
{
var protocol = 'http://';
var domainName = '127.0.0.1';
var port = ':8000';
var path = '/api/';
var model = loc+'/';
let ret = undefined;

$.ajax({
	async: false,
	headers: {
		'Access-Control-Allow-Origin': protocol + domainName,
		'Cookie': document.cookies,
		'X-CSRFToken' : getCookie("csrftoken")
	},

	type: "POST",
	data: datains,
	dataType: 'json',
	url: protocol + domainName + port + path + model,

}).done(function(status) { ret = status; });

return ret;

}

function deleterecord(loc,id) 
{
var protocol = 'http://';
var domainName = '127.0.0.1';
var port = ':8000';
var path = '/api/';
var model = loc+'/';
let ret = undefined;

$.ajax({
	async: false,
	headers: {
		'Access-Control-Allow-Origin': protocol + domainName,
		'Cookie': document.cookies,
		'X-CSRFToken' : getCookie("csrftoken")
	},

	type: "DELETE",
	url: protocol + domainName + port + path + model + id,

}).done(function(status) { ret = status; });

return ret;

}

function getCookie(cname) {
  var name = cname + "=";
  var ca = document.cookie.split(';');
  for(var i = 0; i < ca.length; i++) {
	var c = ca[i];
	while (c.charAt(0) == ' ') {
	  c = c.substring(1);
	}
	if (c.indexOf(name) == 0) {
	  return c.substring(name.length, c.length);
	}
  }
  return "";
}

//preset defaults
function defaultinput(id) {
	if (id == 1) {
		document.getElementById("source").value = "Food";
		document.getElementById("source2").value = 10;
		document.getElementById("costbutton").innerHTML = "FOOD COST";
		addType = 1;
	}
	if (id == 2) {
		document.getElementById("source").value = "Housing";
		document.getElementById("source2").value = 100;
		document.getElementById("costbutton").innerHTML = "HOUSING COST";
		addType = 2;
	}
	if (id == 3) {
		document.getElementById("source").value = "Entertainment";
		document.getElementById("source2").value = 50;
		document.getElementById("costbutton").innerHTML = "ENTERTAINMENT COST";
		addType = 3;
	}
	if (id == 4) {
		document.getElementById("source").value = "Travel";
		document.getElementById("source2").value = 40;
		document.getElementById("costbutton").innerHTML = "TRAVEL COST";
		addType = 4;
	}
	if (id == 5) {
		document.getElementById("source").value = "Other";
		document.getElementById("source2").value = 20;
		document.getElementById("costbutton").innerHTML = "OTHER COST";
		addType = 5;
	}
	if (id == 11) {
		document.getElementById("source3").value = "Pay";
		document.getElementById("source4").value = 100;
	}
	if (id == 12) {
		document.getElementById("source3").value = "Pay";
		document.getElementById("source4").value = 500;
	}
	if (id == 13) {
		document.getElementById("source3").value = "Pay";
		document.getElementById("source4").value = 1250;
	}
}

function addcost() {
	var sname = document.getElementById("source").value
	var sexpenseType = document.getElementById("newExpense").value
	var sdate = editmonth + "/" + document.getElementById("monthcost").value + "/" + edityear
	var sexpense = document.getElementById("source2").value
	console.log(sname + ", " + sdate + ", " + sexpense + ", " + sexpenseType)
	//if(document.getElementById("source2").value > 0) pushrecord("BudgetExpense", data);
	if(sexpense > 0) saveEvent(sname.toString(), sdate.toString(), sexpense, sexpenseType.toString());
	document.getElementById("source").value = "";
	document.getElementById("source2").value = "";
	
	refresh();
}

function addpay() {
	var sday = document.getElementById("monthpay").value
	var sder = sday + "-" + edityear
	var data = {"id":1, "name": document.getElementById("source3").value, "description": sder, "account": editID, "incomeType": 1, "month": editmonth, "income": document.getElementById("source4").value};
	if(document.getElementById("source4").value > 0) pushrecord("BudgetIncome", data);
	//document.getElementById("source3").value = "";
	document.getElementById("source4").value = 0;
	
	refresh();
}

function deletecost(id) {
	deleterecord("BudgetExpense", id);
	
	refresh();
}

function deletepay(id) {
	deleterecord("BudgetIncome", id);
	
	refresh();
}

function getEvents(){
	var ret = []
	
	$.ajax({
		crossOrigin: false,
		type: "GET",
		url: "http://127.0.0.1:8000/event",
		dataType: "json",
		async: false,
		data: { csrfmiddlewaretoken: '{{ csrf_token }}'},
		success: function (json){
			parsed = JSON.parse(json);
			for (let i = 0; i < parsed.length; i++) {
				ret[i] = parsed[i].fields
				ret[i].id = parsed[i].pk
			}
		}
	})
	
	return ret;
}

function saveEvent(name, date, amount, type) {
	$.ajax({
		crossOrigin: true,
		type: "POST",
		url: "http://127.0.0.1:8000/saveEvent/",
		dataType: "json",
		async: false,
		headers: { "X-CSRFToken": '{{ csrf_token }}'},
		data: { csrfmiddlewaretoken: '{{ csrf_token }}',
				"event": name,
				"date": date,
				"amount": amount,
				"expenseType": type},
		success: function (json){}
	})
}

function deleteEvent(id) {
	$.ajax({
		crossOrigin: true,
		type: "POST",
		url: "http://127.0.0.1:8000/deleteEvent/",
		dataType: "json",
		async: false,
		headers: { "X-CSRFToken": '{{ csrf_token }}'},
		data: { csrfmiddlewaretoken: '{{ csrf_token }}',
				"id": id},
		success: function (json){}
	})
	
	refresh();
}

//date handling
function daysBetween(date1, date2) {
	const oneDay = 24 * 60 * 60 * 1000; // hours*minutes*seconds*milliseconds
	const firstDate = new Date(date1.split("-")[0], date1.split("-")[1], date1.split("-")[2]);
	const secondDate = new Date(date2.split("-")[0], date2.split("-")[1], date2.split("-")[2]);

	return Math.round((firstDate - secondDate) / oneDay);
}
