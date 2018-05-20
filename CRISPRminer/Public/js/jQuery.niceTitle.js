/*
 * jQuery niceTitle plugin
 * Version 1.00 (1-SEP-2009)
 * @author leeo(IT北瓜)
 * @requires jQuery v1.2.6 or later
 *
 * Examples at: http://imleeo.com/jquery-example/jQuery.niceTitle.html
 * Copyright (c) 2009-2010 IT北瓜www.imleeo.com
 * Dual licensed under the MIT and GPL licenses:
 * http://www.opensource.org/licenses/mit-license.php
 * http://www.gnu.org/licenses/gpl.html
 
 *History:
 *Version 1.00 (1-SEP-2009) The first release
 *Version 1.10 (7-SEP-2009) Fixed the bug in IE when change parameter "bgColor"(add code: line: 68,69)
 *Version 1.20 (14-SEP-2009) Hide the <img />'s alt and title attributes if <a> includes an image.(code line: 21,46-53,84-87)
 *Version 2.00 (19-SEP-2009) Now niceTitle can works for all HTML tags. Thanks Macek's advice.
 *Version 2.10 (29-Oct-2009) Add a parameter "showLink" to show or hide tag a's href and tag img's src. Fixed the bug, now niceTitle never marks scroll bar appears.
  *Version 2.10 (29-Oct-2009) Add a parameter "brFlag" to make title content multi-line display. Thanks Macek.
 */
;(function($) {
	$.fn.niceTitle = function(options){
		var opts = $.extend({}, $.fn.niceTitle.defaults, options);
		var _self = this, _imgAlt = "", _imgTitle = "", _hasImg = false, _imgObj, _winWidth = $(window).width(), _winHeight = $(window).height(), _scrollTop = $(document).scrollTop(), _domHeight = $(document).height();
		this.initialize = function(_opts){
			$(window).scroll(function () {
			    _scrollTop = $(document).scrollTop();
		    });
			var htmlStr = "";
			//console.log(jQuery.browser);
			if(jQuery.browser && jQuery.browser.msie){//如果是IE浏览器，则通过css来产生圆角效果
			//if(window.ActiveXObject || "ActiveXObject" in window){
				htmlStr = '<div id="niceTitle">' +
							   '<span>' +
								   '<span class="r1"></span>' +
								   '<span class="r2"></span>' +
								   '<span class="r3"></span>' +
								   '<span class="r4"></span>' +
							   '</span>' +
							   '<div id="niceTitle-ie"><p><em></em></p></div>' +
							   '<span>' +
								   '<span class="r4"></span>' +
								   '<span class="r3"></span>' +
								   '<span class="r2"></span>' +
								   '<span class="r1"></span>' +
							   '</span>' +
						    '</div>';
			}else{
				htmlStr = '<div id="niceTitle"><p><em></em></p></div>';
			}
			$(_self).mouseover(function(e){
				var _reg=new RegExp("\\" + _opts.brFlag, "g");
			    this.tmpTitle = $(this).attr("title");//this.title.replace(_reg, "<br />");//等价于$(this).attr("title");//利用正则表达式将"|"替换成"<br />"
				if($(this).is("a")){this.tmpHref = this.href;//等价于$(this).attr("href");
				}else if($(this).is("img")) {this.tmpHref = this.src;//等价于$(this).attr("src");
				}else {this.tmpHref = ""};
			    _imgObj = $(this).find("img");
			    if(_imgObj.length > 0){
			    	_imgAlt = _imgObj.attr("alt");
			    	_imgObj.attr("alt", "");
			    	_imgTitle = _imgObj.attr("title");
			    	_imgObj.attr("title", "");
			    	_hasImg = true;
			    }
				var _length = _opts.urlSize;
				this.title = "";//等价于$(this).attr("title", "");
				if(this.tmpHref.length > 0 && _opts.showLink){
				    this.tmpHref = (this.tmpHref.length > _length ? this.tmpHref.toString().substring(0,_length) + "..." : this.tmpHref);
					$(htmlStr).appendTo("body").find("p").prepend(this.tmpTitle).css({"color": _opts.titleColor}).find("em").text(this.tmpHref).css({"color": _opts.urlColor});
				}else{
					$(htmlStr).appendTo("body").find("p").prepend(this.tmpTitle).css({"color": _opts.titleColor}).find("em").remove();
				}
				var obj = $('#niceTitle');
			    obj.css({
					"position":"absolute",
	                "text-align":"left",
	                "padding":"5px",
					"opacity": _opts.opacity,
				    "top": (_winHeight + _scrollTop - e.pageY - _opts.y) - 10 < obj.height() ? (e.pageY - obj.height() - _opts.y) + "px" : (e.pageY + _opts.y) + "px",
					"left": (_winWidth - e.pageX - _opts.x) - 10 < _opts.maxWidth ?  (e.pageX - _opts.maxWidth - _opts.x) + "px" : (e.pageX + _opts.x) + "px",
					"z-index": _opts.zIndex,
					"max-width": _opts.maxWidth + "px",
					"width": "auto !important",
					"width": _opts.maxWidth + "px",
					"min-height": _opts.minHeight + "px",
					"-moz-border-radius": _opts.radius + "px",
					"-webkit-border-radius": _opts.radius + "px"
				});
				if(!(jQuery.browser && jQuery.browser.msie)){//如果不是IE浏览器
				    obj.css({"background": _opts.bgColor});
				}else{//Version 1.10修正IE下改变背景颜色
				    $('#niceTitle span').css({"background-color": _opts.bgColor, "border-color": _opts.bgColor});
					$('#niceTitle-ie').css({"background": _opts.bgColor, "border-color": _opts.bgColor});
				}
				obj.show('fast');
				return false;//阻止事件冒泡StopPagation()
		    }).mouseout(function(e){
			    this.title = this.tmpTitle;
			    $('#niceTitle').remove();
			    if(_hasImg){
			    	_imgObj.attr("alt", _imgAlt);
			    	_imgObj.attr("title", _imgTitle);
			    }
				return false;//阻止事件冒泡StopPagation()
		    }).mousemove(function(e){
				var obj = $('#niceTitle');
			    obj.css({
			   	    "top": (_winHeight + _scrollTop - e.pageY - _opts.y) - 10 < obj.height() ? (e.pageY - obj.height() - _opts.y) + "px" : (e.pageY + _opts.y) + "px",
					"left": (_winWidth - e.pageX - _opts.x) - 10 < _opts.maxWidth ?  (e.pageX - _opts.maxWidth - _opts.x) + "px" : (e.pageX + _opts.x) + "px"
			    });
				return false;//阻止事件冒泡StopPagation()
		    });
			return _self;
		};
		this.initialize(opts);
	};
    $.fn.niceTitle.defaults = {
		x: 10,
		y: 10,
		urlSize: 30,
		bgColor: "#000",
		titleColor: "#FFF",
		urlColor: "#F60",
		zIndex: 2047,
		maxWidth: 250,
		minHeight: 30,
		opacity: 0.8,
		radius: 8,
		showLink: true,
		brFlag: '|'//标题过长换行分隔符，感谢热心的Macek提出的建议。Thanks Macek!
	};
})(jQuery);