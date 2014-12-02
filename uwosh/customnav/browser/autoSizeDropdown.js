jq(document).ready(function(){
    jq(window).load(function(){

	if (((jq("#mainImage").outerHeight()) > 200)) {

  var imageHeight = jq("#mainImage").outerHeight();
  var pgnHeight = jq("#portal-globalnav").outerHeight();
  var height = imageHeight - pgnHeight;
  var textSize = imageHeight/22;

jq("#portal-globalnav > li  > .submenu").css("height",height);
jq("#portal-globalnav > li  > .submenu").css("font-size",textSize);
jq("#portal-globalnav > li  > .submenu").css("width","700px");
	}

	else {
jq("#portal-globalnav > li  > .submenu").css("height","200px");
jq("#portal-globalnav > li  > .submenu").css("font-size","10");
jq("#portal-globalnav > li  > .submenu").css("width","700px");
}
      });


});
