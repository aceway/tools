//func desc:将input设置为日期段选择控件
//tag_id:input元素的id, 包含#字符
//from_time, 毫秒
//to_time, 毫秒
function set_date_range_picker(tag_id, from_time, to_time)
{
    if(!from_time || (typeof from_time) == 'undefined'){
        var from_time = (new Date()).getTime() - 3600 * 24 * 1000 * 30; 
    }
    ftime = new Date(from_time).format('yyyy-MM-dd');
    if(!to_time || (typeof to_time) == 'undefined'){
        var to_time = (new Date()).getTime();
    }
    ttime = new Date(to_time).format('yyyy-MM-dd');
    $(tag_id).val(ftime + '至' + ttime);

    var the_tag = tag_id.split('#')[1];
    var the_start_id = the_tag +"_start_date";
    var the_end_id   = the_tag +"_end_date";
    var the_old_id   = the_tag +"_old_date";

    $(tag_id).datepicker({
        minDate: "-1y",
        maxDate: "+30d",
        numberOfMonths:2,
        dateFormat:'yy-mm-dd', //    inline: true, 
        monthNames:["1月", "2月", "3月", "4月", "5月", "6月", "7月", "8月", "9月", "10月", "11月", "12月"], 
        dayNamesMin:["日", "一", "二", "三", "四", "五", "六"], 
        showButtonPanel:true,
        beforeShow:this_beforeShowDateSelect,
        onSelect:this_select_start_end_date,
        onClose:this_select_date_cancel,
        closeText:'确定',
        currentText:'今天'
    });
    $(tag_id).parent().append("<span id='"+the_start_id+"'></span>");
    $(tag_id).parent().append("<span id='"+the_end_id+"'></span>");
    $(tag_id).parent().append("<span id='"+the_old_id+"'></span>");

    function this_beforeShowDateSelect(theInput)
    {
        dglog('开始选择之前的老时间：'+ theInput.value, 'info');
        $("#"+the_old_id).text(theInput.value);

        var the_date = $.trim($(tag_id).val()).split('至');
        var d1 = the_date[0].split('-');
        var sy = parseInt(d1[0]);
        var sm = parseInt(d1[1]);
        var sd = parseInt(d1[2]);
        var d2 = the_date[1].split('-');
        var ey = parseInt(d2[0]);
        var em = parseInt(d2[1]);
        var ed = parseInt(d2[2]);

        var ft = (new Date(sy, sm-1, sd)).getTime();
        var tt = (new Date(ey, em-1, ed)).getTime();
        dglog(d1 + ' to ' + d2, 'info');

        //下面功能不能生效, 还没有控件html代码
        $('#ui-datepicker-div td').each(function(idx, ele){//遍历日期上的日期，清除选择的UI标记
            var y = parseInt($(this).attr('data-year'));
            var m = parseInt($(this).attr('data-month'));
            var d = parseInt($(this).text());
            var the_time = (new Date(y, m-1, d)).getTime();
            dglog('from ' + ft + ' to ' + tt + ' now:' + the_time, 'info');
            if(ft<=the_time && the_time<=tt){
                $(this).children('a').removeClass('ui-state-default');
                $(this).addClass('dg-picked-date');
                $(this).children('a').removeClass('ui-state-highlight');
                $(this).children('a').removeClass('ui-state-active');
                $(this).children('a').removeClass('ui-state-hover');
                dglog('set the date:' + y +'-'+ m +'-'+ d, 'info');
            }
        });
    }
    function this_date_range_hover(e)
    {
        var len1 = $.trim($("#"+the_start_id).text());
        var len2 = $.trim($("#"+the_end_id).text());
        if(len1.length >0 && len2.length == 0)
        {
            $('#ui-datepicker-div a').each(function(idx, ele){
                if($(this).hasClass('dg-state-hover')){
                    $(this).removeClass('dg-state-hover');
                    $(this).addClass('ui-state-default');
                }
            });

            var sy = 0;
            var sm = 0;
            var sd = 0;
            $('#ui-datepicker-div a').each(function(idx, ele){//遍历日期上的日期，清除选择的UI标记
                if ($(this).hasClass('ui-state-highlight') && $(this).hasClass('ui-state-active')){
                    sy = parseInt($(this).parent().attr('data-year'));
                    sm = parseInt($(this).parent().attr('data-month'));
                    sd = parseInt($(this).text());
                }
            });
            var ey = parseInt($(this).parent().attr('data-year'));
            var em = parseInt($(this).parent().attr('data-month'));
            var ed = parseInt($(this).text());
            
            $('#ui-datepicker-div a').each(function(idx, ele){
                var ft = (new Date(sy, sm-1, sd)).getTime();
                var tt = (new Date(ey, em-1, ed)).getTime();

                var y = parseInt($(this).parent().attr('data-year'));
                var m = parseInt($(this).parent().attr('data-month'));
                var d = parseInt($(this).text());
                var the_time = (new Date(y, m-1, d)).getTime();

                if(ft <= tt && ft <= the_time && the_time <= tt){
                    $(this).removeClass('ui-state-default');
                    $(this).addClass('dg-state-hover');
                }
                else if(ft>tt && tt <= the_time && the_time <= ft){
                    $(this).removeClass('ui-state-default');
                    $(this).addClass('dg-state-hover');
                }
                else{
                    $(this).addClass('ui-state-default');
                    $(this).removeClass('dg-state-hover');
                }
            });
        }
    }
    
    function this_select_start_end_date(dateText, inst)
    {
        dglog('选择时间:' + dateText, 'info');
        $('#ui-datepicker-div a').removeClass('ui-state-active');
        $('#ui-datepicker-div a').removeClass('ui-state-highlight');
        $('#ui-datepicker-div td').each(function(idx, ele){//遍历日期上的日期，清除选择的UI标记
            var y = parseInt($(this).attr('data-year'));
            var m = parseInt($(this).attr('data-month'));
            var d = parseInt($(this).text());
            var dtinfo = dateText.split('-');
            if(y==parseInt(dtinfo[0]) && m==(parseInt(dtinfo[1])-1) && d==parseInt(dtinfo[2])){
                $(this).children('a').addClass('ui-state-highlight');
                $(this).children('a').addClass('ui-state-active');
            }
            if($(this).children('a').hasClass('dg-state-hover')){
                $(this).children('a').removeClass('dg-state-hover');
            }
        });

        $('button.ui-datepicker-close').click(this_select_date_ok); //设置关闭按钮事件
        $(tag_id).val($("#"+the_old_id).text());  //用老日期初始化控件
    
        var start_date = $.trim($("#"+the_start_id).text());  //取出记录的开始日期
        var end_date   = $.trim($("#"+the_end_id).text());    //取出记录的结束日期
    
        if (start_date.length == 0 && end_date.length == 0){    //如果两个日期都没记录，则本次记录为开始日期
            dglog('选择第一个日期', 'info');
            $('#ui-datepicker-div a').hover(this_date_range_hover);
            //$('#ui-datepicker-div a').bind('hover', this_date_range_hover);
            $("#"+the_start_id).text(dateText);
            $("#"+the_end_id).text('');
            $('#ui-datepicker-div td').each(function(idx, ele){//遍历日期上的日期，清除选择的UI标记
                $(this).removeClass('dg-picked-date');
                $(this).children('a').addClass('ui-state-default');
            });
        }
        else if (start_date.length > 0 && end_date.length > 0){ //如果两个日期都记录在，则本次记录为开始日期, 并清空结束日期
            dglog('重新选择第一个日期', 'info');
            $('#ui-datepicker-div a').hover(this_date_range_hover);
            //$('#ui-datepicker-div a').bind('hover', this_date_range_hover);
            $("#"+the_start_id).text(dateText);
            $("#"+the_end_id).text('');
            $('#ui-datepicker-div td').each(function(idx, ele){//遍历日期上的日期，清除选择的UI标记
                $(this).removeClass('dg-picked-date');
                $(this).children('a').addClass('ui-state-default');
            });
        }
        else if (start_date.length > 0 && end_date.length == 0){ //如果只有开始日期的记录，则本次记录为结束日期
            dglog('选择第二个日期', 'info');
            //$('#ui-datepicker-div a').unbind('hover');
            $("#"+the_end_id).text(dateText);
            var sd_info = start_date.split('-');
            var sd = new Date(sd_info[0], sd_info[1]-1, sd_info[2]);
            var sd_cnt = sd.getTime();//开始日期的秒数
    
            var ed_info = dateText.split('-');
            var ed = new Date(ed_info[0], ed_info[1]-1, ed_info[2]);
            var ed_cnt = ed.getTime();//选择的当前日期的秒数
            $('#ui-datepicker-div td').each(function(idx, ele){//遍历日期上的日期，如果日期在开始 和 结束之间， 则改变UI
                var y = $(this).attr('data-year');
                var m = $(this).attr('data-month');
                var d = $(this).text();
                var the_day = new Date(y, m, d);
                var the_day_cnt = the_day.getTime();
                if(sd<= the_day_cnt && the_day_cnt <= ed){
                    $(this).children('a').removeClass('ui-state-default');
                    $(this).addClass('dg-picked-date');
                    $(this).children('a').removeClass('ui-state-highlight');
                    $(this).children('a').removeClass('ui-state-active');
                    $(this).children('a').removeClass('ui-state-hover');
                }
                else if(ed<= the_day_cnt && the_day_cnt <= sd){
                    $(this).children('a').removeClass('ui-state-default');
                    $(this).addClass('dg-picked-date');
                    $(this).children('a').removeClass('ui-state-highlight');
                    $(this).children('a').removeClass('ui-state-active');
                    $(this).children('a').removeClass('ui-state-hover');
                }
            });
        }
        else{                                                   //如果开始日期没记录，只有结束日期的记录，则重新开始选择
            //$('#ui-datepicker-div a').unbind('hover');
            $("#"+the_start_id).text('');
            $("#"+the_end_id).text('');
        }
    }
    
    function this_select_date_ok(dateText, inst)
    {
        dglog('确定选择,关闭日期窗口：'+ dateText, 'info');
        var start_date = $.trim($("#"+the_start_id).text());
        var end_date   = $.trim($("#"+the_end_id).text());
        if (start_date.length > 0 && end_date.length > 0){
            if(start_date < end_date){
                $(tag_id).val(start_date + "至" + end_date);
            }
            else{
                $(tag_id).val(end_date + "至" + start_date);
            }
        }
        else if(start_date.length > 0){
            $(tag_id).val(start_date + "至" + start_date);
        }
        else if(end_date.length > 0){
            $(tag_id).val(end_date + "至" + end_date);
        }
        else {
            alert('必须选择一个日期才能确定。');
        }
    }
    
    function this_select_date_cancel(dateText, inst)
    {
        var start_date = $.trim($("#"+the_start_id).text());
        var end_date   = $.trim($("#"+the_end_id).text());
        dglog('取消选择,关闭日期窗口：'+ start_date + '至' + end_date, 'info');
    }
}
