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
const widgetWrapper_1 = __webpack_require__(/*! ./widgetWrapper */ "./lib/widgetWrapper.js");
const widgetMenu_1 = __webpack_require__(/*! ./widgetMenu */ "./lib/widgetMenu.js");
const styles_1 = __webpack_require__(/*! @mui/material/styles */ "./node_modules/@mui/material/styles/index.js");
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
            const tabsetId = tabSetNode.getId();
            renderValues.buttons.push(
            // <Button
            //   onClick={() => {
            //     const tabsetId = tabSetNode.getId();
            //     this.innerlayoutRef[nodeId].current.addTabToTabSet(tabsetId, {
            //       component: 'PBS',
            //       name: FlexWidget.COMPONENT_DICT['PBS'],
            //       config: { layoutID: nodeId },
            //     });
            //   }}
            // >
            //   Add widget{' '}
            // </Button>
            react_1.default.createElement(widgetMenu_1.WidgetMenu, { widgetList: this.widgetList, nodeId: nodeId, tabsetId: tabsetId, addTabToTabset: (name, nodeId, tabsetId) => {
                    console.log('called', name, nodeId, tabsetId);
                } }));
        };
        this.onAddRow = () => {
            this.layoutRef.current.addTabToActiveTabSet({
                component: 'sub',
                name: 'New section',
            });
        };
        this.onRenderOuterTabSet = (tabSetNode, renderValues) => {
            renderValues.buttons.push(react_1.default.createElement(Button_1.default, { size: "small", variant: "outlined", onClick: this.onAddRow, style: { height: '27px', minWidth: '40px' } },
                react_1.default.createElement("i", { className: "fas fa-plus" })));
        };
        this.innerlayoutRef = {};
        this.state = {
            model: FlexLayout.Model.fromJson(DEFAULT_OUTER_MODEL),
        };
        this.model = props.model;
        this.widgetList = Object.keys(this.model.get('children'));
    }
    render() {
        return (react_1.default.createElement(styles_1.StyledEngineProvider, { injectFirst: true },
            react_1.default.createElement("div", { style: { height: '100%' } },
                react_1.default.createElement("div", { style: {
                        width: '100%',
                        height: 'calc(100%)',
                    } },
                    react_1.default.createElement(FlexLayout.Layout, { ref: this.layoutRef, model: this.state.model, factory: this.factory, classNameMapper: (className) => {
                            if (className === 'flexlayout__layout') {
                                className = 'ipyflex flexlayout__layout';
                            }
                            else if (className === 'flexlayout__tabset-selected') {
                                className =
                                    'outer__flexlayout__tabset-selected flexlayout__tabset-selected ';
                            }
                            return className;
                        }, onAction: this.onAction, onRenderTabSet: (tabSetNode, renderValues) => {
                            this.onRenderOuterTabSet(tabSetNode, renderValues);
                        } })))));
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
    }
}
exports.FlexLayoutView = FlexLayoutView;
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./lib/widgetMenu.js":
/*!***************************!*\
  !*** ./lib/widgetMenu.js ***!
  \***************************/
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
exports.WidgetMenu = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const Button_1 = __importDefault(__webpack_require__(/*! @mui/material/Button */ "./node_modules/@mui/material/Button/index.js"));
const Menu_1 = __importDefault(__webpack_require__(/*! @mui/material/Menu */ "./node_modules/@mui/material/Menu/index.js"));
const MenuItem_1 = __importDefault(__webpack_require__(/*! @mui/material/MenuItem */ "./node_modules/@mui/material/MenuItem/index.js"));
class WidgetMenu extends react_1.Component {
    constructor(props) {
        super(props);
        this.handleClick = (event) => {
            const target = event.currentTarget;
            this.setState((oldState) => (Object.assign(Object.assign({}, oldState), { anchorEl: target })));
        };
        this.handleClose = () => {
            this.setState((oldState) => (Object.assign(Object.assign({}, oldState), { anchorEl: null })));
        };
        this.menuItem = props.widgetList.map((name) => (react_1.default.createElement(MenuItem_1.default, { key: `${name}}@${props.tabsetId}@${props.nodeId}`, onClick: () => {
                props.addTabToTabset(name, props.nodeId, props.tabsetId);
                this.handleClose();
            } }, name)));
        this.state = {
            anchorEl: null,
        };
    }
    render() {
        const menuId = `add_widget_menu_${this.props.tabsetId}@${this.props.nodeId}`;
        return (react_1.default.createElement("div", { key: menuId },
            react_1.default.createElement(Button_1.default, { "aria-controls": "simple-menu", "aria-haspopup": "true", onClick: this.handleClick }, "Add widget"),
            react_1.default.createElement(Menu_1.default, { id: "simple-menu", anchorEl: this.state.anchorEl, keepMounted: true, open: Boolean(this.state.anchorEl), onClose: this.handleClose }, this.menuItem)));
    }
}
exports.WidgetMenu = WidgetMenu;
//# sourceMappingURL=widgetMenu.js.map

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
        const children = this.model.get('children');
        const manager = this.model.widget_manager;
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
/***/ ((module, exports, __webpack_require__) => {

// Imports
var ___CSS_LOADER_API_IMPORT___ = __webpack_require__(/*! ../node_modules/css-loader/dist/runtime/api.js */ "./node_modules/css-loader/dist/runtime/api.js");
exports = ___CSS_LOADER_API_IMPORT___(false);
// Module
exports.push([module.id, ".custom-widget {\n  padding: 0px 2px;\n  height: 500px;\n  border: solid 0.5px #ddd9d9\n}\n.custom-widget>.p-Widget {\n  height: 100%;\n}\n\n.flexlayout__layout {\n  left: unset!important;\n  top: unset!important;\n  right: unset!important;\n  bottom: unset!important;\n  position: unset!important;\n  overflow: unset!important;\n  height: 100%;\n}\n\n/* .custom-widget .panel {\n  height:100%;\n  display:flex;\n  justify-content:center;\n  align-items:center;\n  background-color:white;\n  border:1px solid #555;\n  box-sizing: border-box;\n} */\n/* \n\n.flexlayout__layout {\n  height: 100%;\n}\n.flexlayout__splitter {\n  background-color: #f7f7f7;\n}\n@media (hover: hover) {\n  .flexlayout__splitter:hover {\n    background-color: #e2e2e2;\n  }\n}\n.flexlayout__splitter_border {\n  z-index: 10;\n}\n.flexlayout__splitter_drag {\n  z-index: 1000;\n  background-color: #e2e2e2;\n}\n.flexlayout__splitter_extra {\n  background-color: transparent;\n}\n.flexlayout__outline_rect {\n  position: absolute;\n  pointer-events: none;\n  box-sizing: border-box;\n  border: 2px solid red;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.2);\n  border-radius: 5px;\n  z-index: 1000;\n}\n.flexlayout__outline_rect_edge {\n  pointer-events: none;\n  border: 2px solid green;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.2);\n  border-radius: 5px;\n  z-index: 1000;\n  box-sizing: border-box;\n}\n.flexlayout__edge_rect {\n  position: absolute;\n  z-index: 1000;\n  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);\n  background-color: gray;\n  pointer-events: none;\n}\n.flexlayout__drag_rect {\n  position: absolute;\n  cursor: move;\n  color: black;\n  background-color: #f7f7f7;\n  border: 2px solid #e2e2e2;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.3);\n  border-radius: 5px;\n  z-index: 1000;\n  box-sizing: border-box;\n  opacity: 0.9;\n  text-align: center;\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n  overflow: hidden;\n  padding: 10px;\n  word-wrap: break-word;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__tabset {\n  overflow: hidden;\n  background-color: #f7f7f7;\n  box-sizing: border-box;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n  background-color: white;\n}\n.flexlayout__tabset_header {\n  position: absolute;\n  display: flex;\n  align-items: center;\n  left: 0;\n  right: 0;\n  padding: 3px 3px 3px 5px;\n  box-sizing: border-box;\n  border-bottom: 1px solid #e9e9e9;\n  color: black;\n  background-color: white;\n}\n.flexlayout__tabset_header_content {\n  flex-grow: 1;\n}\n.flexlayout__tabset_tabbar_outer {\n  box-sizing: border-box;\n  background-color: #f7f7f7;\n  position: absolute;\n  left: 0;\n  right: 0;\n  overflow: hidden;\n  display: flex;\n  background-color: white;\n}\n.flexlayout__tabset_tabbar_outer_top {\n  border-bottom: 1px solid #e9e9e9;\n}\n.flexlayout__tabset_tabbar_outer_bottom {\n  border-top: 1px solid #e9e9e9;\n}\n.flexlayout__tabset_tabbar_inner {\n  position: relative;\n  box-sizing: border-box;\n  display: flex;\n  flex-grow: 1;\n  overflow: hidden;\n}\n.flexlayout__tabset_tabbar_inner_tab_container {\n  display: flex;\n  box-sizing: border-box;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  width: 10000px;\n}\n.flexlayout__tabset_tabbar_inner_tab_container_top {\n  border-top: 2px solid transparent;\n}\n.flexlayout__tabset_tabbar_inner_tab_container_bottom {\n  border-bottom: 2px solid transparent;\n}\n.flexlayout__tabset-selected {\n  background-color: #f7f7f7;\n}\n.flexlayout__tabset-maximized {\n  background-color: #d4d4d4;\n}\n.flexlayout__tab {\n  overflow: auto;\n  position: absolute;\n  box-sizing: border-box;\n  color: black;\n  background-color: white;\n}\n.flexlayout__tab_button {\n  display: inline-flex;\n  align-items: center;\n  box-sizing: border-box;\n  padding: 3px 8px;\n  margin: 0px 2px;\n  cursor: pointer;\n}\n.flexlayout__tab_button--selected {\n  background-color: #e9e9e9;\n  color: black;\n}\n@media (hover: hover) {\n  .flexlayout__tab_button:hover {\n    background-color: #e9e9e9;\n    color: black;\n  }\n}\n.flexlayout__tab_button--unselected {\n  color: gray;\n}\n.flexlayout__tab_button_leading {\n  display: inline-block;\n}\n.flexlayout__tab_button_content {\n  display: inline-block;\n}\n.flexlayout__tab_button_textbox {\n  border: none;\n  color: green;\n  background-color: #e9e9e9;\n}\n.flexlayout__tab_button_textbox:focus {\n  outline: none;\n}\n.flexlayout__tab_button_trailing {\n  display: inline-block;\n  margin-left: 8px;\n  min-width: 8px;\n  min-height: 8px;\n}\n@media (pointer: coarse) {\n  .flexlayout__tab_button_trailing {\n    min-width: 20px;\n    min-height: 20px;\n  }\n}\n@media (hover: hover) {\n  .flexlayout__tab_button:hover .flexlayout__tab_button_trailing {\n    background: transparent url(\"../images/close.png\") no-repeat center;\n  }\n}\n.flexlayout__tab_button--selected .flexlayout__tab_button_trailing {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__tab_button_overflow {\n  margin-left: 10px;\n  padding-left: 12px;\n  border: none;\n  color: gray;\n  font-size: inherit;\n  background: transparent url(\"../images/more2.png\") no-repeat left;\n}\n.flexlayout__tab_toolbar {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tab_toolbar_button {\n  min-width: 20px;\n  min-height: 20px;\n  border: none;\n  outline: none;\n}\n.flexlayout__tab_toolbar_button-min {\n  background: transparent url(\"../images/maximize.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-max {\n  background: transparent url(\"../images/restore.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-float {\n  background: transparent url(\"../images/popout.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-close {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_sticky_buttons_container {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tab_floating {\n  overflow: auto;\n  position: absolute;\n  box-sizing: border-box;\n  color: black;\n  background-color: white;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n.flexlayout__tab_floating_inner {\n  overflow: auto;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n}\n.flexlayout__tab_floating_inner div {\n  margin-bottom: 5px;\n  text-align: center;\n}\n.flexlayout__tab_floating_inner div a {\n  color: royalblue;\n}\n.flexlayout__border {\n  box-sizing: border-box;\n  overflow: hidden;\n  display: flex;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n  background-color: white;\n}\n.flexlayout__border_top {\n  border-bottom: 1px solid #e9e9e9;\n  align-items: center;\n}\n.flexlayout__border_bottom {\n  border-top: 1px solid #e9e9e9;\n  align-items: center;\n}\n.flexlayout__border_left {\n  border-right: 1px solid #e9e9e9;\n  align-content: center;\n  flex-direction: column;\n}\n.flexlayout__border_right {\n  border-left: 1px solid #e9e9e9;\n  align-content: center;\n  flex-direction: column;\n}\n.flexlayout__border_inner {\n  position: relative;\n  box-sizing: border-box;\n  display: flex;\n  overflow: hidden;\n  flex-grow: 1;\n}\n.flexlayout__border_inner_tab_container {\n  white-space: nowrap;\n  display: flex;\n  box-sizing: border-box;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  width: 10000px;\n}\n.flexlayout__border_inner_tab_container_right {\n  transform-origin: top left;\n  transform: rotate(90deg);\n}\n.flexlayout__border_inner_tab_container_left {\n  flex-direction: row-reverse;\n  transform-origin: top right;\n  transform: rotate(-90deg);\n}\n.flexlayout__border_button {\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n  padding: 3px 8px;\n  margin: 2px;\n  box-sizing: border-box;\n  white-space: nowrap;\n  background-color: #f0f0f0;\n}\n.flexlayout__border_button--selected {\n  background-color: #e9e9e9;\n  color: black;\n}\n@media (hover: hover) {\n  .flexlayout__border_button:hover {\n    background-color: #e9e9e9;\n    color: black;\n  }\n}\n.flexlayout__border_button--unselected {\n  color: gray;\n}\n.flexlayout__border_button_leading {\n  display: inline;\n}\n.flexlayout__border_button_content {\n  display: inline-block;\n}\n.flexlayout__border_button_trailing {\n  display: inline-block;\n  margin-left: 8px;\n  min-width: 8px;\n  min-height: 8px;\n}\n@media (pointer: coarse) {\n  .flexlayout__border_button_trailing {\n    min-width: 20px;\n    min-height: 20px;\n  }\n}\n@media (hover: hover) {\n  .flexlayout__border_button:hover .flexlayout__border_button_trailing {\n    background: transparent url(\"../images/close.png\") no-repeat center;\n  }\n}\n.flexlayout__border_button--selected .flexlayout__border_button_trailing {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__border_toolbar {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__border_toolbar_left {\n  flex-direction: column;\n}\n.flexlayout__border_toolbar_right {\n  flex-direction: column;\n}\n.flexlayout__border_toolbar_button {\n  min-width: 20px;\n  min-height: 20px;\n  border: none;\n  outline: none;\n}\n.flexlayout__border_toolbar_button-float {\n  background: transparent url(\"../images/popout.png\") no-repeat center;\n}\n.flexlayout__border_toolbar_button_overflow {\n  border: none;\n  padding-left: 12px;\n  color: gray;\n  font-size: inherit;\n  background: transparent url(\"../images/more2.png\") no-repeat left;\n}\n.flexlayout__border_toolbar_button_overflow_top, .flexlayout__border_toolbar_button_overflow_bottom {\n  margin-left: 10px;\n}\n.flexlayout__border_toolbar_button_overflow_right, .flexlayout__border_toolbar_button_overflow_left {\n  padding-right: 0px;\n  margin-top: 5px;\n}\n.flexlayout__popup_menu {\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__popup_menu_item {\n  padding: 2px 10px 2px 10px;\n  white-space: nowrap;\n}\n@media (hover: hover) {\n  .flexlayout__popup_menu_item:hover {\n    background-color: #d4d4d4;\n  }\n}\n.flexlayout__popup_menu_container {\n  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.15);\n  border: 1px solid #d4d4d4;\n  color: black;\n  background: white;\n  border-radius: 3px;\n  position: absolute;\n  z-index: 1000;\n  max-height: 50%;\n  min-width: 100px;\n  overflow: auto;\n}\n.flexlayout__floating_window _body {\n  height: 100%;\n}\n.flexlayout__floating_window_content {\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n}\n.flexlayout__floating_window_tab {\n  overflow: auto;\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n  box-sizing: border-box;\n  background-color: white;\n  color: black;\n}\n.flexlayout__error_boundary_container {\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n  display: flex;\n  justify-content: center;\n}\n.flexlayout__error_boundary_content {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tabset_sizer {\n  padding-top: 5px;\n  padding-bottom: 3px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__tabset_header_sizer {\n  padding-top: 3px;\n  padding-bottom: 3px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__border_sizer {\n  padding-top: 6px;\n  padding-bottom: 5px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n} */", ""]);
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
module.exports = JSON.parse('{"name":"ipyflex","version":"0.1.0","description":"Jupyter Widget Flex Layout","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//ipyflex","bugs":{"url":"https://github.com//ipyflex/issues"},"license":"BSD-3-Clause","author":{"name":"Trung Le","email":"leductrungxf@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//ipyflex"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyflex/labextension","clean:nbextension":"rimraf ipyflex/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.4.1","@emotion/styled":"^11.3.0","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@jupyter-widgets/controls":"^3.0.0","@jupyterlab/apputils":"^3.2.0","@mui/material":"^5.0.4","flexlayout-react":"^0.5.17"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","process":"^0.11.10","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^9.2.6","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyflex/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true},"react":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_con-d81bea.4d432268cf7e5c65e0f5.js.map