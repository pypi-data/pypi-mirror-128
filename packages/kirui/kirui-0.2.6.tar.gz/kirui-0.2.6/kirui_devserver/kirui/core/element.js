import { registry } from "./registry";
import { h as createElement } from "preact";
import { html_element } from './component';


const k = function(name, props, children) {
    let el = registry.getComponent(name);
    if (el === undefined) {
        return createElement(html_element(name), props, children);
    } else {
        return createElement(el, props, children);
    }
}

const evaluate = function(s) {
    return eval(s.replace(/\n/g, "")); // .replace(/\\/g,'\\\\')));  // TODO: miért kell dupla eval???
}

export { evaluate };
