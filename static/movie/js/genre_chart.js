am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_material);
    am4core.useTheme(am4themes_animated);
    // Themes end

    // Create chart instance
    var chart = am4core.create("chartdiv_2", am4charts.PieChart);
    
	var production = document.getElementById("production").value;
	var acting = document.getElementById("acting").value;
	var story = document.getElementById("story").value;
	var visual = document.getElementById("visual").value;
	var ost = document.getElementById("ost").value;

    // Add data
    chart.data = [ {
      "point": "연출",
      "litres": production
    }, {
      "point": "연기",
      "litres": acting
    }, {
      "point": "스토리",
      "litres": story
    }, {
      "point": "영상미",
      "litres": visual
    }, {
      "point": "OST",
      "litres": ost
    } ];
    
// Add and configure Series
var pieSeries = chart.series.push(new am4charts.PieSeries());
pieSeries.dataFields.value = "litres";
pieSeries.dataFields.category = "point";
pieSeries.slices.template.stroke = am4core.color("#fff");
pieSeries.slices.template.strokeOpacity = 1;

// This creates initial animation
pieSeries.hiddenState.properties.opacity = 1;
pieSeries.hiddenState.properties.endAngle = -90;
pieSeries.hiddenState.properties.startAngle = -90;

chart.hiddenState.properties.radius = am4core.percent(0);


}); // end am4core.ready()