import { useState } from 'react';
import {Button, Form, Input} from "semantic-ui-react";
import {userLogin} from "../apiCalls";
import styled from "styled-components";


const LoginForm = styled.div`
  width: 100vw;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
`


interface Props {
  setToken: (userToken: string) => void
}

function Login(props: Props) {

  const { setToken } = props

  const [loginForm, setloginForm] = useState({
    username: "",
    password: ""
  })

  function logMeIn(event: any) {
    userLogin({
      email: loginForm.username,
      password: loginForm.password
    })
      .then((response) => {
        setToken(response.data.access_token)
      }).catch((error) => {
      if (error.response) {
        console.log(error.response)
        console.log(error.response.status)
        console.log(error.response.headers)
      }
    })

    setloginForm(({
      username: "",
      password: ""}))

    event.preventDefault()
  }

  function handleChange(event: any) {
    const {value, name} = event.target
    setloginForm(prevNote => ({
      ...prevNote, [name]: value})
    )}

  return (
    <LoginForm>
      <Form className="flex-column" style={{width: '100%', height: '100%'}}>
        {Object.keys(loginForm).map(name => (
          <Form.Field
            width={3}
            onChange={handleChange}
            control={Input}
            label={name}
            placeholder={name}
            name={name}
            // @ts-ignore
            value={loginForm[name]}
          />
        ))}
        <Form.Field
          style={{alignSelf: 'flex-start'}}
          onClick={logMeIn}
          control={Button}
          type="submit"
        >
          Submit
        </Form.Field>
      </Form>
    </LoginForm>
  );
}

export default Login;