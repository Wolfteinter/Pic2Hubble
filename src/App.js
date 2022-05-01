import React, { useState } from "react";
import FileUpload from "./components/file-upload/file-upload.component";
import { Header } from "./components/Header";
import 'bootstrap/dist/css/bootstrap.css';
import './App.css';
import ReactLoading from "react-loading";
import { saveAs } from 'file-saver'

function App() {
    const [newUserInfo, setNewUserInfo] = useState({
        profileImages: null
    });
    const [done, setDone] = useState(false);
    const [doneImage, setDoneImage] = useState(false);
    const [image, setImage] = useState('');

    const updateUploadedFiles = (files) =>
        setNewUserInfo({ ...newUserInfo, profileImages: files });

    const handleSubmit = (event) => {
        event.preventDefault();
        // console.log(newUserInfo);
    };
    const getResponse = async () => {
        const formData = new FormData();
        formData.append('image', newUserInfo.profileImages);
        const api_url = "https://pic2hubble.herokuapp.com/v1.0/generator"
        // const api_url = "http://localhost:5000/v1.0/generator"
        const api_call = await fetch(api_url, {
            method: 'POST',
            body: formData
        });

        const data = await api_call.json();
        // console.log(data);
        setImage(data.image);
        setDone(false);
        setDoneImage(true);

    }
    const convertImage = () => {
        setDone(true);
        setDoneImage(false);
        getResponse();
    }

    const getFilename = ()  => {
        let d = new Date();
        let dformat = `${d.getHours()}_${d.getMinutes()}`;

        return "pic2hubble_" + dformat + ".png";
    }

    const downloadImage = () => {
        let filename = getFilename();
        saveAs( "data:image/png;base64,"+image, filename);
    }

    return (
        <div>
            <Header />
            <form className='iform' onSubmit={handleSubmit} style={{ marginTop: 60 }}>
                {doneImage ? (
                    <>
                        <button onClick={downloadImage} className="bn632-hover bn22">Download</button>
                        <img src={`data:image/jpeg;base64,${image}`} />
                    </>

                ) : (
                    <>
                        <FileUpload
                            accept=".jpg,.png,.jpeg"
                            label="Image to process"
                            multiple
                            updateFilesCb={updateUploadedFiles}
                        />
                        {done ? (
                            <ReactLoading
                                type={"bars"}
                                color={"#03fc4e"}
                                height={100}
                                width={100}
                            />
                        ) : (
                            <main>
                                <button onClick={convertImage} className="bn632-hover bn22">Convert image</button>
                            </main>
                        )}
                    </>
                )}
            </form>
        </div>
    );
}

export default App;