/*! For license information please see 5423c55a.js.LICENSE.txt */
"use strict";(self.webpackChunkhome_assistant_frontend=self.webpackChunkhome_assistant_frontend||[]).push([[83411],{54930:(r,e,i)=>{i.d(e,{D:()=>g});var t=i(87480),c=i(26767),s=i(38103),a=i(37500),o=i(5701),n=i(228),d=i(48399),l=i(47501);class p extends a.oi{constructor(){super(...arguments),this.indeterminate=!1,this.progress=0,this.density=0,this.closed=!1}open(){this.closed=!1}close(){this.closed=!0}render(){const r={"mdc-circular-progress--closed":this.closed,"mdc-circular-progress--indeterminate":this.indeterminate},e=48+4*this.density,i={width:`${e}px`,height:`${e}px`};return a.dy`
      <div
        class="mdc-circular-progress ${(0,n.$)(r)}"
        style="${(0,l.V)(i)}"
        role="progressbar"
        aria-label="${(0,d.o)(this.ariaLabel)}"
        aria-valuemin="0"
        aria-valuemax="1"
        aria-valuenow="${(0,d.o)(this.indeterminate?void 0:this.progress)}">
        ${this.renderDeterminateContainer()}
        ${this.renderIndeterminateContainer()}
      </div>`}renderDeterminateContainer(){const r=48+4*this.density,e=r/2,i=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,t=6.2831852*i,c=(1-this.progress)*t,s=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return a.dy`
      <div class="mdc-circular-progress__determinate-container">
        <svg class="mdc-circular-progress__determinate-circle-graphic"
             viewBox="0 0 ${r} ${r}">
          <circle class="mdc-circular-progress__determinate-track"
                  cx="${e}" cy="${e}" r="${i}"
                  stroke-width="${s}"></circle>
          <circle class="mdc-circular-progress__determinate-circle"
                  cx="${e}" cy="${e}" r="${i}"
                  stroke-dasharray="${6.2831852*i}"
                  stroke-dashoffset="${c}"
                  stroke-width="${s}"></circle>
        </svg>
      </div>`}renderIndeterminateContainer(){return a.dy`
      <div class="mdc-circular-progress__indeterminate-container">
        <div class="mdc-circular-progress__spinner-layer">
          ${this.renderIndeterminateSpinnerLayer()}
        </div>
      </div>`}renderIndeterminateSpinnerLayer(){const r=48+4*this.density,e=r/2,i=this.density>=-3?18+11*this.density/6:12.5+5*(this.density+3)/4,t=6.2831852*i,c=.5*t,s=this.density>=-3?4+this.density*(1/3):3+(this.density+3)*(1/6);return a.dy`
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-left">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${c}"
                    stroke-width="${s}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__gap-patch">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${c}"
                    stroke-width="${.8*s}"></circle>
          </svg>
        </div>
        <div class="mdc-circular-progress__circle-clipper mdc-circular-progress__circle-right">
          <svg class="mdc-circular-progress__indeterminate-circle-graphic"
               viewBox="0 0 ${r} ${r}">
            <circle cx="${e}" cy="${e}" r="${i}"
                    stroke-dasharray="${t}"
                    stroke-dashoffset="${c}"
                    stroke-width="${s}"></circle>
          </svg>
        </div>`}update(r){super.update(r),r.has("progress")&&(this.progress>1&&(this.progress=1),this.progress<0&&(this.progress=0))}}(0,t.__decorate)([(0,o.C)({type:Boolean,reflect:!0})],p.prototype,"indeterminate",void 0),(0,t.__decorate)([(0,o.C)({type:Number,reflect:!0})],p.prototype,"progress",void 0),(0,t.__decorate)([(0,o.C)({type:Number,reflect:!0})],p.prototype,"density",void 0),(0,t.__decorate)([(0,o.C)({type:Boolean,reflect:!0})],p.prototype,"closed",void 0),(0,t.__decorate)([s.L,(0,o.C)({type:String,attribute:"aria-label"})],p.prototype,"ariaLabel",void 0);const m=a.iv`.mdc-circular-progress__determinate-circle,.mdc-circular-progress__indeterminate-circle-graphic{stroke:#6200ee;stroke:var(--mdc-theme-primary, #6200ee)}.mdc-circular-progress__determinate-track{stroke:transparent}@keyframes mdc-circular-progress-container-rotate{to{transform:rotate(360deg)}}@keyframes mdc-circular-progress-spinner-layer-rotate{12.5%{transform:rotate(135deg)}25%{transform:rotate(270deg)}37.5%{transform:rotate(405deg)}50%{transform:rotate(540deg)}62.5%{transform:rotate(675deg)}75%{transform:rotate(810deg)}87.5%{transform:rotate(945deg)}100%{transform:rotate(1080deg)}}@keyframes mdc-circular-progress-color-1-fade-in-out{from{opacity:.99}25%{opacity:.99}26%{opacity:0}89%{opacity:0}90%{opacity:.99}to{opacity:.99}}@keyframes mdc-circular-progress-color-2-fade-in-out{from{opacity:0}15%{opacity:0}25%{opacity:.99}50%{opacity:.99}51%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-3-fade-in-out{from{opacity:0}40%{opacity:0}50%{opacity:.99}75%{opacity:.99}76%{opacity:0}to{opacity:0}}@keyframes mdc-circular-progress-color-4-fade-in-out{from{opacity:0}65%{opacity:0}75%{opacity:.99}90%{opacity:.99}to{opacity:0}}@keyframes mdc-circular-progress-left-spin{from{transform:rotate(265deg)}50%{transform:rotate(130deg)}to{transform:rotate(265deg)}}@keyframes mdc-circular-progress-right-spin{from{transform:rotate(-265deg)}50%{transform:rotate(-130deg)}to{transform:rotate(-265deg)}}.mdc-circular-progress{display:inline-flex;position:relative;direction:ltr;line-height:0;transition:opacity 250ms 0ms cubic-bezier(0.4, 0, 0.6, 1)}.mdc-circular-progress__determinate-container,.mdc-circular-progress__indeterminate-circle-graphic,.mdc-circular-progress__indeterminate-container,.mdc-circular-progress__spinner-layer{position:absolute;width:100%;height:100%}.mdc-circular-progress__determinate-container{transform:rotate(-90deg)}.mdc-circular-progress__indeterminate-container{font-size:0;letter-spacing:0;white-space:nowrap;opacity:0}.mdc-circular-progress__determinate-circle-graphic,.mdc-circular-progress__indeterminate-circle-graphic{fill:transparent}.mdc-circular-progress__determinate-circle{transition:stroke-dashoffset 500ms 0ms cubic-bezier(0, 0, 0.2, 1)}.mdc-circular-progress__gap-patch{position:absolute;top:0;left:47.5%;box-sizing:border-box;width:5%;height:100%;overflow:hidden}.mdc-circular-progress__gap-patch .mdc-circular-progress__indeterminate-circle-graphic{left:-900%;width:2000%;transform:rotate(180deg)}.mdc-circular-progress__circle-clipper{display:inline-flex;position:relative;width:50%;height:100%;overflow:hidden}.mdc-circular-progress__circle-clipper .mdc-circular-progress__indeterminate-circle-graphic{width:200%}.mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{left:-100%}.mdc-circular-progress--indeterminate .mdc-circular-progress__determinate-container{opacity:0}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{opacity:1}.mdc-circular-progress--indeterminate .mdc-circular-progress__indeterminate-container{animation:mdc-circular-progress-container-rotate 1568.2352941176ms linear infinite}.mdc-circular-progress--indeterminate .mdc-circular-progress__spinner-layer{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-1{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-1-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-2{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-2-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-3{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-3-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__color-4{animation:mdc-circular-progress-spinner-layer-rotate 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both,mdc-circular-progress-color-4-fade-in-out 5332ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-left .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-left-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--indeterminate .mdc-circular-progress__circle-right .mdc-circular-progress__indeterminate-circle-graphic{animation:mdc-circular-progress-right-spin 1333ms cubic-bezier(0.4, 0, 0.2, 1) infinite both}.mdc-circular-progress--closed{opacity:0}:host{display:inline-flex}.mdc-circular-progress__determinate-track{stroke:transparent;stroke:var(--mdc-circular-progress-track-color, transparent)}`;let g=class extends p{};g.styles=[m],g=(0,t.__decorate)([(0,c.M)("mwc-circular-progress")],g)},23682:(r,e,i)=>{function t(r,e){if(e.length<r)throw new TypeError(r+" argument"+(r>1?"s":"")+" required, but only "+e.length+" present")}i.d(e,{Z:()=>t})},90394:(r,e,i)=>{function t(r){if(null===r||!0===r||!1===r)return NaN;var e=Number(r);return isNaN(e)?e:e<0?Math.ceil(e):Math.floor(e)}i.d(e,{Z:()=>t})},79021:(r,e,i)=>{i.d(e,{Z:()=>a});var t=i(90394),c=i(34327),s=i(23682);function a(r,e){(0,s.Z)(2,arguments);var i=(0,c.Z)(r),a=(0,t.Z)(e);return isNaN(a)?new Date(NaN):a?(i.setDate(i.getDate()+a),i):i}},32182:(r,e,i)=>{i.d(e,{Z:()=>a});var t=i(90394),c=i(34327),s=i(23682);function a(r,e){(0,s.Z)(2,arguments);var i=(0,c.Z)(r),a=(0,t.Z)(e);if(isNaN(a))return new Date(NaN);if(!a)return i;var o=i.getDate(),n=new Date(i.getTime());n.setMonth(i.getMonth()+a+1,0);var d=n.getDate();return o>=d?n:(i.setFullYear(n.getFullYear(),n.getMonth(),o),i)}},59429:(r,e,i)=>{i.d(e,{Z:()=>s});var t=i(34327),c=i(23682);function s(r){(0,c.Z)(1,arguments);var e=(0,t.Z)(r);return e.setHours(0,0,0,0),e}},13250:(r,e,i)=>{i.d(e,{Z:()=>s});var t=i(34327),c=i(23682);function s(r){(0,c.Z)(1,arguments);var e=(0,t.Z)(r);return e.setDate(1),e.setHours(0,0,0,0),e}},34327:(r,e,i)=>{i.d(e,{Z:()=>c});var t=i(23682);function c(r){(0,t.Z)(1,arguments);var e=Object.prototype.toString.call(r);return r instanceof Date||"object"==typeof r&&"[object Date]"===e?new Date(r.getTime()):"number"==typeof r||"[object Number]"===e?new Date(r):("string"!=typeof r&&"[object String]"!==e||"undefined"==typeof console||(console.warn("Starting with v2.0.0-beta.1 date-fns doesn't accept strings as date arguments. Please use `parseISO` to parse strings. See: https://git.io/fjule"),console.warn((new Error).stack)),new Date(NaN))}}}]);
//# sourceMappingURL=5423c55a.js.map