import { DatePicker } from '@ui5/webcomponents-react';
import {Component} from "../../../core/component";
import {Fragment, h} from "preact";
import {registry} from "../../../core/registry";


class DateInput extends Component {
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
                'type': this.props.type,
                'name': this.props.name,
                'value': ev.detail.value
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
            <DatePicker
                value-state={valueState}
                value={this.props.value}
                className={cls}
                onChange={this.handleChange}
                onInput={function noRefCheck(){}}
                primaryCalendarType="Gregorian"
                formatPattern="YYYY-MM-dd"
                style={{width: '100%'}}
                hideWeekNumbers={true}
            />
            <div class="invalid-feedback">{this.props.error}</div>
        </Fragment>;
    }
}

registry.register('kr-date-input', DateInput);

export { DateInput };

