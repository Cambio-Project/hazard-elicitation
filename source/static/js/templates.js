const HELP = `
<h3>Need help?</h3>
<br><br>
    
<h4>Graph</h4>
<p>Use <code>Right Click</code> on a node or edge to open a context menu and inspect an element.</p>
<div class="tip-wrapper"><div class="tip tip-1"></div></div>
<br><br>
    
<h4>Chat</h4>
<p class="d-inline">
    The chat is connected to a chatbot. 
    Use the send button (<div class="tip-wrapper-sm"><div class="tip tip-2"></div></div>) to send a message.
</p>
<div class="tip-wrapper"><div class="tip tip-1"></div></div>`;

const SETTINGS = `
<div class="col">
    <div class="m-md-2">
      <p class="tool-settings"><label for="network-selection">Graph</label></p>
      <select class="form-control btn btn-primary" data-style="btn-new" id="network-selection">
        <option>Hotrod</option>
        <option>Books</option>
        <option>ABCDE</option>
      </select>
    </div>

  <div class="m-md-2">
    <p class="tool-settings"><label for="stickynodes">Sticky nodes</label></p>
    <input type="checkbox" id="stickynodes" onchange="Graph.stickyNodes(this.checked);"/>
  </div>

  <div class="m-md-2">
    <p class="tool-settings"><label for="shownode">Show nodes</label></p>
    <input type="checkbox" id="shownode" onchange="Graph.showNodes(this.checked);" checked/>
  </div>

  <div class="m-md-2">
    <p class="tool-settings"><label for="showlink">Show links</label></p>
    <input type="checkbox" id="showlink" onchange="Graph.showEdges(this.checked);" checked/>
  </div>

  <div class="m-md-2">
    <p class="tool-settings"><label for="shownodelabel">Show node labels</label></p>
    <input type="checkbox" id="shownodelabel" onchange="Graph.showNodeLabels(this.checked);" checked/>
  </div>

  <div class="m-md-2">
    <p class="tool-settings"><label for="showlinklabel">Show link labels</label></p>
    <input type="checkbox" id="showlinklabel" onchange="Graph.showEdgeLabels(this.checked);"/>
  </div>
  
  <div class="m-md-2">
    <p class="tool-settings"><label for="usetooltip">Tooltips</label></p>
    <input type="checkbox" id="usetooltip" onchange="Graph.useTooltip(this.checked);"/>
  </div>
  
  <div class="d-inline-block m-md-2">
    <p class="tool-settings"><label for="zoom">Zoom</label></p>
    <input type="range" min="0.1" max="4" value="1" step="0.1" id="zoom" onchange="zoom(this.value);"/>
  </div>
  
  <div class="row">
      <div class="d-inline-block m-md-1">
        <button class="form-control btn btn-primary" type="button" onclick="Graph.pauseSimulation();">Play</button>
      </div>
      
      <div class="d-inline-block m-md-1">
        <button class="form-control btn btn-primary" type="button" onclick="Graph.pauseSimulation();">Pause</button>
      </div>

      <div class="d-inline-block m-md-1">
        <button class="form-control btn btn-primary" type="button" onclick="Graph.resumeSimulation();">Resume</button>
      </div>
  </div>
  
  <div class="m-md-2">
    <p class="tool-settings"><label for="theme" class="switch">Dark Theme</label></p>
    <input class="toggle" type="checkbox" id="theme" onchange="setDarkTheme(this.checked);">
  </div>
</div>`;
