import { shallow, mount } from 'enzyme';
import React from 'react';
import { Provider } from "react-redux";

jest.mock('react-dom')

import {store} from 'containers/app'
import data from 'containers/App/data.json';
import WizardFormPage from '../WizardFormPage';
import connectedWizardForm, {WizardForm as unConnectedWizardForm} from '../index';

describe('<WizardForm />', () => {
  const props = {
    quesitons: [{
      id: "",
      text: "",
      reply: "",
      type: "",
      next: "",
    }],
    submitted: false,
    finalSubmitForm: jest.fn(),
    formValue: {},
  }
  it('should render one div with .WizardFormPage', () => {
    const renderedComponent = shallow(
      <unConnectedWizardForm />
    );
    expect(renderedComponent.find('.WizardFormPage').length).toBe(1);

  });

  it('should render WizardFormPage firstpage', () => {
    let subject = null
  	let submitting, touched, error, reset, onSave, onSaveResponse, handleSubmit

  	beforeEach(() => {
  		submitting = false
  		touched = false
  		error = null
  		reset = jest.fn()
  		onSaveResponse = Promise.resolve()
  		handleSubmit = fn => fn
  	})
    const props = {
			onSave,
			submitting: submitting,
			// The real redux form has many properties for each field,
			// including onChange and onBlur handlers. We only need to provide
			// the ones that will change the rendered output.
			fields: {
				A01: {
					value: '',
					touched: touched,
					error: error
				}
			},
			handleSubmit,
			reset
		}
    // const firstQuestion = {
    //   id: 'A01',
    //   next: 'A02',
    //   reply: '',
    //   text: 'What happened to your product?',
    //   type: 'string',
    // }
    const html = `<div><ReduxForm page=\"0\" question={{\"id\": \"A01\", \"next\": \"A02\", \"reply\": \"\", \"text\": \"What happened to your product?\", \"type\": \"string\"}} /></div>`
    const text = "What happened to your product?"
    const nextPage = () => {}
    const renderedComponent = shallow(
      <Provider store={store}>
        <connectedWizardForm questions={data.questions} />
      </Provider>
    );
    expect(renderedComponent).toMatchSnapshot();

  });
});
