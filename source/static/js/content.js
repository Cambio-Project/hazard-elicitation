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
            .html(close ? `<span onclick="Content.this.removeTab(${id})">✕ </span>${title}` : title)
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

    removeAllTabs() {
        for (const [id, _] of this.tabs._entries()) {
            this.removeTab(id);
        }
    }

    addHazard(id, type, data) {
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

        const tab_id = this.addTab({
            "title":   "{}: {}".format(type, element.label),
            "content": new Scenario(data).html(),
        }, "hazard", true);
        Graph.CONTEXT_MENU.hide();

        return tab_id;
    }

    addNewHazard(id, type, data) {
        const hazard_id                      = Math.max(Graph.this.graph.hazards._keys()) + 1;
        Graph.this.graph.hazards[hazard_id]  = {tab_id: this.addHazard(id, type, data)};
        Graph.getElement(type, id).hazard_id = hazard_id;
        this.openHazard(id, type);
    }

    openHazard(id, type) {
        const el = Graph.getElement(type, id);
        content.show(Graph.this.graph.hazards[el.hazard_id].tab_id);
    }

    static saveScenario(json) {
        const parsed_json = JSON.parse(JSON.stringify(json));
        const component = parsed_json["artifact"] === "Service" ? "node" : "edge";
        Content.this.addNewHazard(parsed_json["id"], component, parsed_json);
        Chat.this.ws.event("e-next-step");
    }
}

class Scenario {
    constructor(json) {
        console.debug(json);
        this.json = $.extend(true, {
            "description": "",
            "source": "",
            "artifact": "",
            "stimulus": "",
            "environment": "",
            "response": "",
            "response-measure": "",
        }, json);
    }

    export() {

    }

    card(title, body) {
        return "" +
        `<div class="scenario-section col-md-3">
          <div class="card">
            <div class="card-body">
              <h5 class="card-title">${title}</h5>
              <p class="card-text">${body}</p>
            </div>
          </div>
        </div>`;
    }

    html() {
        let html = "";
        const cards = ["Description", "Source", "Artifact", "Stimulus", "Environment", "Response", "Response Measure"];
        for(const card of cards) {
            html += this.card(card, this.json[card.toLowerCase().replaceAll(" ", "-")]);
        }
        return html;
    }
}
