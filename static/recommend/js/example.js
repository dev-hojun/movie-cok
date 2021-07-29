
(function(){

    //IE9+ http://youmightnotneedjquery.com/
    function ready(fn) {
        if (document.attachEvent ? document.readyState === "complete" : document.readyState !== "loading"){
            fn();
        } else {
            document.addEventListener('DOMContentLoaded', fn);
        }
    }

    ready(setupPieChart);


    function setupPieChart() {
		var production = parseFloat(document.getElementById("production").value);
		var acting = parseFloat(document.getElementById("acting").value);
		var story = parseFloat(document.getElementById("story").value);
		var visual = parseFloat(document.getElementById("visual").value);
		var ost = parseFloat(document.getElementById("ost").value);
		
        var dimensions = ['production', 'acting', 'story', 'visual', 'ost'];
        var randomProportions = generateRandomProportions(dimensions.length, 0.05);

		var proportions = [ // 기존 proportions 를 주석처리하고 새로운 proportions 를 만듬
		{ proportion : production, format: {color: "#f44336", label: '연출'}},
		{ proportion : acting, format: {color: "#e91e63", label: '연기'}},
		{ proportion : story, format: {color: "#9c27b0", label: '스토리'}},
		{ proportion : visual, format: {color: "#673ab7", label: '영상미'}},
		{ proportion : ost, format: {color: "#3f51b5", label: 'OST'}}];


        var setup = {
            canvas: document.getElementById('piechart'),
            radius: 0.9,
            collapsing: true,
            proportions: proportions, // 새로 만든 proportions 를 담음
            drawSegment: drawSegmentOutlineOnly,
            onchange: onPieChartChange
        };

        var newPie = new DraggablePiechart(setup); // Draggable.js 파일로 넘김, example.js 에서는 틀만 잡고 실질적인 기능은 Draggable.js 에서 구현

        function drawSegmentOutlineOnly(context, piechart, centerX, centerY, radius, startingAngle, arcSize, format, collapsed) {

            if (collapsed) { return; }

            // Draw segment
            context.save();
            var endingAngle = startingAngle + arcSize;
            context.beginPath();
            context.moveTo(centerX, centerY);
            context.arc(centerX, centerY, radius, startingAngle, endingAngle, false);
            context.closePath();

            context.fillStyle = format.color;
            context.fill();
            context.stroke(); // 구분선 
            context.restore(); 

            // Draw label on top
            context.save();
            context.translate(centerX, centerY);
            context.rotate(startingAngle);

            var fontSize = Math.floor(context.canvas.height / 25);
            var dx = radius - fontSize;
            var dy = centerY / 10;

            context.textAlign = "right";
            context.font = fontSize + "pt Helvetica";
            context.fillText(format.label, dx, dy);
			context.strokeStyle = "white";
            context.restore();
        }

        function onPieChartChange(piechart) {

            var table = document.getElementById('proportions-table');
            var percentages = piechart.getAllSliceSizePercentages();

            var labelsRow = '<tr>';
            var propsRow = '<tr>';
            for(var i = 0; i < proportions.length; i += 1) {
                labelsRow += '<th>' + proportions[i].format.label + '</th>';
				var point = '';
				
                var v = '<var id="'+ dimensions[i] + '" name="'+ dimensions[i] +'" value=' + percentages[i].toFixed(2) + '>' + percentages[i].toFixed(0) + '%</var>';
                var plus = '<div id="plu-' + dimensions[i] + '" class="adjust-button" data-i="' + i + '" data-d="-1">&#43;</div>';
                var minus = '<div id="min-' + dimensions[i] + '" class="adjust-button" data-i="' + i + '" data-d="1">&#8722;</div>';
				var hiddentag = '<input type="hidden" name="' + dimensions[i] + '" value=' + percentages[i].toFixed(2) + '>'
                propsRow += '<td>' + v + plus + minus + hiddentag + '</td>';
            }
            labelsRow += '</tr>';
            propsRow += '</tr>';

            table.innerHTML = labelsRow + propsRow;

            var adjust = document.getElementsByClassName("adjust-button");

            function adjustClick(e) {
                var i = this.getAttribute('data-i');
                var d = this.getAttribute('data-d');

                piechart.moveAngle(i, (d * 0.1));
            }

            for (i = 0; i < adjust.length; i++) {
                adjust[i].addEventListener('click', adjustClick);
            }

        }

        /*
         * Generates n proportions with a minimum percentage gap between them
         */
        function generateRandomProportions(n, min) {

            // n random numbers 0 - 1
            var rnd = Array.apply(null, {length: n}).map(function(){ return Math.random(); });

            // sum of numbers
            var rndTotal = rnd.reduce(function(a, v) { return a + v; }, 0);

            // get proportions, then make sure each propoertion is above min
            return validateAndCorrectProportions(rnd.map(function(v) { return v / rndTotal; }), min);


            function validateAndCorrectProportions(proportions, min) {
                var sortedProportions = proportions.sort(function(a,b){return a - b});

                for (var i = 0; i < sortedProportions.length; i += 1) {
                    if (sortedProportions[i] < min) {
                        var diff = min - sortedProportions[i];
                        sortedProportions[i] += diff;
                        sortedProportions[sortedProportions.length - 1] -= diff;
                        return validateAndCorrectProportions(sortedProportions, min);
                    }
                }

                return sortedProportions;
            }
        }

        /*
         * Array sorting algorithm
         */
        function knuthfisheryates2(arr) {
            var temp, j, i = arr.length;
            while (--i) {
                j = ~~(Math.random() * (i + 1));
                temp = arr[i];
                arr[i] = arr[j];
                arr[j] = temp;
            }

            return arr;
        }
    }

})();



