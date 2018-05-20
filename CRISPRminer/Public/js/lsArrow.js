/**
 * Created by lyk on 2017/6/2 0002.
 */

var lsArrow = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _parent: null,
    _id: null,
    _svgProto: null,
    _svg: null, // svg对象
    _defs: null,
    _leftBtn: null,
    _rightBtn: null,
    _spacer_num: null, // spacer 数量
    _common_num: null, // 相同序列数量
    _inteval_num: null, // spacer之间的间隔序列数量
    _spacer_data: null,
    _common_data: null,
    _inteval_data: null,
    _center_x: null,
    _center_y: null,
    _baseLen: null,
    _sortArr: [],
    _endArr: [],
    _bezierArr: [],
    _startArr: [],
    _arrowLen: 60,
    _arrowH: 16,
    _rectLen: 20,
    _diamondLen: 10,
    _spaceLen: 5,
    _spaceH: 2,
    _height: 20,
    _svgX: 0,
    _colorArr: ["#000", "#f00", "#0f0", "#00f", "#ff0", "#f0f", "#0ff", "#fff"],
    _dir: 0, // 箭头的方向(上方或下方)

    init: function(id, data) {
        lsArrow._sortArr.splice(0, lsArrow._sortArr.length);
        lsArrow._startArr.splice(0, lsArrow._startArr.length);
        lsArrow._endArr.splice(0, lsArrow._endArr.length);
        lsArrow._id = id;
        lsArrow._parent = $("#"+id);
        lsArrow._parent.next(".move").remove();
        lsArrow._center_x = lsArrow._parent.width() / 2;
        if ( lsArrow._center_x==0 ) {
            lsArrow._center_x = lsArrow._parent.parent().parent().width() / 2;
        }
        lsArrow._center_y = lsArrow._parent.height() - 40;
        lsArrow._svgProto = document.createElementNS(lsArrow.SVG_NS, 'svg');
        lsArrow._svg = $(lsArrow._svgProto);
        lsArrow._svg.attr({
            "width": 2*lsArrow._center_x,
            "height": lsArrow._center_y + 40
        });
        lsArrow._svgProto.setAttribute("viewBox", "0 0 "+(2*lsArrow._center_x)+" "+(lsArrow._center_y+40));
        lsArrow._spacer_num = data.spacers.length;
        lsArrow._spacer_data = data.spacers;
        lsArrow._common_num = data.commons.length;
        lsArrow._common_data = data.commons;

        lsArrow._defs = document.createElementNS(lsArrow.SVG_NS, "defs");
        lsArrow._svg.append(lsArrow._defs);

        // 计算序列先后顺序
        lsArrow.sortObj();

        // 绘制
        lsArrow.drawGraph();

        // 给有意义的图形元素添加鼠标事件
        // lsArrow._sortArr.forEach(lsArrow.mouseEvent);

        // 绘制多个颜色的预定义的箭头
        lsArrow._colorArr.forEach(function(curObj, index, objArr) {
            lsArrow.drawDefsArrow(curObj);
        });

        lsArrow._parent.append(lsArrow._svg);
    },

    // 计算序列先后顺序
    sortObj: function() {
        for ( var i=0; i<lsArrow._common_num; i++ ) {
            lsArrow._sortArr.push({"data": lsArrow._common_data[i], "type": 0, "obj": null, "color": null, "flag": 1, "x": null});
        }
        for ( var i=0; i<lsArrow._spacer_num; i++ ) {
            lsArrow._sortArr.push({"data": lsArrow._spacer_data[i], "type": 1, "obj": null, "color": null, "flag": 1, "x": null});
        }
        lsArrow._sortArr.sort(lsArrow.sortRule);
        lsArrow._baseLen = lsArrow._common_num * lsArrow._arrowLen + lsArrow._spacer_num * lsArrow._rectLen + (2+2*lsArrow._common_num)*lsArrow._spaceLen + lsArrow._spacer_num*lsArrow._diamondLen;
        if ( lsArrow._baseLen>lsArrow._center_x*2 ) {
            lsArrow._leftBtn = $(document.createElement("a"));
            lsArrow._leftBtn.addClass("leftBtn");
            lsArrow._rightBtn = $(document.createElement("a"));
            lsArrow._rightBtn.addClass("rightBtn");
            var nextBox = $(document.createElement("div"));
            nextBox.addClass("move");
            nextBox.css({
                // width: "100%",
                // height: "100%"
                "width": "120px",
                "margin": "0 auto",
                "overflow": "auto",
            });
            nextBox.append(lsArrow._leftBtn);
            nextBox.append(lsArrow._rightBtn);
            lsArrow._parent.after(nextBox);
        } else {
            lsArrow._parent.css({
                "width": lsArrow._baseLen,
                "margin": "0 auto"
            });
            lsArrow._svg.attr("width", "100%");
            lsArrow._svgProto.setAttribute("viewBox", "0 0 "+lsArrow._baseLen+" "+(lsArrow._center_y+40));
        }
    },

    // 排序的规则
    sortRule: function(a, b) {
        return parseInt(a.data.startPos) - parseInt(b.data.startPos);
    },

    // 画图
    drawGraph: function() {
        var flag = 0, startPos=0, num, obj;
        num = lsArrow._sortArr.length;
        for ( var i=0; i<num; i++ ) {
            if ( lsArrow._sortArr[i].type ) {
                obj = lsArrow.drawRect(startPos, "#00f");
                lsArrow._sortArr[i].obj = obj;
                lsArrow._sortArr[i].color = "#00f";
                lsArrow._startArr.push({"id": lsArrow._sortArr[i].data.id, "x": startPos, "color": lsArrow._sortArr[i].color, "obj": obj, "leftObj": null, "rightObj": null});
                startPos += lsArrow._rectLen;
                lsArrow.drawDiamond(startPos, "#0f0");
                startPos += lsArrow._diamondLen;
            } else {
                obj = lsArrow.drawLine(startPos);
                startPos += lsArrow._spaceLen;
                obj = lsArrow.drawArraw(startPos, "#f00");
                lsArrow._sortArr[i].obj = obj;
                lsArrow._sortArr[i].color = "#f00";
                lsArrow._endArr.push({"id": lsArrow._sortArr[i].data.parent_id, "x": startPos, "obj": obj, "leftObj": null, "rightObj": null});
                startPos += lsArrow._arrowLen;
                obj = lsArrow.drawLine(startPos);
                startPos += lsArrow._spaceLen;
                lsArrow.drawPoints(startPos);
                startPos += 20;
                obj = lsArrow.drawLine(startPos);
                startPos += lsArrow._spaceLen;
            }
        }

        var k = 0;
        for ( var i=0; i<lsArrow._endArr.length; i++ ) {
            var sx, ex, c;
            ex = lsArrow._endArr[i].x;
            for (var j =0; j<lsArrow._startArr.length; j++ ) {
                if ( lsArrow._startArr[j].id == lsArrow._endArr[i].id ) {
                    sx = lsArrow._startArr[j].x;
                    c = lsArrow._startArr[j].color;
                    break;
                }
            }
            obj = lsArrow.drawBezierArrow(sx+lsArrow._rectLen/2, ex+lsArrow._arrowLen/2, c);
            lsArrow._bezierArr.push({"obj": obj, "color": c, "leftObj": lsArrow._startArr[j].obj, "rightObj": lsArrow._endArr[i].obj});
            lsArrow._startArr[j].leftObj = lsArrow._bezierArr[k];
            lsArrow._startArr[j].rightObj = lsArrow._endArr[i].obj;
            lsArrow._endArr[i].leftObj = lsArrow._bezierArr[k];
            lsArrow._endArr[i].rightObj = lsArrow._startArr[j].obj;
            k ++;
        }

        lsArrow._startArr.forEach(lsArrow.mouseEvent1);
        lsArrow._endArr.forEach(lsArrow.mouseEvent1);
        lsArrow._bezierArr.forEach(lsArrow.mouseEvent2);

        if ( lsArrow._leftBtn && lsArrow._rightBtn ) {
            lsArrow.dragLeft(lsArrow._leftBtn);
            lsArrow.dragRight(lsArrow._rightBtn);
        }
    },

    // 向左拖动svg
    dragLeft: function(btn) {
        btn.click(function() {
            if ( lsArrow._svgX>0 ) {
                lsArrow._svgX -= lsArrow._center_x;
                lsArrow._svgProto.setAttribute("viewBox", lsArrow._svgX+" 0 "+(lsArrow._center_x*2)+" "+(lsArrow._center_y+40));
            }

        });
    },

    // 向右拖动svg
    dragRight: function(btn) {
        btn.click(function() {
            if ( lsArrow._svgX<lsArrow._baseLen ) {
                lsArrow._svgX += lsArrow._center_x;
                lsArrow._svgProto.setAttribute("viewBox", lsArrow._svgX+" 0 "+(lsArrow._center_x*2)+" "+(lsArrow._center_y+40));
            }
        });
    },

    // 鼠标事件
    mouseEvent1: function(curObj, objIndex, objArr) {
        curObj.obj.mouseover(function(event){
            $(this).attr({
                "stroke-width": "2",
                "stroke": "#000",
            });
            if ( curObj.leftObj ) {
                curObj.leftObj.obj.setAttribute("stroke", "#000");
                curObj.leftObj.obj.setAttribute("stroke-width", "2");
                curObj.leftObj.obj.setAttribute("fill", "none");
                curObj.leftObj.obj.setAttribute("style", "marker-end: url(##000); cursor: pointer;");
                curObj.rightObj.attr({
                    "stroke-width": "2",
                    "stroke": "#000",
                });
            }

        });
        curObj.obj.mouseout(function(event){
            // if ( curObj.flag ) {
            $(this).attr({
                "stroke-width": "0"
            });
            if ( curObj.leftObj ) {
                curObj.rightObj.attr({
                    "stroke-width": "0"
                });
                curObj.leftObj.obj.setAttribute("stroke", curObj.leftObj.color);
                curObj.leftObj.obj.setAttribute("stroke-width", "1");
                curObj.leftObj.obj.setAttribute("fill", "none");
                curObj.leftObj.obj.setAttribute("style", "marker-end: url(#"+curObj.leftObj.color+"); cursor: pointer;");
            }

            // }
        });
        // curObj.obj.click(function(event){
        //     for ( var i=0; i<lsArrow._sortArr.length; i++ ) {
        //         lsArrow._sortArr[i].obj.attr("stroke-width", "0");
        //         lsArrow._sortArr[i].flag = 1;
        //     }
        //     $(this).attr("stroke-width", "2");
        //     curObj.flag = 0;
        // });
    },

    // 鼠标事件
    mouseEvent2: function(curObj, objIndex, objArr) {
        curObj.obj.onmouseover = function(event){
            if ( curObj.leftObj ) {
                curObj.leftObj.attr({
                    "stroke-width": "2",
                    "stroke": "#000",
                });
                curObj.rightObj.attr({
                    "stroke-width": "2",
                    "stroke": "#000",
                });
            }

            curObj.obj.setAttribute("stroke", "#000");
            curObj.obj.setAttribute("stroke-width", "2");
            curObj.obj.setAttribute("fill", "none");
            curObj.obj.setAttribute("style", "marker-end: url(##000); cursor: pointer;");
        };
        curObj.obj.onmouseout = function(event){
            // if ( curObj.flag ) {
            if ( curObj.leftObj ) {
                curObj.leftObj.attr({
                    "stroke-width": "0"
                });
                curObj.rightObj.attr({
                    "stroke-width": "0"
                });
            }
            curObj.obj.setAttribute("stroke", curObj.color);
            curObj.obj.setAttribute("stroke-width", "1");
            curObj.obj.setAttribute("fill", "none");
            curObj.obj.setAttribute("style", "marker-end: url(#"+curObj.color+"); cursor: pointer;");
            // }
        };
        // curObj.obj.click(function(event){
        //     for ( var i=0; i<lsArrow._sortArr.length; i++ ) {
        //         lsArrow._sortArr[i].obj.attr("stroke-width", "0");
        //         lsArrow._sortArr[i].flag = 1;
        //     }
        //     $(this).attr("stroke-width", "2");
        //     curObj.flag = 0;
        // });
    },

    // 画箭头
    drawArraw: function(startPos, color) {
        var arrow, description;
        var h = lsArrow._arrowH / 2;
        var duan = lsArrow._arrowLen / 6;
        arrow = $(document.createElementNS(lsArrow.SVG_NS, 'path'));
        description = ['M', startPos, lsArrow._center_y-h,
            'L', startPos+duan, lsArrow._center_y-h/2,
            'L', startPos+duan*2, lsArrow._center_y-h,
            'L', startPos+duan*3, lsArrow._center_y-h/2,
            'L', startPos+duan*4, lsArrow._center_y-h,
            'L', startPos+duan*5, lsArrow._center_y-h/2,
            'L', startPos+duan*6, lsArrow._center_y-h,
            'L', startPos+duan*6, lsArrow._center_y+h,
            'L', startPos+duan*5, lsArrow._center_y+h/2,
            'L', startPos+duan*4, lsArrow._center_y+h,
            'L', startPos+duan*3, lsArrow._center_y+h/2,
            'L', startPos+duan*2, lsArrow._center_y+h,
            'L', startPos+duan, lsArrow._center_y+h/2,
            'L', startPos, lsArrow._center_y+h,
            'Z'];
        arrow.attr({
            "d": description.join(' '),
            "fill": color
        });
        arrow.css("cursor", "pointer");
        lsArrow._svg.append(arrow);
        return arrow;
    },

    // 画矩形
    drawRect: function(startPos, color) {
        var rect = $(document.createElementNS(lsArrow.SVG_NS, 'rect'));
        rect.attr({
            "x": startPos,
            "y": lsArrow._center_y-lsArrow._height/2,
            "width": lsArrow._rectLen,
            "height": lsArrow._height,
            "fill": color
        });
        rect.css("cursor", "pointer");
        lsArrow._svg.append(rect);
        return rect;
    },

    // 画菱形
    drawDiamond: function(startPos, color) {
        var diamond = $(document.createElementNS(lsArrow.SVG_NS, 'polygon'));
        diamond.attr({
            "points": startPos+","+lsArrow._center_y+" "+(startPos+lsArrow._diamondLen/2)+","+(lsArrow._center_y-lsArrow._height/2)+" "+(startPos+lsArrow._diamondLen)+","+(lsArrow._center_y)+" "+(startPos+lsArrow._diamondLen/2)+","+(lsArrow._center_y+lsArrow._height/2),
            "fill": color
        });
        diamond.css("cursor", "pointer");
        lsArrow._svg.append(diamond);
        return diamond;
    },

    // 画分隔线
    drawLine: function(startPos) {
        var line = $(document.createElementNS(lsArrow.SVG_NS, 'rect'));
        line.attr({
            "x": startPos,
            "y": lsArrow._center_y-lsArrow._spaceH/2,
            "width": lsArrow._spaceLen,
            "height": lsArrow._spaceH,
            "fill": "#555"
        });
        lsArrow._svg.append(line);
    },

    // 画预定义箭头
    drawDefsArrow: function(color) {
        var marker = document.createElementNS(lsArrow.SVG_NS, "marker");
        marker.setAttribute("id", color);
        marker.setAttribute("markerWidth", "13");
        marker.setAttribute("markerHeight", "13");
        marker.setAttribute("refX", "2");
        marker.setAttribute("refY", "6");
        marker.setAttribute("orient", "auto");
        var path = document.createElementNS(lsArrow.SVG_NS, "path");
        path.setAttribute("d", "M2,2 L2,11 L10,6 L2,2");
        path.setAttribute("fill", color);
        path.setAttribute("style", "cursor: pointer");
        marker.appendChild(path);
        lsArrow._defs.append(marker);
    },

    // 画箭头连线
    drawBezierArrow: function(startPos, endPos, color) {
        var path = document.createElementNS(lsArrow.SVG_NS, "path");
        // path.setAttribute("d", "M "+startPos+","+(lsArrow._center_y-lsArrow._height/2)+" Q "+(startPos+endPos)/2+","+(lsArrow._center_y-100)+" "+(endPos+5)+","+(lsArrow._center_y-lsArrow._arrowH/2-5));
        var h = Math.round(Math.random()*20);
        if ( lsArrow._dir==0 ) {
            var description = ['M', startPos, lsArrow._center_y-lsArrow._arrowH/2,
                'L', startPos, lsArrow._center_y-lsArrow._arrowH/2-h-20,
                'L', endPos, lsArrow._center_y-lsArrow._arrowH/2-h-20,
                'L', endPos, lsArrow._center_y-lsArrow._arrowH/2
            ];
            lsArrow._dir = 1;
        } else {
            var description = ['M', startPos, lsArrow._center_y+lsArrow._arrowH/2,
                'L', startPos, lsArrow._center_y+lsArrow._arrowH/2+h+20,
                'L', endPos, lsArrow._center_y+lsArrow._arrowH/2+h+20,
                'L', endPos, lsArrow._center_y+lsArrow._arrowH/2
            ];
            lsArrow._dir = 0;
        }
        path.setAttribute("d", description.join(' '));
        path.setAttribute("stroke", color);
        path.setAttribute("stroke-width", "1");
        path.setAttribute("fill", "none");
        path.setAttribute("style", "marker-end: url(#"+color+"); cursor: pointer;");
        lsArrow._svg.append(path);
        return path;
    },

    // 画省略号
    drawPoints: function(startPos) {
        startPos += 5;
        for ( var i=0; i<3; i++ ) {
            var point = $(document.createElementNS(lsArrow.SVG_NS, "circle"));
            point.attr({
                "cx": startPos,
                "cy": lsArrow._center_y,
                "r": 1,
                "fill": "#000"
            });
            lsArrow._svg.append(point);
            startPos += 5;
        }
    }

};