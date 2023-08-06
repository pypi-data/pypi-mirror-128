/*! For license information please see 701f207f.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[70453],{39841:(e,t,n)=>{n(94604),n(65660);var r=n(9672),a=n(87156),o=n(50856),i=n(44181);(0,r.k)({_template:o.d`
    <style>
      :host {
        display: block;
        /**
         * Force app-header-layout to have its own stacking context so that its parent can
         * control the stacking of it relative to other elements (e.g. app-drawer-layout).
         * This could be done using \`isolation: isolate\`, but that's not well supported
         * across browsers.
         */
        position: relative;
        z-index: 0;
      }

      #wrapper ::slotted([slot=header]) {
        @apply --layout-fixed-top;
        z-index: 1;
      }

      #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) {
        height: 100%;
      }

      :host([has-scrolling-region]) #wrapper ::slotted([slot=header]) {
        position: absolute;
      }

      :host([has-scrolling-region]) #wrapper.initializing ::slotted([slot=header]) {
        position: relative;
      }

      :host([has-scrolling-region]) #wrapper #contentContainer {
        @apply --layout-fit;
        overflow-y: auto;
        -webkit-overflow-scrolling: touch;
      }

      :host([has-scrolling-region]) #wrapper.initializing #contentContainer {
        position: relative;
      }

      :host([fullbleed]) {
        @apply --layout-vertical;
        @apply --layout-fit;
      }

      :host([fullbleed]) #wrapper,
      :host([fullbleed]) #wrapper #contentContainer {
        @apply --layout-vertical;
        @apply --layout-flex;
      }

      #contentContainer {
        /* Create a stacking context here so that all children appear below the header. */
        position: relative;
        z-index: 0;
      }

      @media print {
        :host([has-scrolling-region]) #wrapper #contentContainer {
          overflow-y: visible;
        }
      }

    </style>

    <div id="wrapper" class="initializing">
      <slot id="headerSlot" name="header"></slot>

      <div id="contentContainer">
        <slot></slot>
      </div>
    </div>
`,is:"app-header-layout",behaviors:[i.Y],properties:{hasScrollingRegion:{type:Boolean,value:!1,reflectToAttribute:!0}},observers:["resetLayout(isAttached, hasScrollingRegion)"],get header(){return(0,a.vz)(this.$.headerSlot).getDistributedNodes()[0]},_updateLayoutStates:function(){var e=this.header;if(this.isAttached&&e){this.$.wrapper.classList.remove("initializing"),e.scrollTarget=this.hasScrollingRegion?this.$.contentContainer:this.ownerDocument.documentElement;var t=e.offsetHeight;this.hasScrollingRegion?(e.style.left="",e.style.right=""):requestAnimationFrame(function(){var t=this.getBoundingClientRect(),n=document.documentElement.clientWidth-t.right;e.style.left=t.left+"px",e.style.right=n+"px"}.bind(this));var n=this.$.contentContainer.style;e.fixed&&!e.condenses&&this.hasScrollingRegion?(n.marginTop=t+"px",n.paddingTop=""):(n.paddingTop=t+"px",n.marginTop="")}}})},23682:(e,t,n)=>{function r(e,t){if(t.length<e)throw new TypeError(e+" argument"+(e>1?"s":"")+" required, but only "+t.length+" present")}n.d(t,{Z:()=>r})},90394:(e,t,n)=>{function r(e){if(null===e||!0===e||!1===e)return NaN;var t=Number(e);return isNaN(t)?t:t<0?Math.ceil(t):Math.floor(t)}n.d(t,{Z:()=>r})},79021:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(90394),a=n(34327),o=n(23682);function i(e,t){(0,o.Z)(2,arguments);var n=(0,a.Z)(e),i=(0,r.Z)(t);return isNaN(i)?new Date(NaN):i?(n.setDate(n.getDate()+i),n):n}},32182:(e,t,n)=>{n.d(t,{Z:()=>i});var r=n(90394),a=n(34327),o=n(23682);function i(e,t){(0,o.Z)(2,arguments);var n=(0,a.Z)(e),i=(0,r.Z)(t);if(isNaN(i))return new Date(NaN);if(!i)return n;var s=n.getDate(),l=new Date(n.getTime());l.setMonth(n.getMonth()+i+1,0);var u=l.getDate();return s>=u?l:(n.setFullYear(l.getFullYear(),l.getMonth(),s),n)}},70390:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(93752);function a(){return(0,r.Z)(Date.now())}},47538:(e,t,n)=>{function r(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),r=e.getDate(),a=new Date(0);return a.setFullYear(t,n,r-1),a.setHours(23,59,59,999),a}n.d(t,{Z:()=>r})},82045:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(34327),a=n(23682);function o(e,t){(0,a.Z)(2,arguments);var n=(0,r.Z)(e).getTime(),o=(0,r.Z)(t.start).getTime(),i=(0,r.Z)(t.end).getTime();if(!(o<=i))throw new RangeError("Invalid interval");return n>=o&&n<=i}},59429:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(34327),a=n(23682);function o(e){(0,a.Z)(1,arguments);var t=(0,r.Z)(e);return t.setHours(0,0,0,0),t}},13250:(e,t,n)=>{n.d(t,{Z:()=>o});var r=n(34327),a=n(23682);function o(e){(0,a.Z)(1,arguments);var t=(0,r.Z)(e);return t.setDate(1),t.setHours(0,0,0,0),t}},27088:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(59429);function a(){return(0,r.Z)(Date.now())}},83008:(e,t,n)=>{function r(){var e=new Date,t=e.getFullYear(),n=e.getMonth(),r=e.getDate(),a=new Date(0);return a.setFullYear(t,n,r-1),a.setHours(0,0,0,0),a}n.d(t,{Z:()=>r})},34327:(e,t,n)=>{n.d(t,{Z:()=>a});var r=n(23682);function a(e){(0,r.Z)(1,arguments);var t=Object.prototype.toString.call(e);return e instanceof Date||"object"==typeof e&&"[object Date]"===t?new Date(e.getTime()):"number"==typeof e||"[object Number]"===t?new Date(e):("string"!=typeof e&&"[object String]"!==t||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}}}]);
//# sourceMappingURL=701f207f.js.map