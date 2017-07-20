var TDF = function() {

    var data;
    var xDomain;
    var yDomain;

    var _formatData = function(d) {
        // function for testing purposes.
        data = {};
        for (var i = 0; i < d.length; i++) {
            var record = d[i];
            var rider_nr = record.rider_nr;
            var newRecord = {x: record.stage, y: record.rank, name: record.rider_name};
            if (data.hasOwnProperty(rider_nr)) {
                data[rider_nr].push(newRecord);
            } else {
                data[rider_nr] = [newRecord];
            }
        }
    };


    var _init_ = function() {
        d3.json("rankings.json", function(error, alldata) {
            alldata.forEach(function (r) {
                r.stage = parseInt(r.stage);
                r.rank = parseInt(r.rank);
            });
            xDomain = d3.extent(alldata, function(d) {return d.stage;});
            yDomain = d3.extent(alldata, function(d) {return d.rank;});
            _formatData(alldata);
            draw();
        });
    };

    // expose some functions
    this._init_ = _init_;

    function draw() {
        var w = 1100;
        var h = 600;
        var pad = 40;

        var svg = d3.select("#display").append("svg");

        svg.attr("width", w)
            .attr("height", h)
            .attr("id", "chart");

        // Define axes
        var xScale = d3.scale.linear().domain(xDomain).range([pad, w-pad]);
        var xAxis = d3.svg.axis().scale(xScale).orient("bottom").tickSize(h-pad).ticks(21);
        var yScale = d3.scale.linear().domain(yDomain).range([pad, h-pad]);
        var yAxis = d3.svg.axis().scale(yScale).orient("left").ticks(4);

        // Draw xAxis
        var gx = svg.append("g")
            .attr("class", "x axis")
            .attr("transform", "translate(0, " + (pad/2) + ")")
            .call(xAxis);
        gx.selectAll("g").filter(function(d) {return d; })
            .classed("minor", true);

        // Draw yAxis
        svg.append("g")
            .attr("class", "axis")
            .attr("transform", "translate(" + pad + ", 0)")
            .call(yAxis);

        // Define linefunction
        var lineFunction = d3.svg.line()
            .x(function(d) {return xScale(d.x)})
            .y(function(d) {return yScale(d.y)})
            .interpolate("monotone");

        // create the tooltip
        var div = d3.select("#player-name");

        // create a blur filter
        var filter = svg.append("defs")
            .append("filter")
            .attr("id", "blur");

        filter.append("feGaussianBlur")
            .attr("stdDeviation", 3)
            .attr("result", "offsetBlur");

        var feMerge = filter.append("feMerge");

        feMerge.append("feMergeNode")
            .attr("in", "offsetBlur");

        feMerge.append("feMergeNode")
            .attr("in", "SourceGraphic");

        for (var rider_nr in data) {
            if (data.hasOwnProperty(rider_nr)) {
                var standingdata = data[rider_nr];
                standingdata.sort(function (a, b) {
                    if (a.x < b.x) {
                        return -1;
                    } else {
                        return 1;
                    }
                });
                var riderName = data[rider_nr][0].name;
                var playerLine = svg.append("g")
                    .append("path")
                    .attr("d", lineFunction(standingdata))
                    .attr("id", "line-" + rider_nr)
                    .attr("stroke", "#000")
                    .attr("stroke-width", 2)
                    .attr("opacity", ".4")
                    .attr("fill", "none")
                    .attr("name", riderName)
                    .on("mouseover", function (d) {
                        d3.select(this).attr("filter", "url(#blur)")
                            .attr("opacity", "1");
                        div.html("<p>" + d3.select(this).attr("name") + "</p>");
                    })
                    .on("mouseout", function (d) {
                        d3.select(this).attr("filter", "")
                            .attr("opacity", ".4")
                            .attr("stroke", "#000");
                    });
            }
        }

    }

};

var tdf = new TDF();
tdf._init_();