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

    show(tab_id) {
        if (tab_id in this.tabs) {
            $('a[href="#' + this.tabs[tab_id][1][0].id + '"]').tab('show');
        }
    }

    addTab(data, class_name = "") {
        const id      = this.TAB_ID;
        const tab_id  = "tab-" + id;
        const title   = data.title || "_";
        const content = data.content || "...";

        const header = $('<li></li>')
            .addClass("nav-item")
            .append($('<a></a>')
                .text(title)
                .addClass("nav-link " + class_name)
                .attr({
                    "role":        "tab",
                    "data-toggle": "tab",
                    "id":          `${tab_id}-title`,
                    "href":        `#${tab_id}`
                })
            );

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
        }
    }

    static addHazard(id, type) {
        let element;
        if (type === "node") {
            element = Graph.Graph.nodes[id];
            type    = "Service";
        } else {
            element = Graph.Graph.edges[id];
            type    = "Operation";
        }

        let properties = "";
        const addEntry = function (data, indent=0) {
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

        Content.CONTENT.addTab({
            "title":   "{}: {}".format(type, element.label),
            "content": `
              <table>
                <tr><th>Label</th><td>${element.label}</td></tr>
                ${properties}
              </table>`,
        }, "hazard")
    }
}
