/**
 * Created by lyk on 2017/5/26 0026.
 */
var lsLine = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _id: null, // svg对象的父节点的id
    _parent: null, // svg对象的父对象
    _center_x: null, // svg对象的中心x坐标
    _center_y: null, // svg对象的中心y坐标
    _svgProto: null,
    _svg: null, // svg对象
    _leftBtn: null,
    _rightBtn: null,
    _baseLen: null,
    // _base_line: null, // 基线
    // _min: null, // 基线开始在细菌dna中的位置 --- no use
    // _max: null, // 基线结束在细菌dna中的位置 --- no use
    _base: null, // 基线被设计的总长(比例) --- no use
    _protein_num: null, // 蛋白质的数量
    _spacer_num: null, // spacers的数量
    _protein_data: null, // 蛋白质的数据
    _spacer_data: null, // spacer的数据
    _proteinArr: [], // svg中所有的蛋白质对象
    _spacerArr: [], // svg中所有spacer的对象
    _sortArr: [], // svg中所有蛋白质 和 spacer对象的顺序序列数组
    _textArr: [], // 文字数组
    _arrowLen: 60,
    _arrowH: 16,
    _rectLen: 20,
    _diamondLen: 10,
    _spaceLen: 5,
    _spaceH: 2,
    _height: 20,
    _svgX: 0,
    _focusColor: "#000",
    _colorFunction: {"cas1":"acquisition_1","cas2":"acquisition_2","2OG":"ancillary","cas4":"ancillary","casR":"ancillary","cpf1":"ancillary","csa3":"ancillary","csm6":"ancillary","csx1":"ancillary","csx15":"ancillary","csx16":"ancillary","csx18":"ancillary","csx20":"ancillary","csx21":"ancillary","csx3":"ancillary","DEDDh":"ancillary","DinG":"ancillary","PD-DExK":"ancillary","PrimPol":"ancillary","RT":"ancillary","WYL":"ancillary","cas5":"CASCADE_G5","cas5a":"CASCADE_G5","cas5f":"CASCADE_G5","cas5u":"CASCADE_G5","cmr3gr5":"CASCADE_G5","csb2gr5":"CASCADE_G5","csc1gr5":"CASCADE_G5","csf3gr5":"CASCADE_G5","csm4gr5":"CASCADE_G5","csx10gr5":"CASCADE_G5","cas7":"CASCADE_G7","cas7b":"CASCADE_G7","cas7f":"CASCADE_G7","cmr1gr7":"CASCADE_G7","cmr4gr7":"CASCADE_G7","cmr6gr7":"CASCADE_G7","cmr8gr7":"CASCADE_G7","csb1gr7":"CASCADE_G7","csc2gr7":"CASCADE_G7","csf2gr7":"CASCADE_G7","csm3gr7":"CASCADE_G7","csm5gr7":"CASCADE_G7","cas10":"CASCADE_LS","cas10d":"CASCADE_LS","cas8a1":"CASCADE_LS","cas8a2":"CASCADE_LS","cas8a3":"CASCADE_LS","cas8a4":"CASCADE_LS","cas8a5":"CASCADE_LS","cas8a6":"CASCADE_LS","cas8a7":"CASCADE_LS","cas8a8":"CASCADE_LS","cas8b1":"CASCADE_LS","cas8b10":"CASCADE_LS","cas8b2":"CASCADE_LS","cas8b3":"CASCADE_LS","cas8b4":"CASCADE_LS","cas8b5":"CASCADE_LS","cas8b6":"CASCADE_LS","cas8b7":"CASCADE_LS","cas8b8":"CASCADE_LS","cas8b9":"CASCADE_LS","cas8c":"CASCADE_LS","cas8e":"CASCADE_LS","cas8f":"CASCADE_LS","cas8u1":"CASCADE_LS","cas8u2":"CASCADE_LS","csf1gr8":"CASCADE_LS","cas11b":"CASCADE_SS","cas11d":"CASCADE_SS","cmr5gr11":"CASCADE_SS","csa5gr11":"CASCADE_SS","cse2gr11":"CASCADE_SS","csf4gr11":"CASCADE_SS","csm2gr11":"CASCADE_SS","cmr7":"CASCADE_UNK","csb3":"CASCADE_UNK","csf5gr6":"CASCADE_UNK","csx19":"CASCADE_UNK","csx22":"CASCADE_UNK","csx24":"CASCADE_UNK","csx25":"CASCADE_UNK","csx26":"CASCADE_UNK","cas6":"crRNAmaturation","cas6e":"crRNAmaturation","cas6f":"crRNAmaturation","cas3":"helicase_HD","cas3f":"helicase_HD","cas3HD":"helicase_HD","csn2":"helper","csx21":"helper","csx23":"helper","cas9":"multifunctional","cas12b":"multifunctional","c2c4":"multifunctional","c2c5":"multifunctional","cas13a":"multifunctional","cas13b":"multifunctional","cas13c":"multifunctional"},
    _functionColor: {"acquisition_1":"#E08031","acquisition_2":"#C7CEB2","ancillary":"#199475","CASCADE_G5":"#EFCEE8","CASCADE_G7":"#F3D7B5","CASCADE_LS":"#DAF9CA","CASCADE_SS":"#C7B3E5","CASCADE_UNK":"#FE7C67","crRNAmaturation":"#00FF80","helicase_HD":"#E9F01D","helper":"#7bbfea","multifunctional":"#ca8687"},
    _crisprColor: ["#4D157D", "#7D0043", "#A0BD2B"],
    _pos: null, // 缩写坐标
    _proteinLenArr: [],
    _proteinBaseLen: 50,
    _legendArr: [],

    init: function(id, data) {
        lsLine._sortArr.splice(0, lsLine._sortArr.length);
        lsLine._textArr.splice(0, lsLine._textArr.length);
        lsLine._legendArr.splice(0, lsLine._legendArr.length);
        lsLine._proteinLenArr.splice(0, lsLine._proteinLenArr.length);
        lsLine._id = id;
        lsLine._parent = $("#"+lsLine._id);
        lsLine._parent.next(".move").remove();
        lsLine._center_x = lsLine._parent.width() / 2;
        lsLine._center_y = lsLine._parent.height() - 40;
        lsLine._svgProto = document.createElementNS(lsLine.SVG_NS, 'svg');
        lsLine._svg = $(lsLine._svgProto);
        lsLine._svg.attr({
            "width": 2*lsLine._center_x,
            "height": lsLine._center_y + 40,
            // "viewBox": "0 0 "+(2*lsLine._center_x)+" "+(2*lsLine._center_y),
        });
        lsLine._svgProto.setAttribute("viewBox", "0 0 "+(2*lsLine._center_x)+" "+(lsLine._center_y+40));
        lsLine._protein_data = data.protein;
        lsLine._spacer_data = data.spacers;
        lsLine._protein_num = data.protein.length;
        lsLine._spacer_num = data.spacers.length;

        // 计算序列先后顺序
        lsLine.sortObj();

        // 给不同长度的蛋白质以不同的长度显示
        lsLine.sortProteinLen();

        // 绘制所有图形
        lsLine.drawGraph();

        // lsLine._sortArr.forEach(lsLine.mouseEvent);

        // 绘制legend
        lsLine.drawLegend();

        lsLine._parent.append(lsLine._svg);
        return lsLine._sortArr;
    },

    // 绘制cas蛋白颜色所代表的功能
    drawLegend: function() {
        var left = 5, top = 5, height=18, width=30;
        var legend, legendText;
        if ( lsLine._legendArr.length > 0 ) {
            titleText = $(document.createElementNS(ls.SVG_NS, "text"));
            titleText.html('function categories');
            titleText.attr({
                "x": left,
                "y": top+height*2/3,
                "font-weight": "bold",
                "fill": "#f00"
            });
            titleText.css({
                "font-size": '16px',
                "cursor": "pointer"
            });
            lsLine._svg.append(titleText);
        }
        top += 20;
        for ( var i=0; i<lsLine._legendArr.length; i++ ) {
            if ( left>lsLine._baseLen-100 ) {
                top += 20;
                left = 5;
            }
            legend = $(document.createElementNS(ls.SVG_NS, "rect"));
            legend.attr({
                "x": left,
                "y": top,
                "width": width,
                "height": height,
                "rx": 3,
                "ry": 3,
                "fill": lsLine._legendArr[i].color,
            });
            legend.css("cursor", "pointer");
            legendText = $(document.createElementNS(ls.SVG_NS, "text"));
            legendText.html(lsLine._legendArr[i].func);
            legendText.attr({
                "x": left+width,
                "y": top+height*2/3,
            });
            legendText.css({
                "font-size": '10px',
                "cursor": "pointer"
            });
            lsLine._svg.append(legend);
            lsLine._svg.append(legendText);
            left += width + 80;
        }
    },

    // 计算基线的比例长度
    calculateBase: function() {
        var min = 0, max = 0;
        if ( lsLine._protein_num ) {
            min = parseInt(lsLine._protein_data[0].startPos);
            max = parseInt(lsLine._protein_data[0].endPos);
            for ( var i=1; i<lsLine._protein_num; i++ ) {
                if ( min> parseInt(lsLine._protein_data[i].startPos) ) {
                    min = parseInt(lsLine._protein_data[i].startPos);
                }
                if ( max<parseInt(lsLine._protein_data[i].endPos) ) {
                    max = parseInt(lsLine._protein_data[i].endPos);
                }
            }
        }
        if ( lsLine._spacer_num ) {
            if ( !min ) {
                min = parseInt(lsLine._spacer_data[0].startPos);
                max = parseInt(lsLine._spacer_data[0].endPos);
            }
            for ( var i=0; i<lsLine._spacer_num; i++ ) {
                if ( min> parseInt(lsLine._spacer_data[i].startPos) ) {
                    min = parseInt(lsLine._spacer_data[i].startPos);
                }
                if ( max<parseInt(lsLine._spacer_data[i].startPos)+parseInt(lsLine._spacer_data[i].len) ) {
                    max = parseInt(lsLine._spacer_data[i].startPos)+parseInt(lsLine._spacer_data[i].len);
                }
            }
        }
        lsLine._min = min;
        lsLine._max = max;
        lsLine._base = max - min;
        if ( !lsLine._base ) {
            lsLine._base = lsLine._base * 5 / 4;
            lsLine._min = min-lsLine._base / 10;
            lsLine._max = max+lsLine._base / 10;
        }
    },

    // 计算序列先后顺序
    sortObj: function() {
        for ( var i=0; i<lsLine._protein_num; i++ ) {
            lsLine._sortArr.push({"data": lsLine._protein_data[i], "type": 0, "obj": null, "color": null, "flag": 1, "stingObj": null, "len": null});
        }
        for ( var i=0; i<lsLine._spacer_num; i++ ) {
            lsLine._sortArr.push({"data": lsLine._spacer_data[i], "type": 1, "obj": null, "color": null, "flag": 1, "stingObj": null, "len": null});
        }
        lsLine._sortArr.sort(lsLine.sortRule);
    },

    // 排序的规则
    sortRule: function(a, b) {
        return parseInt(a.data.startPos) - parseInt(b.data.startPos);
    },

    // 画出基线
    drawBaseLine: function() {
        lsLine._base_line = $(document.createElementNS(lsLine.SVG_NS, "rect"));
        lsLine._base_line.attr({
            "x": lsLine._center_x-200,
            "y": lsLine._center_y-2,
            "width": 400,
            "height": 4,
            "fill": "#ccc"
        });
        lsLine._svg.append(lsLine._base_line);
    },

    // 画图
    drawGraph: function() {
        var flag = 0, startPos=0, num, obj, textObj, color, kind, k=0;
        num = lsLine._sortArr.length;
        obj = lsLine.drawLine(startPos);
        startPos += lsLine._spaceLen;
        for ( var i=0; i<num; i++ ) {
            if ( lsLine._sortArr[i].type ) {
                if ( flag ) continue;
                lsLine.drawDiamond(startPos, lsLine._crisprColor[0]);
                startPos += lsLine._diamondLen;
                obj = lsLine.drawRect(startPos, lsLine._crisprColor[1]);
                lsLine._pos = startPos + lsLine._rectLen / 2;
                startPos += lsLine._rectLen;
                lsLine.drawSuoxie(lsLine._pos, lsLine._spacer_num);
                lsLine.drawDiamond(startPos, lsLine._crisprColor[2]);
                startPos += lsLine._diamondLen;
                flag = 1;
            } else {
                obj = lsLine.drawLine(startPos);
                startPos += lsLine._spaceLen;
                // kind = lsLine._sortArr[i].data.protein_name.split("_")[0].toLowerCase();
                kind = lsLine._sortArr[i].data.protein_name;
                color = lsLine._functionColor[lsLine._colorFunction[kind]];
                obj = lsLine.drawArraw(startPos, color, lsLine._sortArr[i].len, lsLine._sortArr[i].data.pmc);
                textObj = lsLine.drawText(startPos, color, lsLine._sortArr[i].len, lsLine._sortArr[i].data.protein_name);

                // 计算 legendArr
                if ( !lsLine.isContain(lsLine._colorFunction[kind]) ) {
                    var legendItem = {"func": lsLine._colorFunction[kind], "color": color};
                    lsLine._legendArr.push(legendItem);
                }
                // end

                lsLine._textArr.push(textObj);
                lsLine._sortArr[i].obj = obj;
                lsLine._sortArr[i].stingObj = textObj;
                lsLine._sortArr[i].color = color;
                startPos += lsLine._sortArr[i].len;
                obj = lsLine.drawLine(startPos);
                startPos += lsLine._spaceLen;
            }
        }

        obj = lsLine.drawLine(startPos);
        startPos += lsLine._spaceLen;

        if ( lsLine._leftBtn && lsLine._rightBtn ) {
            lsLine.dragLeft(lsLine._leftBtn);
            lsLine.dragRight(lsLine._rightBtn);
        }
    },

    isContain: function(funcName) {
        for ( var i=0; i<lsLine._legendArr.length; i++ ) {
            if ( lsLine._legendArr[i].func==funcName ) {
                return true;
            }
        }
        return false;
    },

    sortProteinLen: function() {
        for ( var i=0; i<lsLine._sortArr.length; i++ ) {
            if ( !lsLine._sortArr[i].type ) {
                lsLine._proteinLenArr.push({"len": (parseInt(lsLine._sortArr[i].data.endPos)-parseInt(lsLine._sortArr[i].data.startPos)), "index": i, "bili": null});
            }
        }
        lsLine._proteinLenArr.sort(function(a, b){
            return parseInt(a.len) - parseInt(b.len);
        });
        var mid = Math.floor(lsLine._proteinLenArr.length/2);
        if ( lsLine._proteinLenArr.length ) {
            var baseLen = lsLine._proteinLenArr[mid].len;
        }
        //lsLine._proteinLenArr[mid].bili = 1;
        var len = 0, le;
        for ( var i=0; i<lsLine._proteinLenArr.length; i++ ) {
            lsLine._proteinLenArr[i].bili = (lsLine._proteinLenArr[i].len/baseLen).toFixed(2);
            le = lsLine._proteinBaseLen*lsLine._proteinLenArr[i].bili;
            if ( le<20 ) le = 20;
            len += le;
            lsLine._sortArr[lsLine._proteinLenArr[i].index].len = le;
        }
        lsLine._baseLen = Math.round(len) +  lsLine._rectLen + 2*lsLine._diamondLen + (4+2*lsLine._protein_num)*lsLine._spaceLen;
        lsLine._baseLen += 50;
        if ( lsLine._baseLen>lsLine._center_x*2 ) {
            lsLine._leftBtn = $(document.createElement("a"));
            lsLine._leftBtn.addClass("leftBtn");
            lsLine._rightBtn = $(document.createElement("a"));
            lsLine._rightBtn.addClass("rightBtn");
            var nextBox = $(document.createElement("div"));
            nextBox.addClass("move");
            nextBox.css({
                width: "120px",
                // height: "100%"
                height: "100px",
                "margin": "0 auto",
                "overflow": "auto"
            });
            nextBox.append(lsLine._leftBtn);
            nextBox.append(lsLine._rightBtn);
            lsLine._parent.after(nextBox);
        } else {
            lsLine._parent.css({
                "width": lsLine._baseLen,
                "margin": "0 auto"
            });
            lsLine._svg.attr("width", "100%");
            lsLine._svgProto.setAttribute("viewBox", "0 0 "+lsLine._baseLen+" "+(lsLine._center_y+40));
            // lsLine._svg.css("margin-left", lsLine._center_x-lsLine._baseLen/2);
        }
    },

    drawSuoxie: function(startPos, num) {
        var text = $(document.createElementNS(lsLine.SVG_NS, "text"));
        text.attr({
            "x": startPos-15,
            "y": lsLine._center_y+lsLine._height*3/2,
            "fill": "#ff55ff",
            "font-size": 12
        });
        text.html("["+num+"X]");
        lsLine._svg.append(text);
        return text;
    },

    // 向左拖动svg
    dragLeft: function(btn) {
        btn.click(function() {
            if ( lsLine._svgX>0 ) {
                lsLine._svgX -= lsLine._center_x;
                lsLine._svgProto.setAttribute("viewBox", lsLine._svgX+" 0 "+(lsLine._center_x*2)+" "+(lsLine._center_y+40));
            }

        });
    },

    // 向右拖动svg
    dragRight: function(btn) {
        btn.click(function() {
            if ( lsLine._svgX<lsLine._baseLen ) {
                lsLine._svgX += lsLine._center_x;
                lsLine._svgProto.setAttribute("viewBox", lsLine._svgX+" 0 "+(lsLine._center_x*2)+" "+(lsLine._center_y+40));
            }
        });
    },

    // 鼠标事件
    mouseEvent: function(curObj, objIndex, objArr) {
        curObj.obj.mouseover(function(event){
            $(this).attr({
                "stroke-width": "2",
                "stroke": lsLine._focusColor,
            });
            if ( curObj.stingObj ) {
                curObj.stingObj.attr({
                    "stroke": lsLine._focusColor,
                });
            }
        });
        curObj.obj.mouseout(function(event){
            if ( curObj.flag ) {
                $(this).attr({
                    "stroke-width": "0"
                });
                if ( curObj.stingObj ) {
                    curObj.stingObj.attr({
                        "stroke": "none",
                    });
                }
            }
        });
        curObj.obj.click(function(event){
            for ( var i=0; i<lsLine._sortArr.length; i++ ) {
                lsLine._sortArr[i].obj.attr("stroke-width", "0");
                lsLine._sortArr[i].flag = 1;
                if ( lsLine._sortArr[i].stingObj ) {
                    lsLine._sortArr[i].stingObj.attr({
                        "stroke": "none",
                    });
                }
            }
            $(this).attr("stroke-width", "2");
            if ( curObj.stingObj ) {
                curObj.stingObj.attr({
                    "stroke": lsLine._focusColor
                });
            }
            curObj.flag = 0;
        });
    },

    // 画箭头
    drawArraw: function(startPos, color, len, direction) {
        var arrow, description;
        var h = lsLine._arrowH / 2;
        arrow = $(document.createElementNS(lsLine.SVG_NS, 'path'));
        if ( direction=="+" ) {
            description = ['M', startPos, lsLine._center_y-h, 'L', startPos+len-h, lsLine._center_y-h, 'L', startPos+len, lsLine._center_y, 'L', startPos+len-h, lsLine._center_y+h, 'L', startPos, lsLine._center_y+h, 'Z'];
        } else {
            description = ['M', startPos, lsLine._center_y, 'L', startPos+h, lsLine._center_y-h, 'L', startPos+len, lsLine._center_y-h, 'L', startPos+len, lsLine._center_y+h, 'L', startPos+h, lsLine._center_y+h, 'Z'];
        }
        arrow.attr({
            "d": description.join(' '),
            "fill": color
        });
        arrow.css("cursor", "pointer");
        lsLine._svg.append(arrow);
        return arrow;
    },

    // 画矩形
    drawRect: function(startPos, color) {
        var rect = $(document.createElementNS(lsLine.SVG_NS, 'rect'));
        rect.attr({
            "x": startPos,
            "y": lsLine._center_y-lsLine._height/2,
            "width": lsLine._rectLen,
            "height": lsLine._height,
            "fill": color
        });
        rect.css("cursor", "pointer");
        lsLine._svg.append(rect);
        return rect;
    },

    // 画菱形
    drawDiamond: function(startPos, color) {
        var diamond = $(document.createElementNS(lsLine.SVG_NS, 'polygon'));
        diamond.attr({
            "points": startPos+","+lsLine._center_y+" "+(startPos+lsLine._diamondLen/2)+","+(lsLine._center_y-lsLine._height/2)+" "+(startPos+lsLine._diamondLen)+","+(lsLine._center_y)+" "+(startPos+lsLine._diamondLen/2)+","+(lsLine._center_y+lsLine._height/2),
            "fill": color
        });
        diamond.css("cursor", "pointer");
        lsLine._svg.append(diamond);
        return diamond;
    },

    // 画分隔线
    drawLine: function(startPos) {
        var line = $(document.createElementNS(lsLine.SVG_NS, 'rect'));
        line.attr({
            "x": startPos,
            "y": lsLine._center_y-lsLine._spaceH/2,
            "width": lsLine._spaceLen,
            "height": lsLine._spaceH,
            "fill": "#555"
        });
        lsLine._svg.append(line);
    },

    // 画文本
    drawText: function(startPos, color, len, ctx) {
        var text = $(document.createElementNS(lsLine.SVG_NS, "text"));
        text.attr({
            "x": startPos+len/2,
            "y": lsLine._center_y-lsLine._arrowH,
            // "fill": color,
            "fill": "#000",
            "font-weight": "bold",
            "font-size": 12,
            "transform": "rotate(-45 "+(startPos+len/2)+","+(lsLine._center_y-lsLine._arrowH)+")"
        });
        text.html(ctx);
        lsLine._svg.append(text);
        return text;
    },

};