am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
    
    // Create chart instance
    var chart = am4core.create("chartdiv", am4charts.XYChart3D);
    
    // Add data
    chart.data = [{
      "age": "10대",
      "income": 9.12,
      "color": chart.colors.next()
    }, {
      "age": "20대",
      "income": 8.86,
      "color": chart.colors.next()
    }, {
      "age": "30대",
      "income": 8.67,
      "color": chart.colors.next()
    }, {
      "age": "40대",
      "income": 8.00,
      "color": chart.colors.next()
    }, {
      "age": "50대",
      "income": 8.47,
      "color": chart.colors.next()
    }];
    
    // Create axes
    var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "age";
    categoryAxis.numberFormatter.numberFormat = "#";
    categoryAxis.renderer.inversed = true;
    
    var  valueAxis = chart.xAxes.push(new am4charts.ValueAxis()); 
    
    // Create series
    var series = chart.series.push(new am4charts.ColumnSeries3D());
    series.dataFields.valueX = "income";
    series.dataFields.categoryY = "age";
    series.name = "Income";
    series.columns.template.propertyFields.fill = "color";
    series.columns.template.tooltipText = "{valueX}";
    series.columns.template.column3D.stroke = am4core.color("#fff");
    series.columns.template.column3D.strokeOpacity = 0.2;
    
    }); // end am4core.ready()