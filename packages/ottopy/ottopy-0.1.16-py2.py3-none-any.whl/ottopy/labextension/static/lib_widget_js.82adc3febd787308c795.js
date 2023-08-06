(self["webpackChunkottopy"] = self["webpackChunkottopy"] || []).push([["lib_widget_js"],{

/***/ "./lib/models/robot_model.js":
/*!***********************************!*\
  !*** ./lib/models/robot_model.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.RobotModel = exports.orientation_hash = void 0;
const konva_1 = __importDefault(__webpack_require__(/*! konva */ "webpack/sharing/consume/default/konva/konva"));
const world_model_1 = __webpack_require__(/*! ./world_model */ "./lib/models/world_model.js");
const mod = (n, m) => {
    return ((n % m) + m) % m;
};
const _directions = [
    [1, -1],
    [1, 1],
    [-1, 1],
    [-1, -1],
];
// const rotationFix = [
//   [0, 0],
//   [0, -1],
//   [1, -1],
//   [1, 0],
// ];
exports.orientation_hash = {
    EAST: 0,
    NORTH: 1,
    WEST: 2,
    SOUTH: 3,
};
const robot_svg = `<svg xmlns="http://www.w3.org/2000/svg" version="1.1" class="svg-triangle" width='100' height='100' fill="#008080">
<path d="M 95,50 5,95 5,5 z"/>
</svg>`;
class RobotModel {
    constructor(index, world, x, y, orientation, image) {
        this.points = [];
        this.traceColor = 'red';
        this.speed = 1;
        this.move_to = (x, y) => {
            if (!this.node) {
                return Promise.resolve('bot is not created.');
            }
            return new Promise((resolve) => {
                let [cx, cy] = this.cr2xy(x, y);
                let tween = new konva_1.default.Tween({
                    node: this.node,
                    x: cx + world_model_1.IMAGE_PADDING + this.node.width() / 2,
                    y: cy + world_model_1.IMAGE_PADDING + this.node.height() / 2,
                    offsetX: this.node.width() / 2,
                    offsetY: this.node.height() / 2,
                    duration: this.speed,
                    onFinish: () => {
                        this.x = x;
                        this.y = y;
                        console.log('finished', x, y);
                        this.add_point(x, y);
                        resolve('done');
                    },
                });
                tween.play();
            });
        };
        this.rotate_node = (node, rotation) => {
            const degToRad = Math.PI / 180;
            const rotatePoint = ({ x, y }, deg) => {
                const rcos = Math.cos(deg * degToRad), rsin = Math.sin(deg * degToRad);
                return { x: x * rcos - y * rsin, y: y * rcos + x * rsin };
            };
            //current rotation origin (0, 0) relative to desired origin - center (node.width()/2, node.height()/2)
            const displayedWidth = node.width() * node.scaleX();
            const displayedHeight = node.height() * node.scaleY();
            const topLeft = { x: -displayedWidth / 2, y: -displayedHeight / 2 };
            const current = rotatePoint(topLeft, node.rotation());
            const rotated = rotatePoint(topLeft, rotation);
            const dx = rotated.x - current.x, dy = rotated.y - current.y;
            return {
                x: dx,
                y: dy,
                rotation,
            };
        };
        this.turn_left = () => {
            if (!this.node) {
                return Promise.resolve('bot is not created.');
            }
            return new Promise((resolve) => {
                this.orientation = mod(this.orientation + 1, 4);
                // let [cx, cy] = this.cr2xy(this.x, this.y);
                this.rotation_diff = this.rotate_node(this.node, mod(-90 * this.orientation, 360));
                let tween = new konva_1.default.Tween({
                    node: this.node,
                    rotation: this.rotation_diff.rotation,
                    duration: this.speed,
                    // x: this.node.x() + this.rotation_diff.x,
                    // y: this.node.y() + this.rotation_diff.y,
                    onFinish: () => {
                        this.add_point(this.x, this.y);
                        console.log('finished', this.x, this.y);
                        resolve('done');
                    },
                });
                tween.play();
            });
        };
        this.index = index;
        this.x = x;
        this.y = y;
        this.orientation = orientation;
        this.image = image;
        this.world = world;
        this.speed = 0.1;
        this.rotation_diff = { x: 0, y: 0 };
        this.bs = this.world.bs;
    }
    init_canvas() {
        this.canvas = this.world.ui.layers.main;
    }
    cr2xy(x, y) {
        let [cx, cy] = this.world.point2cxy(x, y + 1);
        return [cx, cy];
    }
    trace_point(x, y) {
        let [cx, cy] = this.cr2xy(x, y - 1);
        let direction_vector = _directions[this.orientation];
        let scale = this.world.bs * 0.1;
        let xx = cx + (this.world.bs / 2.0 + scale * direction_vector[0]);
        let yy = cy - (this.world.bs / 2.0 + scale * direction_vector[1]);
        return [xx, yy];
    }
    draw_trace() {
        let trace = new konva_1.default.Line({
            points: this.points.slice(Math.max(this.points.length - 4, 0)),
            stroke: this.traceColor,
            offsetX: -world_model_1.NUMBER_PADDING,
        });
        if (this.world &&
            this.world.ui &&
            this.world.ui.layers &&
            this.world.ui.layers.line) {
            this.world.ui.layers.line.add(trace);
            this.world.ui.layers.line.draw();
        }
    }
    add_point(x, y) {
        const [tx, ty] = this.trace_point(x, y);
        this.points = this.points.concat([tx, ty]);
        this.draw_trace();
    }
    set_trace(color) {
        this.traceColor = color;
        this.add_point(this.x, this.y);
    }
    set_speed(speed) {
        this.speed = speed;
    }
    clear_trace() {
        this.points = [];
        if (this.world &&
            this.world.ui &&
            this.world.ui.layers &&
            this.world.ui.layers.line) {
            this.world.ui.layers.line.destroyChildren();
            this.world.ui.layers.line.draw();
        }
    }
    draw() {
        let [cx, cy] = this.cr2xy(this.x, this.y);
        if (this.image) {
            konva_1.default.Image.fromURL(this.image, (node) => {
                this.rotation_diff = this.rotate_node(node, -(this.orientation * 90));
                node.setAttrs({
                    x: cx,
                    y: cy,
                    width: this.world.image_area,
                    height: this.world.image_area,
                    rotation: -(this.orientation * 90),
                });
                this.node = node;
                this.canvas.add(this.node);
                this.canvas.batchDraw();
            });
        }
        else {
            let svg64 = btoa(robot_svg);
            var b64Start = 'data:image/svg+xml;base64,';
            var image64 = b64Start + svg64;
            konva_1.default.Image.fromURL(image64, (node) => {
                node.setAttrs({
                    x: cx + world_model_1.IMAGE_PADDING,
                    y: cy + world_model_1.IMAGE_PADDING,
                    width: this.world.image_area,
                    height: this.world.image_area,
                    rotation: -(this.orientation * 90),
                });
                node.offsetX(node.width() / 2);
                node.offsetY(node.height() / 2);
                node.x(node.x() + node.width() / 2);
                node.y(node.y() + node.height() / 2);
                this.node = node;
                this.canvas.add(this.node);
                this.canvas.batchDraw();
            });
        }
    }
}
exports.RobotModel = RobotModel;
//# sourceMappingURL=robot_model.js.map

/***/ }),

/***/ "./lib/models/world_model.js":
/*!***********************************!*\
  !*** ./lib/models/world_model.js ***!
  \***********************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WorldModel = exports.IMAGE_PADDING = exports.NUMBER_PADDING = void 0;
const konva_1 = __importDefault(__webpack_require__(/*! konva */ "webpack/sharing/consume/default/konva/konva"));
const robot_model_1 = __webpack_require__(/*! ./robot_model */ "./lib/models/robot_model.js");
const jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"));
const isNumber_1 = __importDefault(__webpack_require__(/*! lodash/isNumber */ "./node_modules/lodash/isNumber.js"));
const random_1 = __importDefault(__webpack_require__(/*! lodash/random */ "./node_modules/lodash/random.js"));
const padStart_1 = __importDefault(__webpack_require__(/*! lodash/padStart */ "./node_modules/lodash/padStart.js"));
const draggable_1 = __importDefault(__webpack_require__(/*! ../utils/draggable */ "./lib/utils/draggable.js"));
const MIN_BOX_SIZE = 23;
const MAX_ROWS = 15;
const MAX_COLS = 15;
const LEFT_PADDING = 50;
exports.NUMBER_PADDING = 30;
exports.IMAGE_PADDING = 3;
const MARGIN_NUMBER_CIRCLE = 2;
const DEFAULT_HEIGHT = 500;
const MIN_HEIGHT = 450;
const MAX_BOX_SIZE = 50;
const walls_config = {
    normal: {
        stroke: 'darkred',
        strokeWidth: 5,
    },
    removable: {
        stroke: '#de1738',
        strokeWidth: 5,
    },
    goal: {
        stroke: 'darkred',
        strokeWidth: 7,
        dash: [5, 5],
    },
};
class WorldModel {
    constructor(zoom_level, onZoomChange) {
        this.onZoomChange = onZoomChange;
        this.zoom_level = zoom_level;
    }
    init(config, ui_id, rows, cols, vwalls = [], hwalls = [], robots = [], objects = {}, tileMap = {}, tiles = [], messages = {}, flags = {}, pending_goals = [], drop_goals = []) {
        this.robots = robots.map((robot, i) => new robot_model_1.RobotModel(i, this, robot.x, robot.y, robot.orientation, robot.image));
        this.draggable = false;
        this.rows = Math.min(MAX_ROWS, rows);
        this.cols = Math.min(MAX_COLS, cols);
        this.vwalls = vwalls;
        this.hwalls = hwalls;
        this.config = config;
        this.ui_id = ui_id;
        let screen_height = jquery_1.default(window).height() || DEFAULT_HEIGHT;
        let grid_height = Math.max(screen_height * 0.6, MIN_HEIGHT);
        this.bs = Math.ceil(Math.max(Math.min(grid_height / Math.max(this.rows, this.cols), MAX_BOX_SIZE), MIN_BOX_SIZE));
        this.image_area = this.bs - 2 * exports.IMAGE_PADDING;
        this.height = rows * this.bs;
        this.width = cols * this.bs;
        this.objects = objects;
        this.tileMap = tileMap;
        this.tiles = tiles;
        this.pending_goals = pending_goals;
        this.drop_goals = drop_goals;
        this.messages = messages;
        this.flags = flags;
        this.init_with_id(this.ui_id);
    }
    incrementZoom() {
        let classess = this.getZoomClasses();
        let classessToRemove = classess.join(' ');
        let nextClass = Math.max(...classess.map((x) => parseInt(x.split('-')[1])));
        if (nextClass < 10) {
            this.onZoomChange(nextClass / 10.0);
            jquery_1.default('.grid-slider', this.current_run)
                .removeClass(classessToRemove)
                .addClass(`zoom-${nextClass + 1}`);
        }
    }
    decrementZoom() {
        let classess = this.getZoomClasses();
        let classessToRemove = classess.join(' ');
        let nextClass = Math.min(...classess.map((x) => parseInt(x.split('-')[1])));
        this.onZoomChange(nextClass / 10.0);
        if (nextClass > 1) {
            jquery_1.default('.grid-slider', this.current_run)
                .removeClass(classessToRemove)
                .addClass(`zoom-${nextClass - 1}`);
        }
    }
    getZoomClasses() {
        var _a;
        let $outputArea = jquery_1.default('.grid-slider', this.current_run);
        let classess = ((_a = $outputArea.attr('class')) === null || _a === void 0 ? void 0 : _a.split(' ')) || ['zoom-10'];
        return classess.filter((x) => x.startsWith('zoom-'));
    }
    init_output_window() {
        let $outputArea = jquery_1.default('#outputArea');
        let $currentRun = this.current_run;
        $currentRun.append(this.skeleton());
        let that = this;
        //button actions
        jquery_1.default('.output-action-toggle', $currentRun).on('click', function () {
            console.log('clicked button');
            if (jquery_1.default(this).html() == 'ᐁ') {
                jquery_1.default(this).html('ᐅ');
            }
            else {
                jquery_1.default(this).html('ᐁ');
            }
            jquery_1.default('.grid-slider', $currentRun).slideToggle();
        });
        jquery_1.default('.output-action-zoom-in', $currentRun).on('click', function () {
            that.incrementZoom();
        });
        jquery_1.default('.output-action-zoom-out', $currentRun).on('click', function () {
            that.decrementZoom();
        });
        //Draggble $current_run
        if (this.config.floating && !this.draggable) {
            draggable_1.default($outputArea[0]);
            this.draggable = true;
        }
        if (!this.config.floating) {
            $outputArea[0].onmousedown = null;
        }
    }
    init_with_id(ui_id) {
        let $outputArea = jquery_1.default('#outputArea');
        this.current_run = jquery_1.default(`#${this.ui_id}`, $outputArea);
        //clean up
        jquery_1.default('.run_output', $outputArea).not(this.current_run).remove();
        if (this.current_run.length === 0) {
            console.log('in the run');
            this.current_run = jquery_1.default(`<div id=${this.ui_id} class='run_output'> </div>`);
            $outputArea.append(this.current_run);
            this.init_output_window();
            this.draw_canvas();
        }
    }
    skeleton() {
        return `
      <div class="output-header clr-info">
        <div class="output-header-msg"></div>
        <div class="output-actions btn-group">
          <button class="output-action-zoom-in">&plus;</button>
          <button class="output-action-zoom-out">&minus;</button>
          <button class="output-action-toggle">ᐁ</button>
        </div>
      </div>   
      <div class="grid-slider zoom-${this.zoom_level * 10}">
        <div class="grid">
          <div class="stats">
            <div class="stats-item">
              <div class="stats-title">Taken Moves</div>
              <div class="no_of_steps stats-value">0</div> 
            </div>
            <div class="stats-item">
              <div class="stats-title">current load</div>
              <div class="current_load stats-value">0</div> 
            </div>
            <div class="stats-item">
              <div class="stats-title">capacity</div>
              <div class="capacity stats-value">Unlimited</div> 
            </div>
          </div>
          <div class="konva-body">
            <div class="konva-grid"></div>
          </div>
        </div>
      </div>
    `;
    }
    draw_canvas() {
        try {
            let stage = new konva_1.default.Stage({
                container: '.konva-grid',
                width: this.width + exports.NUMBER_PADDING,
                height: this.height + exports.NUMBER_PADDING,
            });
            this.ui = {
                stage: stage,
                layers: {
                    bg: new konva_1.default.Layer(),
                    main: new konva_1.default.Layer({ offsetX: -1 * exports.NUMBER_PADDING }),
                    line: new konva_1.default.Layer(),
                },
            };
            this.robots[0].init_canvas();
            this.robots[0].draw();
            stage.add(this.ui.layers.bg);
            stage.add(this.ui.layers.main);
            stage.add(this.ui.layers.line);
            this.draw_border();
            this.draw_grid();
            this.draw_objects();
            this.draw_stats();
            this.draw_envelops();
            this.draw_flags();
            this.draw_drop_goals(this.drop_goals);
            return this.ui.layers.main.draw();
        }
        catch (error) {
            console.log('🚀 ~ file: world_model.ts ~ line 238 ~ WorldModel ~ draw_canvas ~ error', error);
            return Promise.resolve(error);
        }
    }
    draw_stats() {
        let vals = [
            this.stats.total_moves,
            this.stats.current_load,
            this.stats.max_capacity || 'Unlimited',
        ];
        //@ts-ignore
        jquery_1.default('.stats-value').text(function (i) {
            return vals[i];
        });
    }
    alert(msg, type = 'info', waitFor = 3000) {
        const classToRemove = ['info', 'success', 'danger']
            .filter((x) => x !== type)
            .map((x) => `clr-${x}`)
            .join(' ');
        jquery_1.default('.output-header', this.current_run)
            .removeClass(classToRemove)
            .addClass(`clr-${type}`);
        return jquery_1.default('.output-header-msg', this.current_run)
            .text(msg)
            .css({ opacity: 1 })
            .animate({
            width: 'show',
            duration: waitFor,
        });
    }
    success_msg(msg) {
        let arr = [];
        return this.alert(arr.concat(msg).join(','), 'success');
    }
    draw_objects() {
        for (const key in this.objects) {
            const [x, y] = key.split(',').map((zz) => parseInt(zz));
            this.draw_object(x, y, this.objects[key]);
        }
    }
    draw_flags() {
        for (const key in this.flags) {
            const [x, y] = key.split(',').map((zz) => parseInt(zz));
            this.draw_flag(x, y);
        }
    }
    draw_flag(x, y) {
        this.draw_custom('racing_flag_small', x, y, 0);
    }
    draw_object(x, y, obj) {
        for (const obj_name in obj) {
            let val = this.parse_value(obj[obj_name]);
            if (obj_name === 'beeper') {
                this.draw_beeper(x, y, val);
            }
            else {
                this.draw_custom(obj_name, x, y, val);
            }
        }
    }
    draw_envelops() {
        for (const key in this.messages) {
            const [x, y] = key.split(',').map((zz) => parseInt(zz));
            this.draw_envelop(x, y, this.messages[key]);
        }
    }
    draw_envelop(x, y, message) {
        this.draw_custom('envelope', x, y);
    }
    update_object(x, y, val) {
        let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
        if (text) {
            //@ts-ignore
            text.text(`${val}`);
            this.ui.layers.main.draw();
        }
    }
    draw_beeper(x, y, val) {
        let radius = (0.6 * this.bs) / 2;
        let [cx, cy] = this.point2cxy(x, y);
        cx = cx + this.bs / 2;
        cy = cy - this.bs / 2;
        let fontSize = Math.ceil((this.bs * 18) / 50);
        let circle = new konva_1.default.Circle({
            radius: radius,
            x: cx,
            y: cy,
            fill: 'yellow',
            stroke: 'orange',
            strokeWidth: 5,
            name: `obj-${x}-${y}-circle`,
        });
        let num = new konva_1.default.Text({
            text: `${val}`,
            x: cx - circle.radius() / 2,
            y: cy - circle.radius() / 2,
            fontSize: fontSize,
            name: `obj-${x}-${y}-text`,
        });
        this.ui.layers.main.add(circle, num);
    }
    remove_object(x, y) {
        if (!this.ui) {
            return;
        }
        let circle = this.ui.layers.main.find(`.obj-${x}-${y}-circle`)[0];
        let text = this.ui.layers.main.find(`.obj-${x}-${y}-text`)[0];
        let img = this.ui.layers.main.find(`.obj-${x}-${y}-img`)[0];
        if (circle) {
            //@ts-ignore
            circle.destroy();
        }
        if (text) {
            //@ts-ignore
            text.destroy();
        }
        if (img) {
            //@ts-ignore
            img.destroy();
        }
        this.ui.layers.main.draw();
    }
    //not touched yet to fix
    draw_sprite(sprite_name, x, y, frameRate = 1) {
        let spritePath = this.tileMap[sprite_name];
        let [cx, cy] = this.point2cxy(x, y);
        let sprite = new Image();
        sprite.src = spritePath;
        const animations = {
            motion: [0, 0, 40, 40, 40, 0, 40, 40],
        };
        let that = this;
        sprite.onload = function () {
            let imageSprite = new konva_1.default.Sprite({
                x: cx + LEFT_PADDING,
                y: cy - that.bs / 2,
                name: `sprite-${x}-${y}-img`,
                image: sprite,
                animation: 'motion',
                animations: animations,
                frameRate: frameRate,
            });
            that.ui.layers.main.add(imageSprite);
            that.ui.layers.main.batchDraw();
            imageSprite.start();
        };
    }
    draw_custom(obj_name, x, y, val = null, isGoal = false) {
        let imagePath = this.tileMap[obj_name];
        let [cx, cy] = this.point2cxy(x, y + 1);
        let radius = (0.4 * this.bs) / 2;
        let group = new konva_1.default.Group({
            x: cx + (this.bs - radius) - MARGIN_NUMBER_CIRCLE,
            y: cy + (this.bs - radius) - MARGIN_NUMBER_CIRCLE,
        });
        if (!isGoal && !!val) {
            let circle = new konva_1.default.Circle({
                radius: radius,
                fill: 'white',
                stroke: '#aaa',
                opacity: 0.9,
            });
            let TEXT_MARGIN = val > 9 ? MARGIN_NUMBER_CIRCLE : 2 * MARGIN_NUMBER_CIRCLE;
            let fontSize = Math.ceil((this.bs * 14) / 50); // when bs = 50 fontSize=14
            let num = new konva_1.default.Text({
                text: `${val}`,
                fontSize: fontSize,
                name: `obj-${x}-${y}-text`,
                offsetX: circle.x() + radius - TEXT_MARGIN,
                offsetY: circle.y() + radius - TEXT_MARGIN,
            });
            group.add(circle, num);
        }
        konva_1.default.Image.fromURL(imagePath, (node) => {
            node.setAttrs({
                x: cx + exports.IMAGE_PADDING,
                y: cy + exports.IMAGE_PADDING,
                width: this.image_area,
                height: this.image_area,
                name: `obj-${x}-${y}-img`,
            });
            if (isGoal) {
                node.cache();
                node.filters([konva_1.default.Filters.Grayscale]);
                this.ui.layers.main.add(node);
            }
            else {
                this.ui.layers.main.add(node);
                this.ui.layers.main.add(group);
            }
            this.ui.layers.main.batchDraw();
        });
    }
    draw_drop_goals(goals = []) {
        goals.map((goal) => {
            //@ts-ignore
            this.draw_custom(goal.obj_name, goal.x, goal.y, goal.val, true);
        });
    }
    update_stats(stats = {}) {
        this.stats = stats;
        this.draw_stats();
    }
    parse_value(val) {
        if (!val)
            return 0;
        if (isNumber_1.default(val))
            return val;
        else {
            const [min_val, max_val] = val.split('-').map((zz) => parseInt(zz));
            return random_1.default(min_val, max_val);
        }
    }
    draw_border() {
        let box = new konva_1.default.Rect({
            stroke: this.config.border_color,
            strokeWidth: 5,
            closed: true,
            width: this.width,
            height: this.height,
        });
        console.log('🚀 ~ file: world_model.ts ~ line 585 ~ WorldModel ~ draw_border ~ this.height', this.height);
        this.ui.layers.main.add(box);
    }
    draw_grid() {
        this.draw_cols();
        this.draw_rows();
        this.draw_walls();
        this.draw_tiles();
    }
    _draw_tile(x, y, tile) {
        let [cx, cy] = this.point2cxy(x, y + 1);
        let imagePath = this.tileMap[tile];
        konva_1.default.Image.fromURL(imagePath, (node) => {
            node.setAttrs({
                x: cx + exports.NUMBER_PADDING,
                y: cy,
                width: this.bs,
                height: this.bs,
                name: `obj-${x}-${y}-tilebg`,
            });
            this.ui.layers.bg.add(node);
            this.ui.layers.bg.batchDraw();
        });
    }
    draw_tiles() {
        this.tiles.forEach((list, row) => {
            list.forEach((tile, col) => {
                if (!!tile) {
                    this._draw_tile(row + 1, col + 1, tile);
                }
            });
        });
    }
    draw_cols() {
        const BOX_TO_NUM_PADDING = 10;
        for (let col = 1; col < this.cols; col++) {
            let line = new konva_1.default.Line({
                stroke: this.config.grid_line_color,
                points: [col * this.bs, 2.5, col * this.bs, this.height - 2.5],
            });
            let count = new konva_1.default.Text({
                text: `${col}`,
                y: this.height + BOX_TO_NUM_PADDING,
                x: (col - 1) * this.bs + this.bs / 4,
            });
            this.ui.layers.main.add(line, count);
        }
        let last_count = new konva_1.default.Text({
            text: `${this.cols}`,
            y: this.height + BOX_TO_NUM_PADDING,
            x: (this.cols - 1) * this.bs + this.bs / 4,
        });
        this.ui.layers.main.add(last_count);
    }
    draw_rows() {
        for (let row = 1; row < this.rows; row++) {
            let line = new konva_1.default.Line({
                stroke: this.config.grid_line_color,
                points: [this.width - 2.5, row * this.bs, 2.5, row * this.bs],
            });
            let count = new konva_1.default.Text({
                text: `${this.rows + 1 - row}`,
                y: row * this.bs,
                offsetY: this.bs * 0.75,
                offsetX: 20,
            });
            this.ui.layers.main.add(line, count);
        }
        let last_count = new konva_1.default.Text({
            text: `1`,
            y: this.rows * this.bs,
            offsetY: this.bs * 0.75,
            offsetX: 20,
        });
        this.ui.layers.main.add(last_count);
    }
    point2cxy(x, y) {
        return [(x - 1) * this.bs, this.height - (y - 1) * this.bs];
    }
    draw_wall(x, y, dir, wall_type = 'normal') {
        let config = walls_config[wall_type];
        let border = null;
        let [cx, cy] = this.point2cxy(x, y);
        if (dir === 'east') {
            border = new konva_1.default.Line(Object.assign(Object.assign({}, config), { name: `vwall-${x}-${y}`, points: [cx + this.bs, cy - this.bs, cx + this.bs, cy] }));
        }
        if (dir === 'north') {
            border = new konva_1.default.Line(Object.assign(Object.assign({ name: `hwall-${x}-${y}` }, config), { points: [cx, cy - this.bs, cx + this.bs, cy - this.bs] }));
        }
        if (border)
            this.ui.layers.main.add(border);
    }
    read_message(msg, waitFor = 3) {
        return this.alert(`🤖: ${msg}`, 'info', waitFor * 1000);
    }
    remove_wall(x, y, dir) {
        if (dir !== 'north' && dir !== 'east')
            return;
        let wall = this.ui.layers.main.find(`.${dir === 'north' ? 'hwall' : 'vwall'}-${x}-${y}`)[0];
        if (wall) {
            wall.destroy();
        }
        this.ui.layers.main.draw();
    }
    draw_typed_wall(x, y, dir, val) {
        let [isGoal, isRemovable, isWall] = padStart_1.default(Number(val).toString(2), 3, '0');
        if (parseInt(isWall)) {
            if (parseInt(isRemovable)) {
                this.draw_wall(x, y, dir, 'removable');
            }
            else {
                this.draw_wall(x, y, dir, 'normal');
            }
        }
        else if (parseInt(isGoal)) {
            this.draw_wall(x, y, dir, 'goal');
        }
    }
    draw_walls() {
        this.hwalls.forEach((hw, i) => {
            hw.forEach((val, j) => {
                if (val) {
                    this.draw_typed_wall(i, j, 'north', val);
                }
                else {
                    this.remove_wall(i, j, 'north');
                }
            });
        });
        this.vwalls.forEach((vw, i) => {
            vw.forEach((val, j) => {
                if (val) {
                    this.draw_typed_wall(i, j, 'east', val);
                }
                else {
                    this.remove_wall(i, j, 'east');
                }
            });
        });
    }
}
exports.WorldModel = WorldModel;
//# sourceMappingURL=world_model.js.map

/***/ }),

/***/ "./lib/utils/draggable.js":
/*!********************************!*\
  !*** ./lib/utils/draggable.js ***!
  \********************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
function dragElement(elmnt) {
    if (!document)
        return;
    var pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;
    /* otherwise, move the DIV from anywhere inside the DIV:*/
    elmnt.onmousedown = dragMouseDown;
    function dragMouseDown(e) {
        e = e || window.event;
        e.preventDefault();
        // get the mouse cursor position at startup:
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        // call a function whenever the cursor moves:
        document.onmousemove = elementDrag;
    }
    function elementDrag(e) {
        e = e || window.event;
        e.preventDefault();
        // calculate the new cursor position:
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // set the element's new position:
        elmnt.style.position = 'absolute';
        elmnt.style.top = elmnt.offsetTop - pos2 + 'px';
        elmnt.style.left = elmnt.offsetLeft - pos1 + 'px';
        elmnt.style.bottom = "unset";
        elmnt.style.right = "unset";
    }
    function closeDragElement() {
        /* stop moving when mouse button is released:*/
        document.onmouseup = null;
        document.onmousemove = null;
    }
}
exports["default"] = dragElement;
//# sourceMappingURL=draggable.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Indresh Vishwakarma
// Distributed under the terms of the Modified BSD License.
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MODULE_NAME = exports.MODULE_VERSION = void 0;
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore
// eslint-disable-next-line @typescript-eslint/no-var-requires
const data = __webpack_require__(/*! ../package.json */ "./package.json");
/**
 * The _model_module_version/_view_module_version this package implements.
 *
 * The html widget manager assumes that this is the same as the npm package
 * version number.
 */
exports.MODULE_VERSION = data.version;
/*
 * The current package name.
 */
exports.MODULE_NAME = data.name;
//# sourceMappingURL=version.js.map

/***/ }),

/***/ "./lib/widget.js":
/*!***********************!*\
  !*** ./lib/widget.js ***!
  \***********************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

// Copyright (c) Indresh Vishwakarma
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.MazeView = exports.MazeModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
const world_model_1 = __webpack_require__(/*! ./models/world_model */ "./lib/models/world_model.js");
const jquery_1 = __importDefault(__webpack_require__(/*! jquery */ "./node_modules/jquery/dist/jquery.js"));
const p_queue_1 = __importDefault(__webpack_require__(/*! p-queue */ "webpack/sharing/consume/default/p-queue/p-queue"));
const queue = new p_queue_1.default({ concurrency: 1 });
//Allowed method without valid maze
const ALLOWED_METHOD = ['halt', 'draw_all'];
class MazeModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: MazeModel.model_name, _model_module: MazeModel.model_module, _model_module_version: MazeModel.model_module_version, _view_name: MazeModel.view_name, _view_module: MazeModel.view_module, _view_module_version: MazeModel.view_module_version, current_call: '{}', method_return: '{}', zoom: 1, floating: false, is_inited: false });
    }
}
exports.MazeModel = MazeModel;
MazeModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
MazeModel.model_name = 'MazeModel';
MazeModel.model_module = version_1.MODULE_NAME;
MazeModel.model_module_version = version_1.MODULE_VERSION;
MazeModel.view_name = 'MazeView'; // Set to null if no view
MazeModel.view_module = version_1.MODULE_NAME; // Set to null if no view
MazeModel.view_module_version = version_1.MODULE_VERSION;
class MazeView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.method_changed = () => {
            let current_call = JSON.parse(this.model.get('current_call'));
            console.log(`#${current_call.ui_id} need to call current_method: ${current_call.method_name}`);
            if (!current_call.method_name) {
                console.log('clearing queue');
                queue.clear();
            }
            this.report_stats(current_call.stats);
            if (current_call.method_name === 'halt') {
                return this.halt();
            }
            else {
                queue.add(() => {
                    return new Promise((resolve) => {
                        let ret = typeof this[current_call.method_name] ===
                            'function'
                            ? this[current_call.method_name].apply(this, current_call.params)
                            : null;
                        if (!ALLOWED_METHOD.some((e) => e === current_call.method_name) &&
                            !jquery_1.default(`#${current_call.ui_id}`).length) {
                            console.log('maze is not loaded or invalid id: ', current_call.ui_id, current_call.method_name, current_call.method_name in ALLOWED_METHOD);
                            return resolve(null);
                        }
                        console.log('current_call in promise -> new code', current_call);
                        let that = this;
                        Promise.resolve(ret)
                            .then(function (x) {
                            // console.log("reached in promise");
                            let data = JSON.stringify({
                                value: x,
                                cb: +new Date(),
                                params: current_call.params,
                                method: current_call.method_name,
                            });
                            console.log('setting return', data);
                            that.model.set('method_return', data);
                            that.model.save_changes();
                            return data;
                        })
                            .then(resolve)
                            .catch((err) => {
                            console.log('error =>', current_call.method_name, 'execution failed', err);
                        });
                    });
                });
            }
        };
        this.draw_all = (world_config, ui_id, rows, cols, vwalls, hwalls, robots = [], objects = {}, tileMap = {}, tiles = [], messages = {}, flags = {}, pending_goals = [], drop_goals = []) => {
            this.world_model.init(world_config, ui_id, rows, cols, vwalls, hwalls, robots, objects, tileMap, tiles, messages, flags, pending_goals, drop_goals);
            return this.sleepUntil(() => {
                return (this.world_model &&
                    this.world_model.robots &&
                    this.world_model.robots[0] &&
                    this.world_model.robots[0].node);
            }, 3000);
        };
        this.sleepUntil = (f, timeoutMs) => {
            return new Promise((resolve, reject) => {
                let timeWas = new Date();
                let wait = setInterval(function () {
                    if (f()) {
                        clearInterval(wait);
                        resolve('robo init done');
                    }
                    else if (new Date().getTime() - timeWas.getTime() > timeoutMs) {
                        // Timeout
                        clearInterval(wait);
                        reject('error in robo init');
                    }
                }, 20);
            });
        };
        this.halt = () => {
            console.log('halting and clearing queue');
            return queue.clear();
        };
        this.move_to = (index, x, y) => {
            var _a;
            return this.world_model && ((_a = this.world_model.robots[index]) === null || _a === void 0 ? void 0 : _a.move_to(x, y));
        };
        this.report_stats = (stats) => {
            return (this.world_model &&
                this.world_model.update_stats &&
                this.world_model.update_stats(stats));
        };
        this.turn_left = (index) => {
            var _a;
            return (this.world_model &&
                this.world_model.robots &&
                this.world_model.robots.length > 0 && ((_a = this.world_model.robots[index]) === null || _a === void 0 ? void 0 : _a.turn_left()));
        };
        this.set_trace = (index, color) => {
            var _a;
            return (this.world_model &&
                this.world_model.robots &&
                this.world_model.robots.length > 0 && ((_a = this.world_model.robots[index]) === null || _a === void 0 ? void 0 : _a.set_trace(color)));
        };
        this.set_speed = (index, speed) => {
            var _a;
            return (this.world_model &&
                this.world_model.robots &&
                this.world_model.robots.length > 0 && ((_a = this.world_model.robots[index]) === null || _a === void 0 ? void 0 : _a.set_speed(speed)));
        };
        this.add_wall = (x, y, dir) => {
            return this.world_model.draw_wall(x, y, dir);
        };
        this.add_object = (x, y, obj_name, val) => {
            return this.world_model.draw_object(x, y, { [obj_name]: val });
        };
        this.add_goal_object = (x, y, obj_name, val) => {
            return this.world_model.draw_custom(obj_name, x, y, val, true);
        };
        this.update_object = (x, y, val) => {
            return this.world_model.update_object(x, y, val);
        };
        this.remove_object = (x, y) => {
            return this.world_model.remove_object(x, y);
        };
        this.remove_flag = (x, y) => {
            return this.world_model.remove_object(x, y);
        };
        this.remove_wall = (x, y, dir) => {
            return this.world_model.remove_wall(x, y, dir);
        };
        this.set_succes_msg = (msg) => {
            return this.world_model && this.world_model.success_msg(msg);
        };
        this.error = (msg) => {
            let arr = [];
            return (this.world_model &&
                this.world_model.alert(arr.concat(msg).join(', '), 'danger'));
        };
        this.show_message = (msg, waitFor = 1, img = 'envelope') => {
            return this.world_model.read_message(msg, waitFor);
        };
    }
    handle_zoom_level(zoom_level) {
        this.model.set('zoom', zoom_level);
        this.model.save_changes();
    }
    setInited() {
        console.log('widget inited set');
        this.model.set('is_inited', true);
        this.model.save_changes();
    }
    render() {
        this.method_changed();
        this.listenTo(this.model, 'change:current_call', this.method_changed);
        if (!this.world_model) {
            this.world_model = new world_model_1.WorldModel(this.model.get('zoom') || 1, this.handle_zoom_level.bind(this));
        }
        this.initOutput();
        //set methods
        if (!this.model.get('is_inited')) {
            this.setInited();
        }
    }
    initOutput() {
        if (jquery_1.default('#outputArea').length === 0) {
            const $parent = this.model.get('floating') || false ? jquery_1.default('body') : jquery_1.default(this.el);
            let $outputArea = jquery_1.default(`<div id="outputArea" class="${this.model.get('floating') ? 'floating' : 'non-floating'}" />`);
            $parent.append($outputArea);
        }
    }
}
exports.MazeView = MazeView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, "#outputArea .container {\n  position: relative;\n  min-width: 700px;\n  border-left: 1px solid #aaa;\n  border-top: 1px solid #aaa;\n  z-index: 105;\n  min-height: 300px;\n  font-family: 'Roboto', sans-serif;\n}\n\n#outputArea.floating {\n  position: absolute;\n  cursor: move;\n  bottom: 0;\n  right: 0;\n}\n\n#outputArea .zoom-1 {\n  zoom: 0.1;\n}\n#outputArea .zoom-2 {\n  zoom: 0.2;\n}\n#outputArea .zoom-3 {\n  zoom: 0.3;\n}\n#outputArea .zoom-4 {\n  zoom: 0.4;\n}\n#outputArea .zoom-5 {\n  zoom: 0.5;\n}\n#outputArea .zoom-6 {\n  zoom: 0.6;\n}\n#outputArea .zoom-7 {\n  zoom: 0.7;\n}\n#outputArea .zoom-8 {\n  zoom: 0.8;\n}\n#outputArea .zoom-9 {\n  zoom: 0.9;\n}\n#outputArea .zoom-10 {\n  zoom: 1;\n}\n#outputArea .output-header {\n  background-color: #aaa;\n  height: 40px;\n  display: flex;\n  align-items: center;\n  padding-right: 5px;\n  border: 2px solid;\n  border-top-right-radius: 5px;\n  border-top-left-radius: 5px;\n}\n#outputArea .output-header-msg {\n  display: flex;\n  width: 70%;\n  margin: 5px;\n  padding-left: 20px;\n}\n#outputArea .btn-group:after {\n  content: '';\n  clear: both;\n  display: table;\n}\n#outputArea .btn-group button {\n  justify-self: flex-end;\n  border: 1px solid #fff;\n  height: 25px;\n  max-width: 25px;\n  font-size: 1.25em;\n  font-weight: bold;\n  background-color: #fff;\n  color: #888;\n  text-align: center;\n  cursor: pointer;\n  border-radius: 50%;\n}\n#outputArea .btn-group button:not(:last-child) {\n  border-right: none;\n  /* Prevent double borders */\n  margin-right: 5px;\n}\n#outputArea .btn-group button:hover {\n  background-color: #f2f2f2;\n}\n#outputArea .output-actions {\n  display: flex;\n  flex: 1;\n  width: 30%;\n  min-width: 200px;\n  justify-content: flex-end;\n}\n#outputArea .grid-slider {\n  display: block;\n  background-color: #fff;\n}\n#outputArea .hide {\n  display: none;\n}\n#outputArea .show {\n  display: inherit;\n}\n#outputArea .grid {\n  display: flex;\n  justify-content: space-between;\n  border: 1px solid #aaa;\n  height: 100%;\n  min-height: 300px;\n}\n#outputArea .stats {\n  float: left;\n  width: 200px;\n  background-color: #f2f2f2;\n  box-shadow: 5px 0 5px -5px #888;\n  padding: 20px;\n  padding-top: 40px;\n  display: flex;\n  flex-direction: column;\n}\n#outputArea .konva-grid {\n  margin: 10px 0px;\n  padding-right: 20px;\n}\n#outputArea .stats-item {\n  float: left;\n  height: 75px;\n}\n#outputArea .stats-title {\n  text-transform: uppercase;\n  margin-bottom: 4px;\n  font-size: 14px;\n  color: #000 73;\n}\n#outputArea .stats-value {\n  color: #828282;\n  font-size: 24px;\n}\n#outputArea .konva-body {\n  flex: 1;\n}\n#outputArea .alert {\n  margin-top: 0.4rem;\n  margin-left: 0.4rem;\n  position: relative;\n  padding: 0.75rem 1.25rem;\n  border: 1px solid transparent;\n  border-radius: 0.25rem;\n  width: 50%;\n  white-space: nowrap;\n  overflow: hidden;\n  text-overflow: ellipsis;\n  min-height: 20px;\n}\n#outputArea .clr-success {\n  color: #155724;\n  border-color: #155724;\n  background-color: #d4edda;\n}\n#outputArea .clr-info {\n  color: #818182;\n  border-color: #aaa;\n  background-color: #d6d8db;\n}\n#outputArea .clr-danger {\n  color: #721c24;\n  background-color: #f8d7da;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./css/widget.css":
/*!************************!*\
  !*** ./css/widget.css ***!
  \************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

var api = __webpack_require__(/*! !../node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js */ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js");
            var content = __webpack_require__(/*! !!../node_modules/css-loader/dist/cjs.js!./widget.css */ "./node_modules/css-loader/dist/cjs.js!./css/widget.css");

            content = content.__esModule ? content.default : content;

            if (typeof content === 'string') {
              content = [[module.id, content, '']];
            }

var options = {};

options.insert = "head";
options.singleton = false;

var update = api(content, options);



module.exports = content.locals || {};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"ottopy","version":"0.1.15","description":"A configurable maze library","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/totogoto/ottopy","bugs":{"url":"https://github.com/totogoto/ottopy/issues"},"license":"BSD-3-Clause","author":{"name":"Indresh Vishwakarma","email":"indresh@varsito.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/totogoto/ottopy"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ottopy/labextension","clean:nbextension":"rimraf ottopy/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","konva":"^8.2.3","lodash":"^4.17.21","p-queue":"^7.1.0"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ottopy/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.82adc3febd787308c795.js.map