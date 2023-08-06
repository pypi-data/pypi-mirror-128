"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[854],{33220:(e,t,i)=>{var r=i(41248);function a(){a=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var n="static"===a?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!s(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],a=e.decorators,n=a.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),d=this.toElementFinisherExtras((0,a[n])(s)||s);e=d.element,this.addElementPlacement(e,t),d.finisher&&r.push(d.finisher);var l=d.extras;if(l){for(var c=0;c<l.length;c++)this.addElementPlacement(l[c],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return h(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?h(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=c(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:l(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=l(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function n(e){var t,i=c(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function o(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function s(e){return e.decorators&&e.decorators.length}function d(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function l(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function c(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function h(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}function p(e,t,i){return p="undefined"!=typeof Reflect&&Reflect.get?Reflect.get:function(e,t,i){var r=function(e,t){for(;!Object.prototype.hasOwnProperty.call(e,t)&&null!==(e=u(e)););return e}(e,t);if(r){var a=Object.getOwnPropertyDescriptor(r,t);return a.get?a.get.call(i):a.value}},p(e,t,i||e)}function u(e){return u=Object.setPrototypeOf?Object.getPrototypeOf:function(e){return e.__proto__||Object.getPrototypeOf(e)},u(e)}!function(e,t,i,r){var l=a();if(r)for(var c=0;c<r.length;c++)l=r[c](l);var h=t((function(e){l.initializeInstanceElements(e,p.elements)}),i),p=l.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var a,n=e[r];if("method"===n.kind&&(a=t.find(i)))if(d(n.descriptor)||d(a.descriptor)){if(s(n)||s(a))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");a.descriptor=n.descriptor}else{if(s(n)){if(s(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");a.decorators=n.decorators}o(n,a)}else t.push(n)}return t}(h.d.map(n)),e);l.initializeClassElements(h.F,p.elements),l.runClassFinishers(h.F,p.finishers)}([(0,i(26767).M)("ha-radio")],(function(e,t){class i extends t{constructor(...t){super(...t),e(this)}}return{F:i,d:[{kind:"method",key:"firstUpdated",value:function(){p(u(i.prototype),"firstUpdated",this).call(this),this.style.setProperty("--mdc-theme-secondary","var(--primary-color)")}}]}}),r.Y)},32205:(e,t,i)=>{i.r(t),i.d(t,{AddMediaSourceAisWs:()=>g,HuiDialogAddMediaSourceAis:()=>k});i(33220),i(28007),i(53918),i(30879);var r=i(37500),a=i(26767),n=i(5701),o=(i(31206),i(85124),i(43709),i(34821)),s=i(11654),d=i(26765),l=i(47181);function c(){c=function(){return e};var e={elementsDefinitionOrder:[["method"],["field"]],initializeInstanceElements:function(e,t){["method","field"].forEach((function(i){t.forEach((function(t){t.kind===i&&"own"===t.placement&&this.defineClassElement(e,t)}),this)}),this)},initializeClassElements:function(e,t){var i=e.prototype;["method","field"].forEach((function(r){t.forEach((function(t){var a=t.placement;if(t.kind===r&&("static"===a||"prototype"===a)){var n="static"===a?e:i;this.defineClassElement(n,t)}}),this)}),this)},defineClassElement:function(e,t){var i=t.descriptor;if("field"===t.kind){var r=t.initializer;i={enumerable:i.enumerable,writable:i.writable,configurable:i.configurable,value:void 0===r?void 0:r.call(e)}}Object.defineProperty(e,t.key,i)},decorateClass:function(e,t){var i=[],r=[],a={static:[],prototype:[],own:[]};if(e.forEach((function(e){this.addElementPlacement(e,a)}),this),e.forEach((function(e){if(!u(e))return i.push(e);var t=this.decorateElement(e,a);i.push(t.element),i.push.apply(i,t.extras),r.push.apply(r,t.finishers)}),this),!t)return{elements:i,finishers:r};var n=this.decorateConstructor(i,t);return r.push.apply(r,n.finishers),n.finishers=r,n},addElementPlacement:function(e,t,i){var r=t[e.placement];if(!i&&-1!==r.indexOf(e.key))throw new TypeError("Duplicated element ("+e.key+")");r.push(e.key)},decorateElement:function(e,t){for(var i=[],r=[],a=e.decorators,n=a.length-1;n>=0;n--){var o=t[e.placement];o.splice(o.indexOf(e.key),1);var s=this.fromElementDescriptor(e),d=this.toElementFinisherExtras((0,a[n])(s)||s);e=d.element,this.addElementPlacement(e,t),d.finisher&&r.push(d.finisher);var l=d.extras;if(l){for(var c=0;c<l.length;c++)this.addElementPlacement(l[c],t);i.push.apply(i,l)}}return{element:e,finishers:r,extras:i}},decorateConstructor:function(e,t){for(var i=[],r=t.length-1;r>=0;r--){var a=this.fromClassDescriptor(e),n=this.toClassDescriptor((0,t[r])(a)||a);if(void 0!==n.finisher&&i.push(n.finisher),void 0!==n.elements){e=n.elements;for(var o=0;o<e.length-1;o++)for(var s=o+1;s<e.length;s++)if(e[o].key===e[s].key&&e[o].placement===e[s].placement)throw new TypeError("Duplicated element ("+e[o].key+")")}}return{elements:e,finishers:i}},fromElementDescriptor:function(e){var t={kind:e.kind,key:e.key,placement:e.placement,descriptor:e.descriptor};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),"field"===e.kind&&(t.initializer=e.initializer),t},toElementDescriptors:function(e){var t;if(void 0!==e)return(t=e,function(e){if(Array.isArray(e))return e}(t)||function(e){if("undefined"!=typeof Symbol&&null!=e[Symbol.iterator]||null!=e["@@iterator"])return Array.from(e)}(t)||function(e,t){if(e){if("string"==typeof e)return v(e,t);var i=Object.prototype.toString.call(e).slice(8,-1);return"Object"===i&&e.constructor&&(i=e.constructor.name),"Map"===i||"Set"===i?Array.from(e):"Arguments"===i||/^(?:Ui|I)nt(?:8|16|32)(?:Clamped)?Array$/.test(i)?v(e,t):void 0}}(t)||function(){throw new TypeError("Invalid attempt to destructure non-iterable instance.\nIn order to be iterable, non-array objects must have a [Symbol.iterator]() method.")}()).map((function(e){var t=this.toElementDescriptor(e);return this.disallowProperty(e,"finisher","An element descriptor"),this.disallowProperty(e,"extras","An element descriptor"),t}),this)},toElementDescriptor:function(e){var t=String(e.kind);if("method"!==t&&"field"!==t)throw new TypeError('An element descriptor\'s .kind property must be either "method" or "field", but a decorator created an element descriptor with .kind "'+t+'"');var i=y(e.key),r=String(e.placement);if("static"!==r&&"prototype"!==r&&"own"!==r)throw new TypeError('An element descriptor\'s .placement property must be one of "static", "prototype" or "own", but a decorator created an element descriptor with .placement "'+r+'"');var a=e.descriptor;this.disallowProperty(e,"elements","An element descriptor");var n={kind:t,key:i,placement:r,descriptor:Object.assign({},a)};return"field"!==t?this.disallowProperty(e,"initializer","A method descriptor"):(this.disallowProperty(a,"get","The property descriptor of a field descriptor"),this.disallowProperty(a,"set","The property descriptor of a field descriptor"),this.disallowProperty(a,"value","The property descriptor of a field descriptor"),n.initializer=e.initializer),n},toElementFinisherExtras:function(e){return{element:this.toElementDescriptor(e),finisher:f(e,"finisher"),extras:this.toElementDescriptors(e.extras)}},fromClassDescriptor:function(e){var t={kind:"class",elements:e.map(this.fromElementDescriptor,this)};return Object.defineProperty(t,Symbol.toStringTag,{value:"Descriptor",configurable:!0}),t},toClassDescriptor:function(e){var t=String(e.kind);if("class"!==t)throw new TypeError('A class descriptor\'s .kind property must be "class", but a decorator created a class descriptor with .kind "'+t+'"');this.disallowProperty(e,"key","A class descriptor"),this.disallowProperty(e,"placement","A class descriptor"),this.disallowProperty(e,"descriptor","A class descriptor"),this.disallowProperty(e,"initializer","A class descriptor"),this.disallowProperty(e,"extras","A class descriptor");var i=f(e,"finisher");return{elements:this.toElementDescriptors(e.elements),finisher:i}},runClassFinishers:function(e,t){for(var i=0;i<t.length;i++){var r=(0,t[i])(e);if(void 0!==r){if("function"!=typeof r)throw new TypeError("Finishers must return a constructor.");e=r}}return e},disallowProperty:function(e,t,i){if(void 0!==e[t])throw new TypeError(i+" can't have a ."+t+" property.")}};return e}function h(e){var t,i=y(e.key);"method"===e.kind?t={value:e.value,writable:!0,configurable:!0,enumerable:!1}:"get"===e.kind?t={get:e.value,configurable:!0,enumerable:!1}:"set"===e.kind?t={set:e.value,configurable:!0,enumerable:!1}:"field"===e.kind&&(t={configurable:!0,writable:!0,enumerable:!0});var r={kind:"field"===e.kind?"field":"method",key:i,placement:e.static?"static":"field"===e.kind?"own":"prototype",descriptor:t};return e.decorators&&(r.decorators=e.decorators),"field"===e.kind&&(r.initializer=e.value),r}function p(e,t){void 0!==e.descriptor.get?t.descriptor.get=e.descriptor.get:t.descriptor.set=e.descriptor.set}function u(e){return e.decorators&&e.decorators.length}function m(e){return void 0!==e&&!(void 0===e.value&&void 0===e.writable)}function f(e,t){var i=e[t];if(void 0!==i&&"function"!=typeof i)throw new TypeError("Expected '"+t+"' to be a function");return i}function y(e){var t=function(e,t){if("object"!=typeof e||null===e)return e;var i=e[Symbol.toPrimitive];if(void 0!==i){var r=i.call(e,t||"default");if("object"!=typeof r)return r;throw new TypeError("@@toPrimitive must return a primitive value.")}return("string"===t?String:Number)(e)}(e,"string");return"symbol"==typeof t?t:String(t)}function v(e,t){(null==t||t>e.length)&&(t=e.length);for(var i=0,r=new Array(t);i<t;i++)r[i]=e[i];return r}const g=(e,t,i,r,a,n,o)=>e.callWS({type:"ais_cloud/add_ais_media_source",mediaCategory:t,mediaName:i,mediaType:r,mediaStreamUrl:a,mediaImageUrl:n,mediaShare:o});let k=function(e,t,i,r){var a=c();if(r)for(var n=0;n<r.length;n++)a=r[n](a);var o=t((function(e){a.initializeInstanceElements(e,s.elements)}),i),s=a.decorateClass(function(e){for(var t=[],i=function(e){return"method"===e.kind&&e.key===n.key&&e.placement===n.placement},r=0;r<e.length;r++){var a,n=e[r];if("method"===n.kind&&(a=t.find(i)))if(m(n.descriptor)||m(a.descriptor)){if(u(n)||u(a))throw new ReferenceError("Duplicated methods ("+n.key+") can't be decorated.");a.descriptor=n.descriptor}else{if(u(n)){if(u(a))throw new ReferenceError("Decorators can't be placed on different accessors with for the same property ("+n.key+").");a.decorators=n.decorators}p(n,a)}else t.push(n)}return t}(o.d.map(h)),e);return a.initializeClassElements(o.F,s.elements),a.runClassFinishers(o.F,s.finishers)}([(0,a.M)("hui-dialog-add-media-source-ais")],(function(e,t){return{F:class extends t{constructor(...t){super(...t),e(this)}},d:[{kind:"field",decorators:[(0,n.C)({attribute:!1})],key:"hass",value:void 0},{kind:"field",decorators:[(0,n.C)({attribute:!1}),(0,n.C)()],key:"_loading",value:()=>!1},{kind:"field",decorators:[(0,n.C)()],key:"_opened",value:()=>!1},{kind:"field",decorators:[(0,n.C)()],key:"mediaCategory",value:()=>"radio"},{kind:"field",decorators:[(0,n.C)()],key:"mediaName",value:()=>""},{kind:"field",decorators:[(0,n.C)()],key:"mediaType",value:()=>""},{kind:"field",decorators:[(0,n.C)()],key:"mediaStreamUrl",value:()=>""},{kind:"field",decorators:[(0,n.C)()],key:"mediaImageUrl",value:()=>""},{kind:"field",decorators:[(0,n.C)()],key:"mediaShare",value:()=>!1},{kind:"field",decorators:[(0,n.C)()],key:"mediaChips",value:()=>[]},{kind:"field",decorators:[(0,n.C)()],key:"mediaNamePlaceholder",value:()=>"Nazwa (komenda: Włącz radio nazwa)"},{kind:"field",decorators:[(0,n.C)()],key:"mediaTypePlaceholder",value:()=>"Typ radia"},{kind:"field",decorators:[(0,n.C)()],key:"mediaUrlPlaceholder",value:()=>"Adres URL Strumienia"},{kind:"field",key:"_aisMediaInfo",value:void 0},{kind:"method",key:"showDialog",value:function(){this._opened=!0,this._aisMediaInfo=this.hass.states["media_player.wbudowany_glosnik"],this.mediaCategory="radio",this.mediaName="",this.mediaType="",this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id?this.mediaStreamUrl=this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id:this.mediaStreamUrl="",this.mediaImageUrl="",this.mediaShare=!1,this.mediaChips=[];this.hass.states["input_select.radio_type"].attributes.options.forEach((e=>{e.startsWith("Moje")||e.startsWith("Udostępnione")||this.mediaChips.push(e||"")}))}},{kind:"method",key:"closeDialog",value:function(){this._opened=!1,(0,l.B)(this,"dialog-closed",{dialog:this.localName})}},{kind:"method",key:"render",value:function(){return r.dy`
      <ha-dialog
        .open=${this._opened}
        hideActions
        .heading=${(0,o.i)(this.hass,"Dodaj nowe Multimedia do biblioteki")}
        @closed=${this.closeDialog}
      >
        ${this._loading?r.dy`<ha-circular-progress active></ha-circular-progress>`:r.dy`<p>
                ${this._isAudioPlaying()&&!this._loading?r.dy`
                  <span class="aisUrl">
                    Odtwarzasz z URL, <ha-icon icon="mdi:web"></ha-icon>:
                    <b></b>${this.hass.states["media_player.wbudowany_glosnik"].attributes.media_content_id}</b>
                    <br/>ten adres został wypełniony automatycznie - sprawdź czy się zgadza.
                    </span
                  >
                  `:r.dy`
                      Obecnie na wbudowanym odtwarzaczu nie odtwarzasz żadnych
                      mediów. Sugerujemy sprawdzenie działania mediów na
                      odtwarzaczu przed ich dodaniem.
                    `}
              </p>

              <label> Typ audio: </label>
              <div class="audio-types" id="audio_types">
                <ha-radio
                  name="audioType"
                  .checked=${"radio"===this.mediaCategory}
                  value="radio"
                  @change=${this._mediaCategoryChanged}
                ></ha-radio>
                <ha-icon icon="mdi:radio"></ha-icon>

                <ha-radio
                  name="audioType"
                  .checked=${"podcast"===this.mediaCategory}
                  value="podcast"
                  @change=${this._mediaCategoryChanged}
                ></ha-radio>
                <ha-icon icon="mdi:podcast"></ha-icon>

                <ha-radio
                  name="audioType"
                  .checked=${"audiobook"===this.mediaCategory}
                  value="audiobook"
                  @change=${this._mediaCategoryChanged}
                ></ha-radio>
                <ha-icon icon="mdi:book-music"></ha-icon>

                <ha-radio
                  name="audioType"
                  .checked=${"music"===this.mediaCategory}
                  value="music"
                  @change=${this._mediaCategoryChanged}
                ></ha-radio>
                <ha-icon icon="mdi:music"></ha-icon>
              </div>

              <br />
              ${"radio"===this.mediaCategory||"podcast"===this.mediaCategory?r.dy`
                    <paper-input
                      .placeholder=${this.mediaNamePlaceholder}
                      type="text"
                      value=${this.mediaName}
                      id="audio_name"
                      @value-changed=${this._mediaNameChanged}
                    >
                      <ha-icon icon="mdi:account-voice" slot="suffix"></ha-icon>
                    </paper-input>

                    <paper-input
                      .placeholder=${this.mediaTypePlaceholder}
                      type="text"
                      value=${this.mediaType}
                      id="audio_category"
                      @value-changed=${this._mediaTypeChanged}
                    >
                      <ha-icon
                        icon="mdi:format-list-bulleted-type"
                        slot="suffix"
                      ></ha-icon>
                    </paper-input>
                    <ha-chip-set
                      @chip-clicked=${this._mediaTypePicket}
                      .items=${this.mediaChips}
                    >
                    </ha-chip-set>
                    <paper-input
                      .placeholder=${this.mediaUrlPlaceholder}
                      type="text"
                      value=${this.mediaStreamUrl}
                      @value-changed=${this._mediaStreamUrlChanged}
                    >
                      <ha-icon icon="mdi:play-network" slot="suffix"></ha-icon>
                    </paper-input>

                    <paper-input
                      placeholder="Adres URL Okładki"
                      type="text"
                      value=${this.mediaImageUrl}
                      @value-changed=${this._mediaImageUrlChanged}
                    >
                      <ha-icon icon="mdi:image-edit" slot="suffix"></ha-icon>
                    </paper-input>
                    <br />
                    <div style="text-align:center;">
                      <ha-icon icon="mdi:share-variant"></ha-icon>
                      <ha-switch
                        .checked=${this.mediaShare}
                        @change=${this._mediaShareChanged}
                      >
                      </ha-switch>
                      Udostępnij dla wszystkich (po sprawdzeniu w AIS)
                      <br /><br />
                    </div>
                    ${this._canSourceBeAdded()?r.dy` <div class="sourceCheckButton">
                            <mwc-button raised @click=${this._handleAddMedia}>
                              <ha-icon icon="hass:music-note-plus"></ha-icon>
                              ${this.mediaShare?r.dy`Dodaj do swojej biblioteki i udostępnij
                                  dla wszystkich`:r.dy` Dodaj do swojej biblioteki `}
                            </mwc-button>
                          </div>
                          <br />`:r.dy`
                          <div style="text-align: center;">
                            <h2>Wypełnij wszsytkie wymagane pola.</h2>
                          </div>
                          <br />
                        `}
                  `:r.dy`<div class="WorkInProgress">
                      <img src="/static/ais_work_in_progress.png" />
                    </div>
                    <div class="AisGithub">
                      <a href="https://github.com/sviete" target="_blank"
                        ><ha-icon icon="hass:github"></ha-icon> Join AI-Speaker
                        on Github</a
                      >
                    </div>
                    <br />`} `}
      </ha-dialog>
    `}},{kind:"method",key:"_addMediaToAis",value:async function(){this._loading=!0;let e={message:"",error:!1};try{e=await g(this.hass,this.mediaCategory,this.mediaName,this.mediaType,this.mediaStreamUrl,this.mediaImageUrl,this.mediaShare)}catch{this._loading=!1}return this._loading=!1,e}},{kind:"method",key:"_handleAddMedia",value:async function(){const e=await this._addMediaToAis();if(e.error)return void await(0,d.Ys)(this,{title:"AIS",text:e.message});await(0,d.g7)(this,{title:"AIS",text:e.message+" Czy chcesz dodać kolejne media?",confirmText:"TAK",dismissText:"NIE"})?(this.mediaCategory="radio",this.mediaName="",this.mediaType="",this.mediaStreamUrl="",this.mediaImageUrl="",this.mediaShare=!1):this.closeDialog()}},{kind:"method",key:"_isAudioPlaying",value:function(){var e;return!(null===(e=this._aisMediaInfo)||void 0===e||!e.attributes.media_content_id)}},{kind:"method",key:"_canSourceBeAdded",value:function(){return!(this.mediaName.length<3)&&(!(this.mediaType.length<3)&&!(this.mediaStreamUrl.length<10))}},{kind:"method",key:"_mediaCategoryChanged",value:function(e){const t=e.currentTarget.value;if(t!==this.mediaCategory)if(this.mediaCategory=t,"radio"===t){this.mediaNamePlaceholder="Nazwa (komenda: Włącz radio nazwa)",this.mediaTypePlaceholder="Typ radia",this.mediaUrlPlaceholder="Adres URL Strumienia",this.mediaChips=[];this.hass.states["input_select.radio_type"].attributes.options.forEach((e=>{e.startsWith("Moje")||e.startsWith("Udostępnione")||this.mediaChips.push(e)}))}else if("podcast"===t){this.mediaNamePlaceholder="Nazwa (komenda: Włącz podcast nazwa)",this.mediaTypePlaceholder="Typ podcasta",this.mediaUrlPlaceholder="Adres URL Kanału RSS (rss feed)",this.mediaChips=[];this.hass.states["input_select.podcast_type"].attributes.options.forEach((e=>{e.startsWith("Moje")||e.startsWith("Udostępnione")||this.mediaChips.push(e)}))}}},{kind:"method",key:"_mediaTypeChanged",value:function(e){const t=e.detail.value;t!==this.mediaType&&(this.mediaType=t)}},{kind:"method",key:"_mediaTypePicket",value:function(e){const t=e.detail.index,i=this.mediaChips[t];i!==this.mediaType&&(this.mediaType=i)}},{kind:"method",key:"_mediaStreamUrlChanged",value:function(e){const t=e.detail.value;t!==this.mediaStreamUrl&&(this.mediaStreamUrl=t)}},{kind:"method",key:"_mediaImageUrlChanged",value:function(e){const t=e.detail.value;t!==this.mediaImageUrl&&(this.mediaImageUrl=t)}},{kind:"method",key:"_mediaShareChanged",value:function(e){const t=e.target.checked;t!==this.mediaShare&&(this.mediaShare=t)}},{kind:"method",key:"_mediaNameChanged",value:function(e){const t=e.detail.value;t!==this.mediaName&&(this.mediaName=t)}},{kind:"get",static:!0,key:"styles",value:function(){return[s.yu,r.iv`
        ha-dialog {
          --dialog-content-padding: 0 24px 20px;
        }
        div.sourceCheckButton {
          text-align: center;
        }
        div.WorkInProgress {
          text-align: center;
        }
        div.AisGithub {
          text-align: right;
        }
        img {
          max-width: 500px;
          max-height: 300px;
        }
        span.aisUrl {
          word-wrap: break-word;
        }
        ha-circular-progress {
          --mdc-theme-primary: var(--primary-color);
          display: flex;
          justify-content: center;
          margin-top: 40px;
        }
      `]}}]}}),r.oi)}}]);
//# sourceMappingURL=fdfc9525.js.map