(self["webpackChunkobservable_jupyter_widget"] = self["webpackChunkobservable_jupyter_widget"] || []).push([["lib_widget_js"],{

/***/ "./lib/observable_logo.js":
/*!********************************!*\
  !*** ./lib/observable_logo.js ***!
  \********************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.logo = void 0;
exports.logo = '<svg role="img" viewBox="0 0 25 28" width="25" height="28" aria-label="Observable" fill="currentColor" class="near-black" style="width: 18px;"><path d="M12.5 22.6667C11.3458 22.6667 10.3458 22.4153 9.5 21.9127C8.65721 21.412 7.98339 20.7027 7.55521 19.8654C7.09997 18.9942 6.76672 18.0729 6.56354 17.1239C6.34796 16.0947 6.24294 15.0483 6.25 14C6.25 13.1699 6.30417 12.3764 6.41354 11.6176C6.52188 10.8598 6.72292 10.0894 7.01563 9.30748C7.30833 8.52555 7.68542 7.84763 8.14479 7.27274C8.62304 6.68378 9.24141 6.20438 9.95208 5.87163C10.6979 5.51244 11.5458 5.33333 12.5 5.33333C13.6542 5.33333 14.6542 5.58467 15.5 6.08733C16.3428 6.588 17.0166 7.29733 17.4448 8.13459C17.8969 8.99644 18.2271 9.9103 18.4365 10.8761C18.6448 11.841 18.75 12.883 18.75 14C18.75 14.8301 18.6958 15.6236 18.5865 16.3824C18.4699 17.1702 18.2639 17.9446 17.9719 18.6925C17.6698 19.4744 17.2948 20.1524 16.8427 20.7273C16.3906 21.3021 15.7927 21.7692 15.0479 22.1284C14.3031 22.4876 13.4542 22.6667 12.5 22.6667ZM14.7063 16.2945C15.304 15.6944 15.6365 14.864 15.625 14C15.625 13.1073 15.326 12.3425 14.7292 11.7055C14.1313 11.0685 13.3885 10.75 12.5 10.75C11.6115 10.75 10.8688 11.0685 10.2708 11.7055C9.68532 12.3123 9.36198 13.1405 9.375 14C9.375 14.8927 9.67396 15.6575 10.2708 16.2945C10.8688 16.9315 11.6115 17.25 12.5 17.25C13.3885 17.25 14.124 16.9315 14.7063 16.2945ZM12.5 27C19.4031 27 25 21.1792 25 14C25 6.82075 19.4031 1 12.5 1C5.59687 1 0 6.82075 0 14C0 21.1792 5.59687 27 12.5 27Z" fill="currentColor"></path></svg>';
//# sourceMappingURL=observable_logo.js.map

/***/ }),

/***/ "./lib/version.js":
/*!************************!*\
  !*** ./lib/version.js ***!
  \************************/
/***/ ((__unused_webpack_module, exports, __webpack_require__) => {

"use strict";

// Copyright (c) Thomas Ballinger
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

// Copyright (c) Thomas Ballinger
// Distributed under the terms of the Modified BSD License.
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
exports.ObservableWidgetView = exports.ObservableWidgetModel = void 0;
const base_1 = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base");
const version_1 = __webpack_require__(/*! ./version */ "./lib/version.js");
const wrapper_code_1 = __webpack_require__(/*! ./wrapper_code */ "./lib/wrapper_code.js");
const observable_logo_1 = __webpack_require__(/*! ./observable_logo */ "./lib/observable_logo.js");
// ../src/iframe_code.js because path is relative to lib
// eslint-disable-next-line @typescript-eslint/ban-ts-comment
// @ts-ignore // some webpack import syntax doesn't work with TypeScript?
const iframe_code_js_1 = __importDefault(__webpack_require__(/*! !!raw-loader!../src/iframe_code.js */ "./node_modules/raw-loader/dist/cjs.js!./src/iframe_code.js"));
__webpack_require__(/*! ../css/widget.css */ "./css/widget.css");
class ObservableWidgetModel extends base_1.DOMWidgetModel {
    defaults() {
        return Object.assign(Object.assign({}, super.defaults()), { _model_name: ObservableWidgetModel.model_name, _model_module: ObservableWidgetModel.model_module, _model_module_version: ObservableWidgetModel.model_module_version, _view_name: ObservableWidgetModel.view_name, _view_module: ObservableWidgetModel.view_module, _view_module_version: ObservableWidgetModel.view_module_version, value: 'fake initial value', slug: 'nonsense slug', cells: [], inputs: { initialInput: 123 } });
    }
}
exports.ObservableWidgetModel = ObservableWidgetModel;
ObservableWidgetModel.serializers = Object.assign({}, base_1.DOMWidgetModel.serializers);
ObservableWidgetModel.model_name = 'ObservableWidgetModel';
ObservableWidgetModel.model_module = version_1.MODULE_NAME;
ObservableWidgetModel.model_module_version = version_1.MODULE_VERSION;
ObservableWidgetModel.view_name = 'ObservableWidgetView';
ObservableWidgetModel.view_module = version_1.MODULE_NAME;
ObservableWidgetModel.view_module_version = version_1.MODULE_VERSION;
class ObservableWidgetView extends base_1.DOMWidgetView {
    constructor() {
        super(...arguments);
        this.queuedInputs = [];
        // ugly hack until I figure out how to add code to the constructor
        this.pAndR = (function promiseAndResolve() {
            let resolve;
            const p = new Promise((r) => {
                resolve = r;
            });
            return [p, resolve];
        })();
        this.iframeReadyForInputs = this.pAndR[0];
        this.setIframeReadyForInputs = this.pAndR[1];
        this.onInputs = () => __awaiter(this, void 0, void 0, function* () {
            const inputs = this.model.get('inputs');
            this.queuedInputs.push(inputs);
            yield this.iframeReadyForInputs;
            // A lazy way to queue up inputs
            let inputsToSend;
            while ((inputsToSend = this.queuedInputs.shift())) {
                wrapper_code_1.sendInputs(this.iframe, inputsToSend);
            }
        });
        this.onPublishValues = (values) => {
            if (this.outputEl) {
                this.outputEl.textContent =
                    'widget.value: ' + JSON.stringify(values, null, 2);
            }
            this.model.set('value', values);
            this.touch();
        };
    }
    render() {
        this.el.classList.add('custom-widget');
        const slug = this.model.get('slug');
        const cells = this.model.get('cells');
        const pretty_slug = slug.startsWith('d/') ? 'embedded notebook' : slug;
        // TODO make Observable logo optional
        // TODO is this style helpful? I figured it was for aligning the logo
        //<div style="text-align: right; position: relative">
        this.el.innerHTML = `
    <div>
    <a class="observable-link" href="https://observablehq.com/${slug}" target="_blank" style="text-decoration: none; color: inherit;">
    <div class="observable-logo" style="display: flex; align-items: center; justify-content: flex-end;">
    <span>Edit ${pretty_slug} on Observable</span>
    ${observable_logo_1.logo}
    </div>
    </a>

    <iframe sandbox="allow-scripts" style="overflow: auto; min-width: 100%; width: 0px;" frameBorder="0"></iframe>
    <div class="value">initial</div>`;
        this.el.querySelector('iframe').srcdoc = get_srcdoc(slug, cells);
        this.outputEl = this.el.querySelector('.value');
        this.iframe = this.el.querySelector('iframe');
        wrapper_code_1.listenToSizeAndValuesAndReady(this.iframe, this.onPublishValues, this.setIframeReadyForInputs);
        this.onInputs();
        this.model.on('change:inputs', this.onInputs, this);
    }
}
exports.ObservableWidgetView = ObservableWidgetView;
function get_srcdoc(slug, cells) {
    return `<!DOCTYPE html>
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@observablehq/inspector@3/dist/inspector.css">
<style>
body {
  margin: 0;
}
</style>
<div style="overflow: auto;"></div>
<script type="module">
${iframe_code_js_1.default}

const slug = '${slug}';
const into = document.getElementsByTagName('div')[0];
const cells = ${cells ? JSON.stringify(cells) : 'undefined'}
embed(slug, into, cells);
monitor()
// TODO how to clean up monitor or a window event listener when this cell gets rerun?
</script>
`;
}
//# sourceMappingURL=widget.js.map

/***/ }),

/***/ "./lib/wrapper_code.js":
/*!*****************************!*\
  !*** ./lib/wrapper_code.js ***!
  \*****************************/
/***/ ((__unused_webpack_module, exports) => {

"use strict";

Object.defineProperty(exports, "__esModule", ({ value: true }));
exports.sendInputs = exports.listenToSizeAndValuesAndReady = void 0;
function getFrameByEvent(event) {
    return [...document.getElementsByTagName('iframe')].filter((iframe) => {
        return iframe.contentWindow === event.source;
    })[0];
}
// Each embed gets its own event listener.
function listenToSizeAndValuesAndReady(iframe, onValues, onReady) {
    function onMessage(msg) {
        if (!document.body.contains(iframe)) {
            // iframe is gone
            removeEventListener('message', onMessage);
        }
        const senderIframe = getFrameByEvent(msg);
        if (msg.data.type === 'iframeSize' && senderIframe === iframe) {
            iframe.height = msg.data.height;
        }
        else if (msg.data.type === 'allValues' && senderIframe === iframe) {
            onValues(msg.data.allValues);
        }
        else if (msg.data.type === 'ready' && senderIframe === iframe) {
            onReady();
        }
    }
    window.addEventListener('message', onMessage);
}
exports.listenToSizeAndValuesAndReady = listenToSizeAndValuesAndReady;
function sendInputs(iframe, inputs) {
    // TODO error handing when these cannot be serialized!\
    iframe.contentWindow.postMessage({
        type: 'inputs',
        inputs,
    }, '*');
}
exports.sendInputs = sendInputs;
//# sourceMappingURL=wrapper_code.js.map

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
exports.push([module.id, ".observable-logo {\n  position: absolute;\n  bottom: 0;\n  right: 0;\n  margin-bottom: 5px;\n  margin-right: 1px;\n  transition: background-color 0.2s;\n}\n.observable-logo svg {\n  opacity: 0.5;\n  transition: opacity 0.2s;\n}\n.observable-logo span {\n  opacity: 0;\n  transition: opacity 0.2s;\n  padding-right: 0.2em;\n  padding-left: 0.2em;\n}\n.observable-logo:hover {\n  background-color: white;\n}\n.observable-logo:hover span {\n  opacity: 0.8;\n}\n.observable-logo:hover svg {\n  opacity: 0.8;\n}\n/*\n.observable-link:hover ~ iframe {\n  outline: solid 1px #e0e0e0;\n  box-shadow: 0 0 3px;\n  transition: box-shadow 0.2s;\n}\n.observable-link ~ iframe {\n  outline: none;\n}\n*/\n/* Colab-only rule - untested */\nbody > .output-area > .output-body {\n  margin-right: 2px;\n}\n", ""]);
// Exports
module.exports = exports;


/***/ }),

/***/ "./node_modules/css-loader/dist/runtime/api.js":
/*!*****************************************************!*\
  !*** ./node_modules/css-loader/dist/runtime/api.js ***!
  \*****************************************************/
/***/ ((module) => {

"use strict";


/*
  MIT License http://www.opensource.org/licenses/mit-license.php
  Author Tobias Koppers @sokra
*/
// css base code, injected by the css-loader
// eslint-disable-next-line func-names
module.exports = function (useSourceMap) {
  var list = []; // return the list of modules as css string

  list.toString = function toString() {
    return this.map(function (item) {
      var content = cssWithMappingToString(item, useSourceMap);

      if (item[2]) {
        return "@media ".concat(item[2], " {").concat(content, "}");
      }

      return content;
    }).join('');
  }; // import a list of modules into the list
  // eslint-disable-next-line func-names


  list.i = function (modules, mediaQuery, dedupe) {
    if (typeof modules === 'string') {
      // eslint-disable-next-line no-param-reassign
      modules = [[null, modules, '']];
    }

    var alreadyImportedModules = {};

    if (dedupe) {
      for (var i = 0; i < this.length; i++) {
        // eslint-disable-next-line prefer-destructuring
        var id = this[i][0];

        if (id != null) {
          alreadyImportedModules[id] = true;
        }
      }
    }

    for (var _i = 0; _i < modules.length; _i++) {
      var item = [].concat(modules[_i]);

      if (dedupe && alreadyImportedModules[item[0]]) {
        // eslint-disable-next-line no-continue
        continue;
      }

      if (mediaQuery) {
        if (!item[2]) {
          item[2] = mediaQuery;
        } else {
          item[2] = "".concat(mediaQuery, " and ").concat(item[2]);
        }
      }

      list.push(item);
    }
  };

  return list;
};

function cssWithMappingToString(item, useSourceMap) {
  var content = item[1] || ''; // eslint-disable-next-line prefer-destructuring

  var cssMapping = item[3];

  if (!cssMapping) {
    return content;
  }

  if (useSourceMap && typeof btoa === 'function') {
    var sourceMapping = toComment(cssMapping);
    var sourceURLs = cssMapping.sources.map(function (source) {
      return "/*# sourceURL=".concat(cssMapping.sourceRoot || '').concat(source, " */");
    });
    return [content].concat(sourceURLs).concat([sourceMapping]).join('\n');
  }

  return [content].join('\n');
} // Adapted from convert-source-map (MIT)


function toComment(sourceMap) {
  // eslint-disable-next-line no-undef
  var base64 = btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap))));
  var data = "sourceMappingURL=data:application/json;charset=utf-8;base64,".concat(base64);
  return "/*# ".concat(data, " */");
}

/***/ }),

/***/ "./node_modules/raw-loader/dist/cjs.js!./src/iframe_code.js":
/*!******************************************************************!*\
  !*** ./node_modules/raw-loader/dist/cjs.js!./src/iframe_code.js ***!
  \******************************************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("// This code is injected into the iframe via a .srcdoc property\nimport { Runtime, Inspector } from \"https://cdn.jsdelivr.net/npm/@observablehq/runtime@4/dist/runtime.js\";\n\nexport class DocumentBodyDimensionsMutationObserverMonitor {\n    constructor() {\n        this.lastHeight = -1;\n\n        this.onMutation = (entries) => {\n            const height = document.body.clientHeight;\n            if (height !== this.lastHeight) {\n                this.lastHeight = height;\n                postHeight(this.lastHeight);\n            }\n        };\n    }\n\n    start() {\n        this.observer = new MutationObserver(this.onMutation);\n        this.observer.observe(document.body, {\n            childList: true,\n            attributes: true,\n            subtree: true,\n        });\n    }\n}\n\nexport class DocumentBodyDimensionsResizeObserverMonitor {\n    constructor() {\n        if (typeof window.ResizeObserver === 'undefined') {\n            throw Error('ResizeObserver is not supported');\n        }\n        this.lastHeight = -1;\n\n        this.onResize = (entries) => {\n            for (let entry of entries) {\n                const height = entry.contentRect.height;\n                if (height !== this.lastHeight) {\n                    this.lastHeight = height;\n                    postHeight(this.lastHeight);\n                }\n            }\n        };\n    }\n\n    start() {\n        this.observer = new ResizeObserver(this.onResize);\n        this.observer.observe(document.body);\n    }\n}\n\nfunction postHeight(height) {\n    window.parent.postMessage(\n        {\n            type: 'iframeSize',\n            height,\n        },\n        '*'\n    );\n}\n\nexport const monitor = () => {\n    if (typeof window.ResizeObserver !== 'undefined') {\n        new DocumentBodyDimensionsResizeObserverMonitor().start();\n    } else {\n        new DocumentBodyDimensionsMutationObserverMonitor().start();\n    }\n};\n\nclass JupyterWidgetAllValuesObserver {\n    pending() {\n        // could gray something out here\n    }\n    fulfilled(value) {\n        // postMessage does a \"structured clone\" which fails for DOM elements, functions, and more\n        // so let's jsonify\n        // We will probably wastefully jsonify again on the other side of the postMessage\n        const cleaned = {};\n        for (const name of Object.keys(value)) {\n            try {\n                cleaned[name] = JSON.parse(JSON.stringify(value[name]));\n            } catch (e) {\n                cleaned[name] = null;\n            }\n        }\n        window.parent.postMessage(\n            {\n                type: 'allValues',\n                allValues: JSON.parse(JSON.stringify(cleaned)),\n            },\n            '*'\n        );\n    }\n    rejected(error) {\n        console.error('all values rejected:', error);\n    }\n}\n\nexport const embed = async (slug, into, cells) => {\n    const moduleUrl = 'https://api.observablehq.com/' + slug + '.js?v=3';\n    const define = (await import(moduleUrl)).default;\n    const inspect = Inspector.into(into);\n    const filter = cells ? (name) => cells.includes(name) : (name) => true;\n\n    const newDefine = (runtime, observer) => {\n        const main = define(runtime, observer);\n        const outputVariables = new Set();\n        // TODO allow a subset of these to be manually specified?\n        const candidateOutputVariables = cells ? cells : [...main._scope.keys()]\n\n            for (const cell of cells) {\n                if (cell.slice(0, 7) === 'viewof ') {\n                    outputVariables.add(cell.slice(7))\n                } else {\n                    outputVariables.add(cell)\n                }\n            }\n        }\n        main.variable(observer('observableJupyterWidgetAllValues')).define('observableJupyterWidgetAllValues', [\n            ...outputVariables\n        ], function (...args) {\n            const allValues = {};\n            outputVariables.forEach((name, i) => {\n                allValues[name] = args[i];\n            })\n            return allValues;\n        })\n    }\n\n    let main;\n    let setMain;\n    const mainP = new Promise(r => {\n        setMain = r;\n    });\n\n    // TODO wait for this initial inputs message before actually running anything\n    window.addEventListener('message', (msg) => {\n        if (msg.data.type === 'inputs' && msg.source === window.parent) {\n            // only the first time, start things up\n            if (!main) {\n                const runtime = new Runtime();\n                main = runtime.module(newDefine, (name) => {\n                    if (name === 'observableJupyterWidgetAllValues') {\n                        return new JupyterWidgetAllValuesObserver();\n                    }\n                    return filter(name) ? inspect() : true\n                });\n                setMain(main);\n            }\n            window.addEventListener('unload', () => {\n                main._runtime.dispose();\n            });\n\n            const inputs = msg.data.inputs;\n            for (let name of Object.keys(inputs)) {\n                try {\n                    //console.log('redefining', name, 'to', inputs[name]);\n                    main.redefine(name, inputs[name]);\n                } catch (e) {\n                    if (e.message.endsWith(name + ' is not defined')) {\n                        console.log('Send value to Observable that does not exist: ' + name);\n                        console.log(e);\n                        // TODO get this error into Python code? How do widget Python exceptions propagate?\n                    } else {\n                        throw e;\n                    }\n                }\n            }\n        }\n    });\n\n    // iframe is ready to start receiving 'inputs' messages\n    window.parent.postMessage({ type: 'ready', }, '*');\n    return main;\n};");

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

/***/ "./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js":
/*!****************************************************************************!*\
  !*** ./node_modules/style-loader/dist/runtime/injectStylesIntoStyleTag.js ***!
  \****************************************************************************/
/***/ ((module, __unused_webpack_exports, __webpack_require__) => {

"use strict";


var isOldIE = function isOldIE() {
  var memo;
  return function memorize() {
    if (typeof memo === 'undefined') {
      // Test for IE <= 9 as proposed by Browserhacks
      // @see http://browserhacks.com/#hack-e71d8692f65334173fee715c222cb805
      // Tests for existence of standard globals is to allow style-loader
      // to operate correctly into non-standard environments
      // @see https://github.com/webpack-contrib/style-loader/issues/177
      memo = Boolean(window && document && document.all && !window.atob);
    }

    return memo;
  };
}();

var getTarget = function getTarget() {
  var memo = {};
  return function memorize(target) {
    if (typeof memo[target] === 'undefined') {
      var styleTarget = document.querySelector(target); // Special case to return head of iframe instead of iframe itself

      if (window.HTMLIFrameElement && styleTarget instanceof window.HTMLIFrameElement) {
        try {
          // This will throw an exception if access to iframe is blocked
          // due to cross-origin restrictions
          styleTarget = styleTarget.contentDocument.head;
        } catch (e) {
          // istanbul ignore next
          styleTarget = null;
        }
      }

      memo[target] = styleTarget;
    }

    return memo[target];
  };
}();

var stylesInDom = [];

function getIndexByIdentifier(identifier) {
  var result = -1;

  for (var i = 0; i < stylesInDom.length; i++) {
    if (stylesInDom[i].identifier === identifier) {
      result = i;
      break;
    }
  }

  return result;
}

function modulesToDom(list, options) {
  var idCountMap = {};
  var identifiers = [];

  for (var i = 0; i < list.length; i++) {
    var item = list[i];
    var id = options.base ? item[0] + options.base : item[0];
    var count = idCountMap[id] || 0;
    var identifier = "".concat(id, " ").concat(count);
    idCountMap[id] = count + 1;
    var index = getIndexByIdentifier(identifier);
    var obj = {
      css: item[1],
      media: item[2],
      sourceMap: item[3]
    };

    if (index !== -1) {
      stylesInDom[index].references++;
      stylesInDom[index].updater(obj);
    } else {
      stylesInDom.push({
        identifier: identifier,
        updater: addStyle(obj, options),
        references: 1
      });
    }

    identifiers.push(identifier);
  }

  return identifiers;
}

function insertStyleElement(options) {
  var style = document.createElement('style');
  var attributes = options.attributes || {};

  if (typeof attributes.nonce === 'undefined') {
    var nonce =  true ? __webpack_require__.nc : 0;

    if (nonce) {
      attributes.nonce = nonce;
    }
  }

  Object.keys(attributes).forEach(function (key) {
    style.setAttribute(key, attributes[key]);
  });

  if (typeof options.insert === 'function') {
    options.insert(style);
  } else {
    var target = getTarget(options.insert || 'head');

    if (!target) {
      throw new Error("Couldn't find a style target. This probably means that the value for the 'insert' parameter is invalid.");
    }

    target.appendChild(style);
  }

  return style;
}

function removeStyleElement(style) {
  // istanbul ignore if
  if (style.parentNode === null) {
    return false;
  }

  style.parentNode.removeChild(style);
}
/* istanbul ignore next  */


var replaceText = function replaceText() {
  var textStore = [];
  return function replace(index, replacement) {
    textStore[index] = replacement;
    return textStore.filter(Boolean).join('\n');
  };
}();

function applyToSingletonTag(style, index, remove, obj) {
  var css = remove ? '' : obj.media ? "@media ".concat(obj.media, " {").concat(obj.css, "}") : obj.css; // For old IE

  /* istanbul ignore if  */

  if (style.styleSheet) {
    style.styleSheet.cssText = replaceText(index, css);
  } else {
    var cssNode = document.createTextNode(css);
    var childNodes = style.childNodes;

    if (childNodes[index]) {
      style.removeChild(childNodes[index]);
    }

    if (childNodes.length) {
      style.insertBefore(cssNode, childNodes[index]);
    } else {
      style.appendChild(cssNode);
    }
  }
}

function applyToTag(style, options, obj) {
  var css = obj.css;
  var media = obj.media;
  var sourceMap = obj.sourceMap;

  if (media) {
    style.setAttribute('media', media);
  } else {
    style.removeAttribute('media');
  }

  if (sourceMap && typeof btoa !== 'undefined') {
    css += "\n/*# sourceMappingURL=data:application/json;base64,".concat(btoa(unescape(encodeURIComponent(JSON.stringify(sourceMap)))), " */");
  } // For old IE

  /* istanbul ignore if  */


  if (style.styleSheet) {
    style.styleSheet.cssText = css;
  } else {
    while (style.firstChild) {
      style.removeChild(style.firstChild);
    }

    style.appendChild(document.createTextNode(css));
  }
}

var singleton = null;
var singletonCounter = 0;

function addStyle(obj, options) {
  var style;
  var update;
  var remove;

  if (options.singleton) {
    var styleIndex = singletonCounter++;
    style = singleton || (singleton = insertStyleElement(options));
    update = applyToSingletonTag.bind(null, style, styleIndex, false);
    remove = applyToSingletonTag.bind(null, style, styleIndex, true);
  } else {
    style = insertStyleElement(options);
    update = applyToTag.bind(null, style, options);

    remove = function remove() {
      removeStyleElement(style);
    };
  }

  update(obj);
  return function updateStyle(newObj) {
    if (newObj) {
      if (newObj.css === obj.css && newObj.media === obj.media && newObj.sourceMap === obj.sourceMap) {
        return;
      }

      update(obj = newObj);
    } else {
      remove();
    }
  };
}

module.exports = function (list, options) {
  options = options || {}; // Force single-tag solution on IE6-9, which has a hard limit on the # of <style>
  // tags it will allow on a page

  if (!options.singleton && typeof options.singleton !== 'boolean') {
    options.singleton = isOldIE();
  }

  list = list || [];
  var lastIdentifiers = modulesToDom(list, options);
  return function update(newList) {
    newList = newList || [];

    if (Object.prototype.toString.call(newList) !== '[object Array]') {
      return;
    }

    for (var i = 0; i < lastIdentifiers.length; i++) {
      var identifier = lastIdentifiers[i];
      var index = getIndexByIdentifier(identifier);
      stylesInDom[index].references--;
    }

    var newLastIdentifiers = modulesToDom(newList, options);

    for (var _i = 0; _i < lastIdentifiers.length; _i++) {
      var _identifier = lastIdentifiers[_i];

      var _index = getIndexByIdentifier(_identifier);

      if (stylesInDom[_index].references === 0) {
        stylesInDom[_index].updater();

        stylesInDom.splice(_index, 1);
      }
    }

    lastIdentifiers = newLastIdentifiers;
  };
};

/***/ }),

/***/ "./package.json":
/*!**********************!*\
  !*** ./package.json ***!
  \**********************/
/***/ ((module) => {

"use strict";
module.exports = JSON.parse('{"name":"observable-jupyter-widget","version":"0.1.1","description":"Connect Observable notebooks to the Jupyter kernel","keywords":["jupyter","jupyterlab","jupyterlab-extension","widgets"],"files":["lib/**/*.js","dist/*.js","css/*.css"],"homepage":"https://github.com/thomasballinger/observable-jupyter-widget","bugs":{"url":"https://github.com/thomasballinger/observable-jupyter-widget/issues"},"license":"BSD-3-Clause","author":{"name":"Thomas Ballinger","email":"me@ballingt.com"},"main":"lib/index.js","types":"./lib/index.d.ts","repository":{"type":"git","url":"https://github.com/thomasballinger/observable-jupyter-widget"},"scripts":{"build":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension:dev","build:prod":"yarn run build:lib && yarn run build:nbextension && yarn run build:labextension","build:labextension":"jupyter labextension build .","build:labextension:dev":"jupyter labextension build --development True .","build:lib":"tsc","build:nbextension":"webpack","clean":"yarn run clean:lib && yarn run clean:nbextension && yarn run clean:labextension","clean:lib":"rimraf lib","clean:labextension":"rimraf observable_jupyter_widget/labextension","clean:nbextension":"rimraf observable_jupyter_widget/nbextension/static/index.js","lint":"eslint . --ext .ts,.tsx --fix","lint:check":"eslint . --ext .ts,.tsx","prepack":"yarn run build:lib","test":"jest","watch":"npm-run-all -p watch:*","watch:lib":"tsc -w","watch:nbextension":"webpack --watch --mode=development","watch:labextension":"jupyter labextension watch ."},"dependencies":{"@jupyter-widgets/base":"^1.1.10 || ^2.0.0 || ^3.0.0 || ^4.0.0","@observablehq/runtime":"^4.18.0","raw-loader":"^4.0.2"},"devDependencies":{"@babel/core":"^7.5.0","@babel/preset-env":"^7.5.0","@jupyterlab/builder":"^3.0.0","@phosphor/application":"^1.6.0","@phosphor/widgets":"^1.6.0","@types/jest":"^26.0.0","@types/webpack-env":"^1.13.6","@typescript-eslint/eslint-plugin":"^3.6.0","@typescript-eslint/parser":"^3.6.0","acorn":"^7.2.0","css-loader":"^3.2.0","eslint":"^7.4.0","eslint-config-prettier":"^6.11.0","eslint-plugin-prettier":"^3.1.4","fs-extra":"^7.0.0","identity-obj-proxy":"^3.0.0","jest":"^26.0.0","mkdirp":"^0.5.1","npm-run-all":"^4.1.3","prettier":"^2.0.5","rimraf":"^2.6.2","source-map-loader":"^1.1.3","style-loader":"^1.0.0","ts-jest":"^26.0.0","ts-loader":"^8.0.0","typescript":"~4.1.3","webpack":"^5.0.0","webpack-cli":"^4.0.0"},"jupyterlab":{"extension":"lib/plugin","outputDir":"observable_jupyter_widget/labextension/","sharedPackages":{"@jupyter-widgets/base":{"bundled":false,"singleton":true}}}}');

/***/ })

}]);
//# sourceMappingURL=lib_widget_js.20138f10b4dcd5744305.js.map