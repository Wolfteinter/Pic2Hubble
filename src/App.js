import React, { useState } from "react";
import FileUpload from "./components/file-upload/file-upload.component";
import { Header } from "./components/Header";
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';
function App() {
    const [newUserInfo, setNewUserInfo] = useState({
        profileImages: []
    });

    const updateUploadedFiles = (files) =>
        setNewUserInfo({ ...newUserInfo, profileImages: files });

    const handleSubmit = (event) => {
        event.preventDefault();
        console.log(newUserInfo);
    };

    return (
        <div>
            <Header />
            <form className='iform' onSubmit={handleSubmit} style={{ marginTop: 60 }}>
                <FileUpload
                    accept=".jpg,.png,.jpeg"
                    label="Image to process"
                    multiple
                    updateFilesCb={updateUploadedFiles}
                />
                <main>
                    <button className="bn632-hover bn22">Convert image</button>
                </main>
            </form>
        </div>
    );
}

export default App;