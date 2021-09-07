
/**
 * on change of dropdown
 * Update selected time range
 */
var onTimeRangeChanged = function(event){
    showVisuLoadingSpinner();
    document.getElementById("charts").style.visibility = "hidden";
    time_range_selected = $("#select-time-range-dropdown-form :selected").attr("value");
    console.log(time_range_selected);
    $.ajax({
        url : 'select-time-range-dropdown-form',
        type : "POST",
        data : {
            time_range_selected,
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
    $("#select-time-range-dropdown-form").on("change", onTimeRangeChanged);
});