  //var csv is the CSV file with headers
  function csvJSON(csv) {

      var lines = csv.split("\n");

      var result = [];

      var headers = lines[0].split(",");

      for (var i = 1; i < lines.length; i++) {

          var obj = {};
          var currentline = lines[i].split(",");

          for (var j = 0; j < headers.length; j++) {
              obj[headers[j]] = currentline[j];
          }

          result.push(obj);

      }

      //return result; //JavaScript object
      return JSON.stringify(result); //JSON
  }

  function parseCSV(text) {
      let lines = text.split('\n');
      return lines.map(line => {
          // Por cada linea obtenemos los valores
          let values = line.split(',');
          return values;
      });
  }

  function readFile(evt) {
      let fileField1 = evt.target.files[0];
      let reader = new FileReader();
      let jason
      reader.onload = (e) => {
          // Cuando el archivo se terminó de cargar
          jason = csvJSON(e.target.result)
          let lines = parseCSV(e.target.result);
          //let output = reverseMatrix(lines);
          console.log(lines);
          console.log(lines.length)
          console.log(jason)
      };
      // Leemos el contenido del archivo seleccionado
      reader.readAsBinaryString(fileField1);
  }

  document.getElementById('fileField1').addEventListener('change', readFile, false);