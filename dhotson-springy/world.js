function Settler(settlement) {
	this.name = "jeff";
	this.home = settlement;
}

function Settlement(graph) {
	this.graph = graph;
	this.settlers = [];
	for (var i = 0; i < 10; i++) this.settlers.push(Settler(this));
	this.color = "#aaaaaa";
	this.size = function() {return this.settlers.length;};
	
	this.data = {color: this.color, size: this.size()};
	this.links = [];
	this.addLink = function(loc) {this.links.push(loc);};
	this.forestChance = Math.random();
	
	this.node = graph.newNode(this.data);
	
	// --------------------
	
	this.move = function() {
		console.log("moving...");
		if (!this.forest && Math.random() <= this.forestChance) {
			this.forest = new Forest(this.graph);
			graph.newEdge(this.node, this.forest.node);
			console.log("A settlement discovered a forest!");
		}
	};
}

function Forest(graph) {
	this.graph = graph;
	this.settlers = [];
	this.color = "#00ee44";
	this.size = function() {return this.settlers.length + 10;};
	this.data = {color: this.color, size: this.size()};
	this.node = graph.newNode(this.data);
}

function World(graph) {
	this.graph = graph;
	this.setts = [];
	this.addSettlement = function() {
		this.setts.push(new Settlement(this.graph));
		console.log(this.setts.length);
	};
	this.step = function(settsClone) {
		if (settsClone.length > 0) {
			var s = settsClone.pop();
			s.move();
			var t = this.start;
			window.setTimeout(function() {t(settsClone);}, 1000);
		} else {
			var settsClone = this.setts.slice(0);
			var t = this.start;
			window.setTimeout(function() {t(settsClone);}, 1000);
		}
	};
}

function start(world) {
	setts = world.setts.length;
	for (var i = 0; i < setts; i++) {
		window.setTimeout(function() {world.setts[i].move();}, 500*i);
	}
	
	window.setTimeout(function() {start(world);}, 500 * setts);
}
