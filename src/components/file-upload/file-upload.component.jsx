import React, { useRef, useState } from "react";
import {
    FileUploadContainer,
    FormField,
    DragDropText,
    UploadFileBtn,
    FilePreviewContainer,
    ImagePreview,
    PreviewContainer,
    PreviewList,
    FileMetaData,
    RemoveFileIcon,
    InputLabel
} from "./file-upload.styles";

const KILO_BYTES_PER_BYTE = 2000;
const DEFAULT_MAX_FILE_SIZE_IN_BYTES = 900000;

const convertNestedObjectToArray = (nestedObj) =>
    Object.keys(nestedObj).map((key) => nestedObj[key]);

const convertBytesToKB = (bytes) => Math.round(bytes / KILO_BYTES_PER_BYTE);

const FileUpload = ({
    label,
    updateFilesCb,
    maxFileSizeInBytes = DEFAULT_MAX_FILE_SIZE_IN_BYTES,
    ...otherProps
}) => {
    const fileInputField = useRef(null);
    const [files, setFiles] = useState({});

    const handleUploadBtnClick = () => {
        fileInputField.current.click();
    };

    const addNewFiles = (newFiles) => {
        if (Object.keys(files).length == 0) {
            for (let file of newFiles) {
                if (file.size <= maxFileSizeInBytes) {
                    if (!otherProps.multiple) {
                        return { file };
                    }
                    files[file.name] = file;
                }
            }
            return { ...files };
        }
    };

    const callUpdateFilesCb = (files) => {
        //const filesAsArray = convertNestedObjectToArray(files);
        updateFilesCb(files);
    };

    const handleNewFileUpload = (e) => {
        if (Object.keys(files).length == 0) {
            const { target: { files } } = e;
            let images = e.target.files;
            console.log(images);
            if (files.length) {
                let updatedFiles = addNewFiles(images);
                setFiles(updatedFiles);
                updateFilesCb(e.target.files[0]);
            }
        }
    };

    const removeFile = (fileName) => {
        delete files[fileName];
        setFiles({ ...files });
        callUpdateFilesCb({ ...files });
    };

    return (
        <>
            <FileUploadContainer>
                <h3>Drag and drop your pic</h3>

                <h6>Non-profit project. Submitted and generated images are not being stored.</h6>
                    
                <UploadFileBtn type="button" onClick={handleUploadBtnClick}>
                    <i className="fas fa-file-upload" />
                    <span> Upload {otherProps.multiple ? "files" : "a file"}</span>
                </UploadFileBtn>
                <FormField
                    type="file"
                    ref={fileInputField}
                    onChange={handleNewFileUpload}
                    title=""
                    value=""
                    {...otherProps}
                />
            </FileUploadContainer>
            <FilePreviewContainer>
                <PreviewList>
                    {Object.keys(files).map((fileName, index) => {
                        let file = files[fileName];
                        let isImageFile = file.type.split("/")[0] === "image";
                        return (
                            <PreviewContainer key={fileName}>
                                <div>
                                    {isImageFile && (
                                        <ImagePreview
                                            src={URL.createObjectURL(file)}
                                            alt={`file preview ${index}`}
                                        />
                                    )}
                                    <FileMetaData isImageFile={isImageFile}>
                                        <span>{file.name}</span>
                                        <aside>
                                            <span>{convertBytesToKB(file.size)} kb</span>
                                            <RemoveFileIcon
                                                className="fas fa-trash-alt"
                                                onClick={() => removeFile(fileName)}
                                            />
                                        </aside>
                                    </FileMetaData>
                                </div>
                            </PreviewContainer>
                        );
                    })}
                </PreviewList>
            </FilePreviewContainer>
        </>
    );
};

export default FileUpload;