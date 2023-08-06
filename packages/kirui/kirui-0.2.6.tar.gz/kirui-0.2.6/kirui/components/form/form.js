import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h } from 'preact';
import { evaluate } from '/kirui/core/element';
import $ from "jquery";


class Form extends Component {
    constructor(props) {
        super(props);

        this.state = {
            'csrfmiddlewaretoken': this.props.csrfmiddlewaretoken
        }
        this.formData = new FormData();
        this.formData.set('csrfmiddlewaretoken', this.props.csrfmiddlewaretoken);

        this.handleInputChange = this.handleInputChange.bind(this);
        this.bubbleSubmit = this.bubbleSubmit.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.bubbleStateChange = this.bubbleStateChange.bind(this);
    }

    handleInputChange(event) {
        const target = event.target;

        let name, value;
        if (event instanceof CustomEvent) {
            name = event.target.getAttribute('name');
            value = event.detail.data;
        } else if (event instanceof Event) {
            // console.log(event);
            name = target.name;
            if (target.type === 'checkbox') {
                value = target.checked;
            } else if (target.type === 'file') {
                /*let reader = new FileReader();
                reader.onload = (evt) => {
                    value = evt.target.result;
                    this.setState({[name]: value});
                    $.extend(this.state, {[name]: value});
                    value = null;
                };
                reader.readAsArrayBuffer(target.files[0]);*/
                value = target.files[0];
            } else {
                value = target.value;
            }
        } else {
            // console.log(event);
            name = target.name;
            value = target.value.toString();  // TODO: megnézni, hogy ez így jó lesz-e. Minden value-t string-é konvertálunk, különben a default 0 értékbőll null lesz
        }

        if (value !== null) {  // a fájl olvasás async, ezért kell így megcsinálnom
            if (value instanceof Array) {
                this.formData.delete(name);
                for (let bit of value) {
                    this.formData.append(name, bit);
                }
            } else {
                this.formData.set(name, value);
            }
            this.setState({[name]: value});
            $.extend(this.state, {[name]: value});
        }
    }

    bubbleStateChange(orig_event) {
        let params = {bubbles: true, detail: {'data': this.state, 'src': null}}
        if (orig_event !== undefined) {
            orig_event.preventDefault();
            orig_event.stopPropagation();

            if (orig_event.target.tagName === 'INPUT') {
                params.detail.src = orig_event.target.name || "";
            }

            params.detail.forceUpdate = true;
        } else {
            params.detail.forceUpdate = false;
        }

        let event = new CustomEvent('StateChange', params);
        this.base.dispatchEvent(event);
    }

    bubbleSubmit(ev) {
        ev.preventDefault();
        ev.stopPropagation();
        let params = {bubbles: true, detail: {'data': this.state}};

        if (ev.target.tagName === 'INPUT') {
            params.detail.src = ev.target.name || "";
        }

        params.detail.forceUpdate = true;
        let event = new CustomEvent('StateChange', params);
        this.base.dispatchEvent(event);
    }

    handleSubmit(event) {
        event.preventDefault();

        if (event.submitter.name) {
            this.state[event.submitter.name] = ''
        }

        let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': true}});
        this.base.dispatchEvent(e);

        fetch(this.props.action || window.location, {
            method: 'POST',
            body: this.formData,
            redirect: "manual"
        }).then(resp => {
            resp.text().then(data => {
               if (resp.status === 403) {
                    let d = evaluate(data);
                    this.props.children = d.props.children;
                    this.forceUpdate();

                    let e = new CustomEvent('AjaxLoading', {'bubbles': true, 'detail': {'loading': false}});
                    this.base.dispatchEvent(e);
                } else if (resp.status === 340) {
                    window.location.replace(resp.headers.get('Location'));
                }
            });
        }).catch(error => {

        });
        /*$.post({
            url: this.props.action || window.location,
            data: $.param(this.state, true),
            statusCode: {
                340: function (resp) {
                    window.location.replace(resp.getResponseHeader('location'));
                }
            }
        }).done((resp, status, xhr) => {
            let dom = resp;
            this.dataToCreateElement([dom]);
            this.props.children = dom[2];
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
            } else if (resp.status === 302) {
                console.log(resp)
            }
        });*/
    }

    doRender() {
        return <form {...this.props} onHandleInputChange={this.handleInputChange}>
            {this.props.children}
        </form>
    }

    componentDidMount() {
        if (this.props.didMountCallback) {
            this.bubbleStateChange();
        }
    }
}

registry.register('kr-form', Form);
export { Form }