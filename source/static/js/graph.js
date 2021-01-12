class Graph {
    static GRAPH = null;

    constructor(svg, context_menu, graph) {
        Graph.GRAPH = this;

        this.properties = {
            sticky_nodes:    false,
            node_size:       5,
            edge_size:       2,
            edge_arrow_size: {w: 2, h: 6},
            colors:          d3.scaleOrdinal(d3.schemeCategory10)
        }

        this.context_menu = new ContextMenu(context_menu);

        this.svg = d3.select(svg);
        this.svg.on("click", function () { Graph.ContextMenu.hide() });

        this.anchor = this.svg.append("g");
        this.anchor.on("click", function () { Graph.ContextMenu.hide() });

        this.graph       = graph;
        this.graph_nodes = graph.nodes._values();
        this.graph_edges = graph.edges._values();
        const width      = this.svg.node().getBoundingClientRect().width;
        const height     = this.svg.node().getBoundingClientRect().height;

        this.createContainer();
        this.createEdges();
        this.createNodes();
        this.createLinkLabels();
        this.createNodeLabels();

        this.simulation = d3
            .forceSimulation(this.graph_nodes)
            .force("charge", d3.forceManyBody().strength(-10000))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("x", d3.forceX(width / 2).strength(0.1))
            .force("y", d3.forceY(height / 2).strength(0.1))
            .force("link", d3.forceLink(this.graph_edges).id(function (l) { return l.id; }).distance(25).strength(1))
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
                  Graph.ContextMenu.hide();
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

        Graph.zoom(1.5);
    }

    static get SVG() { return Graph.GRAPH.svg; }

    static get Anchor() { return Graph.GRAPH.anchor; }

    static get Simulation() { return Graph.GRAPH.simulation; }

    static get Graph() { return Graph.GRAPH.graph; }

    static get Nodes() { return Graph.GRAPH.nodes; }

    static get NodeLabels() { return Graph.GRAPH.node_labels; }

    static get Edges() { return Graph.GRAPH.edges; }

    static get EdgeLabels() { return Graph.GRAPH.edge_labels; }

    static get ContextMenu() { return Graph.GRAPH.context_menu; }

    static get(property) { return Graph.GRAPH.get(property); }

    static set(property, value) { Graph.GRAPH.set(property, value); }

    get(property) { return this.properties[property]; }

    set(property, value) { this.properties[property] = value; }

    /* Init Graph */

    createContainer() {
        const node_size  = this.get("node_size");
        const arrow_size = this.get("edge_arrow_size");
        this.anchor
            .append("svg:defs")
            .selectAll("marker")
            .data(["end"])
            .enter()
            .append("svg:marker")
            .attr("id", String)
            .attr("class", "arrowhead")
            .attr("viewBox", "0 -{} {} {}".format(arrow_size.w, arrow_size.h, arrow_size.w * 2))
            .attr("markerWidth", node_size)
            .attr("markerHeight", node_size)
            .attr("orient", "auto")
            .append("svg:path")
            .attr("d", "M 0,-{} L {},0 L 0,{}".format(arrow_size.w, arrow_size.h, arrow_size.w));
    }

    createEdges() {
        this.edges = this
            .anchor
            .append("g")
            .attr("class", "edges")
            .selectAll("line")
            .data(this.graph_edges)
            .enter()
            .append("path")
            .attr("marker-end", "url(#end)")
            .attr("d", "M 0 0 L 0 0")
            .on("contextmenu", Graph.onContextMenu)
            .on("click", Graph.onLinkClick);
    }

    createNodes() {
        this.nodes = this
            .anchor
            .append("g")
            .attr("class", "nodes")
            .selectAll("g")
            .data(this.graph_nodes)
            .enter()
            .append("circle")
            .attr("r", this.get("node_size"))
            .attr("id", function (n) { return n.id; })
            .attr("fill", function (n) { if (n.hazard) return "red"; else return Graph.get("colors")(n.group); })
            .on("contextmenu", Graph.onContextMenu)
            .on("click", Graph.onNodeClick);
    }

    createLinkLabels() {
        this.edge_labels = this
            .anchor
            .append("g")
            .attr("class", "edge-labels")
            .selectAll("g")
            .data(this.graph_edges)
            .enter()
            .append("text")
            .text(function (n) { return n.label; });
    }

    createNodeLabels() {
        this.node_labels = this
            .anchor
            .append("g")
            .attr("class", "node-labels")
            .selectAll("g")
            .data(this.graph_nodes)
            .enter()
            .append("text")
            .text(function (l) { return l.label; });
    }

    /* Callbacks */

    static onTick() {
        Graph.Edges.attr("d", function (l) {
            const node_size = Graph.get("node_size");
            const x1        = l.source.x,
                  y1        = l.source.y,
                  x2        = l.target.x,
                  y2        = l.target.y;

            if (l.source !== l.target) {
                const dx = x2 - x1,
                      dy = y2 - y1,
                      dr = Math.sqrt(dx * dx + dy * dy);

                return "M {} {} A {} {} 0 0 1 {} {}".format(x1, y1, dr, dr, x2, y2); // curved line
                // return "M {} {} L {} {}".format(x1, y1, x2, y2) // straight line
            }
            const scale = l.label.length * 3; // TODO size of the curve
            return "M {} {} C {} {} {} {} {} {}".format(x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, x2 + node_size / 2, y2 + node_size / 2);
        })

        Graph.Edges.attr("d", function (l) {
            const node_size  = Graph.get("node_size");
            const edge_size  = Graph.get("edge_size");
            const arrow_size = Graph.get("edge_arrow_size");

            const x1 = l.source.x,
                  y1 = l.source.y,
                  x2 = l.target.x,
                  y2 = l.target.y;

            const pl = this.getTotalLength(),
                  r  = node_size + arrow_size.h + edge_size * 2,
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
        Graph.ContextMenu.hide();
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
        if (e.defaultPrevented)
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
        let svg_pos   = Graph.SVG.node().getBoundingClientRect();
        let mouse_pos = d3.mouse(this)

        // Transformation
        let transform     = d3.zoomTransform(Graph.Anchor.node());
        let zoom_factor   = transform.k;
        let scroll_offset = transform.invert(mouse_pos);

        // New coordinates
        let x = mouse_pos[0] + (mouse_pos[0] - scroll_offset[0] + 20) * zoom_factor;
        let y = mouse_pos[1] + (mouse_pos[1] - scroll_offset[1]) * zoom_factor;

        Graph.ContextMenu.show(svg_pos.x + x, svg_pos.y + y, e);

        d3.event.preventDefault();
    }

    /* Control Callbacks*/

    static zoom(zoom_value) {
        Graph.GRAPH.zoom_level.scaleTo(Graph.SVG, Math.round(zoom_value * 10) / 10)
    }

    static stickyNodes(sticky) {
        Graph.set("sticky", sticky);
    }

    static showNodes(show) {
        Graph.Nodes.style("visibility", show ? "visible" : "hidden");
    }

    static showEdges(show) {
        Graph.Edges.style("visibility", show ? "visible" : "hidden");
    }

    static showNodeLabels(show) {
        Graph.NodeLabels.style("visibility", show ? "visible" : "hidden");
    }

    static showEdgeLabels(show) {
        Graph.EdgeLabels.style("visibility", show ? "visible" : "hidden");
    }

    static toggleSimulation() { }

    static pauseSimulation() { Graph.Simulation.alphaTarget(0); }

    static resumeSimulation() { Graph.Simulation.alphaTarget(0.5); }

    static restartSimulation() { Graph.Simulation.alphaTarget(0.1).restart(); }
}

class ContextMenu {
    constructor(context_menu) {
        this.context_menu = $(context_menu);
        this.body         = this.context_menu.find(".body");
        this.anchor       = this.body.find(".dropdown-menu");
    }

    createItems(data) {
        let content = "";
        for (const key in data) {
            if (typeof data[key] === "object") {
                let nested = data[key]._empty() ? "" : "<ul class='dropdown-menu'>" + this.createItems(data[key]) + "</ul>";
                content +=
                    `<li class="dropdown-submenu">
                        <a class="dropdown-item">${key}</a>
                        ${nested}      
                      </li>`;
            } else {
                content += `<li><a class="dropdown-item"><b>${key}</b>: ${data[key]}</a></li>`;
            }
        }
        return content
    }

    show(x, y, element) {
        this.context_menu
            .css({
                "visibility": "visible",
                "opacity":    "1",
                "left":       x + "px",
                "top":        y + "px"
            });

        const type = "source" in element ? "edge" : "node";

        this.anchor.html("");
        this.anchor.append(`<li><a class="dropdown-item"><b>${element.label}</b></a></li>`);
        this.anchor.append("<div class='dropdown-divider'></div>");
        this.anchor.append(
            `<li class="dropdown-action" name="hazard">
              <a class="dropdown-item" onclick="Content.addHazard('${element.id}', '${type}');">Mark as Hazard</a>
            </li>`);
        this.anchor.append("<div class='dropdown-divider'></div>");
        this.anchor.append(this.createItems(element.data));
    }

    hide() {
        this.context_menu
            .css({
                "visibility": "hidden",
                "opacity":    "0"
            });
    }
}
