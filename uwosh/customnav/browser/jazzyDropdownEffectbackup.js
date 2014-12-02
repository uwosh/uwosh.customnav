jq(document).ready(function(){
jq("#portal-globalnav > li").hover(

function()
{var i = jq("#portal-globalnav > li").index(this);
  var imageHeight = jq("#mainImage").outerHeight(true);
  var textSize = imageHeight/23
jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).css("height",imageHeight);
jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).css("font-size",textSize);
jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).show("slow");


},
function()
{var i = jq("#portal-globalnav > li").index(this);
  jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").stop(clearQueue="True",gotoEnd="True");
  jq("#portal-top > #globalnav-wrapper > #portal-globalnav > li  > .submenu").eq(i).css("display","none");



});
});
