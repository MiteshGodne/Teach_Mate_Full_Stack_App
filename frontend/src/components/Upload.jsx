import "../css/Upload.css";
import { useState } from "react";
import axios from "axios";

const apiBaseFrontendUrl = import.meta.env.VITE_API_URL + "/upload";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [dragActive, setDragActive] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [isUploading, setIsUploading] = useState(false);
  const [isUploaded, setIsUploaded] = useState(false); // Track upload success
  const [videoUrl, setVideoUrl] = useState(""); // Track generated video URL

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setIsUploaded(false); // Reset uploaded state
    setVideoUrl(""); // Clear previous video link
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(true);
  };

  const handleDragLeave = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setDragActive(false);
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      setFile(e.dataTransfer.files[0]);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) {
      alert("Please upload a file!");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    setIsUploading(true);
    setUploadProgress(0);
    setIsUploaded(false); // Reset uploaded state

    try {
      const response = await axios.post(apiBaseFrontendUrl,
        formData,
        {
          headers: {
            "Content-Type": "multipart/form-data",
          },
          onUploadProgress: (progressEvent) => {
            const percentCompleted = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percentCompleted);
          },
          responseType: "blob", // Receive video as binary
        }
      );

      // Assuming the backend provides the video URL or a download link
      const url = window.URL.createObjectURL(new Blob([response.data]));
      setVideoUrl(url);

      setIsUploaded(true); // Mark as uploaded
      setIsUploading(false); // Stop the uploading state
      setFile(null); // Reset the file state
      setUploadProgress(0); // Reset the progress bar
    } catch (error) {
      console.error("Upload failed:", error);
      alert("Something went wrong!");
      setIsUploading(false);
    }
  };

  const handleRemoveFile = () => {
    setFile(null);
    setUploadProgress(0); // Reset progress
    setIsUploading(false); // Stop any ongoing upload
    setIsUploaded(false); // Reset uploaded state
    setVideoUrl(""); // Clear video URL
  };

  return (
    <div className="upload-page">
      <h1 className="upload-heading">Upload Your PPT</h1>
      <div
        className={`drag-drop-area ${dragActive ? "active" : ""}`}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
      >
        <p>
          {file
            ? `Selected file: ${file.name}`
            : "Drag and drop your PPT file here, or click to upload"}
        </p>
        <input
          type="file"
          accept=".ppt, .pptx"
          onChange={handleFileChange}
          className="file-input"
        />
      </div>

      {file && (
        <div className="action-buttons">
          <button
            type="submit"
            className="upload-button"
            onClick={handleSubmit}
            disabled={isUploading || isUploaded}
          >
            {isUploading ? "Uploading..." : isUploaded ? "Uploaded" : "Upload"}
          </button>
          <button
            type="button"
            className="remove-button"
            onClick={handleRemoveFile}
            disabled={isUploading}
          >
            Remove File
          </button>
        </div>
      )}

      {isUploading && (
        <div className="progress-bar">
          <div className="progress" style={{ width: `${uploadProgress}%` }}></div>
        </div>
      )}

      {isUploaded && videoUrl && (
        <div>
          <h2>Video Generated!</h2>
          <video controls>
            <source src={videoUrl} type="video/mp4" />
            Your browser does not support the video tag.
          </video>
          <a href={videoUrl} download="generated_video.mp4">
            Download Video
          </a>
        </div>
      )}
    </div>
  );
};

export default Upload;


























// // src/pages/UploadPage.jsx
// import "../css/Upload.css"
// import { useState } from "react";
// import axios from "axios";
// import VideoPlayer from "../components/VideoPlayer";
// // src/pages/UploadPage.jsx


// const Upload = () => {
//   const [file, setFile] = useState(null);
//   const [dragActive, setDragActive] = useState(false);
//   const [uploadProgress, setUploadProgress] = useState(0);
//   const [isUploading, setIsUploading] = useState(false);
//   const [videoUrl, setVideoUrl] = useState("");

//   const handleFileChange = (e) => {
//     setFile(e.target.files[0]);
//   };

//   const handleDragOver = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(true);
//   };

//   const handleDragLeave = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(false);
//   };

//   const handleDrop = (e) => {
//     e.preventDefault();
//     e.stopPropagation();
//     setDragActive(false);
//     if (e.dataTransfer.files && e.dataTransfer.files[0]) {
//       setFile(e.dataTransfer.files[0]);
//     }
//   };

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     if (!file) {
//       alert("Please upload a file!");
//       return;
//     }

//     const formData = new FormData();
//     formData.append("file", file);

//     setIsUploading(true);
//     setUploadProgress(0);

//     try {
//       const response = await axios.post(
//         "http://localhost:8000/upload/",
//         formData,
//         {
//           headers: {
//             "Content-Type": "multipart/form-data",
//           },
//           onUploadProgress: (progressEvent) => {
//             const percentCompleted = Math.round(
//               (progressEvent.loaded * 100) / progressEvent.total
//             );

//             setUploadProgress(percentCompleted);
//           },
//           responseType: "blob", // so we can receive the video as binary
//         }
//       );
//       // if (file) {
//       //   // Simulate the upload process with a fake progress bar
//       //   setIsUploading(true);
//       //   let progress = 0;
//       //   const uploadInterval = setInterval(() => {
//       //     progress += 10;
//       //     setUploadProgress(progress);
//       //     if (progress >= 100) {
//       //       clearInterval(uploadInterval);
//       //       setIsUploading(false);
//       //       alert('File uploaded successfully!');
//       //     }
//       //   }, 300); // Simulate upload progress
//       // }

//       const videoBlob = new Blob([response.data], { type: "video/mp4" });
//       const videoObjectUrl = URL.createObjectURL(videoBlob);
//       setVideoUrl(videoObjectUrl);
//       // // Create downloadable link
//       // const url = window.URL.createObjectURL(new Blob([response.data]));
//       // const a = document.createElement("a");
//       // a.href = url;
//       // a.download = "lecture.mp4";
//       // a.click();
//       // a.remove();

//       alert("Video generated and downloaded!");
//     } catch (error) {
//       console.error("Upload failed:", error);
//       alert("Something went wrong!");
//     } finally {
//       setIsUploading(false);
//       setUploadProgress(0);
//       setFile(null);
//     }
//   }

//   const handleRemoveFile = () => {
//     setFile(null);
//     setUploadProgress(0); // Reset progress
//     setIsUploading(false); // Stop any ongoing upload
//     setVideoUrl(""); // Clear video
//   };

//   return (
//     <div className="upload-page">
//       <h1 className="upload-heading">Upload Your PPT</h1>
//       <div
//         className={`drag-drop-area ${dragActive ? 'active' : ''}`}
//         onDragOver={handleDragOver}
//         onDragLeave={handleDragLeave}
//         onDrop={handleDrop}
//       >
//         <p>{file ? `Selected file: ${file.name}` : 'Drag and drop your PPT file here, or click to upload'}</p>
//         <input type="file" accept=".ppt, .pptx" onChange={handleFileChange} className="file-input" />
//       </div>

//       {file && (
//         <div className="action-buttons">
//           <button type="submit" className="upload-button" onClick={handleSubmit} disabled={isUploading}>
//             {isUploading ? 'Uploading...' : 'Upload'}
//           </button>
//           <button type="button" className="remove-button" onClick={handleRemoveFile} disabled={isUploading}>
//             Remove File
//           </button>
//         </div>
//       )}

//       {isUploading && (
//         <div className="progress-bar">
//           <div className="progress" style={{ width: `${uploadProgress}%` }}></div>
//         </div>
//       )}
//       {/* Render the video below the uploader */}
//       {videoUrl && (
//         <div className="video-preview mt-6 text-center">
//           <h2 className="text-xl font-semibold mb-2">Your Generated Lecture</h2>

//           <VideoPlayer videoUrl={videoUrl} />
//           <a
//             href={videoUrl}
//             download="lecture.mp4"
//             className="inline-block mt-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 transition"
//           >
//             Download Video
//           </a>
//         </div>
//       )}
//     </div>
//   );
// };
// export default Upload;
