class Content {
    static CONTENT = null;

    constructor(content_id) {
        Content.CONTENT = this;

        this.container  = $(content_id);
        this.tabbar     = this.container.find("#tablist");
        this.tabcontent = this.container.find("#tabcontent");

        this.TAB_ID = 0;
        this.tabs   = {};
    }

    static get this() {
        return Content.CONTENT;
    }

    show(tab_id) {
        if (tab_id in this.tabs) {
            $('a[href="#' + this.tabs[tab_id][1][0].id + '"]').tab("show");
        }
    }

    addTab(data, class_name = "", close = false) {
        const id      = this.TAB_ID;
        const tab_id  = "tab-" + id;
        const title   = data.title || "_";
        const content = data.content || "...";

        const header_content = $("<a></a>")
            .html(close ? `<span onclick="Content.this.removeTab(${id})">✕  </span>${title}` : title)
            .addClass("nav-link " + class_name)
            .attr({
                "role":        "tab",
                "data-toggle": "tab",
                "id":          `${tab_id}-title`,
                "href":        `#${tab_id}`
            });

        const header = $('<li></li>')
            .addClass("nav-item")
            .append(header_content);

        const body = $('<div></div>')
            .html(content)
            .addClass("tab-pane fade")
            .attr({
                "role": "tabpanel",
                "id":   tab_id
            });

        this.tabbar.append(header);
        this.tabcontent.append(body);
        this.tabs[this.TAB_ID] = [header, body];

        this.TAB_ID += 1;
        return id;
    }

    removeTab(tab_id) {
        if (tab_id in this.tabs) {
            this.tabs[tab_id].map(e => e.remove());
            $("#" + tab_id).tab('dispose');
        }
    }

    static addHazard(id, type) {
        let element;
        if (type === "node") {
            element = Graph.this.graph.nodes[id];
            type    = "Service";
            $(".nodes").find(`circle[id="n${id}"]`).addClass("hazard");
        } else {
            element = Graph.this.graph.edges[id];
            type    = "Operation";
            $(".edges").find(`path[id="e${id}"]`).addClass("hazard");
        }

        let properties = "";
        const addEntry = function (data, indent = 0) {
            for (const [key, val] of data._entries()) {
                if (!isObject(val)) {
                    const space = "&nbsp;".repeat(indent);
                    properties += `<tr><th>${space}${key}</th><td>${val}</td></tr>`;
                } else {
                    properties += `<tr><th>${key}</th><td></td></tr>`;
                    addEntry(val, indent + 2)
                }
            }
        }
        addEntry(element.data);

        const tab_id = Content.this.addTab({
            "title":   "{}: {}".format(type, element.label),
            "content": `
              <table>
                <tr><th>Label</th><td>${element.label}</td></tr>
                ${properties}
              </table>`,
        }, "hazard", true);
        Graph.CONTEXT_MENU.hide();

        return tab_id;
    }

    static addNewHazard(id, type) {
        const hazard_id                 = Math.max(Graph.this.graph.hazards._keys()) + 1;
        graph.hazards[hazard_id].tab_id = Content.addHazard(id, type);
    }

    static openHazard(id, type) {
        const G         = Graph.this.graph;
        const hazard_id = type === "node" ? G.nodes[id].hazard_id : G.edges[id].hazard_id;
        content.show(G.hazards[hazard_id].tab_id);
    }
}
