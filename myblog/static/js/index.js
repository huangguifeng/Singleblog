/**
 * Created by python on 17-9-20.
 */
$(function () {
    // 点赞
    $('.top').click(function () {
       var id =  $(this).attr('id');
        var zan = $(this).children('em');
        $.get('/top/',{'id':id},function (data) {
            if(data.is_error == 1){
                zan.text(data.num)
            }
        })
    });
        // 点踩
    $('.step').click(function () {
       var id =  $(this).attr('id');
        var cai =  $(this).children('em');
        $.get('/step/',{'id':id},function (data) {
             if(data.is_error == 1){
                cai.text(data.num)
             }
        })
    });


});
