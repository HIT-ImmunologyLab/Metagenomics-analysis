/**
 * Created by lyk on 2017/6/10 0010.
 */

$(document).ready(function(){
    // click prediction action, change action panel
    $(".hi-icon").click(function(){
        $(".hi-icon").removeClass("a-active");
        $(this).addClass("a-active");
        $(".action1").removeClass("a-show");
        var index = $(this).attr("control");
        console.log(index);
        $(".action1").eq(index).addClass("a-show");
        if ( index!=1 ) {
            $("#ringPanel").addClass("a-hide");
            $("#LineGraph").addClass("a-hide");
        }
    });

    var files = $(".a-file");
    files.change(function(){
        var val = $(this).val();
        $(this).parent().prev().val(val);
        if ( val!=null && val!="" ) {
            $(".a-tip").eq(0).html("");
        }
    });

    $("#submit").click(function(e) {
        var text = $.trim($(".a-input").eq(0).val());
        if ( text==null || text=="" ) {
            $(".a-tip").eq(0).html("You have to choose a file");
            e.preventDefault();
        }
    });
});