/**
 * Created by lyk on 2017/5/26 0026.
 */
var  ls = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _id: null, // 元素的id
    _parent: null, // 父元素对象
    _svg: null, // svg对象
    _svgProto: null, //
    _alertBox: null, // 弹框对象
    _legend: null, // csp的legend
    _legend_text: null, // csp的legend的文字
    _base: null, // 圆环的被设计的总长(比例)
    _num: 0, // 分区的个数
    _data: null, // 圆环上csp的数据
    _inData: null, // 内环上的数据
    _outData: null, // 外环上的数据
    _br_cx: 200, // 基础圆环的圆心的x坐标
    _br_cy: 200, // 基础圆环的圆心的y坐标
    _br_r: 150, // 基础圆环的半径
    _br_color: '#ccc', // 基础圆环的颜色
    _br_thick: 20, // 基础圆环的厚度
    _W: 400, // svg宽度
    _H: 400, // svg高度
    _oR: 150, // 外环半径
    _iR: 130, // 内环半径
    _T: 20, // 圆环的厚度
    _baseColor: '#ccc', // 基础圆环的颜色
    _startPos: {x: 200, y: 50}, // baseRing的初始点坐标
    _nodeArr: [], // svg中所有csp节点的对象
    _center_x: null,
    _center_y: null,

    init: function(id, data) {
        ls._id = id;
        ls._base = parseInt(data.allLen);
        ls._data = data.children;
        ls._inData = data.in;
        ls._outData = data.out;
        ls._parent = $("#"+id);
        ls._br_cx = ls._parent.width()/2;
        ls._br_cy = ls._parent.height()/2;
        ls._svgProto = document.createElementNS(ls.SVG_NS, 'svg');
        ls._svg = $(ls._svgProto);
        ls._svg.attr({
            "width": "100%",
            "height": "100%"
        });
        ls._num = data.children.length;

        // 首先画一个圆环
        ls.drawBaseRing();
        // 绘制legend
        ls.drawLengend();
        // 绘制所有的csp
        ls.drawAllcsp();
        // 绘制内外环的东西
        ls.drawInAndOut();
        // 给所有csp对象添加鼠标事件(悬浮，点击)
        ls._nodeArr.forEach(ls.nodeMouseEvent);

        ls._parent.append(ls._svg);
        return ls._nodeArr;
    },

    // 绘制一个基础的灰色的圆环
    drawBaseRing: function() {
        var baseRing = $(document.createElementNS(ls.SVG_NS, 'circle'));
        baseRing.attr({
            "cx": ls._br_cx,
            "cy": ls._br_cy,
            "r": ls._br_r,
            "stroke-width": ls._br_thick,
            "stroke": "#BA55D3",
            "fill": "#fff"
        });

        ls._svg.append(baseRing);
    },

    // 绘制csp的legend
    drawLengend: function() {
        // CRISPR locus
        ls._legend = $(document.createElementNS(ls.SVG_NS, "rect"));
        ls._legend.attr({
            "x": 5,
            "y": 5,
            "width": 30,
            "height": 18,
            "rx": 3,
            "ry": 3,
            "fill": "#ba2134"
        });
        ls._legend.css("cursor", "pointer");
        ls._legend_text = $(document.createElementNS(ls.SVG_NS, "text"));
        ls._legend_text.html("CRISPR locus");
        ls._legend_text.attr({
            "x": 40,
            "y": 18
        });
        ls._legend_text.css({
            "font-size": '16px',
            "cursor": "pointer"
        });
        if ( ls._num ) {
            ls._legend.attr("fill", "#ba2134");
        } else {
            ls._legend.attr("fill", "#ccc");
        }
        ls._svg.append(ls._legend);
        ls._svg.append(ls._legend_text);

        // Genomic island
        ls._legend = $(document.createElementNS(ls.SVG_NS, "rect"));
        ls._legend.attr({
            "x": 5,
            "y": 25,
            "width": 30,
            "height": 18,
            "rx": 3,
            "ry": 3,
            // "fill": "#FFA500"
            "fill": "#00BFFF"
        });
        ls._legend.css("cursor", "pointer");
        ls._legend_text = $(document.createElementNS(ls.SVG_NS, "text"));
        ls._legend_text.html("Genomic island");
        ls._legend_text.attr({
            "x": 40,
            "y": 38
        });
        ls._legend_text.css({
            "font-size": '16px',
            "cursor": "pointer"
        });
        if ( ls._num ) {
            // ls._legend.attr("fill", "#FFA500");
            ls._legend.attr("fill", "#00BFFF");
        } else {
            ls._legend.attr("fill", "#ccc");
        }
        ls._svg.append(ls._legend);
        ls._svg.append(ls._legend_text);

        // Prophage region
        ls._legend = $(document.createElementNS(ls.SVG_NS, "rect"));
        ls._legend.attr({
            "x": 5,
            "y": 45,
            "width": 30,
            "height": 18,
            "rx": 3,
            "ry": 3,
            // "fill": "#00BFFF"
            "fill": "#FFA500"
        });
        ls._legend.css("cursor", "pointer");
        ls._legend_text = $(document.createElementNS(ls.SVG_NS, "text"));
        ls._legend_text.html("Prophage region");
        ls._legend_text.attr({
            "x": 40,
            "y": 58
        });
        ls._legend_text.css({
            "font-size": '16px',
            "cursor": "pointer"
        });
        if ( ls._num ) {
            // ls._legend.attr("fill", "#00BFFF");
            ls._legend.attr("fill", "#FFA500");
        } else {
            ls._legend.attr("fill", "#ccc");
        }
        ls._svg.append(ls._legend);
        ls._svg.append(ls._legend_text);
    },

    // 绘制内外环上的数据
    drawInAndOut: function() {
        var x1, // csp的起始的x坐标(out)
            y1, // csp的起始的y坐标(out)
            tx1, // csp的终止的x坐标(out)
            ty1, // csp的终止的x坐标(out)
            x2, // csp的起始的x坐标(in)
            y2, // csp的起始的y坐标(in)
            tx2, // csp的终止的x坐标(in)
            ty2, // csp的终止的x坐标(in)
            theta1, // csp的起始的坐标与Y轴的角度
            theta2, // csp的终止的坐标与Y轴的角度
            large_arc_flag, // csp图形是否是大弧度角(out)
            obj, // 矢量对象
            description; // 矢量对象的描述
        if ( ls._inData.length ) {
            for ( var i=0; i<ls._inData.length; i++ ) {
                theta1 = Math.PI * 2 * (parseInt(ls._inData[i].start_coord) / ls._base);
                x1 = ls._br_cx + (ls._br_r-ls._br_thick/2-10) * Math.cos(theta1);
                y1 = ls._br_cy + (ls._br_r-ls._br_thick/2-10) * Math.sin(theta1);
                x2 = ls._br_cx + (ls._br_r-ls._br_thick/2-5) * Math.cos(theta1);
                y2 = ls._br_cy + (ls._br_r-ls._br_thick/2-5) * Math.sin(theta1);
                theta2 = Math.PI * 2 * ( parseInt(ls._inData[i].end_coord) / ls._base);
                if ( theta2-theta1<Math.PI/360 ) {
                    theta2 = theta1 + Math.PI/360;
                }
                tx1 = ls._br_cx + (ls._br_r-ls._br_thick/2-5) * Math.cos(theta2);
                ty1 = ls._br_cy + (ls._br_r-ls._br_thick/2-5) * Math.sin(theta2);
                tx2 = ls._br_cx + (ls._br_r-ls._br_thick/2-10) * Math.cos(theta2);
                ty2 = ls._br_cy + (ls._br_r-ls._br_thick/2-10) * Math.sin(theta2);

                if ( theta2-theta1<Math.PI ) {
                    large_arc_flag = 0;
                } else {
                    large_arc_flag = 1;
                }

                description = ['M', x1, y1, 'L', x2, y2, 'A', ls._br_r-5, ls._br_r-5, 0, large_arc_flag, 1, tx1, ty1, 'L', tx2, ty2, 'A', ls._br_r-5, ls._br_r-5, 0, large_arc_flag, 0, x1, y1]
                //description = ['M', x1, y1, 'A', ls._br_r, ls._br_r, 0, large_arc_flag, 1, tx1, ty1, 'L', tx2, ty2, 'A', ls._br_r, ls._br_r, 0, large_arc_flag, 0, x2, y2, 'Z'];

                obj = $(document.createElementNS(ls.SVG_NS, 'path'));
                obj.attr({
                    "d": description.join(' '),
                    "fill": "#FFA500",
                    // "stroke": "#FFA500"
                });
                ls._svg.append(obj);
            }
        }

        if ( ls._outData.length ) {
            for ( var i=0; i<ls._outData.length; i++ ) {
                theta1 = Math.PI * 2 * (parseInt(ls._outData[i].start) / ls._base);
                x1 = ls._br_cx + (ls._br_r+ls._br_thick/2+10) * Math.cos(theta1);
                y1 = ls._br_cy + (ls._br_r+ls._br_thick/2+10) * Math.sin(theta1);
                x2 = ls._br_cx + (ls._br_r+ls._br_thick/2+5) * Math.cos(theta1);
                y2 = ls._br_cy + (ls._br_r+ls._br_thick/2+5) * Math.sin(theta1);
                theta2 = Math.PI * 2 * ( parseInt(ls._outData[i].end) / ls._base);
                if ( theta2-theta1<Math.PI/360 ) {
                    theta2 = theta1 + Math.PI/360;
                }
                tx1 = ls._br_cx + (ls._br_r+ls._br_thick/2+5) * Math.cos(theta2);
                ty1 = ls._br_cy + (ls._br_r+ls._br_thick/2+5) * Math.sin(theta2);
                tx2 = ls._br_cx + (ls._br_r+ls._br_thick/2+10) * Math.cos(theta2);
                ty2 = ls._br_cy + (ls._br_r+ls._br_thick/2+10) * Math.sin(theta2);

                if ( theta2-theta1<Math.PI ) {
                    large_arc_flag = 0;
                } else {
                    large_arc_flag = 1;
                }

                description = ['M', x1, y1, 'L', x2, y2, 'A', ls._br_r-5, ls._br_r-5, 0, large_arc_flag, 1, tx1, ty1, 'L', tx2, ty2, 'A', ls._br_r-5, ls._br_r-5, 0, large_arc_flag, 0, x1, y1];
                //description = ['M', x1, y1, 'A', ls._br_r, ls._br_r, 0, large_arc_flag, 1, tx1, ty1, 'L', tx2, ty2, 'A', ls._br_r, ls._br_r, 0, large_arc_flag, 0, x2, y2, 'Z'];

                obj = $(document.createElementNS(ls.SVG_NS, 'path'));
                obj.attr({
                    "d": description.join(' '),
                    "fill": "#00BFFF",
                    // "stroke": "#00BFFF"
                });
                ls._svg.append(obj);
            }
        }
    },

    // 绘制所有的csp对象
    // 注：svg绘图有一个需要特别注意的问题
    // 当用path绘制圆环的一部分的时候
    // 其x y轴坐标是基于圆环的中心圆的
    drawAllcsp: function() {
        var x1, // csp的起始的x坐标(out)
            y1, // csp的起始的y坐标(out)
            tx1, // csp的终止的x坐标(out)
            ty1, // csp的终止的x坐标(out)
            x2, // csp的起始的x坐标(in)
            y2, // csp的起始的y坐标(in)
            tx2, // csp的终止的x坐标(in)
            ty2, // csp的终止的x坐标(in)
            theta1, // csp的起始的坐标与Y轴的角度
            theta2, // csp的终止的坐标与Y轴的角度
            large_arc_flag, // csp图形是否是大弧度角(out)
            obj, // 矢量对象
            description; // 矢量对象的描述

        var lenArr = [30, 40, 50];

        for (var i=0; i<ls._num; i++ ) {
            theta1 = Math.PI * 2 * (parseInt(ls._data[i].startPos) / ls._base);
            x1 = ls._br_cx + (ls._br_r+ls._br_thick/2) * Math.cos(theta1);
            y1 = ls._br_cy + (ls._br_r+ls._br_thick/2) * Math.sin(theta1);
            x2 = ls._br_cx + (ls._br_r-ls._br_thick/2) * Math.cos(theta1);
            y2 = ls._br_cy + (ls._br_r-ls._br_thick/2) * Math.sin(theta1);
            theta2 = Math.PI * 2 * ( (parseInt(ls._data[i].startPos)+parseInt(ls._data[i].length)) / ls._base);
            if ( theta2-theta1<Math.PI/360 ) {
                theta2 = theta1 + Math.PI/360;
            }
            tx1 = ls._br_cx + (ls._br_r+ls._br_thick/2) * Math.cos(theta2);
            ty1 = ls._br_cy + (ls._br_r+ls._br_thick/2) * Math.sin(theta2);
            tx2 = ls._br_cx + (ls._br_r-ls._br_thick/2) * Math.cos(theta2);
            ty2 = ls._br_cy + (ls._br_r-ls._br_thick/2) * Math.sin(theta2);

            if ( theta2-theta1<Math.PI ) {
                large_arc_flag = 0;
            } else {
                large_arc_flag = 1;
            }


            description = ['M', x1, y1, 'A', ls._br_r+ls._br_thick/2, ls._br_r+ls._br_thick/2, 0, large_arc_flag, 1, tx1, ty1, 'L', tx2, ty2, 'A', ls._br_r-ls._br_thick/2, ls._br_r-ls._br_thick/2, 0, large_arc_flag, 0, x2, y2, 'Z'];
            obj = $(document.createElementNS(ls.SVG_NS, 'path'));
            obj.attr({
                "d": description.join(' '),
                "fill": "#ba2134",
                // "style": "cursor: pointer"
            });
            ls._nodeArr.push({"obj": obj, "data": ls._data[i], "flag": 1});
            ls._svg.append(obj);

            var theta = (theta1 + theta2 ) / 2;
            var label = $(document.createElementNS(ls.SVG_NS, 'polyline'));
            label.attr({
                "points": (x1+tx1)/2 + "," + (y1+ty1)/2 + " " 
                        + ((x1+tx1)/2 + lenArr[i%3] * Math.cos(theta)) + "," + ((y1+ty1)/2 + lenArr[i%3]*Math.sin(theta)),
                        // + (direction*100 + (x1+tx1)/2 + 10 * Math.cos(theta)) + "," + ((y1+ty1)/2 + 10*Math.sin(theta)),
                "stroke": "#87CEFA",
                "fill": "white"
            });
            ls._svg.append(label);

            var text = $(document.createElementNS(ls.SVG_NS, "text"));
            text.html((i+1) + ": " + ls._data[i].startPos + "-" + (parseInt(ls._data[i].startPos)+parseInt(ls._data[i].length)));
            text.attr({
                "x": ((x1+tx1)/2 + lenArr[i%3] * Math.cos(theta)),
                "y": ((y1+ty1)/2 + lenArr[i%3]*Math.sin(theta)) + 10* Math.sin(theta)
            });
            text.css({
                "font-size": '10px',
                "cursor": "pointer"
            });
            ls._svg.append(text);

        }
    },

    nodeMouseEvent: function(curObj, objIndex, objArr) {
        curObj.obj.mouseover(function(event){
            $(this).attr({
                "stroke-width": "1",
                "stroke": "#00f",
            });
        });
        curObj.obj.mouseout(function(event){
            if ( curObj.flag ) {
                $(this).attr({
                    "stroke-width": "0"
                });
            }

        });
        curObj.obj.click(function(event){
            for ( var i=0; i<ls._nodeArr.length; i++ ) {
                ls._nodeArr[i].obj.attr("stroke-width", "0");
                ls._nodeArr[i].flag = 1;
            }
            $(this).attr("stroke-width", "1");
            curObj.flag = 0;
        });
    },

    // 构造csp图形的颜色
    createColor: function() {
        var r, g, b;
        r = Math.floor(Math.random()*256);
        g = Math.floor(Math.random()*256);
        b = Math.floor(Math.random()*128);
        return {"r": r, "g": g, "b": b};
    }

};