let dnaToggle = document.getElementById('dnacToggle')
let merakiToggle = document.getElementById('merakiToggle')

// ------------------- Firebase Config --------------------
let config = {
   //firebase credentials here
};

//Object to hold the current state of the network
let networkInformation = {
    current: {
        meraki: {
            msCount: [0, 0], //Switches
            mxCount: 0, //Firewalls
            mgCount: 0, //Cellular Gateway
            mrCount: 0, //Wireless
            merakiCount: 0,
            devices: {
                online: 0,
                offline: 0,
                os: [0, 0, 0] //[Windows, Mac, Linux]
            }
        },
        dnac: {
            switchCount: 0, //Switches
            apCount: 0, //Access Points
            routerCount: 0, //Routers
            wlcCount: 0, //wireless LAN controller
            ciscoCount: 0,
            devices: {
                online: 0,
                os: [0, 0, 0] //[Windows, Mac, Linux]
            }
        }

    }
}

// Initialize Firebase
firebase.initializeApp(config);
// Get a reference to the database service
var database = firebase.database();

//References meraki and dnac Devices entry in Firebase
var merakiDeviceInfo = firebase.database().ref('/meraki');
var dnacDeviceInfo = firebase.database().ref('/dnac');

// ------------------ Firebase Functions ---------------------
// On meraki database changing
merakiDeviceInfo.on('value', function (snapshot) {
    if (merakiToggle.checked == true) {

        networkInformation.current.meraki.msCount = getLatestInfo(snapshot.val().networkDevices.ms);
        networkInformation.current.meraki.mrCount = getLatestInfo(snapshot.val().networkDevices.mr);
        networkInformation.current.meraki.mxCount = getLatestInfo(snapshot.val().networkDevices.mx);
        networkInformation.current.meraki.mgCount = getLatestInfo(snapshot.val().networkDevices.mg);
        // Add all the above fields
        networkInformation.current.meraki.merakiCount = getLatestInfo(snapshot.val().networkDevices.ms)[0] + getLatestInfo(snapshot.val().networkDevices.mr)[0] + getLatestInfo(snapshot.val().networkDevices.mx)[0] + getLatestInfo(snapshot.val().networkDevices.mg)[0];

        //Grab the device info
        networkInformation.current.meraki.devices.online = getLatestInfo(snapshot.val().networkClients.online);
        networkInformation.current.meraki.devices.offline = getLatestInfo(snapshot.val().networkClients.offline);
        networkInformation.current.meraki.devices.os = [getLatestInfo(snapshot.val().networkClients.OS.Windows), getLatestInfo(snapshot.val().networkClients.OS.Mac), getLatestInfo(snapshot.val().networkClients.OS.Linux)]

        myLineChart.data.datasets[0].data = getLatestFiveEntries(snapshot.val().networkClients.OS.Windows)[0].reverse()
        myLineChart.data.datasets[1].data = getLatestFiveEntries(snapshot.val().networkClients.OS.Mac)[0].reverse()
        myLineChart.data.datasets[2].data = getLatestFiveEntries(snapshot.val().networkClients.OS.Linux)[0].reverse()

        myLineChart.data.labels = getLatestFiveEntries(snapshot.val().networkClients.OS.Windows)[1].reverse()

        $('#inputImage').val(snapshot.val().photoURL)
        
        //call the render function
        renderPage();
    }
});

//On DNAC database changing
dnacDeviceInfo.on('value', function (snapshot) {
    if (dnaToggle.checked == true) {
        networkInformation.current.dnac.apCount = getLatestInfo(snapshot.val().networkDevices.aps);
        networkInformation.current.dnac.switchCount = getLatestInfo(snapshot.val().networkDevices.sw);
        networkInformation.current.dnac.routerCount = getLatestInfo(snapshot.val().networkDevices.routers);
        networkInformation.current.dnac.wlcCount = getLatestInfo(snapshot.val().networkDevices.wlc);

        //grab all device info
        networkInformation.current.dnac.devices.online = getLatestInfo(snapshot.val().networkClients.wired)[0] + getLatestInfo(snapshot.val().networkClients.wireless)[0] ;

        // Add all the above fields
        networkInformation.current.dnac.ciscoCount = getLatestInfo(snapshot.val().networkDevices.aps)[0] + getLatestInfo(snapshot.val().networkDevices.sw)[0] + getLatestInfo(snapshot.val().networkDevices.routers)[0] + getLatestInfo(snapshot.val().networkDevices.wlc)[0];
        renderPage();
    }
});

//render the page 
function renderPage() {
    //networkDevices component render
    networkDevices.message = networkInformation.current.meraki.merakiCount + networkInformation.current.dnac.ciscoCount;

    //Online Component Render
    onlineDevices.message = networkInformation.current.meraki.devices.online[0] + networkInformation.current.dnac.devices.online;
    onlineDevices.date = 'Updated: ' + formatDate(networkInformation.current.meraki.devices.online[1]);

    //Offline Component Render
    offlineDevices.message = networkInformation.current.meraki.devices.offline[0];
    offlineDevices.date = 'Updated: ' + formatDate(networkInformation.current.meraki.devices.offline[1]);

    //Popular OS Component Render
    popularOS.message = findPopularOS(networkInformation.current.meraki.devices.os);
    popularOS.date = 'Updated: ' + formatDate(networkInformation.current.meraki.devices.os[0][1])

    //--------  Update Charts on page -------
    //---- Update Device Histogram ------
    myDeviceChart.data.datasets[0].data[0] = networkInformation.current.meraki.msCount[0] + networkInformation.current.dnac.switchCount[0];
    myDeviceChart.data.datasets[0].data[1] = networkInformation.current.meraki.mxCount[0] + networkInformation.current.dnac.routerCount[0];
    myDeviceChart.data.datasets[0].data[2] = networkInformation.current.meraki.mrCount[0] + networkInformation.current.dnac.apCount[0];
    myDeviceChart.data.datasets[0].data[3] = networkInformation.current.dnac.wlcCount[0];
    
    //update graphs on page
    myDeviceChart.update();
    myLineChart.update();

    //update sentiment
    processImage();

}



//------------------ Graphs on the page -----------------
//Histogram at the left of the page 
var deviceChartContext = document.getElementById('deviceChart').getContext('2d');
var myDeviceChart = new Chart(deviceChartContext, {
    type: 'horizontalBar',
    data: {
        labels: ["", "", "", ""],
        datasets: [{
            barThickness: 400,
            backgroundColor: ["#3e95cd", "#8e5ea2", "#3cba9f", "#e8c3b9", "#c45850"],
            data: [1, 1, 1, 1]
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                ticks: {
                    beginAtZero: true
                },
                barThickness: 'flex'
            }],
            xAxes: [{
                ticks: {
                    beginAtZero: true
                },
                barThickness: 10
            }]
        },
        legend: {
            display: false
        },

        tooltips: {
            callbacks: {
                label: function (tooltipItem) {
                    return tooltipItem.yLabel;
                }
            }
        }
    }
});

//Line chart in the middle 
let osTrendsContext = document.getElementById('osTrends').getContext('2d');
var myLineChart = new Chart(osTrendsContext, {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
                fill: false,
                borderColor: "#3e95cd",
                data: [1, 2, 3, 4, 5]
            },
            {
                fill: false,
                borderColor: "#8e5ea2",
                data: [5, 4, 3, 2, 1]
            },
            {
                fill: false,
                borderColor: '#3cba9f',
                data: [1, 4, 3, 3, 4]
            }
        ]
    },
    options: {
        legend: {
            display: false
        }
    }
});

//---------- Vue Components To Hold State ---------
//Vue component for the Network Devices
//Number of network devices
var networkDevices = new Vue({
    el: '#networkDevices',
    data: {
        message: "Loading",
        date: "Last Updated: "
    }
})
//Number of online Devices
var onlineDevices = new Vue({
    el: '#onlineDevices',
    data: {
        message: "Loading",
        date: "Loading"
    }
})
//Number of Offline Devices
var offlineDevices = new Vue({
    el: '#offlineDevices',
    data: {
        message: "Loading",
        date: "Loading"
    }
})
//Most Popular OS 
var popularOS = new Vue({
    el: '#popularOS',
    data: {
        message: 'Loading',
        date: 'Loading'
    }
})
//Happiness rating
var happinessRating = new Vue({
    el: '#happinessRating',
    data: {
        message: 'Loading',
    }
})

// --------- Helper Functions ------------
//Reset the current info saved onto the page
function resetNetworkInformation() {
    networkInformation = {
        current: {
            meraki: {
                msCount: [0, 0], //Switches
                mxCount: [0, 0], //Firewalls
                mgCount: [0, 0], //Cellular Gateway
                mrCount: [0, 0], //Wireless
                merakiCount: 0,
                devices: {
                    online: 0,
                    offline: 0,
                    os: [0, 0, 0] //[Windows, Mac, Linux]
                }
            },
            dnac: {
                switchCount: [0, 0], //Switches
                apCount: [0, 0], //Access Points
                routerCount: [0, 0], //Routers
                wlcCount: [0, 0], //wireless LAN controller
                ciscoCount: 0,
                devices: {
                    online: 0,
                    offline: 0,
                    os: [0, 0, 0] //[Windows, Mac, Linux]
                }
            }

        }
    };
    renderPage();
};

//Function to format the date into a readable format
//E.G. Input : 202004181020
//E.G. Output : 10:20 18/04 
function formatDate(dateString) {
    //If a date gets passed in that's undefined, returned nothing
    if (dateString === undefined) {
        return;
    }
    //split the string up
    let SplitString = dateString.split('')
    let year = SplitString[0] + SplitString[1] + SplitString[2] + SplitString[3]
    let month = SplitString[4] + SplitString[5]
    let day = SplitString[6] + SplitString[7]
    let hour = SplitString[8] + SplitString[9]
    let minute = SplitString[10] + SplitString[11]

    //return hh:mm day/month
    return (hour + ':' + minute + ' ' + day + '/' + month)
}

//Function to find the most popular OS
//Input : Nested Array
//Output: String with OS
function findPopularOS(arr) {
    //holds the most popular os
    let currentOS = ""
    //max amount of deices
    let currentCounter = 0;
    //Loop through the array
    for (let i = 0; i < arr.length; i++) {
        //If the current device amount is higher than previous found
        if (arr[i][0] > currentCounter) {
            //update the highest amount
            currentCounter = arr[i][0]
            //set the most popular os depending on index
            if (i == 0) {
                currentOS = 'Windows'
            }
            if (i == 1) {
                currentOS = 'Mac'
            }
            if (i == 2) {
                currentOS = 'Linux'
            }
        }
    }
    return currentOS;
}

//Function which returns sorted keys of a JSON object passed in
function getSortedKeys(object) {
    //returns a sorted array of dates, from oldest to newest
    return Object.keys(object).sort();
}

//Function gets value of newest value in object
function getLatestInfo(object) {
    //get an arr of all the keys in the object sorted
    let sortedKeys = getSortedKeys(object);
    //finds the newest datapoint in the object 
    let lastIndex = sortedKeys[(sortedKeys.length) - 1];

    // Index 0 : Num of Devices, Index 1: Timestamp of when that was taken
    return [object[lastIndex], lastIndex];
}

//Function gets the five latest values of an object
function getLatestFiveEntries(object) {
    //get an arr of all the keys in the object sorted
    let sortedKeys = getSortedKeys(object);

    let listOfData = [
        [],
        []
    ]
    listOfData[0].push(object[sortedKeys[(sortedKeys.length) - 1]]);
    listOfData[0].push(object[sortedKeys[(sortedKeys.length) - 2]]);
    listOfData[0].push(object[sortedKeys[(sortedKeys.length) - 3]]);
    listOfData[0].push(object[sortedKeys[(sortedKeys.length) - 4]]);
    listOfData[0].push(object[sortedKeys[(sortedKeys.length) - 5]]);

    listOfData[1].push(formatDate(sortedKeys[(sortedKeys.length) - 1]));
    listOfData[1].push(formatDate(sortedKeys[(sortedKeys.length) - 2]));
    listOfData[1].push(formatDate(sortedKeys[(sortedKeys.length) - 3]));
    listOfData[1].push(formatDate(sortedKeys[(sortedKeys.length) - 4]));
    listOfData[1].push(formatDate(sortedKeys[(sortedKeys.length) - 5]));

    console.log(listOfData)
    // Index 0 : Num of Devices, Index 1: Timestamp of when that was taken
    return listOfData;
}

//function to toggle the top bar 
function toggleTopRow(){
    $( ".topRow" ).fadeToggle(200);
}

//function to toggle the bottom bar 
function toggleBottomRow(){
    $( ".bottomRow" ).fadeToggle(200);
}

/// ------- AZURE BELOW ------

let baseURL = 'https://westcentralus.api.cognitive.microsoft.com/face/v1.0/detect'
let key1 = '0c18352615074f4fae7f61b82ba78660'
let key2 = 'e5254bdadbe3464aa6fd48943b5964d8'


function processImage() {

    // Request parameters.
    var params = {
        "returnFaceId": "true",
        "returnFaceLandmarks": "false",
        "returnFaceAttributes": "age,gender,headPose,smile,facialHair,glasses,emotion," +
            "hair,makeup,occlusion,accessories,blur,exposure,noise"
    };

    // Display the image.
    var sourceImageUrl = document.getElementById("inputImage").value;


    // Perform the REST API call.
    $.ajax({
            url: baseURL + "?" + $.param(params),

            // Request headers.
            beforeSend: function (xhrObj) {
                xhrObj.setRequestHeader("Content-Type", "application/json");
                xhrObj.setRequestHeader("Ocp-Apim-Subscription-Key", key1);
            },

            type: "POST",

            // Request body.
            data: '{"url": ' + '"' + sourceImageUrl + '"}'
        })

        .done(function (data) {
            // Show formatted JSON on webpage.
            console.log(data[0].faceAttributes)
            numOfDevicesChart.data.datasets[0].data[0] = data[0].faceAttributes.emotion.happiness * 100;
            numOfDevicesChart.data.datasets[0].data[1] = data[0].faceAttributes.emotion.sadness * 100;
            numOfDevicesChart.data.datasets[0].data[2] = data[0].faceAttributes.emotion.neutral * 100;

            happinessRating.message = Math.floor(data[0].faceAttributes.emotion.happiness * 100) + '%';
            numOfDevicesChart.update();
        })

        .fail(function (jqXHR, textStatus, errorThrown) {
            // Display error message.
            var errorString = (errorThrown === "") ?
                "Error. " : errorThrown + " (" + jqXHR.status + "): ";
            errorString += (jqXHR.responseText === "") ?
                "" : (jQuery.parseJSON(jqXHR.responseText).message) ?
                jQuery.parseJSON(jqXHR.responseText).message :
                jQuery.parseJSON(jqXHR.responseText).error.message;
            alert(errorString);
        });
};



// ------------   Unused function -------------

//Function to get the value the update before the current
//NOT CURRENTLY USED
function getDayBefore(object) {

    let sortedKeys = getSortedKeys(object);
    let lastIndex = sortedKeys[(sortedKeys.length) - 2];
    return object[lastIndex];
}

//Function to calcualte percentage change of two values
//NOT CURRENTLY USED
function calculatePercentageChange(previous, current) {
    //calculate the how much change has occured between the two numbers
    let increase = current - previous;
    //calculate the percentage increase/decrease of that change
    let percentageIncrease = (increase / previous) * 100;
    //return the percentageIncrease/Decrease
    return percentageIncrease;
}