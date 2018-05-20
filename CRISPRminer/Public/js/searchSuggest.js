/**
 * Created by lyk on 2017/6/15 0015.
 */

//实现搜索输入框的输入提示js类
function oSearchSuggest(searchFuc){
    var input = $('#gover_search_key');
    var suggestWrap = $('#gov_search_suggest');
    var key = "";
    var init = function(){
        input.bind('keyup',sendKeyWord);
        input.bind('blur',function(){setTimeout(hideSuggest,100);})
    }
    var hideSuggest = function(){
        suggestWrap.hide();
    }

    //发送请求，根据关键字到后台查询
    var sendKeyWord = function(event){

        //键盘选择下拉项
        if(suggestWrap.css('display')=='block'&&event.keyCode == 38||event.keyCode == 40){
            var current = suggestWrap.find('li.hover');
            if(event.keyCode == 38){
                if(current.length>0){
                    var prevLi = current.removeClass('hover').prev();
                    if(prevLi.length>0){
                        prevLi.addClass('hover');
                        input.val(prevLi.html());
                    }
                }else{
                    var last = suggestWrap.find('li:last');
                    last.addClass('hover');
                    input.val(last.html());
                }

            }else if(event.keyCode == 40){
                if(current.length>0){
                    var nextLi = current.removeClass('hover').next();
                    if(nextLi.length>0){
                        nextLi.addClass('hover');
                        input.val(nextLi.html());
                    }
                }else{
                    var first = suggestWrap.find('li:first');
                    first.addClass('hover');
                    input.val(first.html());
                }
            }

            //输入字符
        }else{
            var valText = $.trim(input.val());
            if(valText ==''||valText==key){
                return;
            }
            searchFuc(valText);
            key = valText;
        }

    }
    //请求返回后，执行数据展示
    this.dataDisplay = function(data){
        if(data.length<=0){
            suggestWrap.hide();
            return;
        }

        //往搜索框下拉建议显示栏中添加条目并显示
        var li;
        var tmpFrag = document.createDocumentFragment();
        suggestWrap.find('ul').html('');
        for(var i=0; i<data.length; i++){
            li = document.createElement('LI');
            li.innerHTML = data[i];
            tmpFrag.appendChild(li);
        }
        suggestWrap.find('ul').append(tmpFrag);
        suggestWrap.show();

        //为下拉选项绑定鼠标事件
        suggestWrap.find('li').hover(function(){
            suggestWrap.find('li').removeClass('hover');
            $(this).addClass('hover');

        },function(){
            $(this).removeClass('hover');
        }).bind('click',function(){
            input.val(this.innerHTML);
            suggestWrap.hide();
        });
    }
    init();
};
