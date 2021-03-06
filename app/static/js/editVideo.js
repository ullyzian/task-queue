import { getVideoTaskDiv, updateProgress, getRandom } from "./script.js";

// init local storage
if (localStorage.getItem("processVideo") == null) {
  localStorage.setItem("processVideo", "{}");
}

// get local storage task list
let processVideoDict = JSON.parse(localStorage.getItem("processVideo"));

// display all previous tasks
if (Object.keys(processVideoDict) != null) {
  Object.keys(processVideoDict).forEach((url) => {
    let div = getVideoTaskDiv(getRandom(10000), processVideoDict[url]);
    updateProgress(url, div[0]);
    $(".task-list").prepend(div);
  });
}

// display selected file
$(".custom-file-input").change((e) => {
  let fileName = $("#inputGroupFile02").val().split("\\").pop();
  $(".custom-file-label").text(fileName);
});

// start task
$("#inputGroupFileAddon04").click(() => {
  // //get video file
  var formData = new FormData($("#upload-video")[0]);
  var optionData = $("#edit-options").serializeArray();
  optionData.forEach((e) => {
    formData.append(e.name, e.value)
  })

  // check video file
  if (!formData.get("file")["name"].localeCompare("")) {
    $("#errors-input").empty();
    $("#errors-input").append("<div class='alert alert-danger' role='alert'>You didn't select video file.</div");
    return null
  } else {
    $("#errors-input").empty();
  }

  // add progress
  let div = getVideoTaskDiv(getRandom(10000), "#");
   $(".task-list").prepend(div);

   // start task update
  $.ajax({
    type: "POST",
    url: window.location.pathname,
    data: formData,
    processData: false,
    contentType: false,
    cache: false,
    success: function (data, status, request) {
      let status_url = request.getResponseHeader("location");
      processVideoDict[status_url] = null;
      localStorage.setItem("processVideo", JSON.stringify(processVideoDict));
      updateProgress(status_url, div[0]);
    },
    error: function (request, status, error) {
      alert(request.status + " " + error);
    },
  });
});
