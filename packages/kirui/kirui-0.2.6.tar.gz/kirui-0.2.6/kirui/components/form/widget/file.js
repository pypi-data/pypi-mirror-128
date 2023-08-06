import { Component } from "/kirui/core/component";
import { registry } from "/kirui/core/registry";
import { h, Fragment } from 'preact';


class SimpleFileInput extends Component {
    doRender() {
        let cls = 'form-control'
        if (this.props.error) {
            cls += ' is-invalid'
        }

        if (this.props.value === true) {
            this.props.checked = true;
        }
        return <Fragment>
            <div><input type="file" {...this.props} className={cls} /></div>
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-simple-file', SimpleFileInput);

export { SimpleFileInput };
