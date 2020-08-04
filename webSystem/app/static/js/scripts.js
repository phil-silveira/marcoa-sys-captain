/*
Autor: GKW Agro Tech
Titulares:
    GKW Agro Tech
    MarcoA Instalacao de Sistemas de Aquecimento Ltda
Create Date: 11/11/2019
Update Date: 19/11/2019
Versao: 1.1

Funcoes JavaScripts utilizadas pelo sistema Web Django.
*/

// Trecho que codigo responsabel por gerar os graficos de temperatura dinamicamente
// https://stackoverflow.com/questions/46438373/trying-to-get-multiple-chart-js-charts-to-load-on-the-same-page
function readTempDinamic() {
    var endpointTemp = '/api/weatherData/getSensor/1/'
    //console.log(endpointTemp);

    /* ############################################################################# */
    // Código para obter os dados meteorologicos de TEMPERATURA da API
    $.ajax({
        method: "GET",
        url: endpointTemp,
        success: function(data){
            generateGaugeCharts(data)
        },
        error: function(error_data){
            console.log("error")
            console.log(error_data)
        }
    })
    /* ############################################################################# */
}

/**
* Funcao para recarregar os graficos
*/
function refresh() {
	setTimeout( function() {
	  $('.piechart').fadeOut('slow').fadeIn('slow');
	  readTempDinamic()
	  refresh();
    }, 15000);
}

function addZero(i) {
  if (i < 10) {
    i = "0" + i;
  }
  return i;
}


/** Funcao responsavel por gerar os graficos de temperatura dinamicamente.
 * Os graficos utilizados na pagina rows_list
 */
function generateGaugeCharts(data) {
    var cont = 0
    var charts = document.getElementsByClassName("piechart")
    for (chart of charts) {
        var ctx = chart.getContext('2d')
        var temp = 0

        var idClass = charts[cont].id
        if (idClass == "myChart-" + (cont+1)) {
            read_date = data[cont].read_date[0]

            var dt = new Date(read_date);
            var h = addZero(dt.getHours());
            var m = addZero(dt.getMinutes());
            var s = addZero(dt.getSeconds());

            document.getElementById("datetime-" + (cont+1)).innerHTML = (("0"+dt.getDate()).slice(-2)) +"/"+ (("0"+(dt.getMonth()+1)).slice(-2)) +"/"+ (dt.getFullYear()) +"  " + h + ":" + m + ":" + s;
            temp = data[cont].value[0]
        }
        cont = cont + 1

        // Biblioteca para geracao desse tipo de grafico
        // https://github.com/kluverua/Chartjs-tsgauge
        new Chart(ctx, {
            type: "tsgauge",
            data: {
                datasets: [{
                    backgroundColor: ["#940fdc", "#0fdc63", "#0fdc63", "#dcd50f", "#fd9704", "#dc570f", "#dc0f0f"],
                    borderWidth: 0,
                    gaugeData: {
                        value: temp,
                        valueColor: "#ff7143"
                    },
                    gaugeLimits: [10, 15, 20, 25, 30, 35, 40]
                }]
            },
            options: {
                events: [],
                showMarkers: true
            }
        });
    }
}


/* ############################################################################### */
// Geracao do grafico da TEMPERATURA dos ultimos 60 min
function setChartTemp(data){
    var ctx = document.getElementById("chartTemp");
    console.log(data[0].date);
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Temperatura Observada",
                borderColor: "#3e95cd",
                fill: false
            },{
                data: data[1].value,
                label: "Temperatura Programada",
                borderColor: "#8e5ea2",
                fill: false
            },{
                data: data[2].value,
                label: "Temperatura Ambiente",
                borderColor: "#c45850",
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 25,
                        suggestedMax: 40
                    },
                    scaleLabel: {
                        display:     true,
                        labelString: 'Temperatura (˚C)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico das temperaturas dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico do CONSUMO das últimas 24 horas
function setChartConsum(data){
    var ctx = document.getElementById("chartConsum");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Consumo de energia",
                borderColor: "#3e95cd",
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 1000
                    },
                    scaleLabel: {
                        display:     true,
                        labelString: 'Consumo (watts)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico do consumo dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da Media do CONSUMO das últimos 30 dias
function setChartAvgDailyConsum(data){
    var ctx = document.getElementById("chartAvgDailyConsum");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data[0].date,
            datasets: [{
                label: "Consumo médio diário de energia",
                backgroundColor: 'rgba(0, 99, 132, 0.6)',
                borderColor: 'rgba(0, 99, 132, 1)',
                data: data[0].value,
            }]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    ticks: {
                        suggestedMin: 0,
                        suggestedMax: 1000
                    },
                    scaleLabel: {
                        display:     true,
                        labelString: 'Consumo (watts)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                            display:     true,
                            labelString: 'Histórico do consumo médio diário dos últimos 30 dias'
                    },
                    type: "time",
                    time: {
                        unit: 'day',
                        round: 'day',
                        displayFormats: {
                          day: 'D MMM'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */

/* ############################################################################### */
// Geracao do grafico da TEMPERATURA das últimas 60 min
function setChartReportTemp(data){
    console.log(data);
    var ctx = document.getElementById("chartTempReport");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)',
                fill: false
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)',
                fill: false
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)',
                fill: false
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)',
                fill: false
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Temperatura (˚C)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico das temperaturas observadas dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da TEMPERATURA PROGRAMADA das últimas 7 dias
function setChartReportProgTemp(data){
    var ctx = document.getElementById("chartProgTempReport");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)',
                fill: false
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)',
                fill: false
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)',
                fill: false
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)',
                fill: false
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Temperatura (˚C)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico das temperaturas programadas dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da TEMPERATURA AMBIENTE das últimas 24 horas
function setChartReportEnvTemp(data){
    var ctx = document.getElementById("chartEnvTempReport");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)',
                fill: false
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)',
                fill: false
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)',
                fill: false
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)',
                fill: false
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Temperatura (˚C)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico da temperatura ambiente dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da CONSUMO das últimas 24 horas
function setChartReportConsum(data){
    var ctx = document.getElementById("chartConsumReport");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)',
                fill: false
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)',
                fill: false
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)',
                fill: false
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)',
                fill: false
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Consumo (watts)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico do consumo de energia dos últimos 60 min'
                    },
                    type: 'time',
                    time: {
                        displayFormats: {
                            quarter: 'h:mm a'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */



/* ############################################################################### */
// Geracao do grafico da Media do CONSUMO diario dos últimos 30 dias
function setChartReportAvgDailyConsum(data){
    var ctx = document.getElementById("chartAvgDailyConsumReport");
    var myChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)'
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)'
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)'
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)'
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Consumo (watts)'
                    }
                }],
                xAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Histórico do consumo médio diário dos últimos 30 dias'
                    },
                    type: 'time',
                    time: {
                        unit: 'day',
                        round: 'day',
                        displayFormats: {
                          day: 'D MMM'
                        }
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da TEMPERATURA PROGRAMADA das últimas 7 dias
function setChartReportDimming(data){
    var ctx = document.getElementById("chartDimmingReport");
    var myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: data[0].date,
            datasets: [{
                data: data[0].value,
                label: "Ambiente 1",
                backgroundColor: 'rgba(148, 151, 247, 0.6)',
                borderColor: 'rgba(148, 151, 247, 1)',
                fill: false
            },{
                data: data[1].value,
                label: "Ambiente 2",
                backgroundColor: 'rgba(89, 179, 102, 0.6)',
                borderColor: 'rgba(89, 179, 102, 1)',
                fill: false
            },{
                data: data[2].value,
                label: "Ambiente 3",
                backgroundColor: 'rgba(230, 137, 83, 0.6)',
                borderColor: 'rgba(230, 137, 83, 1)',
                fill: false
            }/*,{
                data: data[3].value,
                label: "Ambiente 4",
                backgroundColor: 'rgba(243, 119, 171, 0.6)',
                borderColor: 'rgba(243, 119, 171, 1)',
                fill: false
            }*/]
        },
        options: {
            responsive: true,
            scales: {
                yAxes: [{
                    scaleLabel: {
                        display:     true,
                        labelString: 'Temperatura (˚C)'
                    }
                }],
                xAxes: [{
                    type: 'time',
                    time: {
                        unit: 'day'
                    }
                }]
            }
        }
    });
}
/* ############################################################################### */



/* ############################################################################### */
// Geracao do grafico da DIMMER das últimas 24 horas
function setChartDimming(labels, defaultData){
    var ctx = document.getElementById("chartDimming");
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Dimmer dos últimos quinze minutos',
            data: defaultData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display:     true,
                    labelString: 'Dimmer (%)'
                }
            }],
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'hA'
                    }
                }
            }]
        }
    }
});
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da TENSAO ELETRICA das últimas 24 horas
function setChartTension(labels, defaultData){
    var ctx = document.getElementById("chartTension");
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Tensão Elétrica dos últimos quinze minutos',
            data: defaultData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display:     true,
                    labelString: 'Tensão Elétrica (V)'
                }
            }],
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'hA'
                    }
                }
            }]
        }
    }
});
}
/* ############################################################################### */


/* ############################################################################### */
// Geracao do grafico da POTENCIA ELETRICA das últimas 24 horas
function setChartPotency(labels, defaultData){
    var ctx = document.getElementById("chartPotency");
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Potência Elétrica dos últimos quinze minutos',
            data: defaultData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display:     true,
                    labelString: 'Potência Elétrica (W)'
                }
            }],
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'hA'
                    }
                }
            }]
        }
    }
});
}
/* ############################################################################### */




/* ############################################################################### */
// Geracao do grafico da CORRENTE ELETRICA das últimas 24 horas
function setChartCurrent(labels, defaultData){
    var ctx = document.getElementById("chartCurrent");
    var myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: labels,
        datasets: [{
            label: 'Corrent Elétrica dos últimos quinze minutos',
            data: defaultData,
            backgroundColor: [
                'rgba(255, 99, 132, 0.2)',
                'rgba(54, 162, 235, 0.2)',
                'rgba(255, 206, 86, 0.2)',
                'rgba(75, 192, 192, 0.2)',
                'rgba(153, 102, 255, 0.2)',
                'rgba(255, 159, 64, 0.2)'
            ],
            borderColor: [
                'rgba(255,99,132,1)',
                'rgba(54, 162, 235, 1)',
                'rgba(255, 206, 86, 1)',
                'rgba(75, 192, 192, 1)',
                'rgba(153, 102, 255, 1)',
                'rgba(255, 159, 64, 1)'
            ],
            borderWidth: 1
        }]
    },
    options: {
        responsive: true,
        scales: {
            yAxes: [{
                scaleLabel: {
                    display:     true,
                    labelString: 'Corrente Elétrica (A)'
                }
            }],
            xAxes: [{
                type: 'time',
                time: {
                    displayFormats: {
                        quarter: 'hA'
                    }
                }
            }]
        }
    }
});
}
/* ############################################################################### */





$(function () {
  /* Functions */

  var loadFormTemp = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-ajust-temp-new .modal-content").html("");
        $("#modal-ajust-temp-new").modal("show");
      },
      success: function (data) {
        $("#modal-ajust-temp-new .modal-content").html(data.html_form);
      }
    });
  };

  var saveFormTemp = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //$("#book-table tbody").html(data.html_book_list);
          $("#modal-ajust-temp-new").modal("hide");
        }
        else {
          $("#modal-ajust-temp-new .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-ajust-temp-new").click(loadFormTemp);
  $("#modal-ajust-temp-new").on("submit", ".js-ajust-temp-new-form", saveFormTemp);

});


$(function () {
  /* Functions */

  var loadFormStatus = function () {
    var btn = $(this);
    $.ajax({
      url: btn.attr("data-url"),
      type: 'get',
      dataType: 'json',
      beforeSend: function () {
        $("#modal-ajust-status-new .modal-content").html("");
        $("#modal-ajust-status-new").modal("show");
      },
      success: function (data) {
        $("#modal-ajust-status-new .modal-content").html(data.html_form);
      }
    });
  };

  var saveFormStatus = function () {
    var form = $(this);
    $.ajax({
      url: form.attr("action"),
      data: form.serialize(),
      type: form.attr("method"),
      dataType: 'json',
      success: function (data) {
        if (data.form_is_valid) {
          //$("#book-table tbody").html(data.html_book_list);
          $("#modal-ajust-status-new").modal("hide");
        }
        else {
          $("#modal-ajust-status-new .modal-content").html(data.html_form);
        }
      }
    });
    return false;
  };


  /* Binding */

  // Create book
  $(".js-ajust-status-new").click(loadFormStatus);
  $("#modal-ajust-status-new").on("submit", ".js-ajust-status-new-form", saveFormStatus);

});