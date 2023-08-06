/*! For license information please see d3958b71.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[87217,49995,93098,11139,5713,22946,92887],{18601:(e,t,o)=>{o.d(t,{qN:()=>s.q,Wg:()=>d});var n,i,r=o(87480),a=o(5701),s=o(78220);const l=null!==(i=null===(n=window.ShadyDOM)||void 0===n?void 0:n.inUse)&&void 0!==i&&i;class d extends s.H{constructor(){super(...arguments),this.disabled=!1,this.containingForm=null,this.formDataListener=e=>{this.disabled||this.setFormData(e.formData)}}findFormElement(){if(!this.shadowRoot||l)return null;const e=this.getRootNode().querySelectorAll("form");for(const t of Array.from(e))if(t.contains(this))return t;return null}connectedCallback(){var e;super.connectedCallback(),this.containingForm=this.findFormElement(),null===(e=this.containingForm)||void 0===e||e.addEventListener("formdata",this.formDataListener)}disconnectedCallback(){var e;super.disconnectedCallback(),null===(e=this.containingForm)||void 0===e||e.removeEventListener("formdata",this.formDataListener),this.containingForm=null}click(){this.formElement&&!this.disabled&&(this.formElement.focus(),this.formElement.click())}firstUpdated(){super.firstUpdated(),this.shadowRoot&&this.mdcRoot.addEventListener("change",(e=>{this.dispatchEvent(new Event("change",e))}))}}d.shadowRootOptions={mode:"open",delegatesFocus:!0},(0,r.__decorate)([(0,a.C)({type:Boolean})],d.prototype,"disabled",void 0)},14114:(e,t,o)=>{o.d(t,{P:()=>n});const n=e=>(t,o)=>{if(t.constructor._observers){if(!t.constructor.hasOwnProperty("_observers")){const e=t.constructor._observers;t.constructor._observers=new Map,e.forEach(((e,o)=>t.constructor._observers.set(o,e)))}}else{t.constructor._observers=new Map;const e=t.updated;t.updated=function(t){e.call(this,t),t.forEach(((e,t)=>{const o=this.constructor._observers.get(t);void 0!==o&&o.call(this,this[t],e)}))}}t.constructor._observers.set(o,e)}},8878:(e,t,o)=>{o(65233),o(8621),o(63207),o(30879),o(78814),o(60748),o(57548),o(73962);var n=o(51644),i=o(26110),r=o(21006),a=o(98235),s=o(18890),l=o(9672),d=o(87156),p=o(81668),c=o(50856),u=o(62276);const h=(0,s.x)(HTMLElement);(0,l.k)({_template:c.d`
    <style include="paper-dropdown-menu-shared-styles"></style>

    <paper-menu-button id="menuButton" vertical-align="[[verticalAlign]]" horizontal-align="[[horizontalAlign]]" dynamic-align="[[dynamicAlign]]" vertical-offset="[[_computeMenuVerticalOffset(noLabelFloat, verticalOffset)]]" disabled="[[disabled]]" no-animations="[[noAnimations]]" on-iron-select="_onIronSelect" on-iron-deselect="_onIronDeselect" opened="{{opened}}" close-on-activate allow-outside-scroll="[[allowOutsideScroll]]" restore-focus-on-close="[[restoreFocusOnClose]]" expand-sizing-target-for-scrollbars="[[expandSizingTargetForScrollbars]]">
      <!-- support hybrid mode: user might be using paper-menu-button 1.x which distributes via <content> -->
      <div class="dropdown-trigger" slot="dropdown-trigger">
        <paper-ripple></paper-ripple>
        <!-- paper-input has type="text" for a11y, do not remove -->
        <paper-input id="input" type="text" invalid="[[invalid]]" readonly disabled="[[disabled]]" value="[[value]]" placeholder="[[placeholder]]" error-message="[[errorMessage]]" always-float-label="[[alwaysFloatLabel]]" no-label-float="[[noLabelFloat]]" label="[[label]]" input-role="button" input-aria-haspopup="listbox" autocomplete="off">
          <!-- support hybrid mode: user might be using paper-input 1.x which distributes via <content> -->
          <iron-icon icon="paper-dropdown-menu:arrow-drop-down" suffix slot="suffix"></iron-icon>
        </paper-input>
      </div>
      <slot id="content" name="dropdown-content" slot="dropdown-content"></slot>
    </paper-menu-button>
`,is:"paper-dropdown-menu",behaviors:[n.P,i.a,r.V,a.x],properties:{selectedItemLabel:{type:String,notify:!0,readOnly:!0},selectedItem:{type:Object,notify:!0,readOnly:!0},value:{type:String,notify:!0},label:{type:String},placeholder:{type:String},errorMessage:{type:String},opened:{type:Boolean,notify:!0,value:!1,observer:"_openedChanged"},allowOutsideScroll:{type:Boolean,value:!1},noLabelFloat:{type:Boolean,value:!1,reflectToAttribute:!0},alwaysFloatLabel:{type:Boolean,value:!1},noAnimations:{type:Boolean,value:!1},horizontalAlign:{type:String,value:"right"},verticalAlign:{type:String,value:"top"},verticalOffset:Number,dynamicAlign:{type:Boolean},restoreFocusOnClose:{type:Boolean,value:!0},expandSizingTargetForScrollbars:{type:Boolean,value:!1}},listeners:{tap:"_onTap"},keyBindings:{"up down":"open",esc:"close"},observers:["_selectedItemChanged(selectedItem)"],_attachDom(e){const t=(0,u.r)(this);return t.attachShadow({mode:"open",delegatesFocus:!0,shadyUpgradeFragment:e}),t.shadowRoot.appendChild(e),h.prototype._attachDom.call(this,e)},focus(){this.$.input._focusableElement.focus()},attached:function(){var e=this.contentElement;e&&e.selectedItem&&this._setSelectedItem(e.selectedItem)},get contentElement(){for(var e=(0,d.vz)(this.$.content).getDistributedNodes(),t=0,o=e.length;t<o;t++)if(e[t].nodeType===Node.ELEMENT_NODE)return e[t]},open:function(){this.$.menuButton.open()},close:function(){this.$.menuButton.close()},_onIronSelect:function(e){this._setSelectedItem(e.detail.item)},_onIronDeselect:function(e){this._setSelectedItem(null)},_onTap:function(e){p.nJ(e)===this&&this.open()},_selectedItemChanged:function(e){var t="";t=e?e.label||e.getAttribute("label")||e.textContent.trim():"",this.value=t,this._setSelectedItemLabel(t)},_computeMenuVerticalOffset:function(e,t){return t||(e?-4:8)},_getValidity:function(e){return this.disabled||!this.required||this.required&&!!this.value},_openedChanged:function(){var e=this.opened?"true":"false",t=this.contentElement;t&&t.setAttribute("aria-expanded",e)}})},25782:(e,t,o)=>{o(65233),o(65660),o(70019),o(97968);var n=o(9672),i=o(50856),r=o(33760);(0,n.k)({_template:i.d`
    <style include="paper-item-shared-styles"></style>
    <style>
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
        @apply --paper-icon-item;
      }

      .content-icon {
        @apply --layout-horizontal;
        @apply --layout-center;

        width: var(--paper-item-icon-width, 56px);
        @apply --paper-item-icon;
      }
    </style>

    <div id="contentIcon" class="content-icon">
      <slot name="item-icon"></slot>
    </div>
    <slot></slot>
`,is:"paper-icon-item",behaviors:[r.U]})},33760:(e,t,o)=>{o.d(t,{U:()=>r});o(65233);var n=o(51644),i=o(26110);const r=[n.P,i.a,{hostAttributes:{role:"option",tabindex:"0"}}]},89194:(e,t,o)=>{o(65233),o(65660),o(70019);var n=o(9672),i=o(50856);(0,n.k)({_template:i.d`
    <style>
      :host {
        overflow: hidden; /* needed for text-overflow: ellipsis to work on ff */
        @apply --layout-vertical;
        @apply --layout-center-justified;
        @apply --layout-flex;
      }

      :host([two-line]) {
        min-height: var(--paper-item-body-two-line-min-height, 72px);
      }

      :host([three-line]) {
        min-height: var(--paper-item-body-three-line-min-height, 88px);
      }

      :host > ::slotted(*) {
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }

      :host > ::slotted([secondary]) {
        @apply --paper-font-body1;

        color: var(--paper-item-body-secondary-color, var(--secondary-text-color));

        @apply --paper-item-body-secondary;
      }
    </style>

    <slot></slot>
`,is:"paper-item-body"})},97968:(e,t,o)=>{o(65660),o(70019);const n=document.createElement("template");n.setAttribute("style","display: none;"),n.innerHTML="<dom-module id=\"paper-item-shared-styles\">\n  <template>\n    <style>\n      :host, .paper-item {\n        display: block;\n        position: relative;\n        min-height: var(--paper-item-min-height, 48px);\n        padding: 0px 16px;\n      }\n\n      .paper-item {\n        @apply --paper-font-subhead;\n        border:none;\n        outline: none;\n        background: white;\n        width: 100%;\n        text-align: left;\n      }\n\n      :host([hidden]), .paper-item[hidden] {\n        display: none !important;\n      }\n\n      :host(.iron-selected), .paper-item.iron-selected {\n        font-weight: var(--paper-item-selected-weight, bold);\n\n        @apply --paper-item-selected;\n      }\n\n      :host([disabled]), .paper-item[disabled] {\n        color: var(--paper-item-disabled-color, var(--disabled-text-color));\n\n        @apply --paper-item-disabled;\n      }\n\n      :host(:focus), .paper-item:focus {\n        position: relative;\n        outline: 0;\n\n        @apply --paper-item-focused;\n      }\n\n      :host(:focus):before, .paper-item:focus:before {\n        @apply --layout-fit;\n\n        background: currentColor;\n        content: '';\n        opacity: var(--dark-divider-opacity);\n        pointer-events: none;\n\n        @apply --paper-item-focused-before;\n      }\n    </style>\n  </template>\n</dom-module>",document.head.appendChild(n.content)},53973:(e,t,o)=>{o(65233),o(65660),o(97968);var n=o(9672),i=o(50856),r=o(33760);(0,n.k)({_template:i.d`
    <style include="paper-item-shared-styles">
      :host {
        @apply --layout-horizontal;
        @apply --layout-center;
        @apply --paper-font-subhead;

        @apply --paper-item;
      }
    </style>
    <slot></slot>
`,is:"paper-item",behaviors:[r.U]})},51095:(e,t,o)=>{o(65233);var n=o(78161),i=o(9672),r=o(50856);(0,i.k)({_template:r.d`
    <style>
      :host {
        display: block;
        padding: 8px 0;

        background: var(--paper-listbox-background-color, var(--primary-background-color));
        color: var(--paper-listbox-color, var(--primary-text-color));

        @apply --paper-listbox;
      }
    </style>

    <slot></slot>
`,is:"paper-listbox",behaviors:[n.i],hostAttributes:{role:"listbox"}})},21560:(e,t,o)=>{o.d(t,{ZH:()=>p,MT:()=>r,U2:()=>l,RV:()=>i,t8:()=>d});const n=function(){if(!(!navigator.userAgentData&&/Safari\//.test(navigator.userAgent)&&!/Chrom(e|ium)\//.test(navigator.userAgent))||!indexedDB.databases)return Promise.resolve();let e;return new Promise((t=>{const o=()=>indexedDB.databases().finally(t);e=setInterval(o,100),o()})).finally((()=>clearInterval(e)))};function i(e){return new Promise(((t,o)=>{e.oncomplete=e.onsuccess=()=>t(e.result),e.onabort=e.onerror=()=>o(e.error)}))}function r(e,t){const o=n().then((()=>{const o=indexedDB.open(e);return o.onupgradeneeded=()=>o.result.createObjectStore(t),i(o)}));return(e,n)=>o.then((o=>n(o.transaction(t,e).objectStore(t))))}let a;function s(){return a||(a=r("keyval-store","keyval")),a}function l(e,t=s()){return t("readonly",(t=>i(t.get(e))))}function d(e,t,o=s()){return o("readwrite",(o=>(o.put(t,e),i(o.transaction))))}function p(e=s()){return e("readwrite",(e=>(e.clear(),i(e.transaction))))}},32930:(e,t,o)=>{o.d(t,{v:()=>i});var n=o(39030);function i(e="",t=!1,o=""){return(0,n.eZ)({descriptor:n=>({get(){var n,i,r;const a="slot"+(e?`[name=${e}]`:":not([name])");let s=null!==(r=null===(i=null===(n=this.renderRoot)||void 0===n?void 0:n.querySelector(a))||void 0===i?void 0:i.assignedNodes({flatten:t}))&&void 0!==r?r:[];return o&&(s=s.filter((e=>e.nodeType===Node.ELEMENT_NODE&&e.matches(o)))),s},enumerable:!0,configurable:!0})})}},19596:(e,t,o)=>{o.d(t,{s:()=>c});var n=o(81563),i=o(38941);const r=(e,t)=>{var o,n;const i=e._$AN;if(void 0===i)return!1;for(const e of i)null===(n=(o=e)._$AO)||void 0===n||n.call(o,t,!1),r(e,t);return!0},a=e=>{let t,o;do{if(void 0===(t=e._$AM))break;o=t._$AN,o.delete(e),e=t}while(0===(null==o?void 0:o.size))},s=e=>{for(let t;t=e._$AM;e=t){let o=t._$AN;if(void 0===o)t._$AN=o=new Set;else if(o.has(e))break;o.add(e),p(t)}};function l(e){void 0!==this._$AN?(a(this),this._$AM=e,s(this)):this._$AM=e}function d(e,t=!1,o=0){const n=this._$AH,i=this._$AN;if(void 0!==i&&0!==i.size)if(t)if(Array.isArray(n))for(let e=o;e<n.length;e++)r(n[e],!1),a(n[e]);else null!=n&&(r(n,!1),a(n));else r(this,e)}const p=e=>{var t,o,n,r;e.type==i.pX.CHILD&&(null!==(t=(n=e)._$AP)&&void 0!==t||(n._$AP=d),null!==(o=(r=e)._$AQ)&&void 0!==o||(r._$AQ=l))};class c extends i.Xe{constructor(){super(...arguments),this._$AN=void 0}_$AT(e,t,o){super._$AT(e,t,o),s(this),this.isConnected=e._$AU}_$AO(e,t=!0){var o,n;e!==this.isConnected&&(this.isConnected=e,e?null===(o=this.reconnected)||void 0===o||o.call(this):null===(n=this.disconnected)||void 0===n||n.call(this)),t&&(r(this,e),a(this))}setValue(e){if((0,n.OR)(this._$Ct))this._$Ct._$AI(e,this);else{const t=[...this._$Ct._$AH];t[this._$Ci]=e,this._$Ct._$AI(t,this,0)}}disconnected(){}reconnected(){}}},81563:(e,t,o)=>{o.d(t,{E_:()=>v,i9:()=>h,_Y:()=>d,pt:()=>r,OR:()=>s,hN:()=>a,ws:()=>m,fk:()=>p,hl:()=>u});var n=o(15304);const{H:i}=n.Al,r=e=>null===e||"object"!=typeof e&&"function"!=typeof e,a=(e,t)=>{var o,n;return void 0===t?void 0!==(null===(o=e)||void 0===o?void 0:o._$litType$):(null===(n=e)||void 0===n?void 0:n._$litType$)===t},s=e=>void 0===e.strings,l=()=>document.createComment(""),d=(e,t,o)=>{var n;const r=e._$AA.parentNode,a=void 0===t?e._$AB:t._$AA;if(void 0===o){const t=r.insertBefore(l(),a),n=r.insertBefore(l(),a);o=new i(t,n,e,e.options)}else{const t=o._$AB.nextSibling,i=o._$AM,s=i!==e;if(s){let t;null===(n=o._$AQ)||void 0===n||n.call(o,e),o._$AM=e,void 0!==o._$AP&&(t=e._$AU)!==i._$AU&&o._$AP(t)}if(t!==a||s){let e=o._$AA;for(;e!==t;){const t=e.nextSibling;r.insertBefore(e,a),e=t}}}return o},p=(e,t,o=e)=>(e._$AI(t,o),e),c={},u=(e,t=c)=>e._$AH=t,h=e=>e._$AH,m=e=>{var t;null===(t=e._$AP)||void 0===t||t.call(e,!1,!0);let o=e._$AA;const n=e._$AB.nextSibling;for(;o!==n;){const e=o.nextSibling;o.remove(),o=e}},v=e=>{e._$AR()}},57835:(e,t,o)=>{o.d(t,{Xe:()=>n.Xe,pX:()=>n.pX,XM:()=>n.XM});var n=o(38941)}}]);
//# sourceMappingURL=d3958b71.js.map