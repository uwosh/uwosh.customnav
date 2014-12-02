jq(document).ready(function(){
jq("#portal-globalnav > li").hover(

function()
{var i = jq("#portal-globalnav > li").index(this);
jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).show("slow");


},
function()
{var i = jq("#portal-globalnav > li").index(this);
  jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").stop(clearQueue="True",gotoEnd="True");
  jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).css("display","none");



});
});
