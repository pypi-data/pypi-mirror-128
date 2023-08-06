"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[72868],{72868:(e,t,i)=>{i.r(t);i(53918),i(30879);var r=i(37500),n=i(26767),o=i(5701),s=i(17717),a=i(67352),l=i(47181),c=(i(31206),i(83270)),d=i(11654),u=i(58831);const h=(e,t,i)=>{if(1!==t.length)return e[t[0]]||(e[t[0]]={}),h(e[t[0]],t.slice(1),i);e[t[0]]=i},p=(e,t)=>1===t.length?e[t[0]]:void 0!==e[t[0]]?p(e[t[0]],t.slice(1)):void 0;i(53973),i(89194),i(51095),i(33076);var f=i(25209),m=i(14516),v=i(85415),y=i(57066),k=i(57292),g=i(74186),b=i(73826);i(10983),i(52039),i(60033);function _(){_=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!D(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return C(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?C(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=P(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:x(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=x(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function w(e){var t,i=P(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function E(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function D(e){return e.decorators&&e.decorators.length}function $(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function x(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function P(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function C(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=_();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if($(o.descriptor)||$(n.descriptor)){if(D(o)||D(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(D(o)){if(D(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}E(o,n)}else t.push(o)}return t}(s.d.map(w)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-devices-picker")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,o.C)({attribute:"picked-device-label"}),(0,o.C)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",key:"pickedDeviceLabel",value:void 0},{kind:"field",decorators:[(0,o.C)({attribute:"pick-device-label"})],key:"pickDeviceLabel",value:void 0},{kind:"method",key:"render",value:function(){if(!this.hass)return r.dy``;const e=this._currentDevices;return r.dy`
      ${e.map((e=>r.dy`
          <div>
            <ha-device-picker
              allow-custom-entity
              .curValue=${e}
              .hass=${this.hass}
              .includeDomains=${this.includeDomains}
              .excludeDomains=${this.excludeDomains}
              .includeDeviceClasses=${this.includeDeviceClasses}
              .value=${e}
              .label=${this.pickedDeviceLabel}
              @value-changed=${this._deviceChanged}
            ></ha-device-picker>
          </div>
        `))}
      <div>
        <ha-device-picker
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .excludeDomains=${this.excludeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .label=${this.pickDeviceLabel}
          @value-changed=${this._addDevice}
        ></ha-device-picker>
      </div>
    `}},{kind:"get",key:"_currentDevices",value:function(){return this.value||[]}},{kind:"method",key:"_updateDevices",value:async function(e){(0,l.B)(this,"value-changed",{value:e}),this.value=e}},{kind:"method",key:"_deviceChanged",value:function(e){e.stopPropagation();const t=e.currentTarget.curValue,i=e.detail.value;i!==t&&""===i&&(""===i?this._updateDevices(this._currentDevices.filter((e=>e!==t))):this._updateDevices(this._currentDevices.map((e=>e===t?i:e))))}},{kind:"method",key:"_addDevice",value:async function(e){e.stopPropagation();const t=e.detail.value;if(e.currentTarget.value="",!t)return;const i=this._currentDevices;i.includes(t)||this._updateDevices([...i,t])}}]}}),r.oi);function A(){A=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!T(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return I(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?I(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=L(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:j(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=j(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function S(e){var t,i=L(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function z(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function T(e){return e.decorators&&e.decorators.length}function O(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function j(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function L(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function I(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function F(e,t,i){return F="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=V(e)););return e}(e,t);if(r){var n=Object.getOwnPropertyDescriptor(r,t);return n.get?n.get.call(i):n.value}},F(e,t,i||e)}function V(e){return V=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},V(e)}const M=e=>r.dy`<style>
    paper-item {
      padding: 0;
      margin: -10px;
      margin-left: 0;
    }
    #content {
      display: flex;
      align-items: center;
    }
    ha-svg-icon {
      padding-left: 2px;
      margin-right: -2px;
      color: var(--secondary-text-color);
    }
    :host(:not([selected])) ha-svg-icon {
      display: none;
    }
    :host([selected]) paper-item {
      margin-left: 10px;
    }
  </style>
  <ha-svg-icon .path=${"M21,7L9,19L3.5,13.5L4.91,12.09L9,16.17L19.59,5.59L21,7Z"}></ha-svg-icon>
  <paper-item>
    <paper-item-body two-line="">
      <div class="name">${e.name}</div>
      <div secondary>${e.devices.length} devices</div>
    </paper-item-body>
  </paper-item>`;!function(e,t,i,r){var n=A();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(O(o.descriptor)||O(n.descriptor)){if(T(o)||T(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(T(o)){if(T(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}z(o,n)}else t.push(o)}return t}(s.d.map(S)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-area-devices-picker")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"label",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"value",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"area",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"devices",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Array,attribute:"include-domains"})],key:"includeDomains",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Array,attribute:"exclude-domains"})],key:"excludeDomains",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Array,attribute:"include-device-classes"})],key:"includeDeviceClasses",value:void 0},{kind:"field",decorators:[(0,o.C)({type:Boolean})],key:"_opened",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_areaPicker",value:()=>!0},{kind:"field",decorators:[(0,s.S)()],key:"_devices",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_areas",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_entities",value:void 0},{kind:"field",key:"_selectedDevices",value:()=>[]},{kind:"field",key:"_filteredDevices",value:()=>[]},{kind:"field",key:"_getAreasWithDevices",value(){return(0,m.Z)(((e,t,i,r,n,o)=>{if(!e.length)return[];const s={};for(const e of i)e.device_id&&(e.device_id in s||(s[e.device_id]=[]),s[e.device_id].push(e));let a=[...e];r&&(a=a.filter((e=>{const t=s[e.id];return!(!t||!t.length)&&s[e.id].some((e=>r.includes((0,u.M)(e.entity_id))))}))),n&&(a=a.filter((e=>{const t=s[e.id];return!t||!t.length||i.every((e=>!n.includes((0,u.M)(e.entity_id))))}))),o&&(a=a.filter((e=>{const t=s[e.id];return!(!t||!t.length)&&s[e.id].some((e=>{const t=this.hass.states[e.entity_id];return!!t&&(t.attributes.device_class&&o.includes(t.attributes.device_class))}))}))),this._filteredDevices=a;const l={};for(const e of t)l[e.area_id]=e;const c={};for(const e of a){const t=e.area_id;t&&(t in c||(c[t]={id:t,name:l[t].name,devices:[]}),c[t].devices.push(e.id))}return Object.keys(c).sort(((e,t)=>(0,v.$)(c[e].name||"",c[t].name||""))).map((e=>c[e]))}))}},{kind:"method",key:"hassSubscribe",value:function(){return[(0,k.q4)(this.hass.connection,(e=>{this._devices=e})),(0,y.sG)(this.hass.connection,(e=>{this._areas=e})),(0,g.LM)(this.hass.connection,(e=>{this._entities=e}))]}},{kind:"method",key:"updated",value:function(e){if(F(V(i.prototype),"updated",this).call(this,e),e.has("area")&&this.area)this._areaPicker=!0,this.value=this.area;else if(e.has("devices")&&this.devices){this._areaPicker=!1;const e=this._filteredDevices.map((e=>e.id)),t=this.devices.filter((t=>e.includes(t)));this._setValue(t)}}},{kind:"method",key:"render",value:function(){if(!this._devices||!this._areas||!this._entities)return r.dy``;const e=this._getAreasWithDevices(this._devices,this._areas,this._entities,this.includeDomains,this.excludeDomains,this.includeDeviceClasses);return this._areaPicker&&0!==e.length?r.dy`
      <vaadin-combo-box-light
        item-value-path="id"
        item-id-path="id"
        item-label-path="name"
        .items=${e}
        .value=${this._value}
        ${(0,f.t7)(M)}
        @opened-changed=${this._openedChanged}
        @value-changed=${this._areaPicked}
      >
        <paper-input
          .label=${void 0===this.label&&this.hass?this.hass.localize("ui.components.device-picker.device"):`${this.label} in area`}
          class="input"
          autocapitalize="none"
          autocomplete="off"
          autocorrect="off"
          spellcheck="false"
        >
          <div class="suffix" slot="suffix">
            ${this.value?r.dy`<ha-icon-button
                  class="clear-button"
                  .label=${this.hass.localize("ui.components.device-picker.clear")}
                  .path=${"M19,6.41L17.59,5L12,10.59L6.41,5L5,6.41L10.59,12L5,17.59L6.41,19L12,13.41L17.59,19L19,17.59L13.41,12L19,6.41Z"}
                  @click=${this._clearValue}
                  no-ripple
                ></ha-icon-button> `:""}
            ${e.length>0?r.dy`
                  <ha-icon-button
                    .label=${this.hass.localize("ui.components.device-picker.show_devices")}
                    .path=${this._opened?"M7,15L12,10L17,15H7Z":"M7,10L12,15L17,10H7Z"}
                    class="toggle-button"
                  ></ha-icon-button>
                `:""}
          </div>
        </paper-input>
      </vaadin-combo-box-light>
      <mwc-button @click=${this._switchPicker}
        >Choose individual devices</mwc-button
      >
    `:r.dy`
        <ha-devices-picker
          @value-changed=${this._devicesPicked}
          .hass=${this.hass}
          .includeDomains=${this.includeDomains}
          .includeDeviceClasses=${this.includeDeviceClasses}
          .value=${this._selectedDevices}
          .pickDeviceLabel=${`Add ${this.label} device`}
          .pickedDeviceLabel=${`${this.label} device`}
        ></ha-devices-picker>
        ${e.length>0?r.dy`
              <mwc-button @click=${this._switchPicker}
                >Choose an area</mwc-button
              >
            `:""}
      `}},{kind:"method",key:"_clearValue",value:function(e){e.stopPropagation(),this._setValue([])}},{kind:"get",key:"_value",value:function(){return this.value||[]}},{kind:"method",key:"_openedChanged",value:function(e){this._opened=e.detail.value}},{kind:"method",key:"_switchPicker",value:async function(){this._areaPicker=!this._areaPicker}},{kind:"method",key:"_areaPicked",value:async function(e){const t=e.detail.value;let i=[];const r=e.target;r.selectedItem&&(i=r.selectedItem.devices),t===this._value&&this._selectedDevices===i||this._setValue(i,t)}},{kind:"method",key:"_devicesPicked",value:function(e){e.stopPropagation();const t=e.detail.value;this._setValue(t)}},{kind:"method",key:"_setValue",value:function(e,t=""){this.value=t,this._selectedDevices=e,setTimeout((()=>{(0,l.B)(this,"value-changed",{value:e}),(0,l.B)(this,"change")}),0)}},{kind:"get",static:!0,key:"styles",value:function(){return r.iv`
      .suffix {
        display: flex;
      }
      ha-icon-button {
        --mdc-icon-button-size: 24px;
        padding: 0px 2px;
        color: var(--secondary-text-color);
      }
      [hidden] {
        display: none;
      }
    `}}]}}),(0,b.f)(r.oi));i(74535);var N=i(5986);function U(){U=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!B(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return H(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?H(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=G(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:W(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=W(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function R(e){var t,i=G(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function q(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function B(e){return e.decorators&&e.decorators.length}function Z(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function W(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function G(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function H(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=U();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(Z(o.descriptor)||Z(n.descriptor)){if(B(o)||B(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(B(o)){if(B(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}q(o,n)}else t.push(o)}return t}(s.d.map(R)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-thingtalk-placeholders")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"opened",value:void 0},{kind:"field",key:"skip",value:void 0},{kind:"field",decorators:[(0,o.C)()],key:"placeholders",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_error",value:void 0},{kind:"field",key:"_deviceEntityLookup",value:()=>({})},{kind:"field",decorators:[(0,s.S)()],key:"_extraInfo",value:()=>({})},{kind:"field",decorators:[(0,s.S)()],key:"_placeholderValues",value:()=>({})},{kind:"field",key:"_devices",value:void 0},{kind:"field",key:"_areas",value:void 0},{kind:"field",key:"_search",value:()=>!1},{kind:"method",key:"hassSubscribe",value:function(){return[(0,g.LM)(this.hass.connection,(e=>{for(const t of e)t.device_id&&(t.device_id in this._deviceEntityLookup||(this._deviceEntityLookup[t.device_id]=[]),this._deviceEntityLookup[t.device_id].includes(t.entity_id)||this._deviceEntityLookup[t.device_id].push(t.entity_id))})),(0,k.q4)(this.hass.connection,(e=>{this._devices=e,this._searchNames()})),(0,y.sG)(this.hass.connection,(e=>{this._areas=e,this._searchNames()}))]}},{kind:"method",key:"updated",value:function(e){e.has("placeholders")&&(this._search=!0,this._searchNames())}},{kind:"method",key:"render",value:function(){return r.dy`
      <ha-dialog
        open
        scrimClickAction
        .heading=${this.hass.localize("ui.panel.config.automation.thingtalk.link_devices.header")}
      >
        <div>
          ${this._error?r.dy` <div class="error">${this._error}</div> `:""}
          ${Object.entries(this.placeholders).map((([e,t])=>r.dy`
                <h3>
                  ${this.hass.localize(`ui.panel.config.automation.editor.${e}s.name`)}:
                </h3>
                ${t.map((t=>{if(t.fields.includes("device_id")){const i=p(this._extraInfo,[e,t.index]);return r.dy`
                      <ha-area-devices-picker
                        .type=${e}
                        .placeholder=${t}
                        @value-changed=${this._devicePicked}
                        .hass=${this.hass}
                        .area=${i?i.area_id:void 0}
                        .devices=${i&&i.device_ids?i.device_ids:void 0}
                        .includeDomains=${t.domains}
                        .includeDeviceClasses=${t.device_classes}
                        .label=${this._getLabel(t.domains,t.device_classes)}
                      ></ha-area-devices-picker>
                      ${i&&i.manualEntity?r.dy`
                            <h3>
                              ${this.hass.localize("ui.panel.config.automation.thingtalk.link_devices.ambiguous_entities")}
                            </h3>
                            ${Object.keys(i.manualEntity).map((i=>r.dy`
                                <ha-entity-picker
                                  id="device-entity-picker"
                                  .type=${e}
                                  .placeholder=${t}
                                  .index=${i}
                                  @change=${this._entityPicked}
                                  .includeDomains=${t.domains}
                                  .includeDeviceClasses=${t.device_classes}
                                  .hass=${this.hass}
                                  .label=${`${this._getLabel(t.domains,t.device_classes)} of device ${this._getDeviceName(p(this._placeholderValues,[e,t.index,i,"device_id"]))}`}
                                  .entityFilter=${r=>{const n=this._placeholderValues[e][t.index][i].device_id;return this._deviceEntityLookup[n].includes(r.entity_id)}}
                                ></ha-entity-picker>
                              `))}
                          `:""}
                    `}return t.fields.includes("entity_id")?r.dy`
                      <ha-entity-picker
                        .type=${e}
                        .placeholder=${t}
                        @change=${this._entityPicked}
                        .includeDomains=${t.domains}
                        .includeDeviceClasses=${t.device_classes}
                        .hass=${this.hass}
                        .label=${this._getLabel(t.domains,t.device_classes)}
                      ></ha-entity-picker>
                    `:r.dy`
                    <div class="error">
                      ${this.hass.localize("ui.panel.config.automation.thingtalk.link_devices.unknown_placeholder")}<br />
                      ${t.domains}<br />
                      ${t.fields.map((e=>r.dy` ${e}<br /> `))}
                    </div>
                  `}))}
              `))}
        </div>
        <mwc-button @click=${this.skip} slot="secondaryAction">
          ${this.hass.localize("ui.common.skip")}
        </mwc-button>
        <mwc-button
          @click=${this._done}
          .disabled=${!this._isDone}
          slot="primaryAction"
        >
          ${this.hass.localize("ui.panel.config.automation.thingtalk.create")}
        </mwc-button>
      </ha-dialog>
    `}},{kind:"method",key:"_getDeviceName",value:function(e){if(!this._devices)return"";const t=this._devices.find((t=>t.id===e));return t&&(t.name_by_user||t.name)||""}},{kind:"method",key:"_searchNames",value:function(){this._search&&this._areas&&this._devices&&(this._search=!1,Object.entries(this.placeholders).forEach((([e,t])=>t.forEach((t=>{if(!t.name)return;const i=t.name,r=this._areas.find((e=>e.name.toLowerCase().includes(i)));if(r)return h(this._extraInfo,[e,t.index,"area_id"],r.area_id),void this.requestUpdate("_extraInfo");const n=this._devices.filter((e=>{const t=e.name_by_user||e.name;return!!t&&t.toLowerCase().includes(i)}));n.length&&(h(this._extraInfo,[e,t.index,"device_ids"],n.map((e=>e.id))),this.requestUpdate("_extraInfo"))})))))}},{kind:"get",key:"_isDone",value:function(){return Object.entries(this.placeholders).every((([e,t])=>t.every((t=>t.fields.every((i=>{const r=p(this._placeholderValues,[e,t.index]);if(!r)return!1;return Object.values(r).every((e=>void 0!==e[i]&&""!==e[i]))}))))))}},{kind:"method",key:"_getLabel",value:function(e,t){return`${e.map((e=>(0,N.Lh)(this.hass.localize,e))).join(", ")}${t?` of type ${t.join(", ")}`:""}`}},{kind:"method",key:"_devicePicked",value:function(e){const t=e.detail.value;if(!t)return;const i=e.target,r=i.placeholder,n=i.type;let o=p(this._placeholderValues,[n,r.index]);o&&(o=Object.values(o));const s=p(this._extraInfo,[n,r.index]);this._placeholderValues[n]&&delete this._placeholderValues[n][r.index],this._extraInfo[n]&&delete this._extraInfo[n][r.index],t.length?t.forEach(((e,t)=>{let i;if(o){const a=o.find(((t,r)=>(i=r,t.device_id===e)));if(a)return h(this._placeholderValues,[n,r.index,t],a),void(s&&h(this._extraInfo,[n,r.index,t],s[i]))}if(h(this._placeholderValues,[n,r.index,t,"device_id"],e),!r.fields.includes("entity_id"))return;const a=this._deviceEntityLookup[e].filter((e=>{if(r.device_classes){const t=this.hass.states[e];return!!t&&(r.domains.includes((0,u.M)(e))&&t.attributes.device_class&&r.device_classes.includes(t.attributes.device_class))}return r.domains.includes((0,u.M)(e))}));0===a.length?this._error=`No ${r.domains.map((e=>(0,N.Lh)(this.hass.localize,e))).join(", ")} entities found in this device.`:1===a.length?(h(this._placeholderValues,[n,r.index,t,"entity_id"],a[0]),this.requestUpdate("_placeholderValues")):(delete this._placeholderValues[n][r.index][t].entity_id,h(this._extraInfo,[n,r.index,"manualEntity",t],!0),this.requestUpdate("_placeholderValues"))})):this.requestUpdate("_placeholderValues")}},{kind:"method",key:"_entityPicked",value:function(e){const t=e.target,i=t.placeholder,r=t.value,n=t.type,o=t.index||0;h(this._placeholderValues,[n,i.index,o,"entity_id"],r),this.requestUpdate("_placeholderValues")}},{kind:"method",key:"_done",value:function(){(0,l.B)(this,"placeholders-filled",{value:this._placeholderValues})}},{kind:"get",static:!0,key:"styles",value:function(){return[d.yu,r.iv`
        ha-dialog {
          max-width: 500px;
        }
        mwc-button.left {
          margin-right: auto;
        }
        h3 {
          margin: 10px 0 0 0;
          font-weight: 500;
        }
        .error {
          color: var(--error-color);
        }
      `]}}]}}),(0,b.f)(r.oi));i(34821);function K(){K=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var n=t.placement;if(t.kind===r&&("static"===n||"prototype"===n)){var o="static"===n?e:i;this.defineClassElement(o,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],n={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,n)}),this),e.forEach((function(e){if(!X(e))return i.push(e);var t=this.decorateElement(e,n);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var o=this.decorateConstructor(i,t);return r.push.apply(r,o.finishers),o.finishers=r,o},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],n=e.decorators,o=n.length-1;o>=0;o--){var s=t[e.placement];s.splice(s.indexOf(e.key),1);var a=this.fromElementDescriptor(e),l=this.toElementFinisherExtras((0,n[o])(a)||a);e=l.element,this.addElementPlacement(e,t),l.finisher&&r.push(l.finisher);var c=l.extras;if(c){for(var d=0;d<c.length;d++)this.addElementPlacement(c[d],t);i.push.apply(i,c)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var n=this.fromClassDescriptor(e),o=this.toClassDescriptor((0,t[r])(n)||n);if(void 0!==o.finisher&&i.push(o.finisher),void 0!==o.elements){e=o.elements;for(var s=0;s<e.length-1;s++)for(var a=s+1;a<e.length;a++)if(e[s].key===e[a].key&&e[s].placement===e[a].placement)throw new TypeError("Duplicated element ("+e[s].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return ie(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?ie(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=te(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var n=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var o={kind:t,key:i,placement:r,descriptor:Object.assign({},n)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(n,"get","The property descriptor of a field descriptor"),this.disallowProperty(n,"set","The property descriptor of a field descriptor"),this.disallowProperty(n,"value","The property descriptor of a field descriptor"),o.initializer=e.initializer),o},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:ee(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=ee(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function Q(e){var t,i=te(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function J(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function X(e){return e.decorators&&e.decorators.length}function Y(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function ee(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function te(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function ie(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}!function(e,t,i,r){var n=K();if(r)for(var o=0;o<r.length;o++)n=r[o](n);var s=t((function(e){n.initializeInstanceElements(e,a.elements)}),i),a=n.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===o.key&&e.placement===o.placement},r=0;r<e.length;r++){var n,o=e[r];if("method"===o.kind&&(n=t.find(i)))if(Y(o.descriptor)||Y(n.descriptor)){if(X(o)||X(n))throw new ReferenceError("Duplicated methods ("+o.key+") can't be decorated.");n.descriptor=o.descriptor}else{if(X(o)){if(X(n))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+o.key+").");n.decorators=o.decorators}J(o,n)}else t.push(o)}return t}(s.d.map(Q)),e);n.initializeClassElements(s.F,a.elements),n.runClassFinishers(s.F,a.finishers)}([(0,n.M)("ha-dialog-thinktalk")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,o.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_error",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_params",value:void 0},{kind:"field",decorators:[(0,s.S)()],key:"_submitting",value:()=>!1},{kind:"field",decorators:[(0,s.S)()],key:"_placeholders",value:void 0},{kind:"field",decorators:[(0,a.I)("#input")],key:"_input",value:void 0},{kind:"field",key:"_value",value:void 0},{kind:"field",key:"_config",value:void 0},{kind:"method",key:"showDialog",value:async function(e){this._params=e,this._error=void 0,e.input&&(this._value=e.input,await this.updateComplete,this._generate())}},{kind:"method",key:"closeDialog",value:function(){this._placeholders=void 0,this._params=void 0,this._input&&(this._input.value=null),(0,l.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"closeInitDialog",value:function(){this._placeholders||this.closeDialog()}},{kind:"method",key:"render",value:function(){return this._params?this._placeholders?r.dy`
        <ha-thingtalk-placeholders
          .hass=${this.hass}
          .placeholders=${this._placeholders}
          .skip=${this._skip}
          @closed=${this.closeDialog}
          @placeholders-filled=${this._handlePlaceholders}
        >
        </ha-thingtalk-placeholders>
      `:r.dy`
      <ha-dialog
        open
        @closed=${this.closeInitDialog}
        .heading=${this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.header")}
      >
        <div>
          ${this._error?r.dy` <div class="error">${this._error}</div> `:""}
          ${this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.introduction")}<br /><br />
          ${this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.language_note")}<br /><br />
          ${this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.for_example")}
          <ul @click=${this._handleExampleClick}>
            <li>
              <button class="link">
                Turn off the lights when I leave home
              </button>
            </li>
            <li>
              <button class="link">
                Turn on the lights when the sun is set
              </button>
            </li>
            <li>
              <button class="link">
                Notify me if the door opens and I am not at home
              </button>
            </li>
            <li>
              <button class="link">
                Turn the light on when motion is detected
              </button>
            </li>
          </ul>
          <paper-input
            id="input"
            label="What should this automation do?"
            .value=${this._value}
            autofocus
            @keyup=${this._handleKeyUp}
          ></paper-input>
          <a
            href="https://almond.stanford.edu/"
            target="_blank"
            rel="noreferrer"
            class="attribution"
            >Powered by Almond</a
          >
        </div>
        <mwc-button class="left" @click=${this._skip} slot="secondaryAction">
          ${this.hass.localize("ui.common.skip")}
        </mwc-button>
        <mwc-button
          @click=${this._generate}
          .disabled=${this._submitting}
          slot="primaryAction"
        >
          ${this._submitting?r.dy`<ha-circular-progress
                active
                size="small"
                title="Creating your automation..."
              ></ha-circular-progress>`:""}
          ${this.hass.localize("ui.panel.config.automation.thingtalk.create")}
        </mwc-button>
      </ha-dialog>
    `:r.dy``}},{kind:"method",key:"_generate",value:async function(){if(this._value=this._input.value,!this._value)return void(this._error=this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.error_empty"));let e,t;this._submitting=!0;try{const i=await(0,c.Wz)(this.hass,this._value);e=i.config,t=i.placeholders}catch(e){return this._error=e.message,void(this._submitting=!1)}this._submitting=!1,Object.keys(e).length?Object.keys(t).length?(this._config=e,this._placeholders=t):this._sendConfig(this._value,e):this._error=this.hass.localize("ui.panel.config.automation.thingtalk.task_selection.error_unsupported")}},{kind:"method",key:"_handlePlaceholders",value:function(e){const t=e.detail.value;Object.entries(t).forEach((([e,t])=>{Object.entries(t).forEach((([t,i])=>{const r=Object.values(i);if(1===r.length)return void Object.entries(r[0]).forEach((([i,r])=>{this._config[e][t][i]=r}));const n={...this._config[e][t]},o=[];r.forEach((e=>{const t={...n};Object.entries(e).forEach((([e,i])=>{t[e]=i})),o.push(t)})),this._config[e].splice(t,1,...o)}))})),this._sendConfig(this._value,this._config)}},{kind:"method",key:"_sendConfig",value:function(e,t){this._params.callback({alias:e,...t}),this.closeDialog()}},{kind:"field",key:"_skip",value(){return()=>{this._params.callback(void 0),this.closeDialog()}}},{kind:"method",key:"_handleKeyUp",value:function(e){13===e.keyCode&&this._generate()}},{kind:"method",key:"_handleExampleClick",value:function(e){this._input.value=e.target.innerText}},{kind:"get",static:!0,key:"styles",value:function(){return[d.Qx,d.yu,r.iv`
        ha-dialog {
          max-width: 500px;
        }
        mwc-button.left {
          margin-right: auto;
        }
        .error {
          color: var(--error-color);
        }
        .attribution {
          color: var(--secondary-text-color);
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=34fe0634.js.map