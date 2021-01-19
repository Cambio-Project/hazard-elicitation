const HELP = `
<h3>Need help?</h3>

<p class="chapter">
  <a class="btn-link" data-toggle="collapse" href="#help-graph" role="button" aria-expanded="false">
    <i class="arrow"></i>Graph
  </a>
</p>
<div class="collapse m-md-2" id="help-graph">
  <p>Use <code>Right Click</code> on a node or edge to open a context menu and inspect an element.</p>
  <div class="tip-wrapper"><div class="tip tip-1"></div></div>
</div>

<p class="chapter">
  <a class="btn-link" data-toggle="collapse" href="#help-chat" role="button" aria-expanded="false">
    <i class="arrow"></i>Chat
  </a>
</p>
<div class="collapse m-md-2" id="help-chat">
  <p class="d-inline">
    The chat is connected to a chatbot. 
    Use the send button (<button type="button" class="position-relative send-button">&#10148;</button>) to send a message.
  </p>
</div>
`;

const SETTINGS = `
<p class="chapter">
  <a class="btn-link" data-toggle="collapse" href="#graph-config" role="button" aria-expanded="false">
    <i class="arrow"></i>Configure Graph
  </a>
</p>
<div class="collapse m-md-2" id="graph-config">
  <div class="d-inline-block m-md-2">
      <div class="d-inline-block m-md-2">
          <div class="m-md-2">
            <p class="tool-settings"><label for="zoom">Zoom</label></p>
            <input type="range" min="0.1" max="4" value="1" step="0.1" id="zoom" onchange="Graph.zoom(this.value);"/>
          </div>
        
          <div class="m-md-2">
              <p class="tool-settings"><label for="network-selection">Graph</label></p>
              <select class="form-control" id="network-selection">
                <option>Hotrod</option>
                <option>Books</option>
                <option>ABCDE</option>
              </select>
          </div>
      </div>
      
      <div class="d-inline-block m-md-2">
          <div class="m-md-2">
            <p class="tool-settings"><label for="stickynodes">Sticky nodes</label></p>
            <input type="checkbox" id="stickynodes" onchange="Graph.stickyNodes(this.checked);"/>
          </div>
          
          <div class="m-md-2">
            <p class="tool-settings"><label for="usetooltip">Tooltips</label></p>
            <input type="checkbox" id="usetooltip" onchange="Graph.useTooltip(this.checked);"/>
          </div>
      </div>
    
    <div class="d-inline-block m-md-2">
      <div class="m-md-2">
        <p class="tool-settings"><label for="shownode">Show nodes</label></p>
        <input type="checkbox" id="shownode" onchange="Graph.showNodes(this.checked);" checked/>
      </div>
      
      <div class="m-md-2">
        <p class="tool-settings"><label for="showlink">Show links</label></p>
        <input type="checkbox" id="showlink" onchange="Graph.showEdges(this.checked);" checked/>
      </div>
    </div>
    
    <div class="d-inline-block m-md-2">
      <div class="m-md-2">
        <p class="tool-settings"><label for="shownodelabel">Show node labels</label></p>
        <input type="checkbox" id="shownodelabel" onchange="Graph.showNodeLabels(this.checked);" checked/>
      </div>
      
      <div class="m-md-2">
        <p class="tool-settings"><label for="showlinklabel">Show link labels</label></p>
        <input type="checkbox" id="showlinklabel" onchange="Graph.showEdgeLabels(this.checked);"/>
      </div>
    </div>
  </div>
</div>
<p class="chapter">
  <a class="btn-link" data-toggle="collapse" href="#sim-config" role="button" aria-expanded="false">
    <i class="arrow"></i>Configure Simulation
  </a>
</p>
<div class="collapse m-md-2" id="sim-config">
      <div class="d-inline-block m-md-1">
        <button class="btn" type="button" onclick="Graph.pauseSimulation();">Play</button>
      </div>
      
      <div class="d-inline-block m-md-1">
        <button class="btn" type="button" onclick="Graph.pauseSimulation();">Pause</button>
      </div>

      <div class="d-inline-block m-md-1">
        <button class="btn" type="button" onclick="Graph.resumeSimulation();">Resume</button>
      </div>
</div>

<div class="m-md-2">
<p class="tool-settings"><label for="theme" class="switch">Dark Theme</label></p>
<input type="checkbox" id="theme" onchange="setDarkTheme(this.checked);">
</div>
`;
