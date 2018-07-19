import React from 'react'
import PropTypes from 'prop-types'
import WizardFormPage from './WizardFormPage'
import { connect } from 'react-redux';
import { finalSubmitForm} from '../../containers/App/actions';

export class WizardForm extends React.Component {
  constructor(props) {
    super(props)
    this.nextPage = this.nextPage.bind(this)
    this.previousPage = this.previousPage.bind(this)
    this.finalSubmit = this.finalSubmit.bind(this)
    this.state = {
      page: 0,
    }
  }
  componentDidMount() {
    let totalQuestions = ["A01"]
    let wizardFormArray = [<WizardFormPage {...this.props} className="firstForm" page="0" onSubmit={this.nextPage} nextPage={this.nextPage} question={ this.props.questions ? this.props.questions.filter(question => question.id=="A01") : {}} />]
    if(this.props.questions) {

      this.props.questions.map((question, index) => {
        if(question.next != null && !totalQuestions.includes(question.next)) {
          totalQuestions.push(question.next)
          wizardFormArray.push(
            <WizardFormPage
              page={index+1}
              question={this.props.questions.filter(questionn => questionn.id==question.next)}
              previousPage={this.previousPage}
              nextPage={this.nextPage}
              onSubmit={this.nextPage}
              finalSubmit={this.finalSubmit.bind(this)}
              {...this.props}
            />)
        }
      })
      wizardFormArray.push(
        <div>
          <h2>Thank you! We will get back to you soon!</h2>
        </div>
      )
    }
    this.setState({wizardFormArray: wizardFormArray})
    const totalQuestionsNumber = totalQuestions.length
  }
  finalSubmit() {
    this.props.finalSubmitForm()
  }
  nextPage() {
    this.setState({page: this.state.page + 1})
  }

  previousPage() {
    this.setState({page: this.state.page - 1})
  }

  render() {
    const {page} = this.state
    return (
      <div className="WizardFormPage">
        {(!this.state.submitted && this.state.wizardFormArray) && this.state.wizardFormArray[this.state.page]}
        { this.props.submitted && Object.keys(this.props.formValue).map(key => {
          return <h3>{`${this.props.questions.filter(question => question.id === key)[0].text}:`}<br/>{`${this.props.formValue[key]}`}</h3>
        })}
      </div>
    )
  }
}

const mapStateToProps = (state, ownProps) => {
  return {
    submitted: state.global.submitted,
  }
}
const mapDispatchToProps = (dispatch, ownProps) => {
  return {
    dispatch,
    finalSubmitForm: () => dispatch(finalSubmitForm()),
  }
}

export default connect(mapStateToProps, mapDispatchToProps)(WizardForm)
