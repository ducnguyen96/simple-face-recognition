// File Upload
//
function capitalize(word) {
  return word[0].toUpperCase() + word.slice(1).toLowerCase();
}

const transferClassName = (str) => {
  const words = str.split("_").map((w) => capitalize(w));
  return words.join(" ");
};
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

    // remove old top5
    const top5 = document.getElementById("top5");
    if (top5) top5.remove();

    // remove old infobox
    const infobox = document.querySelector("table.infobox");
    if (infobox) infobox.remove();

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
            const namesTop5 = response["names_top5"];
            const probTop5 = response["prob_top5"];

            // Add Frame
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
              namesTop5[0] === "the_boss"
                ? "Thiên Hạ Đệ Nhất Đẹp Trai Văn Đức"
                : transferClassName(namesTop5[0]);

            // Add Top 5
            const top5Div = document.createElement("ol");
            top5Div.id = "top5";
            top5Div.style.padding = 0;
            // top5Div.style.display = "flex";
            // top5Div.style.justifyContent = "space-between";
            namesTop5.forEach((name, index) => {
              const elem = document.createElement("li");
              elem.innerHTML = `${transferClassName(name)} (${probTop5[
                index
              ].toFixed(2)} %)`;
              top5Div.appendChild(elem);
            });

            if (namesTop5[0] === "the_boss") return;

            const fileUpload = document.getElementById("file-drag");
            fileUpload.appendChild(top5Div);

            // Update detail
            let search_endpoint = "https://en.wikipedia.org/w/api.php";

            const search_params = {
              action: "query",
              list: "search",
              srsearch: transferClassName(namesTop5[0]),
              srlimit: "1",
              format: "json",
            };

            search_endpoint = search_endpoint + "?origin=*";
            Object.keys(search_params).forEach(function (key) {
              search_endpoint += "&" + key + "=" + search_params[key];
            });

            fetch(search_endpoint)
              .then(function (response) {
                return response.json();
              })
              .then(function (response) {
                const title = response.query.search[0].title;
                queryWikipediaPage(title);
              })
              .catch(function (error) {
                console.log(error);
              });
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

const queryWikipediaPage = (title) => {
  let endpoint = "https://en.wikipedia.org/w/api.php";

  const params = {
    action: "parse",
    page: title.replace(" ", "_"),
    prop: "text",
    formatversion: 2,
    format: "json",
  };

  endpoint = endpoint + "?origin=*";
  Object.keys(params).forEach(function (key) {
    endpoint += "&" + key + "=" + params[key];
  });

  fetch(endpoint)
    .then(function (response) {
      return response.json();
    })
    .then(function (response) {
      const bodyDOM = response["parse"]["text"];
      const fakeDOM = document.createElement("div");
      fakeDOM.innerHTML = bodyDOM;
      const infoBox = fakeDOM.querySelector(".infobox.vcard");
      const infoBoxAbove = infoBox.querySelector(".infobox-above");
      if (infoBoxAbove) infoBoxAbove.remove();

      const form = document.getElementById("file-upload-form");
      form.appendChild(infoBox);
    })
    .catch(function (error) {
      console.log(error);
    });
};
window.onload = () => {
  ekUpload();
};
