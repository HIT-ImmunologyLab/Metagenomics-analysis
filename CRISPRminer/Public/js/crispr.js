/**
 * Created by lyk on 2017/6/10 0010.
 */
var limitNumber = 0, baseHeight = 30, value = null, menuHeight = 0, specieNumber = 0, genusNumber = 0;
$(document).ready(function(){

    $("#class").change(function() {
        console.log(1);
        if ( $(this).val()=='specie' ) {
            $("#tab2").addClass("a-hide");
            $("#tab1").removeClass("a-hide");
        } else if ( $(this).val()=='genus' ) {
            $("#tab1").addClass("a-hide");
            $("#tab2").removeClass("a-hide");
        }
    });

    $(".checkBtn").click(function(){
        var span = $(this).find("span").eq(0);
        $(".checkBtn span").removeClass("glyphicon-ok");
        if ( span.hasClass("glyphicon-ok") ) {
            span.removeClass("glyphicon-ok");
        } else {
            value = $(this).attr("value");
            span.addClass("glyphicon-ok");
        }
    });

    appenLiToUl(limitNumber);

    var menu = document.getElementById("menu");

    console.log(menu);

    var scrollFunc = function(e) {
        var direct=0;
        e=e || window.event;
        var value;
        if(e.wheelDelta){//IE/Opera/Chrome
            value=e.wheelDelta;
        }
        if (e.detail){//Firefox
            value=e.detail;
        }
        var height;
        height = $("#menu").height();
        var top = $("#menu").offset().top;
        var winH = document.documentElement.clientHeight;
        var scrollTop = document.body.scrollTop | document.documentElement.scrollTop;
        console.log(height+top-scrollTop);
        if ( height+top-scrollTop<winH/2 ) {
            appenLiToUl(limitNumber);
        }

    };

    $(document).scroll(function(){
        scrollFunc(this);
    });

    $(".hi-icon").click(function(){
        // tab styles
        $(".hi-icon").removeClass("a-active");
        $(this).addClass("a-active");

        // tab context style
        var prev = $(".a-show");
        prev.slideUp(1000);
        var index = prev.attr("control");
        $(".action1").eq(index).removeClass("a-show");
        index = $(this).attr("control");
        console.log(index);
        setTimeout(1000);
        $(".action1").eq(index).slideDown(1000);
        $(".action1").eq(index).addClass("a-show");
    });

    $("#action1").eq(0).slideDown(1000);


    $("#searchBtn").click(function() {
        var text = $("#searchText").val();

        console.log(value);
        console.log(text);

        if ( text && value) {
            $("#tip1").html("");
            $("#tip2").html("");
            $.ajax({
                url: "__URL__/getSearchBacteria",
                type: "POST",
                data: {
                    "text": text,
                    "value": value,
                },
                success: function(data) {
                    data = eval(data);
                    console.log(data);
                    if ( data.length ) {
                        $("#result").html("");
                        var ul = $("<ul class='a-ul'></ul>");
                        for ( var i=0; i<data.length; i++ ) {
                            var li = $("<li class='item'><a href='__URL__/graph/pid/"+data[i].bacteria_id+"' target='_blank'>"+data[i].name+"</a></li>");
                            ul.append(li);
                        }
                        $("#result").append(ul);
                    } else {
                        $("#result").html("There is no record in database!");
                    }
                },
                error: function() {
                    alert("error!");
                }
            });
        } else {
            if ( !text ) {
                $("#tip1").html("Please input what you want to search");
            } else {
                $("#tip1").html("");
            }
            if ( !value ) {
                $("#tip2").html("Please check one type");
            } else {
                $("#tip2").html("");
            }
        }

    });

});

function appenLiToUl(limit) {
    $.ajax({
        url: "__URL__/handleCrispr",
        type: "POST",
        async: false,
        data: {
            "limit": limit,
        },
        success: function(data) {
            data = eval(data);
            if ( data ) {
                for ( var i=0; i<data.length; i++ ) {
                    var li = $("<li class='item"+data[i]['level']+"'></li>");
                    if ( data[i]['is_last']=='1' ) {
//                            li.append('<a href="javascript:void(0)" onclick="changeIcon(this)" class="glyphicon glyphicon-plus"></a>\
//                                <a href="__URL__/graph/pid/'+data[i]['bacteria_id']+'">'+data[i]['name']+'</a>\
//                            ');
                        li.append('<a href="__URL__/graph/pid/'+data[i]['bacteria_id']+'" target="_blank">'+data[i]['name']+'</a>\
                            ');
                    } else {
                        li.append('<a href="javascript:void(0)" onclick="changeIcon(this)" class="glyphicon glyphicon-minus"></a>\
                                <span>'+data[i]['name']+'</span><span style="margin-left: 20px; color: #f00;">('+data[i]['genomes']+' genomes)</span>\
                            ');
                    }
                    $("#menu").append(li);
                }
                limitNumber ++;
//                    menuHeight = $("#menu").height();
//                    console.log(menuHeight);
            }


        },
        error: function() {
            alert("error!");
        }
    });

}