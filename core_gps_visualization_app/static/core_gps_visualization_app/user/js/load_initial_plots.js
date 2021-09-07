var showVisuLoadingSpinner = function() {
    document.getElementById('visualization-panel-transparent-bgd').style.visibility = "visible";
    document.getElementById('visualization-panel-loading').style.visibility = "visible";
}

var hideVisuLoadingSpinner = function() {
    document.getElementById('visualization-panel-transparent-bgd').style.visibility = "hidden";
    document.getElementById('visualization-panel-loading').style.visibility = "hidden";
}

var loadInitialPlots = function(event){
   document.getElementById("charts").style.visibility = "hidden";
   showVisuLoadingSpinner();
   $.ajax({
    url:"load-initial-plots",
    success: function(data) {
        console.log("Success");
        hideVisuLoadingSpinner();
        // Refresh plots
        var charts = data.charts_html;
        $("#charts").html(charts);
        document.getElementById("charts").style.visibility = "visible";
     },
    error:function(){
           console.log("Error");
           $('#charts').html("Uh oh! An error has occurred. Please check back later...");
    }
    });
 }


 // .ready() called.
$(function() {
   loadInitialPlots();
});