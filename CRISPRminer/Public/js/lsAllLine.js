/**
 * Created by lyk on 2017/6/20 0020.
 */


var lsAllLine = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _id: null, // svg对象的父节点的id
    _parent: null, // svg对象的父对象
    _svgProto: null,
    _svg: null, // svg对象
    _data: null,
    _dataNum: null,
    _bigNum: null,
    _Height: 30,
    _height: 20,
    _width: 80,
    _arrowLen: 60,
    _arrowH: 16,
    _rectLen: 20,
    _diamondLen: 10,
    _spaceLen: 5,
    _spaceH: 2,
    _colorFunction: {"cas1":"acquisition_1","cas2":"acquisition_2","2OG":"ancillary","cas4":"ancillary","casR":"ancillary","cpf1":"ancillary","csa3":"ancillary","csm6":"ancillary","csx1":"ancillary","csx15":"ancillary","csx16":"ancillary","csx18":"ancillary","csx20":"ancillary","csx21":"ancillary","csx3":"ancillary","DEDDh":"ancillary","DinG":"ancillary","PD-DExK":"ancillary","PrimPol":"ancillary","RT":"ancillary","WYL":"ancillary","cas5":"CASCADE_G5","cas5a":"CASCADE_G5","cas5f":"CASCADE_G5","cas5u":"CASCADE_G5","cmr3gr5":"CASCADE_G5","csb2gr5":"CASCADE_G5","csc1gr5":"CASCADE_G5","csf3gr5":"CASCADE_G5","csm4gr5":"CASCADE_G5","csx10gr5":"CASCADE_G5","cas7":"CASCADE_G7","cas7b":"CASCADE_G7","cas7f":"CASCADE_G7","cmr1gr7":"CASCADE_G7","cmr4gr7":"CASCADE_G7","cmr6gr7":"CASCADE_G7","cmr8gr7":"CASCADE_G7","csb1gr7":"CASCADE_G7","csc2gr7":"CASCADE_G7","csf2gr7":"CASCADE_G7","csm3gr7":"CASCADE_G7","csm5gr7":"CASCADE_G7","cas10":"CASCADE_LS","cas10d":"CASCADE_LS","cas8a1":"CASCADE_LS","cas8a2":"CASCADE_LS","cas8a3":"CASCADE_LS","cas8a4":"CASCADE_LS","cas8a5":"CASCADE_LS","cas8a6":"CASCADE_LS","cas8a7":"CASCADE_LS","cas8a8":"CASCADE_LS","cas8b1":"CASCADE_LS","cas8b10":"CASCADE_LS","cas8b2":"CASCADE_LS","cas8b3":"CASCADE_LS","cas8b4":"CASCADE_LS","cas8b5":"CASCADE_LS","cas8b6":"CASCADE_LS","cas8b7":"CASCADE_LS","cas8b8":"CASCADE_LS","cas8b9":"CASCADE_LS","cas8c":"CASCADE_LS","cas8e":"CASCADE_LS","cas8f":"CASCADE_LS","cas8u1":"CASCADE_LS","cas8u2":"CASCADE_LS","csf1gr8":"CASCADE_LS","cas11b":"CASCADE_SS","cas11d":"CASCADE_SS","cmr5gr11":"CASCADE_SS","csa5gr11":"CASCADE_SS","cse2gr11":"CASCADE_SS","csf4gr11":"CASCADE_SS","csm2gr11":"CASCADE_SS","cmr7":"CASCADE_UNK","csb3":"CASCADE_UNK","csf5gr6":"CASCADE_UNK","csx19":"CASCADE_UNK","csx22":"CASCADE_UNK","csx24":"CASCADE_UNK","csx25":"CASCADE_UNK","csx26":"CASCADE_UNK","cas6":"crRNAmaturation","cas6e":"crRNAmaturation","cas6f":"crRNAmaturation","cas3":"helicase_HD","cas3f":"helicase_HD","cas3HD":"helicase_HD","csn2":"helper","csx21":"helper","csx23":"helper","cas9":"multifunctional","cas12b":"multifunctional","c2c4":"multifunctional","c2c5":"multifunctional","cas13a":"multifunctional","cas13b":"multifunctional","cas13c":"multifunctional"},
    _functionColor: {"acquisition_1":"#E08031","acquisition_2":"#C7CEB2","ancillary":"#199475","CASCADE_G5":"#EFCEE8","CASCADE_G7":"#F3D7B5","CASCADE_LS":"#DAF9CA","CASCADE_SS":"#C7B3E5","CASCADE_UNK":"#FE7C67","crRNAmaturation":"#00FF80","helicase_HD":"#E9F01D","helper":"#7bbfea","multifunctional":"#ca8687"},
    _crisprColor: ["#4D157D", "#7D0043", "#A0BD2B"],
    _pos: null, // 缩写坐标
    _proteinBaseLen: 50,
    _svg_len: null,


    init: function(id, data) {
        lsAllLine._id = id;
        lsAllLine._parent = $("#"+lsAllLine._id);
        // lsAllLine._parent.next(".move").remove();
        lsAllLine._data = data;
        lsAllLine._dataNum = data.length;
        // 计算最大的svg宽度
        this.countBigWidth();
        lsAllLine._svgProto = document.createElementNS(lsAllLine.SVG_NS, 'svg');
        lsAllLine._svg = $(lsAllLine._svgProto);
        lsAllLine._svg.attr({
            "width": lsAllLine._width*lsAllLine._bigNum+2*lsAllLine._spaceLen+2*lsAllLine._diamondLen+lsAllLine._rectLen ,
            "height": lsAllLine._Height*lsAllLine._dataNum,
            // "viewBox": "0 0 "+(2*lsAllLine._center_x)+" "+(2*lsAllLine._center_y),
        });

        if ( data.length ) {
            var height = 0;
            for ( var i=0; i<data.length; i++ ) {
                this.drawLineGraph(height, data[i]['one']);
                height += lsAllLine._Height;
            }
        }
        lsAllLine._svg.attr("width", lsAllLine._svg_len*lsAllLine._bigNum+2*lsAllLine._diamondLen+lsAllLine._rectLen);
        lsAllLine._parent.append(lsAllLine._svg);

    },

    drawLineGraph: function(height, data) {
        var sortArr = this.sortObj(data);
        sortArr = this.sortProteinLen(sortArr);
        var pos = lsAllLine.drawGraph(sortArr, height);
        this.drawText(pos, height, "#fff", data['spacers'].length);


    },

    // 画图
    drawGraph: function(sortArr, height) {
        var flag = 0, startPos=0, num, obj, textObj, color, kind, k=0, pos;
        num = sortArr.length;
        obj = lsAllLine.drawLine(startPos, height);
        startPos += lsAllLine._spaceLen;
        for ( var i=0; i<num; i++ ) {
            if ( sortArr[i].type ) {
                if ( flag ) continue;
                lsAllLine.drawDiamond(startPos, height, lsAllLine._crisprColor[0]);
                startPos += lsAllLine._diamondLen;
                obj = lsAllLine.drawRect(startPos, height, lsAllLine._crisprColor[1]);
                 obj.niceTitle();
                pos = startPos;
                startPos += lsAllLine._rectLen;
                lsAllLine.drawDiamond(startPos, height, lsAllLine._crisprColor[2]);
                startPos += lsAllLine._diamondLen;
                flag = 1;
            } else {
                obj = lsAllLine.drawLine(startPos, height);
                startPos += lsAllLine._spaceLen;
                // kind = sortArr[i].data.protein_name.split("_")[0].toLowerCase();
                kind = sortArr[i].data.protein_name;
                color = lsAllLine._functionColor[lsAllLine._colorFunction[kind]];
                obj = lsAllLine.drawArraw(startPos, height, color, sortArr[i].len, sortArr[i].data.pmc);
                this.drawText(startPos, height, "#fff", sortArr[i]['data']['protein_name']);
                sortArr[i].color = color;
                startPos += parseInt(sortArr[i].len);
                obj = lsAllLine.drawLine(startPos, height);
                startPos += lsAllLine._spaceLen;
            }
        }

        obj = lsAllLine.drawLine(startPos, height);
        startPos += lsAllLine._spaceLen;
        return pos;
    },

    sortProteinLen: function(sortArr) {
        var proteinLenArr = [];
        for ( var i=0; i<sortArr.length; i++ ) {
            if ( !sortArr[i].type ) {
                proteinLenArr.push({"len": (parseInt(sortArr[i].data.endPos)-parseInt(sortArr[i].data.startPos)), "index": i, "bili": null});
            }
        }
        proteinLenArr.sort(function(a, b){
            return parseInt(a.len) - parseInt(b.len);
        });
        var mid = Math.floor(proteinLenArr.length/2);
        if ( proteinLenArr.length ) {
            var baseLen = proteinLenArr[mid].len;
        }
        //lsLine._proteinLenArr[mid].bili = 1;
        var len = 0, le;
        for ( var i=0; i<proteinLenArr.length; i++ ) {
            proteinLenArr[i].bili = (proteinLenArr[i].len/baseLen).toFixed(2);
            le = lsAllLine._proteinBaseLen*proteinLenArr[i].bili;
            if ( le<20 ) le = 20;
            if ( len<le ) {
                len = le;
            }
            sortArr[proteinLenArr[i].index].len = le;
        }
        lsAllLine._svg_len = len;
        return sortArr;
    },

    // 画箭头
    drawArraw: function(startPos, height, color, len, direction) {
        var arrow, description;
        var h = lsAllLine._arrowH / 2;
        arrow = $(document.createElementNS(lsAllLine.SVG_NS, 'path'));
        if ( direction=="+" ) {
            description = ['M', startPos, height+10-h, 'L', startPos+len-h, height+10-h, 'L', startPos+len, height+10, 'L', startPos+len-h, height+10+h, 'L', startPos, height+10+h, 'Z'];
        } else {
            description = ['M', startPos, height+10, 'L', startPos+h, height+10-h, 'L', startPos+len, height+10-h, 'L', startPos+len, height+10+h, 'L', startPos+h, height+10+h, 'Z'];
        }
        arrow.attr({
            "d": description.join(' '),
            "fill": color
        });
        arrow.css("cursor", "pointer");
        // arrow.niceTitle();
        lsAllLine._svg.append(arrow);
        return arrow;
    },

    // 画矩形
    drawRect: function(startPos, height, color) {
        var rect = $(document.createElementNS(lsAllLine.SVG_NS, 'rect'));
        rect.attr({
            "x": startPos,
            "y": height+10-lsAllLine._height/2,
            "width": lsAllLine._rectLen,
            "height": lsAllLine._height,
            "fill": color
        });
        rect.css("cursor", "pointer");
        // rect.niceTitle();
        lsAllLine._svg.append(rect);
        return rect;
    },

    // 画菱形
    drawDiamond: function(startPos, height, color) {
        var diamond = $(document.createElementNS(lsAllLine.SVG_NS, 'polygon'));
        diamond.attr({
            "points": startPos+","+(height+10)+" "+(startPos+lsAllLine._diamondLen/2)+","+height+" "+(startPos+lsAllLine._diamondLen)+","+(height+10)+" "+(startPos+lsAllLine._diamondLen/2)+","+(height+20),
            "fill": color
        });
        diamond.css("cursor", "pointer");
        lsAllLine._svg.append(diamond);
        return diamond;
    },

    // 画分隔线
    drawLine: function(startPos, height) {
        var line = $(document.createElementNS(lsAllLine.SVG_NS, 'rect'));
        line.attr({
            "x": startPos,
            "y": height+10-lsAllLine._spaceH/2,
            "width": lsAllLine._spaceLen,
            "height": lsAllLine._spaceH,
            "fill": "#555"
        });
        lsAllLine._svg.append(line);
    },

    // 起始位置 颜色  y轴坐标    文字
    drawText: function(startPos, height, color, ctx) {
        var text = $(document.createElementNS(lsAllLine.SVG_NS, "text"));
        text.attr({
            "x": startPos,
            "y": height+lsAllLine._Height/2,
            "fill": color,
            "font-size": 10,
            "cursor": "pointer"
        });
        if ( ctx!="NULL" ) {
            text.attr("title", ctx);
            if ( ctx.length>7 ) {
                ctx = ctx.slice(0, 6); // 切割字符串
            }
            text.html(ctx);
        }
         text.niceTitle();
        lsAllLine._svg.append(text);
    },

    sortObj: function(data) {
        var sortArr = [];
        if ( data['protein'].length ) {
            for ( var i=0; i<data['protein'].length; i++ ) {
                sortArr.push({"data": data['protein'][i], "type": 0, "obj": null, "color": null, "flag": 1, "stingObj": null, "len": null});
            }
        }
        if ( data['spacers'].length )
        for ( var i=0; i<data['spacers'].length; i++ ) {
            sortArr.push({"data": data['spacers'][i], "type": 1, "obj": null, "color": null, "flag": 1, "stingObj": null, "len": null});
        }
        sortArr.sort(lsAllLine.sortRule);
        return sortArr;
    },

    // 排序的规则
    sortRule: function(a, b) {
        return parseInt(a.data.startPos) - parseInt(b.data.startPos);
    },

    countBigWidth: function() {
        if ( lsAllLine._data.length ) {
            var bigNum = 0;
            for ( var i=0; i<lsAllLine._data.length; i++ ) {
                if ( lsAllLine._data[i]['one']['protein'].length>bigNum ) {
                    bigNum = lsAllLine._data[i]['one']['protein'].length;
                }
            }
            lsAllLine._bigNum = bigNum;
        }
    }

};