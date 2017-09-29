$(function(){
	
	$('#switch_qlogin').click(function(){
		$('#switch_login').removeClass("switch_btn_focus").addClass('switch_btn');
		$('#switch_qlogin').removeClass("switch_btn").addClass('switch_btn_focus');
		$('#switch_bottom').animate({left:'0px',width:'70px'});
		$('#qlogin').css('display','none');
		$('#web_qr_login').css('display','block');
		
		});
	$('#switch_login').click(function(){
		
		$('#switch_login').removeClass("switch_btn").addClass('switch_btn_focus');
		$('#switch_qlogin').removeClass("switch_btn_focus").addClass('switch_btn');
		$('#switch_bottom').animate({left:'154px',width:'70px'});
		
		$('#qlogin').css('display','block');
		$('#web_qr_login').css('display','none');
		});
if(getParam("a")=='0')
{
	$('#switch_login').trigger('click');
}

	});
	
function logintab(){
	scrollTo(0);
	$('#switch_qlogin').removeClass("switch_btn_focus").addClass('switch_btn');
	$('#switch_login').removeClass("switch_btn").addClass('switch_btn_focus');
	$('#switch_bottom').animate({left:'154px',width:'96px'});
	$('#qlogin').css('display','none');
	$('#web_qr_login').css('display','block');
	
}


//根据参数名获得该参数 pname等于想要的参数名 
function getParam(pname) { 
    var params = location.search.substr(1); // 获取参数 平且去掉？ 
    var ArrParam = params.split('&'); 
    if (ArrParam.length == 1) { 
        //只有一个参数的情况 
        return params.split('=')[1]; 
    } 
    else { 
         //多个参数参数的情况 
        for (var i = 0; i < ArrParam.length; i++) { 
            if (ArrParam[i].split('=')[0] == pname) { 
                return ArrParam[i].split('=')[1]; 
            } 
        } 
    } 
}  


var reMethod = "GET",
	pwdmin = 6;

$(document).ready(function() {

    var is_name_error = true;
    var is_upwd_error = true;
    var is_cpwd_error = true;
    var is_email_error = true;
    $('#user').blur(function () {

        	if ($('#user').val() == "") {
			$('#user').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×用户名不能为空</b></font>");
			is_name_error = false;
			return false;
		}

		if ($('#user').val().length < 4 || $('#user').val().length > 16) {

			$('#userCue').html("<font color='red'><b>×用户名位4-16字符</b></font>");
			ris_name_error = false;

		}
		//判断用户名是否注册
        $.post('/login/verify/',{'username':$('#user').val()},function (data) {
            //验证是否存在,存在就提示提示
            if(data.ucode == 1){
               $('#userCue').html("<font color='red'><b>×用户名已存在</b></font>");
                is_name_error = false;
            }else{
                $('#user').focus().css({
				border: "1px solid #D7D7D7",
				boxShadow: "none"
			});
                $('#userCue').html("<font color='black'>快速注册请注意格式</font>");
               is_name_error = true;
            }
            });
        });

    $('#passwd').blur(function () {
         if ($('#passwd').val().length < pwdmin) {
			$('#passwd').focus();
			$('#userCue').html("<font color='red'><b>×密码不能小于" + pwdmin + "位</b></font>");
			is_upwd_error =  false;
		}else {
             $('#userCue').html("<font color='black'>快速注册请注意格式</font>");
             is_upwd_error =  true;
         }
    });
   $('#passwd2').blur(function () {
       	if ($('#passwd2').val() != $('#passwd').val()) {
			$('#passwd2').focus();
			$('#userCue').html("<font color='red'><b>×两次密码不一致！</b></font>");
			is_cpwd_error =  false;
		}else {
       	    $('#userCue').html("<font color='black'>快速注册请注意格式</font>");
       	    is_cpwd_error =  true;
        }
   });

    $('#qq').blur(function () {

        var eamil = /^[a-z0-9][\w\.\-]*@[a-z0-9\-]+(\.[a-z]{2,5}){1,2}$/i;
		if (!eamil.test($('#qq').val() )) {
			$('#qq').focus().css({
				border: "1px solid red",
				boxShadow: "0 0 2px red"
			});
			$('#userCue').html("<font color='red'><b>×Email格式不正确</b></font>");
			is_email_error =  false;
		} else {
			$('#qq').css({
				border: "1px solid #D7D7D7",
				boxShadow: "none"
			});
			$('#userCue').html("<font color='black'>快速注册请注意格式</font>");
			is_email_error = true;
		}
    });

	$('#reg').click(function() {

	    $('#user').blur();
	    $('#passwd').blur();
	    $('#passwd2').blur();
        $('#qq').blur();
        if (is_name_error && is_upwd_error && is_cpwd_error && is_email_error){
           $('#regUser').submit();
        }
	});
	

});