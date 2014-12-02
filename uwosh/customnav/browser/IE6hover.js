jq(document).ready(function(){
jq("#portal-globalnav > li").hover(

function()
{var i = jq("#portal-globalnav > li").index(this);
jq("#portal-globalnav > li  > .submenu").eq(i).css({'display' : 'block'});
},
function()
{var i = jq("#portal-globalnav > li").index(this);
jq("#portal-globalnav > li  > .submenu").eq(i).css({'display' : 'none'});
});
});





