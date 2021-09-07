
/**
 * on change of dropdown
 * Update selected chart
 */
var onChartChanged = function(event){
    showVisuLoadingSpinner();
    document.getElementById("charts").style.visibility = "hidden";
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
            // update two other forms, not applicable if boxplot
            // Refresh plots after they were updated
            var charts = data.charts_html;
            $("#charts").html(charts);
            document.getElementById("charts").style.visibility = "visible";
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