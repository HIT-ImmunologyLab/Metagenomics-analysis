/**
 * Created by lyk on 2017/5/26 0026.
 */
// var objArr;
var tabIndex = 0;
$(document).ready(function() {

    var pid = decodeURI(location.href.split("?")[1].split("=")[1]);

    console.log(pid);

    pid = decodeURI(pid);
    console.log(pid);

    $("#bacteria_name").html(pid);

    // $.ajax({
    //     url: "admin/getRingData.php",
    //     type: "POST",
    //     dataType: "JSON",
    //     data: {
    //         "pid": pid
    //     },
    //     success: function(data) {
    //         data = eval(data);
    //         if ( data ) {
    //             var objArr = ls.init("ringGraph", data);
    //             AddClickEvent(objArr);
    //         } else {
    //             $("#ringGraph").html("获取不到任何数据");
    //         }
    //     },
    //     error: function() {
    //         alert("数据获取出错！");
    //     }
    // });

    $("#changeGraph").click(function() {
        if ( tabIndex ) {
            $("#tab1").removeClass("hide");
            $("#tab2").addClass("hide");
            tabIndex = 0;
            $(this).html("self attacking");
        } else {
            $("#tab2").removeClass("hide");
            $("#tab1").addClass("hide");
            tabIndex = 1;
            $(this).html("spacer graph");
        }
    });

});

function AddClickEvent(arr) {
    arr.forEach(function(curObj, index, objArr) {
        var _this = curObj,
            allMsg;
        _this.obj.click(function() {
            $("#secondPanel").removeClass("hide");
            for ( var i=0; i<arr.length; i++ ) {
                arr[i].obj.attr("stroke-with", 0);
            }
            _this.obj.attr("stroke-width", 2);
            allMsg = "";
            allMsg += "start position: " + _this.data.startPos + "<br/>";
            allMsg += "end position: " + (parseInt(_this.data.startPos)+parseInt(_this.data.length)) + "<br/>";
            allMsg += "plus minus chain: " + _this.data.pmc + "<br/>";
            $("#allMsg").html(allMsg);
            $("#ringLineGraph").html("");
            $("#selfLine").html("");
            getLineGraph(_this.data.id);
        });
    });
}

function getLineGraph(id) {
    id = parseInt(id);
    $.ajax({
        url: "admin/getLineData.php",
        type: "POST",
        dataType: "JSON",
        data: {
            "id": id
        },
        success: function(data) {
            console.log(data['two']);
            data = eval(data);
            if ( data ) {
                var lineArr = lsLine.init("ringLineGraph", data['one']);
                //AddClickEvent2(lineArr);
                var arrowArr = lsArrow.init("selfLine", data['two']);
                //AddClickEvent3(arrowArr);
                if ( lineArr ) {
                    $("#detailMsg").removeClass("hide");
                    var protein = [], spacer = [], msg1, msg2;
                    console.log(!protein && !spacer);
                    for ( var i=0; i<lineArr.length; i++ ) {
                        if ( lineArr[i].type ) {
                            spacer.push(lineArr[i].data);
                        } else {
                            protein.push(lineArr[i].data);
                        }
                    }
                    if ( protein ) {
                        msg1 = "check protein message:<a href=''>protein</a><br/>";
                    }
                    if ( spacer ) {
                        msg2 = "check spacer message:<a href=''>spacer</a><br/>";
                    }
                    $("#detailMsg").html(msg1+msg2);
                }
            } else {
                $("#ringLineGraph").html("获取不到任何数据");
            }
        },
        error: function() {
            alert("数据获取失败！");
        }
    });
}
/*
function AddClickEvent2(arr) {
    arr.forEach(function(curObj, index, objArr) {
        var _this = curObj,
            detailMsg;
        _this.obj.click(function() {
            detailMsg = "";
            $("#detailMsg").removeClass("hide");
            $("#detailMsg").html("");
            if ( _this.type=="0" ) {
                // detailMsg += "<font color='#a52a2a'>bacteria_name: </font>" + _this.data.bacteria_name + "<br/>";
                // detailMsg += "<font color='#a52a2a'>domain start position: </font>" + _this.data.startPos + "<br/>";
                // detailMsg += "<font color='#a52a2a'>domain end position:</font>" + _this.data.endPos + "<br/>";
                // detailMsg += "<font color='#a52a2a'>plus minus chain:</font>" + _this.data.pmc + "<br/>";
                // detailMsg += "<font color='#a52a2a'>hit_type: </font>" + _this.data.hit_type + "<br/>";
                // detailMsg += "<font color='#a52a2a'>accessionID:</font>" + _this.data.accessionID + "<br/>";
                // detailMsg += "<font color='#a52a2a'>actual start position:</font>" + (parseInt(_this.data.startPos)+parseInt(_this.data.logicalStart)) + "<br/>";
                // detailMsg += "<font color='#a52a2a'>actual end position:</font>" + (parseInt(_this.data.startPos)+parseInt(_this.data.logicalEnd)) + "<br/>";
                // detailMsg += "<font color='#a52a2a'>evalue:</font>" + _this.data.evalue + "<br/>";
                // detailMsg += "<font color='#a52a2a'>hit-score:</font>" + _this.data['hit-score'] + "<br/>";
                // detailMsg += "<font color='#a52a2a'>accession:</font>" + _this.data.accession + "<br/>";
                // detailMsg += "<font color='#a52a2a'>protein_name:</font>" + _this.data.protein_name + "<br/>";
                // detailMsg += "<font color='#a52a2a'>description:</font>" + _this.data.description + "<br/>";
                // detailMsg += "<font color='#a52a2a'>dna:</font>" + _this.data.dna + "<br/>";
                // detailMsg += "<font color='#a52a2a'>protein sequence:</font>" + _this.data.protein_sequence + "<br/>";
                table = $("<table class='table table-border table-bordered' id='tableMsg'></table>");
                table.append("<tr><td>bacteria_name</td><td>" + _this.data.bacteria_name + "</td></td></tr>");
                table.append("<tr><td>domain start position</td><td>" +_this.data.startPos + "</td></td></tr>");
                table.append("<tr><td>domain end position</td><td>" + _this.data.endPos + "</td></td></tr>");
                table.append("<tr><td>plus minus chain</td><td>" + _this.data.pmc + "</td></td></tr>");
                table.append("<tr><td>hit_type</td><td>" + _this.data.hit_type + "</td></td></tr>");
                table.append("<tr><td>accessionID</td><td>" + _this.data.accessionID + "</td></td></tr>");
                table.append("<tr><td>actual start position</td><td>" + (parseInt(_this.data.startPos)+parseInt(_this.data.logicalStart)) + "</td></td></tr>");
                table.append("<tr><td>actual end position</td><td>" + (parseInt(_this.data.startPos)+parseInt(_this.data.logicalEnd)) + "</td></td></tr>");
                table.append("<tr><td>evalue</td><td>" +  _this.data.evalue + "</td></td></tr>");
                table.append("<tr><td>hit-score</td><td>" + _this.data['hit-score'] + "</td></td></tr>");
                table.append("<tr><td>accession</td><td> _this.data.accession</td></td></tr>");
                table.append("<tr><td>protein_name</td><td>" + _this.data.protein_name + "</td></td></tr>");
                table.append("<tr><td>description</td><td>" + _this.data.description + "</td></td></tr>");
                table.append("<tr><td>dna</td><td>" + _this.data.dna + "</td></td></tr>");
                table.append("<tr><td>protein sequence</td><td>" + _this.data.protein_sequence + "</td></td></tr>");
                // $("#detailMsg").html(detailMsg);
                $("#detailMsg").append(table);
            } else if ( _this.type=="1" ) {
                table = $("<table class='table table-border table-bordered' id='tableMsg'></table>");
                // detailMsg += "<font color='#a52a2a'>id:</font>" + _this.data.id + "<br/>";
                // detailMsg += "<font color='#a52a2a'>start position:</font>" + _this.data.startPos + "<br/>";
                // detailMsg += "<font color='#a52a2a'>len:</font>" + _this.data.len + "<br/>";
                // detailMsg += "<font color='#a52a2a'>dna:</font>" + _this.data.dna + "<br/>";
                table.append("<tr><td>id</td><td>" + _this.data.id + "</td></td></tr>");
                table.append("<tr><td>start position</td><td>" +_this.data.startPos + "</td></td></tr>");
                table.append("<tr><td>length</td><td>" + _this.data.len + "</td></td></tr>");
                table.append("<tr><td>dna</td><td>" + _this.data.dna + "</td></td></tr>");
                // $("#detailMsg").html(detailMsg);
                $("#detailMsg").append(table);
            }

        });
    });
}
function AddClickEvent3(arr) {

}
*/