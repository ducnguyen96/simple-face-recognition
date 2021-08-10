// File Upload
//
function ekUpload() {
  function Init() {
    console.log("Upload Initialized");

    var fileSelect = document.getElementById("file-upload"),
      fileDrag = document.getElementById("file-drag"),
      submitButton = document.getElementById("submit-button");

    fileSelect.addEventListener("change", fileSelectHandler, false);

    // Is XHR2 available?
    var xhr = new XMLHttpRequest();
    if (xhr.upload) {
      // File Drop
      fileDrag.addEventListener("dragover", fileDragHover, false);
      fileDrag.addEventListener("dragleave", fileDragHover, false);
      fileDrag.addEventListener("drop", fileSelectHandler, false);
    }
  }

  function fileDragHover(e) {
    var fileDrag = document.getElementById("file-drag");

    e.stopPropagation();
    e.preventDefault();

    fileDrag.className =
      e.type === "dragover" ? "hover" : "modal-body file-upload";
  }

  function fileSelectHandler(e) {
    // remove old frame
    const frame = document.getElementById("frame");
    if (frame) frame.remove();

    // Fetch FileList object
    var files = e.target.files || e.dataTransfer.files;

    // Cancel event and hover styling
    fileDragHover(e);

    // Process all File objects
    for (var i = 0, f; (f = files[i]); i++) {
      parseFile(f);
      uploadFile(f);
    }
  }

  // Output
  function output(msg) {
    // Response
    var m = document.getElementById("messages");
    m.innerHTML = msg;
  }

  function parseFile(file) {
    output("<strong>" + encodeURI(file.name) + "</strong>");

    // var fileType = file.type;
    // console.log(fileType);
    var imageName = file.name;

    var isGood = /\.(?=gif|jpg|png|jpeg)/gi.test(imageName);
    if (isGood) {
      document.getElementById("start").classList.add("hidden");
      document.getElementById("response").classList.remove("hidden");
      document.getElementById("notimage").classList.add("hidden");
      // Thumbnail Preview
      document.getElementById("file-image").classList.remove("hidden");
      document.getElementById("file-image").src = URL.createObjectURL(file);
    } else {
      document.getElementById("file-image").classList.add("hidden");
      document.getElementById("notimage").classList.remove("hidden");
      document.getElementById("start").classList.remove("hidden");
      document.getElementById("response").classList.add("hidden");
      document.getElementById("file-upload-form").reset();
    }
  }

  function setProgressMaxValue(e) {
    var pBar = document.getElementById("file-progress");

    if (e.lengthComputable) {
      pBar.max = e.total;
    }
  }

  function updateFileProgress(e) {
    var pBar = document.getElementById("file-progress");

    if (e.lengthComputable) {
      pBar.value = e.loaded;
    }
  }

  function uploadFile(file) {
    var xhr = new XMLHttpRequest(),
      // fileInput = document.getElementById("class-roster-file"),
      pBar = document.getElementById("file-progress"),
      fileSizeLimit = 1024; // In MB
    if (xhr.upload) {
      // Check if file is less than x MB
      if (file.size <= fileSizeLimit * 1024 * 1024) {
        // Progress bar
        pBar.style.display = "inline";
        xhr.upload.addEventListener("loadstart", setProgressMaxValue, false);
        xhr.upload.addEventListener("progress", updateFileProgress, false);

        // File received / failed
        xhr.onreadystatechange = function (e) {
          if (xhr.readyState == 4) {
            // Everything is good!
            // progress.className = xhr.status == 200 ? "success" : "failure";
            // document.location.reload(true);
            const clientImage = document.getElementById("file-image");
            const changePercent =
              clientImage.clientWidth / clientImage.naturalWidth;

            const response = JSON.parse(e.target.response);
            const anchor = response["anchor"];
            const allNames = response["all_names"];
            const allProbability = response["all_probability"];
            const classIndex = response["class_index"];
            const classProbability = response["class_probability"];

            const frame = document.createElement("div");
            frame.id = "frame";
            frame.style.width = `${anchor[2] * changePercent}px`;
            frame.style.height = `${anchor[2] * changePercent}px`;
            frame.style.border = `3px solid green`;
            frame.style.position = "absolute";
            frame.style.top = `calc(${anchor[1] * changePercent}px)`;
            frame.style.left = `calc(${anchor[0] * changePercent}px)`;

            const fileDrag = document.getElementById("image-wrapper");
            fileDrag.appendChild(frame);

            // Update response
            const messages = document.querySelector("#messages > strong");
            messages.innerHTML =
              allNames[+classIndex] === "the_boss"
                ? "Thiên Hạ Đệ Nhất Đẹp Trai Văn Đức"
                : allNames[+classIndex];
          }
        };

        // Start upload
        xhr.open(
          "POST",
          document.getElementById("file-upload-form").action,
          true
        );
        xhr.setRequestHeader("X-File-Name", file.name);
        xhr.setRequestHeader("X-File-Size", file.size);
        // xhr.setRequestHeader("Content-Type", "multipart/form-data");

        const formData = new FormData();
        formData.append("img", file);
        xhr.send(formData);
      } else {
        output("Please upload a smaller file (< " + fileSizeLimit + " MB).");
      }
    }
  }

  // Check for the various File API support.
  if (window.File && window.FileList && window.FileReader) {
    Init();
  } else {
    document.getElementById("file-drag").style.display = "none";
  }
}
window.onload = () => {
  ekUpload();
};
