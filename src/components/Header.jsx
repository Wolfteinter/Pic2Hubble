import React from 'react';
import { Navbar, Container} from 'react-bootstrap';
import hubble from '../images/hubble.png';
export function Header() {
    return (
        <Navbar collapseOnSelect fixed='top' expand='lg' bg='dark' variant='dark'>
            <Container>
                <Navbar id='responsive-navbar-nav'>
                    <img src ={hubble}
                    width="40"
                    height="40"/>
                    <Navbar.Brand href="#home">Hubble 2 pic</Navbar.Brand>
                </Navbar>
            </Container>
        </Navbar>
    );
}