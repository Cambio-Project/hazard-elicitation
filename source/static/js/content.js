class Content {
    static CONTENT = null;

    constructor(content_id) {
        Content.CONTENT = this;

        this.container  = $(content_id);
        this.tabbar     = this.container.find("#tablist");
        this.tabcontent = this.container.find("#tabcontent");

        this.TAB_ID = 0;
        this.tabs = {};
    }

    addTab(data) {
        const id      = "tab-" + this.TAB_ID;
        const title   = data.title || "_";
        const content = data.content || "...";

        const header = $('<li></li>')
            .addClass("nav-item")
            .append($('<a></a>')
                .text(title)
                .addClass("nav-link hazard")
                .attr({
                    "role":          "tab",
                    "data-toggle":   "tab",
                    "id":            `${id}-title`,
                    "href":          `#${id}`,
                    "aria-controls": id,
                    "aria-selected": "true",
                })
            );

        const body = $('<div></div>')
            .html(content)
            .addClass("tab-pane fade")
            .attr({
                "role":            "tabpanel",
                "id":              id,
                "aria-labelledby": `${id}-title`,
            });

        this.tabbar.append(header);
        this.tabcontent.append(body);
        this.tabs[this.TAB_ID] = [header, body];

        this.TAB_ID += 1;
    }

    removeTab(tab_id) {
        if(tab_id in this.tabs) {
            this.tabs[tab_id].map(e => e.remove());
        }
    }

    static addHazard(id, type) {
        let element;
        if(type === "node") {
            element = Graph.Graph.nodes[id];
            type = "Service";
        } else {
            element = Graph.Graph.edges[id];
            type = "Operation";
        }

        Content.CONTENT.addTab({
            "title": "{}: {}".format(type, element.label),
            "content": JSON.stringify(element),
        })
    }
}
