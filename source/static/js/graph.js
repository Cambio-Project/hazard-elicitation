class Graph {
    static GRAPH        = null;
    static CONTEXT_MENU = null;

    constructor(svg, context_menu, graph) {
        Graph.GRAPH        = this;
        Graph.CONTEXT_MENU = new ContextMenu(context_menu);

        this.properties = {
            sticky_nodes:      false,
            tooltip:           false,
            node_size:         5,
            edge_size:         2,
            node_label_offset: {x: 10, y: 0},
            edge_label_offset: {x: 10, y: 15},
            curved_edges:      true,
            edge_arrow_size:   {w: 2, h: 6},
            zoom_range:        {min: 0.4, max: 4},
            colors:            d3.scaleOrdinal(d3.schemeCategory10)
        }

        // HTML
        this.svg = d3.select(svg);
        this.svg.on("click", function () { Graph.ContextMenu.hide() });

        this.anchor = this.svg.append("g");
        this.anchor.on("click", function () { Graph.ContextMenu.hide() });

        this.graph       = graph;
        this.graph_nodes = graph.nodes._values();
        this.graph_edges = graph.edges._values();
        const width      = this.svg.node().getBoundingClientRect().width;
        const height     = this.svg.node().getBoundingClientRect().height;

        this.createAnchor();
        this.createEdges();
        this.createNodes();
        this.createEdgeLabels();
        this.createNodeLabels();

        // Simulation
        this.simulation = d3
            .forceSimulation(this.graph_nodes)
            .force("charge", d3.forceManyBody().strength(-10000))
            .force("center", d3.forceCenter(width / 2, height / 2))
            .force("x", d3.forceX(width / 2).strength(0.1))
            .force("y", d3.forceY(height / 2).strength(0.1))
            .force("link", d3.forceLink(this.graph_edges).id(function (e) { return e.id; }).distance(25).strength(1))
            .on("tick", Graph.onTick);

        // Events
        this.zoom_level = d3
            .zoom()
            .scaleExtent(this.get("zoom_range")._values())
            .on("zoom", Graph.onZoom);
        this.svg.call(this.zoom_level);

        this.nodes.call(
            d3.drag()
              .on("start", function (n) {
                  d3.event.sourceEvent.stopPropagation();
                  if (!d3.event.active)
                      Graph.this.simulation.alphaTarget(0.5).restart();
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
                          Graph.this.simulation.alphaTarget(0);
                      n.fx = null;
                      n.fy = null;
                  }
              })
        );

        // Hazards
        const na = $(".nodes");
        const ea = $(".edges");
        for (const hazard of graph.hazards._values()) {
            for (const nid of hazard.nodes) {
                na.find("[nid='{}']".format(nid)).attr("class", "hazard")
            }

            for (const eid of hazard.edges) {
                ea.find("[eid='{}']".format(eid)).attr("class", "hazard")
            }
        }
    }

    static get this() { return Graph.GRAPH; }

    static get ContextMenu() { return Graph.CONTEXT_MENU; }

    static get(property) { return Graph.this.get(property); }

    static set(property, value) { Graph.this.set(property, value); }

    get(property) { return this.properties[property]; }

    set(property, value) { this.properties[property] = value; }

    /* Init Graph */

    createAnchor() {
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
            .attr("eid", function (e) { return e.id; })
            .attr("marker-end", "url(#end)")
            .attr("d", "M 0 0 L 0 0")
            .on("contextmenu", Graph.onContextMenu)
            .on("click", Graph.onEdgeClick)
            .on("mouseover", Graph.onMouseover)
            .on("mousemove", Graph.onMousemove)
            .on("mouseout", Graph.onMouseout);
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
            .attr("nid", function (n) { return n.id; })
            .attr("r", this.get("node_size"))
            .attr("fill", function (n) { return Graph.get("colors")(n.group); })
            .on("contextmenu", Graph.onContextMenu)
            .on("click", Graph.onNodeClick)
            .on("mouseover", Graph.onMouseover)
            .on("mousemove", Graph.onMousemove)
            .on("mouseout", Graph.onMouseout);
    }

    createEdgeLabels() {
        this.edge_labels = this
            .anchor
            .append("g")
            .attr("class", "edge-labels")
            .selectAll("g")
            .data(this.graph_edges)
            .enter()
            .append("text")
            .text(function (e) { return e.label; });
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
            .text(function (n) { return n.label; });
    }

    static transformCoordinates(ctx, x_offset = 0, y_offset = 0) {
        // Position
        const svg_pos   = Graph.this.svg.node().getBoundingClientRect();
        const mouse_pos = d3.mouse(ctx);

        // Transformation
        const transform     = d3.zoomTransform(Graph.this.anchor.node());
        const zoom_factor   = transform.k;
        const scroll_offset = transform.invert(mouse_pos);

        // New coordinates
        const x = mouse_pos[0] + (mouse_pos[0] - scroll_offset[0] + x_offset / zoom_factor) * zoom_factor;
        const y = mouse_pos[1] + (mouse_pos[1] - scroll_offset[1] + y_offset / zoom_factor) * zoom_factor;
        return {"x": svg_pos.x + x, "y": svg_pos.y + y}
    }

    /*  */

    static selectElement(type, name) {
        const is_edge = type === "edge";
        const search  = is_edge ? Graph.this.graph.edges._values() : Graph.this.graph.nodes._values();
        let el        = search.find(e => e.label === name);

        if (el !== null) {
            if (!is_edge) {
                const nodes = $(".nodes");
                nodes.find('circle[active="true"]').attr("active", false);
                nodes.find(`circle[nid="${el.id}"]`).attr("active", true);
            } else {
                const edges = $(".edges");
                edges.find('path[active="true"]').attr("active", false);
                edges.find(`path[eid="${el.id}"]`).attr("active", true);
            }
        }
    }

    /* Callbacks */

    static onTick() {
        const r                 = Graph.get("node_size")
        const edge_size         = Graph.get("edge_size");
        const arrow_size        = Graph.get("edge_arrow_size");
        const curved_edges      = Graph.get("curved_edges");
        const node_label_offset = Graph.get("node_label_offset");
        const edge_label_offset = Graph.get("edge_label_offset");

        Graph.this.edges.attr("d", function (e) {
            const x1 = e.source.x,
                  y1 = e.source.y,
                  x2 = e.target.x,
                  y2 = e.target.y;

            if (e.source !== e.target) {
                // Normal edge

                if (curved_edges) {
                    const dx   = x2 - x1,
                          dy   = y2 - y1,
                          dist = Math.sqrt(dx * dx + dy * dy);
                    return "M {} {} A {} {} 0 0 1 {} {}".format(x1, y1, dist, dist, x2, y2);
                } else {
                    return "M {} {} L {} {}".format(x1, y1, x2, y2);
                }
            } else {
                // Self edge

                const scale = e.label.length * 3; // TODO size of the curve
                return "M {} {} C {} {} {} {} {} {}".format(
                    x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, x2 + r / 2, y2 + r / 2);
            }
        })

        Graph.this.edges.attr("d", function (e) {
            const x1 = e.source.x,
                  y1 = e.source.y;

            const point_len = this.getTotalLength(),
                  node_hull = r + arrow_size.h + edge_size * 2,
                  mid_point = this.getPointAtLength(point_len - node_hull);

            if (e.source !== e.target) {
                // Normal edge

                if (curved_edges) {
                    const dx   = mid_point.x - x1,
                          dy   = mid_point.y - y1,
                          dist = Math.sqrt(dx * dx + dy * dy);
                    return "M {} {} A {} {} 0 0 1 {} {}".format(x1, y1, dist, dist, mid_point.x, mid_point.y);
                } else {
                    return "M {} {} L {} {}".format(x1, y1, mid_point.x, mid_point.y);
                }
            } else {
                // Self edge

                const scale = e.label.length * 3; // TODO size of the curve
                return "M {} {} C {} {} {} {} {} {}".format(
                    x1, y1, x1 - scale, y1 - scale, x1 - scale, y1 + scale, mid_point.x, mid_point.y);
            }
        })

        Graph.this.nodes
             .attr("cx", function (n) { return n.x; })
             .attr("cy", function (n) { return n.y; });

        Graph.this.node_labels
             .attr("x", function (n) { return n.x + node_label_offset.x; })
             .attr("y", function (n) { return n.y + node_label_offset.y; });

        Graph.this.edge_labels
             .attr("x", function (e) { return e.source.x + (e.target.x - e.source.x) * 0.5 + edge_label_offset.x; })
             .attr("y", function (e) { return e.source.y + (e.target.y - e.source.y) * 0.5 + edge_label_offset.y; });
    }

    static onZoom() {
        if (d3.event.sourceEvent?.type === "wheel")
            Config.setElement("graph-zoom", d3.event.transform.k);

        Graph.this.anchor.attr("transform", d3.event.transform);
        Graph.ContextMenu.hide();
    }

    static zoom(val) { Graph.this.zoom_level.scaleTo(Graph.this.svg, val); }

    static onEdgeClick(e, _, arr) { }

    static onNodeClick(e, _, arr) { }

    static onContextMenu(e) {
        const coords = Graph.transformCoordinates(this, 20, 10)
        Graph.ContextMenu.show(coords.x, coords.y, e);

        d3.event.preventDefault();
    }

    static onMouseover(e) {
        if (e.hasOwnProperty("source")) {
            d3.select(this).attr("stroke-width", Graph.get("edge_size") + 1);
        } else {
            d3.select(this).attr("r", Graph.get("node_size") + 1);
        }
    }

    static onMousemove(e) {
        if (Graph.get("tooltip")) {
            const len    = e.label.length * 6 + 20;
            const coords = Graph.transformCoordinates(this, -len / 2, -50);
            d3.select("#tooltip")
              .text(e.label)
              .style("visibility", "visible")
              .style("opacity", "1")
              .style("left", coords.x + "px")
              .style("top", coords.y + "px");
        }
    }

    static onMouseout(e) {
        if (e.hasOwnProperty("source")) {
            d3.select(this).attr("stroke-width", Graph.get("edge_size"));
        } else {
            d3.select(this).attr("r", Graph.get("node_size"));
        }
        d3.select("#tooltip").style("visibility", "hidden").style("opacity", 0);
    }

    /* Control Callbacks*/

    static stopSimulation() { Graph.this.simulation.stop(); }

    static toggleSimulation() { }

    static pauseSimulation() { Graph.this.simulation.alphaTarget(0); }

    static resumeSimulation() { Graph.this.simulation.alphaTarget(0.5); }

    static restartSimulation() { Graph.this.simulation.alphaTarget(0.1).restart(); }
}

class ContextMenu {
    constructor(context_menu) {
        this.context_menu = $(context_menu);
        this.body         = this.context_menu.find(".body");
        this.anchor       = this.body.find(".dropdown-menu");
    }

    createItems(data) {
        let content = "";
        for (const [key, val] of Object.entries(data)) {
            if (isObject(val)) {
                let nested = val._empty() ? "" : "<ul class='dropdown-menu'>" + this.createItems(val) + "</ul>";
                content +=
                    `<li class="dropdown-submenu">
                        <a class="dropdown-item">${key}</a>
                        ${nested}      
                      </li>`;
            } else {
                content += `<li><a class="dropdown-item"><b>${key}</b>: ${val}</a></li>`;
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
        this.anchor.append('<div class="dropdown-divider"></div>');
        this.anchor.append(
            `<li class="dropdown-action" name="hazard">
              <a class="dropdown-item" onclick='Content.addHazard("${element.id}", "${type}");'>Mark as Hazard</a>
            </li>`);
        this.anchor.append('<div class="dropdown-divider"></div>');
        this.anchor.append(this.createItems(element.data));
    }

    hide() { this.context_menu.css({"visibility": "hidden", "opacity": "0"}); }
}
