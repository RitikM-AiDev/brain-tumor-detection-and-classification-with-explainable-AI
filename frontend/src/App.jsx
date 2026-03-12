import React, { useState } from "react";
import "./App.css";

function UploadImage() {

  const [image, setImage] = useState(null);

  const handleChange = (e) => {
    setImage(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("file", image);

    const response = await fetch("/predict", {
      method: "POST",
      body: formData
    });
    if (response.ok) {
      console.log("sent sucessful");
      const blob = await response.blob();
    const url = window.URL.createObjectURL(blob);

    const a = document.createElement("a");
    a.href = url;
    a.download = "report.pdf";
    document.body.appendChild(a);
    a.click();
    a.remove();
    }
    else {
      console.log("Error");
    }
  };

  return (
    <div style={{ textAlign: "center", marginTop: "100px" }}>
      <h1>BRAIN-TUMOR DETECTOR</h1>
      <h2>Upload Image</h2>

      <form onSubmit={handleSubmit}>
        <input type="file" accept="image/*" onChange={handleChange} />
        <br /><br />

        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default UploadImage;