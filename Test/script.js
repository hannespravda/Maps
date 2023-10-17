document.getElementById('file-input').addEventListener('change', handleFileUpload);

function handleFileUpload(event) {
  const file = event.target.files[0];
  const fileType = file.name.endsWith('.gpx') ? 'gpx' : 'geojson';

  const reader = new FileReader();

  reader.onload = function(e) {
    const content = e.target.result;
    if (fileType === 'gpx') {
      // Handle GPX file
      console.log('Handling GPX file:', content);
    } else if (fileType === 'geojson') {
      // Handle GeoJSON file
      console.log('Handling GeoJSON file:', content);
    }
  };

  reader.readAsText(file);
}
