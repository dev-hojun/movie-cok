am4core.ready(function() {

    // Themes begin
    am4core.useTheme(am4themes_animated);
    // Themes end
	var id_list = document.getElementsByName("movie_id");
	var title_list = document.getElementsByName("title");
	var image_list = document.getElementsByName("image");
	var recommend_list0 = document.getElementsByName(id_list[0].value);
	var recommend_list1 = document.getElementsByName(id_list[1].value);
	var recommend_list2 = document.getElementsByName(id_list[2].value);

	// console.log(title_list[0].text);
	// console.log(first_total.value);
	// console.log(image_list[0].src);
    /**
    * Chart design taken from Samsung health app
    */

    var chart = am4core.create("chartdiv", am4charts.XYChart);
    chart.hiddenState.properties.opacity = 0; // this creates initial fade-in

    chart.paddingRight = 30;

    chart.data = [{
        "name": title_list[2].text,
        "steps": recommend_list2[1].value,
        "href": image_list[2].src
    }, {
        "name": title_list[1].text,
        "steps": recommend_list1[1].value,
        "href": image_list[1].src
    }, {
        "name": title_list[0].text,
        "steps": recommend_list0[1].value,
        "href": image_list[0].src
    }];

    var categoryAxis = chart.yAxes.push(new am4charts.CategoryAxis());
    categoryAxis.dataFields.category = "name";
    categoryAxis.renderer.grid.template.strokeOpacity = 0;
    categoryAxis.renderer.minGridDistance = 10;
    categoryAxis.renderer.labels.template.dx = -40;
    categoryAxis.renderer.minWidth = 120;
    categoryAxis.renderer.tooltip.dx = -40;

    var valueAxis = chart.xAxes.push(new am4charts.ValueAxis());
    valueAxis.renderer.inside = true;
    valueAxis.renderer.labels.template.fillOpacity = 0.3;
    valueAxis.renderer.grid.template.strokeOpacity = 0;
    valueAxis.min = 0;
    valueAxis.cursorTooltipEnabled = false;
    valueAxis.renderer.baseGrid.strokeOpacity = 0;
    valueAxis.renderer.labels.template.dy = 20;

    var series = chart.series.push(new am4charts.ColumnSeries);
    series.dataFields.valueX = "steps";
    series.dataFields.categoryY = "name";
    series.tooltipText = "{valueX.value}";
    series.tooltip.pointerOrientation = "vertical";
    series.tooltip.dy = - 30;
    series.columnsContainer.zIndex = 100;

    var columnTemplate = series.columns.template;
    columnTemplate.height = am4core.percent(30);
    columnTemplate.maxHeight = 30;
    columnTemplate.column.cornerRadius(60, 10, 60, 10);
    columnTemplate.strokeOpacity = 0;

    series.heatRules.push({ target: columnTemplate, property: "fill", dataField: "valueX", min: am4core.color("#EDD200"), max: am4core.color("#FF5E00") });
    series.mainContainer.mask = undefined;

    var cursor = new am4charts.XYCursor();
    chart.cursor = cursor;
    cursor.lineX.disabled = true;
    cursor.lineY.disabled = true;
    cursor.behavior = "none";

    var bullet = columnTemplate.createChild(am4charts.CircleBullet);
    bullet.circle.radius = 30;
    bullet.valign = "middle";
    bullet.align = "left";
    bullet.isMeasured = true;
    bullet.interactionsEnabled = false;
    bullet.horizontalCenter = "right";
    bullet.interactionsEnabled = false;

    var hoverState = bullet.states.create("hover");
    var outlineCircle = bullet.createChild(am4core.Circle);
    outlineCircle.adapter.add("radius", function (radius, target) {
        var circleBullet = target.parent;
        return circleBullet.circle.pixelRadius + 10;
    })

    var image = bullet.createChild(am4core.Image);
    image.width = 60;
    image.height = 60;
    image.horizontalCenter = "middle";
    image.verticalCenter = "middle";
    image.propertyFields.href = "href";

    image.adapter.add("mask", function (mask, target) {
        var circleBullet = target.parent;
        return circleBullet.circle;
    })

    var previousBullet;
    chart.cursor.events.on("cursorpositionchanged", function (event) {
        var dataItem = series.tooltipDataItem;

        if (dataItem.column) {
            var bullet = dataItem.column.children.getIndex(1);

            if (previousBullet && previousBullet != bullet) {
                previousBullet.isHover = false;
            }

            if (previousBullet != bullet) {

                var hs = bullet.states.getKey("hover");
                hs.properties.dx = dataItem.column.pixelWidth;
                bullet.isHover = true;

                previousBullet = bullet;
            }
        }
    })
	

    }); // end am4core.ready()
	// function point(){
		// alert(title_list[0].text);
	// }