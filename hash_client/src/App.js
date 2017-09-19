import React, { Component } from 'react';
import axios from 'axios';
import './App.css';

class App extends Component {
    constructor() {
        super();
        this.state = {
            hash: '',
            errorMessage: '',
            password: '',
            message: '',
            phrase: '',
            action: ''
        };
        this.handleHash = this.handleHash.bind(this);
    }

    handleHash(event){
        event.preventDefault();
        let self = this;
        axios.post('/hash', {
            message: this.message.value,
            password: this.password.value,
            phrase: this.phrase.value,
            action: this.action.value
        })
            .then(function (response) {
                // console.log(response);
                self.setState({
                    hash: JSON.stringify(response.data)
                });
            })
            .catch(function (error) {
                // console.log(error.response.data);
                self.setState({errorMessage: error.response.data});
            });
    }

  render() {
    return (
        <div id='contact-form'>
          <div>
            <h1>Hash generator</h1>
            <h4>Generate everything with 3 layers of protection!</h4>
          </div>
            <div>
                <textarea value={"Key/ Message :\n"+this.state.hash}></textarea>
            </div>
            <div>
                <h4>You can also use this generator with the api</h4>
                <h5>url: {window.location.href}hash</h5>
                <h5>Post request:
                </h5>
                    <h5>{JSON.stringify({
                    'message': 'example',
                    'password': 'example',
                    'phrase': 'example',
                    'action': 'encrypt'
                })}</h5>
            </div>
          <form onSubmit={this.handleHash.bind(this)} className='topBefore'>
            <div>
              <label for='name'>
                <span className='required'>Message</span>
                <textarea type='text' id='name' name='message' placeholder='Your message' required='required' tabindex='1' ref={c => this.message = c} onChange={this._getCharacterCount.bind(this)}/>
                <p>{this.state.message.length} letters</p>
              </label>
            </div>
            <div>
              <label for='email'>
                <span className='required'>Password</span>
                <input id='email' name='password' placeholder='Your password' tabindex='2' required='required' ref={c => this.password = c} onChange={this._getCharacterCount.bind(this)}/>
                <p>{this.state.password.length} letters</p>
              </label>
            </div>
            <div>
               <label for='email'>
                <span className='required'>Phrase</span>
                <input id='email' name='phrase'  placeholder='Your phrase' tabindex='2' required='required' ref={c => this.phrase = c} onChange={this._getCharacterCount.bind(this)}/>
                <p>{this.state.phrase.length} letters</p>
              </label>
            </div>
            <div>
              <label for='subject'>
                <span>Options</span>
                <select id='subject' name='subject' tabindex='4' ref={c => this.action = c} onChange={this._getCharacterCount.bind(this)}>
                  <option value='encrypt'>Encrypt</option>
                  <option value='decrypt'>Decrypt</option>
                </select>
              </label>
            </div>
            <div>
              <button name='submit' type='submit' id='submit' tabIndex='5' >Generate / Encrypt</button>
            </div>
          </form>

        </div>
    );
  }
    _getCharacterCount(e) {
        this.setState({
            password: this.password.value,
            message: this.message.value,
            phrase: this.phrase.value,
            action: this.action.value,
        });
    }
}

export default App;
