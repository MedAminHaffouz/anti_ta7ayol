import{s as n}from"./storage.js";let r=!1;if(!r){let i=function(t){const s=document.querySelector("#scam-detector-notification");s&&s.remove();const e=document.createElement("div");if(e.id="scam-detector-notification",e.style.cssText=`
      position: fixed;
      top: 20px;
      right: 20px;
      background: linear-gradient(135deg, #1f2937 0%, #374151 100%);
      color: white;
      padding: 12px 16px;
      border-radius: 8px;
      box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255, 255, 255, 0.1);
      z-index: 10000;
      font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
      font-size: 14px;
      max-width: 300px;
      animation: slideIn 0.3s ease-out;
      backdrop-filter: blur(10px);
      border: 1px solid rgba(255, 255, 255, 0.1);
      cursor: pointer;
    `,!document.querySelector("#scam-detector-styles")){const o=document.createElement("style");o.id="scam-detector-styles",o.textContent=`
        @keyframes slideIn {
          from { 
            transform: translateX(100%) scale(0.9); 
            opacity: 0; 
          }
          to { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
          }
        }
        @keyframes slideOut {
          from { 
            transform: translateX(0) scale(1); 
            opacity: 1; 
          }
          to { 
            transform: translateX(100%) scale(0.9); 
            opacity: 0; 
          }
        }
      `,document.head.appendChild(o)}e.innerHTML=`
      <div style="display: flex; align-items: center; gap: 8px;">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
          <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
          <circle cx="12" cy="10" r="3"/>
        </svg>
        <span>${t}</span>
      </div>
    `,document.body.appendChild(e),e.addEventListener("click",()=>{e.style.animation="slideOut 0.3s ease-in",setTimeout(()=>e.remove(),300)}),setTimeout(()=>{e.parentNode&&(e.style.animation="slideOut 0.3s ease-in",setTimeout(()=>e.remove(),300))},4e3)};r=!0,chrome.runtime.onMessage.addListener((t,s,e)=>(t.action==="checkSelectedText"&&t.text&&n.storeSelectedText(t.text.trim()).then(()=>{i("Text selected for scam check. Click the extension icon to analyze."),e({success:!0})}).catch(o=>{console.error("Failed to store selected text:",o),e({success:!1,error:o.message})}),!0)),document.addEventListener("keydown",t=>{var s;if((t.ctrlKey||t.metaKey)&&t.shiftKey&&t.key==="S"){t.preventDefault();const e=(s=window.getSelection())==null?void 0:s.toString().trim();e&&e.length>0?n.storeSelectedText(e).then(()=>{i("Text captured! Click the extension icon to analyze."),chrome.runtime.sendMessage({action:"openPopup"}).catch(o=>{console.error("Failed to open popup:",o)})}).catch(o=>{console.error("Failed to store selected text:",o)}):i("No text selected. Please select some text first.")}}),document.addEventListener("mouseup",()=>{var s;const t=(s=window.getSelection())==null?void 0:s.toString().trim();t&&t.length>10&&n.storeSelectedText(t).catch(e=>{console.error("Failed to store selected text:",e)})})}
