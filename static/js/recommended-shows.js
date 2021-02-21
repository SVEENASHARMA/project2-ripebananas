d3.json('/recommendations-data').then(data => {

  var rec = data.map(d => d['recommendation']);
  var count = data.map(d => d['count']);

  var trace1 = {
    x: rec,
    y: count,
    type: 'bar',
    text: rec,
    marker: {
      color: 'rgb(142,124,195)'
    }
  };
  
  var data = [trace1];
  
  var layout = {
    title: 'Recommended Shows',
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
  
  Plotly.newPlot('recommended-shows', data, layout);

});
