// Create a map object
var myMap = L.map("map", {
  center: [38.915722, -77.037399],
  zoom: 12
});

// Add a tile layer
L.tileLayer("https://api.mapbox.com/styles/v1/{id}/tiles/{z}/{x}/{y}?access_token={accessToken}", {
  attribution: "© <a href='https://www.mapbox.com/about/maps/'>Mapbox</a> © <a href='http://www.openstreetmap.org/copyright'>OpenStreetMap</a> <strong><a href='https://www.mapbox.com/map-feedback/' target='_blank'>Improve this map</a></strong>",
  tileSize: 512,
  maxZoom: 18,
  zoomOffset: -1,
  id: "mapbox/streets-v11",
  accessToken: API_KEY
}).addTo(myMap);

// An array containing each city's name, location, and population
var cinemas = [{
  location: [38.902850, -77.061630],
  name: "AMC Georgetown 14",
  status: "Closed",
  screens: "14",
},
{
  location: [38.959690, -77.085730],
  name: "AMC Mazza Gallerie 7",
  status: "Open",
  screens: "7"
},
{
  location: [38.909995, -76.996220],
  name: "Angelika Pop-Up at Union Market",
  status: "Open",
  screens: "3"
},
{
  location: [38.899983, -76.987424],
  name: "Atlas Performing Arts Center",
  status: "Open",
  screens: "1"
},
{
  location: [38.917925, -77.023343],
  name: "Atlantic Plumbing Cinema",
  status: "Open",
  screens: "6"
},
{
  location: [38.965243, -77.076368],
  name: "Avalon Theatre",
  status: "Open",
  screens: "2"
},
{
  location: [38.896744, -77.027436],
  name: "E Street Cinema",
  status: "Open",
  screens: "8"
},
{
  location: [38.891119, -77.017567],
  name: "East Building Auditorium",
  status: "Open",
  screens: "1"
},
{
  location: [38.896136, -77.055433],
  name: "Family Theater",
  status: "Open",
  screens: "1"
},
{
  location: [38.930813, -77.032506],
  name: "Gala Hispanic Theatre",
  status: "Open",
  screens: "1"
},
{
  location: [38.915235, -77.021137],
  name: "Howard Theatre",
  status: "Open",
  screens: "1"
},
{
  location: [38.917446, -77.029010],
  name: "Lincoln Theatre",
  status: "Open",
  screens: "1"
},
{
  location: [38.888160, -77.019868],
  name: "Lockheed Martin IMAX Theater",
  status: "Open",
  screens: "1"
},
{
  location: [38.881689, -76.995344],
  name: "Miracle Theatre",
  status: "Open",
  screens: "1"
},
{
  location: [38.896357, -77.030499],
  name: "National Theatre",
  status: "Closed",
  screens: "1"
},
{
  location: [38.899290, -77.021002],
  name: "Regal Gallery Place Stadium 14",
  status: "Open",
  screens: "14"
},
{
  location: [38.896357, -77.030499],
  name: "National Theatre",
  status: "Closed",
  screens: "1"
},
{
  location: [38.928953, -77.037241],
  name: "Suns Cinema",
  status: "Open",
  screens: "1"
},
{
  location: [38.896509, -77.029182],
  name: "Warner Theatre",
  status: "Open",
  screens: "1"
},
{
  location: [38.905638, -77.050390],
  name: "West End Cinema",
  status: "Closed",
  screens: "3"
}
];

// Loop through the cities array and create one marker for each city, bind a popup containing its name and population add it to the map
cinemas.forEach(cinema => {

  coordinates = cinema['location'];
  name = cinema['name'];
  status = cinema['status'];
  screens = cinema['screens'];

  marker = L.marker(coordinates, {'title': name});
  marker.bindPopup(`<h5>${name}</h5> <hr/> <h5>Status: ${status}</h5> <hr/> <h5>Screens: ${screens}</h5>`)  
  marker.addTo(myMap);

});


