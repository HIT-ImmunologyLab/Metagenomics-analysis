/**
 * Created by lyk on 2017/6/17 0017.
 */
/**
 * Created by lyk on 2017/5/26 0026.
 */



var lsMul = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _id: null, // svg对象的父节点的id
    _parent: null, // svg对象的父对象
    _proteinData: null, // 蛋白质数据
    _dataNum: null,
    _svgProto: null, // svg javascript原生对象
    _svg: null, // svg对象
    _arrowLen: 60,
    _arrowH: 20,
    _marginH: 30,
    _arc: null,

    init: function(id, data, arcname) {
        lsMul._id = id;
        lsMul._arc = arcname;
        lsMul._parent = $("#"+lsMul._id);
        lsMul._svgProto = document.createElementNS(lsMul.SVG_NS, 'svg');
        lsMul._proteinData = data;
        lsMul._dataNum = data.length;
        lsMul._svg = $(lsMul._svgProto);
        lsMul._svg.attr({
            "width": 11*lsMul._arrowLen,
            "height": lsMul._marginH*lsMul._dataNum,
        });
        var height = 0;
        if ( data.length ) {
            for ( var i=0; i<data.length; i++ ) {
                this.drawCaseProteinLine(data[i], height);
                height += lsMul._marginH;
            }
        }

        lsMul._parent.append(lsMul._svg);

    },

    drawCaseProteinLine: function(data, height) {
        // var len = data.length;
        // var id = data[len-1][0];
        //data.splice(len-2, 1); // 删除最后一个元素
        var dir;
        if ( data ) {
            var type, flag, startPos1 = lsMul._arrowLen*5, startPos2 = startPos1;

            var mainDir = "+";
            if ( data["mid"].hasOwnProperty("position") ) {
                var rep = data["mid"]['position'].split("(")[1];
                var rep2 =rep.split(")")[0];
                mainDir = rep2;
            }

            this.drawArrow(startPos1, height, 1, lsMul._arc, mainDir);

            if ( data['before'] && data['before'].length ) {
                for ( var j=0; j<data['before'].length; j++ ) {
                    startPos1 -= lsMul._arrowLen;
                    var rep = data['before'][j][2].split("(")[1];
                    var rep2 = rep.split(")")[0];
                    dir = rep2;
                    this.drawArrow(startPos1, height, 0, data['before'][j][1], dir);
                }
            }

            if ( data['after'] && data['after'].length ) {
                for ( var j=0; j<data['after'].length; j++ ) {
                    startPos2 += lsMul._arrowLen;
                    var rep = data['after'][j][2].split("(")[1];
                    var rep2 = rep.split(")")[0];
                    dir = rep2;
                    this.drawArrow(startPos2, height, 0, data['after'][j][1], dir);
                }
            }
        }


    },

    // 起始位置 y轴坐标    是否是同源蛋白 蛋白名称    蛋白方向
    drawArrow: function(startPos, height, flag, proteindomain, direction) {
        var description, color = "#fff", textColor = "#000";
        var arrow = $(document.createElementNS(lsMul.SVG_NS, 'path'));
        if ( direction=="+" ) {
            description = ['M', startPos, height, 'L', startPos+lsMul._arrowLen-10, height, 'L', startPos+lsMul._arrowLen, height+lsMul._arrowH/2, 'L', startPos+lsMul._arrowLen-10, height+lsMul._arrowH, 'L', startPos, height+lsMul._arrowH, 'Z'];
        } else {
            description = ['M', startPos, height+lsMul._arrowH/2, 'L', startPos+10, height, 'L', startPos+lsMul._arrowLen, height, 'L', startPos+lsMul._arrowLen, height+lsMul._arrowH, 'L', startPos+10, height+lsMul._arrowH, 'Z'];
        }
        if ( flag ) {
            color = "#f00";
            textColor = "#fff";
        } else {
            if ( $.trim(proteindomain)!="NULL" ) {
                color = "#E0FFFF";
            }
        }

        arrow.attr({
            "d": description.join(' '),
            "stroke": "#000",
            "stroke-width": "1",
            "fill": color
        });
        lsMul._svg.append(arrow);
        this.drawText(startPos, textColor, height, proteindomain);
    },

    // 在蛋白质内部写入蛋白名称
    // 起始位置 颜色  y轴坐标    文字
    drawText: function(startPos, color, height, ctx) {
        var text = $(document.createElementNS(lsMul.SVG_NS, "text"));
        text.attr({
            "x": startPos+5,
            "y": height+lsMul._marginH/2,
            "fill": color,
            "font-size": 10,
            "cursor": "pointer"
            // "transform": "rotate(-45 "+(startPos+len/2)+","+(lsMul._center_y-lsMul._arrowH)+")"
        });
        if ( ctx!="NULL" ) {
            text.attr("title", ctx);
            if ( ctx.length>7 ) {
                ctx = ctx.slice(0, 6); // 切割字符串
            }
            text.html(ctx);
        }
        text.niceTitle(); /*显示title */


        lsMul._svg.append(text);
    },

};