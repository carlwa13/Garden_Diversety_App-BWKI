var constraints = { video: { facingMode: "user" }, audio: false };
const cameraView = document.querySelector("#camera--view"),
    cameraOutput = document.querySelector("#camera--output"),
    cameraSensor = document.querySelector("#camera--sensor"),
    cameraTrigger = document.querySelector("#camera--trigger")
    
function cameraStart() {
    navigator.mediaDevices
        .getUserMedia(constraints)
        .then(function(stream) {
        track = stream.getTracks()[0];
        cameraView.srcObject = stream;
    })
    .catch(function(error) {
        console.error("ouu noo", error);
    });
}

cameraTrigger.onclick = function() {
    cameraSensor.width = cameraView.videoWidth;
    cameraSensor.height = cameraView.videoHeight;
    cameraSensor.getContext("2d").drawImage(cameraView, 0, 0);
    cameraOutput.src = cameraSensor.toDataURL("image/webp");
    cameraOutput.classList.add("taken");
	console.log(cameraOutput);
    $.ajax({ 
    	type: "POST",
    	url: "https://168.100.8.7/upload",
    	data: {
    		imgBase64: 	cameraSensor.toDataURL("image/webp")
    	},
    	success: function (data, status, jqXHR) {
    		link = "https://168.100.8.7";
    		 if (data=="gurke"){
    		 	link = "https://168.100.8.7/gurke";
    		 } else if(data=="zucchini"){
    		 	link = "https://168.100.8.7/zucchini";
    		 } else if(data=="tomate"){
    		 	link = "https://168.100.8.7/tomate";
    		 } else if(data=="zuckererbse"){
    		 	link = "https://168.100.8.7/zuckererbse";
    		 }
    		 //link = "https://pornhub.com"
    	     window.location.replace(link);
    	     console.log(data);

    	}
     });
     
};

window.addEventListener("load", cameraStart, false);
