/**
 * Created by lyk on 2017/6/19 0019.
 */


var lsInteraction = {
    SVG_NS: 'http://www.w3.org/2000/svg',
    _parent: null,
    _id: null,
    _svgProto: null,
    _svg: null, // svg对象
    _center_x: null,
    _center_y: null,
    _spacer_data: null,
    _phage_data: null,
    _baseLen: null,
    _arrowLen: 60,
    _rectLen: 20,
    _spaceLen: 5,
    _leftBtn: null,
    _rightBtn: null,


    init: function(id, data1, data2) {
        lsArrow._id = id;
        lsArrow._parent = $("#"+id);
        lsArrow._parent.next(".move").remove();
        lsArrow._svgProto = document.createElementNS(lsArrow.SVG_NS, 'svg');
        lsArrow._svg = $(lsArrow._svgProto);
        lsArrow._center_x = lsArrow._parent.width() / 2;
        if ( lsArrow._center_x==0 ) {
            lsArrow._center_x = lsArrow._parent.parent().parent().width() / 2;
        }
        lsArrow._center_y = lsArrow._parent.height() / 2;
        lsArrow._svg.attr({
            "width": 2*lsArrow._center_x,
            "height": 2*lsArrow._center_y
        });
        lsArrow._spacer_data = data1;
        lsArrow._phage_data = data2;

        // 计算序列先后顺序
        lsArrow.sortObj(data1);

        this.drawGraph();

    },



    // 计算序列先后顺序
    sortObj: function(data) {
        var sortObj = [];
        for ( var i=0; i<data.length; i++ ) {
            sortArr.push({"data": data[i], "type": 0, "obj": null, "color": null, "flag": 1, "x": null});
        }

        sortArr.sort(lsArrow.sortRule);
        lsArrow._baseLen = lsArrow._spacer_num * lsArrow._rectLen + (2+2*lsArrow._common_num)*lsArrow._spaceLen + lsArrow._spacer_num*lsArrow._diamondLen;
        console.log(lsArrow._baseLen);
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
        }
    },

    // 排序的规则
    sortRule: function(a, b) {
        return parseInt(a.data.startPos) - parseInt(b.data.startPos);
    },


};