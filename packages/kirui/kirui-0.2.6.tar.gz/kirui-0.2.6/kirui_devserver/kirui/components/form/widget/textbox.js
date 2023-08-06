import { Editor } from '@tinymce/tinymce-react';
import { Component } from "../../../core/component";
import {Fragment, h} from "preact";
import { registry } from "../../../core/registry";


class RichTextBox extends Component {
    constructor() {
        super();
        this.handleChange = this.handleChange.bind(this);
    }

    beforeRender() {
        super.beforeRender();
        if (this.props.value) {
            let event = {
                target: {
                    'type': this.props.type,
                    'name': this.props.name,
                    'value': this.props.value
                }
            }
            this.props.onChange(event);
        }
    }

    handleChange(ev) {
        let event = {
            target: {
                'type': 'textarea',
                'name': this.props.name,
                'value': ev.target.getContent()
            }
        }
        this.props.onChange(event);
    }

    doRender() {
        let [cls, valueState] = ['', ''];
        if (this.props.error) {
            cls += ' is-invalid'
            valueState = 'Error'
        }

        return <Fragment>
            <Editor
                tinymceScriptSrc="https://cdnjs.cloudflare.com/ajax/libs/tinymce/4.8.2/tinymce.min.js"
                init={{
                    height: this.props.height || 400,
                    menubar: false,
                    branding: false,
                    plugins: 'table',
                    toolbar: 'undo redo | formatselect | ' +
                        'bold italic backcolor | alignleft aligncenter ' +
                        'alignright alignjustify | bullist numlist outdent indent | ' +
                        'table',
                    content_style: 'body { font-family: Helvetica,Arial,sans-serif; font-size:14px }',
                }}
                onChange={this.handleChange}
                initialValue={this.props.value}
            />
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-rich-textbox', RichTextBox);

export { RichTextBox };
