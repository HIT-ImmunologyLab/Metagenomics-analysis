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
        _randArr: [30, 60, 90, 120],

        init: function(id, data1, data2) {
            lsArrow._sortArr.splice(0, lsArrow._sortArr.length);
            lsArrow._startArr.splice(0, lsArrow._startArr.length);
            lsArrow._endArr.splice(0, lsArrow._endArr.length);
            lsArrow._bezierArr.splice(0, lsArrow._bezierArr.length);

            lsArrow._id = id;
            lsArrow._parent = $("#"+id);
            lsArrow._parent.next(".move").remove();
            lsArrow._center_x = lsArrow._parent.width() / 2;
            if ( lsArrow._center_x==0 ) {
                lsArrow._center_x = lsArrow._parent.parent().parent().width() / 2;
            }
            lsArrow._center_y = lsArrow._parent.height() / 2;
            lsArrow._svgProto = document.createElementNS(lsArrow.SVG_NS, 'svg');
            lsArrow._svg = $(lsArrow._svgProto);
            lsArrow._svg.attr({
                "width": 2*lsArrow._center_x,
                "height": 2*lsArrow._center_y
            });
            lsArrow._svgProto.setAttribute("viewBox", "0 0 "+(2*lsArrow._center_x+200)+" "+(2*lsArrow._center_y));
            lsArrow._spacer_num = data1.length;
            lsArrow._spacer_data = data1;
            lsArrow._common_num = data2.length;
            lsArrow._common_data = data2;

            lsArrow._defs = document.createElementNS(lsArrow.SVG_NS, "defs");
            lsArrow._svg.append(lsArrow._defs);

            // lsArrow._svg.css("width", data1.length*(lsArrow._rectLen+2*lsArrow._diamondLen)+100);

            // 计算序列先后顺序
            lsArrow.sortObj();

            // 绘制
            lsArrow.drawGraph();

            lsArrow._parent.append(lsArrow._svg);
        },

        // 计算序列先后顺序
        sortObj: function() {
            for ( var i=0; i<lsArrow._spacer_num; i++ ) {
                lsArrow._sortArr.push({"data": lsArrow._spacer_data[i], "type": 1, "obj": null, "ref": null, "color": null, "flag": 1, "x": null});
            }

            for ( var i=0; i<lsArrow._common_num; i++ ) {
                for ( var j=0; j<lsArrow._sortArr.length; j++ ) {
                    if ( lsArrow._common_data[i]['spacer_id']==lsArrow._sortArr[j]['data']['id'] ) {
                        lsArrow._sortArr[j]['ref'] = lsArrow._common_data[i]['data'];
                        break;
                    }
                }
            }

            lsArrow._sortArr.sort(lsArrow.sortRule);
            lsArrow._baseLen = lsArrow._spacer_num * lsArrow._rectLen + 2*lsArrow._spaceLen + (1+lsArrow._spacer_num)*lsArrow._diamondLen + 200;

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
                lsArrow._svgProto.setAttribute("viewBox", "0 0 "+lsArrow._baseLen+" "+(lsArrow._center_y*2));
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
            lsArrow.drawLine(startPos);
            startPos += lsArrow._spaceLen;
            lsArrow.drawDiamond(startPos, "#0f0");
            startPos += lsArrow._diamondLen;
            var flag = 1, index, pos;
            for ( var i=0; i<num; i++ ) {
                obj = lsArrow.drawRect(startPos, "#00f");
                lsArrow._sortArr[i].obj = obj;
                lsArrow._sortArr[i].color = "#00f";
                if ( lsArrow._sortArr[i].ref ) {
                    index = Math.floor(4*Math.random());
                    pos = lsArrow._randArr[index];
                    lsArrow.drawText(startPos, pos, flag, "#000", lsArrow._sortArr[i].ref[0]['phage_name']);
                    lsArrow.drawStraightLine(startPos+lsArrow._rectLen/2, lsArrow._center_y, startPos+lsArrow._rectLen/2, lsArrow._center_y-flag*pos);
                    flag *= -1;
                }
                startPos += lsArrow._rectLen;
                lsArrow.drawDiamond(startPos, "#0f0");
                startPos += lsArrow._diamondLen;
            }
            lsArrow.drawLine(startPos);
            startPos += lsArrow._spaceLen;

            if ( lsArrow._leftBtn && lsArrow._rightBtn ) {
                lsArrow.dragLeft(lsArrow._leftBtn);
                lsArrow.dragRight(lsArrow._rightBtn);
            }

        },

        drawStraightLine: function(startX, startY, endX, endY) {
            var line = $(document.createElementNS(lsArrow.SVG_NS, 'path'));
            var description = ['M', startX, startY, 'L', endX, endY];
            line.attr({
                "d": description.join(' '),
                "stroke": "#00f"
            });
            lsArrow._svg.append(line);
        },

        // 起始位置 颜色  y轴坐标    文字
        drawText: function(startPos, height, flag, color, ctx) {
            var text = $(document.createElementNS(lsArrow.SVG_NS, "text"));
            var h = lsArrow._center_y-flag*height;
            text.attr({
                "x": startPos,
                "y":h,
                "fill": color,
                "font-size": 10,
                "cursor": "pointer"
            });
            if ( ctx!="NULL" && ctx ) {
                // text.attr("title", ctx);
                // if ( ctx.length>7 ) {
                //     ctx = ctx.slice(0, 6); // 切割字符串
                // }
                text.html(ctx);
            }

            lsArrow._svg.append(text);
        },


        // 向左拖动svg
        dragLeft: function(btn) {
            btn.click(function() {
                console.log("dragLeft");
                if ( lsArrow._svgX>0 ) {
                    lsArrow._svgX -= lsArrow._center_x;
                    lsArrow._svgProto.setAttribute("viewBox", lsArrow._svgX+" 0 "+(lsArrow._center_x*2)+" "+(lsArrow._center_y*2));
                }

            });
        },

        // 向右拖动svg
        dragRight: function(btn) {
            btn.click(function() {
                console.log("dragRight");
                if ( lsArrow._svgX<lsArrow._baseLen ) {
                    lsArrow._svgX += lsArrow._center_x;
                    lsArrow._svgProto.setAttribute("viewBox", lsArrow._svgX+" 0 "+(lsArrow._center_x*2)+" "+(lsArrow._center_y*2));
                }
            });
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


};
