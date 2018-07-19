import React, {Fragment} from 'react'
import {Field, reduxForm} from 'redux-form'
import { connect } from 'react-redux';
import validate from './validate'
import renderField from './renderField'
import moment from 'moment'
import { DatePicker, Form, Input, Radio, Select, Checkbox, Button } from "antd";

const FormItem = Form.Item;
const RadioGroup = Radio.Group;
const { Option } = Select;
const { TextArea } = Input;

const formItemLayout = {
  labelCol: {
    xs: { span: 24 },
    sm: { span: 12 }
  },
  wrapperCol: {
    xs: { span: 24 },
    sm: { span: 14 }
  }
};

const tailFormItemLayout = {
  wrapperCol: {
    xs: {
      span: 24,
      offset: 0
    },
    sm: {
      span: 14,
      offset: 6
    }
  }
};
const required = value => {
  return (value ? undefined : 'Required')
}
const isNumber = value => {
  return (!isNaN(value) ? undefined : 'Must be number')
}
const makeField = Component => ({ input, meta, children, hasFeedback, label, ...rest }) => {
  const hasError = meta.touched && meta.invalid;
  return (
    <FormItem
      {...formItemLayout}
      label={label}
      validateStatus={hasError ? 'error' : 'success'}
      hasFeedback={hasFeedback && hasError}
      help={hasError && meta.error}
    >
      <Component {...input} {...rest} children={children} />
    </FormItem>
  );
};
const makeDatePickerField = Component => ({ input, meta, children, hasFeedback, label, ...rest }) => {
  const hasError = meta.touched && meta.invalid;
  return (
    <FormItem
      {...formItemLayout}
      label={label}
      validateStatus={hasError ? 'error' : 'success'}
      hasFeedback={hasFeedback && hasError}
      help={hasError && meta.error}
    >
      <Component {...rest} value={input.value !== "" ? moment(input.value, 'YYYY-MM-DD') : input.value} format='YYYY-MM-DD' onChange={(date, dateString) => input.onChange(dateString)} children={children} />
    </FormItem>
  );
};
const AInput = makeField(Input);
const ARadioGroup = makeField(RadioGroup);
const ASelect = makeField(Select);
const ACheckbox = makeField(Checkbox);
const ATextarea = makeField(TextArea);
const ADatePicker = makeDatePickerField(DatePicker);

let WizardFormPage = props => {
  const {handleSubmit,  pristine, reset, submitting, onSubmit, previousPage, nextPage, question, finalSubmit} = props

  return (
      <form onSubmit={handleSubmit}>
        {question[0].type == 'string' &&
          <Field
            name={question[0].id}
            component={AInput}
            label={question[0].text}
            validate={required}
            hasFeedback
          />
        }
        {question[0].type == 'date' &&
          <Field
            name={question[0].id}
            component={ADatePicker}
            label={question[0].text}
            validate={required}
            hasFeedback
          />
        }
        {question[0].type == 'number' &&
          <Field
            name={question[0].id}
            component={AInput}
            label={question[0].text}
            validate={isNumber}
            hasFeedback
          />
        }
        {question[0].type == 'boolean' &&
          <Field
            name={question[0].id}
            component={ARadioGroup}
            label={question[0].text}
            validate={required}
            hasFeedback
          >
            <Radio value="yes">Yes</Radio>
            <Radio value="no">No</Radio>
          </Field>
        }
        <div>
          {previousPage &&
            <Button htmlType="button" className="previous" onClick={previousPage}>
              Previous
            </Button>
          }
          { question[0].next !== null &&
            <Button htmlType="submit" className="next">Next</Button>
          }
          { question[0].next === null &&
            <Button htmlType="submit" onClick={finalSubmit} className="submit">Submit</Button>
          }
        </div>
      </form>
  )
}

WizardFormPage = reduxForm({
  form: 'wizard', // <------ same form name
  destroyOnUnmount: false, // <------ preserve form data
  forceUnregisterOnUnmount: true, // <------ unregister fields on unmount
})(WizardFormPage)

WizardFormPage = connect()(WizardFormPage);
export default WizardFormPage
