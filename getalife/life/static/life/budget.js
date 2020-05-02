function showContent(callerYear) {

    let el = $( "#budget-year-" + callerYear);

    if(el.attr('class') == "content-inactive"){
        el.addClass('content-active').removeClass('content-inactive');
    }else{
        el.addClass('content-inactive').removeClass('content-active');
    }
}