import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import {createRef, h, render} from 'preact';
import { evaluate } from '/kirui/core/element';
import $ from "jquery";


class KrAjaxPanel extends Component {
    constructor(props) {
        super(props);
        props.ref = createRef();
        this.handleStateChange = this.handleStateChange.bind(this);
        document.addEventListener('state-change', this.handleStateChange);
    }

    refreshContent(extra_data) {
        let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': true}});
        this.base.dispatchEvent(e);

        let data = this.state;
        if ((extra_data !== undefined) && (extra_data !== null)) {
            $.extend(data, extra_data)
        }
        $.post({
            url: this.props.contentUrl || window.location.href,
            data: $.param(data, true),
            statusCode: {
                340: function (resp) {
                    window.location.replace(resp.getResponseHeader('location'));
                }
            }
        }).done((resp) => {
            let dom = evaluate(resp);
            this.props.children = dom.props.children;
            this.forceUpdate();
            let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
            this.base.dispatchEvent(e);
        }).fail((resp) => {
            if (resp.status === 403) {
                let d = evaluate(resp.responseText);
                this.props.children = d.props.children;
                this.forceUpdate();
                let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
                this.base.dispatchEvent(e);
            }
        });
    }

    doRender() {
        return <kr-ajax-panel {...this.props} onStateChange={this.handleStateChange} onReloadContent={this.handleStateChange}>{this.props.children}</kr-ajax-panel>;
    }

    handleStateChange(ev) {
        let data = this.state;
        $.extend(data, ev.detail.data);
        this.setState(data);

        if (ev.detail.forceUpdate === true) {
            this.refreshContent(ev.detail.src);
        }
    }

    componentDidMount() {
        /* this.base. */
        // window.addEventListener('state-change', this.handleStateChange);
    }
}

registry.register('kr-ajax-panel', KrAjaxPanel);

export { KrAjaxPanel }
