
/**
 * on change of dropdown
 * Update selected chart
 */
var onChartChanged = function(event){
    document.getElementById("visualization").style.visibility = "visible";
    showVisuLoadingSpinner();
    plot_selected = $("#select-chart-dropdown-form :selected").attr("value");
    console.log(plot_selected);
    $.ajax({
        url : 'select-chart-dropdown-form',
        type : "POST",
        data : {
            plot_selected,
        },
        success: function(data){
            hideVisuLoadingSpinner();
            // Refresh plots after they were updated
            if (data.script === '404') {
                document.getElementById("charts404").style.visibility = "visible";
                document.getElementById('charts404').style.height = "200px";
                }
            else {
                $("#visualization").html(data.script);
                document.getElementById('charts404').style.height = "0px";
            }
        },
        error: function(data){
            console.log("Error");
        }
    });
}

// .ready() called.
$(function() {
    // bind change event to dropdown box
    $("#select-chart-dropdown-form").on("change", onChartChanged);
});