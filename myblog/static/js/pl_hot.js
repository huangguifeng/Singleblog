/**
 * Created by python on 17-9-30.
 */
$(function () {
    $.post('/pull/',{},function (data) {
        //获取热门文章，评论，最新发布

        $.each(data.zr,function (i,n) {

            var li = '<li class="hot">'+'<a href="/blog/'+i+'"/">'+ n +'</a>'+'</li>';
            $('.hot_ul').append(li);
        });
        $.each(data.wz,function (i,n) {
            var li = '<li class="bpub">'+'<a href="/blog/'+i+'"/">'+ n +'</a>'+'</li>';
            $('.pub_ul').append(li);

        });
        $.each(data.dis,function (i,n) {

            var li = '<li class="new">' + '<p>'+'<a href="/blog/'+n.id+'"/">'+ n.title +'</a>'+'</p>' + '<p>'+'<a   class="disc" href="/blog/'+n.id+'"/">------'+ i +'</a>'+'</p>' +'</li>';
                $('.new_ul').append(li)




        })
    })
});