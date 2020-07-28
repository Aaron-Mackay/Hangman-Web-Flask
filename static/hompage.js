var existingLists = {{ fileList| tojson }};
  var regex = RegExp('[^a-zA-Z 0-9\n]');

  function checkInput() {
    var phrases = document.querySelector("#phrases").value.split("\n");
    var count = 0;
    var listName = document.querySelector('#listName').value;
    var phrases = document.querySelector('#phrases').value
    for (i = 0; i < phrases.length; i++) {
      if (phrases[i].trim() != "") {
        count++;
      }
    }
    if (listName === '' || phrases === '') {
      document.querySelector('#submit').disabled = true;
    } else if (existingLists.includes(document.querySelector('#listName').value.trim().toLowerCase())) {
      document.getElementById("errorInfo").innerHTML = "List name already in use";
      document.querySelector('#submit').disabled = true;
    } else if (count < 5) {
      document.getElementById("errorInfo").innerHTML = "Please enter at least 5 words or phrases";
      document.querySelector("#submit").disabled = true;
    } else if (regex.test(listName) || regex.test(phrases)) {
      document.getElementById("errorInfo").innerHTML = "Letters, numbers and spaces only";
      document.querySelector("#submit").disabled = true;
    } else {
      document.getElementById("errorInfo").innerHTML = "";
      document.querySelector('#submit').disabled = false;
    }
  }

  function showScoreboard(list) {
    gtag('event', 'OpenScoreboard');
    document.querySelector('.scoreboard').classList.add('opened');
    $(function () {
      $.getJSON('/background_process', {
        list: list,
      }, function (data) {
        let table = document.querySelector("table");
        let header = ["Player", "Highscore"]

        while (table.rows.length > 0) {
          table.deleteRow(0);
        }
        if (data.result.length == 0) {
          $('#debug1').text("No data");
          $('#debug2').text("");
          $('#debug3').text("");;
          $('#debug4').text("");;
        } else {
          $('#debug1').text("");
          generateTable(table, data.result);
          generateTableHead(table, header);

        }
      });
      return false;
    });
  }

  function generateTableHead(table, data) {
    let thead = table.createTHead();
    let row = thead.insertRow();
    for (let key of data) {
      let th = document.createElement("th");
      let text = document.createTextNode(key);
      th.appendChild(text);
      row.appendChild(th);
    }
  }

  function generateTable(table, data) {
    for (let element of data) {
      let row = table.insertRow();
      for (key in element) {
        let cell = row.insertCell();
        let text = document.createTextNode(element[key]);
        cell.appendChild(text);
      }
    }
  }