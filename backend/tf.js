const fs = require('fs');
const path = require('path');

const csvToGeoJSON = (csvData) => {
  const lines = csvData.split('\n');
  const headers = lines[0].split(',');
  const features = lines.slice(1).filter(line => line.trim() !== '').map((line, index) => {
    const [lat, lon, offset] = line.split(',');

    return {
      id: index.toString(),
      type: "Feature",
      properties: {
        lat: parseFloat(lat),
        lon: parseFloat(lon),
        offset: parseInt(offset, 10)  // Assuming offset is an integer
      },
      geometry: {
        type: "Point",
        coordinates: [parseFloat(lon), parseFloat(lat)]
      }
    };
  });

  return {
    type: "FeatureCollection",
    features: features
  };
};

// Load the CSV file
const loadCSVFile = (filename) => {
  const filePath = path.join(__dirname, filename);
  return fs.readFileSync(filePath, 'utf8');
};

// Load and process the CSV file
const csvData = loadCSVFile('./combined_output.csv');  // Change this to your input file name
const geoJSONOutput = csvToGeoJSON(csvData);

// Output the result
console.log(JSON.stringify(geoJSONOutput, null, 2));

// Optionally, save the output to a file
fs.writeFileSync('output.geojson', JSON.stringify(geoJSONOutput, null, 2));
