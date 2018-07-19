import React from 'react';
import { FormattedMessage } from 'react-intl';

import A from './A';
import H1 from 'components/H1'
import Img from './Img';
import NavBar from './NavBar';
import HeaderLink from './HeaderLink';
// import Banner from './simplesurance.jpg';
import messages from './messages';

// <A href="https://www.simplesurance.com/">
//   <Img src="https://www.simplesurance.com/wp-content/uploads/simplesurance_logo.jpg" alt="react-boilerplate - Logo" />
// </A>
class Header extends React.Component { // eslint-disable-line react/prefer-stateless-function
  render() {
    return (
      <div>
        <A href="/">
          <H1 style={{margin: '0 auto', textAlign: 'center', fontSize: '50px'}}>Face To Music Plalylist</H1>
        </A>
        <NavBar>
          <HeaderLink to="/">
            <FormattedMessage {...messages.home} />
          </HeaderLink>
          <HeaderLink to="/features">
            <FormattedMessage {...messages.features} />
          </HeaderLink>
        </NavBar>
      </div>
    );
  }
}

export default Header;
