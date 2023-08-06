(self["webpackChunkipyflex"] = self["webpackChunkipyflex"] || []).push([["lib_widget_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_con-d81bea"],{

/***/ "./lib/reactWidget.js":
/*!****************************!*\
  !*** ./lib/reactWidget.js ***!
  \****************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FlexWidget = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const FlexLayout = __importStar(__webpack_require__(/*! flexlayout-react */ "webpack/sharing/consume/default/flexlayout-react/flexlayout-react"));
__webpack_require__(/*! flexlayout-react/style/light.css */ "./node_modules/flexlayout-react/style/light.css");
const Button_1 = __importDefault(__webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/index.js"));
const Toolbar_1 = __importDefault(__webpack_require__(/*! @mui/material/Toolbar */ "./node_modules/@mui/material/Toolbar/index.js"));
const widgetWrapper_1 = __webpack_require__(/*! ./widgetWrapper */ "./lib/widgetWrapper.js");
const DEFAULT_MODEL = {
    global: {
        tabEnableRename: true,
    },
    layout: {
        type: 'row',
        id: '#1',
        children: [
            {
                type: 'tabset',
                id: '#2',
                children: [],
                active: true,
            },
        ],
    },
    borders: [],
};
const DEFAULT_OUTER_MODEL = {
    global: {
        tabEnableRename: true,
        tabSetTabLocation: 'bottom',
    },
    layout: {
        type: 'row',
        id: '#1',
        children: [
            {
                type: 'tabset',
                id: '#2',
                children: [
                    {
                        type: 'tab',
                        id: '#3',
                        name: 'New section ',
                        component: 'sub',
                        config: {
                            model: {
                                global: {},
                                layout: {
                                    type: 'row',
                                    id: '#1',
                                    children: [
                                        {
                                            type: 'tabset',
                                            id: '#3',
                                            children: [],
                                            active: true,
                                        },
                                    ],
                                },
                                borders: [],
                            },
                        },
                    },
                ],
                active: true,
            },
        ],
    },
    borders: [],
};
class FlexWidget extends react_1.Component {
    constructor(props) {
        super(props);
        this.layoutRef = react_1.default.createRef();
        this.factory = (node) => {
            const component = node.getComponent();
            // const config = node.getConfig();
            const nodeId = node.getId();
            // const name = node.getName();
            const nameList = Object.values(FlexWidget.COMPONENT_DICT);
            nameList.push('Section');
            // if (nameList.includes(name)) {
            //   try {
            //     node
            //       .getModel()
            //       .doAction(FlexLayout.Actions.renameTab(nodeId, `${name} ${nodeId}`));
            //   } catch (error) {
            //     console.log(error);
            //   }
            // }
            switch (component) {
                case 'grid': {
                    return react_1.default.createElement("div", null, "grid");
                }
                case 'controller': {
                    return react_1.default.createElement("div", null, "controller");
                }
                case '3Dview': {
                    return react_1.default.createElement("div", null, "3Dview");
                }
                case 'structureView': {
                    return react_1.default.createElement("div", null, "structureView");
                }
                case 'PBS': {
                    return react_1.default.createElement(widgetWrapper_1.WidgetWrapper, { model: this.model, widget_idx: 0 });
                }
                case 'connectionView': {
                    return react_1.default.createElement("div", null, "connectionView");
                }
                case 'infoView': {
                    return react_1.default.createElement("div", null, "infoView");
                }
                case 'dataView': {
                    return react_1.default.createElement("div", null, "dataView");
                }
                case 'widgetView': {
                    return react_1.default.createElement("div", null, "widgetView");
                }
                case 'documentView': {
                    return react_1.default.createElement("div", null, "documentView");
                }
                case 'sub': {
                    return this.generateSection(node, nodeId);
                }
            }
            return null;
        };
        this.generateSection = (node, nodeId) => {
            let model = node.getExtraData().model;
            let defaultModel;
            this.innerlayoutRef[nodeId] = react_1.default.createRef();
            if (node.getConfig() && node.getConfig().model) {
                defaultModel = node.getConfig().model;
            }
            else {
                defaultModel = DEFAULT_MODEL;
            }
            if (!model) {
                node.getExtraData().model = FlexLayout.Model.fromJson(defaultModel);
                model = node.getExtraData().model;
                // save sub-model on save event
                node.setEventListener('save', (p) => {
                    this.state.model.doAction(FlexLayout.Actions.updateNodeAttributes(nodeId, {
                        config: {
                            model: node.getExtraData().model.toJson(),
                        },
                    }));
                    //  node.getConfig().model = node.getExtraData().model.toJson();
                });
            }
            return (react_1.default.createElement(FlexLayout.Layout, { ref: this.innerlayoutRef[nodeId], classNameMapper: (className) => {
                    if (className === 'flexlayout__tabset-selected') {
                        className =
                            'inner__flexlayout__tabset-selected flexlayout__tabset-selected';
                    }
                    else if (className === 'flexlayout__tabset') {
                        className = 'inner__flexlayout__tabset flexlayout__tabset';
                    }
                    else if (className === 'flexlayout__tab') {
                        className = 'inner__flexlayout__tab flexlayout__tab';
                    }
                    return className;
                }, model: model, factory: this.factory, onRenderTabSet: (tabSetNode, renderValues) => {
                    this.onRenderTabSet(tabSetNode, renderValues, nodeId);
                }, onAction: (action) => this.innerOnAction(nodeId, action) }));
        };
        this.onAction = (action) => {
            if (action.type === 'FlexLayout_MoveNode' ||
                action.type === 'FlexLayout_AdjustSplit' ||
                action.type === 'FlexLayout_DeleteTab' ||
                action.type === 'FlexLayout_MaximizeToggle' ||
                action.type === 'FlexLayout_SelectTab') {
                window.dispatchEvent(new Event('resize'));
            }
            return action;
        };
        this.innerOnAction = (outerNodeID, action) => {
            if (action.type === 'FlexLayout_MoveNode' ||
                action.type === 'FlexLayout_AdjustSplit' ||
                action.type === 'FlexLayout_DeleteTab' ||
                action.type === 'FlexLayout_MaximizeToggle') {
                window.dispatchEvent(new Event('resize'));
            }
            return action;
        };
        this.onRenderTabSet = (tabSetNode, renderValues, nodeId) => {
            // const tabsetId = tabSetNode.getId();
            renderValues.buttons.push(react_1.default.createElement(Button_1.default, { onClick: () => {
                    const tabsetId = tabSetNode.getId();
                    this.innerlayoutRef[nodeId].current.addTabToTabSet(tabsetId, {
                        component: 'PBS',
                        name: FlexWidget.COMPONENT_DICT['PBS'],
                        config: { layoutID: nodeId },
                    });
                } },
                "Add widget",
                ' '));
        };
        this.onAddRow = () => {
            this.layoutRef.current.addTabToActiveTabSet({
                component: 'sub',
                name: 'New section',
            });
        };
        this.innerlayoutRef = {};
        this.state = {
            model: FlexLayout.Model.fromJson(DEFAULT_OUTER_MODEL),
        };
        this.model = props.model;
    }
    render() {
        return (react_1.default.createElement("div", { style: { height: '100%', border: 'solid 1px black' } },
            react_1.default.createElement("div", { style: {
                    width: '100%',
                    height: 'calc(100% - 36px)',
                } },
                react_1.default.createElement(FlexLayout.Layout, { ref: this.layoutRef, model: this.state.model, factory: this.factory, classNameMapper: (className) => {
                        if (className === 'flexlayout__layout') {
                            className =
                                'chartviewer__flexlayout__layout flexlayout__layout ';
                        }
                        else if (className === 'flexlayout__tabset-selected') {
                            className =
                                'outer__flexlayout__tabset-selected flexlayout__tabset-selected ';
                        }
                        return className;
                    }, onAction: this.onAction })),
            react_1.default.createElement(Toolbar_1.default, { variant: "dense" },
                react_1.default.createElement(Button_1.default, { onClick: this.onAddRow }, "Add section"))));
    }
}
exports.FlexWidget = FlexWidget;
FlexWidget.COMPONENT_DICT = {
    grid: 'Chart widget',
    dataView: 'Data widget',
    controller: 'Controller widget',
    '3Dview': '3D widget',
    structureView: 'Structure widget',
    infoView: 'System info widget',
    PBS: 'PBS widget',
    connectionView: 'Connection widget',
    documentView: 'Document widget',
    widgetView: 'Custom widget',
};
exports["default"] = FlexWidget;
//# sourceMappingURL=reactWidget.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Trung Le
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

// Copyright (c) Trung Le
// Distributed under the terms of the Modified BSD License.
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FlexLayoutView = exports.FlexLayoutModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
// import { UUID } from '@lumino/coreutils';
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const react_1 = __importDefault(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const reactWidget_1 = __importDefault(__webpack_require__(/*! ./reactWidget */ "./lib/reactWidget.js"));
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const messaging_1 = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging");
// Import the CSS
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class FlexLayoutModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: FlexLayoutModel.model_name, _model_module: FlexLayoutModel.model_module, _model_module_version: FlexLayoutModel.model_module_version, _view_name: FlexLayoutModel.view_name, _view_module: FlexLayoutModel.view_module, _view_module_version: FlexLayoutModel.view_module_version, children: [], value: 'Hello World' });
    }
    /**
     * Public constructor
     */
    initialize(attributes, options) {
        super.initialize(attributes, options);
        this.widget_manager.display_model(undefined, this, {});
    }
}
exports.FlexLayoutModel = FlexLayoutModel;
FlexLayoutModel.serializers = Object.assign(Object.assign({}, base_1.DOMWidgetModel.serializers), { children: { deserialize: base_1.unpack_models } });
FlexLayoutModel.model_name = 'FlexLayoutModel';
FlexLayoutModel.model_module = version_1.MODULE_NAME;
FlexLayoutModel.model_module_version = version_1.MODULE_VERSION;
FlexLayoutModel.view_name = 'FlexLayoutView'; // Set to null if no view
FlexLayoutModel.view_module = version_1.MODULE_NAME; // Set to null if no view
FlexLayoutModel.view_module_version = version_1.MODULE_VERSION;
class WidgetWrapper extends apputils_1.ReactWidget {
    constructor(send_msg, model) {
        super();
        this.onResize = (msg) => {
            window.dispatchEvent(new Event('resize'));
        };
        this._send_msg = send_msg;
        this._model = model;
    }
    render() {
        return react_1.default.createElement(reactWidget_1.default, { send_msg: this._send_msg, model: this._model });
    }
}
class FlexLayoutView extends base_1.DOMWidgetView {
    render() {
        super.render();
        this.el.classList.add('custom-widget');
        const widget = new WidgetWrapper(this.send.bind(this), this.model);
        messaging_1.MessageLoop.sendMessage(widget, widgets_1.Widget.Msg.BeforeAttach);
        this.el.insertBefore(widget.node, null);
        messaging_1.MessageLoop.sendMessage(widget, widgets_1.Widget.Msg.AfterAttach);
        // this.el.innerHTML = 'hello trung';
        // const children = this.model.get('children');
        // const manager = this.model.widget_manager;
        // // console.log('children', children);
        // // manager
        // //   .create_view(children[0], {})
        // //   .then((view) => this.el.appendChild(view.pWidget.node));
    }
}
exports.FlexLayoutView = FlexLayoutView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./lib/widgetWrapper.js":
/*!******************************!*\
  !*** ./lib/widgetWrapper.js ***!
  \******************************/
/***/ (function(__unused_webpack_module, exports, __webpack_require__) {

"use strict";

var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    Object.defineProperty(o, k2, { enumerable: true, get: function() { return m[k]; } });
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WidgetWrapper = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
class WidgetWrapper extends react_1.Component {
    constructor(props) {
        super(props);
        this.model = props.model;
        this.widget_idx = props.widget_idx;
        this.state = {
            state: 0,
        };
        this.myRef = react_1.default.createRef();
    }
    componentDidMount() {
        console.log('start did mount');
        const children = this.model.get('children');
        const manager = this.model.widget_manager;
        console.log('children', children);
        manager
            .create_view(children[0], {})
            .then((view) => this.myRef.current.appendChild(view.pWidget.node));
    }
    render() {
        return react_1.default.createElement("div", { ref: this.myRef });
    }
}
exports.WidgetWrapper = WidgetWrapper;
//# sourceMappingURL=widgetWrapper.js.map

/***/ }),

/***/ "./node_modules/css-loader/dist/cjs.js!./css/widget.css":
/*!**************************************************************!*\
  !*** ./node_modules/css-loader/dist/cjs.js!./css/widget.css ***!
  \**************************************************************/
/***/ (() => {

throw new Error("Module build failed (from ./node_modules/css-loader/dist/cjs.js):\nCssSyntaxError\n\n(3:11) Missed semicolon\n\n \u001b[90m 1 | \u001b[39m\u001b[33m.custom-widget\u001b[39m \u001b[33m{\u001b[39m\n \u001b[90m 2 | \u001b[39m  padding\u001b[33m:\u001b[39m 0px 2px\u001b[33m;\u001b[39m\n\u001b[31m\u001b[1m>\u001b[22m\u001b[39m\u001b[90m 3 | \u001b[39m  height\u001b[33m:\u001b[39m 500px\n \u001b[90m   | \u001b[39m          \u001b[31m\u001b[1m^\u001b[22m\u001b[39m\n \u001b[90m 4 | \u001b[39m  border\u001b[33m:\u001b[39m solid 0.5px gray\n \u001b[90m 5 | \u001b[39m\u001b[33m}\u001b[39m\n");

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
module.exports = JSON.parse('{"name":"ipyflex","version":"0.1.0","description":"Jupyter Widget Flex Layout","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//ipyflex","bugs":{"url":"https://github.com//ipyflex/issues"},"license":"BSD-3-Clause","author":{"name":"Trung Le","email":"leductrungxf@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//ipyflex"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyflex/labextension","clean:nbextension":"rimraf ipyflex/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.4.1","@emotion/styled":"^11.3.0","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@jupyter-widgets/controls":"^3.0.0","@jupyterlab/apputils":"^3.2.0","@mui/material":"^5.0.4","flexlayout-react":"^0.5.17"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","process":"^0.11.10","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^9.2.6","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyflex/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true},"react":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_con-d81bea.bc6d4e421e3ed5225260.js.map