class Graph {
    static GRAPH = null;

    constructor(svg, graph) {
        Graph.GRAPH = this;

        this.properties = {
            sticky_nodes: false,
            node_size:    5,
            colors:       d3.scaleOrdinal(d3.schemeCategory10)
        }

        this.svg = d3.select(svg);
        this.svg.on("click", Graph.hideContextMenu);

        this.anchor = this.svg.append("g");
        this.anchor.on("click", Graph.hideContextMenu);

        this.graph = graph;
        const width  = this.svg.node().getBoundingClientRect().width;
        const height = this.svg.node().getBoundingClientRect().height;

        this.createContainer();
        this.createLinks();
        this.createNodes();
        this.createLinkLabels();
        this.createNodeLabels();

        this.simulation = d3
            .forceSimulation(this.graph.nodes)
            .force("charge", d3.forceManyBody().strength(-10000))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("x", d3.forceX(width / 2).strength(0.1))
            .force("y", d3.forceY(height / 2).strength(0.1))
            .force("link", d3.forceLink(this.graph.links).id(function (l) {return l.id; }).distance(25).strength(1))
            .on("tick", Graph.onTick);

        this.zoom_level = d3
            .zoom()
            .scaleExtent([.1, 4])
            .on("zoom", Graph.onZoom);
        this.svg.call(this.zoom_level);

        this.nodes.call(
            d3.drag()
              .on("start", function (n) {
                  d3.event.sourceEvent.stopPropagation();
                  if (!d3.event.active)
                      Graph.Simulation.alphaTarget(0.5).restart();
                  n.fx = n.x;
                  n.fy = n.y;
              })
              .on("drag", function (n) {
                  n.fx = d3.event.x;
                  n.fy = d3.event.y;
                  Graph.hideContextMenu();
              })
              .on("end", function (n) {
                  if (!Graph.get("sticky")) {
                      if (!d3.event.active)
                          Graph.Simulation.alphaTarget(0);
                      n.fx = null;
                      n.fy = null;
                  }
              })
        );

        Graph.zoom(2)
    }

    static get SVG() { return Graph.GRAPH.svg; }

    static get Anchor() { return Graph.GRAPH.anchor; }

    static get Simulation() { return Graph.GRAPH.simulation; }

    static get Graph() { return Graph.GRAPH.graph; }

    static get Nodes() { return Graph.GRAPH.nodes; }

    static get NodeLabels() { return Graph.GRAPH.node_labels; }

    static get Edges() { return Graph.GRAPH.edges; }

    static get EdgeLabels() { return Graph.GRAPH.edge_labels; }

    static get(property) { return Graph.GRAPH.get(property); }

    static set(property, value) { Graph.GRAPH.set(property, value); }

    get(property) { return this.properties[property]; }

    set(property, value) { this.properties[property] = value; }

    /* Init Graph */

    createContainer() {
        const node_size = this.get("node_size");
        this.anchor
            .append("svg:defs")
            .selectAll("marker")
            .data(["end"])
            .enter()
            .append("svg:marker")
            .attr("id", String)
            .attr("class", "arrowhead")
            .attr("viewBox", "0 -2 6 4")
            .attr("markerWidth", node_size * 1.25)
            .attr("markerHeight", node_size * 1.25)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M 0,-2 L 6,0 L 0,2");
    }

    createLinks() {
        this.edges = this
            .anchor
            .append("g")
            .attr("class", "edges")
            .selectAll("line")
            .data(this.graph.links)
            .enter()
            .append("path")
            .attr("marker-end", "url(#end)")
            .attr("d", "M 0 0 L 0 0")
            .on("click", Graph.onLinkClick);
    }

    createNodes() {
        this.nodes = this
            .anchor
            .append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(this.graph.nodes)
            .enter()
            .append("circle")
            .attr("r", this.get("node_size"))
            .attr("id", function (n) { return n.id; })
            .attr("fill", function (n) { if (n.hazard) return 'red'; else return Graph.get("colors")(n.group); })
            .on("contextmenu", Graph.onContextMenu)
            .on("click", Graph.onNodeClick);
    }

    createLinkLabels() {
        this.node_labels = this
            .anchor
            .append("g")
            .attr("class", "node-labels")
            .selectAll("g")
            .data(this.graph.nodes)
            .enter()
            .append("text")
            .text(function (n) { return n.label; });
    }

    createNodeLabels() {
        this.edge_labels = this
            .anchor
            .append("g")
            .attr("class", "edge-labels")
            .selectAll("g")
            .data(this.graph.links)
            .enter()
            .append("text")
            .text(function (l) { return l.label; });
    }

    /* Callbacks */

    static onTick() {
        Graph.Edges.attr("d", function (l) {
            const x1 = l.source.x,
                  y1 = l.source.y,
                  x2 = l.target.x,
                  y2 = l.target.y;

            if (l.source !== l.target) {
                const dx = x2 - x1,
                      dy = y2 - y1,
                      dr = Math.sqrt(dx * dx + dy * dy);

                return "M {} {} A {} {} 0 0 1 {} {}".format(x1, y1, dr, dr, x2, y2); // curved line
                // return "M {} {} L {} {}".format(x1, y1, x2, y2) // straight line
            }
            const scale = l.label.length * 3; // TODO size of the curve
            return "M {} {} C {} {} {} {} {} {}".format(x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, x2, y2);
        })

        Graph.Edges.attr("d", function (l) {
            const x1 = l.source.x,
                  y1 = l.source.y,
                  x2 = l.target.x,
                  y2 = l.target.y;

            const pl = this.getTotalLength(),
                  r  = 5 + 6,
                  m  = this.getPointAtLength(pl - r);

            const dx = m.x - x1,
                  dy = m.y - y1,
                  dr = Math.sqrt(dx * dx + dy * dy);

            if (l.source !== l.target) {
                return "M" + x1 + "," + y1 + "A" + dr + "," + dr + " 0 0,1 " + m.x + "," + m.y;
            } else {
                const scale = l.label.length * 3; // TODO size of the curve
                return "M {} {} C {} {} {} {} {} {}".format(x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, m.x, m.y);
            }
        })

        Graph.Nodes
             .attr("cx", function (n) { return n.x; })
             .attr("cy", function (n) { return n.y; });

        Graph.NodeLabels
             .attr("x", function (n) { return n.x + 10; })
             .attr("y", function (n) { return n.y; });

        Graph.EdgeLabels
             .attr("x", function (l) { return l.source.x + (l.target.x - l.source.x) * 0.5 + 10; })
             .attr("y", function (l) { return l.source.y + (l.target.y - l.source.y) * 0.5 + 15; });
    }

    static onZoom() {
        Graph.Anchor.attr("transform", d3.event.transform);
        d3.select("#zoom").property("value", d3.event.transform.k);
        Graph.hideContextMenu();
    }

    static onLinkClick(e, _, arr) {
        let n = d3.select(arr[e.index]);

        if (n.attr("hazard") === "true")
            return;

        if (!n.attr("active") || n.attr("active") === "false") {
            n.attr("active", "true");
            n.style("stroke", "red");
        } else {
            n.attr("active", "false");
            n.style("stroke", e.group);
        }
    }

    static onNodeClick(e, _, arr) {
        if(e.defaultPrevented)
            return;

        let n = d3.select(arr[e.index]);

        if (n.attr("hazard") === "true")
            return;

        if (!n.attr("active") || n.attr("active") === "false") {
            n.attr("active", "true");
            n.style("fill", "red");
        } else {
            n.attr("active", "false");
            n.style("fill", e.group);
        }
    }

    static onContextMenu(e) {
        // Position
        let svg_pos       = Graph.SVG.node().getBoundingClientRect();
        let mouse_pos     = d3.mouse(this)

        // Transformation
        let transform     = d3.zoomTransform(Graph.Anchor.node());
        let zoom_factor   = transform.k;
        let scroll_offset = transform.invert(mouse_pos);

        // New coordinates
        let x             = mouse_pos[0] + (mouse_pos[0] - scroll_offset[0] + 20) * zoom_factor;
        let y             = mouse_pos[1] + (mouse_pos[1] - scroll_offset[1]) * zoom_factor;

        let context_menu = d3.select('#context-menu');
        context_menu
            .style('visibility', 'visible')
            .style('opacity', '1')
            .style('left', svg_pos.x + x + 'px')
            .style('top', svg_pos.y + y + 'px');

        context_menu.select('.header').text(e.label).style("font-weight", "bold");
        let body = context_menu.select('.body');
        body.html('');
        if (e.hazard) {
            body.append('div').html("<b>" + e.hazard.title + "</b> &rArr; " + e.hazard.content).style("color", "red");
        }

        d3.event.preventDefault();
    }

    static hideContextMenu() {
        d3.select('#context-menu')
          .style("visibility", "hidden")
          .style("opacity", "0");
    }

    /* Control Callbacks*/

    static stickyNodes(sticky) {
        Graph.set("sticky", sticky);
    }

    static showNodes(show) {
        Graph.Nodes.style('visibility', show ? 'visible' : 'hidden');
    }

    static showEdges(show) {
        Graph.Edges.style('visibility', show ? 'visible' : 'hidden');
    }

    static showNodeLabels(show) {
        Graph.NodeLabels.style('visibility', show ? 'visible' : 'hidden');
    }

    static showEdgeLabels(show) {
        Graph.EdgeLabels.style('visibility', show ? 'visible' : 'hidden');
    }

    static zoom(zoom_value) {
        Graph.GRAPH.zoom_level.scaleTo(Graph.SVG, Math.round(zoom_value * 10) / 10)
    }
}