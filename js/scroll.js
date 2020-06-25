window.onscroll = function() {scroll();};

//removed document.body.scrollTop > 5 -- not sure what this does
var i = 0;
var height = document.getElementById("main-body").clientHeight;

function scroll() {


  if (document.documentElement.scrollTop > 5) {
    document.getElementById("navBar").style = "background-color: white; border-bottom: 1px solid #EEEEEE;";
  } else {
    document.getElementById("navBar").style = "border-bottom: 0px !important;";
  }
}
