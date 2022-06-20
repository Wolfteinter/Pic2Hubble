import React from 'react';
import GithubIcon from '../images/GitHub-Mark-Light-32px.png';
export function RepoLink() {
    return (
        <button style={{
            borderRadius: '100%',
            width: '4rem',
            height: '4rem',
            position: 'absolute',
            bottom: '2rem',
            right: '2rem',
            backgroundColor: '#111111',
        }} 
        >
            <a href='https://github.com/Wolfteinter/Pic2Hubble' target='_blank'>
                <img src={GithubIcon} alt="Github Icon" />
            </a>
        </button>
    );
}