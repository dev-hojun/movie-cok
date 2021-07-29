$(document).on("click", "input[name='production']", function(){
    thisRadio = $(this);
    if (thisRadio.hasClass("imChecked")) {
        thisRadio.prop('checked', false).removeClass("imChecked");
    } else {
        thisRadio.prop('checked', true);
        thisRadio.parent().siblings().find("input[name='production']").prop('checked', false);
        thisRadio.addClass("imChecked").parent().siblings().find("input[name='production']").removeClass("imChecked");     
    };
})

$(document).on("click", "input[name='acting']", function(){
    thisRadio = $(this);
    if (thisRadio.hasClass("imChecked")) {
        thisRadio.prop('checked', false).removeClass("imChecked");
    } else {
        thisRadio.prop('checked', true);
        thisRadio.parent().siblings().find("input[name='acting']").prop('checked', false);
        thisRadio.addClass("imChecked").parent().siblings().find("input[name='acting']").removeClass("imChecked");     
    };
})

$(document).on("click", "input[name='story']", function(){
    thisRadio = $(this);
    if (thisRadio.hasClass("imChecked")) {
        thisRadio.prop('checked', false).removeClass("imChecked");
    } else {
        thisRadio.prop('checked', true);
        thisRadio.parent().siblings().find("input[name='story']").prop('checked', false);
        thisRadio.addClass("imChecked").parent().siblings().find("input[name='story']").removeClass("imChecked");     
    };
})

$(document).on("click", "input[name='visual']", function(){
    thisRadio = $(this);
    if (thisRadio.hasClass("imChecked")) {
        thisRadio.prop('checked', false).removeClass("imChecked");
    } else {
        thisRadio.prop('checked', true);
        thisRadio.parent().siblings().find("input[name='visual']").prop('checked', false);
        thisRadio.addClass("imChecked").parent().siblings().find("input[name='visual']").removeClass("imChecked");     
    };
})

$(document).on("click", "input[name='ost']", function(){
    thisRadio = $(this);
    if (thisRadio.hasClass("imChecked")) {
        thisRadio.prop('checked', false).removeClass("imChecked");
    } else {
        thisRadio.prop('checked', true);
        thisRadio.parent().siblings().find("input[name='ost']").prop('checked', false);
        thisRadio.addClass("imChecked").parent().siblings().find("input[name='ost']").removeClass("imChecked");     
    };
})