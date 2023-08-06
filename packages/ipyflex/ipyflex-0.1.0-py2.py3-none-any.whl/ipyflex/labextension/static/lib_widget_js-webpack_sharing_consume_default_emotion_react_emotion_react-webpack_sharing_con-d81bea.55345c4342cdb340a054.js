(self["webpackChunkipyflex"] = self["webpackChunkipyflex"] || []).push([["lib_widget_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_con-d81bea"],{

/***/ "./lib/defaultModelFactory.js":
/*!************************************!*\
  !*** ./lib/defaultModelFactory.js ***!
  \************************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.updateModelEditable = exports.defaultModelFactoty = void 0;
function defaultModelFactoty(config, editable = true) {
    const { borderLeft, borderRight } = config;
    const borders = [];
    if (borderLeft) {
        borders.push({
            type: 'border',
            location: 'left',
            size: 250,
            children: [],
        });
    }
    if (borderRight) {
        borders.push({
            type: 'border',
            location: 'right',
            size: 250,
            children: [],
        });
    }
    const globaleDict = {
        tabEnableRename: editable,
        tabEnableClose: editable,
        tabSetEnableClose: editable,
        tabEnableDrag: editable,
        tabSetEnableDrag: editable,
    };
    const defaultModel = {
        global: globaleDict,
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
        borders,
    };
    const defaultOuterModel = {
        global: Object.assign(Object.assign({}, globaleDict), { tabSetTabLocation: 'bottom' }),
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
                                    global: globaleDict,
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
                                    borders,
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
    return { defaultOuterModel, defaultModel };
}
exports.defaultModelFactoty = defaultModelFactoty;
function updateModelEditable(model, editable) {
    const globaleDict = {
        tabEnableRename: editable,
        tabEnableClose: editable,
        tabSetEnableClose: editable,
        tabEnableDrag: editable,
        tabSetEnableDrag: editable,
    };
    if ('global' in model) {
        model.global = Object.assign(Object.assign({}, globaleDict), { tabSetTabLocation: 'bottom' });
    }
    const tabsetList = model['layout']['children'];
    for (const tabset of tabsetList) {
        const children = tabset['children'];
        for (const child of children) {
            child['config']['model']['global'] = Object.assign(Object.assign({}, globaleDict), child['config']['model']['global']);
        }
    }
    return model;
}
exports.updateModelEditable = updateModelEditable;
//# sourceMappingURL=defaultModelFactory.js.map

/***/ }),

/***/ "./lib/dialogWidget.js":
/*!*****************************!*\
  !*** ./lib/dialogWidget.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
class BodyWidget extends widgets_1.Widget {
    constructor(el) {
        super({ node: el });
    }
    getValue() {
        return this.node.value;
    }
}
function dialogBody(title, defaultValue = null) {
    const saveBtn = apputils_1.Dialog.okButton({ label: 'Save' });
    const cancelBtn = apputils_1.Dialog.cancelButton({ label: 'Cancel' });
    const input = document.createElement('input');
    if (defaultValue) {
        input.value = defaultValue;
    }
    return { title, body: new BodyWidget(input), buttons: [cancelBtn, saveBtn] };
}
exports["default"] = dialogBody;
//# sourceMappingURL=dialogWidget.js.map

/***/ }),

/***/ "./lib/menuWidget.js":
/*!***************************!*\
  !*** ./lib/menuWidget.js ***!
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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WidgetMenu = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const Menu_1 = __importDefault(__webpack_require__(/*! @mui/material/Menu */ "./node_modules/@mui/material/Menu/index.js"));
const MenuItem_1 = __importDefault(__webpack_require__(/*! @mui/material/MenuItem */ "./node_modules/@mui/material/MenuItem/index.js"));
const dialogWidget_1 = __importDefault(__webpack_require__(/*! ./dialogWidget */ "./lib/dialogWidget.js"));
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const CREATE_NEW = 'Create new';
class WidgetMenu extends react_1.Component {
    constructor(props) {
        super(props);
        this.on_msg = (data, buffer) => {
            const { action, payload } = data;
            switch (action) {
                case 'update_children':
                    {
                        const wName = payload.name;
                        this.setState((old) => (Object.assign(Object.assign({}, old), { widgetList: [...old.widgetList, wName] })));
                    }
                    return null;
            }
        };
        this.handleClick = (event) => {
            const target = event.currentTarget;
            this.setState((oldState) => (Object.assign(Object.assign({}, oldState), { anchorEl: target })));
        };
        this.handleClose = () => {
            this.setState((oldState) => (Object.assign(Object.assign({}, oldState), { anchorEl: null })));
        };
        props.model.listenTo(props.model, 'msg:custom', this.on_msg);
        this.state = {
            anchorEl: null,
            widgetList: [...props.widgetList, CREATE_NEW],
        };
    }
    render() {
        const menuId = `add_widget_menu_${this.props.tabsetId}@${this.props.nodeId}`;
        const menuItem = [];
        for (const name of this.state.widgetList) {
            if (name !== CREATE_NEW) {
                menuItem.push(react_1.default.createElement(MenuItem_1.default, { key: `${name}}@${this.props.tabsetId}@${this.props.nodeId}`, onClick: () => {
                        this.props.addTabToTabset(name, this.props.nodeId, this.props.tabsetId);
                        this.handleClose();
                    } }, name));
            }
        }
        const createNew = (react_1.default.createElement(MenuItem_1.default, { key: `$#{this.props.tabsetId}@${this.props.nodeId}`, onClick: () => __awaiter(this, void 0, void 0, function* () {
                this.handleClose();
                let widgetName;
                const result = yield apputils_1.showDialog(dialogWidget_1.default('Widget name', ''));
                if (result.button.label === 'Save' && result.value) {
                    widgetName = result.value;
                    this.setState((old) => (Object.assign(Object.assign({}, old), { widgetList: [...old.widgetList, widgetName] })));
                }
                else {
                    return;
                }
                this.props.addTabToTabset(widgetName, this.props.nodeId, this.props.tabsetId);
            }) }, CREATE_NEW));
        menuItem.push(createNew);
        return (react_1.default.createElement("div", { key: menuId },
            react_1.default.createElement("button", { className: utils_1.JUPYTER_BUTTON_CLASS, style: { height: '27px', width: '40px' }, onClick: this.handleClick },
                react_1.default.createElement("i", { className: "fas fa-plus" })),
            react_1.default.createElement(Menu_1.default, { id: "simple-menu", anchorEl: this.state.anchorEl, keepMounted: true, open: Boolean(this.state.anchorEl), onClose: this.handleClose }, menuItem)));
    }
}
exports.WidgetMenu = WidgetMenu;
//# sourceMappingURL=menuWidget.js.map

/***/ }),

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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.FlexWidget = void 0;
__webpack_require__(/*! flexlayout-react/style/light.css */ "./node_modules/flexlayout-react/style/light.css");
const Toolbar_1 = __importDefault(__webpack_require__(/*! @mui/material/Toolbar */ "./node_modules/@mui/material/Toolbar/index.js"));
const FlexLayout = __importStar(__webpack_require__(/*! flexlayout-react */ "webpack/sharing/consume/default/flexlayout-react/flexlayout-react"));
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const utils_1 = __webpack_require__(/*! ./utils */ "./lib/utils.js");
const menuWidget_1 = __webpack_require__(/*! ./menuWidget */ "./lib/menuWidget.js");
const widgetWrapper_1 = __webpack_require__(/*! ./widgetWrapper */ "./lib/widgetWrapper.js");
const defaultModelFactory_1 = __webpack_require__(/*! ./defaultModelFactory */ "./lib/defaultModelFactory.js");
const dialogWidget_1 = __importDefault(__webpack_require__(/*! ./dialogWidget */ "./lib/dialogWidget.js"));
const apputils_1 = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
const commands_1 = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands");
class FlexWidget extends react_1.Component {
    constructor(props) {
        super(props);
        this.on_msg = (data, buffer) => {
            const { action, payload } = data;
            switch (action) {
                case 'update_children':
                    {
                        const wName = payload.name;
                        this.setState((old) => (Object.assign(Object.assign({}, old), { widgetList: [...old.widgetList, wName] })));
                    }
                    return null;
            }
        };
        this.factory = (node) => {
            const component = node.getComponent();
            // const config = node.getConfig();
            const nodeId = node.getId();
            const name = node.getName();
            switch (component) {
                case 'Widget': {
                    return react_1.default.createElement(widgetWrapper_1.WidgetWrapper, { model: this.model, widgetName: name });
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
                defaultModel = this.state.defaultModel;
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
                setTimeout(() => {
                    window.dispatchEvent(new Event('resize'));
                }, 100);
            }
            return action;
        };
        this.innerOnAction = (outerNodeID, action) => {
            if (action.type === 'FlexLayout_MoveNode' ||
                action.type === 'FlexLayout_AdjustSplit' ||
                action.type === 'FlexLayout_DeleteTab' ||
                action.type === 'FlexLayout_MaximizeToggle' ||
                action.type === 'FlexLayout_SelectTab') {
                setTimeout(() => {
                    window.dispatchEvent(new Event('resize'));
                }, 100);
            }
            return action;
        };
        this.onRenderTabSet = (tabSetNode, renderValues, nodeId) => {
            if (this.state.editable) {
                const tabsetId = tabSetNode.getId();
                renderValues.buttons.push(react_1.default.createElement(menuWidget_1.WidgetMenu, { widgetList: this.state.widgetList, nodeId: nodeId, tabsetId: tabsetId, addTabToTabset: (name) => {
                        this.innerlayoutRef[nodeId].current.addTabToTabSet(tabsetId, {
                            component: 'Widget',
                            name: name,
                            config: { layoutID: nodeId },
                        });
                    }, model: this.props.model }));
            }
        };
        this.onAddRow = () => {
            this.layoutRef.current.addTabToActiveTabSet({
                component: 'sub',
                name: 'New section',
            });
        };
        this.onRenderOuterTabSet = (tabSetNode, renderValues) => {
            if (this.state.editable) {
                renderValues.stickyButtons.push(react_1.default.createElement("button", { className: utils_1.JUPYTER_BUTTON_CLASS, onClick: this.onAddRow, style: {
                        width: '25px',
                        height: '25px',
                        paddingLeft: 'unset',
                        paddingRight: 'unset',
                        margin: 0,
                    } },
                    react_1.default.createElement("i", { className: "fas fa-plus" })));
            }
        };
        this.saveTemplate = () => __awaiter(this, void 0, void 0, function* () {
            const oldTemplate = this.props.model.get('template');
            const result = yield apputils_1.showDialog(dialogWidget_1.default('Save template', oldTemplate));
            if (result.button.label === 'Save') {
                const fileName = result.value;
                if (fileName) {
                    this.props.send_msg({
                        action: 'save_template',
                        payload: {
                            file_name: result.value,
                            json_data: this.state.model.toJson(),
                        },
                    });
                }
                else {
                    alert('Invalid file name!');
                }
            }
        });
        this.toggleLock = () => {
            this.setState((old) => (Object.assign(Object.assign({}, old), { editable: !old.editable })));
        };
        this.contextMenuFactory = (node) => {
            const commands = new commands_1.CommandRegistry();
            const nodeId = node.getId();
            commands.addCommand('hide-tab-bar', {
                execute: () => {
                    const subLayout = this.innerlayoutRef[nodeId].current;
                    subLayout.props.model.doAction(FlexLayout.Actions.updateModelAttributes({
                        tabSetEnableTabStrip: false,
                    }));
                },
                label: 'Hide Tab Bar',
                isEnabled: () => true,
            });
            commands.addCommand('show-tab-bar', {
                execute: () => {
                    const subLayout = this.innerlayoutRef[nodeId].current;
                    subLayout.props.model.doAction(FlexLayout.Actions.updateModelAttributes({
                        tabSetEnableTabStrip: true,
                    }));
                },
                label: 'Show Tab Bar',
                isEnabled: () => true,
            });
            const contextMenu = new widgets_1.ContextMenu({ commands });
            contextMenu.addItem({
                command: 'show-tab-bar',
                selector: '.flexlayout__tab_button_bottom',
                rank: 0,
            });
            contextMenu.addItem({
                command: 'hide-tab-bar',
                selector: '.flexlayout__tab_button_bottom',
                rank: 1,
            });
            return contextMenu;
        };
        this.layoutRef = react_1.default.createRef();
        props.model.listenTo(props.model, 'msg:custom', this.on_msg);
        this.innerlayoutRef = {};
        this.layoutConfig = props.model.get('layout_config');
        const { defaultOuterModel, defaultModel } = defaultModelFactory_1.defaultModelFactoty(this.layoutConfig, props.editable);
        let template_json = props.model.get('template_json');
        if (!template_json || Object.keys(template_json).length === 0) {
            template_json = defaultOuterModel;
        }
        else {
            template_json = defaultModelFactory_1.updateModelEditable(template_json, props.editable);
        }
        let flexModel;
        try {
            flexModel = FlexLayout.Model.fromJson(template_json);
        }
        catch (e) {
            console.error(e);
            console.warn('Failed to build model with saved templated, using default template.');
            flexModel = FlexLayout.Model.fromJson(defaultOuterModel);
        }
        this.state = {
            model: flexModel,
            defaultOuterModel,
            defaultModel,
            widgetList: Object.keys(this.props.model.get('children')),
            editable: props.editable,
        };
        this.model = props.model;
        this.contextMenuCache = new Map();
    }
    render() {
        return (react_1.default.createElement("div", { style: Object.assign({ height: '510px' }, this.props.style) },
            react_1.default.createElement("div", { style: {
                    width: '100%',
                    height: this.state.editable ? 'calc(100% - 31px)' : '100%',
                } },
                react_1.default.createElement(FlexLayout.Layout, { ref: this.layoutRef, model: this.state.model, factory: this.factory, supportsPopout: true, classNameMapper: (className) => {
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
                    }, onRenderTab: (node, _) => {
                        const nodeId = node.getId();
                        if (!this.contextMenuCache.has(nodeId)) {
                            const contextMenu = this.contextMenuFactory(node);
                            this.contextMenuCache.set(nodeId, contextMenu);
                        }
                    }, onContextMenu: (node, event) => {
                        event.preventDefault();
                        event.stopPropagation();
                        const contextMenu = this.contextMenuCache.get(node.getId());
                        contextMenu.open(event.nativeEvent);
                    } })),
            this.state.editable ? (react_1.default.createElement(Toolbar_1.default, { variant: "dense", style: {
                    height: '30px',
                    minHeight: '30px',
                } },
                react_1.default.createElement("button", { className: utils_1.JUPYTER_BUTTON_CLASS, onClick: this.saveTemplate }, "Save template"))) : (react_1.default.createElement("div", null))));
    }
}
exports.FlexWidget = FlexWidget;
exports["default"] = FlexWidget;
//# sourceMappingURL=reactWidget.js.map

/***/ }),

/***/ "./lib/utils.js":
/*!**********************!*\
  !*** ./lib/utils.js ***!
  \**********************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.JUPYTER_BUTTON_CLASS = void 0;
exports.JUPYTER_BUTTON_CLASS = 'lm-Widget p-Widget jupyter-widgets jupyter-button widget-button';
//# sourceMappingURL=utils.js.map

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
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: FlexLayoutModel.model_name, _model_module: FlexLayoutModel.model_module, _model_module_version: FlexLayoutModel.model_module_version, _view_name: FlexLayoutModel.view_name, _view_module: FlexLayoutModel.view_module, _view_module_version: FlexLayoutModel.view_module_version, children: [], layout_config: { borderLeft: false, borderRight: false }, style: {}, template_json: null, editable: true });
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
class ReactWidgetWrapper extends apputils_1.ReactWidget {
    constructor(send_msg, model, style = {}, editable = true) {
        super();
        this.onResize = (msg) => {
            window.dispatchEvent(new Event('resize'));
        };
        this._send_msg = send_msg;
        this._model = model;
        this._style = style;
        this._editable = editable;
    }
    render() {
        return (react_1.default.createElement(reactWidget_1.default, { style: this._style, send_msg: this._send_msg, model: this._model, editable: this._editable }));
    }
}
class FlexLayoutView extends base_1.DOMWidgetView {
    setStyle() {
        const style = this.model.get('style');
        if (!style) {
            return;
        }
        for (const [key, value] of Object.entries(style)) {
            const fixedKey = key
                .split(/(?=[A-Z])/)
                .map((s) => s.toLowerCase())
                .join('-');
            this.el.style[fixedKey] = value;
        }
    }
    render() {
        super.render();
        this.setStyle();
        this.el.classList.add('custom-widget');
        const style = this.model.get('style');
        const editable = this.model.get('editable');
        const widget = new ReactWidgetWrapper(this.send.bind(this), this.model, style, editable);
        messaging_1.MessageLoop.sendMessage(widget, widgets_1.Widget.Msg.BeforeAttach);
        this.el.insertBefore(widget.node, null);
        messaging_1.MessageLoop.sendMessage(widget, widgets_1.Widget.Msg.AfterAttach);
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
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.WidgetWrapper = void 0;
const react_1 = __importStar(__webpack_require__(/*! react */ "webpack/sharing/consume/default/react"));
const messaging_1 = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging");
const widgets_1 = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
class WidgetWrapper extends react_1.Component {
    constructor(props) {
        super(props);
        this.on_children_change = (model, newValue, change) => {
            if (this.placeholder && this.widgetName in newValue) {
                this.myRef.current.firstChild.remove();
                this._render_widget(newValue[this.widgetName]);
                this.placeholder = false;
            }
        };
        this._render_widget = (model) => {
            const manager = this.model.widget_manager;
            manager.create_view(model, {}).then((view) => {
                messaging_1.MessageLoop.sendMessage(view.pWidget, widgets_1.Widget.Msg.BeforeAttach);
                this.myRef.current.insertBefore(view.pWidget.node, null);
                view.displayed.then(() => __awaiter(this, void 0, void 0, function* () {
                    yield new Promise((r) => setTimeout(r, 100));
                    window.dispatchEvent(new Event('resize'));
                }));
                messaging_1.MessageLoop.sendMessage(view.pWidget, widgets_1.Widget.Msg.AfterAttach);
            });
        };
        this.model = props.model;
        this.model.listenTo(this.model, 'change:children', this.on_children_change);
        this.widgetName = props.widgetName;
        this.state = {
            state: 0,
        };
        this.myRef = react_1.default.createRef();
    }
    componentDidMount() {
        const children = this.model.get('children');
        const widgetModel = children[this.widgetName];
        if (widgetModel) {
            this._render_widget(widgetModel);
            this.placeholder = false;
        }
        else {
            const placeHolder = document.createElement('p');
            placeHolder.style.textAlign = 'center';
            placeHolder.style.padding = '20px';
            placeHolder.innerText = `Placeholder for ${this.widgetName} widget`;
            this.myRef.current.insertBefore(placeHolder, null);
            this.placeholder = true;
        }
    }
    render() {
        return react_1.default.createElement("div", { className: "ipyflex-widget-box", ref: this.myRef });
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
exports.push([module.id, ".custom-widget {\n  height: 100%;\n  border: var(--jp-border-width) solid var(--jp-cell-editor-border-color);\n}\n.custom-widget > .p-Widget {\n  height: 100%;\n}\n\n.ipyflex-widget-box {\n  height: calc(100% - 12px);\n  width: calc(100% - 10px);\n  margin: 0px 5px 10px 5px;\n  box-shadow: 0 3px 6px rgba(0, 0, 0, 0.16), 0 3px 6px rgba(0, 0, 0, 0.23);\n  border-width: 0px 0px 0px 0px;\n  border-style: solid;\n  border-color: #e2e2e2;\n  border-radius: 0px;\n  outline-width: 0px;\n  outline-style: solid;\n  outline-color: #e2e2e2;\n  overflow: auto;\n}\n\n\n.flexlayout__layout {\n  left: unset !important;\n  top: unset !important;\n  right: unset !important;\n  bottom: unset !important;\n  position: unset !important;\n  overflow: unset !important;\n  height: 100%;\n}\n\n.flexlayout__tabset-selected {\n  background-color: var(--jp-layout-color3);\n  border: var(--jp-border-width) solid var(--jp-cell-editor-border-color);\n}\n\n.flexlayout__tab_button--selected {\n  background-color: var(--jp-layout-color0);\n  color: var(--jp-ui-font-color1);\n}\n.inner__flexlayout__tabset .flexlayout__tab_button--selected {\n  background-color: var(--jp-layout-color1) !important;\n}\n.inner__flexlayout__tabset .inner__flexlayout__tabset-selected {\n  background-color: var(--jp-layout-color2) !important;\n}\n.inner__flexlayout__tabset .flexlayout__tabset_tabbar_outer {\n  background-color: var(--jp-layout-color2) !important;\n}\n.inner__flexlayout__tabset .inner__flexlayout__tabset {\n  background-color: var(--jp-cell-editor-background) !important;\n}\n.inner__flexlayout__tabset.flexlayout__tabset{\n  background: var(--jp-layout-color0);\n  height: 32px!important;\n}\n.inner__flexlayout__tab {\n  background: var(--jp-layout-color0);\n}\n\n.flexlayout__splitter {\n  background-color: var(--jp-cell-editor-background);\n}\n\n@media (hover: hover) {\n  .flexlayout__splitter:hover {\n    background-color: var(--jp-layout-color2);\n  }\n}\n.flexlayout__splitter_drag {\n  z-index: 1000;\n  background-color: var(--jp-layout-color2);\n}\n\ndiv.inner__flexlayout__tabset > div.flexlayout__tabset_tabbar_outer_top {\n  margin-left: 5px;\n  margin-right: 5px;\n  box-shadow: 0 3px 6px rgb(0 0 0 / 16%), 0 3px 6px rgb(0 0 0 / 23%);\n  border-width: 1px 0px 0px 0px;\n  border-style: solid;\n  border-color: #e2e2e2;\n}\n/* .custom-widget .panel {\n  height:100%;\n  display:flex;\n  justify-content:center;\n  align-items:center;\n  background-color:white;\n  border:1px solid #555;\n  box-sizing: border-box;\n} */\n/* \n\n.flexlayout__layout {\n  height: 100%;\n}\n.flexlayout__splitter {\n  background-color: #f7f7f7;\n}\n@media (hover: hover) {\n  .flexlayout__splitter:hover {\n    background-color: #e2e2e2;\n  }\n}\n.flexlayout__splitter_border {\n  z-index: 10;\n}\n.flexlayout__splitter_drag {\n  z-index: 1000;\n  background-color: #e2e2e2;\n}\n.flexlayout__splitter_extra {\n  background-color: transparent;\n}\n.flexlayout__outline_rect {\n  position: absolute;\n  pointer-events: none;\n  box-sizing: border-box;\n  border: 2px solid red;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.2);\n  border-radius: 5px;\n  z-index: 1000;\n}\n.flexlayout__outline_rect_edge {\n  pointer-events: none;\n  border: 2px solid green;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.2);\n  border-radius: 5px;\n  z-index: 1000;\n  box-sizing: border-box;\n}\n.flexlayout__edge_rect {\n  position: absolute;\n  z-index: 1000;\n  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.2);\n  background-color: gray;\n  pointer-events: none;\n}\n.flexlayout__drag_rect {\n  position: absolute;\n  cursor: move;\n  color: black;\n  background-color: #f7f7f7;\n  border: 2px solid #e2e2e2;\n  box-shadow: inset 0 0 60px rgba(0, 0, 0, 0.3);\n  border-radius: 5px;\n  z-index: 1000;\n  box-sizing: border-box;\n  opacity: 0.9;\n  text-align: center;\n  display: flex;\n  justify-content: center;\n  flex-direction: column;\n  overflow: hidden;\n  padding: 10px;\n  word-wrap: break-word;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__tabset {\n  overflow: hidden;\n  background-color: #f7f7f7;\n  box-sizing: border-box;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n  background-color: white;\n}\n.flexlayout__tabset_header {\n  position: absolute;\n  display: flex;\n  align-items: center;\n  left: 0;\n  right: 0;\n  padding: 3px 3px 3px 5px;\n  box-sizing: border-box;\n  border-bottom: 1px solid #e9e9e9;\n  color: black;\n  background-color: white;\n}\n.flexlayout__tabset_header_content {\n  flex-grow: 1;\n}\n.flexlayout__tabset_tabbar_outer {\n  box-sizing: border-box;\n  background-color: #f7f7f7;\n  position: absolute;\n  left: 0;\n  right: 0;\n  overflow: hidden;\n  display: flex;\n  background-color: white;\n}\n.flexlayout__tabset_tabbar_outer_top {\n  border-bottom: 1px solid #e9e9e9;\n}\n.flexlayout__tabset_tabbar_outer_bottom {\n  border-top: 1px solid #e9e9e9;\n}\n.flexlayout__tabset_tabbar_inner {\n  position: relative;\n  box-sizing: border-box;\n  display: flex;\n  flex-grow: 1;\n  overflow: hidden;\n}\n.flexlayout__tabset_tabbar_inner_tab_container {\n  display: flex;\n  box-sizing: border-box;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  width: 10000px;\n}\n.flexlayout__tabset_tabbar_inner_tab_container_top {\n  border-top: 2px solid transparent;\n}\n.flexlayout__tabset_tabbar_inner_tab_container_bottom {\n  border-bottom: 2px solid transparent;\n}\n.flexlayout__tabset-selected {\n  background-color: #f7f7f7;\n}\n.flexlayout__tabset-maximized {\n  background-color: #d4d4d4;\n}\n.flexlayout__tab {\n  overflow: auto;\n  position: absolute;\n  box-sizing: border-box;\n  color: black;\n  background-color: white;\n}\n.flexlayout__tab_button {\n  display: inline-flex;\n  align-items: center;\n  box-sizing: border-box;\n  padding: 3px 8px;\n  margin: 0px 2px;\n  cursor: pointer;\n}\n.flexlayout__tab_button--selected {\n  background-color: #e9e9e9;\n  color: black;\n}\n@media (hover: hover) {\n  .flexlayout__tab_button:hover {\n    background-color: #e9e9e9;\n    color: black;\n  }\n}\n.flexlayout__tab_button--unselected {\n  color: gray;\n}\n.flexlayout__tab_button_leading {\n  display: inline-block;\n}\n.flexlayout__tab_button_content {\n  display: inline-block;\n}\n.flexlayout__tab_button_textbox {\n  border: none;\n  color: green;\n  background-color: #e9e9e9;\n}\n.flexlayout__tab_button_textbox:focus {\n  outline: none;\n}\n.flexlayout__tab_button_trailing {\n  display: inline-block;\n  margin-left: 8px;\n  min-width: 8px;\n  min-height: 8px;\n}\n@media (pointer: coarse) {\n  .flexlayout__tab_button_trailing {\n    min-width: 20px;\n    min-height: 20px;\n  }\n}\n@media (hover: hover) {\n  .flexlayout__tab_button:hover .flexlayout__tab_button_trailing {\n    background: transparent url(\"../images/close.png\") no-repeat center;\n  }\n}\n.flexlayout__tab_button--selected .flexlayout__tab_button_trailing {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__tab_button_overflow {\n  margin-left: 10px;\n  padding-left: 12px;\n  border: none;\n  color: gray;\n  font-size: inherit;\n  background: transparent url(\"../images/more2.png\") no-repeat left;\n}\n.flexlayout__tab_toolbar {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tab_toolbar_button {\n  min-width: 20px;\n  min-height: 20px;\n  border: none;\n  outline: none;\n}\n.flexlayout__tab_toolbar_button-min {\n  background: transparent url(\"../images/maximize.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-max {\n  background: transparent url(\"../images/restore.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-float {\n  background: transparent url(\"../images/popout.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_button-close {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__tab_toolbar_sticky_buttons_container {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tab_floating {\n  overflow: auto;\n  position: absolute;\n  box-sizing: border-box;\n  color: black;\n  background-color: white;\n  display: flex;\n  justify-content: center;\n  align-items: center;\n}\n.flexlayout__tab_floating_inner {\n  overflow: auto;\n  display: flex;\n  flex-direction: column;\n  justify-content: center;\n  align-items: center;\n}\n.flexlayout__tab_floating_inner div {\n  margin-bottom: 5px;\n  text-align: center;\n}\n.flexlayout__tab_floating_inner div a {\n  color: royalblue;\n}\n.flexlayout__border {\n  box-sizing: border-box;\n  overflow: hidden;\n  display: flex;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n  background-color: white;\n}\n.flexlayout__border_top {\n  border-bottom: 1px solid #e9e9e9;\n  align-items: center;\n}\n.flexlayout__border_bottom {\n  border-top: 1px solid #e9e9e9;\n  align-items: center;\n}\n.flexlayout__border_left {\n  border-right: 1px solid #e9e9e9;\n  align-content: center;\n  flex-direction: column;\n}\n.flexlayout__border_right {\n  border-left: 1px solid #e9e9e9;\n  align-content: center;\n  flex-direction: column;\n}\n.flexlayout__border_inner {\n  position: relative;\n  box-sizing: border-box;\n  display: flex;\n  overflow: hidden;\n  flex-grow: 1;\n}\n.flexlayout__border_inner_tab_container {\n  white-space: nowrap;\n  display: flex;\n  box-sizing: border-box;\n  position: absolute;\n  top: 0;\n  bottom: 0;\n  width: 10000px;\n}\n.flexlayout__border_inner_tab_container_right {\n  transform-origin: top left;\n  transform: rotate(90deg);\n}\n.flexlayout__border_inner_tab_container_left {\n  flex-direction: row-reverse;\n  transform-origin: top right;\n  transform: rotate(-90deg);\n}\n.flexlayout__border_button {\n  display: flex;\n  align-items: center;\n  cursor: pointer;\n  padding: 3px 8px;\n  margin: 2px;\n  box-sizing: border-box;\n  white-space: nowrap;\n  background-color: #f0f0f0;\n}\n.flexlayout__border_button--selected {\n  background-color: #e9e9e9;\n  color: black;\n}\n@media (hover: hover) {\n  .flexlayout__border_button:hover {\n    background-color: #e9e9e9;\n    color: black;\n  }\n}\n.flexlayout__border_button--unselected {\n  color: gray;\n}\n.flexlayout__border_button_leading {\n  display: inline;\n}\n.flexlayout__border_button_content {\n  display: inline-block;\n}\n.flexlayout__border_button_trailing {\n  display: inline-block;\n  margin-left: 8px;\n  min-width: 8px;\n  min-height: 8px;\n}\n@media (pointer: coarse) {\n  .flexlayout__border_button_trailing {\n    min-width: 20px;\n    min-height: 20px;\n  }\n}\n@media (hover: hover) {\n  .flexlayout__border_button:hover .flexlayout__border_button_trailing {\n    background: transparent url(\"../images/close.png\") no-repeat center;\n  }\n}\n.flexlayout__border_button--selected .flexlayout__border_button_trailing {\n  background: transparent url(\"../images/close.png\") no-repeat center;\n}\n.flexlayout__border_toolbar {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__border_toolbar_left {\n  flex-direction: column;\n}\n.flexlayout__border_toolbar_right {\n  flex-direction: column;\n}\n.flexlayout__border_toolbar_button {\n  min-width: 20px;\n  min-height: 20px;\n  border: none;\n  outline: none;\n}\n.flexlayout__border_toolbar_button-float {\n  background: transparent url(\"../images/popout.png\") no-repeat center;\n}\n.flexlayout__border_toolbar_button_overflow {\n  border: none;\n  padding-left: 12px;\n  color: gray;\n  font-size: inherit;\n  background: transparent url(\"../images/more2.png\") no-repeat left;\n}\n.flexlayout__border_toolbar_button_overflow_top, .flexlayout__border_toolbar_button_overflow_bottom {\n  margin-left: 10px;\n}\n.flexlayout__border_toolbar_button_overflow_right, .flexlayout__border_toolbar_button_overflow_left {\n  padding-right: 0px;\n  margin-top: 5px;\n}\n.flexlayout__popup_menu {\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__popup_menu_item {\n  padding: 2px 10px 2px 10px;\n  white-space: nowrap;\n}\n@media (hover: hover) {\n  .flexlayout__popup_menu_item:hover {\n    background-color: #d4d4d4;\n  }\n}\n.flexlayout__popup_menu_container {\n  box-shadow: inset 0 0 5px rgba(0, 0, 0, 0.15);\n  border: 1px solid #d4d4d4;\n  color: black;\n  background: white;\n  border-radius: 3px;\n  position: absolute;\n  z-index: 1000;\n  max-height: 50%;\n  min-width: 100px;\n  overflow: auto;\n}\n.flexlayout__floating_window _body {\n  height: 100%;\n}\n.flexlayout__floating_window_content {\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n}\n.flexlayout__floating_window_tab {\n  overflow: auto;\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n  box-sizing: border-box;\n  background-color: white;\n  color: black;\n}\n.flexlayout__error_boundary_container {\n  left: 0;\n  top: 0;\n  right: 0;\n  bottom: 0;\n  position: absolute;\n  display: flex;\n  justify-content: center;\n}\n.flexlayout__error_boundary_content {\n  display: flex;\n  align-items: center;\n}\n.flexlayout__tabset_sizer {\n  padding-top: 5px;\n  padding-bottom: 3px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__tabset_header_sizer {\n  padding-top: 3px;\n  padding-bottom: 3px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n}\n.flexlayout__border_sizer {\n  padding-top: 6px;\n  padding-bottom: 5px;\n  font-size: medium;\n  font-family: Roboto, Arial, sans-serif;\n} */\n", ""]);
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
module.exports = JSON.parse('{"name":"ipyflex","version":"0.1.0","description":"Jupyter Widget Flex Layout","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com//ipyflex","bugs":{"url":"https://github.com//ipyflex/issues"},"license":"BSD-3-Clause","author":{"name":"Trung Le","email":"leductrungxf@gmail.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com//ipyflex"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf ipyflex/labextension","clean:nbextension":"rimraf ipyflex/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@emotion/react":"^11.4.1","@emotion/styled":"^11.3.0","@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@jupyter-widgets/controls":"^3.0.0","@jupyterlab/apputils":"^3.2.0","@mui/material":"^5.0.4","flexlayout-react":"^0.5.20"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","eslint-plugin-react":"^7.26.1","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","process":"^0.11.10","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^9.2.6","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"ipyflex/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true},"react":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js-webpack_sharing_consume_default_emotion_react_emotion_react-webpack_sharing_con-d81bea.55345c4342cdb340a054.js.map