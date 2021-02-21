d3.json('/services-data').then(data => {

  var service = data.map(d => d['service preferred by user']);
  var count = data.map(d => d['count']);

  var trace1 = {
    x: service,
    y: count,
    type: 'bar',
    text: count.map(String),
    marker: {
      color: 'rgb(142,124,195)'
    }
  };
  
  var data = [trace1];
  
  var layout = {
    title: 'Preferred Services Today',
    // font:{
    //   family: 'Raleway, sans-serif'
    // },
    showlegend: false,
    xaxis: {
      tickangle: -45
    },
    yaxis: {
      zeroline: false,
      gridwidth: 2
    },
    bargap :0.05
  };
  
  Plotly.newPlot('preferred-services', data, layout);

});